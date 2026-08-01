from __future__ import annotations

from pathlib import Path
from accgram import tm_changes
from accgram.prose_ob_notes import get_structured_text


def sanity_check_structured_text(
    refs: list[str],
    all_changes_path: Path,
) -> None:
    by_change_url = tm_changes.load_all_changes_by_url(all_changes_path)
    stext = get_structured_text()

    errors: list[str] = []
    for ref in refs:
        structured = stext.get(ref)
        if structured is None:
            continue

        uxlc_change = structured.get("uxlc_change")
        if not isinstance(uxlc_change, str) or not uxlc_change.strip():
            continue

        canonical_url = tm_changes.canonicalize_uxlc_change_url(uxlc_change)
        if canonical_url is None:
            errors.append(
                f"Malformed structured_text.uxlc_change URL for {ref}: {uxlc_change}"
            )
            continue

        change_row = by_change_url.get(canonical_url)
        if change_row is None:
            errors.append(
                "structured_text.uxlc_change not found in all_changes.json "
                f"for {ref}: {uxlc_change}"
            )
            continue

        citation = change_row.get("citation")
        if not isinstance(citation, str):
            errors.append(
                f"all_changes.json row is missing string citation for URL {canonical_url}"
            )
            continue

        if not tm_changes.citation_matches_ref(citation, ref):
            errors.append(
                "citation/ref mismatch for structured_text.uxlc_change "
                f"for {ref}: citation={citation} url={uxlc_change}"
            )

    if errors:
        first_errors = errors[:20]
        remainder_count = len(errors) - len(first_errors)
        details = "\n".join(f"- {error}" for error in first_errors)
        if remainder_count > 0:
            details = f"{details}\n- ... and {remainder_count} more"
        raise ValueError(
            "structured_text sanity checks failed against all_changes.json:\n"
            f"{details}"
        )
