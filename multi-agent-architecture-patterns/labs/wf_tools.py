"""
Tools for the Workflows & Agents labs (wf00-wf06): plain Python, no AI.

Agents call these through shared.run_agent; the docstrings are what the
model reads to choose between them. Validators in the labs call the same
functions, so "the agent says it checked" and "code checked" use one rule.

Data lives in data/workflows/. Self-check, no LLM needed:
    uv run labs/wf_tools.py
"""

import json
import re
from functools import cache
from pathlib import Path

DATA = Path(__file__).parent.parent / "data" / "workflows"


@cache
def _load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


# ── The office move: facts, plain-language checks ────────────────────────────

def lookup_facts(topic: str) -> list[dict]:
    """Facts about the office move matching a keyword (e.g. 'parking',
    'packing', 'fire', 'date'). Returns [{id, fact}]. An empty topic lists all."""
    topic = topic.lower().strip()
    hits = [f for f in _load("office_facts.json")
            if not topic or topic in f["fact"].lower() or any(topic in t for t in f["tags"])]
    return [{"id": f["id"], "fact": f["fact"]} for f in hits]


def get_fact(fact_id: str) -> dict | None:
    """One office-move fact by its id (e.g. 'O07'), or null if there is no such fact."""
    return next(({"id": f["id"], "fact": f["fact"]} for f in _load("office_facts.json")
                 if f["id"] == fact_id.strip().upper()), None)


_MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december"
_DAYS = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"


def check_essentials(text: str) -> dict:
    """Does a notice say when (a date) and who to contact (an email address)?
    Returns {ok, missing}."""
    lower = text.lower()
    missing = []
    if not (re.search(rf"\b\d{{1,2}}\s+({_MONTHS})\b", lower) or re.search(rf"\b({_DAYS})\b", lower)):
        missing.append("a date")
    if not re.search(r"[\w.-]+@[\w.-]+\.\w+", text):
        missing.append("a contact email address")
    return {"ok": not missing, "missing": missing}


def check_jargon(text: str) -> list[dict]:
    """Jargon from the style guide found in the text, with the plain word to
    use instead: [{term, use_instead}]. An empty list means none found."""
    lower = text.lower()
    return [{"term": term, "use_instead": plain or "(leave it out)"}
            for term, plain in _load("style_guide.json")["jargon"].items()
            if re.search(rf"\b{re.escape(term)}\b", lower)]


def check_sentences(text: str) -> dict:
    """Sentence length against the style guide (max 25 words). Returns
    {max_words, limit, too_long: [the start of each long sentence]}."""
    limit = _load("style_guide.json")["max_sentence_words"]
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    lengths = [(len(s.split()), s) for s in sentences]
    return {"max_words": max((n for n, _ in lengths), default=0), "limit": limit,
            "too_long": [s[:60] + "…" for n, s in lengths if n > limit]}


def plain_language_problems(text: str) -> list[str]:
    """Every plain-language rule the text breaks, for validators."""
    problems = [f"jargon '{j['term']}': use '{j['use_instead']}'" for j in check_jargon(text)]
    problems += [f"sentence over {check_sentences(text)['limit']} words: {s!r}"
                 for s in check_sentences(text)["too_long"]]
    return problems


def count_words(text: str) -> int:
    """Number of words in the text."""
    return len(text.split())


def count_chars(text: str) -> int:
    """Number of characters in the text, spaces included."""
    return len(text)


_STOP = set("a an the of to in on at and or but is are was were be it its it's this that "
            "with for as by from i you he she they we my your his her their our what why "
            "how do does did so too very just can not no".split())


def _stem(word: str) -> str:
    """A rough stem so 'park', 'parking' and 'parks' match."""
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    return word


def _content(text: str) -> set[str]:
    return {_stem(w) for w in _words(text) if w not in _STOP and len(w) > 2}


# ── Employees and the help desk (routing) ────────────────────────────────────

def get_employee(employee_id: str) -> dict | None:
    """An employee's profile: name, role, team, zone, how they work, notes."""
    return next((e for e in _load("employees.json") if e["id"] == employee_id.strip()), None)


def search_kb(dept: str, query: str) -> list[dict]:
    """Search one department's help articles ('it', 'facilities' or 'hr').
    Returns up to 3 {id, title}, best first. Read one with read_article."""
    scored = [(_score(query, a["title"], a["text"]), a) for a in _load("helpdesk_kb.json")
              if a["dept"] == dept.lower().strip()]
    return [{"id": a["id"], "title": a["title"]} for s, a in sorted(scored, key=lambda x: -x[0]) if s > 0][:3]


def read_article(article_id: str) -> dict | None:
    """The full text of one help article, by id (e.g. 'FAC-01')."""
    return next((a for a in _load("helpdesk_kb.json") if a["id"] == article_id.strip().upper()), None)


def cited_articles(text: str) -> set[str]:
    """Help-article ids cited as [ID] in a text, e.g. [IT-01]."""
    return set(re.findall(r"\[((?:IT|FAC|HR)-\d\d)\]", text))


# ── Papers (orchestrator-worker) ─────────────────────────────────────────────

def _score(query: str, *fields: str) -> int:
    q = _content(query)
    return sum(len(q & _content(f)) for f in fields)


def list_papers() -> list[dict]:
    """Every paper in the library: id, title, year, tags. No summaries."""
    return [{k: p[k] for k in ("id", "title", "year", "tags")} for p in _load("papers.json")]


