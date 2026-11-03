"""
Writer agents shared by the Workflows & Agents labs: email, chat post, FAQ.

Each writer is a real agent (shared.run_agent): it looks up the facts about
the office move, checks its own draft with the plain-language tools, and
its final answer is validated in code. If it skips a check, the validator
hands the error back and it tries again.

Every writer returns {"text": ..., "fact_ids": [...]}.
"""

import re

import shared
import wf_tools as t

_FINAL = ('Final answer: {"text": "<the piece>", "fact_ids": ["O01", ...]} '
          "listing the ids of the facts the piece actually uses.")


def _check_facts(final: dict, minimum: int) -> list[str]:
    ids = final.get("fact_ids") or []
    problems = [f"fact id {i!r} does not exist" for i in ids if t.get_fact(str(i)) is None]
    if len(ids) < minimum:
        problems.append(f"use at least {minimum} facts from lookup_facts, got {len(ids)}")
    return problems


def _check_faq(text: str) -> list[str]:
    questions = [ln for ln in text.splitlines() if ln.strip().startswith("Q:")]
    answers = [ln for ln in text.splitlines() if ln.strip().startswith("A:")]
    problems = []
    if not 3 <= len(questions) <= 5 or len(answers) != len(questions):
        problems.append(f"need 3 to 5 'Q:' lines, each followed by one 'A:' line "
                        f"(got {len(questions)} Q and {len(answers)} A)")
    for answer in answers:
        cited = re.findall(r"\[(O\d\d)\]", answer)
        if not cited or any(t.get_fact(c) is None for c in cited):
            problems.append(f"answer must end with the fact id it is based on, e.g. [O07]: {answer[:50]!r}")
    return problems


def _validator(kind: str):
    def validate(final):
        if not isinstance(final, dict) or not final.get("text"):
            raise ValueError('final must be {"text": ..., "fact_ids": [...]}')
        text = final["text"]
        problems = t.plain_language_problems(text)
        if kind == "email":
            problems += _check_facts(final, 3)
            if not 120 <= (n := t.count_words(text)) <= 200:
                problems.append(f"{n} words, must be 120-200")
            problems += [f"missing {m}" for m in t.check_essentials(text)["missing"]]
        elif kind == "chat":
            problems += _check_facts(final, 1)
            if (n := t.count_chars(text)) > 280:
                problems.append(f"{n} characters, max 280")
            if "a date" in t.check_essentials(text)["missing"]:
                problems.append("missing a date")
        elif kind == "faq":
            problems += _check_facts(final, 3)
            problems += _check_faq(text)
        if problems:
            raise ValueError("\n".join(problems))
        return final
    return validate


_PLAIN = " Write in plain language: no jargon (check_jargon) and no sentence over 25 words (check_sentences)."

WRITERS = {
    "email": ("Email Writer",
              "You write the staff email announcing the office move: 120 to 200 words. Use at "
              "least three facts from lookup_facts, and say when it happens and who to contact. "
              "Check the length with count_words." + _PLAIN,
              {"lookup_facts": t.lookup_facts, "count_words": t.count_words, "check_jargon": t.check_jargon,
               "check_sentences": t.check_sentences, "check_essentials": t.check_essentials}),
    "chat": ("Chat Writer",
             "You write one short team-chat post about the office move: at most 280 characters, "
             "including the most important date. Check it with count_chars." + _PLAIN,
             {"lookup_facts": t.lookup_facts, "count_chars": t.count_chars, "check_jargon": t.check_jargon}),
    "faq": ("FAQ Writer",
            "You write an FAQ about the office move: 3 to 5 questions people will really ask. "
            "Format each as a line 'Q: ...' followed by a line 'A: ...', and end every answer "
            "with the id of the fact it is based on, e.g. [O07]. Only answer from the facts." + _PLAIN,
            {"lookup_facts": t.lookup_facts, "check_jargon": t.check_jargon,
             "check_sentences": t.check_sentences}),
}


def write(kind: str, brief: str) -> dict:
    """Run the writer agent for one kind: 'email', 'chat' or 'faq'."""
    label, prompt, tools = WRITERS[kind]
    shared.step(label, brief)
    return shared.run_agent(label, prompt + "\n" + _FINAL, brief, tools, validate=_validator(kind))


def write_email(brief: str) -> dict:
    """Ask the Email Writer agent for a 120-200 word staff email. brief says what to write."""
    return write("email", brief)


def write_chat(brief: str) -> dict:
    """Ask the Chat Writer agent for a team-chat post of at most 280 characters."""
    return write("chat", brief)


def write_faq(brief: str) -> dict:
    """Ask the FAQ Writer agent for 3-5 questions and answers, each citing a fact."""
    return write("faq", brief)
