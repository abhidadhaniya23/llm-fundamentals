"""
Check that the Nexus deployment supports OpenAI-style tool calling (the agents depend on it).

    uv run scripts/probe_tools.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from das.config import ConfigError, llm_settings  # noqa: E402
from das.llm import LLMError, NexusClient  # noqa: E402

TOOL = {"type": "function", "function": {
    "name": "get_record", "description": "Fetch an archived record by id.",
    "parameters": {"type": "object", "properties": {"doc_id": {"type": "string"}}, "required": ["doc_id"]}}}


def main() -> int:
    try:
        client = NexusClient(llm_settings(), timeout=60)
        result = client.chat("probe", [{"role": "user", "content": "Fetch archived record 1234 using the tool."}], [TOOL])
    except (ConfigError, LLMError) as error:
        print(f"FAILED: {error}")
        return 1
    if result.tool_calls:
        call = result.tool_calls[0]
        print(f"OK: tool calling works ({call.name} {call.arguments}); endpoint {client.url.split('?')[0]}")
        return 0
    print(f"NO TOOL CALL: the model answered with text instead: {result.content!r}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
