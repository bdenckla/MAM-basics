r"""Test whether the suggested fixes in the goerwitz.html report actually work.

For every *annotated* prose ungrammatical (one carrying an ob_notes_* note), the
goerwitz.html report suggests a fix -- almost always "adopt the MAM-simple value
instead of the wlc_focus value".  This tool tests that suggestion mechanically:
it splices the MAM value into the verse's Michigan-Claremont body
(``fix_apply``), re-scans + re-parses it (the real ``prose_scanner`` /
``prose_ply_grammar``), and classifies the outcome:

  * CONFIRMED  -- the ungrammatical's ERROR cleared (the verse now parses clean);
  * DENIED     -- the same error remains;
  * CHANGED    -- a *different* error appears;
  * UNTESTABLE -- the fix could not be applied mechanically (vowel-/meteg-only,
                  non-adjacent multi-word, context-dependent accent, alignment
                  failure, ...).

For a multi-entry diff, the entry matching the note's ``wlc_focus`` is the one
tested (adjacent multi-word foci are spliced word by word).  When MAM equals WLC
the fix is not a word splice: if the note carries a hand-authored ``synth_fix``
value, that speculated reading is tested instead (flagged ``synthesized``); if it
carries a ``merge_next`` ref (the lone versification ungrammatical nu 25:19, where BHS
maroons a verse number mid-chanted-verse), the named next verse's M-C body is
*appended* and the joined verse re-parsed (``_test_merge_next``).

It then cross-checks the verdict against the note's claim, flagging speculative
claims ("I think the checker wants...") whose mechanical result disagrees, and
writes a standalone text + JSON report under ``out/accgram/fix-tester/``.  It
never edits goerwitz.html or the ob_notes_* prose; a human applies prose edits
from the report.

Depends on ``out/accgram/prose/`` -- run ``run-prose`` first.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from pathlib import Path

from accgram import fix_apply
from accgram import fix_claim
from accgram import classify
from accgram import research_tao
from accgram import rtms_data
from accgram import rtms_focus_diff_expand
from accgram import rtms_rows
from accgram import uni_to_marks
from accgram import lexical_validation
from accgram.prose_ply_grammar import LOCATION_ONLY, build_parser, parse_tokens
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from accgram.tree import TN
from accgram.prose_ob_notes import get_structured_text
from mb_cmn import file_io
from mb_cmn import provenance

import wlc_paths


@dataclass(frozen=True)
class FixTestResult:
    ref: str
    bcv: str
    wlc_focus: str | None
    fix_description: str
    classification: str  # CONFIRMED | DENIED | CHANGED | UNTESTABLE
    untestable_reason: str | None
    transformation: str | None
    before_status: str
    before_labels: tuple[str, ...]
    after_status: str | None
    after_labels: tuple[str, ...]
    before_tokens: tuple[str, ...]
    after_tokens: tuple[str, ...] | None
    speculative: bool
    synthesized: bool  # fix tested came from the note's hand-authored synth_fix
    claimed_outcome: str
    agreement: str  # agree | disagree | n/a
    st_summary: str


@dataclass
class _Eval:
    status: str  # CLEAN | ERROR | NO_PARSE | LOCATION_ONLY
    labels: frozenset[str]
    token_types: tuple[str, ...]


# --- per-verse evaluation (mirrors prose_run.render_book) -----------------------


# THE PARSE HERE IS PLAIN, AND THE WATCHDOG THAT USED TO WRAP IT IS RETIRED (#221).
# ``_ParseGuard`` ran every parse on a daemon thread with an 8-second wall clock and a
# PARSE_TIMEOUT status (wlc-utils 2fae1be, 2026-06-16), because a synthetic stream --
# which is all this tool feeds the grammar -- could drive PLY's error recovery into a
# loop that reads no further input.  #221 found that loop and removed its cause, the bare
# ``pasuq : error`` production; a sweep of 79,798 token streams then found no stream that
# fails to terminate.  The guard is not kept as insurance because it costs more than it
# insures: an 8-second wall clock is a nondeterministic verdict, so a loaded machine could
# turn a real result into an UNTESTABLE row, and each timeout abandoned a live thread
# holding a parser.  A future non-termination would hang this run outright, which is a
# louder signal than a plausible-looking report with a row silently reclassified.
def _evaluate(body: str, bb: str, chnu: int, vrnu: int, parser) -> _Eval:
    tokens = [Token("TILDE", "")] + scan_accents(body, bb, chnu, vrnu, HasLegarmeh())
    token_types = tuple(tok.type for tok in tokens if tok.type != "TILDE")

    # Prose lexical layer fires first and skips the grammar (the same single entry point
    # prose_run uses, so an annotated lexical ungrammatical -- e.g. je 44:17's misplaced telisha
    # qetanna or lv25:20's same-letter pair -- is classified here, not via the grammar).
    ungrammatical = lexical_validation.lexical_ungrammatical(body)
    if ungrammatical:
        labels = frozenset(f"illegal_mark:{mark.code}" for mark in ungrammatical)
        return _Eval("ERROR", labels, token_types)

    tree = parse_tokens(parser, tokens)
    if tree is None:
        return _Eval("NO_PARSE", frozenset({"NO_PARSE"}), token_types)
    if tree is LOCATION_ONLY:
        return _Eval("LOCATION_ONLY", frozenset({"LOCATION_ONLY"}), token_types)
    labels = _error_labels(tree)
    if labels:
        return _Eval("ERROR", frozenset(labels), token_types)
    return _Eval("CLEAN", frozenset(), token_types)


def _error_labels(tree: TN, out: set[str] | None = None) -> set[str]:
    """Labels of leaf nodes whose leaves contain the ERROR token."""
    out = set() if out is None else out
    if tree.left is None:
        if "ERROR" in tree.leaves:
            out.add(tree.label)
    else:
        _error_labels(tree.left, out)
        if tree.right is not None:
            _error_labels(tree.right, out)
    return out


# --- diff -> single testable change ------------------------------------------


def _select_diff_entry(diff: object, wlc_focus: str | None) -> object:
    """Return the single testable diff dict, or a sentinel: _NO_DIFF / _MULTI_DIFF.

    For a multi-entry diff, the entry whose wlc422 side equals the note's wlc_focus
    is the one the annotation is about (mirrors the SAT display selection in
    rtms_sat_source_rows); the other entries are incidental and dropped.  Adjacent
    multi-word foci arrive pre-collapsed into one entry by the wlc_focus expansion.
    """
    if isinstance(diff, dict):
        return diff
    if diff is None:
        return _NO_DIFF
    if isinstance(diff, list):
        entries = [e for e in diff if isinstance(e, dict)]
        if not entries:
            return _NO_DIFF
        if len(entries) == 1:
            return entries[0]
        if wlc_focus:
            focus = " ".join(wlc_focus.split())
            matches = [e for e in entries if _entry_wlc_matches_focus(e, focus)]
            if len(matches) == 1:
                return matches[0]
        return _MULTI_DIFF
    return _NO_DIFF


def _entry_wlc_matches_focus(entry: dict, focus: str) -> bool:
    return " ".join(_side_repr(entry.get("wlc422")).split()) == focus


def _synth_fix(structured_text: object) -> str | None:
    """The note's hand-authored speculated fix value (``synth_fix``), if present."""
    if not isinstance(structured_text, dict):
        return None
    value = structured_text.get("synth_fix")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _merge_next(structured_text: object) -> str | None:
    """The note's adjacent-verse merge target (``merge_next``), if present.

    For the lone versification ungrammatical (nu 25:19) MAM equals WLC word-for-word --
    BHS merely puts a verse number mid-chanted-verse.  The fix is not a word splice
    but a *verse* splice: append the named next verse's M-C body and re-parse.  See
    ``doc/fix-tester-remaining-untestables.md``.
    """
    if not isinstance(structured_text, dict):
        return None
    value = structured_text.get("merge_next")
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


