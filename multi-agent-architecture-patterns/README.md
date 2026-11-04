# Multi-Agent Architecture Patterns: DAS chatbot, Coordinator + Handoff

A fully LLM-driven implementation of `docs/agent-flow-architecture.html`, run for one request from
Priya (Finance Analyst):

> "I uploaded 20 invoices yesterday but I can't find invoice 1240 in Finance. If it got rejected,
> tell me why and get me access to the Compliance archive to re-upload it there."

Every agent is an LLM tool-calling loop. Code enforces the architecture's rules: tool allowlists,
Manager vs Handoff semantics, routing preconditions, schemas and guardrails.

## Setup

Copy `.env.example` to `.env` and fill in the MB Nexus values:

```
LLM_FAST_PROVIDER=nexus
LLM_FAST_MODEL=gpt-4o
LLM_FAST_API_URL=https://genai-nexus.int.api.corpinter.net
LLM_FAST_API_KEY=...
LLM_FAST_API_VERSION=2023-12-01-preview
```

Check that the deployment supports tool calling (the agents depend on it):

```
.venv\Scripts\uv run scripts\probe_tools.py
```

## Run

```
.venv\Scripts\uv run main.py                  # live: prompts "Priya>" for your question (Enter = sample request), then follow-ups
uv run main.py --once           # live: one question, no follow-up prompt
.venv\Scripts\uv run main.py --offline        # same flow with replayed model decisions, no Nexus needed
.venv\Scripts\uv run main.py --full           # never truncate payloads in the trace
.venv\Scripts\uv run main.py --show-prompts   # also print system prompts and full LLM message lists
.venv\Scripts\uv run main.py --trace-file trace.jsonl --confirm-writes
.venv\Scripts\uv run main.py --message "Where is invoice 1234?"   # skip the first prompt
```

`uv` not on your PATH? Use the copy in the project venv: `.venv\Scripts\uv run main.py`.

```
uv run main.py   # type 'exit' or press Enter on an empty follow-up to quit
```

## Reading the trace

Numbered sections match the diagram's badges, and indentation shows who called whom.

| Label | Meaning |
|---|---|
| `① … ⑧` | user, gateway + SSO, Coordinator, A, B, C, D, output guardrails |
| `LLM →` / `LLM ←` | one model call: what was sent, then the tool calls or final answer it returned |
| `M ↓` / `M ↑` | Manager-style call: brief goes down, result comes back, control returns |
| `H ⇒` | Handoff: baton passed, control and ownership move, no return |
| `⇄ ASK` | B's single bounded consult of A, reported upward in B's result |
| `TOOL→` / `TOOL←` | a tool call through the gateway, with arguments and result |
| `PAR ⇉` | tool calls from one turn running in parallel (A and B); each branch is printed in order with real timestamps |
| `GUARD` / `BLOCK` / `WARN` | guardrail or gateway decision (refusals, sanitised data) |
| `SIM` | simulated parts: user consent for writes, ITSM approval by the data owner |
| `SAY` | a message that reaches the Chat UI |

After each request you get a **FLOW SUMMARY** (the hops in order, plus LLM and tool calls and tokens
per agent) and **WHAT PRIYA SEES IN THE CHAT UI**.

## Layout

| Diagram | Code |
|---|---|
| Chat UI, gateway + SSO | `main.py`, `das/runtime.py` (`UserContext` with a fake token placeholder) |
| Input / output guardrails | `das/guardrails.py` |
| ③ Coordinator, ④ A, ⑤ B, ⑥ C, ⑦ D, E | `das/team.py` (prompts, schemas, M/H tools, allowlists) |
| Agent loop | `das/agent.py` |
| Tool gateway | `das/gateway.py`, tools in `das/tools.py` |
| Enterprise systems | `data/*.json` (read-only) + `RuntimeState` in `das/store.py` (in memory) |
| LLM | `das/llm.py` (`NexusClient`, and `ScriptedLLM` for `--offline` and tests) |

The scenario uses invoice **1240**. `data/documents.json` is unchanged: 1234 really is archived in Finance.

## Tests

```
uv run pytest
```

The tests use a scripted LLM and cover:
- least privilege, schema validation, write confirmation and sanitising (doc 1236's planted instruction)
- ownership checks and the bounded consult
- Manager vs Handoff (the Coordinator never sees C's outcome) and the routing preconditions
- the fault path to the platform team
- guardrails and session follow-ups
