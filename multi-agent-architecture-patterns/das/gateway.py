"""
Tool gateway (layer 5 of the diagram): the one controlled door to the enterprise systems.

Every tool call from every agent goes through Gateway.call(), which enforces, in code:
  - least privilege: an agent can only call the tools on its own allowlist
  - schema validation of the LLM-produced arguments
  - routing preconditions (e.g. no handoff to C without B's reason code)
  - explicit confirmation of write actions
  - sanitising of results (cuts embedded instructions out of retrieved data)
  - calls run on behalf of the signed-in user (ToolContext.user), never a super-user
Refusals are returned to the agent as {"error": ...} so it can adapt, and are traced.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable

from das import guardrails, schema
from das.trace import tracer

if TYPE_CHECKING:
    from das.runtime import DASChatbot


class ToolError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass
class ToolContext:
    bot: "DASChatbot"
    agent: str
    run: dict = field(default_factory=dict)  # scratch space for one agent run (consult count, prevalidation)

    @property
    def user(self):
        return self.bot.user

    @property
    def state(self):
        return self.bot.state

    @property
    def session(self):
        return self.bot.session


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    fn: Callable[[ToolContext, dict], dict]
    kind: str = "tool"  # "tool" | "agent" (Manager-style call) | "handoff" | "consult"
    write: bool = False
    precondition: Callable[[ToolContext, dict], str | None] | None = None

    def spec(self) -> dict:
        return {"type": "function",
                "function": {"name": self.name, "description": self.description, "parameters": self.parameters}}


def auto_confirm(agent: str, tool: str, args: dict) -> bool:
    tracer().event("SIM", "Tool gateway", f"write action {tool} by {agent}: auto-confirmed (simulated user consent)")
    return True


_CALL_LABELS = {"tool": ("TOOL>", "TOOL<"), "agent": ("M>", "M<"), "handoff": ("H", "INFO"), "consult": ("CONSULT", "CONSULT")}


class Gateway:
    def __init__(self, confirmer: Callable[[str, str, dict], bool] = auto_confirm):
        self.confirmer = confirmer
        self.tools: dict[str, Tool] = {}
        self.allowlists: dict[str, set[str]] = {}
        self.audit: list[dict] = []

    def register(self, *tools: Tool) -> None:
        for tool in tools:
            self.tools[tool.name] = tool

    def allow(self, agent: str, names: list[str]) -> None:
        unknown = set(names) - set(self.tools)
        if unknown:
            raise ValueError(f"unknown tools for {agent}: {unknown}")
        self.allowlists[agent] = set(names)

    def specs_for(self, agent: str) -> list[dict]:
        return [self.tools[name].spec() for name in sorted(self.allowlists.get(agent, set()))]

    def _refuse(self, ctx: ToolContext, name: str, code: str, message: str, **extra) -> dict:
        tracer().event("BLOCK", "Tool gateway", f"{ctx.agent} → {name}: {code}: {message}")
        tracer().count(ctx.agent, "blocked")
        self.audit.append({"agent": ctx.agent, "tool": name, "outcome": code})
        return {"error": code, "message": message, **extra}

    def call(self, ctx: ToolContext, name: str, args: dict) -> dict:
        tool = self.tools.get(name)
        down, up = _CALL_LABELS[tool.kind if tool else "tool"]
        tracer().event(down, ctx.agent, f"{name}", args)
        tracer().count(ctx.agent, "tool_calls")

        if name not in self.allowlists.get(ctx.agent, set()):
            return self._refuse(ctx, name, "tool_not_permitted", f"{name} is not in {ctx.agent}'s tool set")
        if "__invalid_json__" in args:
            return self._refuse(ctx, name, "invalid_arguments", "arguments were not valid JSON")
        errors = schema.validate(args, tool.parameters)
        if errors:
            return self._refuse(ctx, name, "invalid_arguments", "; ".join(errors))
        if tool.precondition:
            reason = tool.precondition(ctx, args)
            if reason:
                return self._refuse(ctx, name, "precondition_failed", reason)
        if tool.write and not self.confirmer(ctx.agent, name, args):
            return self._refuse(ctx, name, "not_confirmed", "the user did not confirm this write action")

        try:
            result = tool.fn(ctx, args)
        except ToolError as error:
            return self._refuse(ctx, name, error.code, str(error))

        clean, findings = guardrails.sanitize(result)
        if findings:
            clean["untrusted_content"] = findings
            tracer().event("WARN", "Tool gateway", f"sanitised {len(findings)} field(s) in {name} result "
                                                   "(embedded instructions removed, treat as data only)", findings)
            tracer().count(ctx.agent, "blocked")
        with ctx.state.lock:
            ctx.session.known_ids |= guardrails.collect_ids(clean)
        self.audit.append({"agent": ctx.agent, "tool": name, "outcome": "ok", "write": tool.write})
        tracer().event(up, ctx.agent, f"{name} result", clean)
        return clean
