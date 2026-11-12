---
name: to-be-journey
description: Designs the future end-to-end experience of each persona (to-be journey map) and the people, systems and handoffs behind it (service blueprint), traced to pain points and product goals. Use after the as-is journey and product vision exist, when the team needs to define how the service should work before building a story map.
---

# To-Be Journey & Service Blueprint

Produces `to-be-journey.md` and `service-blueprint.md` in the output folder (default `./inception/`).

- **To-be journey map** = the future experience of a persona in the same scenario as the as-is journey, with what changes and why.
- **Service blueprint** (Shostack; Bitner et al.) = the to-be journey plus its backstage: frontstage interactions, line of visibility, backstage actions, support systems, evidence.

## Inputs

- Required: `as-is-journey.md` (steps `A-xx`, pain points `PP-xx`), `product-vision.md` (goals `G-xx`, scope `C-xx`), `personas.md`. If one is missing, ask the user for its content and mark derived content *(to be validated)*.
- Optional: `problem-statement.md`, `stakeholder-map.md`, and any target-process ideas, system lists or policies the user provides.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Summarise scenario, personas, goals, scope and top pain points; agree design principles
- [ ] 2. Decide the future of every as-is step; confirm the to-be journey with the user
- [ ] 3. Write the service blueprint for every to-be step; confirm with the user
- [ ] 4. Self-check, fix, save; ask the user to review
```

**Step 2 – To-be journey.** For each as-is step decide: unchanged, changed, automated, removed, or new. Give each to-be step a stable ID (`T-01`, …) and link it to the as-is steps it replaces, the pain points it resolves, and the goals and capabilities it serves. Stay inside the vision's in-scope areas.

**Step 3 – Service blueprint.** For each to-be step fill: persona action, frontstage, backstage (by role or "product"), support systems and data, handoff, decision and owner, evidence produced. Name systems in business terms ("ticketing system"), not technical components.

**Step 4 – Self-check.** Verify, fix anything that fails, and check again:
- Same scenario as the as-is journey; every mapped persona has a to-be journey.
- Every as-is step maps to a to-be step or is removed with a reason.
- Every top pain point is resolved by a step or listed as unresolved with a reason.
- Every to-be step has a blueprint row; every decision has an owner.
- No technical design (components, APIs, data models, hosting) – technical points go to Open Questions.

## Rules

- Every change traces to a pain point and a goal; a change with neither needs the user's confirmation.
- Decisions stay with the people who own them unless the user decides otherwise.
- Keep `T-` IDs stable once confirmed; the story map uses them as its backbone.

## Templates

- [templates/to-be-journey.md](templates/to-be-journey.md)
- [templates/service-blueprint.md](templates/service-blueprint.md)

## Example

Good to-be step:
> T-04 – Approver reviews the prepared summary and decides (changed from A-05; resolves PP-01-03; serves G-02).

Bad:
> T-04 – Microservice calls the LLM API and writes to the database.
> (Technical design; no persona experience; no traceability.)
