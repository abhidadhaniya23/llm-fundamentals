---
name: user-stories
description: Splits one epic into small, user-visible user stories that meet INVEST, using the SPIDR splitting patterns, each with Given / When / Then acceptance criteria. Use when an epic is agreed and the team needs a refined backlog for sprint planning.
---

# User Stories

Produces `stories/<epic-id>-stories.md` in the output folder (default `./inception/stories/`).

- **User story** = "As a [persona], I want [action], so that [benefit]" – small enough to finish within one sprint.
- **INVEST** (Bill Wake) = Independent, Negotiable, Valuable, Estimable, Small, Testable.
- **SPIDR** (Mike Cohn) = Spike, Paths, Interfaces, Data, Rules.

## Inputs

- Required: one epic file `epics/<epic-id>-<short-name>.md` and `story-map.md`. If missing, ask the user for the content and mark derived content *(to be validated)*.
- Optional: `to-be-journey.md`, `service-blueprint.md`, `personas.md`, and any business rules or examples the user provides.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. List the epic's outcome, cards, acceptance criteria, constraints and known rules
- [ ] 2. Draft the story list with split patterns; confirm with the user
- [ ] 3. Write each story with acceptance criteria and an INVEST check
- [ ] 4. Self-check, fix, save; ask the user to review
```

**Step 2 – Split.** Each card becomes one or more stories. If a card is too big for one sprint, split it with SPIDR, preferring: Paths (basic path first), Rules (simple rule first), Data (one data type first), Interfaces (one channel first). Use a Spike only when the team cannot estimate without learning something; a spike states its question and a timebox. Never split by technical layer.

**Step 3 – Write.** Use [templates/stories.md](templates/stories.md). Each story has: the story sentence, cards and step, business rules, 3–6 acceptance criteria in Given / When / Then (basic path plus at least one alternative or error case), notes and assumptions, dependencies, and an INVEST check. Use business language and concrete example values where the material gives them.

**Step 4 – Self-check.** Verify, fix anything that fails, and check again:
- Every card of the epic is covered; no story outside the epic's cards.
- Every story is written from a persona's view and passes INVEST, or the failing letter is named with a reason.
- Every epic-level acceptance criterion is covered by story criteria.
- No technical tasks, technical design or invented rules.

## Rules

- Technical work ("create table", "build API") is a sprint task inside a story, never a story.
- If something needed is not in the epic, add it to Open Questions – the epic or story map is out of date.
- Estimates stay `TBD`; the team estimates in refinement.

## Template

[templates/stories.md](templates/stories.md)

## Example

Good:
> As the Approver, I want to see a summary of the submitted answers before I decide, so that I can decide without reading every attachment.

Bad:
> As a developer, I want to integrate the email API.
> (Not a persona's value; a technical task.)
