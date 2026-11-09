# Agent working rules

## Fix review findings with RED→GREEN

Fix every issue raised in a pull-request review, whether by a person or a bot, with its own RED→GREEN evidence. This applies to every valid finding, including follow-ups, except a finding the user has explicitly accepted (ACCEPTED) or that was withdrawn (WITHDRAWN). For each one:

1. Write the test first. Run `make test` and record that it fails for the reason the finding names.
2. Make the smallest fix that resolves that finding.
3. Run `make test` again and record that every test passes.
4. Commit each finding separately. When one fix resolves several findings, or code and its tests must land together, make one coherent commit and record each finding's RED and GREEN in it. Put the RED and GREEN results in the commit message, and reply with the commit in each finding's review thread, or in the thread where the finding was posted.

This rule also applies to fixes that are not code:

- **Rule text in `SKILL.md`, `references/` or `roles/`:** add a test that reads the file and checks for the rule. It must fail before the edit and pass after it.
- **A pull-request body or changelog:** no repository test can fail. RED is the reviewed text, quoted, shown to fail the finding. GREEN is the corrected text, checked against the same finding. Put both in the reply to the review thread, or in the thread where the finding was posted.
- **A fix to a test:** show the gap with a deliberate mutation of the code under test. The mutant must pass the old test and fail the new one, and the real code must pass the new one.

If a finding is not valid, reply with the evidence and make no change. Do not batch unrelated findings into one commit. Do not skip the RED step because a fix looks obvious.

## Review every pull request with Baker Street before merge

Before you merge a pull request, review it with Baker Street, the skill in this repository:

1. Run Baker Street on the pull request at its current head. Choose the smallest tier that fits the risk. Review with the rules on `main`. When the pull request changes Baker Street's own rules, those changes are the target of the review, not its authority.
2. Post a concise decision summary to the GitHub thread of the linked issue. If no issue is linked, post it on the pull request. Redact secrets and private material first. Put the full case file in a collapsed section. Never push private evidence to make a link work.
3. Follow the case. Carry out each required repair under the RED→GREEN rule above. Then review the repaired head again with Baker Street. A case is valid only for the artifacts, environment and scope it recorded, including the head, the pull-request body and the base. When one of them changes, reassess the affected claims in a new case before merge.

### Proportion the examination to the change

Choose the least extensive examination that can responsibly settle the question.
State the chosen tier and the reason for it in the case. Use the three tiers
prescribed by the Baker Street skill:

| Tier | Proper occasion | Examination |
| --- | --- | --- |
| `triage` | A bounded, low-risk question which inspection of the source can settle; ordinarily a small documentary amendment | Holmes examines; the front office reconciles the evidence and checks its own decision; one compact case |
| `focused` | A narrow question which requires several perspectives or experimental trials | Holmes, Watson, and Moriarty inquire; Watson returns to consider repairs; the decision receives a check |
| `standard` | Broad or substantial changes, or consequential questions of security, preservation of stored records, migration, compatibility, or dealings between components | All three inquiries, Watson's return, a fresh checker when available, and separate evidence records |

Judge the consequence of an error, not merely the number of altered lines.
A short amendment to a rule governing permission or preservation may require
more examination than a long correction of spelling. Do not summon every
investigator merely because a pull request exists. If a lesser examination
cannot settle a material question, increase its extent or record the unanswered
obligation. No tier dispenses with the governing evidence and merge requirements.

Merge only when all of these are true at the same head:

- **Baker Street passes:** the latest case for that head has the decision `READY`, and no earlier case on that head left a required repair or investigation unresolved. Do not repeat a review on an unchanged head merely to reach a different decision. A new case on an unchanged head is allowed when something material has changed since the last case: a repair that does not change the head, such as a pull-request body fix; a completed investigation; a change to the base or the environment; or the user's explicit acceptance of, or evidenced dispute with, a named finding. The new case states what changed.
- **Clean:** no review thread is unresolved, and no reviewer still has changes requested or a review in progress, whether a person or a bot. Every finding raised on the pull request, wherever it was posted (a review thread, a review body, a pull-request or issue comment, or a Baker Street case), has been fixed under the rule above, is ACCEPTED by the user or WITHDRAWN, or was answered as not valid with evidence.
- **Green:** every CI check on that head has completed. The `test` jobs from the CI workflow must have reported success, and every other check must have finished as success, skipped or neutral. Any other result, including cancelled or timed out, counts as failing. No checks at all is not green.

If any condition fails, do not merge. Report which condition failed.

## Editorial voice

Every agent MUST use the Holmes-and-Watson writing style for all public-facing
writing in this project. This is a requirement, not an optional flourish or a
rule confined to introductory passages. It applies to newly written and revised
prose, whether prepared locally or submitted through a website, CLI, or API.
It applies equally to delegated agents.

Covered material includes GitHub issue titles, bodies, and comments; pull
request titles, bodies, review comments, and replies; GitHub release notes;
Git commit subjects and bodies; the README; documentation; and any other
material intended for public readers. Local commits are included before they
are pushed. An agent must not assume that a short notice or routine reply is
exempt.

Use only period-appropriate terminology and writing style in authored prose.
Necessary literal commands, paths, identifiers, schema fields, error messages,
and exact evidence quotations must remain accurate. Set those literals apart
with code formatting, code blocks, or quotation, as appropriate; their presence
does not license modern slang or contemporary business prose around them.
Preserve required house-template headings and machine-readable metadata.

