# EPIC: Questionnaire Without Chasing

**Epic ID**: EPIC-DC-2026-002
**Epic Name**: Questionnaire Without Chasing
**Domain**: DC Flow - Requirements (Questionnaire)
**Created Date**: 2026-11-13
**Priority**: High
**Status**: Draft

> Sources: `dc/context/business-context.md`. *(TBD)* = number or decision not yet available. *(to be validated)* = assumption not yet confirmed.
> This epic stands on its own. It does not build on or modify any previously drafted epic.

---

## Definition of epic

Every demand starts with the same exchange: the Demand Owner sends the standard questionnaire to the Business Partner and then waits. Today that wait is managed entirely by hand. The Demand Owner writes the email, remembers to chase, reads each reply, works out which answers are still missing or vague, writes the next follow-up, and finally files everything in JIRA. This takes about three follow-up rounds per demand and sits inside the 25-30 days LoDA holds each demand.

This epic makes the questionnaire step run without chasing, while the Demand Owner stays in control. The assistant prepares the standard questionnaire for a registered demand. The Demand Owner reviews and releases it. While the Business Partner has not answered, the assistant prepares reminders at an agreed rhythm and alerts the Demand Owner and the LoDA Manager when a wait becomes long. When replies arrive, the assistant files them on the JIRA ticket, merges the answers across replies, flags what is missing, vague or not stated, and drafts one consolidated follow-up for the Demand Owner to approve.

The principle of the whole product applies: AI prepares the evidence, people make the decisions. Nothing reaches the Business Partner without Demand Owner release, the Business Partner cannot tell whether a person or the assistant wrote the message, and all content is handled by the local model only.

Capabilities in this epic:
- Prepare and release the standard questionnaire.
- Track the wait and prepare reminders; alert on long waits.
- Detect replies, file them in JIRA, and merge answers across several replies.
- Flag gaps and prepare a single follow-up draft for approval.
- Record every step in JIRA.

---

## Who will use this?

**Primary Users**:

| Role | Responsibilities |
|------|------------------|
| Demand Owner | - Reviews and releases the questionnaire<br>- Releases or dismisses prepared reminders<br>- Reviews the merged answers and gap list<br>- Approves each follow-up before it is sent |
| LoDA Manager | - Receives the long-wait alert<br>- Steps in with the Business Partner when a wait stalls<br>- Monitors waiting demands across the pipeline |

**Secondary Users**:
- Business Partner: does not use the assistant. Receives faster, more consistent questionnaire communication and replies by email as today.
- Tech Architect / TPO: indirect. Receives a better-completed questionnaire when the demand reaches alignment.
- LoDA leadership: indirect. Gets a complete JIRA trail of the questionnaire step to prove timing before and after.

---

## What does it need to accomplish?

**Business Objectives**:
1. Cut questionnaire follow-up rounds from about 3 to 1.5 or fewer per demand.
2. Make sure no questionnaire wait goes unseen: every long wait alerts the Demand Owner and LoDA Manager the same day it crosses the threshold.
3. Turn the questionnaire step into a review-and-release action: each AI draft ready in under 30 minutes, with at least 80% approved with only minor edits.
4. Record 100% of questionnaire steps in JIRA (send, reminders, alerts, replies, gaps, decisions).
5. Contribute to the overall target of at most 8 hours manual effort and at most 5 days LoDA-held time per demand.

**User Outcomes**:
1. The Demand Owner releases the questionnaire with one action instead of writing and sending it.
2. The Demand Owner never has to remember to chase; a ready reminder is waiting when one is due.
3. The Demand Owner sees one merged view of what the Business Partner has answered and what is still missing, instead of re-reading every reply.
4. The LoDA Manager hears about a stalled questionnaire the day it stalls.

---

## Why is it important to be done?

**Business Impact**:

1. **Capacity without headcount**: The questionnaire is the first wait of every demand. Removing the write-chase-file work from every demand helps move the team from 10-30 to 30+ demands a month with the same people.