_NO_DIFF = object()
_MULTI_DIFF = object()


def _describe_diff(diff_entry: object) -> str:
    if not isinstance(diff_entry, dict):
        return "(no MAM diff)"
    return f"{_side_repr(diff_entry.get('wlc422'))} -> {_side_repr(diff_entry.get('mam_simple'))}"


def _side_repr(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(_side_repr(v) for v in value)
    if isinstance(value, dict):
        for key in ("word", "text"):
            inner = value.get(key)
            if isinstance(inner, str):
                return inner
    return repr(value)


# --- one ungrammatical verse -------------------------------------------------------------


def _test_one(
    *,
    row: dict[str, object],
    bcv: str,
    ref: str,
    structured_text: dict[str, object],
    wlc_focus: str | None,
    source_indexes: tuple[dict, dict, dict],
    args: argparse.Namespace,
    parser,
) -> FixTestResult:
    speculative = fix_claim.is_speculative(structured_text)
    claimed = fix_claim.claimed_outcome(structured_text)
    st_summary = _summary_text(structured_text)
    bb, chnu, vrnu = rtms_rows.parse_ref(ref, row_kind="ungrammatical")

    def result(
        classification: str,
        *,
        reason: str | None = None,
        transformation: str | None = None,
        before: _Eval | None = None,
        after: _Eval | None = None,
        fix_description: str = "",
        synthesized: bool = False,
    ) -> FixTestResult:
        agreement = _agreement(claimed, classification)
        return FixTestResult(
            ref=ref,
            bcv=bcv,
            wlc_focus=wlc_focus,
            fix_description=fix_description,
            classification=classification,
            untestable_reason=reason,
            transformation=transformation,
            before_status=before.status if before else "n/a",
            before_labels=tuple(sorted(before.labels)) if before else (),
            after_status=after.status if after else None,
            after_labels=tuple(sorted(after.labels)) if after else (),
            before_tokens=before.token_types if before else (),
            after_tokens=after.token_types if after else None,
            speculative=speculative,
            synthesized=synthesized,
            claimed_outcome=claimed,
            agreement=agreement,
            st_summary=st_summary,
        )

    wlc422_by_bcv, uxlc_by_bcv, mam_simple_by_bcv = source_indexes
    # The scanned body is transcoded from the canonical -kq-u verse (issue wlc-utils#9: M-C
    # dropped as an input), not read from the ungrammatical row's stored content.
    raw_verse = wlc422_by_bcv.get(bcv)
    body = uni_to_marks.verse_to_marks(raw_verse) if isinstance(raw_verse, dict) else ""
    if not body:
        return result("UNTESTABLE", reason="no_body")

    try:
        enriched_row, _ = rtms_data.build_enriched_row(
            row=row,
            bcv=bcv,
            ref=ref,
            wlc422_by_bcv=wlc422_by_bcv,
            uxlc_by_bcv=uxlc_by_bcv,
            mam_simple_by_bcv=mam_simple_by_bcv,
            wlc422_kq_u_dir=args.wlc422_kq_u_dir,
            uxlc_dir=args.uxlc_dir,
            mam_simple_dir=args.mam_simple_dir,
            wlc_focus=wlc_focus,
        )
    except (ValueError, KeyError) as exc:
        return result("UNTESTABLE", reason="enrich_error", fix_description=str(exc))

    diff = enriched_row.get("diff_wlc_mam")
    wlc_words = fix_apply.verse_words(enriched_row.get("wlc422_kq_u_verse"))
    before = _evaluate(body, bb, chnu, vrnu, parser)

    synth_fix = _synth_fix(structured_text)
    diff_entry = _select_diff_entry(diff, wlc_focus)
    synthesized = False
    if diff_entry is _NO_DIFF:
        merge_ref = _merge_next(structured_text)
        if merge_ref is not None:
            return _test_merge_next(
                merge_ref=merge_ref,
                body=body,
                bb=bb,
                chnu=chnu,
                vrnu=vrnu,
                before=before,
                wlc422_by_bcv=wlc422_by_bcv,
                parser=parser,
                result=result,
            )
        if synth_fix is None or not wlc_focus:
            return result(
                "UNTESTABLE",
                reason="no_mam_diff",
                before=before,
                fix_description="(MAM equals WLC; nothing to adopt)",
            )
        # MAM offers nothing to adopt; test the note's hand-authored speculation.
        diff_entry = {"wlc422": wlc_focus, "mam_simple": synth_fix}
        synthesized = True
    elif diff_entry is _MULTI_DIFF:
        return result(
            "UNTESTABLE",
            reason="multi_diff",
            before=before,
            fix_description=_describe_diff_list(diff),
        )

    fix_description = _describe_diff(diff_entry)
    if synthesized:
        fix_description = f"{fix_description}  (synthesized)"
    applied = fix_apply.apply_mam_fix(raw_verse, wlc_words, diff_entry)
    if isinstance(applied, fix_apply.UntestableFix):
        return result(
            "UNTESTABLE",
            reason=applied.reason,
            before=before,
            fix_description=fix_description,
            transformation=applied.detail or None,
            synthesized=synthesized,
        )

    after = _evaluate(applied.new_body, bb, chnu, vrnu, parser)
    if after.status == "CLEAN":
        classification = "CONFIRMED"
    elif (after.status, after.labels) == (before.status, before.labels):
        classification = "DENIED"
    else:
        classification = "CHANGED"
    return result(
        classification,
        before=before,
        after=after,
        transformation=applied.transformation(),
        fix_description=fix_description,
        synthesized=synthesized,
    )


def _test_merge_next(
    *,
    merge_ref: str,
    body: str,
    bb: str,
    chnu: int,
    vrnu: int,
    before: _Eval,
    wlc422_by_bcv: dict[str, dict[str, object]],
    parser,
    result,
) -> FixTestResult:
    """The lone *verse*-level splice: append the named next verse's M-C body.

    Unlike every other fix (a single-word accent edit inside one verse via
    ``fix_apply``), nu 25:19's fix is versification: BHS maroons a verse number
    mid-chanted-verse, so the "verse" ends on an atnax with no silluq/sof-pasuq.
    Appending the body BHS labels as the next verse supplies the second half, the
    atnax bisects a complete verse, and the parse comes out CLEAN.
    """
    nbb, nchnu, nvrnu = rtms_rows.parse_ref(merge_ref, row_kind="ungrammatical")
    next_bcv = rtms_rows.to_compact_bcv(nbb, nchnu, nvrnu)
    next_verse = wlc422_by_bcv.get(next_bcv)
    next_body = (
        uni_to_marks.verse_to_marks(next_verse)
        if isinstance(next_verse, dict)
        else None
    )
    fix_description = (
        f"merge next verse {merge_ref} "
        f"(MAM versification: BHS splits one chanted verse in two)"
    )
    if not next_body:
        return result(
            "UNTESTABLE",
            reason="merge_target_missing",
            before=before,
            fix_description=fix_description,
        )

    combined = f"{body} {next_body}"
    after = _evaluate(combined, bb, chnu, vrnu, parser)
    transformation = f"appended {merge_ref} M-C body"
    if after.status == "CLEAN":
        classification = "CONFIRMED"
    elif (after.status, after.labels) == (before.status, before.labels):
        classification = "DENIED"
    else:
        classification = "CHANGED"
    return result(
        classification,
        before=before,
        after=after,
        transformation=transformation,
        fix_description=fix_description,
    )


def _describe_diff_list(diff: object) -> str:
    if isinstance(diff, list):
        return "; ".join(_describe_diff(e) for e in diff if isinstance(e, dict))
    return _describe_diff(diff)


def _summary_text(structured_text: object) -> str:
    if isinstance(structured_text, dict):
        summary = structured_text.get("st-summary")
        if isinstance(summary, str):
            return summary
    return ""


def _agreement(claimed: str, classification: str) -> str:
    if classification == "UNTESTABLE" or claimed == "unclear":
        return "n/a"
    result_fixed = classification == "CONFIRMED"
    if claimed == "expects_fix":
        return "agree" if result_fixed else "disagree"
    if claimed == "rejects_fix":
        return "agree" if not result_fixed else "disagree"
    return "n/a"


# --- run ---------------------------------------------------------------------


def run_tests(args: argparse.Namespace) -> list[FixTestResult]:
    repo_root = _repo_root()

    classify.write_ungrammatical(
        prose_dir=getattr(args, "prose_dir", None)
        or research_tao.default_prose_dir(repo_root),
        wlc422_kq_u_dir=args.wlc422_kq_u_dir,
        ungrammatical_out=args.ungrammatical_in,
    )

    refs_by_book: dict[str, set[tuple[int, int]]] = {}
    parsed_rows = rtms_rows.parse_ungrammatical_rows(
        args.ungrammatical_in, refs_by_book
    )
    structured_text_by_ref = get_structured_text()

    source_indexes = rtms_data.load_source_indexes(
        wlc422_kq_u_dir=args.wlc422_kq_u_dir,
        uxlc_dir=args.uxlc_dir,
        mam_simple_dir=args.mam_simple_dir,
        refs_by_book=refs_by_book,
    )

    parser = build_parser()
    results: list[FixTestResult] = []
    for row, bcv, ref in parsed_rows:
        structured_text = structured_text_by_ref.get(ref)
        if structured_text is None:
            continue
        wlc_focus = rtms_focus_diff_expand.structured_wlc_focus(structured_text)
        results.append(
            _test_one(
                row=row,
                bcv=bcv,
                ref=ref,
                structured_text=structured_text,
                wlc_focus=wlc_focus,
                source_indexes=source_indexes,
                args=args,
                parser=parser,
            )
        )
    results.sort(key=lambda r: _ref_sort_key(r.ref))
    return results


def _ref_sort_key(ref: str) -> tuple[str, int, int]:
    bb, chnu, vrnu = rtms_rows.parse_ref(ref, row_kind="ungrammatical")
    return (bb, chnu, vrnu)


# --- reports -----------------------------------------------------------------

_SECTIONS = (
    ("CONFIRMED", "MAM fix clears the error"),
    ("DENIED", "same error remains after the fix"),
    ("CHANGED", "a different error appears after the fix"),
    ("UNTESTABLE", "fix could not be applied mechanically"),
)


def _summary_counts(results: list[FixTestResult]) -> dict[str, int]:
    counts = {name: 0 for name, _ in _SECTIONS}
    for r in results:
        counts[r.classification] = counts.get(r.classification, 0) + 1
    return counts


def render_text_report(results: list[FixTestResult]) -> str:
    counts = _summary_counts(results)
    specs = [r for r in results if r.speculative]
    spec_conf = sum(1 for r in specs if r.classification == "CONFIRMED")
    spec_denied = sum(1 for r in specs if r.classification in ("DENIED", "CHANGED"))
    spec_untest = sum(1 for r in specs if r.classification == "UNTESTABLE")
    agree = sum(1 for r in results if r.agreement == "agree")
    disagree = sum(1 for r in results if r.agreement == "disagree")
    synth = sum(1 for r in results if r.synthesized)

    lines: list[str] = []
    lines.append(
        "# Fix-tester: do MAM-simple values resolve annotated prose ungrammatical?"
    )
    lines.append("")
    lines.append(
        f"confirmed: {counts['CONFIRMED']}  denied: {counts['DENIED']}  "
        f"changed: {counts['CHANGED']}  untestable: {counts['UNTESTABLE']}  "
        f"({len(results)} annotated ungrammatical tested)"
    )
    lines.append(
        f"speculations: {len(specs)} total; {spec_conf} confirmed, "
        f"{spec_denied} denied/changed, {spec_untest} untestable"
    )
    lines.append(
        f"synthesized fixes (no MAM diff; tested the note's synth_fix): {synth}"
    )
    lines.append(f"claim-vs-result: {agree} agree, {disagree} disagree")
    lines.append("")

    by_class: dict[str, list[FixTestResult]] = {name: [] for name, _ in _SECTIONS}
    for r in results:
        by_class.setdefault(r.classification, []).append(r)

    for name, blurb in _SECTIONS:
        group = by_class.get(name, [])
        lines.append(f"## {name} -- {blurb}  ({len(group)})")
        if name == "UNTESTABLE" and group:
            lines.append(
                "  (note: a *medial* 'vowel_only'/'meteg_only' mark is grammar-inert, "
                "the scanner swallowing it; 'merge_target_missing' means the named "
                "merge_next verse was not found in the source.  None is a verdict on the "
                "ungrammatical verse.)"
            )
        for r in group:
            lines.extend(_render_entry(r))
        lines.append("")

    review = [r for r in results if r.speculative and r.agreement == "disagree"]
    lines.append(
        f"## Review queue: speculative claims whose result disagrees  ({len(review)})"
    )
    for r in review:
        lines.append(f"  {r.ref}  [{r.classification}] claim: {r.st_summary!r}")
    lines.append("")

    return "\n".join(lines) + "\n"


def _render_entry(r: FixTestResult) -> list[str]:
    tags = []
    if r.synthesized:
        tags.append("synthesized")
    if r.speculative:
        tags.append("speculative")
    if r.claimed_outcome != "unclear":
        tags.append(f"claim: {r.claimed_outcome}")
    if r.agreement != "n/a":
        tags.append(r.agreement.upper())
    tag_str = (" [" + "] [".join(tags) + "]") if tags else ""
    out = [f"  {r.ref}{tag_str}"]
    out.append(f"    fix: {r.fix_description}")
    if r.classification == "UNTESTABLE":
        detail = f" ({r.transformation})" if r.transformation else ""
        out.append(f"    reason: {r.untestable_reason}{detail}")
        return out
    if r.transformation:
        out.append(f"    transform: {r.transformation}")
    out.append(
        f"    before: {' '.join(r.before_tokens)}  [{_status_label(r.before_status, r.before_labels)}]"
    )
    after_tokens = " ".join(r.after_tokens) if r.after_tokens else ""
    out.append(
        f"    after:  {after_tokens}  [{_status_label(r.after_status, r.after_labels)}]"
    )
    return out


def _status_label(status: str | None, labels: tuple[str, ...]) -> str:
    if status == "CLEAN":
        return "CLEAN"
    if labels:
        return f"{status}: {', '.join(labels)}"
    return status or "n/a"


def build_json_report(results: list[FixTestResult]) -> dict:
    counts = _summary_counts(results)
    specs = [r for r in results if r.speculative]
    payload = {
        "artifacts_description": (
            "fix-tester verdicts: whether adopting each annotated prose ungrammatical's "
            "MAM-simple value clears its grammar/lexical error"
        ),
        "summary": {
            "tested": len(results),
            **{name.lower(): counts.get(name, 0) for name, _ in _SECTIONS},
            "speculative_total": len(specs),
            "speculative_confirmed": sum(
                1 for r in specs if r.classification == "CONFIRMED"
            ),
            "synthesized": sum(1 for r in results if r.synthesized),
            "agree": sum(1 for r in results if r.agreement == "agree"),
            "disagree": sum(1 for r in results if r.agreement == "disagree"),
        },
        "results": [asdict(r) for r in results],
    }
    return provenance.with_json_provenance(payload, __file__)


# --- CLI ---------------------------------------------------------------------


def _repo_root() -> Path:
    return wlc_paths.wlc_data_root()


def default_report_txt_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "fix-tester" / "_fix_tester.txt"


def default_report_json_path(repo_root: Path) -> Path:
    return wlc_paths.out_dir() / "accgram" / "fix-tester" / "_fix_tester.json"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--wlc422-kq-u-dir",
        type=Path,
        default=research_tao.default_wlc422_kq_u_dir(repo_root),
        help="Directory containing 1verses_*.json files.",
    )
    parser.add_argument(
        "--uxlc-dir",
        type=Path,
        default=research_tao.default_uxlc_dir(repo_root),
        help="Directory containing UXLC XML book files.",
    )
    parser.add_argument(
        "--mam-simple-dir",
        type=Path,
        default=research_tao.default_mam_simple_dir(repo_root),
        help="Directory containing MAM-simple json-vtrad-bhs book files.",
    )
    parser.add_argument(
        "--ungrammatical-in",
        type=Path,
        default=research_tao.default_ungrammatical_in(repo_root),
        help="Path to _oddballs.json (regenerated each run).",
    )
    parser.add_argument(
        "--prose-dir",
        type=Path,
        default=research_tao.default_prose_dir(repo_root),
        help="Directory of *_ag.json outputs for the ungrammatical corpus.",
    )
    parser.add_argument(
        "--report-txt",
        type=Path,
        default=default_report_txt_path(repo_root),
        help="Output path for the text fix-tester report.",
    )
    parser.add_argument(
        "--report-json",
        type=Path,
        default=default_report_json_path(repo_root),
        help="Output path for the JSON fix-tester report.",
    )


def run(args: argparse.Namespace) -> None:
    results = run_tests(args)

    text_path: Path = args.report_txt
    json_path: Path = args.report_json
    # The mkdir still serves the text report, which stays a plain write_text.
    text_path.parent.mkdir(parents=True, exist_ok=True)
    text_path.write_text(render_text_report(results), encoding="utf-8", newline="\n")
    # file_io: temp-file write, PermissionError retry, and it makes the directory.
    # build_json_report stamps provenance itself, so no generator_file= here.
    file_io.json_dump_to_file_path(build_json_report(results), str(json_path))

    counts = _summary_counts(results)
    print(
        f"Fix-tester: {len(results)} tested; {counts['CONFIRMED']} confirmed, "
        f"{counts['DENIED']} denied, {counts['CHANGED']} changed, "
        f"{counts['UNTESTABLE']} untestable -> {text_path}"
    )
