"""
Enterprise systems (layer 6 of the diagram), mocked.

DataStore    read-only JSON from data/ (archive, ingestion batches, validation log,
             reason-code catalogue, IAM, archive rules, staged files).
RuntimeState what changes during a run: IAM grants, ITSM access requests,
             uploads into the Compliance archive, incidents. In memory only,
             so the files in data/ are never modified.
"""

import json
import threading
from dataclasses import asdict, dataclass, field
from functools import cached_property
from pathlib import Path

from das.config import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"


class DataStore:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)

    def _load(self, name: str):
        return json.loads((self.data_dir / name).read_text(encoding="utf-8"))

    @cached_property
    def documents(self) -> list[dict]:
        return self._load("documents.json")

    @cached_property
    def batches(self) -> list[dict]:
        return self._load("ingestion_batches.json")

    @cached_property
    def validation_log(self) -> list[dict]:
        return self._load("validation_log.json")

    @cached_property
    def reason_codes(self) -> dict:
        return self._load("reason_codes.json")

    @cached_property
    def entitlements(self) -> dict:
        return self._load("entitlements.json")

    @cached_property
    def archive_rules(self) -> dict:
        return self._load("archive_rules.json")

    @cached_property
    def staging(self) -> list[dict]:
        return self._load("staging.json")


@dataclass(frozen=True)
class UserContext:
    """What the API gateway + SSO attaches to every call (simulated: the token is a fake placeholder)."""
    user_id: str
    display_name: str
    job: str
    login_roles: tuple[str, ...]
    token: str

    def scope(self) -> dict:
        return {"user_id": self.user_id, "roles": list(self.login_roles), "token": self.token[:12] + "…"}


class RuntimeState:
    def __init__(self, store: DataStore):
        self.store = store
        self.lock = threading.RLock()
        self.user_roles = {user: list(info["roles"]) for user, info in store.entitlements["users"].items()}
        self.access_requests: dict[str, dict] = {}
        self.uploaded: list[dict] = []
        self.incidents: dict[str, dict] = {}
        self._counters = {"REQ": 1000, "INC": 5000}

    def login(self, user_id: str) -> UserContext:
        info = self.store.entitlements["users"][user_id]
        return UserContext(user_id, info["display_name"], info["job"], tuple(self.roles(user_id)),
                           token=f"FAKE-SSO-TOKEN-{user_id}")

    def next_id(self, prefix: str) -> str:
        with self.lock:
            self._counters[prefix] += 1
            return f"{prefix}-{self._counters[prefix]}"

    def roles(self, user_id: str) -> list[str]:
        with self.lock:
            return list(self.user_roles.get(user_id, []))

    def can(self, user_id: str, workspace: str, permission: str) -> bool:
        role_map = self.store.entitlements["roles"]
        return any(role_map[role]["workspace"] == workspace and permission in role_map[role]["permissions"]
                   for role in self.roles(user_id) if role in role_map)

    def grant(self, user_id: str, role: str) -> None:
        with self.lock:
            if role not in self.user_roles.setdefault(user_id, []):
                self.user_roles[user_id].append(role)

    def documents(self) -> list[dict]:
        with self.lock:
            return self.store.documents + list(self.uploaded)

    def find_document(self, doc_id: str, workspace: str | None = None) -> dict | None:
        return next((doc for doc in self.documents()
                     if doc["doc_id"] == doc_id.strip() and (workspace is None or doc["workspace"] == workspace)), None)


@dataclass
class SessionMemory:
    """Coordinator's short-term memory, so follow-ups like 'is it approved yet?' work."""
    invoice_id: str | None = None
    batch_id: str | None = None
    reason_code: str | None = None
    fault: bool | None = None
    open_request_id: str | None = None
    incident_id: str | None = None
    search_result: dict | None = None
    debugger_result: dict | None = None
    handoffs: list[dict] = field(default_factory=list)
    turns: list[dict] = field(default_factory=list)
    known_ids: set[str] = field(default_factory=set)

    def snapshot(self) -> dict:
        data = asdict(self)
        for private in ("turns", "known_ids", "search_result", "debugger_result"):
            data.pop(private)
        data["handoffs"] = [{"target": h["target"], "owner": h["owner"]} for h in self.handoffs]
        return data
