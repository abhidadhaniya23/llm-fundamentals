"""
Input and output guardrails (layer 1 of the diagram), plus sanitising of tool results.

Rule-based on purpose: they are deterministic and testable. The topic filter is
the one LLM-based check (a strict-JSON classifier call).
"""

import json
import re

from das.llm import LLMClient

INJECTION_PATTERNS = {
    "addressed-to-ai": r"\b(?:AI assistant|AI|assistant|chatbot|LLM)\b\s*[,:]\s*(?:ignore|disregard|forget|you must|send|reveal)",
    "ignore-rules": r"\b(?:ignore|disregard|forget)\b.{0,30}\b(?:rules|instructions|guidelines|previous)\b",
    "role-override": r"\byou are now\b|\bact as (?:an? )?(?:admin|system|developer)\b",
    "prompt-leak": r"\b(?:system|developer) prompt\b|\breveal\b.{0,30}\b(?:prompt|instructions|secrets?)\b",
    "jailbreak": r"\bjailbreak\b|\bDAN mode\b",
    "exfiltration": r"\b(?:send|forward|email|exfiltrate)\b.{0,60}\b(?:access list|passwords?|tokens?|credentials|all records)\b",
}

PII_PATTERNS = {
    "email": r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+",
    "phone": r"\+\d{1,3}[\s-]?\(?\d+\)?[\d\s-]{5,}\d",
    "iban": r"\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}(?:\s?[A-Z0-9]{1,4})?\b",
}

ID_PATTERN = re.compile(r"\b(?:REQ-\d+|INC-\d+|BATCH-\d{4}-\d{2}-\d{2}-\d{3}|\d{4})\b")
REMOVED = "[removed: suspected embedded instruction]"


def detect_injection(text: str) -> list[tuple[str, int]]:
    """(pattern name, match start) for every injection pattern found."""
    found = []
    for name, pattern in INJECTION_PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            found.append((name, match.start()))
    return found


def redact_pii(text: str, replacement: str = "[{kind} redacted]") -> tuple[str, list[str]]:
    kinds = []
    for kind, pattern in PII_PATTERNS.items():
        text, count = re.subn(pattern, replacement.format(kind=kind), text)
        kinds += [kind] * count
    return text, kinds


def sanitize(value, path: str = "$") -> tuple[object, list[dict]]:
    """Cut suspected instructions out of retrieved data (e.g. doc 1236's title). Returns (clean, findings)."""
    if isinstance(value, str):
        hits = detect_injection(value)
        if not hits:
            return value, []
        cut = min(start for _, start in hits)
        return value[:cut] + REMOVED, [{"path": path, "patterns": [name for name, _ in hits]}]
    if isinstance(value, dict):
        clean, findings = {}, []
        for key, item in value.items():
            clean[key], found = sanitize(item, f"{path}.{key}")
            findings += found
        return clean, findings
    if isinstance(value, list):
        clean, findings = [], []
        for index, item in enumerate(value):
            item, found = sanitize(item, f"{path}[{index}]")
            clean.append(item)
            findings += found
        return clean, findings
    return value, []


def collect_ids(value) -> set[str]:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    return set(ID_PATTERN.findall(text))


def extract_json(text: str | None):
    """Parse a JSON object from an LLM reply, tolerating ```json fences or surrounding prose."""
    if not text:
        raise ValueError("empty reply")
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start == -1 or end <= start:
            raise ValueError("no JSON object in reply")
        return json.loads(cleaned[start:end + 1])


TOPIC_PROMPT = (
    "You are the topic filter of a document-archive chatbot (DAS). Decide whether the user's message is "
    "about the archive: finding documents, uploads and ingestion batches, rejections, retention, archive "
    "access or the status of archive requests. Short follow-ups about an ongoing archive conversation "
    "count as on-topic. Answer with ONLY JSON: {\"on_topic\": true|false, \"reason\": \"<short>\"}"
)


def check_topic(llm: LLMClient, text: str, history_hint: str = "") -> tuple[bool, str, object]:
    message = f"Conversation so far: {history_hint}\n\nMessage: {text}" if history_hint else text
    reply = llm.chat("InputGuardrail", [{"role": "system", "content": TOPIC_PROMPT},
                                        {"role": "user", "content": message}])
    try:
        verdict = extract_json(reply.content)
        return bool(verdict["on_topic"]), str(verdict.get("reason", "")), reply
    except (ValueError, KeyError, TypeError):
        return False, "topic classifier returned no valid verdict (fail closed)", reply


def check_output(text: str, known_ids: set[str], restricted_ids: set[str]) -> tuple[str, list[str]]:
    """Returns (PII-masked text, problems). Problems block the reply."""
    problems = []
    for found in sorted(set(ID_PATTERN.findall(text))):
        if found in restricted_ids:
            problems.append(f"mentions record {found}, which the user may not see")
        elif found not in known_ids:
            problems.append(f"mentions id {found}, which no tool result or user message contains (hallucinated?)")
    masked, _ = redact_pii(text, "[{kind} masked]")
    return masked, problems
