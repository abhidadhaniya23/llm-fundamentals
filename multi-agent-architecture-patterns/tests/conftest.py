import io
import json
import shutil
from datetime import date

import pytest

from das.gateway import ToolContext
from das.llm import ScriptedLLM
from das.runtime import DASChatbot
from das.store import DATA_DIR, DataStore
from das.trace import Tracer, install


@pytest.fixture(autouse=True)
def quiet_trace():
    stream = io.StringIO()
    install(Tracer(color=False, stream=stream))
    yield stream


@pytest.fixture
def make_bot():
    def build(script: dict | None = None, store: DataStore | None = None, **kwargs) -> DASChatbot:
        return DASChatbot(ScriptedLLM(script or {}), store=store, today=date(2026, 10, 30), **kwargs)
    return build


@pytest.fixture
def ctx_for():
    def build(bot: DASChatbot, agent: str) -> ToolContext:
        return ToolContext(bot, agent)
    return build


@pytest.fixture
def fault_store(tmp_path) -> DataStore:
    """Same data, but invoice 1240 failed with a system fault instead of a user-fixable reason."""
    for file in DATA_DIR.glob("*.json"):
        shutil.copy(file, tmp_path / file.name)
    log = json.loads((tmp_path / "validation_log.json").read_text(encoding="utf-8"))
    for entry in log:
        if entry["doc_id"] == "1240":
            entry.update(stage="archive_write", reason_code="SYS-ARCHIVE-UNAVAILABLE",
                         detail="Archive storage returned 503 during write.")
    (tmp_path / "validation_log.json").write_text(json.dumps(log), encoding="utf-8")
    return DataStore(tmp_path)
