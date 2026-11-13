# DC – Product Context (research input)

> Facts about the LoDA Demand Handling & Consulting (DC) process, taken from the sources below. This is input for the SDLC skills, not a spine artifact. Timestamps refer to the transcript. *(to be validated)* = heard in the meeting but not clearly confirmed.
>
> Sources:
> - **PDF** – `Demand_Handling_Consulting_Process_Flow_Refined (2).pdf` (as-is process flow)
> - **T** – `meeting-transcript-12-11-2026.md` (team session, 2026-11-12)

## 1. Scope

- The product is for internal use only: the LoDA demand team. Business Partners are not users. They should not be able to tell whether a person or the automation is replying. (T 1:14:04, 1:51:54)
- The process runs from "New demand received" to "Product Team notified to commence development". (PDF)

## 2. Roles

| Role | What they do | Source |
|------|--------------|--------|
| Demand Owner | Owns each demand end to end and is the first contact for the Business Partner. Pulls in the Demand Manager or technical roles when needed. After cost approval, also raises the SAP project creation. No separate PMO/SAP role is planned | T 1:12:09, 1:13:27, 1:33:25, 1:34:38 |
| Demand Manager | Is consulted on business and stakeholder questions. Today runs a weekly cadence call that reviews all demands. Escalation point | T 1:12:09, 1:31:26, 1:36:41 |
| Technical roles: Technical Architect, Technical Product Owner / Product Team | Consulted on technical questions. Confirm complexity, assess feasibility, give final approval | T 1:12:09, PDF |
| Business Partner | External. Raises the demand, fills in the questionnaire/BRD/DDS, accepts cost, signs the SA, sends the PO | PDF, T 1:11:01 |

## 3. Today's numbers

- About 60 demands per year. The number is expected to grow. (T 1:44:01, 1:44:12)
- 30–40 hours of Demand Owner effort per demand. (T 1:44:12)
- Each demand runs for 1–2 months, mostly waiting on follow-ups. (T 1:44:12)

## 4. Gaps in the PDF flow (found in the session)

1. **Closure:** the flow does not say what happens after "Demand Closed": is the Business Partner notified, and can the demand be reopened? (T 1:24:09)
2. **Who does what:** the flow shows steps, but no owner for each step. (T 1:24:09, 1:24:15)
3. **Intake:** the flow does not show how a demand really arrives. Today it often reaches the Demand Manager by email and is forwarded to the DC mailbox. (T 1:26:41)
4. **SAP / project creation:** no role is named for step "SA process initiated". In practice the Demand Owner does it. (T 1:26:41, 1:33:25)
5. **Assignment:** no rule for who becomes the Demand Owner. Today the owner picks the demand themselves. (T 1:35:29)
6. **Pipeline view:** the Demand Manager has no status view across all demands. Only a weekly call. (T 1:30:30, 1:31:26)
7. **Knowledge:** there is no catalog of LoDA capabilities. Past demands are not in a usable place either. (T 1:29:51, 1:30:19)

## 5. Decisions for the future product

| Topic | Decision | Source |
|-------|----------|--------|
| Intake | Shared mailbox is the only intake channel. Anyone who receives a demand another way (Teams, personal email) forwards it to the mailbox. Output can go to several channels | T 1:53:07, 1:53:31, 1:54:07 |
| Demand Owner assignment | A demand assistant suggests the Demand Owner | T 1:35:33, 1:36:08 |
| Business Partner waits | Automatic reminders, then internal escalation to the Demand Owner and Demand Manager. Details come at epic level | T 1:36:24, 1:37:21, 1:37:45 |
| Visibility | A dashboard (the LoDA dashboard, which also holds the health check) plus consult requests | T 1:31:19, 1:32:06, 1:40:46 |
| System of record | JIRA Cloud | T 1:54:31, PDF |
| Hosting | On-premise. A company-approved cloud is not available today. Cloud stays open with IT *(to be validated)* | T 1:41:51, 1:42:06, 1:42:34 |
| Sign-in | No login in the MVP: the product is internal-only. Roles and SSO come in a later release | User input 2026-11-13; T 2:30:30 |
| Documents | SharePoint / OneDrive | T 1:56:19, 1:56:20 |
| Notifications | JIRA, email, Teams | T 1:56:05 |
| Minutes of meeting | Drafted from the Teams transcript or the Demand Owner's notes | T 1:54:43 |
| SA signed / PO received | Arrives in the shared mailbox. A person confirms it manually | T 1:55:35, 1:55:45 |
| SAP planning (project creation) | Manual. AI prepares the data only if it has the context | T 1:55:04, 1:55:17 |
| AI labelling | AI content is labelled internally only, never towards the Business Partner | T 1:51:42, 1:51:54 |
| AI unsure | Falls back to manual review | T 1:50:27 |
| AI evidence | From new demands only. LoDA fit check and cost estimate stay manual until a threshold is reached | T 1:50:52, 1:51:19 |
| LoDA fit decision | The Demand Owner decides "Can LoDA address the demand?". They may consult product owners to check whether a technical feature is supported | User input 2026-11-13 |
| Human approval | Anything that goes to the business needs human approval | T 2:08:24 |
| Rollout | Phased by process stage. Pilot with one demand | T 1:58:02, 1:59:57 |

## 6. Automation levels

| Level | Meaning | Example from the session |
|-------|---------|--------------------------|
| A – Direct automation | Rule-based. No human step | Register the demand in JIRA (T 2:07:48) |
| B – AI with suggestion | AI proposes. A person checks and does the extra analysis | Early technical feasibility hints from past demands (T 1:17:45) |
| C – AI with evidence | AI shows the proof behind its recommendation. A person confirms | "4 of 9 BRD columns are empty – send the follow-up?" (T 1:18:43). Technical feasibility should move from B to C (T 2:08:12) |

A + B is used where the product prepares something automatically but a person must release it, for example any email to the Business Partner. (T 2:06:28, 2:07:57)

## 7. Lessons for slicing (from the epic discussion)

- Yesterday's epics were cut by layer (PoC → platform → connectors), so nothing usable reached production until every layer was done. (T 2:25:46)
- The MVP should be a thin end-to-end slice. Example: start with the shared mailbox only, not every connector. Because the app is internal, roles and SSO can wait. (T 2:30:30)