2. **Shorter demand cycle**: Demands take 2-3 months end to end, of which 25-30 days are LoDA-held time. Every day lost at the first wait is lost for the whole demand. Fewer follow-up rounds directly shortens it.

3. **Consistent Business Partner experience**: Today the speed and tone of chasing depend on which Demand Owner handles the demand. Templates and drafts from one source make communication consistent.

4. **A trustworthy JIRA trail**: JIRA timestamps are incomplete today, so LoDA cannot prove how long it holds a demand. Recording every questionnaire event builds the baseline needed to prove the before/after case.

**Real-World Scenario**:

Market Scenario - Sabine's invoice archive demand (Finance Operations):
- Sabine asks LoDA to archive about 4 million supplier invoices. The demand is registered and owned.
- The Demand Owner sends the questionnaire, then moves to other demands.
- Sabine's first reply covers part of it. Access roles and data classification are missing; "before year-end close" is vague; SAP company codes and cost centre are not stated.
- The Demand Owner is busy; the follow-up goes out a week late, and the second reply fixes only some gaps. A third round is needed.
- Nobody outside the Demand Owner knows the demand has been waiting for three weeks.
- With this epic, the follow-up is drafted the same day with all gaps listed together, the LoDA Manager sees the wait once it passes the threshold, and the demand reaches the alignment call a round sooner.

**Without This Epic**:
- About three follow-up rounds per demand continue, each written by hand.
- Stalled questionnaires stay invisible until someone happens to ask.
- Demand Owners keep personal spreadsheets and reminders to track dozens of waits.
- JIRA stays incomplete, so the time LoDA holds a demand cannot be measured.

**With This Epic**:
- Reminders and follow-ups are prepared and waiting for release.
- Long waits alert the LoDA Manager automatically.
- The Demand Owner works from a merged answer and gap view.
- The JIRA record of the step is complete.
- The release-and-remind pattern is proven for the later waits in the process.

---

## Pain points

**Current Challenges**:

1. **Manual chasing**
   - The Demand Owner decides when to chase and writes each message from scratch.
   - Follow-up speed depends on the owner's workload and memory.
   - Affects every demand.

2. **Invisible waits**
   - No list of open questionnaire waits exists; owners track them in spreadsheets and reminders.
   - The LoDA Manager and leadership cannot see how long a Business Partner has been silent.
   - Escalation comes late or not at all.

3. **Repeated rounds on the same gaps**
   - Replies arrive piecemeal; gaps are found one reply at a time.
   - About three follow-up rounds per demand.
   - Business Partners are asked several times for related information.

4. **Manual merging of answers**
   - The Demand Owner reads every reply to work out what is now answered.
   - Easy to miss vague answers such as "before year-end close".
   - Re-work on every demand.

5. **Incomplete JIRA trail**
   - Updates are made late or skipped.
   - Time LoDA holds a demand cannot be proven.
   - Weakens any before/after business case.

6. **Inconsistent communication**
   - Tone, timing and content differ between Demand Owners.
   - Business Partners experience slow and uneven follow-up.
   - Reflects on LoDA as a team.

---

## Bright points

**Opportunities & Strengths**:

1. **Fixed process and standard template**
   - The questionnaire is standard and the process is well defined and not being redesigned.
   - Preparation can start from approved content with little ambiguity.

2. **JIRA is already the system of record**
   - Every questionnaire event has a natural home on the demand ticket.
   - No new source of truth is needed.

3. **Existing building blocks**
   - JIRA, mail and document connectors and an audit record of every external interaction already exist.
   - Document parsing already exists for received attachments.

4. **Pre-approved communication**
   - The questionnaire template and standard reminders are already agreed content.
   - Human release stays in place, so risk to the Business Partner relationship is low.

5. **Reusable pattern**
   - The prepare-release-remind-alert-file cycle repeats for the BRD/DDS, cost acceptance and SA/PO waits.
   - Proving it once saves rebuilding it later.

---

## Current State

