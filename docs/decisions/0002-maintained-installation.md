# Install the skill from a reviewed checkout

Status: design recorded for [issue #29](https://github.com/flyingrobots/baker-street/issues/29);
implementation and its execution evidence remain pending.

## Occasion

> The visitor had copied every direction save the final sheet. Holmes laid the
> complete packet beside his copy. "Our next visitor need not copy these sheets
> at all," he remarked. "Let him receive the complete packet, and keep his
> earlier papers beside it."

The [installation guide](../INSTALL.md) presently asks the reader to copy an
inline installer. Provide `make install` from a reviewed checkout, with
`python3 -m scripts.install --destination PATH` for an explicit destination.
The source of the installed files is that checkout's reviewed inclusion list.

## Decision

Reuse `SKILL_FILES` and the `SHA256SUMS` contract for individual files in
[the release builder](../../scripts/build_release.py). Share the construction
of the bounded payload where necessary; retain its existing archive bytes for
unchanged inputs. The installed tree must contain exactly the general review
payload and its manifest. Evaluation answers, private cases, transcripts and
the correspondence guide remain outside that inclusion list.

The default destination is `~/.agents/skills/baker-street`, as prescribed by the
existing guide. An explicit `--destination` takes precedence over the dedicated
`BAKER_STREET_DESTINATION` environment variable, which takes precedence over
the default. `make install` invokes the maintained command directly. It must
not interpolate an operator's path into shell command text.

This command installs source selected by the reviewed inclusion list. The named
release ZIP remains the distribution format. A separate received-archive parser
is unnecessary for the chosen installation from source; the guide must make
the required checkout clear rather than retain a competing inline installer.
No repository preference is needed to install the skill.

## Destination and interruption

Support the POSIX operations on directory descriptors available on Linux
and macOS hosts. Refuse an unavailable required operation before writing.
Obtain and check the complete bounded source payload before reserving a new
destination. Refuse an occupied destination, including a symbolic link. Open
existing parent directories without following symbolic links, create missing
parents deliberately, and reserve the final directory exclusively.

Keep writes relative to the owned directory descriptors. Create each file
exclusively; never truncate an existing file or replace an occupied name.
Retain a marker for an incomplete installation while copying. Prepare `SKILL.md`
under a private name and publish that entry point only after the complete
payload and checksums have been written and checked, using an operation which
refuses an occupied final name.

On success, remove the temporary names and print a `JSON` account containing
the actual installed entry point. Escaping must preserve path characters even
when the receiving stream has a restricted alphabet. On failure, return a
failure status and identify any retained incomplete destination. Created
parents may remain. A complete entry point may already exist if interruption
follows its publication; the marker requires inspection rather than a claim
that publication was undone. Preserve uncertain output and refuse a subsequent
installation into that occupied location. An upgrade requires the operator to
preserve or move the earlier installation first.

## Alternatives

Continue the copied example: corrections would not reach the private copies.
Overwrite the old tree: a failed copy could destroy the working installation.
Publish the entry point before its resources: the host could discover an
incomplete skill. Add distribution through a package manager: that is separate work.

## Required evidence

Exercise the actual maintained command with an owned temporary destination,
including spaces, then run its installed packet and case commands outside the
checkout. Compare the installed file inventory and manifest with the actual
release builder's output. Preserve byte inventories before and after trials of
occupied and unsafe destinations, missing source, a symbolic link alias and a
bounded interrupted copy. Confirm refusal leaves prior bytes intact and that
an incomplete copy is never reported as successful. Test the default path by
computation; do not install into the developer's real home during verification.
