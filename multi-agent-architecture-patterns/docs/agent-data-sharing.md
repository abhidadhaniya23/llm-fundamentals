# How data is shared between the agents in `das/`

Agents never share a conversation or message history. Each agent run starts with a new message list:
its own system prompt plus one **brief**. Only the Coordinator gets the chat history (`history=`).
Agents A to D see just their brief and their own tool results.

Data moves between agents through five channels. Each one is built in code, not by the LLM.

## Agents

| Agent | Role | Talks to the user? |
|---|---|---|
| ③ Coordinator | Routes the request, composes the reply | yes |
| ④ A·Search | `search_archive`, `get_record` | no |
| ⑤ B·Debugger | batch status, validation log, reason codes, one bounded consult | no |
| ⑥ C·Access | Owned by Compliance: entitlement, access request, calls D, notifies the user | yes (`notify_user`) |
| ⑦ D·Reupload | `prevalidate`, `upload_record` | no |
| E Platform team | Humans: an incident ticket | via ITSM |

Source: `das/team.py` lines 1-13, `ALLOWLISTS` lines 277-286.

## 1. Brief down, structured result up (Manager-style calls, "M")

`call_search_agent` and `call_debugger_agent` are Python tools of the Coordinator (`das/team.py` 133-161). Each one:

- **Builds the brief in code** from the schema-validated tool arguments: goal, ids, expected output and scope.
  `Agent.run()` sends it as the sub-agent's only `user` message (`das/agent.py` 52-55).
- **Gets back JSON checked against a schema.** The final answer must match `SEARCH_OUT`, `DEBUG_OUT`, …,
  with one repair attempt (`das/agent.py` 92-105). The dict is returned to the caller as an ordinary tool result.
- **Writes the result into `SessionMemory`**: `search_result`, `debugger_result`, `batch_id`, `reason_code`, `fault`.

C calls D the same way through `call_reupload_agent` (`das/team.py` 164-171).

## 2. Baton (handoffs, "H": control does not come back)

`handoff_to_access_agent` and `handoff_to_platform_team` build a `Baton` dataclass (`das/team.py` 115-128)
and append it to `bot.pending_handoffs` (`das/team.py` 209-218).

- The Coordinator only gets an acknowledgement ("now owned by …"), never the outcome.
- After the Coordinator's reply is delivered, `_dispatch_handoffs` pops each baton; `baton.to_dict()` becomes
  agent C's brief, or the platform team's incident input (`das/runtime.py` 130-156).
- The baton's `user` field comes from `ctx.user.scope()` (the SSO context), never from LLM arguments.

Baton fields: `target`, `invoice_id`, `batch_id`, `reason_code`, `user`, `reply_owner`, `notifies_next`, `request`.

## 3. Shared objects on `DASChatbot`

`ToolContext` exposes `bot`, `user`, `state` and `session` to every tool (`das/gateway.py` 30-46).

| Object | Scope | What it holds | Who uses it |
|---|---|---|---|
| `DataStore` | read-only | JSON files in `data/` | system tools |
| `RuntimeState` | per bot, `RLock` | IAM grants, access requests, uploads, incidents | C creates requests; D uploads; Coordinator checks request status |
| `SessionMemory` | per session | invoice/batch/reason, A's and B's results, handoffs, chat turns, `known_ids` | Coordinator prompt (`snapshot()`), handoff preconditions, output guardrail |
| `ToolContext.run` | one agent run | `consults`, `prevalidated`, `notified` | B's single consult, D's prevalidate-before-upload rule, C's notify-once rule |

The lock matters because the Coordinator runs A and B in parallel threads (`das/agent.py` 116-125), and both write to `session`.

Source: `das/store.py` 22-134.

## 4. Gateway as the common pipe

Every tool result from every agent goes through `Gateway.call` (`das/gateway.py` 98-133):

