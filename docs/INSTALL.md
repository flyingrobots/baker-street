# Install Baker Street

Python 3.10+ runs the optional packet builder. The skill itself is instructions
for an agent host. It does not provide a model, tool permissions, or a sandbox.

## Download a pinned skill package

Download `baker-street-v3.1.0.zip` and `SHA256SUMS` from the
[v3.1.0 release](https://github.com/flyingrobots/baker-street/releases/tag/v3.1.0).
With GitHub CLI, run in a new download directory:

```sh
gh release download v3.1.0 --repo flyingrobots/baker-street --pattern 'baker-street-v3.1.0.zip' --pattern SHA256SUMS
```

The ZIP contains one `baker-street/` folder: the skill, its required resources,
license, attribution, and per-file checksums. The automatically generated GitHub
source archives contain the entire evaluator repository; use the named skill
ZIP for installation.

## Codex CLI, IDE extension, and desktop Codex

Save this as `install.py` beside the downloaded files and run `python3 install.py`:

```python
import hashlib
from pathlib import Path
import zipfile

archive = Path('baker-street-v3.1.0.zip')
expected, filename = Path('SHA256SUMS').read_text().strip().split('  ', 1)
if filename != archive.name or hashlib.sha256(archive.read_bytes()).hexdigest() != expected:
    raise SystemExit('Archive checksum mismatch')
parent = Path.home() / '.agents' / 'skills'
if (parent / 'baker-street').exists():
    raise SystemExit('Baker Street already exists; preserve or move it before installing')
with zipfile.ZipFile(archive) as bundle:
    bundle.extractall(parent)
print(parent / 'baker-street' / 'SKILL.md')
```

For a project-only installation, change `parent` to
`Path('/absolute/path/to/your/project/.agents/skills')`. This prevents mixed
versions by refusing an existing installation. Preserve the old folder before
an upgrade. In Codex, type `$baker-street` or select it through `/skills`.
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

## OpenAI Responses API

For accounts with API Skills access, upload the same ZIP:

```sh
curl --fail-with-body https://api.openai.com/v1/skills \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F 'files=@./baker-street-v3.1.0.zip;type=application/zip'
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
python3 scripts/build_release.py --version 3.1.0 --out .runs/release-v3.1.0
```

The builder fails on missing required resources, symlinked inputs, or an existing
output directory. Identical source bytes produce identical archive bytes.
