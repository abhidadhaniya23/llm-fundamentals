# LoDA Demand Handling (DC) – Stakeholder Map

> Status: Draft | Version 0.1 | 2026-11-13. *(to be validated)* = assumption, not yet confirmed.
>
> Sources: `dc-sources/Demand_Handling_Consulting_Process_Flow_Refined (2).pdf` (PDF), `dc-sources/dc-context.md` (context; transcript timestamps as T).

## 1. Stakeholders

| ID | Stakeholder group | Role | Interest in the initiative | Influence | Interest | Quadrant | Persona? | Source |
|----|-------------------|------|----------------------------|-----------|----------|----------|----------|--------|
| SH-01 | Demand Owner | Primary user | Owns every demand end to end; wants the manual steps, JIRA updates and follow-ups taken off their plate | High | High | Manage closely | Yes – P-01 | context §2, T 1:12:09 |
| SH-02 | Demand Manager | Secondary user; decision-maker (complexity, with the Architect); escalation point | Needs a view of all demands and to know when a demand is stuck; today relies on a weekly call | High | High | Manage closely | Yes – P-02 | context §2, §4.6, PDF |
| SH-03 | Technical Architect | Approver (confirms complex requirements, with the Demand Manager) | Wants to be consulted at the right point, with the facts already gathered | High | Low | Keep satisfied | Yes – P-03 (shared) | PDF, T 1:12:09 |
| SH-04 | Technical Product Owner & Product Team | Approver (feasibility, final technical approval); receives the handed-over demand | Wants a complete, baselined BRD/DDS and a clean handover to start development | High | High | Manage closely | Yes – P-03 (shared) | PDF |
| SH-05 | Business Partner | Affected party (external; not a user of the product) | Wants a quick, clear answer to their demand; must not notice whether a person or the automation replies | Low | High | Keep informed | No – not a user | PDF, T 1:14:04, 1:51:54 |
| SH-06 | LoDA leadership | Sponsor *(to be validated)* | Wants the demand process to scale and the vision presented for approval | High | Low | Keep satisfied | No | T 2:18:44 |
| SH-07 | IT (hosting, cloud approval) | Supplier | Provides on-premise hosting; decides whether cloud can be used | High | Low | Keep satisfied | No | T 1:41:51, 1:42:34 |

## 2. Influence / Interest Grid

| | Low interest | High interest |
|---|---|---|
| **High influence** | Keep satisfied: SH-03, SH-06, SH-07 | Manage closely: SH-01, SH-02, SH-04 |
| **Low influence** | Monitor: – | Keep informed: SH-05 |

## 3. Open Questions

1. Who is the formal sponsor – LoDA leadership as a group, or a named role? *(assumed: LoDA leadership – to be validated)*
2. Are InfoSec / Data Protection stakeholders for this product? Not mentioned in the sources. *(assumed: not yet – to be validated)*
3. Does the Technical Architect also take part in feasibility (with the Product Team), or only in the complexity check? *(assumed: complexity check only, per the PDF – to be validated)*