**System Behavior**:
- The questionnaire is sent by hand from the Demand Owner's mailbox or the shared DC mailbox.
- Nothing tracks the wait or prompts a follow-up.
- **Gap**: no reminder, no alert, no merged view of answers.
- Impact: waits run long and rounds repeat.
- Workaround: personal spreadsheets, calendar reminders and re-reading email threads.

**Configuration/UI State**:
- JIRA holds the demand ticket; updates are typed in by the Demand Owner.
- No view shows which demands are waiting on a Business Partner or for how long.

**Data Flow** (current):
```
Demand registered -> Demand Owner writes and sends questionnaire
    |
Business Partner replies (some answers) or stays silent
    |
If silent:
    -> Owner may or may not remember to chase
If partial reply:
    -> Owner reads reply, spots gaps, writes follow-up (round 2, 3 ...)
    |
Owner files reply and updates JIRA by hand (often late)
```

**User Workflow** (current manual process):
1. Write and send the questionnaire (about 20-30 min, TBD)
2. Track the wait and chase when remembered (ongoing, TBD)
3. Read each reply and compare against the questions (about 30 min per reply, TBD)
4. Write the follow-up (about 20 min per round, TBD)
5. Save replies and update JIRA (about 15 min, TBD)

**Duration**: Questionnaire stage elapsed time TBD (to be measured from historical JIRA data), risk high: waits go unnoticed.

**Challenges with Current State**:
- Effort is hidden inside the roughly 30 hours per demand.
- Elapsed time cannot be measured reliably.
- Quality of follow-up varies by owner.

---

## Target State

**System Behavior** (after epic implementation):

1. **Questionnaire preparation and release**
   - For a registered demand with an owner, the standard questionnaire is prepared and addressed to the Business Partner on the demand.
   - It carries the demand reference and no sign it was prepared by the assistant.
   - The Demand Owner edits if needed and releases with one action.
   - The send is recorded in JIRA with time, recipient and content.
   - Nothing is sent without release.

2. **Wait and reminder flow**
   ```
   Questionnaire released
       |
   Wait starts (counted in working days)
       |
   Reminder interval passes, no reply
       |
   Reminder prepared -> Demand Owner releases or dismisses
       |
   Repeat up to the maximum number of reminders
       |
   Escalation threshold passes, no reply
       |
   Alert to Demand Owner and LoDA Manager
   ```

3. **Reply handling and gap analysis**

   **Replies**:
   - Detected in the shared mailbox and matched to the demand.
   - Attached to the JIRA ticket; reminders stop when a completed questionnaire is received.
   - Automatic replies (out of office) are not treated as answers.

   **Answers**:
   - Merged across all replies into one view of the questionnaire.
   - Each question marked answered, missing, vague or not stated.
   - Where the assistant is unsure, the item is left for manual review.

4. **Error Handling**

   - **Unmatched reply** (different sender, missing reference):
     - Not attached automatically; reminders continue.
     - Shown to the Demand Owner as an unmatched item.
     - Owner links it by hand.

   - **Send failure or bounce** (address invalid, mail unavailable):
     - Demand Owner told immediately.
     - Not marked as sent; wait paused until fixed.

   - **Partial or vague answer**:
     - Flagged in the gap list, never silently accepted.

5. **Progress Monitoring**
   ```
   Waiting overview for LoDA Manager
       |
   Each waiting demand shows:
   - Business Partner and Demand Owner
   - Days waited (working days)
   - Reminders released
   - Past-threshold flag
   ```

6. **Follow-up flow**
   ```
   Reply received -> Answers merged -> Gaps flagged
       |
   One consolidated follow-up drafted (under 30 minutes)
       |
   Demand Owner edits and approves -> Sent -> New wait starts
       |
   Repeat until the questionnaire is complete
   ```

