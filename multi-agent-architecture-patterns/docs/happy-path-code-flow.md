# DAS happy path: code flow wiki

How Priya's request travels through the code in `das/`, file by file, class by class, with the contract
(schema) at every hop. Source of truth: the code in `das/` and one run of
`.venv\Scripts\python.exe main.py --offline --no-color` (scenario date 2026-10-30).

## 1. Scenario

- **User**: Priya, Finance Analyst, user id `priya`, roles `Finance-Reader`, `Finance-Uploader` (`data/entitlements.json`).
- **Request** (`das/offline.py` `REQUEST`):
  "I uploaded 20 invoices yesterday but I can't find invoice 1240 in Finance. If it got rejected, tell me why
  and get me access to the Compliance archive to re-upload it there."
- **Follow-up** (`das/offline.py` `FOLLOW_UP`): "Is it approved yet?"
- **Outcome**: 1240 is not in Finance; batch `BATCH-2026-10-29-001` archived 19 of 20, 1240 rejected with
  `CLS-COMPLIANCE`; access request `REQ-1001` created and approved (simulated); 1240 archived in
  `Compliance/VAT-Evidence/2026`; Priya gets two chat messages (Coordinator, then C·Access).
- **Offline mode**: only the model decisions are replayed (`ScriptedLLM`). Agents, gateway, guardrails,
  tools and data are the real code.

Run numbers (first request): 20 LLM calls, 15 tool calls, 6 agents/roles active, 0 blocked, 2 messages to the user.

## 2. Two call types

- **M (Manager-style call)**: a tool whose `fn` runs another `Agent.run()` and returns its output. Control returns
  to the caller. Used by Coordinator → A, Coordinator → B, C → D. `Tool.kind = "agent"`.
- **H (Handoff)**: a tool that appends a `Baton` to `DASChatbot.pending_handoffs` and returns at once. Control and
  ownership move; the Coordinator never sees the outcome. Used by Coordinator → C. `Tool.kind = "handoff"`.
- **Consult**: B asks A one structured question (`consult_search_exists`), allowed once (`consult_once`), reported
  upward in B's `consults`. `Tool.kind = "consult"`.

## 3. Files and classes

| File | Class / function | Role in the flow |
|---|---|---|
| `main.py` | `main()` | Parses args, installs `Tracer`, builds `offline_llm()` or `NexusClient`, creates `DASChatbot`, calls `bot.handle(text)` per message |
| `das/config.py` | `LLMSettings`, `llm_settings()`, `scenario_today()` | Env-only settings (`LLM_FAST_*`); key never printed; scenario date `2026-10-30` |
| `das/runtime.py` | `DASChatbot` | One session: `handle()` → `_input_guardrails()` → `COORDINATOR.run()` → `_deliver_checked()` → `_dispatch_handoffs()` |
| `das/guardrails.py` | `detect_injection`, `redact_pii`, `check_topic`, `check_output`, `sanitize`, `collect_ids`, `extract_json` | Input checks, output checks, tool-result sanitising, id tracking |
| `das/agent.py` | `Agent` (`run`, `resume`, `_loop`, `_execute`), `AgentError` | The LLM tool-calling loop every agent uses; parallel tool calls; output-schema validation with one repair |
| `das/llm.py` | `LLMClient` (Protocol), `NexusClient`, `ScriptedLLM`, `LLMReply`, `ToolCall`, `reply()` | Model access; `ScriptedLLM` replays per-agent queues |
| `das/offline.py` | `happy_path_script()`, `offline_llm()` | The scripted model decisions for this scenario |
| `das/team.py` | `COORDINATOR`, `SEARCH`, `DEBUGGER`, `ACCESS`, `REUPLOAD`, `Baton`, `TEAM_TOOLS`, `ALLOWLISTS`, `build_gateway()` | Agent definitions, prompts, output schemas, M/H tools, preconditions, allowlists |
| `das/gateway.py` | `Gateway`, `Tool`, `ToolContext`, `ToolError`, `auto_confirm` | The one door to tools: allowlist, arg schema, precondition, write confirm, sanitise, audit |
| `das/tools.py` | `SYSTEM_TOOLS` + one function per tool | Enterprise-system tools, run as the signed-in user |
| `das/schema.py` | `validate()`, `obj()`, `STR`, `DOC_ID`, `BATCH_ID`, … | JSON-Schema subset: same schema sent to the LLM and enforced by the gateway |
| `das/store.py` | `DataStore`, `RuntimeState`, `UserContext`, `SessionMemory` | Read-only `data/*.json`, in-memory changes, SSO user, Coordinator memory |
| `das/trace.py` | `Tracer`, `tracer()`, `install()` | Every hop printed; milestones and per-agent counters for the FLOW SUMMARY |

