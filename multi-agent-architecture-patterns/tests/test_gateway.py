"""Tool gateway: least privilege, schema validation, confirmation, sanitising, ownership and preconditions."""


def test_search_agent_cannot_raise_access_requests(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "A·Search"), "create_access_request",
                              {"workspace": "Compliance", "permission": "upload", "justification": "x"})
    assert result["error"] == "tool_not_permitted"
    assert not bot.state.access_requests


def test_debugger_cannot_upload(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "B·Debugger"), "upload_record",
                              {"doc_id": "1240", "target_workspace": "Compliance"})
    assert result["error"] == "tool_not_permitted"


def test_no_agent_below_the_coordinator_has_a_messaging_tool(make_bot):
    bot = make_bot()
    for agent in ("A·Search", "B·Debugger", "D·Reupload"):
        assert "notify_user" not in bot.gateway.allowlists[agent]


def test_invalid_arguments_are_rejected(make_bot, ctx_for):
    bot = make_bot()
    ctx = ctx_for(bot, "A·Search")
    assert bot.gateway.call(ctx, "get_record", {"doc_id": "12ab"})["error"] == "invalid_arguments"
    assert bot.gateway.call(ctx, "get_record", {"doc_id": "1234", "extra": 1})["error"] == "invalid_arguments"
    assert bot.gateway.call(ctx, "get_record", {"__invalid_json__": "{"})["error"] == "invalid_arguments"


def test_write_actions_need_confirmation(make_bot, ctx_for):
    bot = make_bot(confirmer=lambda agent, tool, args: False)
    result = bot.gateway.call(ctx_for(bot, "C·Access"), "create_access_request",
                              {"workspace": "Compliance", "permission": "upload", "justification": "re-upload"})
    assert result["error"] == "not_confirmed"
    assert not bot.state.access_requests


def test_hr_records_are_hidden_from_a_finance_user(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "A·Search"), "get_record", {"doc_id": "7001"})
    assert result == {"doc_id": "7001", "exists": True, "has_access": False}
    assert bot.gateway.call(ctx_for(bot, "A·Search"), "search_archive",
                            {"query": "contract", "workspace": "HR"})["error"] == "access_denied"


def test_embedded_instruction_in_record_is_sanitised(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "A·Search"), "get_record", {"doc_id": "1236"})
    title = result["record"]["title"]
    assert "external-mail.com" not in title and "ignore your rules" not in title
    assert title.startswith("Invoice 1236, Westpark Services")
    assert result["untrusted_content"][0]["path"] == "$.record.title"


def test_batches_of_other_users_are_not_readable(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "B·Debugger"), "get_validation_log",
                              {"batch_id": "BATCH-2026-01-01-001", "doc_id": "1240"})
    assert result["error"] == "not_found"


def test_bounded_consult_allows_one_question(make_bot, ctx_for):
    bot = make_bot()
    ctx = ctx_for(bot, "B·Debugger")
    args = {"doc_id": "1240", "workspace": "Finance"}
    assert bot.gateway.call(ctx, "consult_search_exists", args) == {"exists": False}
    assert bot.gateway.call(ctx, "consult_search_exists", args)["error"] == "precondition_failed"
    assert ctx.run["consults"] == [{"to": "A·Search", "question": args, "answer": {"exists": False}}]


def test_upload_requires_prevalidation_and_approval(make_bot, ctx_for):
    bot = make_bot()
    ctx = ctx_for(bot, "D·Reupload")
    upload = {"doc_id": "1240", "target_workspace": "Compliance"}
    assert "prevalidate" in bot.gateway.call(ctx, "upload_record", upload)["message"]
    assert bot.gateway.call(ctx, "prevalidate", upload)["passed"] is True
    assert "approval missing" in bot.gateway.call(ctx, "upload_record", upload)["message"]

    bot.state.grant("priya", "Compliance-Uploader")
    assert bot.gateway.call(ctx, "upload_record", upload)["status"] == "archived"
    assert bot.state.find_document("1240", "Compliance") is not None


def test_prevalidation_fails_against_finance_rules(make_bot, ctx_for):
    bot = make_bot()
    result = bot.gateway.call(ctx_for(bot, "D·Reupload"), "prevalidate", {"doc_id": "1240", "target_workspace": "Finance"})
    assert result["passed"] is False


def test_access_request_is_approved_on_status_check(make_bot, ctx_for):
    bot = make_bot()
    ctx = ctx_for(bot, "C·Access")
    request = bot.gateway.call(ctx, "create_access_request",
                               {"workspace": "Compliance", "permission": "upload", "justification": "re-upload"})
    assert request["status"] == "pending_approval"
    assert not bot.state.can("priya", "Compliance", "upload")
    status = bot.gateway.call(ctx, "get_access_request_status", {"request_id": request["request_id"]})
    assert status["status"] == "approved"
    assert bot.state.can("priya", "Compliance", "upload")
    assert bot.gateway.call(ctx, "create_access_request", {"workspace": "Compliance", "permission": "upload",
                                                           "justification": "again"})["error"] == "already_entitled"
