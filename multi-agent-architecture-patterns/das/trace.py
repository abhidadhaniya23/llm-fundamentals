"""
Detailed flow trace: every hop of a request is printed while it runs.

Numbered sections match the badges in docs/agent-flow-architecture.html
(1 user, 2 gateway + SSO, 3 Coordinator, 4 A, 5 B, 6 C, 7 D, 8 output guardrails).
Indentation shows who called whom. Tool calls made in parallel are buffered
per branch and printed branch by branch, with their real timestamps, so
concurrent agents stay readable.
"""

import contextvars
import json
import os
import sys
import threading
import time
from collections import defaultdict
from contextlib import contextmanager

BADGES = {1: "①", 2: "②", 3: "③", 4: "④", 5: "⑤", 6: "⑥", 7: "⑦", 8: "⑧"}

KINDS = {
    "LLM>": ("LLM →", "blue"),
    "LLM<": ("LLM ←", "blue"),
    "TOOL>": ("TOOL→", "yellow"),
    "TOOL<": ("TOOL←", "yellow"),
    "M>": ("M ↓  ", "teal"),
    "M<": ("M ↑  ", "teal"),
    "H": ("H ⇒  ", "violet"),
    "CONSULT": ("⇄ ASK", "teal"),
    "GUARD": ("GUARD", "green"),
    "BLOCK": ("BLOCK", "red"),
    "STATE": ("STATE", "grey"),
    "SIM": ("SIM  ", "grey"),
    "PAR": ("PAR ⇉", "grey"),
    "SAY": ("SAY  ", "green"),
    "INFO": ("INFO ", "grey"),
    "WARN": ("WARN ", "red"),
}

ANSI = {"blue": "34", "yellow": "33", "teal": "36", "violet": "35", "green": "32",
        "red": "31", "grey": "90", "bold": "1"}

_depth: contextvars.ContextVar[int] = contextvars.ContextVar("trace_depth", default=0)
_buffer: contextvars.ContextVar[list | None] = contextvars.ContextVar("trace_buffer", default=None)


class Tracer:
    def __init__(self, color: bool | None = None, max_chars: int = 700, show_prompts: bool = False,
                 stream=None, jsonl_path: str | None = None):
        self.stream = stream or sys.stdout
        if color is None:
            color = hasattr(self.stream, "isatty") and self.stream.isatty() and not os.environ.get("NO_COLOR")
        self.color = color
        self.max_chars = max_chars
        self.show_prompts = show_prompts
        self._lock = threading.Lock()
        self._t0 = time.perf_counter()
        self._jsonl = open(jsonl_path, "a", encoding="utf-8") if jsonl_path else None
        self.stats = defaultdict(int)
        self.per_agent: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.milestones: list[str] = []

    def _paint(self, text: str, color: str | None) -> str:
        return f"\033[{ANSI[color]}m{text}\033[0m" if self.color and color else text

    def _emit(self, lines: list[str]) -> None:
        buffer = _buffer.get()
        if buffer is not None:
            buffer.extend(lines)
            return
        with self._lock:
            for line in lines:
                print(line, file=self.stream)
            self.stream.flush()

    def _format_data(self, data) -> list[str]:
        text = data if isinstance(data, str) else json.dumps(data, indent=2, ensure_ascii=False, default=str)
        if self.max_chars and len(text) > self.max_chars:
            text = text[: self.max_chars] + f" … (+{len(text) - self.max_chars} chars, use --full)"
        return text.splitlines() or [""]

    def event(self, kind: str, actor: str, text: str, data=None) -> None:
        label, color = KINDS[kind]
        elapsed = time.perf_counter() - self._t0
        indent = "│  " * _depth.get()
        head = f"{self._paint(f'{elapsed:7.2f}s', 'grey')} {indent}{self._paint(label, color)} [{actor}] {text}"
        lines = [head]
        if data is not None:
            pad = " " * 9 + indent + "      "
            lines += [self._paint(pad + "│ ", "grey") + line for line in self._format_data(data)]
        self._emit(lines)
        if self._jsonl:
            with self._lock:
                self._jsonl.write(json.dumps({"t": round(elapsed, 3), "kind": kind, "actor": actor,
                                              "text": text, "data": data}, default=str) + "\n")

    def section(self, step: int | None, title: str, subtitle: str = "") -> None:
        badge = BADGES.get(step, "•") if step else "•"
        indent = "│  " * _depth.get()
        rule = "═" * max(10, 60 - len(title))
        line = f"{' ' * 9}{indent}{self._paint(f'{badge} {title} {rule}', 'bold')}"
        lines = ([""] if _depth.get() == 0 else []) + [line]
        if subtitle:
            lines.append(f"{' ' * 9}{indent}  {self._paint(subtitle, 'grey')}")
        self._emit(lines)

    def milestone(self, text: str) -> None:
        with self._lock:
            self.milestones.append(text)

    def count(self, agent: str, key: str, amount: int = 1) -> None:
        with self._lock:
            self.stats[key] += amount
            self.per_agent[agent][key] += amount

    @contextmanager
    def nested(self):
        token = _depth.set(_depth.get() + 1)
        try:
            yield
        finally:
            _depth.reset(token)

    @contextmanager
    def capture(self):
        """Buffer this branch's lines (used for parallel tool calls); flush with flush()."""
        lines: list[str] = []
        token = _buffer.set(lines)
        try:
            yield lines
        finally:
            _buffer.reset(token)

    def flush(self, lines: list[str]) -> None:
        self._emit(lines)

    def summary(self) -> None:
        elapsed = time.perf_counter() - self._t0
        out = ["", self._paint("FLOW SUMMARY " + "═" * 50, "bold")]
        out += [f"  {number:>2}. {text}" for number, text in enumerate(self.milestones, start=1)]
        out.append("")
        out.append(f"  {'agent (session totals)':<22}{'LLM calls':>10}{'tool calls':>12}{'tokens in':>11}{'tokens out':>12}")
        for agent, numbers in self.per_agent.items():
            out.append(f"  {agent:<22}{numbers['llm_calls']:>10}{numbers['tool_calls']:>12}"
                       f"{numbers['prompt_tokens']:>11}{numbers['completion_tokens']:>12}")
        out.append(f"  {'TOTAL':<22}{self.stats['llm_calls']:>10}{self.stats['tool_calls']:>12}"
                   f"{self.stats['prompt_tokens']:>11}{self.stats['completion_tokens']:>12}")
        out.append(f"  blocked by guardrails/gateway: {self.stats['blocked']}   elapsed: {elapsed:.2f}s")
        self._emit(out)


_current = Tracer(stream=open(os.devnull, "w", encoding="utf-8"))  # silent until main() installs one


def tracer() -> Tracer:
    return _current


def install(new: Tracer) -> Tracer:
    global _current
    _current = new
    return new
