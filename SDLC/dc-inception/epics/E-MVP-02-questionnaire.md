# E-MVP-02 – Questionnaire without chasing

> Status: Draft | Version 0.1 | 2026-11-13. Release: MVP. Type: Feature. *(to be validated)* = assumption, not yet confirmed.

## 1. Epic Hypothesis

For Demand Owners who write, send, chase and record the standard questionnaire by hand, the Questionnaire flow sends the prepared questionnaire on the Demand Owner's release, prepares reminders while the Business Partner has not answered, alerts on long waits, and files the reply in JIRA. Unlike today's manual chasing, no questionnaire wait goes unnoticed and nothing is re-typed.

## 2. Outcome

- **Business outcome:** A shorter questionnaire wait and less Demand Owner effort (G-01, G-02); long waits are visible (G-03).
- **Leading indicator:** Share of questionnaire reminders released from the product, and the number of long-wait alerts per demand.
- **What the persona can do afterwards:** The Demand Owner releases the questionnaire with one action, releases reminders when prompted, and finds the completed questionnaire attached in JIRA.

## 3. Personas

- P-01 – The Demand Owner – releases the questionnaire and reminders; reviews the answers.
- P-02 – The Demand Manager – receives the long-wait alert.

## 4. Journey Steps & Cards

| Step | Step name | Cards |
|------|-----------|-------|
| T-04 | Release questionnaire | S-07 Release the prepared questionnaire |
| T-05 | Wait with reminders | S-08 Release a prepared reminder; S-09 Get alerted on a long wait; S-10 See the reply attached in JIRA |
| T-06 | Review answers | S-12 Review the questionnaire *(manual)* |

## 5. Scope

### 5.1 In Scope

- Preparing the standard questionnaire email for a demand, and sending it on release.
- Tracking the wait; preparing reminders at set intervals; alerting the Demand Owner and the Demand Manager on a long wait.
- Detecting the reply in the mailbox and attaching it to the JIRA ticket.
- Recording each step in JIRA.

The release-and-remind pattern built here is reused for the later waits in E-MVP-03.

### 5.2 Out of Scope

- AI summary and gap flags (S-11, Release 2).
- Changing the questionnaire content.

## 6. Acceptance Criteria (epic level)

**AC1 – Nothing goes out without release**
Given a registered demand with an owner
When the questionnaire is prepared
Then it is sent to the Business Partner only after the Demand Owner releases it, and the sending is recorded in JIRA

**AC2 – Reminders are ready when needed**
Given the questionnaire has not been answered within the reminder interval
When the interval passes
Then the Demand Owner has a prepared reminder to release

**AC3 – Long waits are seen**
Given the questionnaire is still not answered after the escalation interval
When that interval passes
Then the Demand Owner and the Demand Manager are alerted

**AC4 – The reply is filed**
Given the Business Partner returns the completed questionnaire to the mailbox
When it arrives
Then it is attached to the demand's JIRA ticket and reminders stop

## 7. Constraints

| Constraint | Source |
|------------|--------|
| Nothing goes to the Business Partner without Demand Owner release | Story map §4 |
| No AI labelling towards the Business Partner | Story map §4 |
| JIRA records every step | Story map §4 |

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| E-MVP-01 (registered demand with an owner) | Epic | Open |
| Send access for the shared DC mailbox | System | Open |
| Standard questionnaire template | Team (Demand Owner) | Open |

## 9. Risks & Assumptions

| Item | Type | Mitigation or validation |
|------|------------------|--------------------------|
| The Business Partner replies from a different address or thread | Risk | The Demand Owner can link a reply by hand |
| Reminder and escalation intervals are not agreed yet | Assumption | Agree them with the Demand Manager before the pilot |

## 10. Size

TBD *(to be validated)*

## 11. Open Questions

1. Reminder interval, maximum number of reminders, and escalation interval? *(TBD with the Demand Manager)*
2. How are alerts delivered – email, Teams, or the dashboard? *(assumed: email – to be validated)*
