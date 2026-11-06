"""
The agent loop every agent in the team uses: an LLM tool-calling loop over the gateway.

Each turn: send the conversation plus this agent's tool specs, run any tool calls
through the gateway (several calls in one turn run in parallel), feed the results
back, repeat until the LLM gives a final answer. A final answer must match the
agent's output schema; one repair attempt is allowed.
"""

import contextvars
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from das import guardrails, schema
from das.gateway import ToolContext
from das.llm import ToolCall
from das.trace import tracer

if TYPE_CHECKING:
    from das.runtime import DASChatbot


class AgentError(Exception):
    pass


def _short(text: str | None, limit: int = 400) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …"


@dataclass
class Agent:
    name: str
    title: str
    step: int | None
    system_prompt: Callable[["DASChatbot"], str]
    output_schema: dict | None = None
    max_steps: int = 8

    def run(self, bot: "DASChatbot", brief, ctx: ToolContext | None = None,
            history: list[dict] | None = None) -> tuple[object, list[dict], ToolContext]:
        ctx = ctx or ToolContext(bot, self.name)
        tools = sorted(bot.gateway.allowlists.get(self.name, set()))
        tracer().section(self.step, self.title, f"tools: {', '.join(tools) or '(none)'}")
        with tracer().nested():
            system = self.system_prompt(bot)
            if tracer().show_prompts:
                tracer().event("INFO", self.name, "system prompt", system)
            content = brief if isinstance(brief, str) else json.dumps(brief, ensure_ascii=False)
            tracer().event("INFO", self.name, "brief received", brief)
            messages = [{"role": "system", "content": system}, *(history or []), {"role": "user", "content": content}]
            return self._loop(bot, messages, ctx), messages, ctx

    def resume(self, bot: "DASChatbot", messages: list[dict], ctx: ToolContext, note: str):
        with tracer().nested():
            tracer().event("WARN", self.name, "resumed with feedback", note)
            messages.append({"role": "user", "content": note})
            return self._loop(bot, messages, ctx)

    def _loop(self, bot: "DASChatbot", messages: list[dict], ctx: ToolContext):
        tool_specs = bot.gateway.specs_for(self.name)
        repaired = False
        for turn in range(1, self.max_steps + 1):
            last = messages[-1]
            tracer().event("LLM>", self.name, f"turn {turn}: {len(messages)} messages, {len(tool_specs)} tools offered",
                           messages if tracer().show_prompts else f"last {last['role']} message: {_short(last.get('content'))}")
            reply = bot.llm.chat(self.name, messages, tool_specs or None)
            tracer().count(self.name, "llm_calls")
            tracer().count(self.name, "prompt_tokens", reply.prompt_tokens)
            tracer().count(self.name, "completion_tokens", reply.completion_tokens)

            if reply.tool_calls:
                tracer().event("LLM<", self.name, f"turn {turn}: wants {len(reply.tool_calls)} tool call(s): "
                               + ", ".join(call.name for call in reply.tool_calls),
                               _short(reply.content) if reply.content else None)
                messages.append({"role": "assistant", "content": reply.content, "tool_calls": [
                    {"id": call.id, "type": "function",
                     "function": {"name": call.name, "arguments": call.raw_arguments or json.dumps(call.arguments)}}
                    for call in reply.tool_calls]})
                for call, result in zip(reply.tool_calls, self._execute(bot, ctx, reply.tool_calls)):
                    messages.append({"role": "tool", "tool_call_id": call.id,
                                     "content": json.dumps(result, ensure_ascii=False, default=str)})
                continue

            tracer().event("LLM<", self.name, f"turn {turn}: final answer", reply.content)
            messages.append({"role": "assistant", "content": reply.content or ""})
            if self.output_schema is None:
                return reply.content or ""
            try:
                output = guardrails.extract_json(reply.content)
                errors = schema.validate(output, self.output_schema)
            except ValueError as error:
                output, errors = None, [str(error)]
            if not errors:
                return output
            if repaired:
                raise AgentError(f"{self.name} returned invalid output twice: {errors}")
            repaired = True
            tracer().event("WARN", self.name, "final answer rejected by output schema, asking for a repair", errors)
            messages.append({"role": "user", "content": "Your final answer was rejected: " + "; ".join(errors)
                             + ". Reply again with ONLY a JSON object matching this schema: "
                             + json.dumps(self.output_schema)})
        raise AgentError(f"{self.name} did not finish within {self.max_steps} turns")

    def _execute(self, bot: "DASChatbot", ctx: ToolContext, calls: list[ToolCall]) -> list[dict]:
        writes = [call.name for call in calls if getattr(bot.gateway.tools.get(call.name), "write", False)]
        if len(calls) == 1 or writes:
            if len(calls) > 1:
                tracer().event("INFO", self.name, f"{len(calls)} tool calls include write action(s) {writes}: "
                                                  "running them one after another, in the order given")
            return [bot.gateway.call(ctx, call.name, call.arguments) for call in calls]

        def branch(call: ToolCall):
            with tracer().capture() as lines:
                result = bot.gateway.call(ctx, call.name, call.arguments)
            return result, lines

        tracer().event("PAR", self.name, f"running {len(calls)} tool calls in parallel: "
                       + " ‖ ".join(call.name for call in calls))
        with ThreadPoolExecutor(max_workers=len(calls)) as pool:
            futures = [pool.submit(contextvars.copy_context().run, branch, call) for call in calls]
            outcomes = [future.result() for future in futures]
        for index, (call, (_, lines)) in enumerate(zip(calls, outcomes), start=1):
            tracer().event("PAR", self.name, f"── parallel branch {index}/{len(calls)}: {call.name} "
                                             "(lines below ran concurrently; see timestamps)")
            tracer().flush(lines)
        tracer().event("PAR", self.name, f"all {len(calls)} parallel branches returned")
        return [result for result, _ in outcomes]
