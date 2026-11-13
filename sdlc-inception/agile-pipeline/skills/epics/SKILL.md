---
name: epics
description: Cuts one release slice of a user story map into vertical epics, each with an epic hypothesis statement (SAFe), outcome, scope and epic-level acceptance criteria. Use when a story map with release lines exists and the team needs epics for a release; rejects horizontal (technical-layer) epics.
---

# Epics

Produces, in `<output folder>/epics/` (default `./inception/epics/`):
- `<release>-index.md` – the epics in the slice and the coverage of every card;
- `<epic-id>-<short-name>.md` – one file per epic.

- **Epic** = a large body of work inside one release that delivers a clear user and business outcome, later split into stories.
- **Vertical** = cuts through everything needed for a result a persona can see. A **horizontal** epic covers one layer or system ("integrations", "UI", "AI model") and is not allowed.

## Inputs

- Required: `story-map.md` (cards `S-xx`, steps `T-xx`, releases), `release-plan.md`, `product-vision.md`. If one is missing, ask the user for its content and mark derived content *(to be validated)*.
- Optional: `to-be-journey.md`, `service-blueprint.md`, `personas.md`.
- The release slice to work on. One slice per run; default is the earliest slice without epics.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. List the slice's goal, metric, cards and constraints
- [ ] 2. Propose the epic cut; confirm with the user
- [ ] 3. Write each epic and the index
- [ ] 4. Self-check, fix, save; ask the user to review
```

**Step 2 – Epic cut.** Group the slice's cards into epics, preferring in this order:
1. Journey segment – consecutive steps ending in a result the persona can see.
2. Persona – when personas get separate outcomes.
3. Variation – basic path in one epic, exception or alternative paths in another.
4. Business rule – when one rule set is large enough to stand alone.

Test each epic: does it end in a visible outcome, can it be demonstrated on its own, does it cross more than one layer? If not, re-cut. Typically 3–8 epics per slice. An **enabler** epic is allowed only when a named epic cannot be delivered without it; label it and name that epic.

Show the cut as a table (epic → outcome → cards → steps spanned → why vertical) before writing files.

**Step 3 – Write.** Use [templates/epic.md](templates/epic.md). Each epic has:
- Epic hypothesis statement (SAFe): For [customers] who [need], the [epic] is a [what] that [value]. Unlike [today], it [difference].
- Business outcome and a leading indicator.
- Personas, steps spanned, cards, in / out of scope.
- 3–7 epic-level acceptance criteria (Given / When / Then, outcome level).
- Constraints, dependencies, risks and assumptions, size (`TBD` unless given).

**Step 4 – Self-check.** Verify, fix anything that fails, and check again:
- Every card of the slice is in exactly one epic; no cards from other releases.
- Every epic ends in an outcome a persona can see; no horizontal epics.
- Release constraints are carried into the epics they affect.
- No user stories, technical design or invented estimates.

## Templates

- [templates/epic-index.md](templates/epic-index.md)
- [templates/epic.md](templates/epic.md)

## Example

Good:
> E-MVP-02 – Partner receives and returns the questionnaire (T-03 to T-05; S-07, S-08, S-11)

Bad:
> E-MVP-02 – Email integration
> (Horizontal: one system, no outcome a persona can see.)
