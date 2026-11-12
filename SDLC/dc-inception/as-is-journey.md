# LoDA Demand Handling (DC) – As-Is Journey

> Status: Draft | Version 0.1 | 2026-11-13. Steps confirmed by the user on 2026-11-13. *(to be validated)* = assumption, not yet confirmed.

## 1. Scenario

- **Start trigger:** A Business Partner raises a new demand through any channel.
- **End point:** "Product Team notified to commence development". There are 5 early exits to "Demand Closed": A-07, A-08, A-13, A-16 and A-20.
- **Personas mapped:** P-01 The Demand Owner, end to end. P-02 The Demand Manager and P-03 The Technical Reviewer appear as others involved and in the handoffs.
- **Sources:** `dc-sources/Demand_Handling_Consulting_Process_Flow_Refined (2).pdf` (PDF), `dc-sources/dc-context.md` (context; transcript timestamps as T), `personas.md`, user input.

**Whole-journey facts:** 30–40 hours of Demand Owner effort per demand, and 1–2 months elapsed, mostly in follow-ups (PP-01-02, T 1:44:12). Every step with a JIRA tag needs a manual ticket update before the flow can go on (PP-01-01, PDF). The Demand Manager sees status only in the weekly call (PP-02-01).

## 2. Journey – P-01 The Demand Owner

### 2.1 Stages

| Stage | Steps | Goal of the persona in this stage |
|-------|-------|-----------------------------------|
| 1. Intake | A-01 – A-03 | Get the demand into the process with an owner |
| 2. Questionnaire | A-04 – A-05 | Get the Business Partner's basic information |
| 3. Initial alignment | A-06 – A-08 | Understand the demand and decide whether LoDA takes it on |
| 4. Detailed requirements | A-09 – A-11 | Get a complete BRD and DDS |
| 5. Technical approval | A-12 – A-14 | Get technical sign-off and freeze the requirements |
| 6. Cost acceptance | A-15 – A-16 | Get the Business Partner to accept the cost |
| 7. Handover & contract | A-17 – A-21 | Get the contract in place and development started |

### 2.2 Steps

| Step ID | Stage | What the persona does | Touchpoint / channel | Others involved | Tools | Time / effort | Feeling | Pain points | Opportunities |
|---------|-------|----------------------|----------------------|-----------------|-------|---------------|---------|-------------|---------------|
| A-01 | 1 | Receives the new demand. It often reaches the Demand Manager by email first and is forwarded to the DC mailbox | Email, Teams, DC mailbox | Business Partner, Demand Manager | Mailbox | TBD | TBD | PP-01-06: several entry points; PP-02-04: Demand Manager forwards demands by hand | One intake channel |
| A-02 | 1 | Picks the demand up themselves | Mailbox | Other Demand Owners | – | TBD | TBD | PP-02-02: no assignment rule; PP-01-10: ownership is not defined | Suggested owner |
| A-03 | 1 | Registers the demand as a JIRA entry | JIRA | – | JIRA | TBD | TBD | PP-01-01: manual JIRA entry (repeats at every JIRA-tagged step) | Automatic registration |
| A-04 | 2 | Issues the standard questionnaire to the Business Partner; updates JIRA | Email | Business Partner | Questionnaire template, JIRA | TBD | TBD | PP-01-01 | Questionnaire prepared for release |
| A-05 | 2 | ⏳ Waits for the completed questionnaire; chases by hand; updates JIRA when it arrives | Email | Business Partner | Mailbox, JIRA | TBD | TBD | PP-01-03: chasing; PP-02-03: nobody sees a long wait | Reminders; visible wait status |
| A-06 | 3 | Runs the initial alignment: clarifies scope and intent, demos the LoDA product, issues updated BRD and DDS; updates JIRA | Meeting, email | Business Partner | BRD/DDS templates, JIRA | TBD | TBD | PP-01-04: BRD/DDS issued again; PP-01-01 | Drafted minutes and BRD/DDS updates |
| A-07 | 3 | ◇ Decides whether LoDA can address the demand; may ask product owners whether a technical feature is supported | Meeting, chat | Product owners (P-03) | – | TBD | TBD | PP-01-05: no catalog or usable past demands; PP-01-08: consults are ad hoc | Similar past demands as evidence |
| A-08 | 3 | ◇ For complex demands: gets the complexity confirmed with the Architect and the Demand Manager | Meeting | Technical Architect (P-03), Demand Manager (P-02) | – | TBD | TBD | PP-01-08, PP-03-01: pulled in ad hoc | Consult request with context |
| A-09 | 4 | Holds detailed requirement meetings, circulates minutes, issues updated BRD and DDS for the Business Partner to complete; updates JIRA | Meeting, email | Business Partner | BRD/DDS templates, JIRA | TBD | TBD | PP-01-04; PP-01-01 | Drafted minutes; BRD/DDS gap check |
| A-10 | 4 | (Optional, on request) Shares an indicative cost estimate; updates JIRA | Email | Business Partner | JIRA | TBD | TBD | PP-01-05: no reference estimates | Reference to past estimates |
| A-11 | 4 | ⏳ Waits for the completed BRD and DDS; chases by hand; updates JIRA | Email | Business Partner | Mailbox, JIRA | TBD | TBD | PP-01-03; PP-02-03 | Reminders; completeness check |
| A-12 | 5 | Gets technical feasibility assessed and finalised with the Product Team; updates JIRA | Meeting | Product Team (P-03) | JIRA | TBD | TBD | PP-03-02: no evidence from past demands; PP-03-01 | Feasibility evidence pack |
| A-13 | 5 | ◇ Gets the final approval from the Technical Product Owner | Meeting, JIRA | Technical Product Owner (P-03) | JIRA | TBD | TBD | PP-03-02 | Summary of evidence and risks |
| A-14 | 5 | Baselines and freezes the BRD and DDS; updates JIRA | JIRA | – | JIRA, document storage | TBD | TBD | PP-01-01 | Automatic baseline record |
| A-15 | 6 | Shares the cost estimation, final BRD, final DDS and DPoB (where required); updates JIRA | Email | Business Partner | JIRA | TBD | TBD | PP-01-01 | Package assembled for release |
| A-16 | 6 | ⏳◇ Waits for the Business Partner to accept the cost | Email | Business Partner | Mailbox | TBD | TBD | PP-01-03; PP-02-03 | Reminders; visible wait status |
| A-17 | 7 | Hands the demand over to the Product Team (it may start prerequisites); updates JIRA | Meeting, JIRA | Product Team (P-03) | JIRA | TBD | TBD | PP-01-01 | Handover package |
| A-18 | 7 | Starts the SA process: raises project creation and SAP planning; updates JIRA | SAP | – | SAP, JIRA | TBD | TBD | PP-01-07: task outside the DC role | SAP data prepared |
| A-19 | 7 | Issues the Service Agreement to the Business Partner for signature; updates JIRA | Email | Business Partner | SA template, JIRA | TBD | TBD | PP-01-01 | SA drafted for release |
| A-20 | 7 | ⏳◇ Waits for the signed SA and the Purchase Order; confirms receipt from the mailbox | Email, DC mailbox | Business Partner | Mailbox | TBD | TBD | PP-01-03; PP-02-03 | Detect SA/PO in the mailbox |
| A-21 | 7 | Notifies the Product Team to start development; demand completed; updates JIRA | Email, JIRA | Product Team (P-03) | JIRA | TBD | TBD | PP-01-01 | Automatic notification and closure |

