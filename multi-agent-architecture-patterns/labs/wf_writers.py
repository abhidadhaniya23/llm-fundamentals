"""
Writer agents shared by the Workflows & Agents labs: joke, story, poem.

Each writer is a real agent (shared.run_agent): it looks up facts, checks
its own draft with tools, and its final answer is validated in code. If it
skips a check, the validator hands the error back and it tries again.

Every writer returns {"text": ..., "fact_ids": [...]}.
"""

import shared
import wf_tools as t

_FINAL = ('Final answer: {"text": "<the piece>", "fact_ids": ["F01", ...]} '
          "listing the ids of the cat facts the piece actually uses.")


def _check_facts(final: dict, minimum: int) -> list[str]:
    ids = final.get("fact_ids") or []
    problems = [f"fact id {i!r} does not exist" for i in ids if t.get_fact(str(i)) is None]
    if len(ids) < minimum:
        problems.append(f"use at least {minimum} real cat fact(s) from lookup_facts, got {len(ids)}")
    return problems


def _validator(kind: str):
    def validate(final):
        if not isinstance(final, dict) or not final.get("text"):
            raise ValueError('final must be {"text": ..., "fact_ids": [...]}')
        text = final["text"]
        problems = []
        if kind == "joke":
            problems += _check_facts(final, 1)
            if not t.check_punchline(text)["has_punchline"]:
                problems.append("no punchline ('?' or '!')")
            if (o := t.check_originality(text))["original"] is False:
                problems.append(f"too close to a known joke: {o['closest_known_joke']!r}")
            if t.count_words(text) > 50:
                problems.append(f"{t.count_words(text)} words, max 50")
        elif kind == "story":
            problems += _check_facts(final, 2)
            if not 150 <= (n := t.count_words(text)) <= 200:
                problems.append(f"{n} words, must be 150-200")
        elif kind == "poem":
            problems += _check_facts(final, 1)
            problems += t.check_limerick(text)["problems"]
        if not (s := t.kid_safe(text))["safe"]:
            problems.append(f"not kid-safe: {s['flagged']}")
        if problems:
            raise ValueError("\n".join(problems))
        return final
    return validate


WRITERS = {
    "joke": ("Joke Writer",
             "You write one short, original cat joke (max 50 words) with a clear punchline. "
             "Build it on a real cat fact. Check it with check_originality and "
             "check_punchline before you hand it in.",
             {"lookup_facts": t.lookup_facts, "find_puns": t.find_puns,
              "check_originality": t.check_originality, "check_punchline": t.check_punchline,
              "count_words": t.count_words}),
    "story": ("Story Writer",
              "You write one short story of 150 to 200 words. Weave in at least two real "
              "cat facts. Check the length with count_words before you hand it in.",
              {"lookup_facts": t.lookup_facts, "count_words": t.count_words, "kid_safe": t.kid_safe}),
    "poem": ("Poem Writer",
             "You write one limerick: 5 lines, rhyme scheme AABBA, lines 1, 2 and 5 longer "
             "than lines 3 and 4. Build it on a real cat fact. Pick clear, simple rhymes and "
             "check the poem with check_limerick before you hand it in.",
             {"lookup_facts": t.lookup_facts, "rhymes": t.rhymes, "syllables": t.syllables,
              "check_limerick": t.check_limerick}),
}


def write(kind: str, brief: str) -> dict:
    """Run the writer agent for one kind: 'joke', 'story' or 'poem'."""
    label, prompt, tools = WRITERS[kind]
    shared.step(label, brief)
    return shared.run_agent(label, prompt + " Everything must be suitable for children.\n" + _FINAL,
                            brief, tools, validate=_validator(kind))


def write_joke(brief: str) -> dict:
    """Ask the Joke Writer agent for an original cat joke. brief says what to write and for whom."""
    return write("joke", brief)


def write_story(brief: str) -> dict:
    """Ask the Story Writer agent for a 150-200 word story. brief says what to write and for whom."""
    return write("story", brief)


def write_poem(brief: str) -> dict:
    """Ask the Poem Writer agent for a limerick. brief says what to write and for whom."""
    return write("poem", brief)
