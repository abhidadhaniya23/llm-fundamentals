"""
DAS chatbot: Coordinator + Handoff multi-agent flow for Priya's request (docs/agent-flow-architecture.html).

    uv run main.py                 live, agents driven by the Nexus LLM (LLM_FAST_* in .env); prompts for your question
    uv run main.py --message "…"   live, ask this question without prompting
    uv run main.py --offline       same flow with replayed model decisions, no Nexus needed
    uv run main.py --full          do not truncate tool results / payloads in the trace
    uv run main.py --show-prompts  also print every system prompt and full message list

Every hop is printed while it runs: numbered sections match the diagram's badges,
M ↓ / M ↑ are Manager-style calls (control returns), H ⇒ is a handoff (control moves),
TOOL→ / TOOL← are gateway calls, GUARD / BLOCK are guardrail and gateway decisions.
"""

import argparse
import os
import sys

from das.config import ConfigError, llm_settings, scenario_today
from das.gateway import auto_confirm
from das.llm import NexusClient
from das.offline import FOLLOW_UP, REQUEST, offline_llm
from das.runtime import DASChatbot
from das.trace import Tracer, install


def interactive_confirm(agent: str, tool: str, args: dict) -> bool:
    return input(f"\n  Confirm write action {tool} by {agent} with {args}? [y/N] ").strip().lower() == "y"


def show_replies(replies: list[tuple[str, str]], tracer: Tracer) -> None:
    print("\n" + tracer._paint("WHAT PRIYA SEES IN THE CHAT UI " + "═" * 32, "bold"))
    for sender, text in replies:
        print(f"\n  [{sender}]")
        for line in text.splitlines():
            print(f"    {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--message", help="ask this instead of prompting for the first question")
    parser.add_argument("--offline", action="store_true", help="replay scripted model decisions instead of calling Nexus")
    parser.add_argument("--once", action="store_true", help="exit after the first request (no follow-up prompt)")
    parser.add_argument("--today", help="scenario date, default 2026-10-30 (or DAS_TODAY)")
    parser.add_argument("--full", action="store_true", help="never truncate payloads in the trace")
    parser.add_argument("--show-prompts", action="store_true", help="print system prompts and full LLM message lists")
    parser.add_argument("--no-color", action="store_true")
    parser.add_argument("--trace-file", help="also append every trace event as JSON lines to this file")
    parser.add_argument("--confirm-writes", action="store_true", help="ask before each write action (default: auto-confirm)")
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if os.name == "nt" and not args.no_color:
        os.system("")  # enables ANSI colours in the Windows console
    tracer = install(Tracer(color=False if args.no_color else None, max_chars=0 if args.full else 700,
                            show_prompts=args.show_prompts, jsonl_path=args.trace_file))

    if args.offline:
        if args.message:
            print("--offline replays Priya's scripted scenario only; --message is ignored.")
        llm = offline_llm(with_follow_up=not args.once)
        mode = "OFFLINE replay (scripted model decisions; agents, gateway, guardrails and data are real)"
    else:
        try:
            settings = llm_settings()
        except ConfigError as error:
            print(error)
            return 2
        llm = NexusClient(settings)
        mode = f"LIVE via {settings.provider} model {settings.model}"

    bot = DASChatbot(llm, today=scenario_today(args.today),
                     confirmer=interactive_confirm if args.confirm_writes else auto_confirm)
    print(tracer._paint(f"DAS chatbot · Coordinator + Handoff · {mode} · today {bot.today}", "bold"))

    name = bot.user.display_name
    if args.offline:
        messages = [REQUEST] + ([] if args.once else [FOLLOW_UP])
    elif args.message:
        messages = [args.message]
    else:
        print(f"\nSigned in as {name} ({bot.user.job}). Sample request (press Enter to use it):\n  {REQUEST}")
        messages = [ask(f"\n{name}> ") or REQUEST]
    while messages:
        text = messages.pop(0)
        if text.lower() in ("exit", "quit"):
            break
        tracer.milestones.clear()
        replies = bot.handle(text)
        tracer.summary()
        show_replies(replies, tracer)
        if not messages and not args.once and not args.offline:
            follow_up = ask(f"\n{name}> (follow-up, empty or 'exit' to quit) ")
            if follow_up:
                messages.append(follow_up)
    return 0


def ask(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return ""


if __name__ == "__main__":
    sys.exit(main())
