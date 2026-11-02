"""
Workflows & Agents 03 · Routing, every step an agent

The notes' exercise: route "Write me a joke about cats" to a story, joke or
poem writer. That request names its own route, so here most requests are
vaguer and come from readers with profiles. The Router has to look up who is
asking (get_reader) before it can pick a writer and write a brief.

--mode workflow (default): the Router agent decides, code branches.
    request -> Router (agent, get_reader) -> Route{step, brief}
            -> if/elif (code) -> Story | Joke | Poem Writer (agent)

--mode agentic: the Router hands off itself. The writers are its tools;
    it calls one and returns that writer's piece. Code checks it really did.

Run it:
    uv run labs/wf03_routing.py
    uv run labs/wf03_routing.py --mode agentic --request 2
"""

import argparse
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t
import wf_writers

REQUESTS = [
    ("r1", "Write me a joke about cats"),
    ("r2", "Can I have something about cats please? With rhymes!"),
    ("r3", "Tell me something about cats in the old days"),
    ("r6", "My kids need something for tonight, they love our cat"),
    ("r5", "cats lol"),
]


class Route(BaseModel):
    step: Literal["poem", "story", "joke"] = Field(description="The next step in the routing process")
    brief: str = Field(description="What the writer should write, for whom, and what to avoid")


ROUTER_PROMPT = (
    "Route the input to story, joke, or poem based on the user's request. Requests can "
    "be vague: look up the reader with get_reader and use their age, likes, things to "
    "avoid and past requests. Then write a brief for the writer: what to write, for whom, "
    "and what to avoid."
)


# ── Mode 1: the Router agent decides, code branches ──────────────────────────

def validate_route(final) -> Route:
    try:
        return Route.model_validate(final)
    except ValidationError as error:
        raise ValueError(str(error)) from None


def llm_call_router(state: dict) -> None:
    route = shared.run_agent(
        "Router", ROUTER_PROMPT + '\nFinal answer: {"step": "poem" | "story" | "joke", "brief": ""}',
        f"Reader id: {state['reader']}\nRequest: {state['input']}",
        {"get_reader": t.get_reader}, validate=validate_route)
    state["decision"], state["brief"] = route.step, route.brief
    shared.step("Router", f"-> {route.step}: {route.brief}")


def route_and_write(state: dict) -> None:
    # The conditional edge, hand-rolled: a plain if/elif.
    if state["decision"] == "story":
        state["output"] = wf_writers.write_story(state["brief"])
    elif state["decision"] == "joke":
        state["output"] = wf_writers.write_joke(state["brief"])
    elif state["decision"] == "poem":
        state["output"] = wf_writers.write_poem(state["brief"])


def run_workflow(reader: str, request: str) -> None:
    state = {"reader": reader, "input": request}
    llm_call_router(state)
    route_and_write(state)
    print(f"\n[{state['decision']}]\n{state['output']['text']}")


# ── Mode 2: the Router agent hands off itself ────────────────────────────────

def run_agentic(reader: str, request: str) -> None:
    handed_off: dict[str, dict] = {}  # code records what the writers really returned

    def recorded(kind: str, writer):
        def call(brief: str) -> dict:
            handed_off[kind] = writer(brief)
            return handed_off[kind]
        call.__doc__ = writer.__doc__
        return call

    def validate(final):
        kind = final.get("routed_to") if isinstance(final, dict) else None
        if kind not in handed_off:
            raise ValueError(f"routed_to {kind!r} was never called; call a writer and return its piece")
        return kind

    tools = {"get_reader": t.get_reader, "write_story": recorded("story", wf_writers.write_story),
             "write_joke": recorded("joke", wf_writers.write_joke),
             "write_poem": recorded("poem", wf_writers.write_poem)}
    kind = shared.run_agent(
        "Router", ROUTER_PROMPT + " Then call the matching writer tool with that brief.\n"
        'Final answer: {"routed_to": "poem" | "story" | "joke"}',
        f"Reader id: {reader}\nRequest: {request}", tools, validate=validate)
    # The piece the user gets comes from the writer, not from the Router's retelling.
    print(f"\n[{kind}]\n{handed_off[kind]['text']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    parser.add_argument("--request", type=int, help=f"run only request 1-{len(REQUESTS)}")
    args = parser.parse_args()
    chosen = [REQUESTS[args.request - 1]] if args.request else REQUESTS
    for reader, request in chosen:
        print(f"\n══ {reader}: {request!r}")
        (run_agentic if args.mode == "agentic" else run_workflow)(reader, request)
    shared.print_usage()


if __name__ == "__main__":
    main()
