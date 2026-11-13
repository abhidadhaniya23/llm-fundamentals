---
name: discovery-users
description: Creates a stakeholder map and evidence-based personas for a product or initiative. Use at the start of discovery, when the user describes an idea or shares research material (interviews, process notes, org charts) and needs to know who the product is for and who has a say in it.
---

# Discovery: Stakeholders & Personas

Produces `stakeholder-map.md` and `personas.md` in the output folder (default `./inception/`).

- **Stakeholder** = any group that affects or is affected by the initiative.
- **Persona** = an archetype of one user group, built from research. Never a real, named individual.

## Inputs

- Required: an idea or initiative description.
- Recommended: research material. Without it, write **proto-personas** and label them so in the status line.

## Workflow

Copy this checklist and track progress:

```
- [ ] 1. Read all input; list every role, team and organisation mentioned
- [ ] 2. Build the stakeholder map; confirm it with the user
- [ ] 3. Agree which user groups get a persona
- [ ] 4. Write the personas
- [ ] 5. Self-check, fix, save; ask the user to review
```

**Step 2 – Stakeholder map.** Classify each group by role: primary user, secondary user, sponsor, decision-maker, approver, affected party, supplier. Rate influence and interest (High / Low) and place each group on the power–interest grid: Manage closely, Keep satisfied, Keep informed, Monitor. Show the table to the user and adjust it before writing any file.

**Step 3 – Persona selection.** Every primary user group gets a persona. A secondary group gets one only if its goals or way of working differ clearly.

**Step 4 – Personas.** Use [templates/personas.md](templates/personas.md). For each persona capture: role and context, goals, tasks, decisions owned, pain points, needs, behaviours and tools. Every attribute cites its source (file or "user input") or is marked *(to be validated)*.

**Step 5 – Self-check.** Verify, fix anything that fails, and check again:
- Every group from step 1 is in the stakeholder map or excluded with a reason.
- Every primary user group has a persona.
- Every persona attribute has a source or a *(to be validated)* marker.
- No invented quotes, names, numbers or personal details.

## Rules

- Personas are named by role ("The Approver"), not with invented personal names.
- Quotes only if verbatim from provided research.
- Describe users and their situation only. Solution ideas from the input go to Open Questions.
- Keep the user's own terms for roles and groups.

## Templates

- [templates/stakeholder-map.md](templates/stakeholder-map.md)
- [templates/personas.md](templates/personas.md)

## Example

Good pain point:
> Re-enters the same request details in two systems for every request *(source: interview notes, p. 3)*.

Bad:
> "I hate my job!" – Sarah, 34, loves coffee.
> (Invented quote, name and personal details; no source.)