7. **User Workflow** (new streamlined process):
   1. Review and release the questionnaire (about 5 min)
   2. Release due reminders as prompted (about 2 min each)
   3. Review merged answers and gap list (about 10 min)
   4. Approve the consolidated follow-up (about 5 min)
   5. Record that the questionnaire is sufficient and move to alignment (about 2 min)

   **Duration**: Targets TBD, set against the measured baseline. Risk low: every outbound message is reviewed.

**Improvements Over Current State**:
- Follow-up rounds from about 3 to 1.5 or fewer.
- AI drafts ready in under 30 minutes.
- Long waits visible the same day instead of unseen.
- JIRA trail for the step from partial to 100%.

---

## Acceptance Criteria

### AC1: Questionnaire preparation

**Given** a demand is registered in JIRA with a Demand Owner and a Business Partner address
**When** the Demand Owner opens the demand
**Then** the standard questionnaire is already prepared for that Business Partner
**And** it carries the demand reference and no indication it was prepared automatically

**Given** a registered demand has no Business Partner address
**When** the questionnaire is due to be prepared
**Then** it is not prepared
**And** the Demand Owner is told what is missing and preparation continues once supplied

---

### AC2: Release control

**Given** a prepared, unreleased questionnaire
**When** any amount of time passes
**Then** nothing is sent to the Business Partner
**And** no wait begins

**Given** a prepared questionnaire
**When** the Demand Owner edits and releases it
**Then** the edited version is sent
**And** the send is recorded in JIRA with time, recipient and content
**And** the wait begins

**Given** the Business Partner already supplied the information
**When** the Demand Owner records that the questionnaire is not required, with a reason
**Then** nothing is sent
**And** the reason is recorded in JIRA and no reminders are prepared

**Given** the Demand Owner releases the questionnaire
**When** sending fails
**Then** the Demand Owner is told, the demand is not marked as sent, and the questionnaire stays available to release

---

### AC3: Reminders

**Given** a released questionnaire with no reply
**When** the reminder interval passes
**Then** a reminder is prepared and the Demand Owner is notified
**And** nothing has been sent yet

**Given** a prepared reminder
**When** the Demand Owner releases it
**Then** it is sent and recorded in JIRA
**And** the next reminder is scheduled one interval later

**Given** a prepared reminder
**When** the Demand Owner dismisses it
**Then** nothing is sent and the dismissal is recorded
**And** the next reminder is still prepared at the following interval

**Given** the maximum number of reminders has been released with no reply
**When** a further interval passes
**Then** no more reminders are prepared
**And** the demand stays flagged in the waiting overview

---

### AC4: Long-wait alert

**Given** a questionnaire wait passes the escalation threshold with no reply
**When** the threshold is crossed
**Then** the Demand Owner and the LoDA Manager are alerted the same day
**And** the alert names the demand, Business Partner, days waited and reminders released
**And** the alert is recorded in JIRA and nothing is sent to the Business Partner

**Given** an alert has been raised
**When** the wait continues
**Then** the same alert is not repeated every day

---

### AC5: Reply filing

**Given** an open questionnaire wait
**When** the Business Partner replies with the completed questionnaire and the demand reference intact
**Then** the reply and attachment are attached to the JIRA ticket
**And** receipt is recorded and reminders stop

**Given** an open questionnaire wait
**When** a reply arrives that cannot be matched to a demand with confidence
**Then** nothing is attached automatically and reminders continue
**And** the Demand Owner is shown the message and can link it by hand

**Given** an open questionnaire wait
**When** an out-of-office reply arrives
**Then** it is not treated as an answer and reminders continue

---

### AC6: Merged answers and gaps

**Given** the Business Partner has sent two partial replies
**When** the Demand Owner opens the demand
**Then** one merged view shows each question as answered, missing, vague or not stated
**And** each entry points back to the reply it came from

**Given** an answer such as "before year-end close"
**When** answers are merged
**Then** it is flagged as vague rather than accepted as a date

**Given** the assistant cannot tell whether a question is answered
**When** the merged view is built
**Then** the item is marked for manual review

---

### AC7: Follow-up draft