**Feeling** is TBD for every step: there are no user interviews yet.

### 2.3 Decision Points & Waiting Times

| Step ID | Decision or wait | Who decides / who is waited on | Possible outcomes | Typical duration |
|---------|-------------------|--------------------------------|-------------------|------------------|
| A-05 | Wait: completed questionnaire | Business Partner | Received / still waiting | TBD |
| A-07 | Can LoDA address the demand? | Demand Owner (may consult product owners) | Yes – straightforward → A-09; Yes – complex → A-08; No – outside LoDA scope → **Demand Closed** | TBD |
| A-08 | Complex requirement confirmed? | Technical Architect + Demand Manager | Yes – accepted → A-09; No – not accepted → **Demand Closed** | TBD |
| A-11 | Wait: completed BRD and DDS | Business Partner | Received / still waiting | TBD |
| A-13 | Final approval from the Technical Product Owner? | Technical Product Owner | Yes → A-14; No → **Demand Closed** | TBD |
| A-16 | Cost estimate accepted? (wait + decision) | Business Partner | Yes → A-17; No → **Demand Closed** | TBD |
| A-20 | SA signed and PO received? (wait + decision) | Business Partner | Yes → A-21; No → **Demand Closed** | TBD |

At every "Demand Closed" exit, no next step is defined today: no Business Partner notification and no reopen path (PP-01-09).

## 3. Handoffs Between Personas

| From (persona, step) | To (persona, step) | What is handed over | Known issues |
|----------------------|--------------------|---------------------|--------------|
| P-02, A-01 | P-01, A-01 | Forwarded demand email | Manual forward; demand may be missed (PP-02-04) |
| P-01, A-07 | P-03 (product owners), A-07 | Feature support question | No defined consult route (PP-01-08) |
| P-01, A-08 | P-03 (Architect) + P-02, A-08 | Complexity question | Pulled in ad hoc (PP-03-01) |
| P-01, A-12 | P-03 (Product Team), A-12 | BRD/DDS for feasibility | No evidence from past demands (PP-03-02) |
| P-03 (TPO), A-13 | P-01, A-14 | Approval decision | None known |
| P-01, A-17 | P-03 (Product Team), A-17 | Handed-over demand | None known |
| P-01, A-21 | P-03 (Product Team), A-21 | Start-development notification | None known |
| P-01, all steps | P-02 (weekly call) | Demand status | Visible only weekly (PP-02-01) |

## 4. Open Questions

1. How long are the typical waits at A-05, A-11, A-16 and A-20? *(unknown – needed as a baseline)*
2. Does a closed demand today get any note to the Business Partner? *(assumed: no defined step – to be validated)*
3. Variant: demands that skip the questionnaire, or where the Business Partner calls a Demand Owner directly. *(not mapped – to be validated)*
4. How often is A-10 (indicative cost) requested? *(unknown)*
