"""
Workflows & Agents 05 · Evaluator-Optimizer, every step an agent

The notes' exercise: generate a joke, have an evaluator grade it "funny" or
"not funny" with feedback, loop until funny. A bare "grade this joke" is
pure taste, so here the Evaluator grades against a rubric with checks it
must run: originality against known jokes, a real cat fact, kid-safety,
length. The Generator has its own tools: facts and puns.

--mode workflow (default): code runs the loop, as in the notes.
    topic -> Generator (agent) -> Evaluator (agent) --funny--> done
                 ^                     |
                 +---- feedback -------+  (max 4 rounds)

--mode agentic: the Generator owns the loop. The Evaluator is its tool
    grade_joke; it decides when to resubmit. Code still checks the joke it
    hands in is one the Evaluator graded "funny" (trust, but verify).

Run it:
    uv run labs/wf05_evaluator_optimizer.py
    uv run labs/wf05_evaluator_optimizer.py --mode agentic
"""

import argparse
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t

TOPIC = "Cats"
MAX_ROUNDS = 4


class Feedback(BaseModel):
    grade: Literal["funny", "not funny"] = Field(description="Decide if the joke is funny or not.")
    feedback: str = Field(description="If the joke is not funny, provide feedback on how to improve it.")


RUBRIC = """A joke is "funny" only if ALL of these hold:
1. Original: check_originality says original (overlap below 0.5).
2. Grounded: it rests on a real cat fact (find it with lookup_facts).
3. Kid-safe: kid_safe says safe.
4. Short: at most 40 words (count_words).
5. Surprise: the punchline turns the setup in a way you did not see coming.
Otherwise it is "not funny", and the feedback names which rule failed and how to fix it."""


# ── The two agents ───────────────────────────────────────────────────────────

def llm_call_generator(state: dict) -> None:
    """Generator agent writes a joke, using the feedback if there is any."""
    task = f"Write a joke about {state['topic']}"
    if state.get("feedback"):
        task += f" but take into account the feedback: {state['feedback']}\nPrevious joke: {state['joke']}"
    state["joke"] = shared.run_agent(
        "Generator", "You write one short joke. Ground it in a real cat fact (lookup_facts) "
        "and use cat puns (find_puns) where they help.\n" + 'Final answer: {"joke": ""}',
        task, {"lookup_facts": t.lookup_facts, "find_puns": t.find_puns},
        validate=joke_of)


def joke_of(final) -> str:
    if not isinstance(final, dict) or not isinstance(final.get("joke"), str):
        raise ValueError('final must be {"joke": "<the joke>"}')
    return final["joke"]


def evaluate(joke: str) -> Feedback:
    def validate(final) -> Feedback:
        try:
            return Feedback.model_validate(final)
        except ValidationError as error:
            raise ValueError(str(error)) from None

    return shared.run_agent(
        "Evaluator", "You are a strict comedy judge. Grade the joke against this rubric, "
        "running the checks with your tools rather than guessing.\n" + RUBRIC +
        '\nFinal answer: {"grade": "funny" | "not funny", "feedback": ""}',
        f"Grade the joke {joke}",
        {"check_originality": t.check_originality, "lookup_facts": t.lookup_facts,
         "kid_safe": t.kid_safe, "count_words": t.count_words}, validate=validate)


def llm_call_evaluator(state: dict) -> None:
    """Evaluator agent grades the joke."""
    grade = evaluate(state["joke"])
    state["funny_or_not"], state["feedback"] = grade.grade, grade.feedback
    shared.step("Evaluator", f"{grade.grade}: {grade.feedback}")


# ── Mode 1: code runs the loop ───────────────────────────────────────────────

def run_workflow() -> None:
    state = {"topic": TOPIC}
    for round_no in range(1, MAX_ROUNDS + 1):
        shared.step("Loop", f"round {round_no}")
        llm_call_generator(state)
        llm_call_evaluator(state)
        if state["funny_or_not"] == "funny":  # Accepted
            break
        # Rejected + Feedback: go round again
    else:
        print(f"\nNo joke passed in {MAX_ROUNDS} rounds; the last one:")
    print(f"\n{state['joke']}")


# ── Mode 2: the Generator owns the loop ──────────────────────────────────────

def run_agentic() -> None:
    graded: dict[str, str] = {}  # code's own record of every grade the Evaluator gave

    def grade_joke(joke: str) -> dict:
        """Send a joke to the Evaluator agent. Returns {grade, feedback}."""
        result = evaluate(joke)
        graded[joke.strip()] = result.grade
        shared.step("Evaluator", f"{result.grade}: {result.feedback}")
        return result.model_dump()

    def validate(final) -> str:
        joke = final.get("joke", "").strip() if isinstance(final, dict) else ""
        if graded.get(joke) != "funny":
            raise ValueError("hand in only a joke that grade_joke graded 'funny', word for word")
        return joke

    joke = shared.run_agent(
        "Generator", "You write one short joke about the topic and get it graded with "
        "grade_joke. Improve it using the feedback and resubmit until it is graded funny. "
        "Ground it in a real cat fact (lookup_facts) and use puns (find_puns) where they help.\n"
        'Final answer: {"joke": "<the joke exactly as graded>"}',
        f"Topic: {TOPIC}",
        {"lookup_facts": t.lookup_facts, "find_puns": t.find_puns, "grade_joke": grade_joke},
        max_steps=20, validate=validate)
    print(f"\n{joke}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    (run_agentic if parser.parse_args().mode == "agentic" else run_workflow)()
    shared.print_usage()


if __name__ == "__main__":
    main()