- It removes instructions embedded in the data (`guardrails.sanitize`).
- It adds every id it sees to `session.known_ids`. The output guardrail only lets replies (Coordinator reply
  and C's `notify_user`) cite ids in that set.

## 5. Code checks on what the LLM passes along

Preconditions compare LLM arguments with recorded state:

- **Handoff to C:** `access_handoff_allowed` rejects the call unless `batch_id`/`reason_code` match
  `session.debugger_result`, `fault` is false, and the invoice is the session's (`das/team.py` 189-199).
- **Handoff to E:** `platform_handoff_allowed` requires B to have reported `fault=true` (`das/team.py` 202-206).
- **Call to D:** `reupload_allowed` checks `state.access_requests`: the request must be approved, for this user
  and this workspace (`das/team.py` 174-180).
- **B's consult:** `output["consults"]` is copied from the gateway's record in `run_ctx.run`, not from what B
  says about itself (`das/team.py` 153).

## Detail to note

`consult_search_exists` (B asking A) does not start an A agent run. It calls the helper `exists_in` directly,
is allowed once (`consult_once`), records it in `ctx.run["consults"]`, and the record is passed up to the
Coordinator (`das/tools.py` 74-83).

## Relation to the "Pass or Share" deck

Source: `pass-or-share-live.html` (deck with two walkthroughs: *Passing data* on a warranty claim, *Shared state*
on a technical case board). This section maps each deck concept to the `das/` code.

### Verdict

`das/` is a **pass** system with one **orchestrator-owned record**. By the deck's rule ("share inside one case
when the next step depends on a finding; pass when the order and consumer are known", deck Shared state Q9),
that fits: the route is known in advance (A ‖ B, then C or E), so no case board is needed.

### Passing-data concepts → `das/`

| Deck concept | In `das/` | Fit |
|---|---|---|
| Agent (LLM in a loop) vs plain code | Coordinator, A, B, C, D run `Agent._loop`; system tools, `consult_search_exists` and E (humans) are not agents | match |
| Orchestrator: code or LLM supervisor | Coordinator is an **LLM supervisor**; `_dispatch_handoffs` and gateway preconditions are **code** around it | match (hybrid) |
| Handoff = brief down, result up | "M" calls: brief `{goal, ids, output, scope}`, schema-checked JSON back | match |
| Brief: objective, context, constraints, return | `goal`, ids, `scope` ("no uploads, never reply to the user"), `output` | match |
| Pass vs share | Agents only pass; nothing an agent writes is read by another agent except through a tool result or a baton | pass |
| Record owned by the orchestrator (deck: "usually right") | `SessionMemory`: written only by code (the `call_*` wrappers, `_hand_off`, the gateway), never by an agent directly | match |
| Reducers not needed when code collects return values | Partly: the wrappers write to `session` from parallel threads, so an `RLock` is used; `known_ids \|=` is a set-union merge | partial |
| Contract = fixed envelope + varying payload | Output schemas exist (`SEARCH_OUT`, `DEBUG_OUT`, `ACCESS_OUT`, `REUPLOAD_OUT`) but are flat payloads; **no shared envelope** (`status`, `confidence`, `evidence_ids`, `caveats`) | gap |
| Claim check (ids point to evidence elsewhere) | Results carry ids (`doc_id`, `batch_id`, `reason_code`, `REQ-…`) that point into `DataStore` / `RuntimeState`; no `evidence_ids` field | partial |
| Contract test at the boundary | `schema.validate` + one repair; gateway argument validation; handoff preconditions check the baton against B's result | match |
| Strictness follows the reader | Code (preconditions) reads strict fields `batch_id`, `reason_code`, `fault`; only the Coordinator LLM reads free-text `explanation` / `note` | match |
| Free-text hops lose hedges | The baton is built from typed fields, not from the Coordinator's prose; `justification` is the only free text | match |
| Front door: intake turns text into finite intents | Input guardrails: injection check, PII redaction, on/off-topic classifier. **No intent classification**: the Coordinator LLM routes | partial |
| Agent owned by someone else | C·Access is owned by the Compliance team; reached only by a baton; its tool set is its menu | match |
| Twist: messages can carry instructions | `DATA_ONLY` line in every prompt; `guardrails.sanitize` on every tool result | match |
| Twist: evidence can be hallucinated | Output guardrail only allows ids in `session.known_ids` (ids seen in tool results) | match |

### Shared-state concepts → `das/`

| Deck concept | In `das/` | Fit |
|---|---|---|
| Case board (blackboard) | None. Not needed: the order is known | n/a (correct) |
| Write rules per author | `ALLOWLISTS` (only C may `create_access_request`, only D `upload_record`, only E `open_incident`) + preconditions (`notify_once`, `consult_once`, `upload_allowed`) | match |
| Views: each agent reads a projection | Sub-agents get only a brief; the Coordinator gets `session.snapshot()`, which hides `turns`, `known_ids`, `search_result`, `debugger_result` | match |
| Controller in code: wakes, budgets, stops | `max_steps` per agent (Coordinator 8, A 5, B 8, C 10, D 5); one schema repair; output guardrail twice → fallback; one consult | match |
| Concurrent writes: append or single writer | `session.handoffs.append`, `known_ids \|=` are appends/merges; scalar fields (`invoice_id`, …) are last-write-wins under the lock | partial |
| Provenance and trust labels | Gateway adds `untrusted_content` to sanitised results; `gateway.audit` records agent, tool, outcome; user identity from SSO. Session fields carry **no author** | partial |
| Share inside, pass at the edges | The edge to Compliance (C) and to the platform team (E) is a passed baton, never shared state | match |

### Terminology clash

- Deck **handoff** = any move of work between two parties (brief down, result up). In `das/` that is an **M** call.
- `das/` **H handoff** = control and reply ownership move, no result comes back. The deck has no separate word for it;
  its closest idea is the board's exit ("the decision leaves as a passed message").

### Suggestions from the deck (not in the code)

- Add a shared envelope (`status`, `confidence`, `evidence_ids`, `caveats`) to every agent output schema (deck Passing data a6, Q6).
- Add an intent field at intake so routing uses a finite set of intents (deck Passing data Q9).
- Record the author of each `SessionMemory` write, or make the scalar fields single-writer (deck Shared state a6, a7).

## Summary flow

```
User → Coordinator ──brief──► A ──JSON──► Coordinator ─┐
                   ──brief──► B ──JSON──► Coordinator  ├─ writes SessionMemory
                       (B ─consult→ exists_in, 1x)     ┘
Coordinator ──Baton──► pending_handoffs ──► C ──brief──► D ──JSON──► C ──notify_user──► User
                                          (C/D read/write RuntimeState: requests, grants, uploads)
```
