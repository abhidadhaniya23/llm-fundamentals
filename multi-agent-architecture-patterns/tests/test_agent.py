"""The agent loop: schema repair, step limit, parallel tool calls."""

import threading
import time

import pytest

from das.agent import Agent, AgentError
from das.gateway import Tool
from das.llm import reply
from das.schema import BOOL, STR, obj

OUT = obj(["ok"], ok=BOOL)


def _agent(**kwargs) -> Agent:
    return Agent("T", "test agent", None, lambda bot: "test", OUT, **kwargs)


def test_invalid_final_answer_gets_one_repair(make_bot):
    bot = make_bot({"T": [reply("not json"), reply({"ok": True})]})
    output, messages, _ = _agent().run(bot, "go")
    assert output == {"ok": True}
    assert "rejected" in messages[-2]["content"]


def test_invalid_final_answer_twice_raises(make_bot):
    bot = make_bot({"T": [reply({"ok": "yes"}), reply("```json\n{\"wrong\": 1}\n```")]})
    with pytest.raises(AgentError):
        _agent().run(bot, "go")


def test_step_limit(make_bot):
    bot = make_bot({"T": [reply(None, ("get_record", {"doc_id": "1234"}))] * 3})
    bot.gateway.allow("T", ["get_record"])
    with pytest.raises(AgentError, match="within 2 turns"):
        _agent(max_steps=2).run(bot, "go")


def test_turn_with_a_write_runs_sequentially_in_order(make_bot):
    bot = make_bot({"D·Reupload": [
        reply(None, ("prevalidate", {"doc_id": "1240", "target_workspace": "Compliance"}),
              ("upload_record", {"doc_id": "1240", "target_workspace": "Compliance"})),
        reply({"doc_id": "1240", "workspace": "Compliance", "prevalidation": "passed", "status": "archived"})]})
    bot.state.grant("priya", "Compliance-Uploader")
    from das.team import REUPLOAD
    REUPLOAD.run(bot, {"doc_id": "1240"})
    assert bot.state.find_document("1240", "Compliance") is not None


def test_tool_calls_in_one_turn_run_concurrently(make_bot):
    threads = set()

    def slow(ctx, args):
        threads.add(threading.get_ident())
        time.sleep(0.3)
        return {"done": args["name"]}

    bot = make_bot({"T": [reply(None, ("slow", {"name": "a"}), ("slow", {"name": "b"})), reply({"ok": True})]})
    bot.gateway.register(Tool("slow", "sleeps", obj(name=STR), slow))
    bot.gateway.allow("T", ["slow"])
    started = time.perf_counter()
    _, messages, _ = _agent().run(bot, "go")
    assert time.perf_counter() - started < 0.55
    assert len(threads) == 2
    assert [m["content"] for m in messages if m["role"] == "tool"] == ['{"done": "a"}', '{"done": "b"}']
