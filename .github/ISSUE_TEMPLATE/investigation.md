---
name: "House investigation"
about: "An unfamiliar system that needs a map of questions."
title: ""
labels: []
assignees: []
---

<!--
Use when a system matters but we do not yet know what questions to ask about it.

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
.type: investigation
.blocked_by: []
title: "<issue title>"
area: "<affected paths or surfaces>"
source: "<request or evidence>"
template: house investigation
```

# Investigation

```text
You work in the flyingrobots/baker-street repository. Complete this investigation task.

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
The system, and why we are taking it on.

## 2. What we do not understand
The area, not a question. If you have one question, file Research instead.
## 2b. Where to look
Surfaces, repositories, dashboards, people.
## 2c. Time box
## 2d. Findings
Empty at filing. One line per finding, each with the card it became.

## 3. Prerequisites
- [ ]

## 4. Scope
In:
Out:

## 5. Why now
## 6. Risks
## 7. Definition of Done
The map exists and every finding has a typed card.
## 8. Stakeholders
## 9. Related Issues
