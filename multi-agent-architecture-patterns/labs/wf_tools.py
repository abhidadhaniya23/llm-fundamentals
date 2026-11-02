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


# ── Cat facts, puns, jokes ───────────────────────────────────────────────────

def lookup_facts(topic: str) -> list[dict]:
    """Cat facts matching a keyword (e.g. 'sleep', 'whiskers', 'egypt').
    Returns [{id, fact}]. An empty topic lists every fact."""
    topic = topic.lower().strip()
    hits = [f for f in _load("cat_facts.json")
            if not topic or topic in f["fact"].lower() or any(topic in t for t in f["tags"])]
    return [{"id": f["id"], "fact": f["fact"]} for f in hits]


def get_fact(fact_id: str) -> dict | None:
    """One cat fact by its id (e.g. 'F07'), or null if there is no such fact."""
    return next(({"id": f["id"], "fact": f["fact"]} for f in _load("cat_facts.json")
                 if f["id"] == fact_id.strip().upper()), None)


def check_punchline(text: str) -> dict:
    """Does the joke have a punchline? The same simple rule as the original
    exercise: it must contain '?' or '!'."""
    ok = "?" in text or "!" in text
    return {"has_punchline": ok, "reason": "" if ok else "no '?' or '!' found"}


def find_puns(word: str) -> list[str]:
    """Cat puns for an ordinary word, e.g. 'perfect' -> ['purr-fect']."""
    puns = _load("puns.json")
    word = word.lower().strip()
    return puns.get(word) or [p for key, ps in puns.items() if word in key for p in ps]


_STOP = set("a an the of to in on at and or but is are was were be it its it's this that "
            "with for as by from i you he she they we my your his her their our what why "
            "how do does did so too very just can not no".split())


def _content(text: str) -> set[str]:
    return {w for w in _words(text) if w not in _STOP and len(w) > 2}


def check_originality(text: str) -> dict:
    """Compare a joke with a corpus of well-known cat jokes. Returns the
    closest known joke and a word-overlap score 0..1; original means < 0.5."""
    mine = _content(text)
    best, best_score = "", 0.0
    for joke in _load("known_jokes.json"):
        theirs = _content(joke)
        score = len(mine & theirs) / max(1, min(len(mine), len(theirs)))
        if score > best_score:
            best, best_score = joke, score
    return {"original": best_score < 0.5, "overlap": round(best_score, 2), "closest_known_joke": best}


_UNSAFE = {"kill", "killed", "dead", "death", "die", "dies", "blood", "gun", "drunk", "beer",
           "hate", "stupid", "idiot", "damn", "hell", "sexy", "scary", "monster", "nightmare"}


def kid_safe(text: str) -> dict:
    """Check text for words not suitable for children. Returns {safe, flagged}."""
    flagged = sorted(set(_words(text)) & _UNSAFE)
    return {"safe": not flagged, "flagged": flagged}


def count_words(text: str) -> int:
    """Number of words in the text."""
    return len(text.split())


# ── Poems ────────────────────────────────────────────────────────────────────

def syllables(line: str) -> int:
    """Approximate syllable count of a line (a heuristic, +-1 per word)."""
    total = 0
    for word in _words(line):
        word = word.replace("'", "")
        groups = re.findall(r"[aeiouy]+", word)
        count = len(groups)
        if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
            count -= 1
        total += max(1, count)
    return total


# Common words whose spelling hides their sound: word -> a spelling that rhymes like it.
_SOUNDS_LIKE = {"done": "dun", "none": "nun", "one": "wun", "someone": "sumwun", "anyone": "enywun",
                "love": "luv", "above": "abuv", "glove": "gluv", "dove": "duv", "of": "uv",
                "come": "cum", "some": "sum", "eight": "ate", "great": "grate", "said": "sed",
                "head": "hed", "bread": "bred", "four": "for", "more": "mor", "door": "dor",
                "floor": "flor", "your": "yor", "through": "thru", "blue": "blu",
                "two": "tu", "too": "tu", "you": "yu", "who": "hu", "shoe": "shu", "new": "nu",
                "knew": "nu", "flew": "flu", "eyes": "ize", "flies": "flize", "lies": "lize"}


def _rime(word: str) -> str:
    word = re.sub(r"[^a-z]", "", word.lower())
    word = _SOUNDS_LIKE.get(word, word)
    if len(word) > 2 and word.endswith("e") and word[-2] not in "aeiouy":
        word = word[:-1]  # silent e: time -> tim
    match = re.search(r"[aeiouy]+[^aeiouy]*$", word)
    return (match.group(0) if match else word).replace("y", "i")


def rhymes(word_a: str, word_b: str) -> bool:
    """Do two words rhyme? Heuristic on their spelling: same ending from the
    last vowel sound, or the same last three letters. Prefer clear rhymes."""
    a, b = word_a.lower().strip(" .,!?;:'\""), word_b.lower().strip(" .,!?;:'\"")
    return _rime(a) == _rime(b) or (len(a) > 3 and len(b) > 3 and a[-3:] == b[-3:])


def check_limerick(poem: str) -> dict:
    """Check a limerick: 5 lines, lines 1-2-5 rhyme and 3-4 rhyme (AABBA).
    Returns {ok, problems, syllables_per_line}."""
    lines = [ln.strip() for ln in poem.strip().splitlines() if ln.strip()]
    problems = []
    if len(lines) != 5:
        return {"ok": False, "problems": [f"needs 5 lines, has {len(lines)}"], "syllables_per_line": []}
    last = [(_words(ln) or [""])[-1] for ln in lines]
    for i, j in ((0, 1), (0, 4), (2, 3)):
        if not rhymes(last[i], last[j]):
            problems.append(f"line {i + 1} '{last[i]}' and line {j + 1} '{last[j]}' do not rhyme")
    return {"ok": not problems, "problems": problems, "syllables_per_line": [syllables(ln) for ln in lines]}


# ── Readers (routing) ────────────────────────────────────────────────────────

def get_reader(reader_id: str) -> dict | None:
    """A reader's profile: age group, likes, things to avoid, past requests."""
    return next((r for r in _load("readers.json") if r["id"] == reader_id.strip()), None)


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
    assert len(lookup_facts("sleep")) >= 1 and get_fact("f07")["id"] == "F07"
    assert check_punchline("Why? Because.")["has_punchline"] and not check_punchline("A cat.")["has_punchline"]
    assert not check_originality("What do you call a pile of cats? A meowtain.")["original"]
    assert check_originality("My cat filed taxes; she claimed the sofa as a scratching expense!")["original"]
    assert not kid_safe("a scary monster")["safe"]
    assert rhymes("cat", "hat") and rhymes("night", "light") and rhymes("time", "rhyme") and not rhymes("cat", "dog")
    limerick = ("A cat with a taste for the sun\nWould nap until napping was done\nShe'd stretch and she'd yawn\n"
                "From dusk until dawn\nThen nap once again just for fun")
    assert check_limerick(limerick)["ok"], check_limerick(limerick)
    assert search_papers("compute-optimal tokens per parameter")[0]["id"] == "hoffmann2022"
    assert cited_papers("as shown [kaplan2020] and [hoffmann2022].") == {"kaplan2020", "hoffmann2022"}
    assert web_search("calcium CT score cholesterol statin")[0]["id"] in {"W01", "W02", "W03", "W04"}
    assert cafe_total({"kibble": 3, "scratching post": 2}, "bergen", "WHISKERS10", "EUR") == 232.42
    print("wf_tools self-check passed")
