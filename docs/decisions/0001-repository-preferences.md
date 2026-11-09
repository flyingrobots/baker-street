# Repository preferences are bounded data

Status: accepted for implementation under [issue #28](https://github.com/flyingrobots/baker-street/issues/28).
No reader or integration is delivered by this decision alone.

## Decision

Read `.bakerstreetrc` only at the Git root identified for the supplied repository.
Do not search a home directory or walk unrelated ancestors for preference files.
For a linked worktree, use its own worktree root, not the shared Git authority.
An enclosing repository's preferences do not govern a separately identified one.

Use UTF-8 JSON with an object at its root and these fields:

| Field | Contract |
| --- | --- |
| `schema_version` | Required exact integer `1`; a Boolean is not an integer version |
| `plain` | Optional exact Boolean; no coercion from strings or integers |
| `tier` | Optional `triage`, `focused` or `standard` |
| `case_directory` | Optional nonempty relative subdirectory beneath an operator-supplied case root |

Example of the accepted preference format:

```json
{"schema_version":1,"plain":true,"tier":"focused","case_directory":"reviews"}
```

Reject unknown fields, duplicate keys, arrays, nested objects, nonfinite numbers,
floating-point versions, malformed UTF-8 and unsupported versions. Bound the
file to 8192 bytes before decoding and reject nesting before recursive decoding.
Keep a finite bound on numeric tokens. Errors identify the disputed setting
without copying private file contents into the diagnostic.

The POSIX reader will open the preference file without following a final
symlink, refuse nonregular files without waiting upon a pipe, and retain one
bounded snapshot. If those admission controls are unavailable, refuse with an
explicit unsupported-platform diagnostic. Linux and macOS are the initial
validation targets; no Windows reader claim is made by this decision.

## Precedence and actual application

Validate the whole file before applying any preference. An explicit override
does not conceal a malformed or unsafe file. Apply ordinary defaults first,
then explicit header fields, then explicit invocation options. Governing
instructions and host safeguards remain above every one of these choices.
An absent preference file preserves the existing header and ordinary defaults.

The canonical reader will support preparing an actual packet header, rather
than merely printing advisory prose. It will map the selected plain manner and
tier into that header and preserve unrelated header fields. The packet builder
will consume the prepared header through its existing interface. Document and
exercise that complete route, including use from the installed skill.

For a preference-derived destination, require a trusted operator to supply the
case root. Reject absolute paths, traversal components, empty components and
control characters in `case_directory`. Resolve it beneath that root, refuse an
escape through an existing symlink, and refuse a destination inside the subject
checkout or shared Git authority. Resolve existing directory ancestors; refuse
unresolved link cycles and non-directory ancestors. Missing directory tails
remain permitted. A supplied
header's explicit destination is an invocation input, not a permission granted
by the preference file.

The reader creates no directory and writes no case. Its output is data for the
commission. A later writer must establish its own destination admission at the
actual effect point; a prior resolution does not protect against later changes
to filesystem names. No publication, execution or write permission is inferred
from this file or from its normalized header.

## Alternatives and consequences

YAML would add a parser dependency and a larger admission contract for four
flat fields. TOML has no standard-library reader on the retained Python 3.10
floor. Executable settings would give preferences an authority they do not need.
JSON keeps the initial reader within the standard library.

An arbitrary absolute destination is convenient but would allow inspected
repository data to select another part of the host. Requiring an operator's
case root preserves a useful directory preference without granting that choice.
It adds one explicit input when the file supplies a destination; a file which
only chooses manner or tier needs no case root.

Do not add provider commands, credentials, publication switches, permission
overrides or resource-limit exemptions. The Action's trusted adapter selection
is a separate operator contract under issue #30.

## Evidence owed before admission

Exercise strict decoding and refusal bounds, root discovery in ordinary and
linked worktrees, precedence including explicit false, absent-file preservation,
unsafe and symlinked paths, and preparation of a packet which actually receives
the selected values. Calibrate the behavioural checks with diagnostic faults;
an import failure alone supplies no such evidence.

Run the relevant full suite and supported CI interpreters. Check the new reader
and its tests with the prepared formatting, lint, typing and coverage tools,
including the separate critical-component coverage dimensions. Record existing
legacy enforcement gaps without representing them as implemented checks.
No parser, installed-artifact result or conformance result is asserted here.
