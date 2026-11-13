# E-MVP-04 – Demand Manager sees what is stuck or closed

> Status: Draft | Version 0.1 | 2026-11-13. Release: MVP. Type: Feature. *(to be validated)* = assumption, not yet confirmed.

## 1. Epic Hypothesis

For the Demand Manager, who sees demand status only in the weekly call, the Waiting overview is a list of every demand waiting on the Business Partner and for how long, together with closed demands and their reasons. Unlike the weekly call, it shows stalled demands at any time.

## 2. Outcome

- **Business outcome:** Stuck demands are noticed between weekly calls (G-03). Every closed demand has a reason (G-03).
- **Leading indicator:** How often the Demand Manager opens the overview between weekly calls.
- **What the persona can do afterwards:** The Demand Manager opens one list and sees which demands are waiting, on what, since when, and who owns them. Closed demands show their reason.

## 3. Personas

- P-02 – The Demand Manager – uses the overview.
- P-01 – The Demand Owner – records the closure reason.

## 4. Journey Steps & Cards

| Step | Step name | Cards |
|------|-----------|-------|
| T-23 | Close / reopen | S-49 Close a demand with a reason *(manual)* |
| T-24 | Demand overview | S-52 See the demands waiting on the Business Partner, and for how long |

## 5. Scope

### 5.1 In Scope

- A list of open demands that are waiting on the Business Partner: wait type, days waiting, owner, alert state.
- A closure reason recorded in JIRA when a demand is closed (by hand in the MVP), shown in the overview.

### 5.2 Out of Scope

- Full overview of all demands and statuses (S-53, Release 3).
- Closure note to the Business Partner (S-50, Release 2); reopening (S-51, Release 3).
- Login and roles: no login in the MVP.

## 6. Acceptance Criteria (epic level)

**AC1 – Waiting demands are visible**
Given demands waiting on the questionnaire, BRD/DDS, cost acceptance or SA/PO
When the Demand Manager opens the overview
Then each one shows what it waits for, for how many days, and its owner

**AC2 – Long waits stand out**
Given a demand has passed the escalation interval
When it appears in the overview
Then it is marked as escalated

**AC3 – Closures have a reason**
Given a demand is closed at any decision point
When the Demand Owner records the closure in JIRA
Then the reason is stored and the demand no longer appears as waiting

## 7. Constraints

| Constraint | Source |
|------------|--------|
| No login in the MVP; internal use only | Story map §4 |
| JIRA is the source for status | Story map §4 |

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| E-MVP-02 and E-MVP-03 (wait tracking) | Epic | Open |
| A place to show the list (LoDA dashboard or a JIRA view) | Decision | Open |

## 9. Risks & Assumptions

| Item | Type | Mitigation or validation |
|------|------------------|--------------------------|
| Without login, anyone on the internal network can see the list | Assumption | Accepted for the MVP (internal only); roles come in a later release |

## 10. Size

TBD *(to be validated)*

## 11. Open Questions

1. Does the list live on the LoDA dashboard or as a JIRA filter? *(assumed: LoDA dashboard – to be validated)*
2. What are the closure reason options? *(TBD – e.g. outside LoDA scope, not accepted, no approval, cost rejected, SA/PO not received)*
