"""
One chatbot session: input guardrails → Coordinator → output guardrails → reply,
then the queued handoffs run under their new owners (C, or E for system faults).
"""

from datetime import date

from das import guardrails
from das.agent import AgentError
from das.config import scenario_today
from das.gateway import ToolContext, auto_confirm
from das.llm import LLMClient, LLMError
from das.store import DataStore, RuntimeState, SessionMemory
from das.team import ACCESS, COORDINATOR, PLATFORM, Baton, build_gateway
from das.trace import tracer

FALLBACK = ("Sorry, I couldn't put together a reliable answer for that. Please try again, "
            "or contact the records help desk.")
REFUSE_INJECTION = "I can't process that message: it looks like an attempt to change my instructions."
REFUSE_TOPIC = "I can only help with questions about the document archive (finding, uploading, access, retention)."
UNAVAILABLE = "The assistant is unavailable right now (language-model service error). Please try again later."


class DASChatbot:
    def __init__(self, llm: LLMClient, store: DataStore | None = None, user_id: str = "priya",
                 today: date | None = None, confirmer=auto_confirm):
        self.llm = llm
        self.store = store or DataStore()
        self.state = RuntimeState(self.store)
        self.today = today or scenario_today()
        self.user = self.state.login(user_id)
        self.session = SessionMemory()
        self.gateway = build_gateway(confirmer)
        self.pending_handoffs: list[Baton] = []
        self.outbox: list[tuple[str, str]] = []

    def restricted_ids(self) -> set[str]:
        return {doc["doc_id"] for doc in self.state.documents()
                if not self.state.can(self.user.user_id, doc["workspace"], "read")}

    def deliver(self, sender: str, text: str) -> None:
        self.outbox.append((sender, text))
        self.session.turns.append({"role": "assistant", "content": f"[{sender}] {text}"})
        tracer().event("SAY", sender, f"→ {self.user.display_name} (Chat UI)", text)

    def handle(self, text: str) -> list[tuple[str, str]]:
        start = len(self.outbox)
        tracer().section(1, f"USER REQUEST · {self.user.display_name}, {self.user.job}")
        with tracer().nested():
            tracer().event("SAY", self.user.display_name, "via Chat UI", text)

        tracer().section(2, "API GATEWAY + SSO")
        with tracer().nested():
            tracer().event("INFO", "API gateway", "authenticated (simulated OIDC); token scope attached to every tool call",
                           self.user.scope())

        cleaned = self._input_guardrails(text)
        if cleaned is None:
            return self.outbox[start:]

        history = list(self.session.turns)
        self.session.turns.append({"role": "user", "content": cleaned})
        with self.state.lock:
            self.session.known_ids |= guardrails.collect_ids(cleaned)
        try:
            reply, messages, ctx = COORDINATOR.run(self, cleaned, history=history)
            self._deliver_checked(reply, messages, ctx)
        except (AgentError, LLMError) as error:
            tracer().event("WARN", "Runtime", f"Coordinator failed: {error}")
            self.deliver("DAS assistant", FALLBACK)
        self._dispatch_handoffs()
        return self.outbox[start:]

    def _input_guardrails(self, text: str) -> str | None:
        tracer().section(None, "INPUT GUARDRAILS")
        with tracer().nested():
            hits = guardrails.detect_injection(text)
            if hits:
                tracer().event("BLOCK", "Input guardrail", f"prompt injection detected: {[name for name, _ in hits]}")
                tracer().count("InputGuardrail", "blocked")
                tracer().milestone("① user → input guardrail ✗ blocked (prompt injection)")
                self.deliver("DAS assistant", REFUSE_INJECTION)
                return None
            tracer().event("GUARD", "Input guardrail", "prompt-injection / jailbreak check: passed")
            cleaned, pii = guardrails.redact_pii(text)
            tracer().event("GUARD", "Input guardrail", f"PII redaction: {pii or 'nothing to redact'}")
            hint = " | ".join(turn["content"][:120] for turn in self.session.turns[-4:])
            tracer().event("LLM>", "InputGuardrail", "topic classifier (archive questions only)")
            try:
                on_topic, reason, reply = guardrails.check_topic(self.llm, cleaned, hint)
            except LLMError as error:
                tracer().event("WARN", "Input guardrail", f"topic classifier unavailable: {error}")
                tracer().milestone("① user → input guardrail: LLM unavailable, request not processed")
                self.deliver("DAS assistant", UNAVAILABLE)
                return None
            tracer().count("InputGuardrail", "llm_calls")
            tracer().count("InputGuardrail", "prompt_tokens", reply.prompt_tokens)
            tracer().count("InputGuardrail", "completion_tokens", reply.completion_tokens)
            if not on_topic:
                tracer().event("BLOCK", "Input guardrail", f"off-topic: {reason}")
                tracer().count("InputGuardrail", "blocked")
                tracer().milestone("① user → input guardrail ✗ blocked (off-topic)")
                self.deliver("DAS assistant", REFUSE_TOPIC)
                return None
            tracer().event("GUARD", "Input guardrail", f"topic filter: on-topic ({reason})")
            tracer().milestone(f"① {self.user.display_name} → ② SSO {list(self.user.login_roles)} → input guardrails ✓ "
                               f"(injection: none, PII: {len(pii)}, topic: on) → ③ Coordinator")
            return cleaned

    def _deliver_checked(self, reply: str, messages: list[dict], ctx: ToolContext) -> None:
        for attempt in (1, 2):
            tracer().section(8, "OUTPUT GUARDRAILS (Coordinator reply)")
            with tracer().nested():
                masked, problems = guardrails.check_output(reply, self.session.known_ids, self.restricted_ids())
                cited = sorted(guardrails.collect_ids(reply))
                if not problems:
                    tracer().event("GUARD", "Output guardrail", f"passed: cited ids {cited} all come from tool results; "
                                                                "PII masked; no restricted records")
                    tracer().milestone(f"⑧ output guardrail ✓ → Coordinator reply delivered (cites {cited})")
                    self.deliver("DAS assistant", masked)
                    return
                tracer().event("BLOCK", "Output guardrail", f"attempt {attempt}: reply blocked", problems)
                tracer().count("OutputGuardrail", "blocked")
            if attempt == 1:
                reply = COORDINATOR.resume(self, messages, ctx, "OUTPUT GUARDRAIL blocked your reply: "
                                           + "; ".join(problems) + ". Rewrite it citing only real ids.")
        tracer().milestone("⑧ output guardrail ✗ twice → safe fallback delivered")
        self.deliver("DAS assistant", FALLBACK)

    def _dispatch_handoffs(self) -> None:
        while self.pending_handoffs:
            baton = self.pending_handoffs.pop(0)
            try:
                if baton.target == ACCESS.name:
                    output, _, _ = ACCESS.run(self, baton.to_dict())
                    tracer().milestone(f"⑥ C·Access finished: request={output['request_id']} access={output['access']} "
                                       f"reupload={output['reupload_status']} notified={output['notified']}")
                elif baton.target == PLATFORM:
                    self._platform_team(baton)
            except (AgentError, LLMError) as error:
                tracer().event("WARN", baton.target, f"handoff target failed: {error}")
                self.deliver(baton.reply_owner, "Your request was handed over but could not be completed "
                                                "automatically. The owning team has been informed.")

    def _platform_team(self, baton: Baton) -> None:
        tracer().section(None, "E · Developer / Platform team (humans)", "handoff target for system faults")
        with tracer().nested():
            ctx = ToolContext(self, PLATFORM)
            incident = self.gateway.call(ctx, "open_incident", {
                "invoice_id": baton.invoice_id, "batch_id": baton.batch_id,
                "reason_code": baton.reason_code, "summary": baton.request["summary"]})
            if "error" in incident:
                return
            tracer().milestone(f"E Platform team owns {incident['incident_id']}; the bot is done")
            self.deliver("Platform team (via ITSM)", f"Incident {incident['incident_id']} is open for invoice "
                         f"{baton.invoice_id} ({baton.reason_code}). The platform team owns it and will notify you.")
