# Business Context Document

**System**: DC Flow — Demand Assistant (EPIC-LODA-2026-001)
**Generated**: 2026-11-13, via repository scan + stakeholder Q&A
**Sources**:  `context/DC.md`, current codebase under `src/dc_flow/`

---

## 1. Why This System Exists

LoDA (the team that runs the Demand Handling & Consulting process) spends **25–30 days of its own time per demand** on work that doesn't require human judgement: reading inbound messages and typing them into JIRA, chasing the same questionnaire gaps over multiple rounds, writing up call minutes and draft BRD/DDS documents by hand, emailing approvers with no tracking, estimating effort from scratch each time, and manually chasing signatures and purchase orders. None of this is the actual value LoDA provides — the value is in scoping, deciding, and consulting. DC Flow exists to remove the administrative and drafting load around the process so LoDA's people spend their time on judgement calls, not paperwork.

The process itself is not broken or being redesigned — it's well-defined and already anchored in JIRA as the system of record. The problem is that **every handoff between process steps waits for a person to notice it**, with no automation or tracking filling the gaps.

## 2. Business Problem & Impact

| Who is affected | What breaks without this system |
| --- | --- |
| **Demand Owners** | Spend more time writing (minutes, BRD/DDS drafts, follow-up emails) than consulting; personally track dozens of demands with spreadsheets and reminders because there is no system doing it for them |
| **Business Partners** (e.g. the example used throughout, Sabine Krüger / Finance Operations) | Experience slow, inconsistent communication; demands can sit for weeks waiting on an internal step they have no visibility into |
| **Tech Architect / TPO and LoDA Manager** | Receive approval requests by email/meeting with no SLA tracking, no reminders, and no visibility into how many approvals are pending across the pipeline |
| **LoDA leadership** | Cannot currently prove how long LoDA actually holds a demand (no reliable JIRA timestamp baseline exists) or compare performance across time, because the JIRA trail is incomplete — updates are made late or skipped, closure reasons go unrecorded |
| **Product Team** | Receives hand-offs and feasibility requests without a consistent, evidence-backed package, and finds out about new SA/PO work manually |

**Today**: ~2–3 months end to end per demand, of which ~25–30 days is LoDA-held time and ~30 hours of manual effort.
**Target**: ≤5 days LoDA-held time, ≤8 hours manual effort, AI-drafted items ready in under 30 minutes.

## 3. Users & Stakeholders

| Role | Responsibilities | Relationship to the assistant |
| --- | --- | --- |
| **Demand Owner** | Owns each demand end to end; approves all AI-drafted outbound communication; makes the scope decision and runs calls; prepares the commercial package | Primary user — reviews/approves nearly every A2 draft, decides every A3 recommendation |
| **Tech Architect / TPO** | Co-approves complex demands (with LoDA Manager); assesses technical feasibility with the Product Team; gives final technical approval before baseline | Approver on complex/feasibility gates |
| **LoDA Manager** | Super admin: has all Demand Owner and Tech Architect/TPO permissions; co-approves complex demands; approves cost estimate and SA; **may approve items they themselves prepared** (exempted from the approver≠requester rule because they are the final authority in the chain, and the team is too small to insert a second approver above them — every such approval is logged as the compensating control) | Monitors the whole pipeline and SLAs; final approver |
| **Business Partner** (secondary user) | Raises the original demand; completes questionnaires; accepts or rejects cost estimates; signs the SA | Does not interact with the assistant directly — receives faster, more consistent communication from the Demand Owner, drafted by the assistant |
| **Product Team** (secondary user) | Assesses technical feasibility; receives hand-over packs; executes SA/project creation steps | Receives evidence packs and start notifications; not a direct system user in the current scope |

## 4. Value Creation Points

- **Capacity, not (primarily) revenue.** LoDA's funding model is mixed — mostly a cost center operating on a fixed budget, with some demands billable or cost-recoverable depending on the arrangement with the business partner. The dominant value created by DC Flow is **more demand capacity for the same headcount/budget** (10–30 → 30+ demands/month with the same team); for billable demands specifically, faster throughput also has a direct cost-recovery/revenue benefit.
- **Consistency of communication**, independent of which Demand Owner is handling a given demand — templates, drafts and evidence packs come from the same source rather than each owner's personal style and memory.
- **A complete, trustworthy JIRA audit trail** — every step, decision and reason logged, which today is "partial" at best. This itself has value for pipeline reporting and for proving the before/after business case.
- **Reusable institutional knowledge.** Past demands (e.g. the reference example, DEM-0915) are currently **tribal knowledge** — in people's heads and scattered across old JIRA tickets, not a maintained library. The Knowledge Base (`STORY-LODA-2026-021`) is building this capability from near-zero, not digitizing something that already exists in structured form. This is both a value creator (better triage/feasibility/estimates over time) and a near-term risk (early recommendations have a thin evidence base until the library is populated).

