# AI-Enabled LoDA Demand Handling (working title) – Product Vision

> Status: v1.0 – approved by the user on 2026-11-12. Items marked *(to be validated)* are assumptions that need confirmation by the relevant stakeholders.
>
> Source: "Demand Handling & Consulting Process Flow (LoDA)" process diagram, plus user input.

## 1. Vision Statement

Provide the LoDA demand team with one AI-enabled demand handling product that takes every demand from first contact with the Business Partner to the start of development, so that the Demand Owner, Demand Manager and technical roles no longer have to run each step, document and JIRA update manually.

**Business vision:** Convert the complete, currently manual demand process into an AI transformation in which each phase is handled at the right level of automation – direct automation, AI with suggestion, or AI with evidence – while people keep every business and technical decision.

**Focus:** Internal use case – the LoDA demand handling and consulting process, from "New demand received" to "Product Team notified to commence development".

### 1.1 Why This Product / Why Now

- Every step of the demand process is manual today (user input).
- Every step, decision and deliverable must be recorded in the JIRA demand ticket before the flow can proceed, which creates repeated manual update effort (process diagram).
- Each demand takes the Demand Owner 30–40 hours of effort and runs for 1–2 months, much of it waiting on follow-ups (user input).
- Today there are about 60 demands per year, and the number is expected to grow (user input).

## 2. Problem Statement

The Demand Owner owns each demand from start to end and is the first contact for the Business Partner. Along the way they work with the Demand Manager and with technical roles (Technical Architect, Technical Product Owner / Product Team). The process has around 20 steps (see section 7.3), 5 decision points that can end in "Demand Closed", and multiple deliverables (questionnaire, BRD, DDS, minutes of meeting, cost estimation, DPoB, Service Agreement).

Today this creates the following challenges:

- All steps are performed manually (user input).
- JIRA is the single source of truth, so status, comments and attachments must be updated by hand at almost every step (process diagram).
- Documents (BRD, DDS, minutes, cost estimation) are created and re-issued manually across several rounds with the Business Partner *(to be validated)*.
- Decisions (LoDA fit, complexity, technical approval, cost acceptance, SA/PO) depend on information spread across meetings, documents and people *(to be validated)*.

Without this product, the demand process stays fully manual and dependent on individual effort *(to be validated)*.

## 3. Target Users & Stakeholders

| Group | Interest |
|-------|----------|
| Demand Owner (primary user) | Owns the demand end to end and is the first contact for the Business Partner; needs the manual steps, documents and JIRA updates taken off their plate. Also maintains the document templates (questionnaire, BRD, DDS, Service Agreement) and performs project creation and SAP planning in the SA process – no separate admin or SAP role |
| Demand Manager | Is consulted by the Demand Owner on stakeholder and management questions; assigns the Demand Owner to each new demand (with an AI suggestion); needs a pipeline view of all demands, their status and decisions |
| Technical roles – Technical Architect, Technical Product Owner / Product Team | Consulted on technical questions; confirm complexity, assess feasibility, give final technical approval and receive the handed-over demand |
| Business Partner (external to the product, indirect) | Raises demands, completes questionnaire, BRD and DDS, accepts cost, signs Service Agreement and issues PO *(whether BPs interact with the product directly – to be validated)* |

## 4. Context & Constraints *(to be validated)*

### 4.1 Process

- The existing process flow (process diagram) is the baseline; the product automates and supports it rather than replacing its decision points *(to be validated)*.
- All "Demand Closed" exits lead to the same end state (process diagram).

### 4.2 Systems

- JIRA is the single source of truth; every step, decision outcome and deliverable must be recorded in the JIRA demand ticket before the flow proceeds (process diagram).

| System | Role in the product | Integration |
|--------|---------------------|-------------|
| JIRA Cloud (existing, company-approved) | System of record for every demand: status, comments, decisions, audit trail, links to documents | Product reads and updates tickets; mapping to the JIRA workflow statuses TBD |
| Shared demand mailbox | Single intake channel for new demands; also receives BP replies, signed Service Agreements and POs | Product reads the mailbox, detects demands and documents, attaches them to the right ticket; Demand Owner confirms |
| SharePoint / OneDrive | Master storage for all document versions (questionnaire, BRD, DDS, minutes, cost estimation, DPoB, SA) | JIRA ticket holds the link and the final baselined copy |
| Microsoft Teams | Meeting transcripts for minutes (where available); notifications | Transcripts used where available, otherwise the Demand Owner's notes; notifications via Teams and email |
| Email | Notifications and messages to the BP (after Demand Owner release) | Via the shared mailbox *(to be validated)* |
| SAP | Project creation and SAP planning (step 17) | No integration: the product prepares the data, the Demand Owner enters it in SAP and records the result in JIRA |

