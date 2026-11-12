# LoDA Demand Assistant – To-Be Journey

> Status: Draft | Version 0.1 | 2026-11-13. Steps confirmed by the user on 2026-11-13. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `as-is-journey.md`, `product-vision.md`, `personas.md`, `problem-statement.md`, `dc-sources/dc-context.md` (transcript timestamps as T).

## 1. Scenario & Design Principles

- **Scenario:** Same as the as-is journey. It starts when a Business Partner raises a new demand. It ends with "Product Team notified to commence development", or "Demand Closed" at any decision point.
- **Personas:** P-01 The Demand Owner (mapped end to end). P-02 The Demand Manager and P-03 The Technical Reviewer appear in their steps and handoffs.
- **Design principles:**
  1. People keep every decision. The product prepares, people decide. *(context §5 Human approval)*
  2. Nothing reaches the Business Partner without Demand Owner release. *(T 2:08:24)*
  3. One intake door: the shared DC mailbox. *(T 1:53:31)*
  4. Every step runs at its own automation level: A, B, C or A+B (see legend). *(context §6)*
  5. JIRA stays the single source of truth and is updated automatically. *(PDF)*
  6. When the AI is unsure, the step falls back to manual. LoDA fit and cost stay manual until the evidence threshold is reached. *(T 1:50:27, 1:51:19)*
  7. The Business Partner's experience does not show AI involvement. *(T 1:51:54)*

**Automation level legend:**
- A = direct automation
- B = AI with suggestion
- C = AI with evidence
- A+B = prepared automatically, released by a person
- \* = manual until the evidence threshold is reached

## 2. Journey – P-01 The Demand Owner

### 2.1 Steps

| Step ID | Stage | What the persona does | Touchpoint / channel | Change type | Level | Replaces | Resolves | Goals | Capability | Expected experience |
|---------|-------|----------------------|----------------------|-------------|-------|----------|----------|-------|------------|---------------------|
| T-01 | 1. Intake | Sees each new demand arrive in the shared DC mailbox. Anyone who gets a demand another way forwards it there | DC mailbox | Changed | A | A-01 | PP-01-06, PP-02-04 | G-03 | C-01 | No demand is missed; one place to look *(to be validated)* |
| T-02 | 1. Intake | Finds the demand already registered in JIRA, with the key facts filled in | JIRA | Automated | A | A-03 | PP-01-01 | G-02 | C-01, C-04 | No manual registration |
| T-03 | 1. Intake | Is assigned as owner: the product suggests an owner, and the Demand Manager confirms | JIRA, dashboard | Changed | B | A-02 | PP-02-02, PP-01-10 | G-03 | C-01 | Clear ownership from day one |
| T-04 | 2. Questionnaire | Releases the prepared standard questionnaire to the Business Partner | Email (via the product) | Changed | A+B | A-04 | PP-01-01 | G-02 | C-03, C-04 | One click instead of writing and recording |
| T-05 | 2. Questionnaire | ⏳ Releases prepared reminders while waiting. Long waits escalate to them and the Demand Manager. The reply is attached to JIRA when it arrives | Email, dashboard | Changed | A+B | A-05 | PP-01-03, PP-02-03, PP-01-01 | G-01, G-03 | C-02, C-04 | No manual chasing; stalled demands are seen |
| T-06 | 2. Questionnaire | Reviews an AI summary of the completed questionnaire, with the missing answers flagged | JIRA | New | C | – | PP-01-04 | G-01, G-02 | C-03 | Gaps known before the alignment meeting |
| T-07 | 3. Alignment | Runs the alignment meeting (scope, LoDA demo) with a prepared brief. Reviews and releases the drafted minutes and BRD/DDS updates | Meeting, email | Changed | B | A-06 | PP-01-04, PP-01-01 | G-01, G-02 | C-03 | Less document re-work |
| T-08 | 3. Alignment | ◇ Decides whether LoDA can address the demand. Can send a consult request to product owners on technical feature support. Sees similar past demands once the threshold is reached | Dashboard, JIRA | Changed | C* | A-07 | PP-01-05, PP-01-08 | G-04 | C-05, C-06 | Decision backed by facts; a defined route to ask |
| T-09 | 3. Alignment | ◇ For complex demands: the Architect and the Demand Manager confirm, through a consult request that comes with an evidence pack | Dashboard, JIRA | Changed | C | A-08 | PP-01-08, PP-03-01 | G-04 | C-05, C-06 | Reviewers get the context up front |
| T-10 | 4. Requirements | Runs detailed requirement meetings. Reviews and releases the drafted minutes and BRD/DDS updates | Meeting, email | Changed | B | A-09 | PP-01-04, PP-01-01 | G-01, G-02 | C-03 | Less document re-work |
| T-11 | 4. Requirements | (Optional, on request) Releases an indicative cost estimate. Drafted from past demands once the threshold is reached | Email | Changed | B* | A-10 | PP-01-05 | G-04 | C-05 | Estimates grounded in past demands (later) |
| T-12 | 4. Requirements | ⏳ Releases prepared reminders for the BRD/DDS. When they arrive, reviews a completeness check (e.g. "4 of 9 fields empty – send follow-up?") | Email, JIRA | Changed | C | A-11 | PP-01-03, PP-02-03, PP-01-04 | G-01 | C-02, C-03 | Fewer rounds; follow-up ready to send |
| T-13 | 5. Tech approval | Gets technical feasibility assessed with the Product Team, using a feasibility evidence pack | Meeting, JIRA | Changed | C | A-12 | PP-03-02, PP-03-01 | G-04 | C-05 | Faster, more consistent assessment |
| T-14 | 5. Tech approval | ◇ Gets the Technical Product Owner's final approval, with an evidence and risk summary | JIRA | Changed | C | A-13 | PP-03-02 | G-04 | C-05 | Traceable approval |
| T-15 | 5. Tech approval | Sees the BRD/DDS baselined and frozen, recorded in JIRA automatically | JIRA | Automated | A | A-14 | PP-01-01 | G-02 | C-04 | No manual baseline record |
| T-16 | 6. Cost | Releases the cost package (cost estimation, final BRD/DDS, DPoB), assembled by the product. The cost figure is manual until the threshold is reached | Email | Changed | B* | A-15 | PP-01-01 | G-02 | C-03 | Package ready to send |
| T-17 | 6. Cost | ⏳◇ Releases prepared reminders while the Business Partner decides. The answer is recorded and routes the flow | Email, JIRA | Changed | A+B | A-16 | PP-01-03, PP-02-03 | G-01 | C-02, C-04 | No manual chasing |
| T-18 | 7. Handover | Hands over to the Product Team with a prepared handover package | JIRA, email | Changed | A+B | A-17 | PP-01-01 | G-02 | C-03, C-04 | Complete handover without assembling it |
| T-19 | 7. Handover | Enters the prepared project / SAP planning data in SAP | SAP | Changed | B | A-18 | PP-01-07 | G-02 | C-03 | Less effort on a task outside the role |
| T-20 | 7. Handover | Releases the drafted Service Agreement | Email | Changed | B | A-19 | PP-01-01 | G-02 | C-03 | Less drafting |
| T-21 | 7. Handover | ⏳◇ Confirms the signed SA and PO, detected in the DC mailbox. Releases prepared reminders while waiting | DC mailbox, JIRA | Changed | A+B | A-20 | PP-01-03, PP-02-03 | G-01 | C-02 | No manual chasing or attaching |
| T-22 | 7. Handover | Sees the Product Team notified and the demand closed as complete in JIRA | JIRA, email | Automated | A | A-21 | PP-01-01 | G-02 | C-04 | Clean finish without manual steps |
| T-23 | Any closed exit | Records the closure reason and releases a drafted closure note to the Business Partner. Can reopen the demand later | JIRA, email | New | A+B | (closed exits of A-07, A-08, A-13, A-16, A-20) | PP-01-09 | G-01, G-03 | C-07 | Every closure is clean and reversible |
| T-24 | Cross-cutting (P-02) | The Demand Manager sees all demands, owners, status and waits on a dashboard at any time | Dashboard | New | A | – (weekly call) | PP-02-01 | G-03 | C-06 | Status without waiting for the weekly call |

