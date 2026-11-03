"""
Workflows & Agents 03 · Routing, every step an agent

The notes' exercise: classify an input and send it to one of three
specialists. Here the inputs are employees' questions about the office
move, and the specialists are the IT, Facilities and HR help desks. Some
questions only make sense once you know who is asking (a new starter, a
part-timer, a wheelchair user), so the Router looks up the employee first.
Each specialist searches its own help articles and must cite one it read.

--mode workflow (default): the Router agent decides, code branches.
    request -> Router (agent, get_employee) -> Route{dept, brief}
            -> if/elif (code) -> IT | Facilities | HR desk (agent, search_kb)

--mode agentic: the Router hands off itself. The desks are its tools; it
    calls one and returns that desk's reply. Code checks it really did.

Run it:
    uv run labs/wf03_routing.py
    uv run labs/wf03_routing.py --mode agentic --request 2
"""

import argparse
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t

REQUESTS = [
    ("e1", "My second monitor is still at Station Road. Do I need to bring it over myself?"),
    ("e3", "Where can I park on my first day, and how do I get out of the building if there's a fire?"),
    ("e5", "I only work Monday to Wednesday. Can I still work from home two days a week?"),
    ("e2", "I start on 7 December. What do I need to bring and where do I go?"),
    ("e6", "Is there somewhere safe to leave my bike?"),
]

DESKS = {"it": "IT Desk", "facilities": "Facilities Desk", "hr": "HR Desk"}


class Route(BaseModel):
    dept: Literal["it", "facilities", "hr"] = Field(description="The help desk that should answer")
    brief: str = Field(description="What the desk should answer, and what it needs to know about the person")


ROUTER_PROMPT = (
    "Route an employee's question about the office move to the IT, Facilities or HR help desk. "
    "Look up the employee with get_employee first: their role, how they work and their notes "
    "can change which desk should answer and what the answer must cover. Then write a brief "
    "for the desk: the question, who is asking, and anything about them that matters."
)


# ── A help-desk specialist ───────────────────────────────────────────────────

def answer(dept: str, brief: str) -> dict:
    """One help desk answers, citing a help article it actually read."""
    read: set[str] = set()

    def search(query: str) -> list[dict]:
        """Search this desk's help articles. Returns up to 3 {id, title}."""
        return t.search_kb(dept, query)

    def read_tracked(article_id: str) -> dict | None:
        """The full text of one help article, by id."""
        article = t.read_article(article_id)
        if article:
            read.add(article["id"])
        return article

    def validate(final) -> dict:
        reply = final.get("reply") if isinstance(final, dict) else None
        if not isinstance(reply, str):
            raise ValueError('final must be {"reply": "..."}')
        cited = t.cited_articles(reply)
        problems = t.plain_language_problems(reply)
        if not cited:
            problems.append("cite the help article(s) you used, e.g. [FAC-01]")
        if unread := cited - read:
            problems.append(f"you cite {sorted(unread)} but never read them with read_article")
        if (n := t.count_words(reply)) > 150:
            problems.append(f"{n} words, max 150")
        if problems:
            raise ValueError("\n".join(problems))
        return {"dept": dept, "reply": reply}

    label = DESKS[dept]
    shared.step(label, brief)
    return shared.run_agent(
        label, f"You answer staff questions for the {label}. Search your help articles, read "
        "the ones that fit, and answer only from them, citing each as [ID]. Address the person "
        "by name, in plain language, at most 150 words. If part of the question belongs to "
        "another desk, say which one.\n" + 'Final answer: {"reply": "..."}',
        brief, {"search_kb": search, "read_article": read_tracked}, validate=validate)


def ask_it(brief: str) -> dict:
    """Send the question to the IT Desk agent. brief: the question and who is asking."""
    return answer("it", brief)


def ask_facilities(brief: str) -> dict:
    """Send the question to the Facilities Desk agent. brief: the question and who is asking."""
    return answer("facilities", brief)


def ask_hr(brief: str) -> dict:
    """Send the question to the HR Desk agent. brief: the question and who is asking."""
    return answer("hr", brief)


# ── Mode 1: the Router agent decides, code branches ──────────────────────────

def validate_route(final) -> Route:
    try:
        return Route.model_validate(final)
    except ValidationError as error:
        raise ValueError(str(error)) from None


def llm_call_router(state: dict) -> None:
    route = shared.run_agent(
        "Router", ROUTER_PROMPT + '\nFinal answer: {"dept": "it" | "facilities" | "hr", "brief": ""}',
        f"Employee id: {state['employee']}\nQuestion: {state['input']}",
        {"get_employee": t.get_employee}, validate=validate_route)
    state["decision"], state["brief"] = route.dept, route.brief
    shared.step("Router", f"-> {route.dept}: {route.brief}")


def route_and_answer(state: dict) -> None:
    # The conditional edge, hand-rolled: a plain if/elif.
    if state["decision"] == "it":
        state["output"] = ask_it(state["brief"])
    elif state["decision"] == "facilities":
        state["output"] = ask_facilities(state["brief"])
    elif state["decision"] == "hr":
        state["output"] = ask_hr(state["brief"])


def run_workflow(employee: str, request: str) -> dict:
    state = {"employee": employee, "input": request}
    llm_call_router(state)
    route_and_answer(state)
    print(f"\n[{state['decision']}]\n{state['output']['reply']}")
    return state["output"]


# ── Mode 2: the Router agent hands off itself ────────────────────────────────

def run_agentic(employee: str, request: str) -> dict:
    handed_off: dict[str, dict] = {}  # code records what the desks really returned

    def recorded(dept: str, desk):
        def call(brief: str) -> dict:
            handed_off[dept] = desk(brief)
            return handed_off[dept]
        call.__doc__ = desk.__doc__
        return call

    def validate(final):
        dept = final.get("routed_to") if isinstance(final, dict) else None
        if dept not in handed_off:
            raise ValueError(f"routed_to {dept!r} was never called; call a desk and return its reply")
        return dept

    tools = {"get_employee": t.get_employee, "ask_it": recorded("it", ask_it),
             "ask_facilities": recorded("facilities", ask_facilities), "ask_hr": recorded("hr", ask_hr)}
    dept = shared.run_agent(
        "Router", ROUTER_PROMPT + " Then call the matching desk tool with that brief. If the "
        "question has parts for two desks, call both.\n"
        'Final answer: {"routed_to": "it" | "facilities" | "hr"} (the main desk)',
        f"Employee id: {employee}\nQuestion: {request}", tools, validate=validate)
    # The reply the employee gets comes from the desks, not from the Router's retelling.
    for name, result in handed_off.items():
        print(f"\n[{name}]\n{result['reply']}")
    return {"routed_to": dept, "replies": handed_off}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    parser.add_argument("--request", type=int, help=f"run only request 1-{len(REQUESTS)}")
    args = parser.parse_args()
    chosen = [REQUESTS[args.request - 1]] if args.request else REQUESTS
    outputs = []
    for employee, request in chosen:
        print(f"\n══ {employee}: {request!r}")
        outputs.append((run_agentic if args.mode == "agentic" else run_workflow)(employee, request))
    shared.print_usage()
    shared.save_transcript("wf03", args.mode, chosen, outputs)


if __name__ == "__main__":
    main()
