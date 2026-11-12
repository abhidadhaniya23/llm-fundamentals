# E-MVP-01 – Demand in, registered and owned – User Stories

> Status: Draft | Version 0.1 | 2026-11-13. Sprint length: TBD. *(to be validated)* = assumption, not yet confirmed.

## 1. Epic Summary

- **Epic:** E-MVP-01 – Demand in, registered and owned
- **Outcome:** The Demand Owner opens JIRA and finds each new demand already registered, with the original email attached and an owner assigned.
- **Personas:** P-01 The Demand Owner, P-02 The Demand Manager

## 2. Story Overview

| Story ID | Title | Persona | Cards | Step | Split pattern | Type |
|----------|-------|---------|-------|------|---------------|------|
| E-MVP-01-SP-01 | How do we recognise a new demand in the mailbox? | – | S-01, S-03 | T-01, T-02 | Spike | Spike |
| E-MVP-01-US-01 | New demand email becomes a JIRA demand | P-01 | S-01, S-03 | T-01, T-02 | Paths (basic path) | Story |
| E-MVP-01-US-02 | Replies do not create new demands | P-01 | S-03 | T-02 | Rules | Story |
| E-MVP-01-US-03 | Forwarded demands are registered under the Business Partner | P-01, P-02 | S-02, S-03 | T-01, T-02 | Paths (variation) | Story |
| E-MVP-01-US-04 | Demand Manager assigns the owner of a new demand | P-02 | S-05 | T-03 | none | Story |

**Ready for the live session:** E-MVP-01-US-01 (basic path; no AI; one visible result).

## 3. E-MVP-01-US-01 – New demand email becomes a JIRA demand

**As** the Demand Owner, **I want** every new demand email in the shared DC mailbox to appear as a JIRA demand ticket with the email attached, **so that** I no longer register demands by hand and no demand is missed.

- **Cards / step:** S-01, S-03 / T-01, T-02
- **Business rules:**
  - The shared DC mailbox is the only intake channel *(T 1:53:31)*.
  - JIRA is the single source of truth *(PDF)*.
  - Ticket title = email subject; sender = Business Partner contact; received date = demand date *(to be validated)*.

**Acceptance criteria**

**AC1 – New demand is registered**
Given the email "New demand: dashboard for plant logistics" from a Business Partner arrives in the shared DC mailbox
When the product checks the mailbox
Then a JIRA demand ticket "New demand: dashboard for plant logistics" exists, with the sender, the received date and the original email attached

**AC2 – Registration is visible to the team**
Given a demand ticket was created
When a Demand Owner opens the JIRA demand list
Then the new ticket appears with status "New" and no owner yet

**AC3 – Each demand is registered once**
Given the same email has already been registered
When the product checks the mailbox again
Then no second ticket is created

**AC4 – Failure is visible**
Given the product cannot create the ticket (e.g. JIRA unavailable)
When it checks the mailbox
Then the email stays unprocessed and is retried on the next check, and no demand is lost *(to be validated)*

- **Notes & assumptions:** How "new demand" is recognised comes from SP-01. The JIRA project and issue type are still to be named.
- **Dependencies:** E-MVP-01-SP-01; mailbox read access; JIRA Cloud access
- **Estimate:** TBD

**INVEST check**

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ removes manual registration | ✅ after SP-01 | ✅ | ✅ |

## 4. E-MVP-01-US-02 – Replies do not create new demands

**As** the Demand Owner, **I want** replies and follow-ups on a registered demand not to be registered as new demands, **so that** the demand list has no duplicates.

- **Cards / step:** S-03 / T-02
- **Business rules:** A reply in the thread of a registered demand is not a new demand *(to be validated – SP-01)*.

**Acceptance criteria**

**AC1 – Reply in the same thread**
Given a demand "New demand: dashboard for plant logistics" is registered
When the Business Partner sends "RE: New demand: dashboard for plant logistics"
Then no new demand ticket is created

**AC2 – Unclear email**
Given an email that cannot be clearly matched as new or as a reply
When the product checks the mailbox
Then it is registered as a new demand and flagged "check: possible duplicate" for the Demand Owner *(to be validated)*

**AC3 – Non-demand mail**
Given an internal or automatic email (e.g. out-of-office) arrives in the mailbox
When the product checks the mailbox
Then no demand ticket is created *(to be validated)*

