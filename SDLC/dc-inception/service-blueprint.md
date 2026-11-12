# LoDA Demand Assistant – Service Blueprint

> Status: Draft | Version 0.1 | 2026-11-13. *(to be validated)* = assumption, not yet confirmed.
>
> Source: `to-be-journey.md` (T-IDs, levels), `dc-sources/dc-context.md`.

## 1. How to Read This Blueprint

- **Persona action** – what the persona does (from the to-be journey).
- **Frontstage** – what the persona sees or interacts with.
- ─ ─ ─ *line of visibility* ─ ─ ─
- **Backstage** – actions by people or the product that the persona does not see.
- **Support systems & data** – systems and information the step relies on, in business terms.
- **Evidence** – documents or records the step produces.

## 2. Stage: Intake

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-01 | Sees the new demand | New demand in the DC mailbox and on the dashboard | Anyone who got it elsewhere forwards it; product detects the new demand | Shared DC mailbox | Product | None | Demand email |
| T-02 | Checks the registered demand | JIRA ticket with key facts | Product creates the ticket and extracts the facts from the email | Ticketing system (JIRA), DC mailbox | None | None | JIRA demand ticket |
| T-03 | Gets assigned | Owner suggestion on the dashboard (Demand Manager); assignment notice (Demand Owner) | Product suggests an owner; Demand Manager confirms | JIRA, dashboard, list of Demand Owners | Demand Manager | Owner – Demand Manager | Assignment in JIRA |

## 3. Stage: Questionnaire

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-04 | Releases the questionnaire | Prepared questionnaire email, ready to release | Product fills the template and sends it on release | Questionnaire template, DC mailbox, JIRA | Business Partner | Release – Demand Owner | Sent questionnaire, JIRA comment |
| T-05 | Releases reminders; handles escalations | Reminder ready to release; escalation alert | Product tracks the wait, prepares reminders, escalates long waits, detects the reply and attaches it | DC mailbox, JIRA, dashboard | Demand Manager (on escalation) | Release – Demand Owner | Reminder log, attached questionnaire |
| T-06 | Reviews the summary | Summary with flagged missing answers | Product compares the answers to the template and lists the gaps | Questionnaire, JIRA | None | None | Summary in JIRA |

## 4. Stage: Initial Alignment

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-07 | Runs the meeting; releases minutes and BRD/DDS | Meeting brief; drafted minutes and BRD/DDS updates | Product drafts from the Teams transcript or the Demand Owner's notes | Meeting transcripts / notes, BRD/DDS templates, document storage (SharePoint / OneDrive) | Business Partner | Release – Demand Owner | Minutes, BRD/DDS versions |
| T-08 | Decides LoDA fit; may ask product owners | Consult request form; similar past demands (after the threshold) | Product finds similar past demands; routes and logs the consult request | Past demands (new ones only), JIRA | Product owners | LoDA fit – Demand Owner | Decision + evidence in JIRA |
| T-09 | Requests confirmation of complexity | Consult request with an evidence pack | Product assembles the pack; Architect and Demand Manager review it | JIRA, past demands | Architect, Demand Manager | Complexity – Architect + Demand Manager | Decision in JIRA |

## 5. Stage: Detailed Requirements

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-10 | Runs the meetings; releases drafts | Drafted minutes and BRD/DDS updates | Product drafts from the transcript or notes | Transcripts / notes, document storage | Business Partner | Release – Demand Owner | Minutes, BRD/DDS versions |
| T-11 | Releases an indicative cost (optional) | Draft estimate (after the threshold), otherwise a blank template | Product drafts from similar past estimates once the threshold is reached | Past estimates | Business Partner | Release – Demand Owner | Indicative estimate in JIRA |
| T-12 | Releases reminders; reviews the completeness check | Gap list ("4 of 9 fields empty") with a follow-up ready | Product tracks the wait, checks the BRD/DDS fields, drafts the follow-up | DC mailbox, BRD/DDS, JIRA | Business Partner | Release – Demand Owner | Completeness check, follow-up log |

