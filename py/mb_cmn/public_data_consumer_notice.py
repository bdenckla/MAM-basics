"""Canonical warning labels embedded in public structured-data products."""

import json

MAM_PARSED_PLAIN_DOCUMENTATION = (
    "https://bdenckla.github.io/MAM-basics/MAM-parsed/plain/html/"
    "mpplain.html#consumer-notice"
)
MAM_PARSED_PLUS_DOCUMENTATION = (
    "https://bdenckla.github.io/MAM-basics/MAM-parsed/plus/html/"
    "mpplus.html#consumer-notice"
)
MAM_SIMPLE_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "MAM-simple/doc/reading-mam-simple.md#consumer-notice"
)
LENINGRAD_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "doc/scan-pages.md#codex-entry-indexes"
)
ALEPPO_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "aleppo/README.md#consumer-guide"
)
CAMBRIDGE_INDEX_DOCUMENTATION = (
    "https://github.com/bdenckla/MAM-basics/blob/main/"
    "cam1753/README.md#consumer-guide"
)


def mam_parsed_notice(variant: str) -> dict[str, object]:
    """Return the notice for a MAM-parsed plain or plus payload."""
    if variant == "plain":
        variant_rule = (
            "Plain retains the 0 and triple-tav pseudo-verses and other source "
            "structure; those records are not automatically Scripture."
        )
        documentation = MAM_PARSED_PLAIN_DOCUMENTATION
    elif variant == "plus":
        variant_rule = (
            "Plus omits plain's 0 and triple-tav pseudo-verses, but its remaining "
            "structures still require documented role and choice handling."
        )
        documentation = MAM_PARSED_PLUS_DOCUMENTATION
    else:
        raise ValueError(f"unknown MAM-parsed variant: {variant!r}")
    return {
        "summary": (
            "This is a structured dataset, not ready-to-display Scripture; interpret "
            "each structure by its documented role and choose a projection wherever "
            "the payload presents alternatives."
        ),
        "critical_rules": [
            (
                "Use a closed, role-aware template dispatch: recurse only through "
                "documented Scripture-bearing fields, and fail on an unknown template "
                "instead of guessing from its parameters or skipping it."
            ),
            (
                "Choose one documented branch of each choice-bearing structure, "
                "including ketiv/qere, dual cantillation, qamats, and stress-helper "
                "alternatives where present; do not concatenate the branches."
            ),
            (
                "A special-letter template's interrupted spelling and uninterrupted "
                "atom-form are two representations of one atom-form; select one text "
                "representation rather than collecting both."
            ),
            (
                "Reassemble text fragments before identifying atoms or chanted words; "
                "array, template, and element boundaries are not segmentation "
                "boundaries."
            ),
            variant_rule,
            (
                "For literal search, byte comparison, or MAM-compatible output, "
                "preserve MAM mark order or transform both sides deliberately; "
                "Unicode-normalized text can look identical while comparing "
                "differently."
            ),
        ],
        "documentation": documentation,
    }


def mam_simple_notice() -> dict[str, object]:
    """Return the notice shared by every MAM-simple JSON and XML file."""
    return {
        "summary": (
            "This is a projected extract of MAM, not a complete representation of the "
            "source; consume its documented roles and retained alternatives "
            "explicitly."
        ),
        "critical_rules": [
            (
                "If a requested BHS or Sefaria book-group file is absent, read the MAM "
                "file for that book group and confirm that its "
                "versification-tradition value names the requested tradition."
            ),
            (
                "Use a closed, role-aware element dispatch and fail on an unknown "
                "element; choose one branch where alternatives remain, including kq "
                "and cant-all-three, and do not concatenate note branches or repeated "
                "endings. MAM-simple has already resolved or removed some MAM-parsed "
                "choices, so absence here does not establish absence there."
            ),
            (
                "The children of slh-word spell one atom-form and slhw-desc-0 repeats "
                "that atom-form without letter formatting; do not collect both as "
                "running text."
            ),
            (
                "Reassemble fragments before identifying atoms or chanted words; a "
                "standalone paseq or legarmeh element belongs with the preceding atom, "
                "and structural boundaries do not define units of cantillation."
            ),
            (
                "The free parashah marker and the adjacent starts-with-sampe and "
                "ends-with-sampe attributes describe one break, not three."
            ),
            (
                "For literal search, byte comparison, or MAM-compatible output, "
                "preserve MAM mark order or transform both sides deliberately; "
                "Unicode-normalized text can look identical while comparing "
                "differently."
            ),
        ],
        "documentation": MAM_SIMPLE_DOCUMENTATION,
    }


def codex_index_notice(documentation: str) -> dict[str, object]:
    """Return the notice for one of the three public codex entry indexes."""
    if documentation not in {
        LENINGRAD_INDEX_DOCUMENTATION,
        ALEPPO_INDEX_DOCUMENTATION,
        CAMBRIDGE_INDEX_DOCUMENTATION,
    }:
        raise ValueError(f"unknown codex-index documentation URL: {documentation!r}")
    return {
        "summary": (
            "This file is a locator index, not a manuscript transcription or a Bible "
            "edition."
        ),
        "critical_rules": [
            (
                "Text ranges and text cues locate content on photographed pages; they "
                "must not be cited as a diplomatic transcription of the manuscript."
            ),
            (
                "Gaps and mid-verse boundaries are meaningful locator evidence; do not "
                "round them to whole verses or fill them from another edition."
            ),
            (
                "Line-break and page-geometry annotations are separate supporting data; "
                "do not infer either from this entry index."
            ),
        ],
        "documentation": documentation,
    }


def xml_comment(notice: dict[str, object]) -> str:
    """Serialize a notice as one parseable XML comment payload."""
    payload = json.dumps(notice, ensure_ascii=False, separators=(",", ":"))
    if "--" in payload:
        raise ValueError("XML comments cannot contain a double hyphen")
    return f"consumer_notice: {payload}"
