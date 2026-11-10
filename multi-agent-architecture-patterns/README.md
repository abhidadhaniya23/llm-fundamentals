# Multi-Agent Architecture Patterns

Six multi-agent patterns, each run as a hands-on lab against the DAS
(Data Archival System) chatbot used throughout this training. Standalone
project: it only depends on this folder's own `archive.py` and `data/`.

| Pattern | Lab |
|---|---|
| 01 Sequential Pipeline | `labs/01_sequential_pipeline.py` |
| 01b Sequential Pipeline, with real agents ([design](docs/01b_sequential_agents.md)) | `labs/01b_sequential_agents.py` |
| 01b hardened: contracts, checkpoints, cost ([notes](docs/01b_fixes_in_our_example.md)) | `labs/01b_sequential_agents_hardened.py` |
| 02 Coordinator + Specialists | `labs/02_coordinator_specialists.py` |
| 03 Parallel Fan-Out | `labs/03_parallel_fanout.py` |
| 04 Hierarchical Escalation | `labs/04_hierarchical_escalation.py` |
| 05 Event-Driven | `labs/05_event_driven.py` |
| 06 Blackboard / P2P | `labs/06_blackboard.py` |

**Pattern 01b explained without the code:** open [`docs/01b/index.html`](docs/01b/index.html) in a browser. It reads as a page, and the arrow keys turn it into slides.

## Workflows & Agents, hand-rolled (no LangGraph)

The seven exercises from *Building Effective Agents with LangGraph*, with the
same pattern shapes, rebuilt in plain Python on
`labs/shared.py`. In the original only the last one is an agent; here **every
step is an agent** (`shared.run_agent`). Each exercise is bigger than the
original, so the tools are actually needed. The joke exercises (01, 02, 03, 05)
use an office scenario instead: a team moving to a new building, with real facts
to ground the text, plain-language checks, employee profiles and help-desk
articles. 04 keeps the scaling-laws report (a paper library with citations) and
06 the café prices. Code validates every
final answer and hands errors back to the agent.

**Explained without the code:** open [`docs/workflows-and-agents/index.html`](docs/workflows-and-agents/index.html)
in a browser. It has diagrams, notes, run commands and real traces for each exercise, and the arrow keys turn it into slides.

Labs 01–05 run two ways:
- `--mode workflow` (default): your code keeps the flow from the notes, and each step is an agent.
- `--mode agentic`: an agent runs the flow by calling the other agents as tools.

| Exercise | Lab |
|---|---|
| 00 Augmented LLM (one-shot, then a research agent) | `labs/wf00_augmented_llm.py` |
| 01 Prompt chaining (memo → draft → gate → plain language → final edit) | `labs/wf01_prompt_chaining.py` |
| 02 Parallelization (email, chat post, FAQ → aggregator) | `labs/wf02_parallelization.py` |
| 03 Routing (5 employee questions → IT / Facilities / HR desk) | `labs/wf03_routing.py` |
| 04 Orchestrator-worker (report on LLM scaling laws) | `labs/wf04_orchestrator_worker.py` |
| 05 Evaluator-optimizer (fire-drill notice until the reviewer approves) | `labs/wf05_evaluator_optimizer.py` |
| 06 Agent (calculator warm-up, then a café order) | `labs/wf06_agent.py` |

Shared code: `labs/wf_tools.py` (tools; `uv run labs/wf_tools.py` self-checks
them without an LLM), `labs/wf_writers.py` (the email, chat and FAQ writer
agents). Data: `data/workflows/`. Every lab saves a transcript to `runs/wf/`;
`docs/workflows-and-agents/build_examples.py --from-runs` turns them into the
worked examples on the page.

| LangGraph | Hand-rolled |
|---|---|
| `StateGraph(State)` + nodes | a `state` dict and plain functions |
| `add_edge` | calling the next function |
| `add_conditional_edges` | `if` / `elif` / `while` |
| several edges from `START`, `Send()` | `ThreadPoolExecutor` |
| `with_structured_output(Model)` | schema in the prompt + pydantic in `validate=` |
| `bind_tools` + `MessagesState` + tool node | `shared.run_agent`'s loop |

## Content deck extras (TBD)

Extra pages for the multi-agent content deck; the full deck lives elsewhere.
Folder naming and linking are still to be decided.

- `docs/design-exercises/index.html`: DAS multi-agent design session (exercises)
- `docs/recap/recap-2026-10-29.html`: recap, agent fundamentals + multi-agent
- `docs/recap/recap-multi-agent.html`: recap continued (Q12–Q47), multi-agent concepts (except "Why they fail") explained with the DAS chatbot in `das/`
- `docs/subagents/index.html`: subagents vs standalone agents
- `docs/fanout-vs-coordinator/index.html`: fan-out vs coordinator & specialist
- `docs/pass-or-share/index.html`: pass or share, agent contracts and shared state, plus a review of the DAS code against them

## Setup

Quick path: `bash setup.sh` installs `uv` if missing, creates `.env` and syncs dependencies. Then fill in `.env`. Manual steps:

Copy `.env.example` to `.env`, pick a provider and fill in its settings:

```
LLM_PROVIDER=nexus            # or: anthropic

NEXUS_BASE_URL=https://nexus.example.internal/v1
NEXUS_API_KEY=...
NEXUS_MODEL=MODEL-NAME

ANTHROPIC_API_KEY=...         # only for LLM_PROVIDER=anthropic
```

Every lab reads these from the environment — nothing is hardcoded.

## Run

```
uv run labs/01_sequential_pipeline.py
```

Each lab prints one trace line per agent step, so the pattern's flow is
visible while it runs.

## DAS chatbot: Coordinator + Handoff

A fully LLM-driven implementation of `docs/agent-flow-architecture.html`, run for one request from
Priya (Finance Analyst):

> "I uploaded 20 invoices yesterday but I can't find invoice 1240 in Finance. If it got rejected,
> tell me why and get me access to the Compliance archive to re-upload it there."

Every agent is an LLM tool-calling loop. Code enforces the architecture's rules: tool allowlists,
Manager vs Handoff semantics, routing preconditions, schemas and guardrails.

### Setup

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

### Run

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

### Reading the trace

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

### Layout

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

### Tests

```
uv run pytest
```

The tests use a scripted LLM and cover:
- least privilege, schema validation, write confirmation and sanitising (doc 1236's planted instruction)
- ownership checks and the bounded consult
- Manager vs Handoff (the Coordinator never sees C's outcome) and the routing preconditions
- the fault path to the platform team
- guardrails and session follow-ups
