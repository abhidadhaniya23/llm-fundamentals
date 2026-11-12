# E-MVP-01 – Demand in, registered and owned

> Status: Draft | Version 0.1 | 2026-11-13. Release: MVP. Type: Feature. *(to be validated)* = assumption, not yet confirmed.

## 1. Epic Hypothesis

For Demand Owners and the Demand Manager, who today receive demands through several channels and register them by hand, Demand intake is a single entry through the shared DC mailbox that registers every new demand in JIRA automatically. Unlike today's forwarding, self-picking and manual registration, every demand starts in one place, is recorded at once, and gets a named owner.

## 2. Outcome

- **Business outcome:** No demand is missed, and each one has a JIRA ticket and an owner from the start (G-03, G-01).
- **Leading indicator:** Share of new demands registered in JIRA without manual entry.
- **What the persona can do afterwards:** The Demand Owner opens JIRA and finds the new demand already registered, with the original email attached and their name as owner.

## 3. Personas

- P-01 – The Demand Owner – sees and owns the registered demand; forwards demands received elsewhere.
- P-02 – The Demand Manager – forwards demands received personally; assigns the owner (manual in the MVP).

## 4. Journey Steps & Cards

| Step | Step name | Cards |
|------|-----------|-------|
| T-01 | See new demand in the mailbox | S-01 See new demand from the DC mailbox; S-02 Forward a demand received elsewhere *(manual)* |
| T-02 | Demand registered | S-03 Get the demand registered in JIRA |
| T-03 | Owner assigned | S-05 Assign the Demand Owner *(manual)* |

## 5. Scope

### 5.1 In Scope

- Detecting a new demand email in the shared DC mailbox.
- Creating the JIRA demand ticket automatically, with the email attached.
- Recording the owner in JIRA (assigned by hand in the MVP).

### 5.2 Out of Scope

- Extracting key facts into the ticket (S-04, Release 2).
- Owner suggestion (S-06, Release 3).
- Intake from any channel other than the shared mailbox.

## 6. Acceptance Criteria (epic level)

**AC1 – Every demand is registered**
Given a Business Partner's demand email arrives in the shared DC mailbox
When the product processes the mailbox
Then a JIRA demand ticket exists for it, with the email attached

**AC2 – No duplicates**
Given a follow-up email on a demand that is already registered
When it arrives in the mailbox
Then no second demand ticket is created *(to be validated)*

**AC3 – Forwarded demands count too**
Given a demand that first reached a Demand Owner or the Demand Manager directly
When it is forwarded to the shared DC mailbox
Then it is registered like any other demand

**AC4 – Every demand has an owner**
Given a newly registered demand
When the Demand Manager assigns the Demand Owner
Then the ticket shows the owner, and the owner can see the demand

## 7. Constraints

| Constraint | Source |
|------------|--------|
| The shared DC mailbox is the only intake channel | Story map §4 |
| JIRA records every step | Story map §4 |
| On-premise hosting; JIRA Cloud; no login in the MVP | Story map §4 |

## 8. Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| Read access to the shared DC mailbox | System | Open |
| JIRA Cloud project and permission to create demand tickets | System | Open |
| On-premise hosting | Team (IT) | Open |

## 9. Risks & Assumptions

| Item | Type | Mitigation or validation |
|------|------|--------------------------|
| Not every email in the mailbox is a new demand (replies, spam, internal mails) | Risk | Rule for what counts as a new demand; review in the pilot |
| People keep sending demands to individuals | Risk | Team agreement to forward; check in the pilot |

## 10. Size

TBD *(to be validated)*

## 11. Open Questions

1. How does the product tell a new demand from a reply on an existing one? *(assumed: by email thread / subject reference – to be validated)*
2. Which JIRA project and issue type are used for demands? *(unknown)*
