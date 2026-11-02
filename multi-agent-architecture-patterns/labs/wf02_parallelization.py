"""
Workflows & Agents 02 · Parallelization, every step an agent

The notes' exercise: take a topic, write a joke, a story and a poem in
parallel, then combine them. Here each piece has a bar that needs tools:
    joke   original (checked against known jokes), punchline, max 50 words
    story  150-200 words, at least two real cat facts
    poem   a limerick (5 lines, AABBA), checked with check_limerick
and the Aggregator checks every fact the pieces claim before combining.

--mode workflow (default): code fans out and joins, as in the notes.
    topic -+-> Joke Writer  (agent) -+
           +-> Story Writer (agent) -+-> Aggregator (agent) -> combined output
           +-> Poem Writer  (agent) -+
    ThreadPoolExecutor is the hand-rolled version of three edges from START.

--mode agentic: a Coordinator agent decides what to dispatch. Its
    dispatch tool runs writer agents in parallel; it reviews the pieces,
    sends weak ones back, then writes the combined output.

Run it:
    uv run labs/wf02_parallelization.py
    uv run labs/wf02_parallelization.py --mode agentic
"""

import argparse
import json
from concurrent.futures import ThreadPoolExecutor

import shared
import wf_tools as t
import wf_writers

TOPIC = "cats"
HEADINGS = ("STORY:", "JOKE:", "POEM:")


def validate_combined(final) -> str:
    text = final.get("combined_output") if isinstance(final, dict) else None
    if not isinstance(text, str):
        raise ValueError('final must be {"combined_output": "..."}')
    if missing := [h for h in HEADINGS if h not in text]:
        raise ValueError(f"combined output is missing the headings {missing}")
    return text


AGGREGATOR_PROMPT = (
    "You combine a story, a joke and a poem about a topic into one output. Each piece "
    "lists the cat fact ids it uses. Check each id with get_fact and make sure the piece "
    "does not contradict that fact; if a piece states something about cats that the fact "
    "base does not support, note it under ISSUES. Do not rewrite the pieces.\n"
    "Format: a one-line intro, then STORY:, JOKE:, POEM: each followed by the piece, "
    "then ISSUES: (or 'none').\n"
    'Final answer: {"combined_output": "<the text>"}'
)


def aggregator(state: dict) -> str:
    pieces = {k: state[k] for k in ("story", "joke", "poem")}
    return shared.run_agent("Aggregator", AGGREGATOR_PROMPT,
                            f"Topic: {state['topic']}\n{json.dumps(pieces, indent=1)}",
                            {"get_fact": t.get_fact}, validate=validate_combined)


# ── Mode 1: code fans out and joins ──────────────────────────────────────────

def run_workflow() -> None:
    state = {"topic": TOPIC}
    briefs = {"joke": f"Write a joke about {TOPIC}", "story": f"Write a story about {TOPIC}",
              "poem": f"Write a poem about {TOPIC}"}
    with ThreadPoolExecutor() as pool:
        futures = {kind: pool.submit(wf_writers.write, kind, brief) for kind, brief in briefs.items()}
        for kind, future in futures.items():
            state[kind] = future.result()
    state["combined_output"] = aggregator(state)
    print(f"\n{state['combined_output']}")


# ── Mode 2: a Coordinator agent dispatches ───────────────────────────────────

def dispatch(jobs: list) -> list[dict]:
    """Run writer agents in parallel. jobs is a list like
    [{"kind": "joke" | "story" | "poem", "brief": "what to write"}]. Returns one
    result per job: {"kind", "text", "fact_ids"} or {"kind", "error"}."""
    def one(job: dict) -> dict:
        try:
            return {"kind": job["kind"], **wf_writers.write(job["kind"], job["brief"])}
        except Exception as error:  # one failed writer must not sink the others
            return {"kind": job.get("kind"), "error": str(error)}
    with ThreadPoolExecutor() as pool:
        return list(pool.map(one, jobs))


COORDINATOR_PROMPT = (
    "You produce a story, a joke and a poem about a topic, combined into one output. "
    "Use dispatch to have writer agents write pieces; dispatch several jobs in one call "
    "so they run in parallel. Read what comes back: if a piece failed or is weak, "
    "dispatch it again with a better brief. Check the fact ids pieces claim with get_fact.\n"
    "Format: a one-line intro, then STORY:, JOKE:, POEM: each followed by the piece.\n"
    'Final answer: {"combined_output": "<the text>"}'
)


def run_agentic() -> None:
    text = shared.run_agent("Coordinator", COORDINATOR_PROMPT, f"Topic: {TOPIC}",
                            {"dispatch": dispatch, "get_fact": t.get_fact}, validate=validate_combined)
    print(f"\n{text}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    (run_agentic if parser.parse_args().mode == "agentic" else run_workflow)()
    shared.print_usage()


if __name__ == "__main__":
    main()
