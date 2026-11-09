# Examine the preference reader

The profiles in this directory govern the newly introduced preference path and
its tests. They do not pronounce the older Python tree compliant with a new
standard, change the repository's `unittest` convention, or add a runtime
dependency to the distributed skill.

Use the existing project verification environment when available. The recorded
development interpreter is Python `3.13.15`; the runtime floor remains `3.10`.
The prepared tool versions are Ruff `0.16.9`, Pyright `1.1.407`, and Coverage.py
`7.11.0`. The repository-only admission command requires Python `3.13`; it is
excluded from the installed skill and does not raise the skill's runtime floor.
Dependency preparation is a separate, explicitly networked setup step;
tests must not install missing tools or repair their environment. The exact
tool resolution and its artifact hashes are in `requirements.txt`; prepare it
with `python3 -m pip install --require-hashes -r verification/requirements.txt`
inside the owned environment. Regeneration uses the pinned interpreter and
`uv pip compile verification/requirements.in --python 3.13.15 --generate-hashes
--only-binary :all: --no-header --output-file verification/requirements.txt`.

From the repository root, with that environment on `PATH`:

```sh
ruff format --check --config verification/ruff.toml .
ruff check --config verification/ruff.toml .
pyright --project verification/pyrightconfig.json
python3 -m unittest discover -s tests -v
coverage erase
coverage run --branch --source=scripts.preference_schema,scripts.preference_file,scripts.preference_roots,scripts.preference_header,scripts.prepare_header,verification.check_preferences,verification.preference_coverage,verification.preference_exceptions,verification.preference_proofs,verification.preference_suppressions -m unittest discover -s tests -p 'test_preference*.py'
coverage json -o preference-coverage.json
python3 -m verification.check_preferences --coverage preference-coverage.json
python3 -O -m unittest discover -s tests -p 'test_preference*.py'
```

The type profile must examine all twenty-two named source and test files. An empty
selection is not a successful examination. The installed-package test builds
the actual skill ZIP, extracts it outside the source checkout, removes inherited
`PYTHONPATH` and `PYTHONHOME`, and passes the prepared header to the installed
packet builder. It does not claim that an agent has performed a review.

The new runtime component comprises `preference_schema.py`, `preference_file.py`,
`preference_roots.py`, `preference_header.py`, and `prepare_header.py`. Measure
statement and branch coverage separately across this complete component; each
dimension requires at least 95 percent. Inspect each file's uncovered paths as
well. A combined percentage alone is insufficient. Retain the JSON inventory
and exact counts; an absent or empty expected module is a failed measurement.
The admission instrument is a second, separately measured scope with the same
two floors. Its five modules have distinct duties: `check_preferences.py` owns
the command, `preference_proofs.py` owns bounded reads and primitive admission,
`preference_coverage.py` owns source inventories and coverage,
`preference_suppressions.py` locates source symbols and comments, and
`preference_exceptions.py` reconciles registry and configuration records. Its
result cannot compensate for a deficit in the five runtime
modules. The command compares integer counts without rounding, requires branch
measurement, and refuses excluded lines, empty modules and changed inventories.

The CI quality job executes these commands and retains `preference-coverage.json`
as the `preference-coverage` artifact for seven days, including on failure when a
report was produced. The retained producer projection in
[coverage-7.11.json](fixtures/coverage-7.11.json) checks the report format. Its
frozen counts describe an earlier authoring measurement; they are not current
coverage evidence.

The bounded assertion trials belong in the case evidence. A failing import,
missing dependency or unrelated exception does not establish the intended RED.
Keep the green control, exact source fault, named assertion failure, source
identity and command. These are selected fault trials, not a completeness or
mutation-score claim.

## Recorded limits of enforcement

The formatting, lint and strict-type profiles and their CI job are implemented
for the named preference scope. Their results are authoring evidence until the
candidate's CI executes them. The existing CI matrix supplies the full
behavioural suite. The scoped
`S603` examinations are confined to five identified calls. Each has one
`# noqa: S603` comment and an immediately preceding
`# policy-exception: EX-ID -- factual reason` comment, resolved to the registry.
The former trailing-identity form, detached reasons, empty reasons and combined
diagnostics are refused. Ordinary remarks which mention a diagnostic are not
suppression directives. Each exception in
[exceptions.json](exceptions.json) names one diagnostic. The inapplicable
`PT009` and `PT027` recommendations are confined to the named `unittest` files
and classes, with identities and reasons beside their configuration entries.
Unused framework exceptions have been removed. The registry retains reasons,
risks, owner, expiry and required independent examination. No approval is inferred
from an entry whose approver remains pending.

The policy trials count nonblank physical lines other than full-line comments,
including docstrings, throughout the preference source and tests. No file in
that scope has an approved locality exception; each must remain at or below
300 such lines. The target remains 200. This check establishes the file-size
limit; it does not purport to measure every function or complexity requirement.

The policy trials check the single-diagnostic rule, the prohibition on whole-file
`S603` exceptions and the adjacent identities at the calls. A fixed unrelated
process-call input was also passed to Ruff under each of the four formerly
waived filenames: each now receives `S603`. This remains retained authoring
evidence rather than a claim that a future unrelated call has been reviewed.

The admission command reconciles source annotations and the parsed Ruff
configuration with the registry in both directions. It refuses missing,
orphaned, duplicated and expired entries; unknown paths or absent symbols;
whole-file process exceptions; and missing adjacent identities and reasons.
Parent `owner`, `tracking`, `review_condition` and `expires` fields are explicit
defaults for entries which do not override them. Metadata and correspondence
checks do not determine whether a reason is sound or an approver has consented.
That judgment remains part of the required PR examination.

Repository-wide migration of legacy formatting and typing, a complete
rule-to-gate inventory, and retained general tool-calibration gates remain
pending. So do exact patch pins for the existing runtime matrix and a complete
dependency-audit gate.
The maintainers own those adoption decisions; review this inventory when the
preference PR is examined and before extending its scope. Do not describe these
pending mechanisms as implemented enforcement or full standard compliance.
