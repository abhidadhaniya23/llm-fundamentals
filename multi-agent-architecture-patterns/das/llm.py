"""
LLM clients.

NexusClient talks to the MB Nexus portal. With LLM_FAST_API_VERSION set, Nexus
speaks the Azure OpenAI format (deployment in the path, api-version in the
query), the same convention as ../ai-application-architecture/llm_client.py.

ScriptedLLM replays fixed replies per agent: used by the tests and --offline.
"""

import json
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, Protocol

import httpx

from das.config import LLMSettings


class LLMError(Exception):
    pass


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict
    raw_arguments: str = ""


@dataclass
class LLMReply:
    content: str | None
    tool_calls: list[ToolCall] = field(default_factory=list)
    prompt_tokens: int = 0
    completion_tokens: int = 0


class LLMClient(Protocol):
    def chat(self, agent: str, messages: list[dict], tools: list[dict] | None = None) -> LLMReply: ...


def parse_tool_calls(raw_calls: list[dict] | None) -> list[ToolCall]:
    calls = []
    for call in raw_calls or []:
        raw = call["function"].get("arguments") or "{}"
        try:
            arguments = json.loads(raw)
        except json.JSONDecodeError:
            arguments = {"__invalid_json__": raw}
        calls.append(ToolCall(call["id"], call["function"]["name"], arguments, raw))
    return calls


class NexusClient:
    def __init__(self, settings: LLMSettings, timeout: float = 120, retries: int = 1):
        self.settings = settings
        self.timeout = timeout
        self.retries = retries

    @property
    def url(self) -> str:
        base = self.settings.api_url.rstrip("/")
        if self.settings.api_version:
            return (f"{base}/openai/deployments/{self.settings.model}/chat/completions"
                    f"?api-version={self.settings.api_version}")
        return base + "/chat/completions"

    def chat(self, agent: str, messages: list[dict], tools: list[dict] | None = None) -> LLMReply:
        request: dict = {"model": self.settings.model, "messages": messages, "temperature": 0}
        if tools:
            request["tools"] = tools
        headers = {"api-key": self.settings.api_key, "Authorization": f"Bearer {self.settings.api_key}"}
        for attempt in range(self.retries + 1):
            try:
                response = httpx.post(self.url, headers=headers, json=request, timeout=self.timeout)
                if response.status_code in (429, 500, 502, 503, 504) and attempt < self.retries:
                    time.sleep(2 * (attempt + 1))
                    continue
                response.raise_for_status()
                break
            except httpx.TransportError as error:
                if attempt >= self.retries:
                    raise LLMError(f"Cannot reach Nexus ({type(error).__name__}). Check LLM_FAST_API_URL / network.")
                time.sleep(2 * (attempt + 1))
            except httpx.HTTPStatusError as error:
                raise LLMError(f"Nexus answered HTTP {error.response.status_code} for {agent}: "
                               f"{error.response.text[:300]}")
        body = response.json()
        message = body["choices"][0]["message"]
        usage = body.get("usage") or {}
        return LLMReply(message.get("content"), parse_tool_calls(message.get("tool_calls")),
                        usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))


Step = LLMReply | Callable[[list[dict]], LLMReply]


def reply(content: str | dict | None = None, *calls: tuple[str, dict]) -> LLMReply:
    """Shorthand for scripts: reply('text') or reply(None, ('tool', {args}), ...)."""
    if isinstance(content, dict):
        content = json.dumps(content)
    return LLMReply(content, [ToolCall(f"call_{name}_{index}", name, args, json.dumps(args))
                              for index, (name, args) in enumerate(calls, start=1)])


class ScriptedLLM:
    """Replays a queue of replies per agent name. Thread-safe (A and B run in parallel)."""

    def __init__(self, script: dict[str, list[Step]]):
        self._queues = defaultdict(list, {agent: list(steps) for agent, steps in script.items()})
        self._lock = threading.Lock()
        self.calls: list[tuple[str, list[dict]]] = []

    def chat(self, agent: str, messages: list[dict], tools: list[dict] | None = None) -> LLMReply:
        with self._lock:
            self.calls.append((agent, [dict(m) for m in messages]))
            if not self._queues[agent]:
                raise LLMError(f"ScriptedLLM: no scripted reply left for {agent}")
            step = self._queues[agent].pop(0)
        result = step(messages) if callable(step) else step
        result.prompt_tokens = result.prompt_tokens or sum(len(str(m.get("content") or "")) for m in messages) // 4
        result.completion_tokens = result.completion_tokens or len(result.content or "") // 4 + 10 * len(result.tool_calls)
        return result

    def remaining(self) -> dict[str, int]:
        return {agent: len(queue) for agent, queue in self._queues.items() if queue}
