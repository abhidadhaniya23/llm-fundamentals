# LoDA Demand Handling (DC) – Personas

> Status: Draft | Version 0.1 | 2026-11-13. Basis: **Proto-persona – not research-based.** Built from the process flow and a team session, not from interviews with the users. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `dc-sources/Demand_Handling_Consulting_Process_Flow_Refined (2).pdf` (PDF), `dc-sources/dc-context.md` (context; transcript timestamps as T).

## 1. Persona Overview

| ID | Persona (role name) | Type | Stakeholder group | One-line summary |
|----|---------------------|------|-------------------|------------------|
| P-01 | The Demand Owner | Primary | SH-01 | Runs every demand from first email to development start, mostly by hand |
| P-02 | The Demand Manager | Secondary | SH-02 | Oversees all demands and steps in on escalations, without a live view of them |
| P-03 | The Technical Reviewer | Secondary | SH-03, SH-04 | Architect or Technical Product Owner who confirms complexity, feasibility and final approval |

## 2. P-01 – The Demand Owner

### 2.1 Role & Context

Owns each demand from "new demand received" to "Product Team notified" and is the first contact for the Business Partner. Handles about 60 demands a year across the team; each takes 30–40 hours of effort and runs 1–2 months. *(context §2, §3)*

### 2.2 Goals

- Move each demand to a clear decision (closed or handed over) without it stalling *(context §3 – to be validated)*
- Keep the JIRA ticket complete, as the process requires *(PDF)*
- Send the Business Partner correct, complete documents (questionnaire, BRD, DDS, cost estimation, SA) *(PDF)*

### 2.3 Responsibilities & Tasks

- Registers the demand in JIRA and issues the standard questionnaire *(PDF)*
- Runs the initial alignment (scope, LoDA demo) and detailed requirement meetings; circulates minutes *(PDF)*
- Issues and re-issues updated BRD and DDS to the Business Partner *(PDF)*
- Shares the indicative and final cost estimate, final BRD/DDS and DPoB *(PDF)*
- Hands over to the Product Team; raises SAP project creation and issues the Service Agreement *(PDF; T 1:33:25)*
- Chases the Business Partner for responses *(T 1:44:12)*
- Updates the JIRA ticket at every tagged step *(PDF)*

### 2.4 Decisions They Own

- Initial product identification: can LoDA address the demand? May consult product owners to check whether a technical feature is supported. *(PDF; user input 2026-11-13)*

### 2.5 Pain Points & Frustrations

| ID | Pain point | Frequency | Impact | Source |
|----|-----------|-----------|--------|--------|
| PP-01-01 | Updates the JIRA ticket by hand at almost every step before the flow can continue | Every demand, 13 tagged steps | Repeated manual effort | PDF |
| PP-01-02 | Spends 30–40 hours of effort on each demand | Every demand | Limits how many demands the team can handle | T 1:44:12 |
| PP-01-03 | Waits on Business Partner replies; demands run 1–2 months, mostly in follow-ups | Every demand | Slow outcome; manual chasing | T 1:44:12 |
| PP-01-04 | Issues BRD and DDS several times as the discussion moves on | Every demand, 2–3 rounds | Re-work on documents | PDF |
| PP-01-05 | No capability catalog, and past demands are not in a usable place, to judge fit or feasibility | Every new demand | Decisions depend on memory and people | T 1:29:51, 1:30:19 |
| PP-01-06 | Demands arrive through different channels and people, not one entry point | TBD | Demands can be missed or start late | T 1:26:41, 1:53:35 |
| PP-01-07 | Also does SAP project creation, which is not part of the DC process | Every accepted demand | Extra task outside the role | T 1:33:25 |
| PP-01-08 | No defined way to pull in the Demand Manager or Architect during a demand | TBD | Ad-hoc consults | T 1:30:30 |
| PP-01-09 | Nothing is defined after "Demand Closed": no Business Partner notification, no reopen path | Every closed demand | Inconsistent closure; returning demands start from scratch | T 1:24:09 |
| PP-01-10 | The process flow names no owner for each step; who does what lives in people's heads | Every demand | Unclear accountability; hard to onboard others | T 1:24:09, 1:24:15 |

### 2.6 Needs from the Initiative

- Routine steps (registration, JIRA updates, reminders) done without manual effort *(context §6)*
- Drafts of documents and messages to review and release, never sent without them *(context §5 Human approval)*
- One place to see all their demands and what is waiting on whom *(to be validated)*