def search_papers(query: str) -> list[dict]:
    """Papers relevant to a query, best first: id, title, year (no summary)."""
    scored = [(_score(query, p["title"], " ".join(p["tags"]), p["summary"]), p) for p in _load("papers.json")]
    return [{"id": p["id"], "title": p["title"], "year": p["year"]}
            for s, p in sorted(scored, key=lambda sp: -sp[0]) if s > 0][:5]


def read_paper(paper_id: str) -> dict | None:
    """The full summary and key claims of one paper, by id."""
    return next((p for p in _load("papers.json") if p["id"] == paper_id.strip()), None)


def paper_ids() -> set[str]:
    return {p["id"] for p in _load("papers.json")}


def cited_papers(text: str) -> set[str]:
    """Paper ids cited as [id] in a text."""
    return set(re.findall(r"\[([a-z]+\d{4})\]", text))


# ── Mock web search (augmented LLM) ──────────────────────────────────────────

def web_search(query: str) -> list[dict]:
    """Search the web. Returns up to 4 results: id, title, source (no text).
    Use read_result(id) to read one. Results can be off-topic: refine the
    query if they are."""
    scored = [(_score(query, s["title"], s["text"]), s) for s in _load("search_snippets.json")]
    return [{"id": s["id"], "title": s["title"], "source": s["source"]}
            for sc, s in sorted(scored, key=lambda x: -x[0]) if sc > 0][:4]


def read_result(result_id: str) -> dict | None:
    """The full text of one search result, by id (e.g. 'W03')."""
    return next((s for s in _load("search_snippets.json") if s["id"] == result_id.strip().upper()), None)


# ── Cat café (agent) ─────────────────────────────────────────────────────────

def get_price(item: str) -> dict:
    """Catalog price in NOK for an item (partial names work, e.g. 'kibble')."""
    catalog = _load("cafe.json")["catalog"]
    hits = {name: price for name, price in catalog.items() if item.lower().strip() in name}
    if len(hits) != 1:
        return {"error": f"{len(hits)} matches", "catalog": list(catalog)}
    (name, price), = hits.items()
    return {"item": name, "price_nok": price}


def get_shipping(city: str) -> dict:
    """Shipping cost in NOK to a city."""
    return {"city": city, "shipping_nok": _load("cafe.json")["shipping"][city.lower().strip()]}


def get_tax_rate(city: str) -> dict:
    """VAT rate for a city as a fraction (0.25 = 25%)."""
    return {"city": city, "tax_rate": _load("cafe.json")["tax_rates"][city.lower().strip()]}


def get_discount(code: str) -> dict:
    """What a discount code gives, and its conditions."""
    codes = _load("cafe.json")["discount_codes"]
    return codes.get(code.strip().upper()) or {"error": f"unknown code {code!r}"}


def get_rules() -> str:
    """The order of operations for pricing an order. Read this first."""
    return _load("cafe.json")["rules"]


def exchange_rate(currency: str) -> dict:
    """How many units of a currency one NOK buys (e.g. EUR)."""
    return {"from": "NOK", "to": currency.upper(), "rate": _load("cafe.json")["fx_to"][currency.upper()]}


def add(a: float, b: float) -> float:
    """a + b"""
    return a + b


def subtract(a: float, b: float) -> float:
    """a - b"""
    return a - b


def multiply(a: float, b: float) -> float:
    """a * b"""
    return a * b


def divide(a: float, b: float) -> float:
    """a / b"""
    return a / b


def cafe_total(items: dict[str, int], city: str, code: str, currency: str) -> float:
    """Ground truth in code, used only to check the agent's answer."""
    cafe = _load("cafe.json")
    subtotal = sum(get_price(name)["price_nok"] * qty for name, qty in items.items())
    discount = cafe["discount_codes"].get(code, {})
    if subtotal >= discount.get("min_subtotal", 0):
        subtotal *= 1 - discount.get("percent", 0) / 100
    taxable = subtotal + cafe["shipping"][city]
    total = taxable * (1 + cafe["tax_rates"][city])
    return round(total * cafe["fx_to"][currency], 2)


if __name__ == "__main__":
    assert len(lookup_facts("parking")) >= 1 and get_fact("o07")["id"] == "O07"
    assert check_essentials("We move on Monday 7 December. Ask move-team@example.com.")["ok"]
    assert check_essentials("We move soon.")["missing"] == ["a date", "a contact email address"]
    assert [j["term"] for j in check_jargon("Going forward we will leverage synergies.")] == \
        ["leverage", "going forward", "synergies"]
    assert check_sentences("Short one. " + "word " * 30 + ".")["too_long"]
    assert get_employee("e3")["name"] == "Chloe Martin"
    assert search_kb("facilities", "where can I park my car")[0]["id"] == "FAC-01"
    assert cited_articles("See [IT-01] and [FAC-04].") == {"IT-01", "FAC-04"}
    assert search_papers("compute-optimal tokens per parameter")[0]["id"] == "hoffmann2022"
    assert cited_papers("as shown [kaplan2020] and [hoffmann2022].") == {"kaplan2020", "hoffmann2022"}
    assert web_search("calcium CT score cholesterol statin")[0]["id"] in {"W01", "W02", "W03", "W04"}
    assert cafe_total({"kibble": 3, "scratching post": 2}, "bergen", "WHISKERS10", "EUR") == 232.42
    print("wf_tools self-check passed")
