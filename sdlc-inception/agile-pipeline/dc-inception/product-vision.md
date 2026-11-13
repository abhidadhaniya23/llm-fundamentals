# LoDA Demand Assistant – Product Vision

> Status: Draft | Version 0.1 | 2026-11-13. Time horizon: TBD. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `problem-statement.md`, `personas.md`, `stakeholder-map.md`, `as-is-journey.md`, `dc-sources/dc-context.md`.

## 1. Vision Statement

Help every Demand Owner turn a Business Partner's demand into a clear decision faster. Routine work is done for them, and evidence is ready at each decision point.

## 2. Elevator Pitch

For LoDA Demand Owners who spend 30–40 hours per demand tracking, chasing and recording, the LoDA Demand Assistant is an internal demand-handling assistant. It runs the routine steps and follow-ups and brings evidence to each decision. Unlike today's manual JIRA-and-email process, it keeps every demand moving and visible, while people keep every decision.

## 3. Product Vision Board

| Target group | Needs | Product | Business goals |
|--------------|-------|---------|----------------|
| P-01 The Demand Owner (primary); P-02 The Demand Manager; P-03 The Technical Reviewer | Keep demands moving while waiting on the Business Partner (theme 1); stop re-typing records and re-working documents (theme 2); see who owns what and where each demand stands (themes 3, 5); have facts from similar demands at each decision (theme 4) | An internal assistant for the LoDA demand team. It carries each demand from intake to handover, prepares the routine work for people to release, and keeps the record complete. People make every decision | Handle a growing number of demands with the same team; faster answers to Business Partners; consistent, traceable decisions |

## 4. Product Goals & Success Metrics

| ID | Goal (outcome) | Pain point theme | Metric | Baseline | Target |
|----|----------------|------------------|--------|----------|--------|
| G-01 | Demands reach a clear decision faster | 1 – Waiting on and chasing the Business Partner | Elapsed time from demand received to "Product Team notified" or "Demand Closed" | 1–2 months | TBD |
| G-02 | Demand Owners spend less effort per demand | 2 – Manual record keeping and document re-work; 6 – Tasks outside the DC role | Demand Owner hours per demand | 30–40 hours | TBD |
| G-03 | Every demand is owned and its status visible at any time | 3 – No ownership or visibility; 5 – Scattered intake | Share of demands with a named owner and a current status, visible without the weekly call | Weekly call; owners self-pick | TBD |
| G-04 | Decisions are backed by evidence | 4 – Decisions without evidence or a consult route | Share of decisions (A-07, A-08, A-12, A-13) with evidence recorded in JIRA | TBD | TBD |

## 5. Scope

### 5.1 In Scope

| ID | Capability area (what users will be able to do) | Goals served |
|----|------------------------------------------------|--------------|
| C-01 | Demand Owners receive every new demand through one intake, already registered and with a suggested owner | G-01, G-03 |
| C-02 | Demand Owners keep Business Partner follow-ups going with prepared reminders they release, and long waits are escalated to them and the Demand Manager | G-01, G-03 |
| C-03 | Demand Owners get drafts to review and release: questionnaire, minutes, BRD/DDS updates, cost package, Service Agreement, SAP planning data | G-01, G-02 |
| C-04 | Demand Owners keep the JIRA record complete without re-typing it | G-02 |
| C-05 | Demand Owners and technical reviewers see evidence from similar past demands at each decision | G-04 |
| C-06 | The Demand Manager sees all demands, their owner, status and waits in one view, and Demand Owners can send consult requests from there | G-03, G-04 |
| C-07 | Demand Owners close a demand with a reason, notify the Business Partner, and can reopen it | G-01, G-03 |

### 5.2 Out of Scope

- Business Partners do not use the product. Nothing goes to them without Demand Owner release.
- The product does not replace people at any decision point.
- No SAP integration. The product prepares the data, and the Demand Owner enters it.
- No building of a LoDA capability catalog.
- No work after "Product Team notified to commence development".
- No AI labelling towards the Business Partner. AI content is labelled internally only.

## 6. Open Questions

1. What time horizon should this vision cover? *(unknown)*
2. What are the targets for G-01 – G-04? *(TBD – set with the Demand Manager)*
3. Moved from the input (architecture / NFR / roadmap, decided later in the spine):
   - on-premise hosting, with cloud still open with IT
   - JIRA Cloud as the system of record
   - SharePoint / OneDrive for documents
   - no login in the MVP; roles and SSO come later
   - minutes drafted from the Teams transcript or the Demand Owner's notes
   - phasing by process stage, with a pilot on one demand
4. Evidence threshold: how many new demands before the AI fit and cost support is switched on? *(unknown)*
