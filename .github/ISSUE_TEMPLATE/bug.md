---
name: "House bug"
about: "A symptom with no known cause."
title: ""
labels: []
assignees: []
---

<!--
Use when there is a symptom and no known cause. No Proposed Solution at filing; Diagnosis is required before fix work starts.

Use this house template for the complete issue. Keep all section headings.
Replace placeholders with facts. Use "none" or "not applicable, because ..." where appropriate.
Keep sections designated empty at filing empty until the required work occurs.
Use period-appropriate narrative prose without blockquotes in GitHub issues.
Use ASD-STE100 guidance for technical instructions; preserve exact identifiers.

-->

```yaml
.dag: issue-dag/2
.id: flyingrobots/baker-street#<number assigned after filing>
.kind: task
.type: bug
.blocked_by: []
title: "<issue title>"
area: "<affected paths or surfaces>"
source: "<request or evidence>"
template: house bug
```

# Bug

```text
You work in the flyingrobots/baker-street repository. Complete this bug task.

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

## 2. Observed
What happens now.
## 2b. Expected
What should happen instead.
## 2c. Reproduction
Steps, or: not reproduced, observed in production at <time> from <source>.
## 2d. Blast radius
Who is affected, as a population.
How many, with the query that produced the number, marked observed or estimated.
Since when.
Downstream: what consumed the wrong value.
## 2e. Hypothesis
What I think is happening, and the observation that would kill it.
## 2f. Diagnosis
Empty at filing. Required before any fix work starts.

## 3. Prerequisites
- [ ]

## 4. Scope
In:
Out:

## 5. Why now
## 6. Risks
## 7. Definition of Done
A regression test that fails before the fix and passes after it.
## 8. Stakeholders
## 9. Related Issues