### 4.3 Organisational

- Decisions stay with the named roles: Architect and Manager (complexity), Technical Product Owner (final approval), Business Partner (cost acceptance, SA signature, PO) (process diagram) *(human decision ownership – to be validated)*.

## 5. Product Goals

1. **Remove manual effort from routine steps** – registration, JIRA updates and notifications happen automatically; questionnaires and reminders to the BP are prepared automatically and sent after one Demand Owner release.
2. **Speed up document work** – AI drafts BRD, DDS, minutes and other deliverables for people to review.
3. **Support better decisions** – at each decision point the responsible role sees an AI-prepared evidence pack and recommendation, and makes the decision.
4. **Keep JIRA always complete** – every step, decision and deliverable is recorded without manual re-typing.

(Measurable targets – see section 10, TBD.)

## 6. Core Capabilities (Summary)

See section 7 for details.

- Automation-level model: every process phase is assigned one of three levels – Direct Automation, AI with Suggestion, AI with Evidence.
- Automated demand intake and JIRA registration.
- AI-drafted documents (questionnaire analysis, BRD, DDS, minutes, cost estimation drafts).
- AI evidence packs for the internal decision points (LoDA fit, complexity, feasibility / TPO approval), with human decision.
- Automatic, continuous JIRA updates as the single source of truth.
- Role-based support: Demand Manager dashboard and in-product consult requests.
- AI-suggested Demand Owner assignment.
- Business Partner reminders, prepared automatically and released by the Demand Owner, with escalation.
- Learning from past demands as AI evidence.
- Demand closure with reason, BP notice and reopening.
- Handover with an AI-drafted prerequisites checklist.
- AI feedback capture and quality view for the Demand Manager.

## 7. Capabilities

### 7.1 Reference Benchmark *(optional)*

TBD

### 7.2 Automation Levels

| Level | Meaning | Who decides |
|-------|---------|-------------|
| **A – Direct Automation** | Routine, rule-based step performed by the product without human action. Exception: anything sent to the Business Partner (even fixed-template messages) is prepared automatically and sent only after the Demand Owner releases it | No decision needed; people can see and correct the result |
| **B – AI with Suggestion** | AI produces a draft or proposal (document, summary, classification) | A person reviews, edits and releases it |
| **C – AI with Evidence** | AI gathers facts, compares them with criteria and gives a recommendation with the supporting evidence | The named role makes and records the decision |

Rules that apply to all AI output:
- The AI does not show confidence levels; people review every AI output to the same standard.
- AI-written content is labelled as such in JIRA and the web app. Documents sent to the Business Partner are released by the Demand Owner as their own, in line with the company AI-use policy *(to be validated)*.
- AI evidence comes only from demands handled in the new product. Until enough of these exist (threshold TBD), the LoDA fit check (step 6) and cost drafting (steps 9 and 14) are done manually, without an AI recommendation.

### 7.3 Process Phases and Proposed Automation Level *(proposal, to be validated)*

