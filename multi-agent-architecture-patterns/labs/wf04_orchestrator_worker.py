"""
Workflows & Agents 04 · Orchestrator-Worker, every step an agent

The notes' exercise: plan a report on LLM scaling laws, have one worker
write each section, then join them. Here the report must be grounded in a
small paper library (data/workflows/papers.json): the Orchestrator plans
sections around the papers that exist, and every claim a worker makes is
cited as [paper-id] from a paper it actually read.

--mode workflow (default): code runs the plan, as in the notes.
    topic -> Orchestrator (agent, search_papers) -> Sections
          -> one Worker (agent, read_paper) per section, in parallel
          -> synthesizer (code): join + check every citation

    The notes use Send() to start one worker per section; here that is
    ThreadPoolExecutor.map over the sections.

--mode agentic: the Orchestrator assigns workers itself, reads what comes
    back, can add or redo sections, and writes the intro and conclusion.

Run it:
    uv run labs/wf04_orchestrator_worker.py
    uv run labs/wf04_orchestrator_worker.py --mode agentic
"""

import argparse
import threading
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t

TOPIC = "Create a report on LLM scaling laws"


class Section(BaseModel):
    name: str = Field(description="Name for this section of the report.")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    paper_ids: list[str] = Field(description="Ids of the papers this section should draw on.")


class Sections(BaseModel):
    sections: list[Section] = Field(description="Sections of the report.")


# Every paper any worker read, so citations can be checked in code.
READ: set[str] = set()
_READ_LOCK = threading.Lock()


def check_citations(text: str, read: set[str]) -> list[str]:
    cited = t.cited_papers(text)
    problems = []
    if not cited:
        problems.append("no [paper-id] citations")
    if unknown := cited - t.paper_ids():
        problems.append(f"cites papers that do not exist: {sorted(unknown)}")
    if unread := (cited & t.paper_ids()) - read:
        problems.append(f"cites papers never read with read_paper: {sorted(unread)}")
    return problems


# ── The Orchestrator's plan ──────────────────────────────────────────────────

PLAN_PROMPT = (
    "Generate a plan for the report. Use list_papers and search_papers to see which "
    "papers the library has, and plan 3 to 5 sections that the library can support. "
    "Give each section the ids of the papers it should draw on.\n"
    'Final answer: {"sections": [{"name": "", "description": "", "paper_ids": [""]}]}'
)


def validate_plan(final) -> list[Section]:
    try:
        plan = Sections.model_validate(final)
    except ValidationError as error:
        raise ValueError(str(error)) from None
    if not 3 <= len(plan.sections) <= 5:
        raise ValueError(f"plan has {len(plan.sections)} sections, need 3 to 5")
    unknown = {p for s in plan.sections for p in s.paper_ids} - t.paper_ids()
    if unknown:
        raise ValueError(f"these paper ids do not exist: {sorted(unknown)}")
    return plan.sections


def orchestrator(state: dict) -> None:
    state["sections"] = shared.run_agent(
        "Orchestrator", PLAN_PROMPT, f"Here is the report topic: {state['topic']}",
        {"list_papers": t.list_papers, "search_papers": t.search_papers}, validate=validate_plan)
    shared.step("Orchestrator", f"planned {[s.name for s in state['sections']]}")


# ── A Worker writes one section ──────────────────────────────────────────────

WORKER_PROMPT = (
    "Write a report section in markdown, starting with '## <section name>'. Read the "
    "papers you were given with read_paper (search_papers if you need more). Every "
    "claim must come from a paper you read, cited inline as [paper-id], e.g. "
    "[kaplan2020]. 120 to 250 words.\n"
    'Final answer: {"text": "<the section>"}'
)


