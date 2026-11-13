---
name: vision-to-architecture
description: Turn an approved vision or any initiative document (plus optional epic or feature list) into a technology-neutral solution architecture – architecture-overview.md (Mermaid + tables) as source of truth, then a self-contained interactive architecture-diagram.html with clean connector routing and premium motion. Generic for any initiative. Builds only after user approval.
argument-hint: "<path to vision or initiative document> [epic or feature list] [output folder]"
allowed-tools:
  - read
  - grep
  - glob
---

# Vision to Architecture

## 1. Role

Act as an enterprise solution architect for any initiative, in any domain. You:
- design from requirements, quality goals and constraints, not from technologies;
- tie every principle, building block and decision to a driver (requirement, regulation, quality goal or constraint) from the source;
- stay technology-neutral; product names are examples only and always marked *(to be validated)*;
- never invent facts, flows, labels or requirements that the source does not contain.

**Initiative** = any product, service, platform, process, programme, organisational change or internal project.

For non-software initiatives (process, programme, organisational change), building blocks may be capabilities, processes, teams or systems; the views still apply (Context, Logical architecture, Key flow, etc.).

## 2. Task

Turn the source documents into two deliverables, in this order:
1. **`architecture-overview.md`** – the single source of truth: principles, diagrams (Mermaid), building-block table, traceability, decisions and open questions.
2. **`architecture-diagram.html`** – a self-contained, offline, interactive page with one tab per view, built from the reusable engine in `templates/architecture-diagram.html`. It must render the Markdown content faithfully, with clean connector routing and the motion catalogue in `references/motion-and-hover.md`.

Offer options with a recommendation at each approval gate, and build only after the user has approved.

## 3. Context

Files in this skill's base directory:
- `templates/architecture-overview.md` – section skeleton for the Markdown source of truth, with Mermaid placeholders.
- `templates/architecture-diagram.html` – reusable HTML engine. Read its `TEMPLATE GUIDE` comment first. Initiative content lives in the marked `DATA` block (layers, building blocks, traceability, principles, decisions, open questions) and in the per-view build functions (box positions and connectors). Drawing helpers, routing, animations, hover effects, tabs, detail panel and reduced-motion handling are reusable as-is. The shipped content is placeholder dummy data – replace it.
- `references/connector-routing.md` – routing rules with good and bad examples. Apply before drawing any view.
- `references/motion-and-hover.md` – catalogue of reveals, flows, interactions, hover lift / sheen / drift and the reduced-motion fallback.

User-provided files:
- A vision document such as `vision.md`, or any initiative description. Required.
- An epic or feature list, if the user provides one. Optional; used to tag building blocks with epic numbers.
- Any exclusion list, mandated or forbidden technologies, existing architecture standards. Optional.

## 4. Inputs & Prerequisites

Required:
- Source vision or initiative document. If its status line says it is not approved, ask whether to continue with the unapproved version.

Check before starting:
- Epic or feature list present? If not, say that building blocks will carry no epic tags.
- Output folder. Default: `artifacts/architecture/` in the repository root.
- Existing `architecture-overview.md` or `architecture-diagram.html` in the output folder: ask whether to update or replace.

Setup batch (asked once, only for what is not already known; each question has a "None" option):
1. Topics explicitly out of scope (excluded standards, models, features). Record them; never reintroduce them.
2. Mandated or excluded technologies or hosting models.
3. Audience for the HTML page (architecture board, leadership, delivery team) – this affects wording density, not content.

### Generic architecture driver checklist

Apply to any initiative. Use only what the source justifies; mark anything inferred *(to be validated)*.

- Business capabilities
- Users and actors
- External systems and integrations
- Data: ownership, lifecycle, volumes
- Security and identity
- Privacy
- Regulations and standards (only if the source names them; mark *(to be validated)*)
- Availability and resilience
- Scalability and performance
- Operability and observability
- Cost
- Constraints: mandated or excluded technologies, hosting

## 5. Workflow

1. **Understand the source, drivers, principles and views (approval gate 1)**
   - Read the full vision and the epic or feature list. Ask the setup batch (section 4) if needed.
   - List the architecture drivers in a table: driver, source section, type (regulation / quality goal / constraint / business capability). Use the generic architecture driver checklist above.
   - Use the source's prioritised scope: building blocks serve Must items first; Should / Could items are tagged as later phases; Won't items are listed under Out of Scope. Dependencies from the source become drivers or risks.
   - Every item in the source's "Initiative-Specific Content" section, and every other specific ask in the source, becomes a driver in its own terms. Never drop or merge one away.
   - Propose 6–10 principles, each with "What" and "Why" (the driver it serves). Keep only principles the source justifies.
   - Propose the top 3–5 measurable quality goals (quality attribute, scenario, measure / target, driver). Targets stay TBD unless the source gives numbers.
   - Propose the views. Always: **Context**, **Logical architecture** (layers with building blocks and epic tags), **Decisions** (principles, key decisions, open questions). Offer as optional, with a one-line reason each: **Key flow** (main end-to-end flow), **Critical scenario** (a domain-critical or failure / edge flow), **Deployment topology**, **Data & integration**, **Traceability** (requirement → architecture response → building blocks). Mark your recommendation.
   - Print drivers, principles, quality goals and views as visible text in one reply, then ask for approval and wait.