### 2.2 Removed As-Is Steps

| As-is step | Why it is no longer needed |
|------------|----------------------------|
| None | Every as-is step is kept, changed or automated. |

### 2.3 Decision Points

| Step ID | Decision | Owner | Possible outcomes |
|---------|----------|-------|-------------------|
| T-03 | Who owns the demand? | Demand Manager (confirms the suggestion) | Suggested owner confirmed / other owner chosen |
| T-08 | Can LoDA address the demand? | Demand Owner (may consult product owners) | Yes – straightforward → T-10; Yes – complex → T-09; No → T-23 |
| T-09 | Complex requirement confirmed? | Technical Architect + Demand Manager | Yes → T-10; No → T-23 |
| T-14 | Final technical approval? | Technical Product Owner | Yes → T-15; No → T-23 |
| T-17 | Cost estimate accepted? | Business Partner | Yes → T-18; No → T-23 |
| T-21 | SA signed and PO received? | Business Partner (receipt confirmed by the Demand Owner) | Yes → T-22; No → T-23 |
| T-23 | Reopen a closed demand? | Demand Owner | Reopened (back to its last step) / stays closed |

## 3. Handoffs Between Personas

| From (persona, step) | To (persona, step) | What is handed over | How it improves on today |
|----------------------|--------------------|---------------------|--------------------------|
| Product, T-03 | P-02, T-03 | Owner suggestion | Defined assignment, not self-pick |
| Product, T-05 / T-12 / T-17 / T-21 | P-01 + P-02 | Escalation of a long wait | Stalled demands become visible |
| P-01, T-08 | P-03 (product owners) | Consult request on feature support | Defined route, logged in JIRA |
| P-01, T-09 | P-03 (Architect) + P-02 | Consult request with an evidence pack | Context up front instead of ad hoc |
| P-01, T-13 | P-03 (Product Team) | BRD/DDS + feasibility evidence pack | Evidence from past demands |
| P-03 (TPO), T-14 | P-01, T-15 | Approval decision | Recorded with its evidence |
| P-01, T-18 | P-03 (Product Team) | Handover package | Complete and consistent |
| Product, all steps | P-02, T-24 | Live demand status | Replaces the weekly-only view |

## 4. Unresolved Pain Points

| Pain point | Reason not resolved |
|------------|---------------------|
| PP-01-07 (partly) | SAP integration is out of scope. The data is prepared, but the Demand Owner still enters it. |
| PP-01-05 (partly, at first) | Past-demand evidence is only switched on after the threshold. Until then, LoDA fit and cost are manual. |

## 5. Open Questions

1. What wait duration triggers an escalation? *(TBD at epic level – T 1:38:26)*
2. Reopening: does a reopened demand go back to its last step, or to the start? *(assumed: last step – to be validated)*
3. Technical: dashboard hosting, mailbox and JIRA connection, on-premise AI. These are left to architecture. *(context §5)*
4. Evidence threshold value. *(unknown)*
