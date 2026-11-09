# Examine the maintained installation

The installation profiles govern `scripts/install.py`, `scripts/install_paths.py`,
`scripts/release_payload.py`, the named installation tests, and
`check_install_coverage.py`. The type profile names eleven files. The older release
builder retains its existing source conventions; this amendment shares its
payload reader and preserves its archive bytes for unchanged selected inputs.
It does not pronounce the whole repository compliant with a new standard.

Use the prepared verification environment with Python `3.13.15`, Ruff `0.16.9`,
Pyright `1.1.407` and Coverage.py `7.11.0`. The installation command itself requires
Python `3.10` or later and the documented POSIX operations. Tool preparation is a
separate operation using the hashed `requirements.txt`; tests install nothing.

From the repository root:

```sh
ruff format --check --config verification/install-ruff.toml .
ruff check --config verification/install-ruff.toml .
pyright --project verification/install-pyrightconfig.json
make test
python3 -O -m unittest discover -s tests -p 'test_install*.py'
```

The CI job measures the complete three-module installation component, including
one actual command invocation, and measures the admission instrument separately.
It combines the separate process measurements before producing the report.
`python3 -m verification.check_install_coverage REPORT` requires exact source
inventories, nonempty modules, no exclusions, and separate statement and branch
floors of 95 percent in each group. Integer comparisons prevent rounding from
concealing a deficiency. These measurements and fixed refusal trials establish
the stated obligations; they do not establish general correctness or authenticate
an arbitrarily supplied report. CI retains its actual producer report for seven days.

`install-exceptions.json` records one diagnostic per exception: the fixed process
call in the owned fixture helper and the named `unittest` assertion and exception
contexts. The process exception uses the prescribed preceding identified reason.
The named framework exceptions retain every other source rule. Their pending
approver fields confer no approval; the required PR examination must assess them.
The correspondence records in this file are examined by the reviewer rather than
by a newly claimed general exception-registry instrument.

The locality trial limits each installation source and test file to 300 nonblank,
non-comment physical lines, including docstrings. No locality exception is claimed;
the target remains 200. The source-inventory trials prevent added installation
modules from silently escaping the fixed coverage scope. The installed packet
and case trials assemble synthetic records outside the checkout; they do not
claim that an agent conducted those synthetic investigations.