**Given** gaps remain after a reply
**When** the merged view is complete
**Then** one consolidated follow-up covering all gaps is drafted within 30 minutes
**And** nothing is sent until the Demand Owner approves it

**Given** the Demand Owner approves the follow-up
**When** it is sent
**Then** it is recorded in JIRA and a new wait begins

**Given** no gaps remain
**When** the Demand Owner confirms the questionnaire is sufficient
**Then** the decision is recorded in JIRA and the demand can move to alignment

---

### AC8: Waiting visibility

**Given** demands with open questionnaire waits
**When** the LoDA Manager opens the waiting overview
**Then** each demand shows Business Partner, Demand Owner, days waited and reminders released
**And** the list can be ordered by days waited and past-threshold demands are distinguishable

---

### AC9: Business rules

**Given** any message prepared for a Business Partner
**When** it is shown or sent
**Then** it carries no label or sign that it was machine-prepared

**Given** any questionnaire content, including personal data such as names and emails
**When** it is processed by AI
**Then** it is handled by the local model only, with personal data masked

---

### AC10: JIRA record and closure

**Given** any questionnaire event (send, reminder, dismissal, alert, reply, gap list, follow-up, decision)
**When** it happens
**Then** it is recorded in the demand's JIRA ticket with a timestamp

**Given** a demand is closed during an open wait
**When** the closure is recorded
**Then** reminders and alerts stop immediately and the demand leaves the waiting overview

---

## Test cases (attach test data as well)

### Test Case 1: Happy path - answer after one reminder

**Preconditions**:
- Demand DEM-TEST-001 registered, owner assigned, address on file
- Reminder interval and escalation threshold configured

**Test Data**:
- Business Partner: Sabine Krueger, Finance Operations (test address)
- Reply with a fully completed questionnaire

**Test Steps**:
1. Open the demand and review the prepared questionnaire
2. Release it
3. Let the reminder interval pass; release the prepared reminder
4. Send the completed reply to the shared mailbox
5. Check the JIRA ticket

**Expected Result**:
- Send, reminder and reply all recorded in JIRA
- Reminders stop; demand leaves the waiting overview
- Drafts were ready in under 30 minutes

**Test Owner**: QA Team - DC Flow

---

### Test Case 2: Nothing sent without release

**Preconditions**:
- Prepared questionnaire for DEM-TEST-002, not released

**Test Data**:
- Test mailbox watching for outbound mail

**Test Steps**:
1. Leave the questionnaire unreleased past two reminder intervals
2. Check the test mailbox

**Expected Result**:
- No message received by the Business Partner
- No wait started; reminders remain internal drafts

**Test Owner**: QA Team - DC Flow

---

### Test Case 3: Long-wait alert

**Preconditions**:
- Released questionnaire, two reminders released, no reply

**Test Data**:
- Demand DEM-TEST-003; LoDA Manager test account

**Test Steps**:
1. Advance time past the escalation threshold
2. Check Demand Owner and LoDA Manager notifications
3. Advance one more day

**Expected Result**:
- Both alerted the same day with demand, partner, days waited and reminders released
- Alert recorded in JIRA; not repeated the next day
- Nothing sent to the Business Partner

**Test Owner**: QA Team - DC Flow

---

### Test Case 4: Merging partial replies and flagging gaps

**Preconditions**:
- Released questionnaire for DEM-TEST-004

**Test Data**:
- Reply 1: access roles and data classification missing; "before year-end close" given as the deadline; company codes and cost centre not stated
- Reply 2: supplies access roles only

**Test Steps**:
1. Send reply 1; open the merged view
2. Send reply 2; reopen the merged view
3. Open the follow-up draft

**Expected Result**:
- After reply 1: access roles, data classification missing; deadline vague; company codes, cost centre not stated
- After reply 2: access roles answered; remaining items still flagged
- One follow-up lists only the remaining gaps

**Test Owner**: QA Team - DC Flow

---

### Test Case 5: Unmatched reply

**Preconditions**:
- Open wait on DEM-TEST-005

