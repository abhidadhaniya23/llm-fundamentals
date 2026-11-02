"""
Workflows & Agents 01 · Prompt Chaining, every step an agent

The notes' exercise: take a topic, write a joke, check it has a punchline,
improve it with wordplay, then add a surprising twist. Here the bar is
higher, so each step needs tools: the joke must rest on a real cat fact, be
original (checked against known jokes), stay kid-safe and under 40 words.

--mode workflow (default): code keeps the chain from the notes.
    topic -> Writer (agent) -> gate: check_punchline (code) --Fail--> stop
                               --Pass--> Wordplay (agent) -> Polisher (agent)

--mode agentic: an Editor agent runs the chain itself. The three step
    agents are its tools; it decides the order, repeats, and when to stop.
    Code still validates the final joke.

Run it:
    uv run labs/wf01_prompt_chaining.py
    uv run labs/wf01_prompt_chaining.py --mode agentic
"""

import argparse

import shared
import wf_tools as t

TOPIC = "cats"
MAX_WORDS = 40
JOKE_FINAL = 'Final answer: {"joke": "<the joke>"}'


def final_checks(joke: str) -> list[str]:
    """The bar every finished joke must clear, checked in code."""
    problems = []
    if not t.check_punchline(joke)["has_punchline"]:
        problems.append("no punchline ('?' or '!')")
    if not (o := t.check_originality(joke))["original"]:
        problems.append(f"too close to a known joke ({o['overlap']}): {o['closest_known_joke']!r}")
    if (n := t.count_words(joke)) > MAX_WORDS:
        problems.append(f"{n} words, max {MAX_WORDS}")
    if not (s := t.kid_safe(joke))["safe"]:
        problems.append(f"not kid-safe: {s['flagged']}")
    return problems


def joke_of(final) -> str:
    if not isinstance(final, dict) or not isinstance(final.get("joke"), str):
        raise ValueError('final must be {"joke": "<the joke>"}')
    return final["joke"]


def validate_original(final) -> str:
    joke = joke_of(final)
    if not (o := t.check_originality(joke))["original"]:
        raise ValueError(f"too close to a known joke: {o['closest_known_joke']!r}")
    return joke


def validate_finished(final) -> str:
    joke = joke_of(final)
    if problems := final_checks(joke):
        raise ValueError("\n".join(problems))
    return joke


# ── The three step agents ────────────────────────────────────────────────────

def generate_joke(topic: str) -> str:
    """Writer agent: a first joke about the topic, built on a real cat fact."""
    return shared.run_agent(
        "Writer", "You write a short joke about the given topic. Look up real cat facts "
        "with lookup_facts and build the joke on one of them. " + JOKE_FINAL,
        f"Write a short joke about {topic}",
        {"lookup_facts": t.lookup_facts, "check_punchline": t.check_punchline},
        validate=joke_of)


def improve_joke(joke: str) -> str:
    """Wordplay agent: make the joke funnier with puns, without copying a known joke."""
    return shared.run_agent(
        "Wordplay", "Make this joke funnier by adding wordplay. Find cat puns for words "
        "in the joke with find_puns. The result must stay original: check it with "
        "check_originality. " + JOKE_FINAL,
        joke, {"find_puns": t.find_puns, "check_originality": t.check_originality},
        validate=validate_original)


def polish_joke(joke: str) -> str:
    """Polisher agent: add a surprising twist, keep it short, kid-safe and original."""
    return shared.run_agent(
        "Polisher", f"Add a surprising twist to this joke. Keep it under {MAX_WORDS} words, "
        "kid-safe and original, and keep the punchline. Check with the tools before you "
        "hand it in. " + JOKE_FINAL,
        joke, {"count_words": t.count_words, "kid_safe": t.kid_safe,
               "check_originality": t.check_originality, "check_punchline": t.check_punchline},
        validate=validate_finished)


# ── Mode 1: code keeps the chain ─────────────────────────────────────────────

def run_workflow() -> None:
    state = {"topic": TOPIC}
    state["joke"] = generate_joke(state["topic"])
    print(f"\nInitial joke:\n{state['joke']}")

    # The gate is code, exactly as in the notes.
    if not t.check_punchline(state["joke"])["has_punchline"]:
        print("\nJoke failed quality gate - no punchline detected!")
        return
    state["improved_joke"] = improve_joke(state["joke"])
    print(f"\n--- --- ---\nImproved joke:\n{state['improved_joke']}")
    state["final_joke"] = polish_joke(state["improved_joke"])
    print(f"\n--- --- ---\nFinal joke:\n{state['final_joke']}")


# ── Mode 2: an Editor agent runs the chain ───────────────────────────────────

EDITOR_PROMPT = (
    "You are a comedy editor. Produce one finished joke about the topic. You have "
    "three writers as tools: generate_joke (first draft), improve_joke (wordplay) "
    "and polish_joke (twist and final polish). Use them in whatever order helps, "
    "repeat a step if the result is weak, and check drafts yourself. A finished "
    f"joke has a punchline, is original, kid-safe and at most {MAX_WORDS} words.\n"
    + JOKE_FINAL
)


def run_agentic() -> None:
    tools = {"generate_joke": generate_joke, "improve_joke": improve_joke, "polish_joke": polish_joke,
             "check_punchline": t.check_punchline, "check_originality": t.check_originality,
             "count_words": t.count_words, "kid_safe": t.kid_safe}
    joke = shared.run_agent("Editor", EDITOR_PROMPT, f"Topic: {TOPIC}", tools,
                            validate=validate_finished)
    print(f"\nFinal joke:\n{joke}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    (run_agentic if parser.parse_args().mode == "agentic" else run_workflow)()
    shared.print_usage()


if __name__ == "__main__":
    main()