def llm_call(section: Section) -> str:
    """Worker writes a section of the report."""
    read: set[str] = set()

    def read_tracked(paper_id: str) -> dict | None:
        """The full summary and key claims of one paper, by id."""
        paper = t.read_paper(paper_id)
        if paper:
            read.add(paper["id"])
            with _READ_LOCK:
                READ.add(paper["id"])
        return paper

    def validate(final) -> str:
        text = final.get("text") if isinstance(final, dict) else None
        if not isinstance(text, str):
            raise ValueError('final must be {"text": "<the section>"}')
        if problems := check_citations(text, read):
            raise ValueError("\n".join(problems))
        return text

    label = f"Worker: {section.name[:9]}"  # short, so the usage table stays aligned
    return shared.run_agent(
        label, WORKER_PROMPT,
        f"Here is the section name: {section.name} and description: {section.description}. "
        f"Papers: {section.paper_ids}",
        {"read_paper": read_tracked, "search_papers": t.search_papers}, validate=validate)


def references(text: str) -> str:
    lines = [f"- [{p['id']}] {p['authors']} ({p['year']}). {p['title']}"
             for p in map(t.read_paper, sorted(t.cited_papers(text)))]
    return "## References\n" + "\n".join(lines)


# ── Mode 1: code runs the plan ───────────────────────────────────────────────

def synthesizer(state: dict) -> None:
    """Synthesize full report from sections (code, as in the notes) and check it."""
    report = "\n\n---\n\n".join(state["completed_sections"])
    if problems := check_citations(report, READ):
        shared.step("Synthesizer", f"citation problems: {problems}")
    state["final_report"] = report + "\n\n---\n\n" + references(report)


def run_workflow() -> str:
    state = {"topic": TOPIC}
    orchestrator(state)
    with ThreadPoolExecutor() as pool:  # Send() by hand: one worker per section
        state["completed_sections"] = list(pool.map(llm_call, state["sections"]))
    synthesizer(state)
    print(f"\n{state['final_report']}")
    return state["final_report"]


# ── Mode 2: the Orchestrator assigns workers itself ──────────────────────────

def assign_workers(sections: list) -> list[dict]:
    """Start one worker agent per section, in parallel. sections is a list of
    {"name", "description", "paper_ids"}. Returns [{"name", "text"}] or
    [{"name", "error"}] per section."""
    def one(raw: dict) -> dict:
        try:
            section = Section.model_validate(raw)
            return {"name": section.name, "text": llm_call(section)}
        except Exception as error:
            return {"name": raw.get("name"), "error": str(error)}
    with ThreadPoolExecutor() as pool:
        return list(pool.map(one, sections))


AGENTIC_PROMPT = (
    "You are writing a report. Use list_papers and search_papers to see what the "
    "library supports, then plan 3 to 5 sections and call assign_workers once with all "
    "of them, so they are written in parallel. Read what comes back: redo a section "
    "that failed or is weak, or add one if there is a gap. Then write the report: a "
    "short intro, the sections exactly as the workers wrote them, and a short "
    "conclusion. Cite only papers that the sections cite, as [paper-id].\n"
    'Final answer: {"report": "<the full report in markdown>"}'
)


def run_agentic() -> str:
    def validate(final) -> str:
        report = final.get("report") if isinstance(final, dict) else None
        if not isinstance(report, str):
            raise ValueError('final must be {"report": "..."}')
        if report.count("## ") < 3:
            raise ValueError("the report needs at least 3 '## ' sections")
        if problems := check_citations(report, READ):
            raise ValueError("\n".join(problems))
        return report

    report = shared.run_agent(
        "Orchestrator", AGENTIC_PROMPT, TOPIC,
        {"list_papers": t.list_papers, "search_papers": t.search_papers,
         "assign_workers": assign_workers}, max_steps=20, validate=validate)
    print(f"\n{report}\n\n---\n\n{references(report)}")
    return report + "\n\n---\n\n" + references(report)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["workflow", "agentic"], default="workflow")
    mode = parser.parse_args().mode
    output = (run_agentic if mode == "agentic" else run_workflow)()
    shared.print_usage()
    shared.save_transcript("wf04", mode, TOPIC, output)


if __name__ == "__main__":
    main()