**Test Data**:
- Reply from a colleague's address with no demand reference

**Test Steps**:
1. Send the reply to the shared mailbox
2. Check the JIRA ticket and the Demand Owner's view
3. Link the message by hand

**Expected Result**:
- Not attached automatically; reminders continue
- Shown as unmatched; after linking it is attached and the wait closes

**Test Owner**: QA Team - DC Flow

---

### Test Case 6: Out-of-office reply

**Preconditions**:
- Open wait on DEM-TEST-006

**Test Data**:
- Automatic out-of-office message from the Business Partner

**Test Steps**:
1. Send the automatic reply
2. Let the next reminder interval pass

**Expected Result**:
- Not treated as an answer; wait stays open
- Reminder is still prepared; out-of-office visible to the owner

**Test Owner**: QA Team - DC Flow

---

### Test Case 7: Send failure and invalid address

**Preconditions**:
- Demand DEM-TEST-007 with an address that bounces

**Test Data**:
- Non-existent address

**Test Steps**:
1. Release the questionnaire
2. Observe the Demand Owner's notification
3. Correct the address and release again

**Expected Result**:
- Owner told immediately; no wait started or reminders prepared while invalid
- After correction the send succeeds and the wait starts

**Test Owner**: QA Team - DC Flow

---

### Test Case 8: Demand closed during a wait

**Preconditions**:
- Open wait with one reminder prepared on DEM-TEST-008

**Test Data**:
- Closure reason: not_accepted

**Test Steps**:
1. Close the demand with the reason
2. Let the next interval and the threshold pass

**Expected Result**:
- No further reminders or alerts; demand leaves the overview
- Closure reason recorded in JIRA

**Test Owner**: QA Team - DC Flow

---

### Test Case 9: Dismissed reminder and maximum reminders

**Preconditions**:
- Maximum reminders set to 3 (test value)

**Test Data**:
- Demand DEM-TEST-009, no reply throughout

**Test Steps**:
1. Dismiss the first reminder
2. Release the second and third
3. Let a further interval pass

**Expected Result**:
- Dismissal recorded; next reminder still prepared
- No fourth reminder; demand stays flagged in the overview

**Test Owner**: QA Team - DC Flow

---

### Test Case 10: Volume and concurrent waits

**Preconditions**:
- 30 demands with open questionnaire waits, owned by 5 Demand Owners

**Test Data**:
- Mix of replies, silent partners, and past-threshold demands

**Test Steps**:
1. Let intervals pass for all demands at once
2. Send replies to a third of the demands during the run
3. Open the waiting overview as LoDA Manager

**Expected Result**:
- Every due reminder is prepared once per owner; none duplicated or missed
- Replies match the right demands; overview figures are correct
- Drafts ready within 30 minutes

**Test Owner**: QA Team - DC Flow

---

### Test Case 11: Local-model and masking rule

**Preconditions**:
- Questionnaire reply containing names and email addresses

**Test Data**:
- Reply with personal data

**Test Steps**:
1. Process the reply into the merged view
2. Review the audit record

**Expected Result**:
- Personal data masked before AI use; only the local model used
- No external AI route appears in the audit record

**Test Owner**: QA Team - DC Flow with InfoSec

---

## Risks

### High Risks

| Risk ID | Risk Description | Impact | Probability | Mitigation Strategy |
|---------|------------------|--------|-------------|---------------------|
| R1 | **Wrong message reaches a Business Partner** | High - damages LoDA's relationship and trust | Low | - Nothing sent without Demand Owner release<br>- Drafts always editable and reviewed<br>- Pilot on one live demand first |
| R2 | **No reliable baseline to prove improvement** | High - benefit cannot be demonstrated | High | - Pull 3 months of historical JIRA data before go-live<br>- Record every questionnaire event from day one |
| R3 | **Reply matched to the wrong demand** | High - answers filed on the wrong ticket | Medium | - Match only on confident evidence<br>- Show unmatched items to the owner<br>- Owner can always re-link |
| R4 | **Business Partner can tell the message is automated** | High - breaks the agreed experience | Low | - No labels or tell-tale wording<br>- Owner edits before release |

