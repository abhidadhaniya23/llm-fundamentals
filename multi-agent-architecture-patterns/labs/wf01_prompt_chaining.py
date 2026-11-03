"""
Workflows & Agents 01 · Prompt Chaining, every step an agent

The notes' exercise: take a topic, write a first version, check it with a
gate, improve it, then polish it. Here the topic is the office move: the
move team's internal memo (full of jargon) has to become a staff
announcement. Each step needs tools: the facts must be real (lookup_facts),
the language plain (check_jargon, check_sentences), the notice complete
(check_essentials) and at most 150 words.

--mode workflow (default): code keeps the chain from the notes.
    memo -> Drafter (agent) -> gate: check_essentials (code) --Fail--> stop
                               --Pass--> Plain-language (agent) -> Final editor (agent)

--mode agentic: an Editor-in-chief agent runs the chain itself. The three
    step agents are its tools; it decides the order, repeats, and when to
    stop. Code still validates the final notice.

Run it:
    uv run labs/wf01_prompt_chaining.py
    uv run labs/wf01_prompt_chaining.py --mode agentic
"""

import argparse

import shared
import wf_tools as t

MEMO = (
    "Internal memo from the move team. Going forward, in order to facilitate a seamless "
    "relocation, all stakeholders are kindly requested to utilise the crates provided and "
    "action the packing of personal items prior to the close of business on the last day at "
    "Station Road. IT will leverage its own resources for hardware. Further details re desks, "
    "badges and the commencement date at the new premises will be communicated in due course."
)
MAX_WORDS = 150
NOTICE_FINAL = 'Final answer: {"notice": "<the notice>"}'


def final_checks(notice: str) -> list[str]:
    """The bar every finished notice must clear, checked in code."""
    problems = [f"missing {m}" for m in t.check_essentials(notice)["missing"]]
    problems += t.plain_language_problems(notice)
    if (n := t.count_words(notice)) > MAX_WORDS:
        problems.append(f"{n} words, max {MAX_WORDS}")
    return problems


def notice_of(final) -> str:
    if not isinstance(final, dict) or not isinstance(final.get("notice"), str):
        raise ValueError('final must be {"notice": "<the notice>"}')
    return final["notice"]


def validate_draft(final) -> str:
    notice = notice_of(final)
    ids = final.get("fact_ids") or []
    if len(ids) < 3 or any(t.get_fact(str(i)) is None for i in ids):
        raise ValueError("list at least 3 real fact ids from lookup_facts in fact_ids")
    return notice


def validate_plain(final) -> str:
    notice = notice_of(final)
    if problems := t.plain_language_problems(notice):
        raise ValueError("\n".join(problems))
    return notice


def validate_finished(final) -> str:
    notice = notice_of(final)
    if problems := final_checks(notice):
        raise ValueError("\n".join(problems))
    return notice


# ── The three step agents ────────────────────────────────────────────────────

def draft_notice(memo: str) -> str:
    """Drafter agent: turn the memo into a first staff notice, using the real facts."""
    return shared.run_agent(
        "Drafter", "You turn an internal memo into a first draft of a staff notice. The memo is "
        "vague: look up the real dates, places and contacts with lookup_facts and put them in "
        "where the memo is vague. Keep the memo's own wording otherwise; later steps fix the "
        "style. "
        'Final answer: {"notice": "<the draft>", "fact_ids": ["O01", ...]}',
        memo, {"lookup_facts": t.lookup_facts, "check_essentials": t.check_essentials},
        validate=validate_draft)


def make_plain(notice: str) -> str:
    """Plain-language agent: rewrite the notice without jargon or long sentences."""
    return shared.run_agent(
        "Plain-language", "Rewrite this notice in plain language. Replace every term that "
        "check_jargon finds, and split any sentence that check_sentences says is too long. "
        "Keep every fact. " + NOTICE_FINAL,
        notice, {"check_jargon": t.check_jargon, "check_sentences": t.check_sentences},
        validate=validate_plain)


def polish_notice(notice: str) -> str:
    """Final editor agent: add a short 'What you need to do' list and finish the notice."""
    return shared.run_agent(
        "Final editor", "Finish this staff notice. Add a short 'What you need to do' list, keep "
        f"it at most {MAX_WORDS} words, make sure it says when and who to contact, and keep it "
        "in plain language. Check every fact you keep with get_fact. " + NOTICE_FINAL,
        notice, {"count_words": t.count_words, "check_essentials": t.check_essentials,
                 "check_jargon": t.check_jargon, "check_sentences": t.check_sentences,
                 "get_fact": t.get_fact, "lookup_facts": t.lookup_facts},
        max_steps=25, validate=validate_finished)


# ── Mode 1: code keeps the chain ─────────────────────────────────────────────

def run_workflow() -> str | None:
    state = {"memo": MEMO}
    state["draft"] = draft_notice(state["memo"])
    print(f"\nDraft:\n{state['draft']}")

    # The gate is code, as in the notes: a notice with no date or contact stops here.
    if not t.check_essentials(state["draft"])["ok"]:
        print("\nDraft failed the gate - no date or contact address!")
        return None
    state["plain"] = make_plain(state["draft"])
    print(f"\n--- --- ---\nPlain language:\n{state['plain']}")
    state["final"] = polish_notice(state["plain"])
    print(f"\n--- --- ---\nFinal notice:\n{state['final']}")
    return state["final"]


# ── Mode 2: an Editor-in-chief agent runs the chain ──────────────────────────

EDITOR_PROMPT = (
    "You are the editor-in-chief for staff communications. Produce one finished staff notice "
    "from the memo. You have three agents as tools: draft_notice (first draft from the memo), "
    "make_plain (plain language) and polish_notice (action list and final check). Use them in "
    "whatever order helps, repeat a step if the result is weak, and check drafts yourself. Pass "
    "each agent the full text it should work on. A finished notice says when and who to "
    f"contact, is in plain language and at most {MAX_WORDS} words. Hand in the text an agent "
    "returned; do not write the notice yourself.\n" + NOTICE_FINAL
)


def run_agentic() -> str:
    tools = {"draft_notice": draft_notice, "make_plain": make_plain, "polish_notice": polish_notice,
             "check_essentials": t.check_essentials, "check_jargon": t.check_jargon,
             "check_sentences": t.check_sentences, "count_words": t.count_words,
             "lookup_facts": t.lookup_facts}
    notice = shared.run_agent("Editor-in-chief", EDITOR_PROMPT, f"Memo:\n{MEMO}", tools,
                              max_steps=20, validate=validate_finished)
    print(f"\nFinal notice:\n{notice}")
    return notice


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    mode = parser.parse_args().mode
    output = (run_agentic if mode == "agentic" else run_workflow)()
    shared.print_usage()
    shared.save_transcript("wf01", mode, MEMO, output)


if __name__ == "__main__":
    main()
