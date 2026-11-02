"""
Workflows & Agents 00 · Augmented LLM, without a framework

The notes augment an LLM two ways: structured output (with_structured_output)
and a tool (bind_tools), each used ONCE. Part 1 does exactly that by hand.
Part 2 makes it an agent: one search is not enough, so the model searches,
reads, refines its query and only then returns the structured answer.

    Part 1  question -> LLM -> SearchQuery JSON  (one call, no tools)
            "2 times 3" -> LLM -> {"tool": "multiply"} -> code runs it once
    Part 2  question -> Research Agent <-> web_search / read_result (loop)
                     -> SearchQuery + answer, validated in code

Run it:
    uv run labs/wf00_augmented_llm.py
"""

import json

from pydantic import BaseModel, Field, ValidationError

import shared
import wf_tools as t

QUESTION = "How does Calcium CT score relate to high cholesterol?"


class SearchQuery(BaseModel):
    search_query: str = Field(description="Query that is optimized for web search.")
    justification: str = Field(description="Why this query is relevant to the user's request.")


class ResearchAnswer(SearchQuery):
    answer: str = Field(description="A short answer to the question, from the sources only.")
    sources: list[str] = Field(description="Ids of the search results the answer is based on.")


# ── Part 1: the augmented LLM, one call each ─────────────────────────────────

def structured_output() -> SearchQuery:
    """with_structured_output by hand: describe the schema, parse, validate."""
    schema = json.dumps(SearchQuery.model_json_schema()["properties"])
    reply = shared.ask(f"Reply with one JSON object matching this schema and nothing else: {schema}",
                       QUESTION, label="Structured LLM")
    return SearchQuery.model_validate(shared._parse_json(reply))


def one_tool_call() -> float:
    """bind_tools by hand: the model names a tool and its args; code runs it."""
    reply = shared.ask('You can call multiply(a, b). Reply only with '
                       '{"tool": "multiply", "args": {"a": ..., "b": ...}}.',
                       "What is 2 times 3?", label="Tool LLM")
    call = shared._parse_json(reply)
    shared.step("Tool LLM", f"asked for {call['tool']}({call['args']})")
    return t.multiply(**call["args"])


# ── Part 2: the same augmentations inside an agent loop ──────────────────────

RESEARCH_PROMPT = (
    "You are a research assistant. Answer the user's question using web search. "
    "Search results can be off-topic: read the promising ones with read_result, and "
    "if they do not answer the question, search again with a better query. Base your "
    "answer only on results you have read, cite at least two of them, and do not give "
    "personal medical advice.\n"
    'Final answer: {"search_query": "<the query that found your sources>", '
    '"justification": "", "answer": "", "sources": ["W..", "W.."]}'
)


def research_agent() -> ResearchAnswer:
    read: set[str] = set()  # code remembers what the agent really read

    def read_tracked(result_id: str) -> dict | None:
        """The full text of one search result, by id (e.g. 'W03')."""
        result = t.read_result(result_id)
        if result:
            read.add(result["id"])
        return result

    def validate(final) -> ResearchAnswer:
        try:
            answer = ResearchAnswer.model_validate(final)
        except ValidationError as error:
            raise ValueError(str(error)) from None
        unread = [s for s in answer.sources if s.upper() not in read]
        if unread:
            raise ValueError(f"you cite {unread} but never read them with read_result")
        if len(answer.sources) < 2:
            raise ValueError("cite at least two results you read")
        return answer

    tools = {"web_search": t.web_search, "read_result": read_tracked}
    return shared.run_agent("Research Agent", RESEARCH_PROMPT, QUESTION, tools, validate=validate)


def main() -> None:
    print("── Part 1: augmented LLM, one call each ──")
    query = structured_output()
    print(f"search_query:  {query.search_query}\njustification: {query.justification}")
    print(f"multiply result: {one_tool_call()}")

    print("\n── Part 2: research agent ──")
    result = research_agent()
    print(f"\nsearch_query:  {result.search_query}\njustification: {result.justification}")
    print(f"answer:        {result.answer}\nsources:       {', '.join(result.sources)}")
    shared.print_usage()


if __name__ == "__main__":
    main()