## 4. Agents

| Agent (`das/team.py`) | Step | Output schema | Allowlisted tools | max_steps |
|---|---|---|---|---|
| `COORDINATOR` "Coordinator" | ③ | none (plain text reply) | `call_search_agent`, `call_debugger_agent`, `handoff_to_access_agent`, `handoff_to_platform_team`, `get_access_request_status` | 8 |
| `SEARCH` "A·Search" | ④ | `SEARCH_OUT` | `search_archive`, `get_record` | 5 |
| `DEBUGGER` "B·Debugger" | ⑤ | `DEBUG_OUT` | `get_batch_status`, `get_validation_log`, `get_reason_code_doc`, `consult_search_exists` | 8 |
| `ACCESS` "C·Access" | ⑥ | `ACCESS_OUT` | `check_entitlement`, `create_access_request`, `get_access_request_status`, `call_reupload_agent`, `notify_user` | 10 |
| `REUPLOAD` "D·Reupload" | ⑦ | `REUPLOAD_OUT` | `prevalidate`, `upload_record` | 5 |
| `PLATFORM` "E·Platform team" | E | n/a (humans) | `open_incident` | n/a, not used on the happy path |

## 5. Contracts

### 5.1 Core interfaces

- `LLMClient.chat(agent: str, messages: list[dict], tools: list[dict] | None) -> LLMReply` (`das/llm.py`)
- `LLMReply(content: str | None, tool_calls: list[ToolCall], prompt_tokens: int, completion_tokens: int)`
- `ToolCall(id: str, name: str, arguments: dict, raw_arguments: str)`
- `Agent.run(bot, brief, ctx=None, history=None) -> (output, messages, ctx)` (`das/agent.py`)
- `Agent.resume(bot, messages, ctx, note) -> output`
- `Tool(name, description, parameters: dict, fn: (ToolContext, dict) -> dict, kind, write, precondition: (ToolContext, dict) -> str | None)` (`das/gateway.py`)
- `Gateway.call(ctx: ToolContext, name: str, args: dict) -> dict`; a refusal is `{"error": code, "message": ...}`
- `ToolContext(bot, agent, run: dict)`; properties `user`, `state`, `session`
- `DASChatbot.handle(text: str) -> list[(sender, text)]` (`das/runtime.py`)
- `Baton(target, invoice_id, batch_id, reason_code, user, reply_owner, notifies_next, request)` (`das/team.py`)

### 5.2 Agent output schemas (`das/team.py`)

- `SEARCH_OUT`: required `doc_id`, `workspace`, `exists: bool`, `has_access: bool`; optional `note`.
- `DEBUG_OUT`: required `batch_id: str|null`, `status`, `reason_code: str|null`, `fault: bool`, `explanation` (≤1500); optional `consults: array`.
- `ACCESS_OUT`: required `request_id: str|null`, `access ∈ {granted, already_had, pending, rejected}`, `reupload_status`, `notified: bool`.
- `REUPLOAD_OUT`: required `doc_id`, `workspace`, `prevalidation ∈ {passed, failed}`, `status ∈ {archived, not_uploaded}`; optional `detail`.

All built with `obj()`, so `additionalProperties: false`.

### 5.3 Tool argument schemas used on the happy path

