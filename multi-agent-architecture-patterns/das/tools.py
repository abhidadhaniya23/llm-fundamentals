"""
Enterprise-system tools behind the gateway. Each call runs as the signed-in user (ctx.user):
ownership checks happen here, so no agent can read another user's batches or requests.
"""

from das.gateway import Tool, ToolContext, ToolError
from das.schema import BATCH_ID, DATE, DOC_ID, PERMISSION, REASON_CODE, REQUEST_ID, STR, WORKSPACE, obj
from das.trace import tracer


def _require(ctx: ToolContext, workspace: str, permission: str) -> None:
    if not ctx.state.can(ctx.user.user_id, workspace, permission):
        raise ToolError("access_denied", f"{ctx.user.user_id} has no {permission} access to the {workspace} archive")


# --- archive storage + metadata/search index (agent A) ---------------------------------

def search_archive(ctx: ToolContext, args: dict) -> dict:
    _require(ctx, args["workspace"], "read")
    terms = [term for term in args["query"].lower().split() if len(term) > 2]
    matches = [{key: doc[key] for key in ("doc_id", "title", "folder", "archived_on")}
               for doc in ctx.state.documents()
               if doc["workspace"] == args["workspace"]
               and any(term in f"{doc['doc_id']} {doc['title']}".lower() for term in terms)]
    return {"workspace": args["workspace"], "query": args["query"], "count": len(matches), "matches": matches}


def get_record(ctx: ToolContext, args: dict) -> dict:
    doc = ctx.state.find_document(args["doc_id"])
    if doc is None:
        return {"doc_id": args["doc_id"], "exists": False}
    if not ctx.state.can(ctx.user.user_id, doc["workspace"], "read"):
        return {"doc_id": args["doc_id"], "exists": True, "has_access": False}
    return {"doc_id": args["doc_id"], "exists": True, "has_access": True, "record": doc}


def exists_in(ctx: ToolContext, doc_id: str, workspace: str) -> bool:
    return ctx.state.find_document(doc_id, workspace) is not None


# --- ingestion pipeline + validation log + policy KB (agent B) -------------------------

def _own_batch(ctx: ToolContext, batch_id: str) -> dict:
    batch = next((b for b in ctx.state.store.batches if b["batch_id"] == batch_id), None)
    if batch is None or batch["uploader"] != ctx.user.user_id:
        raise ToolError("not_found", f"no batch {batch_id} uploaded by {ctx.user.user_id}")
    return batch


def get_batch_status(ctx: ToolContext, args: dict) -> dict:
    batches = [b for b in ctx.state.store.batches
               if b["uploader"] == ctx.user.user_id and b["uploaded_on"] == args["batch_date"]]
    return {"batch_date": args["batch_date"], "uploader": ctx.user.user_id, "batches": [
        {"batch_id": b["batch_id"], "workspace": b["workspace"], "files_total": b["files_total"],
         "archived": sum(f["status"] == "archived" for f in b["files"]),
         "rejected": [f["doc_id"] for f in b["files"] if f["status"] == "rejected"],
         "files": b["files"]} for b in batches]}


def get_validation_log(ctx: ToolContext, args: dict) -> dict:
    _own_batch(ctx, args["batch_id"])
    entries = [e for e in ctx.state.store.validation_log
               if e["batch_id"] == args["batch_id"] and e["doc_id"] == args["doc_id"]]
    return {"batch_id": args["batch_id"], "doc_id": args["doc_id"], "entries": entries}


def get_reason_code_doc(ctx: ToolContext, args: dict) -> dict:
    entry = ctx.state.store.reason_codes.get(args["reason_code"])
    if entry is None:
        raise ToolError("unknown_reason_code", f"{args['reason_code']} is not in the rejection-code catalogue")
    return {"reason_code": args["reason_code"], **entry}


