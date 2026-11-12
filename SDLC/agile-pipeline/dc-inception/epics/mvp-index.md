# LoDA Demand Assistant – Epics for MVP

> Status: Draft | Version 0.1 | 2026-11-13. Epic cut confirmed by the user on 2026-11-13. *(to be validated)* = assumption, not yet confirmed.

## 1. Release

- **Release:** MVP – "Nothing waits unseen"
- **Release goal:** Demands reach a decision faster because no wait on the Business Partner goes unnoticed (G-01), and waiting demands are visible (G-03).
- **Release metric:** Elapsed time waiting on the Business Partner per demand – target TBD.

## 2. Epics

| Epic ID | Name | Type | Outcome | Steps spanned | Personas | File |
|---------|------|------|---------|---------------|----------|------|
| E-MVP-01 | Demand in, registered and owned | Feature | The Demand Owner sees each new demand already in JIRA, with an owner | T-01 – T-03 | P-01, P-02 | E-MVP-01-demand-intake.md |
| E-MVP-02 | Questionnaire without chasing | Feature | The questionnaire goes out, reminders are released, long waits raise an alert, and the reply lands in JIRA | T-04 – T-06 | P-01, P-02 | E-MVP-02-questionnaire.md |
| E-MVP-03 | Demand reaches handover with every later wait followed up | Feature | The BRD/DDS, cost and SA/PO waits are chased with released reminders; the demand ends at "Product Team notified" | T-07 – T-22 | P-01, P-03 | E-MVP-03-follow-ups-to-handover.md |
| E-MVP-04 | Demand Manager sees what is stuck or closed | Feature | The Demand Manager sees every demand waiting on the Business Partner and for how long; closures are recorded with a reason | T-23 – T-24 | P-02, P-01 | E-MVP-04-waiting-overview.md |

No enabler epics. Mailbox access, JIRA access and hosting are dependencies, listed in each epic.

## 3. Card Coverage

| Card ID | Card | Step | Epic |
|---------|------|------|------|
| S-01 | See new demand from the DC mailbox | T-01 | E-MVP-01 |
| S-02 | Forward a demand received elsewhere *(manual)* | T-01 | E-MVP-01 |
| S-03 | Get the demand registered in JIRA | T-02 | E-MVP-01 |
| S-05 | Assign the Demand Owner *(manual)* | T-03 | E-MVP-01 |
| S-07 | Release the prepared questionnaire | T-04 | E-MVP-02 |
| S-08 | Release a prepared reminder | T-05 | E-MVP-02 |
| S-09 | Get alerted on a long wait | T-05 | E-MVP-02 |
| S-10 | See the reply attached in JIRA | T-05 | E-MVP-02 |
| S-12 | Review the questionnaire *(manual)* | T-06 | E-MVP-02 |
| S-13 | Run the meeting and issue minutes, BRD/DDS *(manual)* | T-07 | E-MVP-03 |
| S-17 | Record the LoDA fit decision *(manual)* | T-08 | E-MVP-03 |
| S-20 | Record the complexity confirmation *(manual)* | T-09 | E-MVP-03 |
| S-22 | Run requirement meetings and issue BRD/DDS *(manual)* | T-10 | E-MVP-03 |
| S-24 | Share an indicative cost *(manual)* | T-11 | E-MVP-03 |
| S-26 | Release BRD/DDS reminders | T-12 | E-MVP-03 |
| S-28 | Assess feasibility with the Product Team *(manual)* | T-13 | E-MVP-03 |
| S-30 | Record the TPO approval *(manual)* | T-14 | E-MVP-03 |
| S-32 | Baseline the BRD/DDS *(manual)* | T-15 | E-MVP-03 |
| S-34 | Send the cost package *(manual)* | T-16 | E-MVP-03 |
| S-37 | Release cost-acceptance reminders | T-17 | E-MVP-03 |
| S-39 | Hand over to the Product Team *(manual)* | T-18 | E-MVP-03 |
| S-41 | Enter the SAP data *(manual)* | T-19 | E-MVP-03 |
| S-43 | Issue the Service Agreement *(manual)* | T-20 | E-MVP-03 |
| S-45 | Release SA/PO reminders | T-21 | E-MVP-03 |
| S-47 | Notify the Product Team and complete *(manual)* | T-22 | E-MVP-03 |
| S-49 | Close a demand with a reason *(manual)* | T-23 | E-MVP-04 |
| S-52 | See the demands waiting on the Business Partner, and for how long | T-24 | E-MVP-04 |

All 27 MVP cards are covered once each.

## 4. Open Questions

1. Reminder and escalation timings. *(TBD – decided in E-MVP-02 stories, reused by E-MVP-03)*
2. Which live demand is the pilot? *(TBD)*
