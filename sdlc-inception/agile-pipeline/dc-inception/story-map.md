# LoDA Demand Assistant – User Story Map

> Status: Draft | Version 0.1 | 2026-11-13. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `to-be-journey.md`, `service-blueprint.md`, `product-vision.md`.

## 1. Backbone

Activities and steps from the to-be journey, left to right. P-01 = Demand Owner, P-02 = Demand Manager, P-03 = Technical Reviewer.

| Activity | Step | Persona |
|----------|------|---------|
| 1. Intake | T-01 See new demand in mailbox · T-02 Demand registered · T-03 Owner assigned | P-01 · P-01 · P-02 |
| 2. Questionnaire | T-04 Release questionnaire · T-05 Wait with reminders · T-06 Review answers | P-01 |
| 3. Alignment | T-07 Alignment meeting · T-08 ◇ LoDA fit · T-09 ◇ Complexity | P-01 · P-01 · P-03/P-02 |
| 4. Requirements | T-10 Requirement meetings · T-11 Indicative cost · T-12 Wait for BRD/DDS | P-01 |
| 5. Tech approval | T-13 Feasibility · T-14 ◇ TPO approval · T-15 Baseline | P-03 · P-03 · P-01 |
| 6. Cost | T-16 Send cost package · T-17 ◇ Wait for cost acceptance | P-01 |
| 7. Handover | T-18 Handover · T-19 SAP data · T-20 Issue SA · T-21 ◇ Wait for SA/PO · T-22 Notify and complete | P-01 |
| Cross-cutting | T-23 Close / reopen · T-24 Demand overview | P-01 · P-02 |

## 2. Map

Cards under each step. Release lines cut across all steps. *(m)* = manual in this release: the step works as today, and the result is recorded in JIRA by hand.

| Step | MVP – "Nothing waits unseen" | Release 2 – "Less re-typing" | Release 3 – "Clear ownership & consults" | Later – "Evidence" |
|------|------------------------------|------------------------------|-------------------------------------------|--------------------|
| T-01 | S-01 See new demand from the DC mailbox; S-02 Forward a demand received elsewhere *(m)* | – | – | – |
| T-02 | S-03 Get the demand registered in JIRA | S-04 See key facts extracted into the ticket | – | – |
| T-03 | S-05 Assign the Demand Owner *(m)* | – | S-06 Confirm a suggested owner | – |
| T-04 | S-07 Release the prepared questionnaire | – | – | – |
| T-05 | S-08 Release a prepared reminder; S-09 Get alerted on a long wait; S-10 See the reply attached in JIRA | – | – | – |
| T-06 | S-12 Review the questionnaire *(m)* | S-11 Review the summary with gaps flagged | – | – |
| T-07 | S-13 Run the meeting and issue minutes, BRD/DDS *(m)* | S-14 Review drafted minutes; S-15 Review drafted BRD/DDS updates | – | S-16 Get a meeting brief |
| T-08 | S-17 Record the LoDA fit decision *(m)* | – | S-18 Send a consult request to product owners | S-19 See similar past demands |
| T-09 | S-20 Record the complexity confirmation *(m)* | – | S-21 Send a consult request with context | – |
| T-10 | S-22 Run requirement meetings and issue BRD/DDS *(m)* | S-23 Review drafted minutes and BRD/DDS | – | – |
| T-11 | S-24 Share an indicative cost *(m)* | – | – | S-25 Get an estimate drafted from past demands |
| T-12 | S-26 Release BRD/DDS reminders | S-27 Review the completeness check with a follow-up ready | – | – |
| T-13 | S-28 Assess feasibility with the Product Team *(m)* | – | – | S-29 Get a feasibility evidence pack |
| T-14 | S-30 Record the TPO approval *(m)* | – | – | S-31 See an evidence and risk summary |
| T-15 | S-32 Baseline the BRD/DDS *(m)* | S-33 Get the baseline recorded automatically | – | – |
| T-16 | S-34 Send the cost package *(m)* | S-35 Get the cost package assembled | – | S-36 Get the cost drafted from past demands |
| T-17 | S-37 Release cost-acceptance reminders | S-38 Get the cost answer detected and recorded | – | – |
| T-18 | S-39 Hand over to the Product Team *(m)* | S-40 Get a handover package prepared | – | – |
| T-19 | S-41 Enter the SAP data *(m)* | – | – | S-42 Get the SAP data prepared |
| T-20 | S-43 Issue the Service Agreement *(m)* | S-44 Review a drafted Service Agreement | – | – |
| T-21 | S-45 Release SA/PO reminders | S-46 Confirm the SA/PO detected in the mailbox | – | – |
| T-22 | S-47 Notify the Product Team and complete *(m)* | S-48 Get the completion done automatically | – | – |
| T-23 | S-49 Close a demand with a reason *(m)* | S-50 Release a drafted closure note | S-51 Reopen a closed demand | – |
| T-24 | S-52 See the demands waiting on the Business Partner, and for how long | – | S-53 See all demands with owner and status | – |