def consult_search_exists(ctx: ToolContext, args: dict) -> dict:
    """Bounded consult B → A: one structured question, no free text, reported upward."""
    tracer().event("CONSULT", "A·Search (consult)", f"exists({args['doc_id']}, {args['workspace']})")
    answer = {"exists": exists_in(ctx, args["doc_id"], args["workspace"])}
    ctx.run.setdefault("consults", []).append({"to": "A·Search", "question": dict(args), "answer": answer})
    return answer


def consult_once(ctx: ToolContext, args: dict) -> str | None:
    return "bounded consult: only one question to A per DebuggerAgent run" if ctx.run.get("consults") else None


# --- IAM + ITSM access workflow (agent C) ---------------------------------------------

def check_entitlement(ctx: ToolContext, args: dict) -> dict:
    return {"user_id": ctx.user.user_id, "workspace": args["workspace"], "permission": args["permission"],
            "granted": ctx.state.can(ctx.user.user_id, args["workspace"], args["permission"]),
            "roles": ctx.state.roles(ctx.user.user_id)}


def create_access_request(ctx: ToolContext, args: dict) -> dict:
    entitlements = ctx.state.store.entitlements
    if ctx.state.can(ctx.user.user_id, args["workspace"], args["permission"]):
        raise ToolError("already_entitled", "the user already has this access")
    role = entitlements["grantable"].get(f"{args['workspace']}:{args['permission']}")
    if role is None:
        raise ToolError("not_requestable", f"{args['permission']} on {args['workspace']} cannot be requested")
    request = {"request_id": ctx.state.next_id("REQ"), "user_id": ctx.user.user_id, "workspace": args["workspace"],
               "permission": args["permission"], "role": role, "justification": args["justification"],
               "status": "pending_approval", "routed_to": entitlements["data_owners"][args["workspace"]],
               "created_on": ctx.bot.today.isoformat()}
    with ctx.state.lock:
        ctx.state.access_requests[request["request_id"]] = request
        ctx.session.open_request_id = request["request_id"]
    tracer().event("SIM", "ITSM", f"{request['request_id']} created, routed to data owner {request['routed_to']}")
    return dict(request)


def get_access_request_status(ctx: ToolContext, args: dict) -> dict:
    request = ctx.state.access_requests.get(args["request_id"])
    if request is None or request["user_id"] != ctx.user.user_id:
        raise ToolError("not_found", f"no access request {args['request_id']} for {ctx.user.user_id}")
    if request["status"] == "pending_approval":  # approval is simulated: the owner approves right away
        with ctx.state.lock:
            request.update(status="approved", approved_by=request["routed_to"], approved_on=ctx.bot.today.isoformat())
            ctx.state.grant(request["user_id"], request["role"])
        tracer().event("SIM", "ITSM", f"data owner {request['routed_to']} approved {request['request_id']} "
                                      f"(simulated); IAM granted {request['role']} to {request['user_id']}")
    return dict(request)


# --- re-upload into the Compliance archive (agent D) -----------------------------------

def prevalidate(ctx: ToolContext, args: dict) -> dict:
    staged = next((f for f in ctx.state.store.staging
                   if f["doc_id"] == args["doc_id"] and f["uploaded_by"] == ctx.user.user_id), None)
    if staged is None:
        raise ToolError("not_found", f"no staged file {args['doc_id']} uploaded by {ctx.user.user_id}")
    rules = ctx.state.store.archive_rules[args["target_workspace"]]
    checks = [{"check": "document_class", "value": staged["document_class"],
               "passed": staged["document_class"] in rules["accepted_classes"]}]
    checks += [{"check": f"required:{name}", "passed": bool(staged.get(name))} for name in rules["required_fields"]]
    passed = all(check["passed"] for check in checks)
    ctx.run.setdefault("prevalidated", {})[args["doc_id"]] = passed
    return {"doc_id": args["doc_id"], "target_workspace": args["target_workspace"], "passed": passed, "checks": checks}


