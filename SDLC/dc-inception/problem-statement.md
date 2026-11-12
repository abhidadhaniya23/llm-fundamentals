# LoDA Demand Handling (DC) – Problem Statement

> Status: Draft | Version 0.1 | 2026-11-13. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `as-is-journey.md`, `personas.md`, `dc-sources/dc-context.md` (transcript timestamps as T), process flow PDF.

## 1. Problem Statement

The Demand Owner needs a way to move each demand from first contact to a clear outcome without tracking, chasing and recording every step by hand. The reason: one demand passes through 21 steps, 13 manual JIRA updates and 4 waits on the Business Partner *(as-is journey; PDF)*, and the knowledge behind the decisions sits in people's heads, not in a usable place *(T 1:29:51, 1:30:19)*. Today each demand costs 30–40 hours of effort and runs 1–2 months, mostly in follow-ups *(T 1:44:12)*, while the Demand Manager sees status only in a weekly call *(T 1:31:26)*. This limits how many demands the team can handle as volume grows beyond about 60 a year *(T 1:44:01)*.

## 2. Pain Point Themes (ranked)

| Rank | Theme | Pain points (IDs) | Journey steps | Frequency | Severity | Evidence |
|------|-------|-------------------|---------------|-----------|----------|----------|
| 1 | Waiting on and chasing the Business Partner | PP-01-03, PP-02-03 | A-05, A-11, A-16, A-20 | High – 4 waits per demand | High – most of the 1–2 months | T 1:44:12, 1:37:21 |
| 2 | Manual record keeping and document re-work | PP-01-01, PP-01-02, PP-01-04 | A-03 – A-21 (13 JIRA-tagged steps), A-06, A-09 | High – every demand | Medium – drives the 30–40 h effort *(to be validated)* | PDF, T 1:44:12 |
| 3 | No ownership or visibility across demands | PP-02-01, PP-02-02, PP-01-10, PP-01-09 | A-02, all steps, every "Demand Closed" exit | High – every demand | Medium | T 1:24:09, 1:31:26, 1:35:29 |
| 4 | Decisions made without evidence or a consult route | PP-01-05, PP-01-08, PP-03-01, PP-03-02 | A-07, A-08, A-10, A-12, A-13 | Medium – 2–4 decisions per demand | High *(to be validated)* | T 1:29:51, 1:30:30, 2:08:12 |
| 5 | Scattered intake | PP-01-06, PP-02-04 | A-01 | Every new demand | Medium – demands can be missed *(to be validated)* | T 1:26:41, 1:53:35 |
| 6 | Tasks outside the DC role | PP-01-07 | A-18 | Every accepted demand | Low *(to be validated)* | T 1:33:25 |

## 3. Baseline Facts

| Fact | Value | Source |
|------|-------|--------|
| Demands per year | About 60, expected to grow | T 1:44:01, 1:44:12 |
| Demand Owner effort per demand | 30–40 hours | T 1:44:12 |
| Elapsed time per demand | 1–2 months | T 1:44:12 |
| Steps per demand (full path) | 21 | as-is journey |
| Manual JIRA updates per demand | 13 tagged steps | PDF |
| Waits on the Business Partner | 4 (A-05, A-11, A-16, A-20) | as-is journey |
| Decision points with a "Demand Closed" exit | 5 | PDF |
| Demand status visibility for the Demand Manager | Weekly call | T 1:31:26 |
| Typical wait duration per step | TBD | – |

## 4. Impact of Not Solving It

- The team cannot take on more demands without adding Demand Owner effort *(T 1:44:12 – to be validated)*.
- Demands keep stalling unseen while the team waits on the Business Partner *(T 1:37:21)*.
- Fit and feasibility decisions keep depending on who happens to remember a similar past demand *(T 1:29:51 – to be validated)*.
- Closed demands keep ending without a notice or a way back *(T 1:24:09)*.

## 5. How Might We

1. How might we keep a demand moving while we wait on the Business Partner, without the Demand Owner chasing by hand?
2. How might we keep the JIRA record complete without the Demand Owner re-typing it at every step?
3. How might we let the Demand Manager see, at any time, which demands are stuck and who owns them?
4. How might we give the Demand Owner and technical reviewers the facts from similar past demands at each decision?
5. How might we make sure every demand enters through one door and every closed demand ends cleanly?

## 6. Open Questions

1. Which steps account for most of the 30–40 hours? *(unknown – needed to rank theme 2 against theme 1)*
2. How long are the typical waits? *(unknown – baseline for theme 1)*