## 6. Stage: Technical Approval

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-13 | Gets feasibility assessed | Feasibility evidence pack | Product assembles the pack; Product Team assesses | BRD/DDS, past demands, JIRA | Product Team | Feasibility – Product Team | Assessment in JIRA |
| T-14 | Gets the final approval | Evidence and risk summary | Technical Product Owner decides | JIRA | Technical Product Owner | Final approval – TPO | Approval in JIRA |
| T-15 | Sees the baseline | Baselined BRD/DDS | Product locks the versions and records the baseline | Document storage, JIRA | None | None | Baselined BRD/DDS |

## 7. Stage: Cost Acceptance

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-16 | Releases the cost package | Assembled package; cost entered by hand (until the threshold) | Product assembles the final BRD/DDS, DPoB and cost template | Document storage, JIRA | Business Partner | Release – Demand Owner | Sent package |
| T-17 | Releases reminders; records the answer | Reminder; answer recorded | Product tracks the wait, detects the reply, routes the flow | DC mailbox, JIRA | None | Acceptance – Business Partner | Answer in JIRA |

## 8. Stage: Handover & Contract

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-18 | Hands over | Prepared handover package | Product assembles it and notifies on release | JIRA, document storage | Product Team | Release – Demand Owner | Handover record |
| T-19 | Enters the SAP data | Prepared SAP planning data | Product prepares the data from the demand | JIRA, SAP (manual entry) | None | None | SAP entry recorded in JIRA |
| T-20 | Releases the SA | Drafted Service Agreement | Product drafts from the agreed deliverables | SA template, document storage | Business Partner | Release – Demand Owner | Sent SA |
| T-21 | Confirms SA and PO | Detected SA/PO, waiting for confirmation | Product detects them in the mailbox, attaches them, prepares reminders | DC mailbox, JIRA | None | SA/PO – Business Partner; receipt – Demand Owner | Signed SA, PO in JIRA |
| T-22 | Sees the completion | Completion notice | Product notifies the Product Team and closes the ticket | JIRA, email | Product Team | None | Closed ticket |

## 9. Cross-Cutting

| Step ID | Persona action | Frontstage | Backstage (who / what) | Support systems & data | Handoff to | Decision & owner | Evidence |
|---------|----------------|-----------|------------------------|------------------------|-----------|------------------|----------|
| T-23 | Closes or reopens a demand | Reason form; drafted closure note | Product records the reason, drafts the note, keeps the demand reopenable | JIRA, DC mailbox | Business Partner | Reopen – Demand Owner | Closure reason, note, reopen log |
| T-24 | (Demand Manager) Views all demands | Dashboard: owner, status, waits, escalations | Product keeps the status current from JIRA | JIRA, dashboard | None | None | – |

## 10. Systems Overview

| System (business term) | Used in steps | Role in the service |
|------------------------|---------------|---------------------|
| Shared DC mailbox | T-01, T-04, T-05, T-12, T-17, T-21, T-23 | Single intake; outgoing messages; Business Partner replies, SA and PO |
| Ticketing system (JIRA Cloud) | All | Single source of truth for every demand, decision and document link |
| LoDA dashboard | T-01, T-03, T-05, T-08, T-09, T-24 | Demand overview, owner confirmation, consult requests, escalations |
| Document storage (SharePoint / OneDrive) | T-07, T-10, T-15, T-16, T-18, T-20 | Master copies of all document versions |
| Meeting transcripts / Demand Owner notes | T-07, T-10 | Input for drafted minutes |
| Past demands (new demands only) | T-08, T-09, T-11, T-13 | Evidence, once the threshold is reached |
| SAP | T-19 | Project creation; manual entry |

## 11. Open Questions

1. No login in the MVP. How does the dashboard know which Demand Owner is looking? *(assumed: not needed for the MVP – to be validated)*
2. Where are the document templates kept and who maintains them? *(unknown)*