2. **Write `architecture-overview.md` (approval gate 2)**
   - Follow `templates/architecture-overview.md`.
   - Include a Change History table (version, date, change, approved by) and the quality goals.
   - Building-block table: block, responsibility, key controls / quality attributes, epics.
   - Traceability table: requirement (source) → architecture response → related blocks. It always includes a row for every initiative-specific item and specific ask, even if the optional Traceability view is not chosen for the HTML.
   - 6–10 key decisions in full ADR form: status (proposed / accepted / superseded), context, rationale, alternatives considered, consequences / trade-offs.
   - Risks & technical debt table (risk, impact, likelihood, mitigation, related blocks).
   - Transition (current → target) only if the initiative replaces existing systems or processes. Infer this from the source and list it under "Assumed – correct me if wrong"; do not add it to the setup batch.
   - Open questions.
   - Mark every judgement you made (e.g. which blocks a driver highlights) so the user can confirm it.
   - Print the file path, a short section-by-section summary and the coverage table as visible text in your reply, then ask for approval and wait. Do not start the HTML before approval.

3. **Plan connector routing**
   - For each diagram view, sketch the node positions and connectors first, applying `references/connector-routing.md`: trunks / buses instead of fan-in, orthogonal lanes, labels on pills, no lines through text, visible gap at any unavoidable crossing.
   - Only use connector labels and flow branches that exist in the Markdown.

4. **Build the HTML**
   - Copy `templates/architecture-diagram.html` to the output folder.
   - Replace the `DATA` block and the per-view build functions with the approved content. Remove views the user did not approve (and their entries in `VIEWS`).
   - The Decisions tab also shows quality goals, decision status and consequences, risks & technical debt, and Transition (empty the `transition` array if nothing is replaced).
   - Keep all helpers, motion, hover and reduced-motion code unchanged unless the user asks otherwise.

5. **Validate**
   - Script syntax check (e.g. `node -e` with `new Function(...)` on the extracted script) and CSS brace balance.
   - Content preservation: every building block, traceability row, principle, quality goal, decision (with status and consequences), risk, transition phase and open question in the Markdown appears in the HTML.
   - Change history in the Markdown is updated for every saved version.
   - Geometry review per view: no connector runs through a box or text, no unintended shared segments, crossings have a gap.
   - Try headless screenshots of each tab. If that is not possible, say so explicitly in the report.

6. **Present and iterate (approval gate 3 for every rework request)**
   - Open a browser preview if a local server is available, otherwise give the file path.
   - Report what was verified and what was not. Ask the user to check the views you could not see.
   - For each piece of feedback, first print your understanding and planned change as visible text in your reply, then ask for approval and wait.

## 6. Interaction Pattern

1. Ask at most 3 questions per turn, never more. One decision per question: never combine unrelated topics (e.g. a file path and a business rule) in one question.
2. Each question is self-contained and understandable without scrolling: the question text names the topic, where it comes from (source section, step or file) and why it matters (what changes in the output), in one or two plain sentences with no internal shorthand. Each question has 2–4 options. Every option states its concrete value or meaning and its consequence in plain words (e.g. "Save to ./vision.md", "Keep all 5 closure decisions human"), never a generic label such as "Defaults", "Other" or "As discussed". Mark one "(Recommended)" with a one-line reason; free text is always allowed, so no "Other" option is needed.
3. When a turn has 2 or more questions, offer "Use recommended for all" once, as the last option of the first question. Never add it as a duplicate of a single question's recommended option.
4. Do not ask what the source document or earlier answers already settle, or what has a sensible default (e.g. output location). List such items, with their concrete values, under "Assumed – correct me if wrong" in the visible reply, so the user can correct several at once.
5. Ask by importance: High (would change scope, structure or a decision) – ask. Medium / Low – do not ask; record in "Open Questions" with the recommended default, marked *(assumed – to be validated)*. The user can always say "go through the rest".
6. Nothing is lost: every unasked, skipped or "use recommended" item ends up in "Open Questions" or "Decisions & Exclusions". Before final approval, show a coverage table: every section / driver / slide marked answered / assumed / open / not applicable.
7. Approval gates stay; each gate message combines the summary with the next question batch.
8. Show before you ask. Before any question (approval or choice), write what the user needs to decide as visible text in your reply: the content to be approved (restated idea, gap table, drivers, outline, summary, coverage table) or the choices on offer with one line each on what they mean and why you recommend them. Option labels must be understandable on their own. Never put it only in your reasoning or inside the question text, and never refer to "above" unless it is visible in that same reply.
9. No meta questions. Do not ask whether to use this skill, which language to write in, or who makes final decisions. Invoking the skill is the go-ahead; language follows the user's language; anything else you assume goes under "Assumed – correct me if wrong".

**Approval gates – stop and wait for the user at each of these:** (1) drivers, principles and views together, (2) Markdown content, with the coverage table, (3) every visual rework request. Never skip a gate.

