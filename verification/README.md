# Examine the preference reader

The profiles in this directory govern the newly introduced preference path and
its tests. They do not pronounce the older Python tree compliant with a new
standard, change the repository's `unittest` convention, or add a runtime
dependency to the distributed skill.

Use the existing project verification environment when available. The recorded
development interpreter is Python `3.13.15`; the runtime floor remains `3.10`.
The prepared tool versions are Ruff `0.16.9`, Pyright `1.1.407`, and Coverage.py
`7.11.0`. Dependency preparation is a separate, explicitly networked setup step;
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
python3 -O -m unittest discover -s tests -p 'test_preference*.py'
```

The type profile must examine all ten named source and test files. An empty
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
`S603` examinations and the inapplicable `pytest` conversion recommendations are
listed in [exceptions.json](exceptions.json), with their reasons, risks, owner,
expiry and required independent examination. No approval is inferred from an
entry whose approver remains pending.

Repository-wide migration of legacy formatting and typing, a complete
rule-to-gate inventory, automated exception-orphan checks, separate coverage
gates, and retained tool-calibration gates remain pending. So do exact patch
pins for the existing runtime matrix and a complete dependency-audit gate.
The maintainers own those adoption decisions; review this inventory when the
preference PR is examined and before extending its scope. Do not describe these
pending mechanisms as implemented enforcement or full standard compliance.
