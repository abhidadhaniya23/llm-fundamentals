# LoDA Demand Assistant – Release Plan

> Status: Draft | Version 0.1 | 2026-11-13. *(to be validated)* = assumption, not yet confirmed. No dates or estimates: none were given.
>
> Sources: `story-map.md`, `product-vision.md`, `problem-statement.md`.

## 1. MVP Definition – "Nothing waits unseen"

- **Goal:** Demands reach a decision faster because no wait on the Business Partner goes unnoticed (G-01). Waiting demands are visible to the Demand Manager (G-03).
- **Learning goal:**
  - Do prepared reminders and escalation shorten the 4 waits?
  - Will Demand Owners use a release-before-send flow?
  - Does mailbox intake catch every demand?
- **What users can do:** A demand arriving in the DC mailbox is registered in JIRA automatically. The Demand Owner releases the questionnaire and reminders at every wait (questionnaire, BRD/DDS, cost acceptance, SA/PO), and replies are attached to the ticket. Long waits alert the Demand Owner and the Demand Manager, and the Demand Manager sees every demand that is waiting on the Business Partner. All other steps work as today and are recorded in JIRA by hand, so a demand can still run from intake to "Product Team notified".
- **Included cards:**
  - Automated: S-01, S-03, S-07, S-08, S-09, S-10, S-26, S-37, S-45, S-52
  - Manual: S-02, S-05, S-12, S-13, S-17, S-20, S-22, S-24, S-28, S-30, S-32, S-34, S-39, S-41, S-43, S-47, S-49
- **Manual in the MVP:** owner assignment, the meetings and documents, all decisions, baseline, cost package, handover, SAP, SA, completion, closure.
- **Explicitly not in the MVP:**
  - AI drafting
  - extracted facts
  - consult requests
  - past-demand evidence
  - closure notes and reopening
  - the full dashboard
  - login and roles
- **Pilot:** one live demand *(T 1:59:57)*.
- **Success criteria:**
  - Elapsed time spent waiting on the Business Partner (TBD)
  - Share of reminders released from the product (TBD)
  - No demand missed at intake (TBD)

## 2. Releases

| Release | Goal (G-IDs) | What users can do afterwards | Cards (S-IDs) | Metric | Target |
|---------|--------------|------------------------------|---------------|--------|--------|
| MVP – Nothing waits unseen | G-01, G-03 | Run a demand end to end, with intake, registration, reminders and wait alerts handled by the product | See §1 | Waiting time per demand | TBD |
| Release 2 – Less re-typing | G-02 | Review and release AI drafts (summary, minutes, BRD/DDS, completeness check, packages, SA, closure note); answers, baseline and completion are recorded automatically | S-04, S-11, S-14, S-15, S-23, S-27, S-33, S-35, S-38, S-40, S-44, S-46, S-48, S-50 | Demand Owner hours per demand | TBD |
| Release 3 – Clear ownership & consults | G-03, G-04 | Owner suggestion confirmed by the Demand Manager; consult requests to product owners, the Architect and the Demand Manager; reopen closed demands; full demand overview | S-06, S-18, S-21, S-51, S-53 | Share of demands with an owner and current status | TBD |
| Later – Evidence | G-04 | See similar past demands, drafted estimates and costs, evidence packs for feasibility and approval, meeting briefs, prepared SAP data | S-16, S-19, S-25, S-29, S-31, S-36, S-42 | Share of decisions with evidence recorded | TBD |

## 3. Sequencing Rationale

- **MVP first:** waiting on the Business Partner is the top-ranked pain point theme (most of the 1–2 months). It needs no AI drafting, so the team learns quickly and with low risk.
- **Release 2 next:** document and record effort drives the 30–40 hours. It depends on on-premise AI drafting quality.
- **Release 3:** ownership and consults build on the drafts and the dashboard.
- **Evidence last:** it needs enough new demands to pass the threshold *(T 1:51:19)*.
- Every release crosses the journey; none is cut by stage or by technical layer.

## 4. Dependencies

| Dependency | Needed for | Owner | Status |
|------------|-----------|-------|--------|
| Read and send access to the shared DC mailbox | MVP | IT | Open |
| JIRA Cloud access to create and update demand tickets | MVP | IT / JIRA admin | Open |
| Standard questionnaire template | MVP | Demand Owner | Open |
| On-premise hosting | MVP | IT | Open |
| On-premise AI model good enough for drafting | Release 2 | TBD | Open |
| Teams transcript access for minutes | Release 2 | IT | Open |
| Evidence threshold reached (count of new demands) | Later | Demand Manager | Open |

## 5. Open Questions

1. Reminder and escalation timings. *(TBD)*
2. Targets for every metric. *(TBD – set with the Demand Manager)*
3. Which live demand is the pilot? *(TBD)*