| Tool | File | Kind | Args | Write | Precondition |
|---|---|---|---|---|---|
| `call_search_agent` | team.py | agent (M) | `invoice_id: DOC_ID`, `workspace: WORKSPACE` | no | none |
| `call_debugger_agent` | team.py | agent (M) | `invoice_id: DOC_ID`, `batch_date: DATE` | no | none |
| `search_archive` | tools.py | tool | `query: STR`, `workspace: WORKSPACE` | no | none (checks read access inside) |
| `get_batch_status` | tools.py | tool | `batch_date: DATE` | no | none |
| `get_validation_log` | tools.py | tool | `batch_id: BATCH_ID`, `doc_id: DOC_ID` | no | none (`_own_batch` inside) |
| `get_reason_code_doc` | tools.py | tool | `reason_code: REASON_CODE` | no | none |
| `consult_search_exists` | tools.py | consult | `doc_id: DOC_ID`, `workspace: WORKSPACE` | no | `consult_once` |
| `handoff_to_access_agent` | team.py | handoff (H) | `invoice_id`, `batch_id`, `reason_code`, `target_workspace`, `permission`, `justification` | no | `access_handoff_allowed` |
| `check_entitlement` | tools.py | tool | `workspace`, `permission: PERMISSION` | no | none |
| `create_access_request` | tools.py | tool | `workspace`, `permission`, `justification: STR` | yes | none |
| `get_access_request_status` | tools.py | tool | `request_id: REQUEST_ID` | no | none |
| `call_reupload_agent` | team.py | agent (M) | `doc_id`, `target_workspace`, `request_id` | no | `reupload_allowed` |
| `prevalidate` | tools.py | tool | `doc_id`, `target_workspace` | no | none |
| `upload_record` | tools.py | tool | `doc_id`, `target_workspace` | yes | `upload_allowed` |
| `notify_user` | team.py | tool | `message` (≤1500) | no | `notify_once` |

Schema atoms (`das/schema.py`): `STR` string ≤500, `DOC_ID` `\d{4}`, `DATE` `\d{4}-\d{2}-\d{2}`,
`WORKSPACE` ∈ {Finance, Compliance, HR}, `PERMISSION` ∈ {read, upload}, `REQUEST_ID` `REQ-\d+`,
`BATCH_ID` `BATCH-\d{4}-\d{2}-\d{2}-\d{3}`, `REASON_CODE` `[A-Z]{3}-[A-Z-]+`.

### 5.4 Gateway.call checks, in order (`das/gateway.py`)

1. Tool is on the calling agent's allowlist, else `tool_not_permitted`.
2. Arguments were valid JSON, else `invalid_arguments`.
3. `schema.validate(args, tool.parameters)`, else `invalid_arguments`.
4. `tool.precondition(ctx, args)` returns `None`, else `precondition_failed`.
5. If `tool.write`: `confirmer(agent, tool, args)` (default `auto_confirm`), else `not_confirmed`.
6. Run `tool.fn(ctx, args)`; a `ToolError` becomes a refusal with its code.
7. `guardrails.sanitize(result)`; findings added as `untrusted_content`.
8. Add ids in the result to `session.known_ids` (used later by the output guardrail); append to `audit`.

### 5.5 Routing preconditions (`das/team.py`, `das/tools.py`)

- `access_handoff_allowed`: B must have returned a `reason_code`; `fault` must be false; baton `reason_code` and `batch_id` must equal B's; `invoice_id` must equal the session's.
- `reupload_allowed`: the request exists, belongs to the user, is `approved`, and is for the target workspace.
- `upload_allowed`: `prevalidate` passed for this doc in this run, and the user now has upload access.
- `consult_once`: only one consult per DebuggerAgent run.
- `notify_once`: only one notification per handoff.

## 6. Happy path, step by step