def upload_allowed(ctx: ToolContext, args: dict) -> str | None:
    if not ctx.run.get("prevalidated", {}).get(args["doc_id"]):
        return "prevalidate must pass for this file before upload_record"
    if not ctx.state.can(ctx.user.user_id, args["target_workspace"], "upload"):
        return f"{ctx.user.user_id} has no upload access to {args['target_workspace']} (approval missing)"
    return None


def upload_record(ctx: ToolContext, args: dict) -> dict:
    staged = next(f for f in ctx.state.store.staging if f["doc_id"] == args["doc_id"])
    rules = ctx.state.store.archive_rules[args["target_workspace"]]
    today = ctx.bot.today
    record = {"doc_id": staged["doc_id"], "title": staged["title"], "type": staged["type"],
              "workspace": args["target_workspace"],
              "folder": rules["folder"].format(year=today.year, quarter=(today.month - 1) // 3 + 1),
              "platform": "CSP", "owner": ctx.state.store.entitlements["data_owners"][args["target_workspace"]],
              "retention_class": rules["retention_class"], "archived_on": today.isoformat(),
              "delete_after": f"{today.year + 10}-12-31"}
    with ctx.state.lock:
        ctx.state.uploaded.append(record)
    return {"status": "archived", "record": record}


# --- ITSM incident (handoff target E, humans) ------------------------------------------

def open_incident(ctx: ToolContext, args: dict) -> dict:
    incident = {"incident_id": ctx.state.next_id("INC"), "assigned_to": "platform-team", "status": "open",
                "summary": args["summary"], "invoice_id": args["invoice_id"], "batch_id": args["batch_id"],
                "reason_code": args["reason_code"], "reported_for": ctx.user.user_id}
    with ctx.state.lock:
        ctx.state.incidents[incident["incident_id"]] = incident
        ctx.session.incident_id = incident["incident_id"]
    return dict(incident)


SYSTEM_TOOLS = [
    Tool("search_archive", "Search one archive workspace by document id or title words (exact metadata match).",
         obj(query=STR, workspace=WORKSPACE), search_archive),
    Tool("get_record", "Fetch one archived record by document id, if the user may see it.",
         obj(doc_id=DOC_ID), get_record),
    Tool("get_batch_status", "List the current user's ingestion batches uploaded on a date, with per-file status.",
         obj(batch_date=DATE), get_batch_status),
    Tool("get_validation_log", "Validation-log entries for one file in one of the user's batches.",
         obj(batch_id=BATCH_ID, doc_id=DOC_ID), get_validation_log),
    Tool("get_reason_code_doc", "Plain-language explanation of a rejection reason code from the policy knowledge base.",
         obj(reason_code=REASON_CODE), get_reason_code_doc),
    Tool("consult_search_exists", "Bounded consult: ask the Search agent ONE question, whether doc_id exists in a "
         "workspace. Returns only {exists}. Allowed once.", obj(doc_id=DOC_ID, workspace=WORKSPACE),
         consult_search_exists, kind="consult", precondition=consult_once),
    Tool("check_entitlement", "Check whether the user holds a permission on an archive workspace.",
         obj(workspace=WORKSPACE, permission=PERMISSION), check_entitlement),
    Tool("create_access_request", "Raise an ITSM access request, routed to the workspace's data owner for approval.",
         obj(workspace=WORKSPACE, permission=PERMISSION, justification=STR), create_access_request, write=True),
    Tool("get_access_request_status", "Current status of one of the user's access requests.",
         obj(request_id=REQUEST_ID), get_access_request_status),
    Tool("prevalidate", "Check the user's staged (held) file against the target archive's rules before upload.",
         obj(doc_id=DOC_ID, target_workspace=WORKSPACE), prevalidate),
    Tool("upload_record", "Archive the pre-validated staged file in the target workspace.",
         obj(doc_id=DOC_ID, target_workspace=WORKSPACE), upload_record, write=True, precondition=upload_allowed),
    Tool("open_incident", "Open a platform incident ticket for a system fault.",
         obj(invoice_id=DOC_ID, batch_id=BATCH_ID, reason_code=REASON_CODE, summary=STR), open_incident, write=True),
]
