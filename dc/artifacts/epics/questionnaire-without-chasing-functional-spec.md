# Questionnaire Without Chasing - Functional Specification

> Status: Draft | Version 0.1 | 2026-11-13
> Epic: EPIC-DC-2026-002 (`questionnaire-without-chasing-epic.md`)
> Source: `dc/context/business-context.md`
> *(TBD)* = not yet available. *(to be validated)* = assumption, not yet confirmed.

---

## 1. Executive Summary

Every LoDA demand starts with the standard questionnaire. Today the Demand Owner writes and sends it, remembers to chase, reads each reply, works out what is still missing, writes the next follow-up, and updates JIRA by hand. This takes about three follow-up rounds per demand and sits inside the 25-30 days LoDA holds each demand.

This feature runs the questionnaire step without chasing, while the Demand Owner stays in control. The assistant prepares the questionnaire; the Demand Owner releases it. While the Business Partner has not answered, reminders are prepared at an agreed rhythm and long waits alert the Demand Owner and the LoDA Manager. Replies are filed in JIRA, answers are merged across replies, gaps are flagged, and one consolidated follow-up is drafted for approval.

**Target users:** Demand Owner (primary), LoDA Manager (secondary). The Business Partner does not use the assistant and cannot tell whether a person or the assistant wrote a message.

**Key metrics:** follow-up rounds from about 3 to 1.5 or fewer; AI drafts ready in under 30 minutes; at least 80% of drafts approved with minor edits; 100% of questionnaire steps recorded in JIRA.

---

## 2. Business Case & Impact

### 2.1 Why This Feature?

- **Problem:** the questionnaire is the first wait of every demand. It is chased by hand, tracked in personal spreadsheets, and gaps are found one reply at a time.
- **Trigger:** LoDA spends 25-30 days of its own time per demand and about 30 hours of manual effort, mostly on work that needs no judgement. Demand volume is meant to grow from 10-30 to 30+ per month with the same team.
- **Cost of not building:** about three rounds per demand continue; stalled waits stay unseen; JIRA stays incomplete so LoDA-held time cannot be proven.
- **Who asks for it:** LoDA leadership and Demand Owners, through the DC Flow business case.

### 2.2 Expected Business Impact

- Fewer follow-up rounds and a shorter first wait.
- Same-day visibility of long waits for the LoDA Manager.
- Consistent communication regardless of which Demand Owner handles the demand.
- A complete JIRA trail for the questionnaire step, usable as a measurement baseline.
- A release-and-remind pattern reusable for the BRD/DDS, cost acceptance and SA/PO waits.

**Compliance rules (internal):** no outbound message without Demand Owner release; no AI labelling towards the Business Partner; local model only for all data, with personal data masked.

### 2.3 Success Metrics

| # | Metric | Current (Baseline) | Target | Measurement Method |
|---|--------|-------------------|--------|-------------------|
| M1 | Follow-up rounds per demand | About 3 | 1.5 or fewer | Count of follow-ups released per demand in JIRA |
| M2 | AI draft turnaround | Not applicable | Under 30 minutes | Time from trigger to draft ready |
| M3 | Draft acceptance | Not applicable | At least 80% approved with minor edits | Edit rate recorded at approval |
| M4 | JIRA completeness for the step | Partial | 100% of events recorded | Events recorded vs. events that occurred |
| M5 | Questionnaire elapsed time (release to complete answers) | TBD | TBD | Release and completion timestamps |
| M6 | Demand Owner effort on the step | TBD, part of about 30 h | TBD | Time study on pilot demands |
| M7 | Time from threshold crossing to LoDA Manager awareness | TBD, no alert exists | Same day | Alert time vs. threshold crossing |

No reliable baseline exists, because JIRA timestamps are incomplete. Baselines for M5 and M6 will be taken from 3 months of historical JIRA data before go-live.

### 2.4 Return on Investment

- **Time:** write-chase-merge-file work becomes review-and-release; hours saved TBD until M6 is baselined.
- **Capacity:** the same team handles more demands per month.
- **Cycle time:** each day saved at the first wait shortens the whole demand.
- **Risk:** a complete record of every send, reminder, alert and reply.

---

## 3. Business Context

**Limitations today**
- The questionnaire is composed and sent by hand.
- No record of the wait, no prompt to chase, no list of open waits.
- Each follow-up is written from scratch; tone and timing vary by owner.
- Replies are read one by one to find gaps; vague answers are easy to miss.
- The LoDA Manager cannot see a stalled questionnaire.