| # | From → To | Call | File · function | Contract in / out |
|---|---|---|---|---|
| 1 | Priya → Runtime | `bot.handle(REQUEST)` | main.py `main` → runtime.py `DASChatbot.handle` | text in; list of (sender, text) out |
| 2 | Runtime → Runtime (SSO) | `state.login("priya")` (at construction) | store.py `RuntimeState.login` | `UserContext` with token `FAKE-SSO-TOKEN-priya` |
| 3 | Runtime → Guardrails | `detect_injection`, `redact_pii` | guardrails.py | passed; nothing to redact |
| 4 | Guardrails → LLM | `check_topic` (agent "InputGuardrail") | guardrails.py `check_topic` | `{"on_topic": true, "reason": ...}` |
| 5 | Runtime → Coordinator | `COORDINATOR.run(bot, cleaned, history)` | agent.py `Agent.run` → `_loop` | text brief; 5 tool specs offered |
| 6 | Coordinator → LLM | turn 1 | llm.py `chat` | 2 tool calls: `call_search_agent`, `call_debugger_agent` |
| 7 | Coordinator → Coordinator (parallel) | `_execute` runs both in a `ThreadPoolExecutor` | agent.py `Agent._execute` | no write tools, so parallel |
| 8 | Coordinator → A·Search (M, via Gateway.call) | `call_search_agent` → `SEARCH.run(brief)` | team.py `call_search_agent` | `{invoice_id:"1240", workspace:"Finance"}` |
| 9 | A·Search → Gateway + tools | `search_archive` | tools.py `search_archive` | `{count: 0, matches: []}` |
| 10 | A·Search → Coordinator | final answer (validated by `SEARCH_OUT`) | agent.py `_loop` | `{doc_id:"1240", workspace:"Finance", exists:false, has_access:true}` |
| 11 | Coordinator → B·Debugger (M, via Gateway.call) | `call_debugger_agent` → `DEBUGGER.run(brief)` | team.py `call_debugger_agent` | `{invoice_id:"1240", batch_date:"2026-10-29"}` |
| 12 | B → Gateway + tools | `get_batch_status` | tools.py | `BATCH-2026-10-29-001`: 20 files, 19 archived, rejected `["1240"]` |
| 13 | B → Gateway + tools | `get_validation_log` | tools.py | stage classification, `CLS-COMPLIANCE`, confidence 0.94 |
| 14 | B → Gateway + tools | `get_reason_code_doc` | tools.py | user_fixable true, fault false, target_workspace Compliance |
| 15 | B → A (consult, via Gateway.call) | `consult_search_exists` | tools.py `consult_search_exists` | `{exists: false}`; recorded in `ctx.run["consults"]` |
| 16 | B → Coordinator | final answer (validated by `DEBUG_OUT`) + `consults` | team.py `call_debugger_agent` | `{batch_id, status:"rejected", reason_code:"CLS-COMPLIANCE", fault:false, ...}`; stored in `SessionMemory` |
| 17 | Coordinator → LLM | turn 2 | llm.py | 1 tool call: `handoff_to_access_agent` |
| 18 | Coordinator → Runtime (H, via Gateway.call) | `access_handoff_allowed` passes; `_hand_off` appends `Baton` to `bot.pending_handoffs` | team.py `handoff_to_access_agent` | `{accepted:true, now_owned_by:"C·Access agent (Compliance team)"}` |
| 19 | Coordinator → Runtime | LLM turn 3 gives the final answer; `run()` returns it | agent.py `_loop` | plain text reply |
| 20 | Runtime → Guardrails (output) | `check_output(reply, known_ids, restricted_ids)` | runtime.py `_deliver_checked` | cited ids `1240`, `BATCH-2026-10-29-001` all known; passed |
| 21 | Runtime → Priya | `deliver("DAS assistant", masked)` | runtime.py `deliver` | message 1 in Chat UI |
| 22 | Runtime → C·Access (H target) | `_dispatch_handoffs` → `ACCESS.run(bot, baton.to_dict())` | runtime.py `_dispatch_handoffs` | baton as brief |
| 23 | C → Gateway + tools | `check_entitlement` | tools.py | `granted: false` |
| 24 | C → Gateway + tools | `create_access_request` (write, auto-confirmed) | tools.py | `REQ-1001`, `pending_approval`, routed to `compliance-records-lead` |
| 25 | C → Gateway + tools | `get_access_request_status` | tools.py | simulated approval; IAM grants `Compliance-Uploader`; `status: approved` |
| 26 | C → D·Reupload (M, via Gateway.call) | `reupload_allowed` passes; `REUPLOAD.run(brief)` | team.py `call_reupload_agent` | `{doc_id:"1240", target_workspace:"Compliance", request_id:"REQ-1001"}` |
| 27 | D → Gateway + tools | `prevalidate` | tools.py | 4 checks passed (document_class, title, supplier_vat_id, customs_reference) |
| 28 | D → Gateway + tools | `upload_record` (write; `upload_allowed` passes; auto-confirmed) | tools.py | archived in `Compliance/VAT-Evidence/2026`, retention 10 years, delete_after 2036-12-31 |
| 29 | D → C | final answer (validated by `REUPLOAD_OUT`) | agent.py `_loop` | `{prevalidation:"passed", status:"archived"}` |
| 30 | C → Priya (via Gateway.call, output guardrail) | `notify_user`: output guardrail then `deliver` | team.py `notify_user` | message 2 in Chat UI, from "C·Access agent (Compliance team)" |
| 31 | C → Runtime | final answer (validated by `ACCESS_OUT`) | runtime.py `_dispatch_handoffs` | `{request_id:"REQ-1001", access:"granted", reupload_status:"archived in Compliance", notified:true}` |

