"""Apply validated ordinary preferences to an actual case header."""

from pathlib import Path

from scripts.preference_file import case_destination, read_preferences
from scripts.preference_roots import git_roots
from scripts.preference_schema import TIERS, Preferences


def prepare_header(
    repository: Path,
    header: dict[str, object],
    *,
    invocation: Preferences | None = None,
    case_root: Path | None = None,
) -> dict[str, object]:
    """Return a new header, preserving unrelated fields and the original input.

    Validate the whole repository file before considering overrides. For plain
    and tier, apply ordinary defaults, file defaults, explicit header fields,
    then explicit invocation choices. An explicit write_directory in the header
    supersedes the directory preference. Governing instructions and host
    safeguards remain above all of these ordinary choices; this creates no
    directory, performs no review, and grants no execution or publication.
    """
    root, common = git_roots(repository)
    preferences = read_preferences(root)
    choices = invocation if invocation is not None else Preferences()
    result = dict(header)
    result["plain"] = _plain_choice(header, preferences, choices)
    result["tier"] = _tier_choice(header, preferences, choices)
    if "write_directory" not in result:
        try:
            destination = case_destination(preferences, case_root, root, common)
        except OSError as error:
            message = (
                f"The case destination could not be admitted (errno {error.errno}); "
                "check --case-root"
            )
            raise ValueError(message) from error
        if destination is not None:
            result["write_directory"] = str(destination)
    return result


def _plain_choice(
    header: dict[str, object], preferences: Preferences, invocation: Preferences
) -> bool:
    """Preserve explicit false and refuse an ill-typed header choice."""
    ordinary = preferences.plain if preferences.plain is not None else False
    value = header.get("plain", ordinary)
    if not isinstance(value, bool):
        message = "The header plain choice must be a Boolean"
        raise TypeError(message)
    return invocation.plain if invocation.plain is not None else value


def _tier_choice(
    header: dict[str, object], preferences: Preferences, invocation: Preferences
) -> str:
    """Admit only a named tier even when an invocation overrides the header."""
    value = header.get("tier", preferences.tier or "triage")
    if not isinstance(value, str) or value not in TIERS:
        message = "The header tier choice must be triage, focused or standard"
        raise ValueError(message)
    return invocation.tier if invocation.tier is not None else value
