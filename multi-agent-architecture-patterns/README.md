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
- `docs/subagents/index.html`: subagents vs standalone agents
- `docs/fanout-vs-coordinator/index.html`: fan-out vs coordinator & specialist

## Setup

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