## 3. Card List

| Card ID | Card (verb + object) | Step | Persona | Path | Capability | Release | Manual? |
|---------|----------------------|------|---------|------|------------|---------|---------|
| S-01 | See new demand from the DC mailbox | T-01 | P-01 | Basic | C-01 | MVP | No |
| S-02 | Forward a demand received elsewhere | T-01 | P-01/P-02 | Variation | C-01 | MVP | Yes |
| S-03 | Get the demand registered in JIRA | T-02 | P-01 | Basic | C-01, C-04 | MVP | No |
| S-04 | See key facts extracted into the ticket | T-02 | P-01 | Basic | C-01 | R2 | No |
| S-05 | Assign the Demand Owner | T-03 | P-02 | Basic | C-01 | MVP | Yes |
| S-06 | Confirm a suggested owner | T-03 | P-02 | Basic | C-01 | R3 | No |
| S-07 | Release the prepared questionnaire | T-04 | P-01 | Basic | C-03, C-04 | MVP | No |
| S-08 | Release a prepared reminder | T-05 | P-01 | Basic | C-02 | MVP | No |
| S-09 | Get alerted on a long wait | T-05 | P-01/P-02 | Exception | C-02 | MVP | No |
| S-10 | See the reply attached in JIRA | T-05 | P-01 | Basic | C-02, C-04 | MVP | No |
| S-11 | Review the summary with gaps flagged | T-06 | P-01 | Basic | C-03 | R2 | No |
| S-12 | Review the questionnaire | T-06 | P-01 | Basic | C-03 | MVP | Yes |
| S-13 | Run the meeting and issue minutes, BRD/DDS | T-07 | P-01 | Basic | C-03 | MVP | Yes |
| S-14 | Review drafted minutes | T-07 | P-01 | Basic | C-03 | R2 | No |
| S-15 | Review drafted BRD/DDS updates | T-07 | P-01 | Basic | C-03 | R2 | No |
| S-16 | Get a meeting brief | T-07 | P-01 | Variation | C-03 | Later | No |
| S-17 | Record the LoDA fit decision | T-08 | P-01 | Basic | C-04 | MVP | Yes |
| S-18 | Send a consult request to product owners | T-08 | P-01 | Variation | C-06 | R3 | No |
| S-19 | See similar past demands | T-08 | P-01 | Basic | C-05 | Later | No |
| S-20 | Record the complexity confirmation | T-09 | P-03/P-02 | Basic | C-04 | MVP | Yes |
| S-21 | Send a consult request with context | T-09 | P-01 | Basic | C-06 | R3 | No |
| S-22 | Run requirement meetings and issue BRD/DDS | T-10 | P-01 | Basic | C-03 | MVP | Yes |
| S-23 | Review drafted minutes and BRD/DDS | T-10 | P-01 | Basic | C-03 | R2 | No |
| S-24 | Share an indicative cost | T-11 | P-01 | Variation | C-03 | MVP | Yes |
| S-25 | Get an estimate drafted from past demands | T-11 | P-01 | Variation | C-05 | Later | No |
| S-26 | Release BRD/DDS reminders | T-12 | P-01 | Basic | C-02 | MVP | No |
| S-27 | Review the completeness check with a follow-up ready | T-12 | P-01 | Basic | C-03 | R2 | No |
| S-28 | Assess feasibility with the Product Team | T-13 | P-03 | Basic | C-04 | MVP | Yes |
| S-29 | Get a feasibility evidence pack | T-13 | P-03 | Basic | C-05 | Later | No |
| S-30 | Record the TPO approval | T-14 | P-03 | Basic | C-04 | MVP | Yes |
| S-31 | See an evidence and risk summary | T-14 | P-03 | Basic | C-05 | Later | No |
| S-32 | Baseline the BRD/DDS | T-15 | P-01 | Basic | C-04 | MVP | Yes |
| S-33 | Get the baseline recorded automatically | T-15 | P-01 | Basic | C-04 | R2 | No |
| S-34 | Send the cost package | T-16 | P-01 | Basic | C-03 | MVP | Yes |
| S-35 | Get the cost package assembled | T-16 | P-01 | Basic | C-03 | R2 | No |
| S-36 | Get the cost drafted from past demands | T-16 | P-01 | Basic | C-05 | Later | No |
| S-37 | Release cost-acceptance reminders | T-17 | P-01 | Basic | C-02 | MVP | No |
| S-38 | Get the cost answer detected and recorded | T-17 | P-01 | Basic | C-04 | R2 | No |
| S-39 | Hand over to the Product Team | T-18 | P-01 | Basic | C-04 | MVP | Yes |
| S-40 | Get a handover package prepared | T-18 | P-01 | Basic | C-03 | R2 | No |
| S-41 | Enter the SAP data | T-19 | P-01 | Basic | C-03 | MVP | Yes |
| S-42 | Get the SAP data prepared | T-19 | P-01 | Basic | C-03 | Later | No |
| S-43 | Issue the Service Agreement | T-20 | P-01 | Basic | C-03 | MVP | Yes |
| S-44 | Review a drafted Service Agreement | T-20 | P-01 | Basic | C-03 | R2 | No |
| S-45 | Release SA/PO reminders | T-21 | P-01 | Basic | C-02 | MVP | No |
| S-46 | Confirm the SA/PO detected in the mailbox | T-21 | P-01 | Basic | C-02, C-04 | R2 | No |
| S-47 | Notify the Product Team and complete | T-22 | P-01 | Basic | C-04 | MVP | Yes |
| S-48 | Get the completion done automatically | T-22 | P-01 | Basic | C-04 | R2 | No |
| S-49 | Close a demand with a reason | T-23 | P-01 | Exception | C-07 | MVP | Yes |
| S-50 | Release a drafted closure note | T-23 | P-01 | Exception | C-07 | R2 | No |
| S-51 | Reopen a closed demand | T-23 | P-01 | Exception | C-07 | R3 | No |
| S-52 | See the demands waiting on the Business Partner, and for how long | T-24 | P-02 | Basic | C-02, C-06 | MVP | No |
| S-53 | See all demands with owner and status | T-24 | P-02 | Basic | C-06 | R3 | No |

## 4. Constraints (cross-cutting, not cards)

| Constraint | Applies to | Source |
|------------|-----------|--------|
| Nothing is sent to the Business Partner without Demand Owner release | T-04, T-05, T-12, T-16, T-17, T-20, T-21, T-23 | Vision §5.2; T 2:08:24 |
| JIRA records every step, decision and document link | All | PDF |
| No AI labelling towards the Business Partner; internal labelling only | All AI output | T 1:51:54 |
| When the AI is unsure, the step falls back to manual | All AI output | T 1:50:27 |
| Past-demand evidence only from new demands, after the threshold | S-19, S-25, S-29, S-31, S-36 | T 1:50:52, 1:51:19 |
| On-premise hosting; JIRA Cloud; no login in the MVP | All | context §5 |
| Single intake through the shared DC mailbox | T-01 | T 1:53:31 |

## 5. Open Questions

1. Reminder and escalation timings for S-08, S-09, S-26, S-37, S-45. *(TBD at story level)*
2. Can the MVP send emails from the shared mailbox, or does the Demand Owner copy the prepared text? *(assumed: sent on release – to be validated with IT)*