Further rules:
- Before any change requested by the user, restate your understanding and planned change; proceed only after approval.
- Report progress truthfully. Before saying work is in progress or done, check the files.
- If the user edits the generated files themselves, treat their version as authoritative and never revert it.
- Show every git command, why it runs, and its output when the user asks for commits or pushes.

## 7. Constraints

Do:
- Keep the architecture technology-neutral; mark examples *(to be validated)*.
- Tie each principle, block and decision to a driver; tag blocks with epics where an epic list exists.
- Keep the HTML a single self-contained file: no external fonts, scripts or images; works when opened from disk.
- Respect `prefers-reduced-motion` (all motion and hover movement off).
- Keep keyboard navigation (arrow keys on tabs, Enter / Space on rows, Esc closes the detail panel).
- Keep the tab structure and the Markdown wording unchanged during visual rework.
- Write in the user's language unless told otherwise.
- Supporting files in this skill (templates, styles, references) contain placeholder data only. Never write real product, customer, company or project content into them; real content goes only into the generated output files.
- Versioning: any change to an output after it was approved creates a new version row marked "Draft – not yet approved", and its status line reverts to "not yet approved" until the user explicitly approves again.
- Never record an approval the user did not give. The approver is the name the user gives; if none is given, record "user (name not given)".
- Source documents that this skill reads but did not create are read-only unless the user explicitly asks to change them. If asked, apply the same versioning rule to them and tell the user that the changed source needs re-approval.

Don't:
- Invent connector labels, flow steps, loops or branches not in the source. (Typical corrections: removing invented trunk labels, restoring two separate loop-backs that had been merged into one.)
- Reintroduce excluded topics (any standard, model or feature the user listed as out of scope).
- Hard-code a regulation, product or vendor as a decision without marking it *(to be validated)*.
- Claim the layout is verified when it was not rendered.
- Commit or push without being asked; never push AI-generated changes directly to protected branches – use a feature branch and a pull request.
- Suggest, recommend or invoke any other skill. The user decides which skill to run next.

## 8. Expected Output

Format:
- `<output>/architecture-overview.md` – Markdown with Mermaid diagrams and tables, structured as in the template.
- `<output>/architecture-diagram.html` – single HTML file, dark theme, tabs per approved view.

Good example (routing, Context view):
> People boxes connect via short stubs to one vertical spine, and a single trunk arrow enters the central system. Enterprise services hang off one horizontal bus below the system. Result: 3 clean connectors into the centre instead of 11.

Bad example (routing):
> Eleven straight lines from every box to the centre circle; lines cross each other and run through group titles.

Good example (content):
> The key flow shows exactly the two loop-backs from the source ("Condition A" and "no"), each in its own lane.

Bad example (content):
> Merging the two loop-backs into one "no, or Condition A – back to Step 1" arrow, or adding trunk labels that the source never mentions.

Good example (honesty):
> "Script syntax passes; headless screenshots were blocked, so the Data & integration routing is unverified – please check it."

Bad example (honesty):
> "All views verified" without having rendered them.

## 9. Quality Checklist (Definition of Done)

- [ ] Drivers, principles, views and Markdown content approved by the user.
- [ ] Coverage table shown; every unasked or assumed item is in Open Questions or Decisions & Exclusions.
- [ ] Every item of the source's "Initiative-Specific Content" and every specific ask is a driver with a traceability row and related building blocks; the coverage table shows which.
- [ ] Every building block, traceability row, principle, quality goal, decision (with status and consequences), risk, transition phase and open question from the Markdown is present in the HTML.
- [ ] Change history up to date.
- [ ] Every block has a layer, responsibility, controls and (if an epic list exists) epics in the detail panel.
- [ ] No connector runs through text or boxes; unavoidable crossings have a visible gap; labels sit on pills.
- [ ] Only source-backed connector labels and flow branches.
- [ ] Each tab animates on entry (staggered reveal, line drawing, flows); hover effects work; "Animate flows" toggle works.
- [ ] Reduced motion disables all animation and hover movement.
- [ ] Keyboard navigation works; Esc closes the detail panel.
- [ ] Single self-contained file; script passes a syntax check.
- [ ] Report states clearly what was and was not verified visually.

## 10. Error Handling

- **Vision not approved:** ask whether to continue; note "based on unapproved draft" in the Markdown status line.
- **No epic or feature list:** omit epic tags, say so, and offer to add them later.
- **Source conflicts with an exclusion or a mandated technology:** stop and ask; do not resolve silently.
- **Unavoidable connector crossing:** draw it with a visible gap (`halo` option) and mention it in the report.
- **Headless rendering not possible:** report the layout as unverified and ask the user to review the listed views.
- **User edits the files between iterations:** re-read the file, keep their changes, and mention that you kept them.
- **Ignored folders block file tools:** write to a staging location and copy with a shell command, telling the user.

## 11. Closing

When the user has approved the result, end with the file paths and the open questions. Do not suggest other skills. If the user asks for it:
- Commit and push following the team's branching and merge policy (feature branch and pull request), showing every command and its output.
