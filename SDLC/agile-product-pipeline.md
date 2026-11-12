# Agile Product Pipeline – From Idea to Delivery

Agile has no single official list of inception artifacts. The accepted process is a sequence of established practices, each owning one stage:

| Stage | Standard practice |
|-------|-------------------|
| Discovery | Design Thinking, Lean UX |
| Inception | Agile Inception Deck (Jonathan Rasmusson), Disciplined Agile |
| Backlog definition | User Story Mapping (Jeff Patton) |
| Delivery | Scrum |

## 1. The Pipeline

```
Idea ─► DISCOVERY ─► INCEPTION ─► BACKLOG DEFINITION ─► DELIVERY ─┐
        (problem &   (solution &   (story map → epics     (sprints)  │
         users)       plan)         → stories)                       │
          ▲                                                          │
          └──────────────── feedback & learning ◄───────────────────┘
```

**The spine:** Personas → As-Is Journey → To-Be Journey → Story Map → Epics → Stories.
Every other artifact either feeds this chain or constrains it.

## 2. Stage 0 – Idea

| Activity | Artifact | Feeds |
|----------|----------|-------|
| Opportunity assessment | **Opportunity Canvas** or **Lean Canvas** | Decision to start discovery |

## 3. Stage 1 – Discovery (understand the problem and the users)

| Activity | Artifact | Feeds |
|----------|----------|-------|
| Stakeholder identification | **Stakeholder Map** | Research plan, governance |
| User research (interviews, observation) | **Research Findings** | Personas, journeys |
| Persona creation | **Personas** (+ Empathy Map) | Journeys |
| Current-state mapping | **As-Is Journey Map**: steps, touchpoints, pain points | Problem statement, to-be journey |
| Problem definition | **Problem Statement** / "How Might We" questions | Vision |

**Gate:** the problem is confirmed as worth solving.

## 4. Stage 2 – Inception (agree on the solution and the plan)

| Activity | Artifact | Feeds |
|----------|----------|-------|
| Visioning | **Product Vision** (elevator pitch, product box) | Everything after it |
| Goal setting | **Product Goals & Success Metrics** (OKRs) | Business case, MVP |
| Scope boundaries | **In / Out of Scope** ("NOT list") | Story map |
| Future-state design | **To-Be Journey Map** | Story map |
| Backstage design | **Service Blueprint**: people, systems, handoffs behind each journey step | Story map, architecture |
| Prototyping | **Prototype / Wireframes** | Validation |
| Assumption testing | **Hypotheses & Experiment Results** | Scope, MVP |
| Technical strategy | **Architecture Vision** + **Non-Functional Requirements (NFRs)** | Definition of Done, enabler epics |
| Prioritisation | **Trade-off Sliders** (scope, time, cost, quality) | Release plan |
| Sizing and funding | **Lean Business Case** (value, rough size, team, cost) | Go decision |
| Risk identification | **RAID Log** (Risks, Assumptions, Issues, Dependencies) | Ongoing governance |
| Team set-up | **Team Charter** + **Definition of Ready (DoR) / Definition of Done (DoD)** | Delivery |

**Gate:** the go / funding decision.

## 5. Stage 3 – Backlog Definition

| Activity | Artifact | Feeds |
|----------|----------|-------|
| Story mapping (built from the to-be journey) | **User Story Map** | Release plan, epics |
| Release slicing | **MVP Definition** + **Release Plan / Roadmap** | Epics |
| Epic definition | **Epics**, cut from the map's release slices, so vertical by design | Stories |
| Story writing and splitting | **Initial Product Backlog**: user stories (INVEST) with acceptance criteria | Sprint planning |

## 6. Stage 4 – Delivery (Scrum, repeated every sprint)

| Event | Artifact | Feeds |
|-------|----------|-------|
| Backlog refinement | Ready stories (meet the DoR) | Sprint planning |
| Sprint planning | **Sprint Goal** + **Sprint Backlog** | Sprint |
| Sprint | **Increment** (meets the DoD) | Sprint review |
| Sprint review | Updated backlog / roadmap | Next refinement |
| Retrospective | Improvement actions | Next sprint |

## 7. Kept Up to Date Throughout

- **Decision Log**
- **RAID Log**
- **Success Metrics tracking**
- **Roadmap**

## 8. Where Splitting Happens

1. **Vertical slicing is decided on the story map,** not when epics are written. Each horizontal release line cuts through every journey step and becomes an MVP or a release.
2. **Epics are cut from those slices.**
3. **Stories are split again inside each epic**, using the SPIDR patterns (Spike, Path, Interface, Data, Rules).

Never split by technical layer (for example "database", "API", "UI"). Every epic and story must deliver something a user can see working.

## 9. Skill per Stage

Skills live in `skills/<skill-name>/`. Each skill reads the files of the step before it from the output folder (default `./inception/`) and writes its own.

| Stage | Artifacts | Skill | Reads |
|-------|-----------|-------|-------|
| Discovery | Stakeholder Map, Personas | `discovery-users` | Idea, research material |
| Discovery | As-Is Journey Map, Problem Statement | `as-is-journey` | `personas.md` |
| Inception | Product Vision (statement, goals & metrics, in / out of scope) | `product-vision` | `problem-statement.md`, `personas.md` |
| Inception | To-Be Journey Map, Service Blueprint | `to-be-journey` | `as-is-journey.md`, `product-vision.md`, `personas.md` |
| Backlog definition | User Story Map, MVP + Release Plan | `story-map` | `to-be-journey.md`, `service-blueprint.md`, `product-vision.md` |
| Backlog definition | Epics (one release slice per run) | `epics` | `story-map.md`, `release-plan.md`, `product-vision.md` |
| Backlog definition | User Stories (one epic per run) | `user-stories` | `epics/<epic>.md`, `story-map.md` |

**Traceability IDs** carried from one artifact to the next:

| ID | Meaning | Created by |
|----|---------|-----------|
| `SH-` | Stakeholder group | `discovery-users` |
| `P-` | Persona | `discovery-users` |
| `PP-` | Pain point | `discovery-users`, `as-is-journey` |
| `A-` | As-is journey step | `as-is-journey` |
| `G-` / `C-` | Product goal / in-scope capability | `product-vision` |
| `T-` | To-be journey step (story map backbone) | `to-be-journey` |
| `S-` | Story map card | `story-map` |
| `E-` | Epic | `epics` |
| `US-` | User story | `user-stories` |

Not yet covered by a skill: Opportunity Canvas, Prototype / Hypotheses & Experiments, Architecture Vision & NFRs, Trade-off Sliders & Lean Business Case, Team Charter & DoR / DoD, RAID Log, Decision Log.