**Proposed solution:** prepare, release, remind, alert, file, merge, flag, draft follow-up. Every step is recorded in JIRA. Every outbound message needs Demand Owner release.

**Binding constraints**

| Constraint | Source |
|------------|--------|
| No decision is automated; the assistant proposes, a person decides | Business rules |
| Nothing goes to the Business Partner without Demand Owner release | Business rules |
| No AI labelling towards the Business Partner | Business rules |
| Local model only; personal data masked | Business rules |
| JIRA is the single source of truth for demand stage | Business rules |
| When the assistant is unsure, the item falls back to manual review | Product decision |

---

## 4. Functional Requirements

### 4.1 Questionnaire Preparation
- Prepared automatically for a registered demand with an owner and a Business Partner address.
- Uses the team's standard questionnaire; changing its content is out of scope.
- Carries the demand reference so replies can be matched.
- Contains no indication it was prepared by the assistant.
- Editable by the Demand Owner before release.

### 4.2 Release
- Sent only on explicit Demand Owner release; no automatic send and no timeout send.
- On release: sent from the shared DC mailbox and recorded in JIRA with time, recipient and content.
- The Demand Owner may decide the questionnaire is not required and record a reason; nothing is sent.
- If sending fails, the Demand Owner is told, the demand is not marked as sent, and it stays available to release.

### 4.3 Wait Tracking
- The wait starts at release and ends when complete answers arrive or the Demand Owner ends it.
- Elapsed time is counted in working days. Holiday calendar handling is TBD.
- Open waits are visible to the LoDA Manager with days waited and reminders released.
- The Demand Owner can pause a wait, for example for a known Business Partner absence *(to be validated)*.

### 4.4 Reminders
- When the reminder interval passes with no reply, a reminder is prepared for the Demand Owner.
- It references the original questionnaire, is professional, and carries no sign of automation.
- Sent only on release; the owner can edit, release or dismiss it.
- A dismissed reminder is recorded and the next one is prepared at the following interval.
- Reminders stop on a complete reply, on closure, or at the maximum number of reminders.
- Interval and maximum are adjustable settings, not fixed behaviour. Values TBD.

### 4.5 Long-Wait Alert
- When the escalation threshold passes with no reply, the Demand Owner and the LoDA Manager are alerted the same day.
- The alert states the demand, Business Partner, days waited and reminders released.
- Internal only; nothing goes to the Business Partner.
- Recorded in JIRA; raised once per threshold crossing, not daily.
- Channel assumed email plus the waiting overview *(to be validated)*.

### 4.6 Reply Detection and Filing
- Replies are detected in the shared DC mailbox and matched to the demand by reference and conversation.
- On a confident match, the reply and attachments are attached to the JIRA ticket and receipt is recorded.
- On a weak match, nothing is attached automatically; the item is shown to the Demand Owner, who links it by hand.
- Out-of-office and other automatic replies are not answers and do not stop reminders.
- A reply that is a question rather than answers is filed but the wait stays open.
- Bounced messages tell the Demand Owner immediately and pause the wait.

### 4.7 Answer Merging and Gap Flagging
- Answers are merged across all replies into one view of the questionnaire.
- Each question is marked answered, missing, vague or not stated, with a pointer to the source reply.
- Examples: access roles missing; "before year-end close" vague; SAP company codes and cost centre not stated.
- Where the assistant is unsure, the item is marked for manual review.
- Personal data is masked and only the local model is used.

### 4.8 Follow-Up Draft
- When gaps remain, one consolidated follow-up covering all gaps is drafted within 30 minutes.
- Sent only after the Demand Owner approves it; sending starts a new wait.
- When no gaps remain, the Demand Owner records that the questionnaire is sufficient and the demand moves to alignment. That decision is the owner's, never the assistant's.

### 4.9 JIRA Record
- Send, reminder, dismissal, alert, reply, gap list, follow-up and decision are each recorded with a timestamp.

### 4.10 Settings
- Reminder interval, maximum reminders and escalation threshold are changeable without a product change.
- A change applies to open waits from that moment; reminders already sent are unaffected.

---

## 5. User Workflows

### Workflow 1 - Happy path, one reminder
1. Demand is registered with an owner and Business Partner address.
2. The questionnaire is prepared; the Demand Owner reviews, edits slightly and releases.
3. The send is recorded in JIRA; the wait starts.
4. The reminder interval passes; a reminder is prepared; the owner releases it.
5. The Business Partner replies with the completed questionnaire.
6. The reply is attached to the ticket, reminders stop, and the owner confirms the questionnaire is sufficient.

