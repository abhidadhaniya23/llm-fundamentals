"""
Settings, read only from the environment (or the project's .env file).

The LLM comes from the MB Nexus portal, configured with the LLM_FAST_* variables.
Nothing is hardcoded: a missing variable is reported by name, never by value.
"""

import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCENARIO_TODAY = "2026-10-30"  # the day after Priya's 20-invoice upload batch in data/


class ConfigError(Exception):
    pass


def load_env_file(path: Path = PROJECT_ROOT / ".env") -> None:
    """Read KEY=VALUE lines from .env. The project's .env wins over variables set system-wide."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ[name.strip()] = value.strip().strip("'\"")


@dataclass(frozen=True)
class LLMSettings:
    provider: str
    model: str
    api_url: str
    api_key: str
    api_version: str | None

    def __repr__(self) -> str:  # never print the key
        return f"LLMSettings(provider={self.provider!r}, model={self.model!r}, api_url={self.api_url!r}, api_version={self.api_version!r})"


def llm_settings() -> LLMSettings:
    load_env_file()
    required = ("LLM_FAST_MODEL", "LLM_FAST_API_URL", "LLM_FAST_API_KEY")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        raise ConfigError(
            f"Missing {', '.join(missing)}. Set them in .env (see .env.example) or run with --offline."
        )
    return LLMSettings(
        provider=os.environ.get("LLM_FAST_PROVIDER", "nexus"),
        model=os.environ["LLM_FAST_MODEL"],
        api_url=os.environ["LLM_FAST_API_URL"],
        api_key=os.environ["LLM_FAST_API_KEY"],
        api_version=os.environ.get("LLM_FAST_API_VERSION") or None,
    )


def scenario_today(override: str | None = None) -> date:
    load_env_file()
    return date.fromisoformat(override or os.environ.get("DAS_TODAY") or SCENARIO_TODAY)
