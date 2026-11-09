---
name: "House decision"
about: "Known facts; choose an option and name the decision owner."
title: ""
labels: []
assignees: []
---

<!--
Use when the facts are known and the open item is which option, and who says so.

Use this house template for the complete issue. Keep all section headings.
Replace placeholders with facts. Use "none" or "not applicable, because ..." where appropriate.
Write title, area, and source as valid YAML strings.
Escape embedded double quotes and backslashes within double-quoted values.
Example: title: "Correct \"none\" in C:\\cases"
Keep sections designated empty at filing empty until the required work occurs.
Use period-appropriate narrative prose without blockquotes in GitHub issues.
Use ASD-STE100 guidance for technical instructions; preserve exact identifiers.

-->

```yaml
.dag: issue-dag/2
.id: flyingrobots/baker-street#<number assigned after filing>
.kind: task
.type: decision
.blocked_by: []
title: "<issue title>"
area: "<affected paths or surfaces>"
source: "<request or evidence>"
template: house decision
```

# Decision

```text
You work in the flyingrobots/baker-street repository. Complete this decision task.

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

## 2. The choice
A question with named options.
## 2b. Options and consequences
One line each.
## 2c. Rests on
Evidence, cited by something immutable, or a person, named.
## 2d. Who decides, and by when
## 2e. What is blocked until then
## 2f. Reversible

## 3. Prerequisites
- [ ]

## 4. Scope
In:
Out:

## 5. Why now
## 6. Risks
## 7. Definition of Done
Recorded where the next reader will find it, which is usually not only this card.
## 8. Stakeholders
## 9. Related Issues