Follow-up "Is it approved yet?": input guardrails → Coordinator reads `SessionMemory.snapshot()` in its prompt →
`get_access_request_status(REQ-1001)` → reply citing `1240`, `REQ-1001` → output guardrail passed.

## 7. Sequence diagram

The HTML page draws the 31 steps of §6 on 10 lifelines: Priya, Runtime, Guardrails, Coordinator, A·Search,
B·Debugger, C·Access, D·Reupload, Gateway + tools, LLM. The LLM turns of A, B, C and D are not drawn as
separate arrows (they happen between each of their tool calls). Every tool and agent call passes `Gateway.call`.

```
Priya  Runtime  InGuard  Coordinator  Gateway  A·Search  B·Debugger  C·Access  D·Reupload  Tools/Data
  |--handle-->|
  |           |--check-->|  (injection, PII, topic LLM)
  |           |---------run------->|
  |           |                    |==call_search_agent (M)==>A--search_archive-->Data
  |           |                    |==call_debugger_agent (M)=>B--batch/log/reason-->Data, consult A
  |           |                    |<====== A result, B result (parallel) ======|
  |           |                    |--handoff_to_access_agent (H)--> Baton queued
  |           |<----reply text-----|
  |<--msg 1 (output guardrail ✓)---|
  |           |--------------- dispatch baton ---------------->C
  |           |                                                C--entitlement/request/status-->Data
  |           |                                                C==call_reupload_agent (M)==>D--prevalidate/upload-->Data
  |<--------------------- msg 2 notify_user (output guardrail ✓) --C
```

### 7.1 How to read the diagram

- **Columns are lifelines.** Each column is one participant. The box at the top gives its name and its file
  (for example `team.py · DEBUGGER`). The dashed vertical line under it is that participant over time.
- **Time runs top to bottom.** The number on each arrow is the step number in §6, so step 12 happens after step 11.
- **An arrow goes from caller to callee.** The arrowhead points at whoever receives the call, result or message.
- **Line style shows the kind of call** (legend above the diagram):
  - solid blue: Manager call (M); the caller waits and control comes back to it
  - dashed grey: return or result going back to the caller
  - thick purple: handoff (H); control and ownership move and do not come back
  - teal: bounded consult (B asks A one question)
  - thin grey: read tool through `Gateway.call`
  - orange: write tool (auto-confirmed, simulated consent)
  - dotted blue: LLM call
  - green: guardrail check passed, or a message to Priya
- **A loop that comes back to the same column** is an internal step with no call to anyone else
  (step 2 SSO, step 7 parallel dispatch).
- **Shaded bands are phases.** The label at the top right of each band names it: Input, Manager calls,
  Handoff + reply, C·Access owns it.
- **Parallel work is drawn in sequence.** Steps 8–10 (A) and 11–16 (B) run at the same time in two threads.
  They are drawn one after the other only so they are readable.
- **Watch the Coordinator column after step 18.** After the handoff, the Coordinator's only remaining arrow is its
  reply (step 19). From step 22 on, C·Access does the work and sends message 2 itself; nothing returns to the Coordinator.
- **Not drawn:** the LLM turns of A, B, C and D between their tool calls, and the `Gateway.call` checks inside each
  tool arrow (§5.4).

## 8. Per-agent numbers (first request)

| Agent | LLM calls | Tool calls | Tokens in | Tokens out |
|---|---|---|---|---|
| InputGuardrail | 1 | 0 | 139 | 19 |
| Coordinator | 3 | 3 | 1820 | 165 |
| A·Search | 2 | 1 | 497 | 51 |
| B·Debugger | 5 | 4 | 4036 | 132 |
| C·Access | 6 | 5 | 2946 | 77 |
| D·Reupload | 3 | 2 | 814 | 66 |
| TOTAL | 20 | 15 | 10252 | 510 |