## 5. Core Business Domains

Derived from the epic's five process stages and the stories/code built against them:

| Domain | What it covers | Status in the codebase |
| --- | --- | --- |
| **Intake & Classification** | Reading inbound BP messages, deciding new/update/not-a-demand, registering in JIRA | Not yet built (`STORY-LODA-2026-001`) |
| **Requirements (Questionnaire + BRD/DDS)** | Sending/merging questionnaires, gap detection, BRD/DDS drafting and completeness checks | Document parsing and per-demand SharePoint document flow built (`demand_documents.py`, `parsers/`); the agent logic that drives the conversation is not yet built |
| **Alignment & Triage** | Call prep, minutes, scope/complexity recommendation, complex-demand approval routing | Not yet built; depends on Knowledge Base and Approval Service |
| **Technical Feasibility** | Evidence pack for the Product Team, TPO final approval, baseline freeze | Not yet built |
| **Commercials** | Effort estimation from past demands, cost package, SA cover, pricing approval | Not yet built; explicitly the domain where the local-model-only rule is strictest ("local model only, or no LLM") |
| **Handoff & Tracking** | Hand-over pack, SA/PO signature tracking, start notification | Not yet built; SAP integration explicitly **deferred** (manual status-entry fallback planned instead) |
| **Connectors (cross-cutting infrastructure)** | JIRA, Microsoft Graph (Mail, Calendar, SharePoint), document parsing | **Built** — these are the foundation every domain above depends on |
| **Audit & Compliance** | Durable record of every external-system interaction (operation, target, outcome, attempt, correlation ID) | **Built** (`AuditEventRecord`) — driven equally by compliance/InfoSec needs (proving no data left LoDA's control, who approved what) and operational needs (resolving disputes, debugging failures) |

## 6. Critical Business Workflows

The canonical example used throughout the project (`context/DC.md`) is **Sabine's demand**: a Finance Operations request to archive ~4 million supplier invoices. It illustrates the full journey:

1. **Intake** — email arrives, classified, registered in JIRA.
2. **Questionnaire** — sent, answers merged across replies; gaps are flagged (missing: access roles, data classification; vague: "before year-end close"; not stated: SAP company codes, cost centre) and a follow-up is drafted for the owner to approve.
3. **Alignment & Triage** — a pre-call brief draws on a similar past demand (DEM-0915: 3.5M invoices, SAP integration, complex, 6 months BRD-to-go-live) as evidence; the Demand Owner decides scope; if complex, both the Tech Architect/TPO and LoDA Manager must approve.
4. **Requirements** — detailed call(s), minutes, BRD/DDS completeness checks against the template, repeated until complete.
5. **Technical Feasibility** — Product Team assesses with similar-demand evidence supplied by the assistant; TPO gives final approval; BRD/DDS is baselined and frozen.
6. **Commercials** — cost estimate and final package (BRD, DDS, and DPoB **when the demand is finance-related**) assembled using effort data from past demands (local model only); BP accepts or the demand closes.
7. **Handoff** — SA issued, signature and PO tracked with reminders; Product Team notified to start.

**Every "no" along this journey ends in the same state, "Demand closed," distinguished only by a logged `closed_reason`** (e.g. `out_of_scope`, `not_accepted`, `feasibility_rejected`, `cost_not_accepted`) — there is no separate rejection workflow per decision point.

## 7. Business Rules & Constraints

- **No decision diamond is ever automated.** The assistant may only propose; a named person always decides. This is the project's single non-negotiable rule ("AI prepares the evidence. People make the decisions.").
- **No outbound message to a Business Partner leaves LoDA without human approval**, except the pre-approved questionnaire template and standard reminders.
- **Local-model-only AI routing, for every data class, on every demand** — a blanket internal risk stance, not tied to one named contract or regulation (e.g. not a specific GDPR clause or OEM data-handling term). It applies uniformly regardless of which business partner or data class is involved.
  - Public/internal data (product docs, templates) → local model
  - Confidential data (BRD/DDS, questionnaire answers) → local model
  - Personal data (names, emails) → masked, then local model
  - Commercially sensitive data (cost, price, SA, PO) → local model only, **or no AI at all**
- **Approver ≠ requester**, except the LoDA Manager, who may approve items they personally prepared (every such approval is logged as the compensating control rather than requiring a second signature).
- **Complex demands always require two approvals**: Tech Architect/TPO **and** LoDA Manager — never either alone.
- **JIRA is the single source of truth for demand stage.** No parallel state machine; every stage transition is a JIRA write.
- **SAP integration is explicitly deferred.** The Handoff step uses a manual status-entry fallback until SAP connectivity is separately prioritized and scoped — this is a conscious scope cut, not an oversight.

## 8. Success Metrics

There is **no single headline metric** — leadership cares about the following as a balanced set, and trade-offs between them (e.g. speed vs. draft quality) should be surfaced, not resolved by silently favoring one:

| Metric | Baseline (estimated) | Target |
| --- | --- | --- |
| LoDA-held time per demand | 25–30 days | ≤ 5 days |
| Total manual effort per demand | ~30 hrs | ≤ 8 hrs |
| AI draft turnaround | – | < 30 minutes |
| Questionnaire follow-up rounds | ~3 | ≤ 1.5 |
| Approval turnaround | 5–10 days | ≤ 2–3 business days |
| Demands per month (same team) | 10–30 | 30+ |
| JIRA completeness | Partial | 100% of steps + closure reasons |
| AI draft acceptance rate | – | ≥ 80% approved with only minor edits |

**No reliable baseline exists today** — JIRA timestamps are incomplete, so the plan is to pull 3 months of historical JIRA data before go-live to validate these targets (flagged as risk R4 in the epic).

## 9. Explicit Non-Goals

- **Redesigning the DC process.** The five stages and their decision points are fixed; this system automates around them, not instead of them.
- **Automating any human decision.** Scope judgement, technical feasibility assessment, pricing approval, commercial negotiation, and signing documents remain fully human (level "H" in the epic's automation-level scheme).
- **SAP / SA-process integration** — deferred to a future, separately scoped effort.
- **A shared, externally-reusable connector platform.** The JIRA/Mail/Calendar/SharePoint connectors are deliberately built decoupled (parameter-driven, no DC-Flow-specific logic hard-coded) but are **not** being extracted into a shared LoDA-level package now — that is a separate, deferred story (`STORY-LODA-2026-022`), triggered only once a second project actually needs to reuse one.
- **Any AI route other than the local/on-prem model.** No external or public AI provider is used for any data class, on any demand.

## 10. Assumptions & Open Questions

**Confirmed assumptions (validated with stakeholder):**
- LoDA's funding is mixed: a cost center with a fixed budget, plus some billable/cost-recoverable demands — efficiency gains translate mostly into capacity, partly into direct cost recovery.
- The LoDA Manager's self-approval exemption is permanent operating practice (final authority + small team size), not a temporary gap to be closed as the team grows.
- **Local model only** is the confirmed, current-state approach for every demand, regardless of domain — a blanket internal risk stance, not tied to one named external obligation. It stays as-is with no near-term need to formalize it into a named policy document or contract reference.
- **DPoB** is a detailed finance-related document, similar in nature to the DDS, and is required **only for finance-related demands** (e.g. financial data archival, as in the Sabine/supplier-invoices example) — not a universal deliverable. Its exact acronym expansion is still informal, but scope and purpose are confirmed.
- **The SharePoint share-link hand-off is a planned future capability of the Demand Assistant**, not a permanent manual control point. The assistant will generate and send the share link to the Business Partner directly, rather than the Demand Owner doing this by hand — target state only; see `context/TECHNICAL_CONTEXT.md` section 2 for the current manual-only state of `demand_documents.py`.

**Open questions carried forward:**
1. The remaining items already listed as open in the epic itself (`artifacts/epics/dc-flow-automation-epic.md`, "Open Questions"): the "already exists" message-linking assumption; whether BP acceptance of the cost estimate is a separate formal gate; what happens when the LoDA Manager rejects a commercial package vs. when the BP rejects a cost estimate; confirming data classes and model routing with InfoSec and Data Protection; and approver SLAs/delegates for the Tech Architect/TPO and LoDA Manager.
