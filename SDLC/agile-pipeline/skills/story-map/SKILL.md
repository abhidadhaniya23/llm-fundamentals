---
name: story-map
description: Builds a user story map (Jeff Patton) from a to-be journey and service blueprint, then slices it into an MVP walking skeleton and further releases. Use when the future journey is agreed and the team needs a release plan and the input for vertical epics.
---

# Story Map & Release Plan

Produces `story-map.md` and `release-plan.md` in the output folder (default `./inception/`).

- **Story map** = journey activities and steps left to right (the backbone); user tasks under each step, most essential at the top; horizontal release lines across all steps.
- **Walking skeleton** = the thinnest release that still lets a persona go through the whole journey end to end.

## Inputs

- Required: `to-be-journey.md` (steps `T-xx`), `service-blueprint.md`, `product-vision.md` (goals `G-xx`, scope `C-xx`). If one is missing, ask the user for its content and mark derived content *(to be validated)*.
- Optional: `personas.md`, and any priorities, deadlines or capacity the user gives.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Lay out the backbone from the to-be stages and steps
- [ ] 2. Write cards under each step; confirm the map with the user
- [ ] 3. Draw release lines (MVP first); confirm with the user
- [ ] 4. Write the release plan
- [ ] 5. Self-check, fix, save; ask the user to review
```

**Step 1 – Backbone.** Use the to-be stages as activities and the `T-` steps as the backbone, in order. Do not reorder or rename them; if they need changing, the to-be journey is out of date – note it in Open Questions.

**Step 2 – Cards.** Short user tasks in "verb + object" form that a persona can see working. Each card gets a stable ID (`S-01`, …), a step and a persona. Put the basic path at the top, variations and exceptions below. Cross-cutting constraints (security, audit, access, performance) go in a separate Constraints list, not on cards.

**Step 3 – Releases.** The MVP line must cross every backbone step. Where the MVP has no card for a step, add one that keeps the step working manually and mark it "manual in this release". Each release gets a goal (linked to `G-` IDs), what users can do afterwards, and a metric.

**Step 5 – Self-check.** Verify, fix anything that fails, and check again:
- Every `T-` step has at least one card; every in-scope `C-` capability is covered.
- Every card is user-visible and sits in exactly one release.
- The MVP is a walking skeleton; manual steps are marked.
- No release is cut by stage or technical layer.

## Rules

- No technical tasks as cards ("set up message queue").
- No dates, estimates or capacity unless the user gives them.
- If the user insists on a release that does not cross the backbone, record the decision and its trade-off: users cannot complete the journey until a later release.

## Templates

- [templates/story-map.md](templates/story-map.md)
- [templates/release-plan.md](templates/release-plan.md)

## Example

Good card:
> S-12 – Confirm assigned owner (T-02, P-02, MVP)

Bad:
> S-12 – Set up message queue
> (Technical task; no persona can see it working.)
