---
name: product-vision
description: Writes a short, stable product vision – vision statement, elevator pitch, product vision board, product goals with success metrics, and in / out of scope – from an evidence-based problem statement and personas. Use when the problem and target users are known and the team needs a shared direction before designing the future state.
---

# Product Vision

Produces `product-vision.md` in the output folder (default `./inception/`).

A **product vision** states who the product is for, what need it meets and what outcome it achieves. It changes rarely and fits on two pages. It is not a requirements document, roadmap or architecture.

## Inputs

- `problem-statement.md` and `personas.md` (required). If missing, ask the user to describe the problem and the users, and mark derived content *(to be validated)*.
- `stakeholder-map.md`, `as-is-journey.md` (optional).
- Any strategy papers or sponsor statements the user provides.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Summarise target users, problem, desired outcome and scope signals
- [ ] 2. Draft 2–3 vision statements and an elevator pitch; let the user choose
- [ ] 3. Fill the product vision board
- [ ] 4. Derive product goals and metrics; draft in / out of scope; confirm with the user
- [ ] 5. Self-check, fix, save; ask the user to review
```

**Step 2 – Vision statement.** One or two sentences naming the users and the outcome. Elevator pitch (Geoffrey Moore):
> For [target users] who [need], [product] is a [category] that [key benefit]. Unlike [current alternative], it [main difference].

**Step 3 – Vision board** (Roman Pichler): target group, needs, product, business goals.

**Step 4 – Goals and scope.**
- 3–5 product goals, each an outcome (not a feature) tracing to a pain point theme.
- Each goal gets a metric, a baseline from the problem statement, and a target (`TBD` unless the user gives one).
- In scope: 4–8 capability areas in user terms ("users can …"), not features or systems.
- Out of scope: everything the input excludes, plus the scenario's boundaries.

**Step 5 – Self-check.** Verify, fix anything that fails, and check again:
- Every top pain point theme is covered by a goal or explicitly excluded.
- No roadmap, features, architecture, NFRs, risks or budget in the document; anything like that from the input goes to Open Questions.
- No invented numbers; no hype words.

## Template

[templates/product-vision.md](templates/product-vision.md)

## Example

Good:
> Give approvers one place to see, decide and track every request, so that decisions take days instead of weeks.

Bad:
> A revolutionary AI-powered platform delivering 70% savings across the enterprise.
> (Hype, invented number, no user, no need.)