### 2.7 Behaviours, Tools & Channels

- JIRA demand ticket as the single source of truth *(PDF)*
- Email, shared DC mailbox, Teams, SharePoint / OneDrive *(context §5)*
- Picks up new demands themselves today *(T 1:35:29)*

### 2.8 Quotes from Research

Not applicable.

## 3. P-02 – The Demand Manager

### 3.1 Role & Context

Consulted by the Demand Owner on business and stakeholder questions; confirms complex requirements together with the Technical Architect; the escalation point. Today reviews all demands in a weekly cadence call. *(context §2; PDF)*

### 3.2 Goals

- Know the status and health of every demand without waiting for the weekly call *(T 1:31:26 – to be validated)*
- Step in early when a demand is stuck or the Business Partner does not respond *(T 1:37:21)*

### 3.3 Responsibilities & Tasks

- Runs the weekly review of all demands *(T 1:31:26)*
- Confirms complex requirements with the Architect *(PDF)*
- Often receives new demands by email and forwards them to the DC mailbox *(T 1:26:41)*

### 3.4 Decisions They Own

- Complex requirement confirmed? (with the Technical Architect) *(PDF)*

### 3.5 Pain Points & Frustrations

| ID | Pain point | Frequency | Impact | Source |
|----|-----------|-----------|--------|--------|
| PP-02-01 | No live status view of all demands; relies on a weekly call | Weekly | Late visibility of stuck demands | T 1:31:26 |
| PP-02-02 | No rule for who owns a new demand; owners self-pick | Every new demand | Unclear accountability | T 1:35:29 |
| PP-02-03 | Does not see when a Business Partner has not replied for weeks | TBD | Escalation comes late | T 1:37:21 |
| PP-02-04 | Receives demands personally and must forward them | TBD | Extra step; demands can be missed | T 1:26:41 |

### 3.6 Needs from the Initiative

- A dashboard of all demands, plus consult requests from Demand Owners *(T 1:31:19, 1:32:06)*
- Alerts when a demand waits too long on the Business Partner *(T 1:37:21)*
- A suggested Demand Owner for each new demand *(T 1:36:08)*

### 3.7 Behaviours, Tools & Channels

- Weekly cadence call; email; JIRA *(T 1:31:26; PDF)*

### 3.8 Quotes from Research

Not applicable.

## 4. P-03 – The Technical Reviewer

### 4.1 Role & Context

The Technical Architect (complexity check) and the Technical Product Owner / Product Team (feasibility, final approval, receiving the handover). Consulted by the Demand Owner on technical questions. *(PDF; context §2)*

### 4.2 Goals

- Decide on complexity, feasibility and approval with the facts in front of them *(T 1:18:43, 2:08:12 – to be validated)*
- Receive a baselined BRD/DDS and a clear handover *(PDF)*

### 4.3 Responsibilities & Tasks

- Product owners: when the Demand Owner asks, check whether a technical feature is supported, as input to the LoDA fit decision *(user input 2026-11-13)*
- Confirms whether a requirement is complex *(PDF)*
- Assesses and finalises technical feasibility *(PDF)*
- Gives the final technical approval *(PDF)*
- Takes over the demand and may start prerequisites early *(PDF)*

### 4.4 Decisions They Own

- Complex requirement confirmed? (Architect, with the Demand Manager) *(PDF)*
- Final approval obtained from the Technical Product Owner? *(PDF)*

### 4.5 Pain Points & Frustrations

| ID | Pain point | Frequency | Impact | Source |
|----|-----------|-----------|--------|--------|
| PP-03-01 | Pulled in ad hoc; no defined consult route in the flow | TBD | Interruptions; late involvement | T 1:30:30 |
| PP-03-02 | Feasibility is judged without evidence from similar past demands | Every demand reaching feasibility | Slower, less consistent decisions | T 1:29:51, 2:08:12 *(to be validated)* |

### 4.6 Needs from the Initiative

- An evidence pack (similar past demands, gaps in the BRD/DDS) for each decision *(context §6)*
- Consult requests that arrive with context *(T 1:32:06 – to be validated)*

### 4.7 Behaviours, Tools & Channels

- JIRA; meetings with the Demand Owner *(PDF – to be validated)*

### 4.8 Quotes from Research

Not applicable.

## 5. Open Questions

1. Interview at least one Demand Owner to turn these proto-personas into research-based personas. *(recommended)*
2. How many Demand Owners are there today? *(unknown)*
