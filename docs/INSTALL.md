# Install Baker Street

Local installation uses a reviewed source checkout. Its maintained command is
`make install`; the named ZIP serves the separate API upload route below.

Python 3.10+ runs the optional packet builder. The skill itself is instructions
for an agent host. It does not provide a model, tool permissions, or a sandbox.

## Install from a reviewed checkout

> Holmes put the complete packet beside the visitor's unfinished copy.
> "Keep the earlier papers," he said. "The new set must stand complete
> before its first sheet is offered to the reader."

Use a reviewed source checkout containing `scripts/install.py`. A downloaded
skill ZIP alone does not supply this source-installation command. From the
checkout's root, with Python `3.10` or later on `PATH`, run:

```sh
make install
```

The default is `~/.agents/skills/baker-street`. To choose an explicit destination,
including one with spaces, run:

```sh
python3 -m scripts.install --destination '/absolute/path/agent skills/baker-street'
```

For `make install`, the dedicated environment choice is:

```sh
BAKER_STREET_DESTINATION='/absolute/path/agent skills/baker-street' make install
```

The explicit argument precedes `BAKER_STREET_DESTINATION`, which precedes the
default. Relative choices are relative to the current directory. The command
prints one `JSON` object containing the actual installed `entrypoint`; refusal
returns status `2` with its account on standard error. An empty choice is refused.
No dependency or agent configuration is installed or altered.

This route requires POSIX directory descriptors, as supplied by supported Linux
and macOS hosts. Existing parent directories must not be symbolic links. Where
an ordinary temporary-directory name is a system link, choose its physical path.
The final destination must be absent: an existing file, directory or link is
refused. Missing parents are created deliberately. Before any destination is
created, every file in the reviewed release inclusion list is read and admitted:
regular files only, at most one MiB per file and four MiB together. Source links
are refused. The copied files and per-file `SHA256SUMS` match a release built from
the same source bytes. The general review skill excludes evaluation answers,
private papers and the separate correspondence guide.

Each destination file is created exclusively and its bytes are read back.
The incomplete marker remains while the resources are copied; `SKILL.md` is
published only after those checks. On success, the temporary names are removed.
The tests admit the observed files and directory identities. Concurrent alteration
by another writer and recovery after loss of power remain outside their scope.

For an upgrade, preserve or move the earlier installation before choosing the
new destination. On failure, inspect the reported destination and any
`.baker-street-incomplete` marker; the command retains its partial files and any
created parents. A complete `SKILL.md` may already exist if interruption followed
its publication. A second attempt refuses that occupied destination. Preserve
the uncertain copy and choose a fresh destination rather than treating a failed
attempt as a successful installation.

## Codex CLI, IDE extension, and desktop Codex

For a project-only installation, select
`/absolute/path/to/your/project/.agents/skills/baker-street` explicitly.
In Codex, type `$baker-street` or select it through `/skills`.
Restart the host if it has not detected the new folder.
These locations and explicit invocation follow the
[official local skill instructions](https://learn.chatgpt.com/docs/build-skills).

## ChatGPT desktop / Work

Use the same local installation for a desktop project, open that project in
the desktop app, and open **Skills** in the sidebar. Select Baker Street with
the `@` picker for ChatGPT or `$` for Codex. If the local skill is not exposed
in your Work context, use the desktop Codex project containing the installed
folder; do not assume an attached ZIP registers a skill. Local skill support
and invocation are described in [Build skills](https://learn.chatgpt.com/docs/build-skills).

This release is a filesystem skill, not a published ChatGPT plugin. ChatGPT
web/mobile plugin distribution and an Atlas-specific installation are not
provided or verified here. The original metadata's product labels are not
evidence of a separate installer for those surfaces.

## Download a pinned skill package

The supplied packet, case, ledger, mutant and evaluation instruments require
Python 3.10 or later. The mutant instrument additionally requires POSIX process
groups and Git support for explicit object-format discovery and initialization.
These download and extraction instructions do not check those requirements.
The host must supply them before the instruments can be used.

Download `baker-street-v3.3.0.zip` and `SHA256SUMS` from the
[v3.3.0 release](https://github.com/flyingrobots/baker-street/releases/tag/v3.3.0).
With GitHub CLI, run in a new download directory:

```sh
gh release download v3.3.0 --repo flyingrobots/baker-street --pattern 'baker-street-v3.3.0.zip' --pattern SHA256SUMS
```

The ZIP contains one `baker-street/` folder: the skill, its required resources,
license, attribution, and per-file checksums. The automatically generated GitHub
source archives contain the entire evaluator repository. The named skill ZIP
is used by the API upload instructions below and for inspection of the distribution.

The repository’s [correspondence guide](../skills/house-correspondence/SKILL.md)
and [prospective independent examination](INDEPENDENT-TRIAL.md) accompany this
edition in the source repository. They are not included in the general review
ZIP. The writing guide does not impose the house manner upon unrelated reviews.

## OpenAI Responses API

For accounts with API Skills access, upload the same ZIP:

```sh
curl --fail-with-body https://api.openai.com/v1/skills \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./baker-street-v3.3.0.zip;type=application/zip'
```

Retain the returned skill ID and version. Retrieve
`GET /v1/skills/{skill_id}/versions/{version}` until that version is available,
using bounded retries for a transient 404. Attach it to a Responses shell tool:

```json
{
  "type": "shell",
  "environment": {
    "type": "container_auto",
    "skills": [
      {"type": "skill_reference", "skill_id": "<returned-id>", "version": "<returned-version>"}
    ]
  }
}
```

Use an explicit input such as `Use Baker Street to review the supplied source
in triage, plain voice.` Configure the model and source files in your own
Responses request. See the [official API Skills guide](https://developers.openai.com/api/docs/guides/tools-skills).
This repository tests archive contents and packet assembly; it does not claim
a live API upload or every host's discovery UI was exercised.

## Try a small case

Follow the [minimal worked example](../examples/triage/README.md). To build the
release locally, use a new output directory:

```sh
python3 scripts/build_release.py --version 3.3.0 --out .runs/release-v3.3.0
```

The builder fails on missing required resources, symlinked inputs, or an existing
output directory. Identical source bytes produce identical archive bytes.