- Use original Conan Doyle pastiche: Watson recounts a concrete incident;
  Holmes draws out the principle. Do not present invented lines as quotations
  from Conan Doyle.
- Use only period-appropriate terminology and writing style in the literary
  passages. Keep vocabulary, idiom, syntax, cadence, objects, and comparisons
  faithful to the late-Victorian Holmes-and-Watson setting. Exclude modern
  slang, contemporary business language, and modern rhetorical habits, even
  when individual words existed in the period. Put modern technical terms in
  the plain technical prose that follows, never in Watson's narration or
  Holmes's dialogue.
- Always set literary passages in Markdown blockquotes (`>`), except in
  GitHub issues, where those sections remain ordinary prose. This applies to
  whole narrative sections, not just spoken dialogue.
- Let the story explain the actual engineering constraint. The amended folios
  explain delta review, the commonplace book explains the findings ledger,
  and forged entries in a fair copy explain mutation testing without altering
  the original checkout. Choose equally concrete metaphors for new topics.
- Follow literary passages with plain, exact technical prose. Names, commands,
  schemas, scope, acceptance checks, and authority boundaries must remain
  unambiguous and executable. A metaphor cannot substitute for a requirement
  or evidence.
- In the README, use the literary passage to introduce a principle, then explain
  the deliverable or behavior directly. Keep the practical output easy to find.
- In issues, pair the narrative with structured metadata and a concrete work
  order. Background, motivation, and risks may sustain the narrative voice;
  implementation steps and acceptance criteria must specify the actual work.
- Write review comments and replies in this voice, not merely respectfully
  toward it. Identify the ambiguity, consequence, and proposed correction
  plainly. A brief contribution may use restrained period prose without
  inventing a scene or adding dialogue merely to fill space.
- Keep titles and commit subjects brief and informative in period-appropriate
  language. Place narrative passages in their bodies, using blockquotes except
  in GitHub issue bodies and comments. Pull request bodies and comments retain
  the blockquote rule.
- Only an explicit human instruction may authorize a departure from this
  style. A request for plain voice removes literary flourishes; it does not
  by itself authorize anachronistic terminology or weaken evidence standards.

Before committing or submitting public-facing writing, read the whole text
for period vocabulary, idiom, syntax, and cadence; correct anachronisms;
check the blockquote rule; and confirm that every technical fact remains
exact. Passing a structural check does not establish that the prose meets
this rule.

The atmosphere should help the reader understand and remember the method.
Avoid ornamental passages that obscure the task, unsupported assurances, or
theatrical verdicts that overstate the evidence.

## Required issue templates

Use the house templates in [.github/ISSUE_TEMPLATE](.github/ISSUE_TEMPLATE)
for every new issue. They come from the seven cards supplied in `house.txt`.
This rule applies to the GitHub website, CLI, API, and delegated agents.
Do not file a free-form issue or replace the template with a short summary.
GitHub disables the blank-issue choice. CLI and API authors must check their
issue bodies against the selected template before submission.

- Select `bug.md` for a symptom without a known cause. Do not prescribe a
  solution at filing. Record the diagnosis before fix work starts.
- Select `feature.md` when the required end state is known.
- Select `decision.md` when the facts are known but someone must choose an option.
- Select `investigation.md` to examine a system whose questions are not yet known.
- Select `research.md` for one answerable question that blocks a decision.
- Select `spike.md` for a time-limited trial with disposable code.
- Select `nine-section-card.md` when no typed card fits. Preserve its own
  headings and numbering; they differ from the typed cards.

Keep every heading in the selected card. Complete each applicable section with
facts, evidence, or explicit unknowns. Write `none` or `not applicable, because
...` when appropriate. Keep fields designated empty at filing empty until the
required work occurs. Do not invent evidence, people, counts, or prerequisites.

Start each issue with YAML metadata in a fenced block, then a `# Type` heading
and a fenced `text` execution prompt. GitHub template frontmatter configures
the chooser; it does not replace this issue metadata. Include the issue identity,
kind, type, recorded blockers, title, affected area, source, and template name.
After GitHub assigns the issue number, replace the identity placeholder with it.
Use `.kind: container` for tracking parents. Do not count them as executable tasks.
Record only established prerequisites as blockers, with reasons in the body.

The prompt must specify the outcome, required reading, prerequisites, permitted
scope, actions, validation, deliverables, and authorized stopping point. Keep it
consistent with the card. Distinguish acceptance criteria from the Definition of
Done. If project completion requires a later merge, distinguish that from the
implementer's authorized stopping point. A template grants no publication or
merge authority.

Use ASD-STE100 guidance for clarity in technical instructions where it is
compatible with the mandatory period voice. Preserve exact commands and
identifiers. Do not use controlled prose as an exception to the editorial
rule. In GitHub issues, write narrative sections without blockquotes.

Use the same cards for local task-plan documents, with actual YAML frontmatter
instead of the issue's fenced metadata block. When creating or updating
`ROADMAP.md`, describe the remaining work and how it completes the project.
Start with an executive summary. Follow it with an ordered Markdown checkbox
list of atomic executable tasks. Link each task to its task-plan document.