### Medium Risks

| Risk ID | Risk Description | Impact | Probability | Mitigation Strategy |
|---------|------------------|--------|-------------|---------------------|
| R5 | **Reminder timings not agreed** | Medium - reminders too early annoy partners, too late waste time | High | - Agree interval, maximum and threshold with the LoDA Manager before the pilot<br>- Make them adjustable |
| R6 | **Drafts need heavy editing** | Medium - owners lose trust and the 80% minor-edit target is missed | Medium | - Track edit rate<br>- Refine the template and drafting from owner feedback |
| R7 | **Vague answers missed or wrongly flagged** | Medium - extra rounds or false alarms | Medium | - Mark unsure items for manual review<br>- Review flagged items in the pilot |
| R8 | **Replies sent to personal mailboxes** | Medium - assistant never sees them | Medium | - Ask owners to forward to the shared mailbox<br>- Allow manual linking |

### Low Risks

| Risk ID | Risk Description | Impact | Probability | Mitigation Strategy |
|---------|------------------|--------|-------------|---------------------|
| R9 | **Alert fatigue** | Low - alerts get ignored | Medium | - One alert per threshold crossing<br>- Tune thresholds after the pilot |
| R10 | **Holiday periods distort wait counts** | Low - early or late reminders | Medium | - Count working days<br>- Allow owners to pause a wait |
| R11 | **Owner handover mid-wait** | Low - reminders go to the wrong person | Low | - Reminders and alerts follow the current owner |

---

## Additional Information

### Success Criteria

**Business Success Metrics**:
1. Questionnaire follow-up rounds from about 3 to 1.5 or fewer per demand.
2. 100% of long waits alerted to the Demand Owner and LoDA Manager the same day.
3. At least 80% of AI drafts approved with only minor edits; each draft ready in under 30 minutes.
4. 100% of questionnaire steps recorded in JIRA.
5. Questionnaire elapsed time and Demand Owner effort reduced against a baseline measured from 3 months of JIRA history *(target TBD)*.

### Dependencies

**External Systems**:
- Shared DC mailbox: send access to issue questionnaire and reminders; read access to detect replies.
- JIRA Cloud: record events and attach replies on the demand ticket.

**Internal Dependencies**:
- Demand intake and registration: a registered demand with a Business Partner address and an assigned Demand Owner.
- Standard questionnaire template and approved reminder wording from the team.
- Agreed reminder interval, maximum reminders and escalation threshold *(TBD, LoDA Manager)*.
- Existing JIRA, mail and document connectors and audit record.

### Timeline Estimate

**Estimated Duration**: TBD *(to be sized with the team; indicative phases below)*

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| **Requirements & Design** | TBD | - Agree reminder and escalation timings<br>- Confirm questionnaire template and baseline plan |
| **Development** | TBD | - Release, reminders, alerts, reply filing<br>- Answer merge and gap flags |
| **Testing & QA** | TBD | - Run the test cases above<br>- InfoSec check of local-model rule |
| **Deployment & Rollout** | TBD | - Pilot with one live demand<br>- Review metrics, tune, then widen |

---

**Epic Status**: Ready for Review
**Next Steps**: Review with the LoDA Manager; agree reminder and escalation timings; decide whether to produce the functional spec and a UI mockup.

**Open Questions**:
1. Reminder interval, maximum reminders and escalation threshold? *(TBD, LoDA Manager)*
2. How are alerts delivered: email, Teams or the overview? *(assumed email plus overview, to be validated)*
3. Can the assistant send from the shared mailbox, or does the Demand Owner copy the text? *(assumed sent on release, to be validated with IT)*
4. Business rules allow pre-approved questionnaires and standard reminders to go without approval; this epic requires release for all of them to be safe. Confirm.
5. Which live demand is the pilot? *(TBD)*

---

*End of Epic Document*
