"""
Build the worked-example slides of the Workflows & Agents page from run transcripts.

Every wf lab writes runs/wf/<lab>_<mode>.json when it finishes (shared.save_transcript):
the input, each agent's task, tool calls, rejections and answer, and the output. This
script turns them into slides and writes them into index.html between the markers
<!-- examples:wfNN --> and <!-- /examples:wfNN -->. No LLM is called.

    python docs/workflows-and-agents/build_examples.py              # from examples/
    python docs/workflows-and-agents/build_examples.py --from-runs  # copy runs/wf/ first

The copies in examples/ are the runs shown on the page; runs/ itself is gitignored.
"""

import argparse
import html
import json
import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
PAGE = HERE / "index.html"
EXAMPLES = HERE / "examples"
RUNS = HERE.parent.parent / "runs" / "wf"

TITLES = {
    "wf00": "Augmented LLM: one question, a research agent",
    "wf01": "Prompt chaining: memo to staff notice",
    "wf02": "Parallelization: email, chat post and FAQ",
    "wf03": "Routing: an employee's question to the right desk",
    "wf04": "Orchestrator-worker: report on LLM scaling laws",
    "wf05": "Evaluator-optimizer: the fire-drill notice",
    "wf06": "Agent: the café order",
}
MODE_NOTE = {
    "workflow": "Your code calls each agent in the order the pattern sets.",
    "agentic": "Agent 1 is the lead. Every other agent below was started by one of its tool calls.",
    "agent": "",
}
WF03_REQUEST = 2  # which request the page shows in full (1-based; Chloe asks two desks a question)


def esc(value) -> str:
    return html.escape(str(value), quote=False)


def as_text(value) -> str:
    """An agent's answer as readable text: the text field if it has one, else JSON."""
    if isinstance(value, dict):
        for key in ("notice", "text", "reply", "combined_output", "report", "joke"):
            if isinstance(value.get(key), str) and len(value) <= 2:
                rest = {k: v for k, v in value.items() if k != key}
                return value[key] + (f"\n\n{json.dumps(rest, ensure_ascii=False)}" if rest else "")
        return json.dumps(value, indent=1, ensure_ascii=False)
    if isinstance(value, list):
        return json.dumps(value, indent=1, ensure_ascii=False)
    return str(value)


def args_text(args: dict) -> str:
    text = ", ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in args.items())
    return text if len(text) <= 140 else text[:140] + "…"


def agent_card(n: int, agent: dict) -> str:
    parallel = agent.get("thread", "").startswith("ThreadPool")
    badge = ' <span class="tag y">ran in parallel</span>' if parallel else ""
    steps = []
    for s in agent["steps"]:
        if "tool" in s:
            steps.append(f'<li><code>{esc(s["tool"])}({esc(args_text(s["args"]))})</code>'
                         f'<details><summary>result</summary><pre>{esc(s["result"])}</pre></details></li>')
        elif "rejected" in s:
            steps.append(f'<li class="rej"><strong>Rejected by code:</strong> {esc(s["rejected"])}'
                         f'<details><summary>the answer it had sent</summary>'
                         f'<pre>{esc(as_text(s["answer"]))}</pre></details></li>')
        else:
            steps.append(f'<li class="c">{esc(s["note"])}</li>')
    tools = (f'<div class="lbl">Tool calls and checks ({len(agent["steps"])})</div><ol class="calls">{"".join(steps)}</ol>'
             if steps else '<div class="lbl">No tool calls</div>')
    final = agent.get("final")
    answer = (f'<div class="lbl">Response</div><pre class="resp">{esc(as_text(final))}</pre>' if final is not None
              else f'<div class="lbl rej">No answer: {esc(agent.get("error", "failed"))}</div>')
    return (f'<div class="agent"><div class="who"><span class="n">{n}</span> '
            f'<span class="tag m">{esc(agent["agent"])}</span>{badge}</div>'
            f'<div class="lbl">Received</div><pre class="recv">{esc(agent["task"])}</pre>'
            f'{tools}{answer}</div>')


def pick(run: dict) -> tuple[object, list[dict], object]:
    """The input, agents and output to show. For wf03 workflow: one request only."""
    given, agents, output = run["input"], run["agents"], run["output"]
    if run["lab"] == "wf03":
        if run["mode"] == "workflow":
            starts = [i for i, a in enumerate(agents) if a["agent"] == "Router"] + [len(agents)]
            i = WF03_REQUEST - 1
            agents = agents[starts[i]:starts[i + 1]]
            given, output = given[i], output[i]
        else:
            given, output = given[0], output[0]
        given = f"Employee {given[0]} asks: {given[1]}"
    if isinstance(given, list):
        given = "\n".join(map(str, given))
    return given, agents, output


def slide(run: dict) -> str:
    lab, mode = run["lab"], run["mode"]
    given, agents, output = pick(run)
    calls = sum(u["calls"] for u in run["usage"].values())
    tokens = sum(u["in"] for u in run["usage"].values())
    cards = "".join(agent_card(n, a) for n, a in enumerate(agents, 1))
    mode_label = f"--mode {mode}" if mode in ("workflow", "agentic") else "single agent"
    note = MODE_NOTE.get(mode, "")
    scope = " (this whole run, all 5 requests)" if lab == "wf03" and mode == "workflow" else ""
    return f"""
<section class="slide example" id="ex-{lab}-{mode}" data-short="{lab[2:]} {'ex' if mode == 'agent' else mode[:4] + '.'}">
  <div class="eyebrow">{lab} · full example · {mode_label}</div>
  <h2>{esc(TITLES[lab])}</h2>
  <p class="lede">A real run, as recorded ({esc(run['provider'])}). {len(agents)} agent run(s) shown{', ' if note else ''}{esc(note[0].lower() + note[1:]) if note else ''}</p>
  <figure><figcaption>Input</figcaption><pre class="cmd">{esc(given)}</pre></figure>
  <div class="agents">{cards}</div>
  <figure><figcaption class="m">Final output</figcaption><pre class="m resp">{esc(as_text(output))}</pre></figure>
  <p class="c">Cost{scope}: {calls} model calls, {tokens:,} input tokens. Transcript: <code>docs/workflows-and-agents/examples/{lab}_{mode}.json</code></p>
</section>"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--from-runs", action="store_true", help="copy runs/wf/*.json into examples/ first")
    if parser.parse_args().from_runs:
        EXAMPLES.mkdir(exist_ok=True)
        for path in RUNS.glob("*.json"):
            shutil.copy(path, EXAMPLES / path.name)
    runs: dict[str, list[dict]] = {}
    for path in sorted(EXAMPLES.glob("*.json")):
        run = json.loads(path.read_text(encoding="utf-8"))
        runs.setdefault(run["lab"], []).append(run)

    page = PAGE.read_text(encoding="utf-8")
    for lab, lab_runs in runs.items():
        lab_runs.sort(key=lambda r: ["workflow", "agentic", "agent"].index(r["mode"]))
        block = "".join(slide(r) for r in lab_runs)
        pattern = re.compile(rf"(<!-- examples:{lab} -->).*?(<!-- /examples:{lab} -->)", re.S)
        if not pattern.search(page):
            print(f"no markers for {lab} in index.html, skipped")
            continue
        page = pattern.sub(lambda m: m.group(1) + block + "\n" + m.group(2), page)
        print(f"{lab}: {len(lab_runs)} example slide(s)")
    PAGE.write_text(page, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
