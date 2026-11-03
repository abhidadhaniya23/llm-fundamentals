"""
Workflows & Agents 02 · Parallelization, every step an agent

The notes' exercise: take one topic, write three different pieces about it
in parallel, then combine them. Here the topic is the office move and the
three pieces are what a real communications team sends out:
    email  120-200 words, at least three real facts, a date and a contact
    chat   one team-chat post of at most 280 characters, with the key date
    FAQ    3-5 questions and answers, each answer citing the fact it uses
All three must pass the plain-language checks, and the Aggregator checks
every fact the pieces claim before combining them.

--mode workflow (default): code fans out and joins, as in the notes.
    topic -+-> Email Writer (agent) -+
           +-> Chat Writer  (agent) -+-> Aggregator (agent) -> combined output
           +-> FAQ Writer   (agent) -+
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

TOPIC = "the office move to Riverside House"
HEADINGS = ("EMAIL:", "CHAT:", "FAQ:")


def validate_combined(final) -> str:
    text = final.get("combined_output") if isinstance(final, dict) else None
    if not isinstance(text, str):
        raise ValueError('final must be {"combined_output": "..."}')
    if missing := [h for h in HEADINGS if h not in text]:
        raise ValueError(f"combined output is missing the headings {missing}")
    return text


AGGREGATOR_PROMPT = (
    "You combine an email, a chat post and an FAQ about one topic into a single pack for the "
    "communications team. Each piece lists the fact ids it uses. Check each id with get_fact "
    "and make sure the piece says the same as the fact (dates, times, places). If a piece "
    "contradicts a fact or the pieces contradict each other, note it under ISSUES. Do not "
    "rewrite the pieces.\n"
    "Format: a one-line intro, then EMAIL:, CHAT:, FAQ: each followed by the piece, then "
    "ISSUES: (or 'none').\n"
    'Final answer: {"combined_output": "<the text>"}'
)


def aggregator(state: dict) -> str:
    pieces = {k: state[k] for k in ("email", "chat", "faq")}
    return shared.run_agent("Aggregator", AGGREGATOR_PROMPT,
                            f"Topic: {state['topic']}\n{json.dumps(pieces, indent=1)}",
                            {"get_fact": t.get_fact}, validate=validate_combined)


# ── Mode 1: code fans out and joins ──────────────────────────────────────────

def run_workflow() -> str:
    state = {"topic": TOPIC}
    briefs = {"email": f"Write the staff email about {TOPIC}",
              "chat": f"Write a team-chat post about {TOPIC}",
              "faq": f"Write an FAQ about {TOPIC}"}
    with ThreadPoolExecutor() as pool:
        futures = {kind: pool.submit(wf_writers.write, kind, brief) for kind, brief in briefs.items()}
        for kind, future in futures.items():
            state[kind] = future.result()
    state["combined_output"] = aggregator(state)
    print(f"\n{state['combined_output']}")
    return state["combined_output"]


# ── Mode 2: a Coordinator agent dispatches ───────────────────────────────────

def dispatch(jobs: list) -> list[dict]:
    """Run writer agents in parallel. jobs is a list like
    [{"kind": "email" | "chat" | "faq", "brief": "what to write"}]. Returns one
    result per job: {"kind", "text", "fact_ids"} or {"kind", "error"}."""
    def one(job: dict) -> dict:
        try:
            return {"kind": job["kind"], **wf_writers.write(job["kind"], job["brief"])}
        except Exception as error:  # one failed writer must not sink the others
            return {"kind": job.get("kind"), "error": str(error)}
    with ThreadPoolExecutor() as pool:
        return list(pool.map(one, jobs))


COORDINATOR_PROMPT = (
    "You produce the communications pack for a topic: a staff email, a team-chat post and an "
    "FAQ, combined into one output. Use dispatch to have writer agents write the pieces; "
    "dispatch several jobs in one call so they run in parallel. Read what comes back: if a "
    "piece failed or contradicts another, dispatch it again with a better brief. Check the "
    "fact ids the pieces claim with get_fact.\n"
    "Format: a one-line intro, then EMAIL:, CHAT:, FAQ: each followed by the piece.\n"
    'Final answer: {"combined_output": "<the text>"}'
)


def run_agentic() -> str:
    text = shared.run_agent("Coordinator", COORDINATOR_PROMPT, f"Topic: {TOPIC}",
                            {"dispatch": dispatch, "get_fact": t.get_fact}, validate=validate_combined)
    print(f"\n{text}")
    return text


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    mode = parser.parse_args().mode
    output = (run_agentic if mode == "agentic" else run_workflow)()
    shared.print_usage()
    shared.save_transcript("wf02", mode, TOPIC, output)


if __name__ == "__main__":
    main()