Token counts in offline mode are estimates by `ScriptedLLM` (characters / 4), not real model usage.

## 9. Not on the happy path

- Fault path: B returns `fault: true` → `handoff_to_platform_team` → `DASChatbot._platform_team` → `open_incident`.
- Refusals: off-topic, prompt injection, gateway `BLOCK`s, output guardrail blocking twice → `FALLBACK`.
- Sanitising of planted instructions (doc 1236's title) in `guardrails.sanitize`.

## 10. Plain-language guide (Wiki tab)

For readers who don't write code. Each part says what happens, why it is built that way, and where it is in the
code (file · function, and the step numbers from §6).

### 10.1 The cast (an office analogy)

The analogy is only there to help you understand. The real names are in brackets.

| Character | In the office | In the code |
|---|---|---|
| Priya | The customer at the counter | `UserContext` (store.py) |
| Office manager | Runs the conversation: takes the message, passes it on, delivers replies, later passes on handed-over work | `DASChatbot` (runtime.py) |
| Mailroom check | Checks every message coming in and every reply going out | guardrails.py |
| Front-desk lead | Splits the request, sends workers, writes the reply. Never looks anything up itself | `COORDINATOR` (team.py) |
| Archive clerk (A) | Checks whether a document is in a cabinet | `SEARCH` (team.py) |
| Investigator (B) | Reads the upload logs and the rulebook to find out what went wrong | `DEBUGGER` (team.py) |
| Compliance access officer (C) | Owns the access request and re-upload, and tells Priya the result | `ACCESS` (team.py) |
| Compliance filing clerk (D) | Checks the file meets the rules, then files it | `REUPLOAD` (team.py) |
| Security door | The one door into every office system: checks badge, form, order of steps, consent, and strips suspicious text | `Gateway` (gateway.py) |
| The "thinking" | Each worker asks the language model what to do next. Offline, the answers are replayed from a script | `NexusClient` / `ScriptedLLM` (llm.py) |
| Office systems | Archive, upload logs, rulebook, access rights (IAM), ticketing (ITSM) | tools.py + `data/*.json` |

### 10.2 Glossary

| Term | Plain meaning | In the code |
|---|---|---|
| Agent | A worker: instructions, a set of allowed tools, and an answer form | `Agent` (agent.py) |
| LLM | The language model that decides the next step | `LLMClient.chat` (llm.py) |
| Tool | One action in an office system, e.g. "search the archive" | `Tool` (gateway.py), functions in tools.py |
| Tool call | A worker asking to use a tool, with filled-in fields | `ToolCall` (llm.py) |
| Gateway | The single door every tool call passes through | `Gateway.call` (gateway.py) |
| Allowlist | The tools a worker may use (its key ring) | `ALLOWLISTS` (team.py) |
| Schema / contract | The form an input or answer must fit: which fields, which types, which values | schema.py, `*_OUT` (team.py) |
| Brief | The written task one worker gives another | `brief` dicts in team.py |
| Manager call | "Do this and report back to me" | `kind="agent"` tools |
| Handoff / baton | "This is yours now"; the case folder that moves with it | `Baton`, `_hand_off` (team.py) |
| Consult | B's one allowed question to A | `consult_search_exists` (tools.py) |
| Precondition | A rule that must be true before a tool may run | `precondition=` on `Tool` |
| Write action | A tool that changes something (needs consent) | `write=True` on `Tool` |
| Guardrail | An automatic check on messages in and out | guardrails.py |
| Known ids | Every id that came from Priya or from a tool result; the reply may only mention these | `SessionMemory.known_ids` (store.py) |
| Session memory | What the front desk remembers between Priya's messages | `SessionMemory` (store.py) |
| Offline mode | The model's decisions are replayed; everything else is real | `offline_llm()` (offline.py) |

### 10.3 How a worker thinks (the loop)

1. It reads its instructions and the brief.
2. It asks the language model what to do next and shows it the tools it may use.
3. The model either asks for one or more tools, or gives a final answer.
4. Tool requests go through the security door. Each result is added to the worker's notes. Back to step 2.
5. The final answer must fit the worker's answer form. If it doesn't, the worker gets one retry. Each worker also
   has a limit on turns (`max_steps`). Breaking either rule stops the worker with an error.

Code: agent.py `Agent.run`, `Agent._loop`, `Agent._execute`.

### 10.4 The story, chapter by chapter

1. **Priya asks** (steps 1–2). She is already signed in. Her identity and roles come from sign-in (SSO), with a fake
   token placeholder in this demo. Why: every later action runs as Priya, never as an admin, so she can only reach
   what she is allowed to. Code: runtime.py `DASChatbot.handle`, store.py `RuntimeState.login`.
2. **The mailroom checks the message** (steps 3–4). It asks three questions. Is someone trying to trick the bot? Is
   there personal data (email, phone, IBAN) to mask? Is the message about the archive (a yes/no question to the
   model)? Why: misuse is stopped before any worker spends effort. If the topic check gets an unclear answer, it
   refuses (fails closed). If something goes wrong, Priya gets a refusal or an "unavailable" message. Code:
   guardrails.py `detect_injection`, `redact_pii`, `check_topic`; runtime.py `_input_guardrails`.
3. **The front desk plans** (steps 5–7). It sees two separate questions: "where is 1240?" and "what happened to
   yesterday's upload?" ("yesterday" is 2026-10-29). It sends both workers at the same time. Why: the questions don't
   depend on each other, so running them together saves time. The front desk never looks things up itself, so each
   worker keeps a small key ring. Code: team.py `coordinator_prompt`; agent.py `_loop`, `_execute`.
4. **A checks the archive** (steps 8–10). It searches Finance for 1240 and finds nothing. Priya does have read access
   to Finance. A answers on a fixed form (`SEARCH_OUT`). Why: a fixed form gives the front desk predictable facts.
   A cannot upload and cannot talk to Priya. Code: team.py `call_search_agent`; tools.py `search_archive`.
5. **B investigates** (steps 11–16). It finds yesterday's batch: 20 files, 19 archived. The log says 1240 was
   rejected when its type was recognised: the classifier saw import VAT evidence (a customs declaration is attached),
   confidence 0.94, and Finance accepts plain invoices only. The rulebook entry for `CLS-COMPLIANCE` says Priya can
   fix this herself, it is not a system fault, and the right place is Compliance. B double-checks once with A that
   1240 didn't turn up late. Why: "not a system fault" decides the route. Only one question to A is allowed, and it
   is reported, so workers can't chat endlessly. Code: tools.py `get_batch_status`, `get_validation_log`,
   `get_reason_code_doc`, `consult_search_exists`, `consult_once`.
6. **The front desk hands over** (steps 17–18). It may not grant access in another team's system, so it passes a
   baton to Compliance's access officer. The baton holds the invoice, batch, reason code and request, plus Priya's
   identity, which comes from sign-in and not from the AI. From now on C owns the case. Why: ownership is clear.
   The door only lets the handoff through if it matches what B actually found, so the AI can't invent a reason.
   Code: team.py `handoff_to_access_agent`, `access_handoff_allowed`, `Baton`, `_hand_off`.
7. **Priya gets the first answer** (steps 19–21). The front desk writes the reply. The mailroom then checks that
   every id it mentions came from Priya or from a tool result, and masks personal data. Why: this catches invented ids
   and records Priya may not see. If the check blocks the reply, there is one rewrite, then a safe fallback message.
   Code: runtime.py `_deliver_checked`; guardrails.py `check_output`.
8. **Compliance takes over** (steps 22–25). C checks Priya's rights and finds she can't upload to Compliance. It raises
   access request REQ-1001 to the data owner (`compliance-records-lead`). This is a change, so consent is asked first
   (automatic in this demo). It then checks the status: approved, and Priya gets the `Compliance-Uploader` role. The
   approval is simulated: it happens instantly. Why: changes need consent, and the team that owns the system does the
   work. Code: tools.py `check_entitlement`, `create_access_request`, `get_access_request_status`; gateway.py `auto_confirm`.
9. **The file is filed** (steps 26–29). C asks D to do the upload. D first checks the held file against Compliance's
   rules: type `import_vat_evidence` is accepted; title, supplier VAT id and customs reference are present. Only then
   does it upload. The file lands in `Compliance/VAT-Evidence/2026`, kept 10 years, delete after 2036-12-31. Why: the
   door refuses the upload unless the check passed and the approval exists. The order is enforced by code, not by
   trusting the AI. Code: team.py `call_reupload_agent`, `reupload_allowed`; tools.py `prevalidate`, `upload_record`,
   `upload_allowed`.
10. **Priya gets the second message** (steps 30–31). C tells Priya itself, through the same mailroom check, and only
    once. The front desk never hears the outcome. Why: the owner reports. Code: team.py `notify_user`, `notify_once`.
11. **Follow-up: "Is it approved yet?"** The front desk remembers REQ-1001 from session memory and checks the live
    status. Code: store.py `SessionMemory`; team.py `coordinator_prompt`.

### 10.5 Safety rules the code enforces

- **Each worker has its own key ring.** It only sees and can only use its allowed tools. Code: team.py `ALLOWLISTS`, gateway.py `specs_for`, `call`.
- **Every form is checked.** Fields, types and formats (e.g. a 4-digit document id) are validated before a tool runs. Code: schema.py `validate`.
- **Steps must happen in order.** E.g. no upload before the file passes its check and access is approved. Code: tool preconditions in team.py and tools.py.
- **Changes need consent.** Access requests, uploads and incidents ask first (automatic in this demo, or `--confirm-writes`). Code: gateway.py `confirmer`.
- **Retrieved text is data, not orders.** Instructions hidden in documents are cut out (e.g. doc 1236's title). Code: guardrails.py `sanitize`.
- **No invented ids.** Replies may only mention ids that came from Priya or from a tool result. Code: guardrails.py `check_output`.
- **Acts as Priya, never as admin.** Tools check ownership, e.g. only Priya's own batches. Code: tools.py `_require`, `_own_batch`.
- **Secrets only from settings.** The model key comes from the environment and is never printed. Code: config.py `LLMSettings`.

### 10.6 Questions people ask

- **Does the AI make up the answer?** The facts come from tool results. The reply is checked so that it only cites
  ids that really appeared. Code: guardrails.py `check_output`.
- **Is the approval real?** No, not in this demo. `get_access_request_status` approves a pending request at once.
- **Why two messages from two senders?** The handoff moved ownership. The front desk answers what it owns, and
  Compliance's officer reports its own outcome.
- **What does "offline" mean?** The model's choices are replayed from `das/offline.py`. Everything else runs for real.
- **What if a worker fails?** Priya gets a safe fallback message. If handed-over work fails, she is told it could
  not be completed automatically and that the owning team has been informed. Code: runtime.py `handle`, `_dispatch_handoffs`.
- **Why several workers and not one big AI?** Each worker has a small key ring, the code checks every hand-over between
  them, and it is always clear who owns the reply. Code: team.py docstring and `ALLOWLISTS`.

### 10.7 Each step in plain words

1. Priya's message reaches the chatbot.
2. Her sign-in tells the system who she is and what roles she has.
3. The message is checked for tricks and personal data.
4. The model confirms the message is about the archive.
5. The front desk starts working on the request.
6. It decides to ask two workers at once.
7. Both workers start at the same time.
8. The archive clerk is asked: is 1240 in Finance?
9. It searches the Finance archive: nothing found.
10. It reports: not there, but Priya has read access.
11. The investigator is asked: what happened to 1240 in yesterday's upload?
12. It finds yesterday's batch: 19 of 20 archived, 1240 rejected.
13. It reads the log: 1240 was recognised as import VAT evidence.
14. It looks up the rejection code: Priya can fix it; it belongs in Compliance.
15. It double-checks with the archive clerk once: still not in Finance.
16. It reports the reason and that this is not a system fault.
17. The front desk decides to hand the case to Compliance.
18. The baton is passed; Compliance's access officer now owns the case.
19. The front desk writes its reply to Priya.
20. The reply is checked: only real ids, no personal data.
21. Priya receives message 1.
22. Compliance's access officer picks up the baton.
23. It checks Priya's rights: no upload access to Compliance.
24. It raises access request REQ-1001 (with consent).
25. The request is approved (simulated) and Priya gets the role.
26. It asks the filing clerk to upload 1240.
27. The filing clerk checks the file against Compliance's rules: all pass.
28. It files 1240 in Compliance/VAT-Evidence/2026.
29. It reports back: archived.
30. Compliance's access officer tells Priya the outcome (message 2).
31. It closes the case; the front desk is not told.
