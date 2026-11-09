# Prepare a case with repository preferences

> The client's standing instructions lay beside the new commission. Holmes read
> both before taking up his pen. “The former may spare us a repeated choice,” he
> said, “but they cannot enlarge the authority of the latter.”

Place `.bakerstreetrc` at the subject's Git worktree root. The initial reader
supports Linux and macOS with Python 3.10 or later and Git which understands
`rev-parse --path-format=absolute`. The file contains ordinary defaults only:

```json
{"schema_version":1,"plain":true,"tier":"focused","case_directory":"reviews"}
```

From the installed skill directory, prepare the actual case header:

```sh
python3 -m scripts.prepare_header \
  --repository /path/to/subject \
  --header /path/to/header.json \
  --case-root /path/to/cases > /path/to/prepared-header.json
python3 scripts/build_packet.py --role holmes \
  --header /path/to/prepared-header.json --out /path/to/packets/holmes.md
```

The paths are placeholders for the operator's actual subject, inputs and output
locations. Run the packet command only after preparation exits successfully.
The shell may leave an empty redirected file after a refusal; it is not a
prepared header. The command itself creates no directory and writes no case.

The prepared header has `plain: true`, `tier: focused`, and a `write_directory`
of `/path/to/cases/reviews`, unless the supplied header explicitly chooses those
fields. Other header fields retain their values. The packet builder receives
the prepared header through its existing `--header` option.

## Which instruction takes precedence?

For `plain` and `tier`, apply these choices in order:

1. Ordinary defaults: `plain: false`, `tier: triage`.
2. The subject's `.bakerstreetrc` defaults.
3. Fields explicitly present in the supplied header.
4. Invocation options: `--plain`, `--no-plain`, and `--tier`.

Governing instructions and host safeguards remain above every ordinary choice.
The complete file must pass admission even when an explicit choice supersedes
one of its values. An invalid header choice is likewise refused rather than
silently repaired by an invocation option.

The packet builder's printed template already contains `plain`, `tier`, and
`write_directory`. Omit those fields from the input header when they are to
come from repository preferences. Retaining them is an explicit header choice.
The header must still supply the commission's required authority, evidence,
scope and other particulars; defaults do not invent those particulars.

An explicit header `write_directory` supersedes the directory preference.
Otherwise, `case_directory` requires `--case-root`; its resolved destination
must lie beneath that root and outside the subject checkout and shared Git
authority. Existing links cannot take it outside those bounds. Preparation
checks the physical identity of existing ancestors as well as their spelling;
a differently capitalised alias of the subject or Git authority is not outside
it. Preparation refuses unresolved link cycles and non-directory ancestors.
The later writer must repeat destination admission when it acts: an earlier
resolution does not protect against a later change to a filesystem name.

## File contract and refusals

| Field | Accepted value |
| --- | --- |
| `schema_version` | Required exact integer `1` |
| `plain` | Optional Boolean; explicit `false` is preserved |
| `tier` | Optional `triage`, `focused`, or `standard` |
| `case_directory` | Optional nonempty relative subdirectory, at most 1024 UTF-8 bytes and sixteen components |

Read only the file at the identified worktree root. Subdirectories and enclosing
or home directories supply no alternative file. A linked worktree uses its own
root; a separately identified nested repository does not inherit the outer
repository's preferences. An absent file supplies no file defaults.

The preference file is flat UTF-8 JSON, at most 8192 bytes. Duplicate or unknown
fields, nested containers, optional `null`, unsupported versions, floats,
nonfinite numbers and integer tokens exceeding eight characters are refused.
Final symlinks and nonregular files, including pipes, are refused. Absolute
directory names, traversal, empty or dot components, control characters
(`U+0000`–`U+001F` and `U+007F`–`U+009F`), backslashes, and drive or scheme
prefixes are refused.

The explicit header input is bounded to 262144 bytes and integer tokens to 128
characters. It must be a JSON object. Nonfinite values and strings which cannot
be written as UTF-8 are refused; excessive
nesting may be refused. The header remains an operator-supplied commission, not
an instruction discovered in the subject.

The Git-root inquiry has five seconds and 32768 output bytes. Root names with
newlines are unsupported. The reader requires POSIX file-admission facilities;
there is no Windows-reader claim. Refusal exits with code `2`, writes a brief
diagnostic to stderr, and emits no partial header. Correct the input or supply
the missing operator choice before trying again.

No command, credential, permission, publication switch, or exemption from limits
is admitted through `.bakerstreetrc`. The Action's operator-chosen execution
adapter is a separate contract. For the design grounds and remaining proof
obligations, see the [preference decision](decisions/0001-repository-preferences.md).
