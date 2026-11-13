---
name: as-is-journey
description: Maps the current end-to-end experience of each primary persona (as-is user journey map) and derives an evidence-based problem statement from the pain points. Use after personas exist, when the user wants to understand how work is done today and where it hurts.
---

# As-Is Journey & Problem Statement

Produces `as-is-journey.md` and `problem-statement.md` in the output folder (default `./inception/`).

- **As-is journey map** = today's experience of one persona in one scenario: stages, steps, touchpoints, people involved, pain points, opportunities.
- **Problem statement** = the problem worth solving, grounded in the journey's pain points. It contains no solution.

## Inputs

- `personas.md` (required). If missing, ask the user to describe the user groups and mark persona references *(to be validated)*.
- `stakeholder-map.md` (optional).
- A description of how the work is done today: process documents, diagrams, interview notes, or the user's own walkthrough.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Agree the scenario (start trigger, end point) and the personas to map
- [ ] 2. Draft stages and steps per persona; confirm with the user
- [ ] 3. Fill the journey lanes for every step
- [ ] 4. Rank pain points into themes; draft the problem statement; confirm with the user
- [ ] 5. Self-check, fix, save; ask the user to review
```

**Step 2 – Steps.** Break the scenario into stages, and each stage into steps the persona experiences. Give each step a stable ID (`A-01`, `A-02`, …). Mark decision points and waiting times explicitly.

**Step 3 – Lanes.** For each step: what the persona does, touchpoint / channel, others involved, tools, time or effort, feeling, pain points, opportunities. Feelings, times and numbers only from evidence; otherwise `TBD` or *(to be validated)*.

**Step 4 – Problem statement.** Group pain points into themes; rank them by frequency and severity. Write the statement in the form:
> [Persona] needs a way to [need] because [insight]. Today [current situation], which causes [impact].

Add baseline facts from the material and 3–5 "How might we" questions.

**Step 5 – Self-check.** Verify, fix anything that fails, and check again:
- Each mapped persona's journey covers the full scenario.
- Every known pain point from `personas.md` sits on a step or is excluded with a reason.
- Steps describe today's reality; improvement ideas are only in the Opportunities lane.
- The problem statement names a persona, a need, evidence and an impact, and no solution.

## Rules

- Map the most common path; list variants in Open Questions.
- Keep step and pain point IDs stable once the user has confirmed them.
- Keep the user's own terms for steps, documents and roles.

## Templates

- [templates/as-is-journey.md](templates/as-is-journey.md)
- [templates/problem-statement.md](templates/problem-statement.md)

## Example

Good problem statement:
> The Approver needs a complete view of each request before deciding, because the information is spread over emails and attachments *(interview notes)*. Today they chase missing details by email, which adds 1–2 weeks per request *(time log)*.

Bad:
> We need an AI platform to automate the process.
> (A solution, not a problem; no persona, no evidence.)
