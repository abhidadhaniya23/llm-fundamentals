# E-MVP-03 – Demand reaches handover with every later wait followed up

> Status: Draft | Version 0.1 | 2026-11-13. Release: MVP. Type: Feature. *(to be validated)* = assumption, not yet confirmed.

## 1. Epic Hypothesis

For Demand Owners who chase the Business Partner by hand for the BRD/DDS, the cost acceptance and the signed SA/PO, Follow-ups to handover extends the release-and-remind flow to every later wait. It keeps all other steps running as today, recorded in JIRA. Unlike today, a demand can run from alignment to "Product Team notified" without a wait going unnoticed.

## 2. Outcome

- **Business outcome:** Shorter waits at BRD/DDS, cost acceptance and SA/PO (G-01). The pilot demand completes end to end (G-03).
- **Leading indicator:** Wait time at each of the three waits in the pilot demand.
- **What the persona can do afterwards:** The Demand Owner runs the meetings and decisions as today. At each of the three waits they release prepared reminders, and the demand ends at "Product Team notified".

## 3. Personas

- P-01 – The Demand Owner – runs the steps and releases reminders.
- P-03 – The Technical Reviewer – takes part in complexity, feasibility and approval, as today.

## 4. Journey Steps & Cards

| Step | Step name | Cards |
|------|-----------|-------|
| T-07 | Alignment meeting | S-13 Run the meeting and issue minutes, BRD/DDS *(manual)* |
| T-08 | ◇ LoDA fit | S-17 Record the LoDA fit decision *(manual)* |
| T-09 | ◇ Complexity | S-20 Record the complexity confirmation *(manual)* |
| T-10 | Requirement meetings | S-22 Run requirement meetings and issue BRD/DDS *(manual)* |
| T-11 | Indicative cost | S-24 Share an indicative cost *(manual)* |
| T-12 | Wait for BRD/DDS | S-26 Release BRD/DDS reminders |
| T-13 | Feasibility | S-28 Assess feasibility with the Product Team *(manual)* |
| T-14 | ◇ TPO approval | S-30 Record the TPO approval *(manual)* |
| T-15 | Baseline | S-32 Baseline the BRD/DDS *(manual)* |
| T-16 | Send cost package | S-34 Send the cost package *(manual)* |
| T-17 | ◇ Wait for cost acceptance | S-37 Release cost-acceptance reminders |
| T-18 | Handover | S-39 Hand over to the Product Team *(manual)* |
| T-19 | SAP data | S-41 Enter the SAP data *(manual)* |
| T-20 | Issue SA | S-43 Issue the Service Agreement *(manual)* |
| T-21 | ◇ Wait for SA/PO | S-45 Release SA/PO reminders |
| T-22 | Notify and complete | S-47 Notify the Product Team and complete *(manual)* |

## 5. Scope

### 5.1 In Scope

- Release-and-remind at T-12, T-17 and T-21, with long-wait alerts (the same pattern as E-MVP-02).
- Starting each wait when the Demand Owner marks the outgoing item as sent (BRD/DDS, cost package, SA) *(to be validated)*.
- Stopping reminders when the reply arrives in the mailbox and is attached to JIRA.

Manual cards need no build. They keep the walking skeleton complete.

### 5.2 Out of Scope

- AI drafts, completeness check, packages, answer detection (Release 2).
- Consult requests (Release 3); evidence (Later).

## 6. Acceptance Criteria (epic level)

**AC1 – BRD/DDS wait is followed up**
Given the BRD/DDS has been issued to the Business Partner
When it is not returned within the reminder interval
Then the Demand Owner has a prepared reminder to release, and a long wait alerts the Demand Owner and the Demand Manager

**AC2 – Cost acceptance wait is followed up**
Given the cost package has been sent
When there is no answer within the reminder interval
Then the Demand Owner has a prepared reminder to release

**AC3 – SA/PO wait is followed up**
Given the Service Agreement has been issued
When the signed SA and the PO have not arrived within the reminder interval
Then the Demand Owner has a prepared reminder to release

**AC4 – The pilot demand completes**
Given a pilot demand registered through E-MVP-01
When all steps are done (manual or in the product)
Then the JIRA ticket shows every step and decision, and the demand ends at "Product Team notified"

## 7. Constraints

| Constraint | Source |
|------------|--------|
| Nothing goes to the Business Partner without Demand Owner release | Story map §4 |
| JIRA records every step and decision | Story map §4 |
| People make every decision | Vision §5.2 |

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| E-MVP-02 (release-and-remind pattern, alerts) | Epic | Open |
| E-MVP-01 (registered demand) | Epic | Open |

## 9. Risks & Assumptions

| Item | Type | Mitigation or validation |
|------|------------------|--------------------------|
| The Demand Owner forgets to mark an item as sent, so no wait starts | Risk | Prompt in JIRA; check in the pilot |
| The pilot demand takes 1–2 months to complete | Assumption | Measure the wait times as they happen; don't wait for completion to learn |

## 10. Size

TBD *(to be validated)*

## 11. Open Questions

1. Can the same reminder intervals be used for all three waits? *(assumed: yes – to be validated)*
2. How does the product know an outgoing item was sent? Demand Owner marks it, or the product sees it in the mailbox? *(assumed: Demand Owner marks it – to be validated)*
