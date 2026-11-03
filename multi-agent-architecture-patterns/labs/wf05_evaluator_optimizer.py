"""
Workflows & Agents 05 · Evaluator-Optimizer, every step an agent

The notes' exercise: one LLM writes, another grades it and gives feedback,
loop until it passes. Here the writer drafts the notice for the first fire
drill at the new building, and the Reviewer grades it against a style-guide
rubric it must check with tools: facts right, plain language, at most 120
words, says what/when/where/what to do, and an accessibility note.

--mode workflow (default): code runs the loop, as in the notes.
    task -> Writer (agent) -> Reviewer (agent) --approved--> done
                ^                   |
                +---- feedback -----+  (max 4 rounds)

--mode agentic: the Writer owns the loop. The Reviewer is its tool
    review_notice; it decides when to resubmit. Code still checks the notice
    it hands in is one the Reviewer approved (trust, but verify).

Run it:
    uv run labs/wf05_evaluator_optimizer.py
    uv run labs/wf05_evaluator_optimizer.py --mode agentic
"""

import argparse
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t

TASK = "Write the staff notice for the first fire drill at Riverside House"
MAX_ROUNDS = 4


class Feedback(BaseModel):
    grade: Literal["approved", "needs changes"] = Field(description="Decide if the notice can be sent.")
    feedback: str = Field(description="If it needs changes, say which rule failed and how to fix it.")


RUBRIC = """A notice is "approved" only if ALL of these hold:
1. Correct: every date, time and place matches a fact (check with lookup_facts / get_fact).
2. Complete: it says what is happening, when, where to go, and what people must do.
3. Inclusive: it tells people who may need help leaving the building what to do.
4. Plain: check_jargon finds nothing and check_sentences finds no sentence over 25 words.
5. Short: at most 120 words (count_words).
Otherwise it "needs changes", and the feedback names which rule failed and how to fix it."""


# ── The two agents ───────────────────────────────────────────────────────────

def notice_of(final) -> str:
    if not isinstance(final, dict) or not isinstance(final.get("notice"), str):
        raise ValueError('final must be {"notice": "<the notice>"}')
    return final["notice"]


def llm_call_generator(state: dict) -> None:
    """Writer agent drafts the notice, using the feedback if there is any."""
    task = state["task"]
    if state.get("feedback"):
        task += f", but take into account the feedback: {state['feedback']}\nPrevious notice: {state['notice']}"
    state["notice"] = shared.run_agent(
        "Writer", "You write short staff notices. Look up the facts with lookup_facts and use "
        "only those.\n" + 'Final answer: {"notice": ""}',
        task, {"lookup_facts": t.lookup_facts, "get_fact": t.get_fact}, validate=notice_of)


def review(notice: str) -> Feedback:
    def validate(final) -> Feedback:
        try:
            return Feedback.model_validate(final)
        except ValidationError as error:
            raise ValueError(str(error)) from None

    return shared.run_agent(
        "Reviewer", "You are the communications reviewer. Grade the notice against this rubric, "
        "running the checks with your tools rather than guessing.\n" + RUBRIC +
        '\nFinal answer: {"grade": "approved" | "needs changes", "feedback": ""}',
        f"Review the notice:\n{notice}",
        {"lookup_facts": t.lookup_facts, "get_fact": t.get_fact, "check_jargon": t.check_jargon,
         "check_sentences": t.check_sentences, "count_words": t.count_words,
         "check_essentials": t.check_essentials}, validate=validate)


def llm_call_evaluator(state: dict) -> None:
    """Reviewer agent grades the notice."""
    grade = review(state["notice"])
    state["grade"], state["feedback"] = grade.grade, grade.feedback
    shared.step("Reviewer", f"{grade.grade}: {grade.feedback}")


# ── Mode 1: code runs the loop ───────────────────────────────────────────────

def run_workflow() -> str:
    state = {"task": TASK}
    for round_no in range(1, MAX_ROUNDS + 1):
        shared.step("Loop", f"round {round_no}")
        llm_call_generator(state)
        llm_call_evaluator(state)
        if state["grade"] == "approved":  # Accepted
            break
        # Needs changes + feedback: go round again
    else:
        print(f"\nNo notice was approved in {MAX_ROUNDS} rounds; the last one:")
    print(f"\n{state['notice']}")
    return state["notice"]


# ── Mode 2: the Writer owns the loop ─────────────────────────────────────────

def run_agentic() -> str:
    graded: dict[str, str] = {}  # code's own record of every grade the Reviewer gave

    def review_notice(notice: str) -> dict:
        """Send a notice to the Reviewer agent. Returns {grade, feedback}."""
        result = review(notice)
        graded[notice.strip()] = result.grade
        shared.step("Reviewer", f"{result.grade}: {result.feedback}")
        return result.model_dump()

    def validate(final) -> str:
        notice = final.get("notice", "").strip() if isinstance(final, dict) else ""
        if graded.get(notice) != "approved":
            raise ValueError("hand in only a notice that review_notice approved, word for word")
        return notice

    notice = shared.run_agent(
        "Writer", "You write the staff notice and get it reviewed with review_notice. Improve it "
        "using the feedback and resubmit until it is approved. Look up the facts with "
        "lookup_facts and use only those.\n"
        'Final answer: {"notice": "<the notice exactly as approved>"}',
        TASK, {"lookup_facts": t.lookup_facts, "get_fact": t.get_fact, "review_notice": review_notice},
        max_steps=20, validate=validate)
    print(f"\n{notice}")
    return notice


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    mode = parser.parse_args().mode
    output = (run_agentic if mode == "agentic" else run_workflow)()
    shared.print_usage()
    shared.save_transcript("wf05", mode, TASK, output)


if __name__ == "__main__":
    main()