| # | Process step (from the diagram) | Proposed level | What the product does | Human role |
|---|---------------------------------|----------------|-----------------------|-----------|
| 1 | New demand received from the Business Partner (any channel) | A + B | Captures the incoming demand from the shared demand mailbox; AI extracts the key facts and suggests a Demand Owner (e.g. workload, similar past demands) | Demand Manager assigns the Demand Owner; Demand Owner confirms the facts |
| 2 | Demand registered in JIRA | A | Creates the JIRA demand ticket automatically | – |
| 3 | Standard questionnaire issued to the BP | A | Prepares the standard questionnaire and reminders, tracks the response and alerts the Demand Owner if there is still no response | Demand Owner releases each message to the BP |
| 4 | Completed questionnaire received | A + B | Attaches it to JIRA; AI summarises it and flags gaps | Demand Owner reviews |
| 5 | Initial alignment with the BP (scope, LoDA demo, updated BRD/DDS) | B | AI prepares the meeting brief, drafts minutes (from the Teams transcript where available, otherwise the Demand Owner's notes) and the updated BRD/DDS | Demand Owner leads and releases |
| 6 | Decision: can LoDA address the demand? | C (manual until evidence threshold) | AI compares the demand with similar past demands and recommends fit / no fit, showing the past demands as evidence | Demand Owner decides *(to be validated)* |
| 7 | Decision: complex requirement confirmed with Architect and Manager? | C | AI recommends "complex" or "straightforward" with reasons | Technical Architect and Demand Manager confirm |
| 8 | Detailed requirement gathering (discussions, minutes, updated BRD/DDS) | B | AI drafts questions, minutes (Teams transcript or Demand Owner's notes) and BRD/DDS updates | Demand Owner releases |
| 9 | Indicative cost estimate on request (optional) | B (manual until evidence threshold) | AI drafts an indicative estimate based on similar past demands and their estimates | Demand Owner / Demand Manager release |
| 10 | Completed BRD and DDS received from BP | A + B | Tracks the response, prepares reminders and escalates; scans and attaches documents to JIRA; AI checks completeness and consistency | Demand Owner releases reminders and reviews |
| 11 | Technical feasibility assessed with the Product Team | C | AI prepares a feasibility evidence pack | Product Team assesses |
| 12 | Decision: final approval by the Technical Product Owner? | C | AI summarises evidence and open risks | Technical Product Owner decides |
| 13 | BRD and DDS baselined and frozen | A | Locks the versions and records the baseline in JIRA | – |
| 14 | Cost estimation shared (cost estimation, final BRD, final DDS, DPoB where required) | B (cost drafting manual until evidence threshold) | AI assembles the deliverable package and drafts the cost estimation based on similar past demands | Demand Owner releases |
| 15 | Decision: cost estimate accepted by the BP? | A | Records the BP's answer, prepares reminders while waiting, and routes the flow | Business Partner decides; Demand Owner releases reminders |
| 16 | Demand handed over to the Product Team | A + B | Creates the handover package and notifies the Product Team; AI drafts a prerequisites checklist from the final BRD/DDS | Product Team confirms the checklist and may start prerequisites early |
| 17 | SA process: project creation and SAP planning | B | Prepares the project/SAP planning data (no SAP integration) | Demand Owner enters it in SAP and records the result in JIRA |
| 18 | Service Agreement issued to the BP | B | AI drafts the Service Agreement from the agreed deliverables | Demand Owner / Demand Manager release |
| 19 | Decision: SA signed and PO received? | A | Detects the signed SA and the PO in the shared mailbox, attaches them, prepares reminders while waiting, and routes the flow | Business Partner decides; Demand Owner confirms receipt and releases reminders |
| 20 | Product Team notified to start development; demand completed | A | Sends the notification and closes the demand in JIRA | – |
| All | JIRA update at each step | A | Updates status, comments and attachments automatically | – |
| All | "Demand Closed" exits | A + B | Records a closure reason in JIRA; AI drafts the closure message to the BP; a closed demand can be reopened if the BP comes back | Demand Owner releases the message and decides on reopening |

### 7.4 Must-Have Capabilities

1. **Demand intake and registration**
   - Captures demands from the shared demand mailbox and creates the JIRA ticket with the key facts.
2. **Questionnaire and document flow**
   - Prepares the questionnaire for the Demand Owner to release, tracks responses, scans incoming documents for malware, stores all versions in SharePoint / OneDrive and links them from the JIRA ticket (final baselined copies also attached to JIRA).
3. **AI document drafting**
   - Drafts meeting briefs, minutes, BRD, DDS, cost estimation and the Service Agreement for human review.
4. **AI decision evidence packs**
   - For each decision point, prepares facts, criteria and a recommendation for the responsible role.
5. **Automatic JIRA record keeping**
   - Keeps status, comments, attachments and decision outcomes in JIRA up to date.
6. **Role-based support**
   - Gives the Demand Owner an end-to-end view of their demands.
   - Gives the Demand Manager a pipeline dashboard of all demands, status and decisions.
   - Lets the Demand Owner send consult requests to the Demand Manager (stakeholder questions) or the Technical Architect / Technical Product Owner (technical questions) from inside the product; requests and answers are logged in JIRA.
7. **Demand Owner assignment**
   - AI suggests a Demand Owner for each new demand (e.g. workload, similar past demands); the Demand Manager confirms.
8. **Business Partner follow-ups**
   - Automatically prepares reminders to the BP while the product waits for a response (questionnaire, BRD/DDS, cost acceptance, SA signature, PO); the Demand Owner releases each reminder with one action; if there is still no response, the Demand Owner is alerted. Timings TBD.
9. **Learning from past demands**
   - The AI uses past demands (including BRDs, DDSs and estimates) as evidence for the LoDA fit check and cost drafts. There is no separate LoDA capability catalogue.
   - Only demands handled in the new product are used; existing JIRA history is not used. Until enough new demands exist (threshold TBD), the fit check and cost drafting stay manual.
10. **Demand closure and reopening**
   - At every "Demand Closed" exit, records the closure reason in JIRA, drafts the closure message to the BP for the Demand Owner to release, and allows the demand to be reopened later.
11. **Handover with prerequisites checklist**
   - AI drafts a prerequisites checklist from the final BRD/DDS as part of the handover package; the Product Team confirms it and may start prerequisites before the SA/PO.
12. **Template maintenance**
   - The Demand Owner maintains the questionnaire, BRD, DDS and Service Agreement templates and the AI settings; every change is versioned and logged, and the Demand Manager approves it before it goes live.
13. **AI feedback and quality view**
   - Captures every human edit and override of AI output (part of the audit trail) and gives the Demand Manager a periodic view of AI quality.

## 8. Non-Functional Requirements *(targets to be validated)*

| Area | Requirement |
|------|-------------|
| Deployment & hosting | The product and its AI models run on-premise only; no demand data is sent to external AI services. Existing company-approved systems (JIRA Cloud, Microsoft 365: mailbox, Teams, SharePoint / OneDrive) remain in use |
| Access channels | Daily work inside JIRA; a companion web app for the dashboard, AI drafting and consult requests; notifications via email and Teams |
| Authentication & identity | Corporate single sign-on; product roles managed inside the web app |
| Availability & recovery | Available during business hours on working days; JIRA remains the system of record so no demand data is lost if the product is unavailable *(proposal – to be validated)* |
| Scalability | Today about 60 demands per year; must scale with the future demand forecast (forecast TBD) |
| Performance | AI drafts and evidence packs ready within minutes, not hours; automated JIRA updates near-immediate *(proposal – to be validated)* |
| Usability & accessibility | English only (UI and all AI drafts) |
| Maintainability | TBD |
| Observability | TBD |

### 8.1 Security & Privacy Requirements *(to be validated)*

| Area | Requirement |
|------|-------------|
| Data classification & protection | Demand data (BRD, DDS, cost, Service Agreement, PO) treated as confidential; Business Partner contact details treated as personal data; the company's existing classification and data-protection policies apply *(details to be validated with InfoSec / Data Protection)* |
| Access control | All demand roles can see all demands (for reuse and consulting); cost, Service Agreement and PO data visible only to the assigned Demand Owner, the Demand Manager and the Technical Product Owner |
| Encryption & keys | Company encryption standard for data at rest and in transit *(to be validated with InfoSec)* |
| Audit & monitoring | Full trail in the JIRA ticket for every AI output and decision: the AI draft, the human-released version, who released or decided, when, and the evidence shown |
| Malicious content | Incoming BP attachments are scanned for malware; the AI treats BP content strictly as data, never as instructions; nothing is sent to the BP without Demand Owner release |
| Retention & reuse | Company retention policy applies; reuse of past demands as AI evidence to be confirmed with Data Protection / Legal; BP personal data excluded or minimised in AI evidence |
| Separation of duties | Template and AI-setting changes by the Demand Owner are versioned, logged and approved by the Demand Manager before going live |

## 9. Roadmap & Operating Model *(proposal, to be validated)*

### 9.1 Phased Roadmap

| Phase | Scope |
|-------|-------|
| 0 – Proof of concept | Check that the on-premise AI models draft BRD, DDS and minutes well enough before the Phase 1 build |
| 1 – MVP: Intake to alignment | Steps 1–7: mailbox intake, Demand Owner assignment, JIRA registration, questionnaire and reminders, questionnaire summary, initial alignment (brief, minutes, BRD/DDS drafts), LoDA fit and complexity decisions, demand closure / reopening |
| 2 – Requirements to cost acceptance | Steps 8–15: detailed requirement gathering, indicative cost, BRD/DDS completeness check, feasibility and TPO approval evidence packs, baselining, cost estimation package, cost acceptance |
| 3 – SA / PO to handover | Steps 16–20: handover with prerequisites checklist, SAP data preparation, Service Agreement draft, SA / PO detection, development start notification |

Shared capabilities (JIRA record keeping, audit trail, dashboard, consult requests, template maintenance, AI quality view) are built up from Phase 1 onwards *(to be validated)*. AI fit check and cost drafting are switched on only once the evidence threshold is reached, whatever the phase.

Each phase is piloted with 1–2 Demand Owners before it is rolled out to all Demand Owners.

### 9.2 Operating Model

- **Ownership** – TBD
- **Support & service levels** – TBD

### 9.3 Risks & Dependencies *(to be validated)*

| # | Risk / dependency | Mitigation |
|---|-------------------|------------|
| 1 | On-premise AI models may not draft BRD, DDS and minutes well enough | Phase 0 proof of concept before the Phase 1 build |
| 2 | Human release and review of every BP message and AI output limits time saved | Accepted trade-off: human control is more important than time saving |
| 3 | Evidence cold start: with about 60 demands a year and new demands only, AI fit and cost support may take a long time to switch on | Fit check and cost stay manual until the threshold is reached |
| 4 | Dependency on InfoSec, Data Protection and Legal approvals (classification, retention, Teams transcripts, AI-use policy) | TBD |
| 5 | Dependency on IT for on-premise hosting and access to JIRA Cloud, the shared mailbox, Teams and SharePoint / OneDrive | TBD |
| 6 | Adoption: Demand Owners take on extra tasks (templates, SAP entry, release steps) and may not trust AI drafts | Pilot each phase with 1–2 Demand Owners before full rollout |
| 7 | BPs may contact Demand Owners directly and bypass the shared mailbox | See Open Question 12 |

## 10. Success Metrics *(targets to be defined)*

| Metric | Baseline | Target |
|--------|----------|--------|
| Time from demand received to Product Team notified | 1–2 months, largely spent waiting on follow-ups | TBD |
| Manual JIRA updates per demand | TBD | TBD |
| Demand Owner effort per demand | 30–40 hours | TBD |
| Demands handled per year (capacity) | About 60 per year today; future growth expected (forecast TBD) | TBD |
| Share of AI drafts accepted with minor edits | TBD | TBD |

## 11. Non-Goals *(to be validated)*

- The product does not replace the people who make decisions at the five decision points.
- The product does not send anything to the Business Partner without Demand Owner release.
- No integration with SAP; no use of existing JIRA history as AI evidence; no separate LoDA capability catalogue.
- The product does not cover the development work after the Product Team is notified.

## 12. Decisions & Exclusions

| Date | Decision / Exclusion | Reason |
|------|----------------------|--------|
| 2026-11-12 | Scope is the internal LoDA demand process, from "demand received" to "Product Team notified to commence development" | Confirmed by user |
| 2026-11-12 | Three primary roles: Demand Owner (end-to-end owner), Demand Manager, technical roles (Technical Architect, Technical Product Owner / Product Team) | Confirmed by user |
| 2026-11-12 | Each phase is classified as Direct Automation, AI with Suggestion or AI with Evidence | User request |
| 2026-11-12 | Closure: reason recorded, AI-drafted BP notice, reopen possible | Review 1 – user choice |
| 2026-11-12 | AI evidence for fit check and cost comes from past demands only; no separate LoDA capability catalogue | Review 1 – user choice |
| 2026-11-12 | Demand Manager gets a pipeline dashboard; consult requests are handled in the product and logged in JIRA | Review 1 – user choice |
| 2026-11-12 | No new roles: Demand Owner also maintains templates and performs project creation / SAP planning; no separate admin or SAP role | Review 1 – user choice |
| 2026-11-12 | Demand Manager assigns the Demand Owner, based on an AI suggestion | Review 1 – user choice |
| 2026-11-12 | Automatic BP reminders, escalating to the Demand Owner | Review 1 – user choice |
| 2026-11-12 | Handover includes an AI-drafted prerequisites checklist | Review 1 – user choice |
| 2026-11-12 | On-premise only, including AI models; no external AI services | Review 2 – user choice |
| 2026-11-12 | Access via JIRA plus a companion web app | Review 2 – user choice |
| 2026-11-12 | Corporate SSO, with roles managed inside the web app | Review 2 – user choice |
| 2026-11-12 | English only | Review 2 – user choice |
| 2026-11-12 | All demands visible team-wide; cost, SA and PO data restricted to assigned Demand Owner, Demand Manager and TPO | Review 3 – user choice |
| 2026-11-12 | Company data classification, protection and encryption standards apply | Review 3 – user choice |
| 2026-11-12 | Malware scan plus AI guardrails for BP content | Review 3 – user choice |
| 2026-11-12 | Every message to the BP, including the standard questionnaire and reminders, is sent only after Demand Owner release (overrides the earlier fully automatic sending) | Review 3 – user choice, conflict resolved |
| 2026-11-12 | Full audit trail of AI drafts, released versions and decisions in JIRA | Review 3 – user choice |
| 2026-11-12 | Company retention policy; reuse of past demands to be confirmed with Data Protection / Legal | Review 3 – user choice |
| 2026-11-12 | Template / AI-setting changes logged and approved by the Demand Manager | Review 3 – user choice |
| 2026-11-12 | No AI confidence levels shown; every AI output gets the same human review | Review 4 – user choice |
| 2026-11-12 | AI evidence only from demands handled in the new product; existing JIRA history not used | Review 4 – user choice (narrows the Review 1 "past demands only" decision) |
| 2026-11-12 | Fit check and cost drafting manual until an evidence threshold is reached | Review 4 – user choice |
| 2026-11-12 | Capture human edits/overrides and provide an AI quality view to the Demand Manager | Review 4 – user choice |
| 2026-11-12 | AI content labelled internally only; BP-facing documents not marked as AI-assisted | Review 4 – user choice |
| 2026-11-12 | The shared demand mailbox is the only intake channel; no web form, Teams intake or manual intake | Review 5 – user choice |
| 2026-11-12 | JIRA Cloud is used. Hosting rule clarified: product and AI on-premise; JIRA Cloud and Microsoft 365 allowed as existing approved systems; no data sent to external AI services | Review 5 – user choice, conflict resolved |
| 2026-11-12 | Minutes drafted from the Teams transcript where available, otherwise from the Demand Owner's notes | Review 5 – user choice |
| 2026-11-12 | No SAP integration; product prepares the data, Demand Owner enters it in SAP | Review 5 – user choice |
| 2026-11-12 | Signed SA and PO detected from the shared mailbox; Demand Owner confirms | Review 5 – user choice |
| 2026-11-12 | SharePoint / OneDrive holds the master documents; JIRA holds the link and the final baselined copy; notifications via email and Teams | Review 5 – user choice |
| 2026-11-12 | Roadmap in three phases by process stage (not by automation level, not big bang) | Review 6 – user choice |
| 2026-11-12 | Proof of concept of the on-premise AI models before the Phase 1 build | Review 6 – user choice |
| 2026-11-12 | Human release and review effort accepted as a trade-off; no bulk release, no change to the release rules | Review 6 – user choice |
| 2026-11-12 | Pilot each phase with 1–2 Demand Owners | Review 6 – user choice |
| 2026-11-12 | Excluded for now: early InfoSec / Legal sign-off gate, and naming a product owner and business sponsor as mitigations | Review 6 – not selected by user |

## 13. Open Questions

1. Is the automation level proposed per step in section 7.3 correct?
2. Should Business Partners interact with the product directly, or only through the Demand Owner?
3. Who decides "Can LoDA address the demand?" – the Demand Owner alone, or together with others?
4. Who owns, supports and funds the product (operating model)?
5. What is the future demand forecast (demands per year) the product must scale to?
6. Product name.
7. Reminder and escalation timings for BP follow-ups.
8. How many demands handled in the new product are needed before the AI fit check and cost drafts are switched on (evidence threshold)?
9. Does the company AI-use policy allow BP-facing documents to be released without an AI-assisted label?
10. Confirmation from InfoSec / Data Protection / Legal on data classification, encryption, retention, reuse of past demands as AI evidence, and use of Teams transcripts.
11. How do the product's steps map to the existing JIRA workflow statuses?
12. Are BPs who send demands from outside the shared mailbox (e.g. calling or emailing a Demand Owner directly) redirected to the mailbox, or forwarded by the Demand Owner?
