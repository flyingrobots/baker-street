---
name: "House task"
about: "The flat nine-section card for work without a suitable typed card."
title: ""
labels: []
assignees: []
---

<!--
The plain version every card we author or are assigned carries, as James set it out on 2026-09-23. The typed templates in this folder refine the middle of it by card type. There is deliberately no effort or estimate section; sizing belongs to Scope (and to Blast radius for a Bug).

Use this house template for the complete issue. Keep all section headings.
Replace placeholders with facts. Use "none" or "not applicable, because ..." where appropriate.
Keep sections designated empty at filing empty until the required work occurs.
Use period-appropriate narrative prose without blockquotes in GitHub issues.
Use ASD-STE100 guidance for technical instructions; preserve exact identifiers.
Notes:
- Acceptance Criteria and Definition of Done are different: the first is what the result must satisfy, the second is the signal to stop, usually including recording the result.
- Write "none" or "not applicable, because X" instead of padding a section.
- Stakeholders names people where the record supports a name, and says why each cares.
-->

```yaml
.dag: issue-dag/2
.id: flyingrobots/baker-street#<number assigned after filing>
.kind: task
.type: task
.blocked_by: []
title: "<issue title>"
area: "<affected paths or surfaces>"
source: "<request or evidence>"
template: house nine-section-card
```

# Task

```text
You work in the flyingrobots/baker-street repository. Complete this task task.

Goal: <one observable outcome>
Read: <required sources and repository instructions>
Prerequisites: <required prior results and reasons, or none>
Scope: <permitted changes and exclusions>
Steps: <ordered actions appropriate to this card type>
Validation: <checks and evidence required by this card>
Stop when: <the authorized stopping point and required deliverables>

Follow every completion criterion below. Do not bypass Git hooks.
Do not publish, merge, or perform other actions without authorization.
```

## 1. Background Context
What this concerns.

## 2. Problem Description
What is broken or missing.

## 3. Proposed Solution
How to fix it.

## 4. Prerequisites
Before we start, these must be true.
- [ ]

## 5. Scope
In:
Out:

## 6. Acceptance Criteria
What must be true before this is considered finished.

## 7. Definition of Done
How to know when to stop.

## 8. Test Plan
Golden:
Edges:
Known failure modes:
Fuzz and stress:

## 9. Stakeholders
Named people or teams who care about this issue, and why.
