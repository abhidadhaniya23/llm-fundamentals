"""
Workflows & Agents 06 · Agent

The one exercise in the notes that already is an agent: the LLM picks a
tool, sees the result, and decides again until it can answer. The notes'
version (add, multiply, divide on "3 and 4") is the warm-up. The main task
needs lookups and several steps the model cannot see in advance: price a
cat café order from a catalog, a discount code, shipping, tax and an
exchange rate.

    task -> LLM --tool call--> tool (code) --result--+
             ^                                       |
             +---------------------------------------+
             --no tool call--> answer

shared.run_agent is the hand-rolled loop (LangGraph's llm_call +
environment nodes and should_continue edge). Code checks the answer
against a total it computes itself, and that the number came out of a
tool, not the model's head.

Run it:
    uv run labs/wf06_agent.py
"""

import shared
import wf_tools as t

ARITHMETIC = {"add": t.add, "subtract": t.subtract, "multiply": t.multiply, "divide": t.divide}

WARM_UP = "Add 3 and 4. Then, take the output and multiply by 4."

ORDER = {"kibble": 3, "scratching post": 2}
CITY, CODE, CURRENCY = "bergen", "WHISKERS10", "EUR"
TASK = ("Our cat café in Bergen is ordering 3 bags of salmon kibble and 2 scratching "
        "posts, with discount code WHISKERS10. What do we pay in total, in EUR?")

PROMPT = ("You are a helpful assistant tasked with performing arithmetic on a set of inputs. "
          "Do every calculation with the tools, never in your head, one step at a time.")


def number_of(final) -> float:
    value = final.get("total") if isinstance(final, dict) else final
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError('final must be {"total": <number>}') from None


def recorded(tools: dict, results: list[float]) -> dict:
    """Wrap tools so code keeps every number they returned."""
    def wrap(fn):
        def call(a: float, b: float) -> float:
            results.append(fn(a, b))
            return results[-1]
        call.__doc__ = fn.__doc__
        return call
    return {name: wrap(fn) for name, fn in tools.items()}


def warm_up() -> None:
    results: list[float] = []

    def validate(final) -> float:
        if (total := number_of(final)) != 28:
            raise ValueError(f"{total} is not right; redo the steps with the tools")
        return total

    total = shared.run_agent("Calculator", PROMPT + '\nFinal answer: {"total": <number>}',
                             WARM_UP, recorded(ARITHMETIC, results), validate=validate)
    print(f"\nWarm-up answer: {total}  (tool results along the way: {results})")


def cafe_order() -> None:
    results: list[float] = []
    expected = t.cafe_total(ORDER, CITY, CODE, CURRENCY)

    def validate(final) -> float:
        total = number_of(final)
        if not any(round(r, 2) == round(total, 2) for r in results):
            raise ValueError(f"{total} did not come out of a tool; compute it with the tools")
        if round(total, 2) != expected:
            raise ValueError(f"{total} is not right; read get_rules and check each step")
        return round(total, 2)

    tools = {"get_rules": t.get_rules, "get_price": t.get_price, "get_discount": t.get_discount,
             "get_shipping": t.get_shipping, "get_tax_rate": t.get_tax_rate,
             "exchange_rate": t.exchange_rate, **recorded(ARITHMETIC, results)}
    total = shared.run_agent("Café Agent", PROMPT + " Look up every price, rate and rule "
                             "with the tools; do not assume any.\n"
                             'Final answer: {"total": <number>, "working": "<one line per step>"}',
                             TASK, tools, max_steps=25, validate=validate)
    print(f"\nCafé order total: {total} {CURRENCY}  (code's own total: {expected})")


def main() -> None:
    warm_up()
    cafe_order()
    shared.print_usage()


if __name__ == "__main__":
    main()