- **Notes & assumptions:** Attaching replies to the existing ticket is part of E-MVP-02 (S-10), not this story.
- **Dependencies:** E-MVP-01-US-01, E-MVP-01-SP-01
- **Estimate:** TBD

**INVEST check**

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ❌ builds on US-01 (accepted: rule split) | ✅ | ✅ clean demand list | ✅ after SP-01 | ✅ | ✅ |

## 5. E-MVP-01-US-03 – Forwarded demands are registered under the Business Partner

**As** the Demand Manager or a Demand Owner who received a demand personally, **I want** to forward it to the shared DC mailbox and have it registered under the original Business Partner, **so that** the demand is handled like any other and the right contact is recorded.

- **Cards / step:** S-02, S-03 / T-01, T-02
- **Business rules:** Anyone who receives a demand outside the mailbox forwards it there *(T 1:54:07)*.

**Acceptance criteria**

**AC1 – Forwarded email**
Given the Demand Manager forwards a Business Partner's email "FW: Demand for supplier reporting" to the shared DC mailbox
When the product checks the mailbox
Then a demand ticket is created with the original Business Partner as the contact, and the forwarder noted

**AC2 – Original sender cannot be read**
Given a forwarded email whose original sender cannot be identified
When it is registered
Then the ticket is created with the contact field empty and flagged for the Demand Owner to complete

- **Notes & assumptions:** Demands from Teams messages are forwarded as email by hand *(to be validated)*.
- **Dependencies:** E-MVP-01-US-01
- **Estimate:** TBD

**INVEST check**

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ❌ builds on US-01 (accepted: path split) | ✅ | ✅ | ✅ | ✅ | ✅ |

## 6. E-MVP-01-US-04 – Demand Manager assigns the owner of a new demand

**As** the Demand Manager, **I want** to assign a Demand Owner on each new demand ticket, **so that** every demand has a named owner from the start.

- **Cards / step:** S-05 / T-03 (manual in the MVP – done in JIRA)
- **Business rules:** The Demand Manager decides the owner *(user input 2026-11-13)*. No owner suggestion in the MVP.

**Acceptance criteria**

**AC1 – Assign owner**
Given a new demand ticket with no owner
When the Demand Manager sets the Demand Owner on the ticket
Then the ticket shows the owner, and the owner sees it in their JIRA demand list

**AC2 – Unassigned demands are findable**
Given several new demands
When the Demand Manager opens the JIRA demand list
Then demands without an owner can be filtered and shown first

- **Notes & assumptions:** Uses standard JIRA assignment and a saved filter. No product build is expected *(to be validated)*.
- **Dependencies:** E-MVP-01-US-01
- **Estimate:** TBD

**INVEST check**

| I | N | V | E | S | T |
|---|---|---|---|---|---|
| ✅ | ✅ | ✅ clear ownership | ✅ | ✅ | ✅ |

## 7. Spikes

| Spike ID | Question to answer | Timebox | Unblocks |
|----------|--------------------|---------|----------|
| E-MVP-01-SP-01 | How can the product read the shared DC mailbox, and which signals separate a new demand from a reply, a forward or other mail? Look at real examples from recent demands. | 2 days *(to be validated)* | US-01, US-02, US-03 |

## 8. Coverage

### 8.1 Cards → Stories

| Card ID | Card | Stories |
|---------|------|---------|
| S-01 | See new demand from the DC mailbox | US-01 |
| S-02 | Forward a demand received elsewhere | US-03 |
| S-03 | Get the demand registered in JIRA | US-01, US-02, US-03 |
| S-05 | Assign the Demand Owner | US-04 |

### 8.2 Epic Acceptance Criteria → Story Criteria

| Epic AC | Covered by |
|---------|-----------|
| AC1 – Every demand is registered | US-01 AC1, AC2, AC4 |
| AC2 – No duplicates | US-01 AC3, US-02 AC1–AC3 |
| AC3 – Forwarded demands count too | US-03 AC1, AC2 |
| AC4 – Every demand has an owner | US-04 AC1, AC2 |

## 9. Open Questions

1. Which JIRA project and issue type hold demands, and what is the starting status? *(assumed: "New" – to be validated)*
2. How often should the mailbox be checked? *(TBD)*
3. Should the Demand Manager be notified of each new unassigned demand? *(not in the epic – add to the epic if wanted)*