### Workflow 2 - Partial replies and gaps (Sabine's invoice archive demand)
1. The first reply leaves access roles and data classification missing, gives a vague deadline, and omits SAP company codes and cost centre.
2. The merged view marks each item; one follow-up covering all of them is drafted.
3. The owner approves it and it is sent; a new wait starts.
4. A second reply answers access roles only; the merged view updates and a smaller follow-up is drafted.
5. The cycle repeats until nothing is missing; the owner records the questionnaire as sufficient.

### Workflow 3 - Long wait escalation
1. Two reminders are released with no reply.
2. The threshold passes; the Demand Owner and LoDA Manager are alerted the same day.
3. The LoDA Manager contacts the Business Partner directly, outside the assistant.
4. A reply arrives and is filed; the wait closes.

### Workflow 4 - Questionnaire not required
1. The questionnaire is prepared.
2. The owner sees the information was already supplied and records the reason.
3. Nothing is sent; no wait or reminders; the decision is in JIRA.

### Workflow 5 - Unmatched reply
1. A colleague replies from another address without the reference.
2. It is not attached and reminders continue.
3. The owner is shown the message and links it; it is attached and the wait closes.

### Workflow 6 - Waiting review
1. The LoDA Manager reviews waiting demands ordered by days waited.
2. Past-threshold demands are distinguishable, with reminders released shown.
3. The Manager decides where to step in.

---

## 6. Edge Cases & Special Scenarios

| # | Scenario | Expected Behaviour |
|---|----------|-------------------|
| E1 | No Business Partner address | Not prepared; owner told what is missing |
| E2 | No Demand Owner yet | Not prepared until an owner is assigned |
| E3 | Send fails | Owner told; not marked sent; no wait |
| E4 | Reply before any reminder is due | Filed; no reminder ever prepared |
| E5 | Reply from a different person with the reference intact | Matched and filed |
| E6 | Reply without reference | Presented as unmatched; owner links |
| E7 | Reply is a question, not answers | Filed; wait stays open; owner decides |
| E8 | Out-of-office reply | Not an answer; reminders continue; owner may pause |
| E9 | Hard bounce | Owner told; wait paused until address fixed |
| E10 | Maximum reminders reached | No more prepared; demand stays flagged |
| E11 | Demand closed during a wait | Reminders and alerts stop immediately |
| E12 | Two replies for the same demand | Both filed; later one treated as current |
| E13 | Owner changes mid-wait | Wait continues; reminders and alerts go to new owner |
| E14 | Settings changed mid-wait | New values apply from that moment |
| E15 | Reply sent to a personal mailbox | Not seen; owner forwards or links by hand |
| E16 | Wrong content already sent | Cannot be recalled; corrected follow-up released and recorded |
| E17 | Assistant unsure whether an answer is complete | Marked for manual review |
| E18 | Weekend or holiday in the wait | Counted in working days; calendar TBD |

---

## 7. Acceptance Criteria

### 7.1 Preparation
**Given** a registered demand with an owner and Business Partner address
**When** the Demand Owner opens the demand
**Then** the standard questionnaire is prepared with the demand reference
**And** it shows no sign of automatic preparation

**Given** no Business Partner address
**When** preparation is due
**Then** it is not prepared and the owner is told what is missing

### 7.2 Release
**Given** an unreleased questionnaire
**When** any time passes
**Then** nothing is sent and no wait starts

**Given** a prepared questionnaire
**When** the owner edits and releases it
**Then** it is sent and recorded in JIRA with time, recipient and content
**And** the wait starts

**Given** a prepared questionnaire
**When** the owner records it as not required with a reason
**Then** nothing is sent and the reason is recorded

**Given** the owner releases it
**When** sending fails
**Then** the owner is told and it stays available to release

### 7.3 Reminders
**Given** a released questionnaire with no reply
**When** the reminder interval passes
**Then** a reminder is prepared and the owner is notified
**And** nothing is sent yet

**Given** a prepared reminder
**When** the owner releases or dismisses it
**Then** a release sends and records it; a dismissal sends nothing and is recorded
**And** the next reminder is prepared at the following interval

**Given** the maximum reminders have been released with no reply
**When** a further interval passes
**Then** no more are prepared and the demand stays flagged

### 7.4 Long-wait alert
**Given** the escalation threshold passes with no reply
**When** it is crossed
**Then** the Demand Owner and LoDA Manager are alerted the same day
**And** the alert is recorded in JIRA and nothing goes to the Business Partner

**Given** an alert already raised
**When** the wait continues
**Then** the same alert is not repeated daily

