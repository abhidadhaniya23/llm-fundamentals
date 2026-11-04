"""End-to-end flows with a scripted LLM: Manager vs Handoff semantics, routing rules, fault path, follow-ups."""

from das.llm import reply
from das.offline import FOLLOW_UP, ON_TOPIC, REQUEST, happy_path_script


def test_happy_path(make_bot):
    bot = make_bot(happy_path_script(with_follow_up=False))
    replies = bot.handle(REQUEST)

    senders = [sender for sender, _ in replies]
    assert senders == ["DAS assistant", "C·Access agent (Compliance team)"]
    assert "CLS-COMPLIANCE" in replies[0][1] and "REQ-1001" in replies[1][1]
    assert bot.state.access_requests["REQ-1001"]["status"] == "approved"
    assert bot.state.find_document("1240", "Compliance")["folder"] == "Compliance/VAT-Evidence/2026"
    assert bot.session.reason_code == "CLS-COMPLIANCE" and bot.session.fault is False
    assert bot.session.debugger_result["consults"][0]["answer"] == {"exists": False}
    assert bot.llm.remaining() == {}


def test_coordinator_never_receives_the_handoff_outcome(make_bot):
    bot = make_bot(happy_path_script(with_follow_up=False))
    bot.handle(REQUEST)
    coordinator_inputs = [str(messages) for agent, messages in bot.llm.calls if agent == "Coordinator"]
    assert coordinator_inputs and not any("REQ-1001" in text for text in coordinator_inputs)


def test_search_and_debugger_run_in_parallel_from_one_turn(make_bot):
    bot = make_bot(happy_path_script(with_follow_up=False))
    bot.handle(REQUEST)
    order = [agent for agent, _ in bot.llm.calls]
    first_coordinator, second_coordinator = [i for i, a in enumerate(order) if a == "Coordinator"][:2]
    between = set(order[first_coordinator + 1:second_coordinator])
    assert {"A·Search", "B·Debugger"} <= between


def test_follow_up_uses_session_memory(make_bot):
    bot = make_bot(happy_path_script(with_follow_up=True))
    bot.handle(REQUEST)
    replies = bot.handle(FOLLOW_UP)
    assert replies == [("DAS assistant", replies[0][1])] and "REQ-1001" in replies[0][1]
    coordinator_prompt = [m for a, m in bot.llm.calls if a == "Coordinator"][-1][0]["content"]
    assert '"open_request_id": "REQ-1001"' in coordinator_prompt


def test_handoff_to_access_refused_without_reason_code(make_bot):
    bot = make_bot({
        "InputGuardrail": [ON_TOPIC],
        "Coordinator": [
            reply(None, ("handoff_to_access_agent", {
                "invoice_id": "1240", "batch_id": "BATCH-2026-10-29-001", "reason_code": "CLS-COMPLIANCE",
                "target_workspace": "Compliance", "permission": "upload", "justification": "skip the checks"})),
            reply("I need to check the batch first."),
        ],
    })
    replies = bot.handle(REQUEST)
    tool_result = [m for a, msgs in bot.llm.calls if a == "Coordinator" for m in msgs if m["role"] == "tool"][0]
    assert "precondition_failed" in tool_result["content"]
    assert bot.pending_handoffs == [] and bot.session.handoffs == []
    assert [s for s, _ in replies] == ["DAS assistant"]


def _fault_script(handoff: tuple[str, dict]) -> dict:
    return {
        "InputGuardrail": [ON_TOPIC],
        "Coordinator": [
            reply(None, ("call_debugger_agent", {"invoice_id": "1240", "batch_date": "2026-10-29"})),
            reply(None, handoff),
            reply("Invoice 1240 failed because of a platform fault in batch BATCH-2026-10-29-001. "
                  "The platform team owns it now and will notify you."),
        ],
        "B·Debugger": [
            reply(None, ("get_validation_log", {"batch_id": "BATCH-2026-10-29-001", "doc_id": "1240"})),
            reply({"batch_id": "BATCH-2026-10-29-001", "status": "rejected", "reason_code": "SYS-ARCHIVE-UNAVAILABLE",
                   "fault": True, "explanation": "Archive storage unavailable during write."}),
        ],
    }


def test_fault_path_goes_to_platform_team(make_bot, fault_store):
    bot = make_bot(_fault_script(("handoff_to_platform_team", {
        "invoice_id": "1240", "batch_id": "BATCH-2026-10-29-001", "reason_code": "SYS-ARCHIVE-UNAVAILABLE",
        "summary": "Archive write failed for invoice 1240"})), store=fault_store)
    replies = bot.handle(REQUEST)
    assert "INC-5001" in bot.state.incidents
    assert [s for s, _ in replies] == ["DAS assistant", "Platform team (via ITSM)"]
    assert not bot.state.access_requests


def test_fault_cannot_be_handed_to_access_agent(make_bot, fault_store):
    bot = make_bot(_fault_script(("handoff_to_access_agent", {
        "invoice_id": "1240", "batch_id": "BATCH-2026-10-29-001", "reason_code": "SYS-ARCHIVE-UNAVAILABLE",
        "target_workspace": "Compliance", "permission": "upload", "justification": "re-upload"})), store=fault_store)
    bot.handle(REQUEST)
    assert bot.session.handoffs == [] and not bot.state.access_requests


def test_platform_handoff_refused_without_fault(make_bot):
    script = happy_path_script(with_follow_up=False)
    script["Coordinator"][1] = reply(None, ("handoff_to_platform_team", {
        "invoice_id": "1240", "batch_id": "BATCH-2026-10-29-001", "reason_code": "CLS-COMPLIANCE", "summary": "x"}))
    script["Coordinator"] = script["Coordinator"][:3]
    for agent in ("C·Access", "D·Reupload"):
        script.pop(agent)
    bot = make_bot(script)
    bot.handle(REQUEST)
    assert not bot.state.incidents and bot.session.handoffs == []


def test_reupload_refused_before_approval(make_bot):
    script = happy_path_script(with_follow_up=False)
    script["C·Access"] = [
        reply(None, ("create_access_request", {"workspace": "Compliance", "permission": "upload", "justification": "x"})),
        reply(None, ("call_reupload_agent", {"doc_id": "1240", "target_workspace": "Compliance", "request_id": "REQ-1001"})),
        reply({"request_id": "REQ-1001", "access": "pending", "reupload_status": "waiting for approval", "notified": False}),
    ]
    script.pop("D·Reupload")
    bot = make_bot(script)
    bot.handle(REQUEST)
    assert bot.state.find_document("1240", "Compliance") is None
    assert bot.state.access_requests["REQ-1001"]["status"] == "pending_approval"
