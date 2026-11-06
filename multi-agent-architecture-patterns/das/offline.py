"""
Scripted LLM replies for Priya's scenario, so the full flow runs without Nexus (--offline, and the tests).

The agents, gateway, guardrails, data and handoffs are all real; only the model's
decisions are replayed. A live run (Nexus) makes these decisions itself.
"""

from das.llm import ScriptedLLM, reply

REQUEST = ("I uploaded 20 invoices yesterday but I can't find invoice 1240 in Finance. If it got rejected, "
           "tell me why and get me access to the Compliance archive to re-upload it there.")
FOLLOW_UP = "Is it approved yet?"

ON_TOPIC = reply({"on_topic": True, "reason": "archive upload, rejection and access question"})


def happy_path_script(with_follow_up: bool = True) -> dict:
    script = {
        "InputGuardrail": [ON_TOPIC],
        "Coordinator": [
            reply(None, ("call_search_agent", {"invoice_id": "1240", "workspace": "Finance"}),
                  ("call_debugger_agent", {"invoice_id": "1240", "batch_date": "2026-10-29"})),
            reply(None, ("handoff_to_access_agent", {
                "invoice_id": "1240", "batch_id": "BATCH-2026-10-29-001", "reason_code": "CLS-COMPLIANCE",
                "target_workspace": "Compliance", "permission": "upload",
                "justification": "Re-upload invoice 1240, rejected from Finance as import VAT evidence (CLS-COMPLIANCE)."})),
            reply("I checked both things for you.\n"
                  "• Invoice 1240 is not in the Finance archive.\n"
                  "• Yesterday's batch BATCH-2026-10-29-001 archived 19 of your 20 invoices. Invoice 1240 was rejected "
                  "with reason CLS-COMPLIANCE: the classifier recognised it as import VAT evidence (a customs "
                  "declaration is attached), and that kind of tax evidence must be filed in the Compliance archive.\n"
                  "Next step: I've handed your access request and the re-upload to the Compliance team's Access & "
                  "policy agent. It owns this from here and will notify you directly when it's done."),
        ],
        "A·Search": [
            reply(None, ("search_archive", {"query": "1240", "workspace": "Finance"})),
            reply({"doc_id": "1240", "workspace": "Finance", "exists": False, "has_access": True,
                   "note": "No record 1240 in the Finance archive; the user has read access to Finance."}),
        ],
        "B·Debugger": [
            reply(None, ("get_batch_status", {"batch_date": "2026-10-29"})),
            reply(None, ("get_validation_log", {"batch_id": "BATCH-2026-10-29-001", "doc_id": "1240"})),
            reply(None, ("get_reason_code_doc", {"reason_code": "CLS-COMPLIANCE"})),
            reply(None, ("consult_search_exists", {"doc_id": "1240", "workspace": "Finance"})),
            reply({"batch_id": "BATCH-2026-10-29-001", "status": "rejected", "reason_code": "CLS-COMPLIANCE",
                   "fault": False,
                   "explanation": "19/20 archived; 1240 rejected at classification as import VAT evidence. It belongs "
                                  "in the Compliance archive (target workspace: Compliance). User-fixable: get "
                                  "Compliance upload access and re-upload there. Re-checked with A: still not in Finance."}),
        ],
        "C·Access": [
            reply(None, ("check_entitlement", {"workspace": "Compliance", "permission": "upload"})),
            reply(None, ("create_access_request", {
                "workspace": "Compliance", "permission": "upload",
                "justification": "Re-upload invoice 1240 (import VAT evidence) rejected from Finance with CLS-COMPLIANCE."})),
            reply(None, ("get_access_request_status", {"request_id": "REQ-1001"})),
            reply(None, ("call_reupload_agent", {"doc_id": "1240", "target_workspace": "Compliance",
                                                 "request_id": "REQ-1001"})),
            reply(None, ("notify_user", {"message":
                "Hello Priya, this is the Compliance team's Access & policy agent. Your request REQ-1001 for upload "
                "access to the Compliance archive was approved by the data owner. Invoice 1240 passed pre-validation "
                "and is now archived in Compliance (folder Compliance/VAT-Evidence/2026)."})),
            reply({"request_id": "REQ-1001", "access": "granted", "reupload_status": "archived in Compliance",
                   "notified": True}),
        ],
        "D·Reupload": [
            reply(None, ("prevalidate", {"doc_id": "1240", "target_workspace": "Compliance"})),
            reply(None, ("upload_record", {"doc_id": "1240", "target_workspace": "Compliance"})),
            reply({"doc_id": "1240", "workspace": "Compliance", "prevalidation": "passed", "status": "archived",
                   "detail": "All Compliance archive rules passed; archived in Compliance/VAT-Evidence/2026."}),
        ],
    }
    if with_follow_up:
        script["InputGuardrail"].append(reply({"on_topic": True, "reason": "follow-up on the archive access request"}))
        script["Coordinator"] += [
            reply(None, ("get_access_request_status", {"request_id": "REQ-1001"})),
            reply("Yes. REQ-1001 was approved by the Compliance data owner, and invoice 1240 is now archived in "
                  "the Compliance archive. The Compliance team owns this request, so any further updates come from them."),
        ]
    return script


def offline_llm(with_follow_up: bool = True) -> ScriptedLLM:
    return ScriptedLLM(happy_path_script(with_follow_up))