### 7.5 Reply filing
**Given** an open wait
**When** a completed reply arrives with the reference intact
**Then** it is attached to the JIRA ticket and reminders stop

**Given** an open wait
**When** a reply cannot be matched with confidence
**Then** it is not attached automatically and reminders continue
**And** the owner can link it by hand

**Given** an open wait
**When** an out-of-office reply arrives
**Then** it is not treated as an answer and reminders continue

**Given** an open wait
**When** the message bounces
**Then** the owner is told immediately and the wait is paused

### 7.6 Merge and gaps
**Given** two partial replies
**When** the owner opens the demand
**Then** each question is shown as answered, missing, vague or not stated, with its source reply

**Given** an answer such as "before year-end close"
**When** answers are merged
**Then** it is flagged as vague

**Given** the assistant is unsure
**When** the merged view is built
**Then** the item is marked for manual review

### 7.7 Follow-up
**Given** gaps remain
**When** the merged view is ready
**Then** one consolidated follow-up is drafted within 30 minutes
**And** it is sent only after owner approval, which starts a new wait

**Given** no gaps remain
**When** the owner confirms the questionnaire is sufficient
**Then** the decision is recorded and the demand can move to alignment

### 7.8 Visibility
**Given** open questionnaire waits
**When** the LoDA Manager reviews waiting demands
**Then** each shows Business Partner, Demand Owner, days waited and reminders released
**And** past-threshold demands are distinguishable

### 7.9 Business rules
**Given** any message prepared for a Business Partner
**When** it is shown or sent
**Then** it carries no sign it was machine-prepared

**Given** any questionnaire content
**When** it is processed by AI
**Then** only the local model is used and personal data is masked

### 7.10 Record, closure and settings
**Given** any questionnaire event
**When** it occurs
**Then** it is recorded in JIRA with a timestamp

**Given** a demand is closed during an open wait
**When** closure is recorded
**Then** reminders and alerts stop

**Given** the team agrees new timings
**When** the settings are changed
**Then** open waits use them from that moment with no product change

---

## 8. Success Metrics (Detailed)

**Functional**
- 100% of due reminders prepared.
- 100% of threshold crossings alerted the same day.
- 100% of replies attached to the correct ticket, automatic or manually linked.

**Data quality**
- 100% complete JIRA trail for the step.
- Zero replies filed on the wrong demand.
- Zero automatic replies treated as answers.

**User experience**
- One action to release the questionnaire after review.
- At least 80% of drafts approved with minor edits.
- Drafts ready in under 30 minutes.

**Business KPIs affected**
- LoDA-held time per demand: 25-30 days to 5 days or fewer.
- Manual effort per demand: about 30 hours to 8 or fewer.
- Demands per month with the same team: 10-30 to 30+.

---

## 9. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| Q1 | Reminder interval? | LoDA Manager | TBD |
| Q2 | Maximum number of reminders? | LoDA Manager | TBD |
| Q3 | Escalation threshold? | LoDA Manager | TBD |
| Q4 | Alert channel: email, Teams, overview? | LoDA Manager | Assumed email plus overview |
| Q5 | Can the assistant send from the shared mailbox? | IT | Assumed yes, on release |
| Q6 | Baselines for M5 and M6? | LoDA Manager | Pull 3 months of JIRA history |
| Q7 | Do pre-approved questionnaire and standard reminders need release? | LoDA Manager | Spec requires release; confirm |
| Q8 | Holiday calendar for working days? | LoDA Manager | TBD |
| Q9 | Can an owner pause a wait? | Demand Owner | Proposed; confirm |
| Q10 | Pilot demand? | LoDA Manager | TBD |

---

## 10. Dependencies

- **Shared DC mailbox:** send access on release; read access to detect replies.
- **JIRA Cloud:** record events and attach replies on the demand ticket.
- **Demand intake and registration:** a registered demand with a Business Partner address and an owner.
- **Standard questionnaire template and approved reminder wording.**
- **Agreed timings:** reminder interval, maximum reminders, escalation threshold.
- **Existing connectors and audit record** for JIRA, mail and documents.

---

## 11. Out of Scope

- Changing the questionnaire content.
- Any send to a Business Partner without Demand Owner release.
- Any automated decision, including whether the questionnaire is sufficient.
- Reminders for later waits (BRD/DDS, cost acceptance, SA/PO); they reuse this pattern separately.
- SAP integration.
- Any Business Partner-facing portal; the Business Partner uses email only.
- Any AI route other than the local model.
- A user interface mockup; this is a backend flow.

---

*End of Functional Specification*
