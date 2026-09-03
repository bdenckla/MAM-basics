"""Build and re-check the Holman meteg rollout's two Wikisource bot edit specs.

Item 2 of ``doc/PLAN-holman-meteg-rollout-programme.md``.  Thirty of Daniel
Holman's MAM suggestions differ from their Aleppo Codex comparison form in
metegs alone; Ben accepted all thirty on 2026-09-03.  This module turns those
records into the two files ``py/main_ws_bot.py`` consumes, and re-runs the
checks that say the files still describe the corpus.

    .venv/Scripts/python.exe py/main_ws_bot.py holman-meteg-spec
    .venv/Scripts/python.exe py/main_ws_bot.py holman-meteg-spec --write

The default is check-only, because the programme requires the check be
re-runnable immediately before item 3's live save, and a check that silently
rewrote its own subject would prove nothing.

WHY ``old`` IS LIFTED FROM THE WIKITEXT RATHER THAN COPIED FROM ``mam_form``

``mam_form`` in ``holman/docs-not-served/mam_suggestions.json`` is in
MAM-normal mark order, this repository's order: shin dot, sin dot, dagesh,
rafe, then every other mark.  Hebrew Wikisource's wikitext is not: measured
2026-09-03 over the 30 records' chapters, seventeen of the thirty forms fail a
verbatim search of their own chapter, and eleven of those seventeen fail for
mark order alone -- the wikitext writes the dagesh, shin dot or sin dot after
the vowel rather than before it.  Both orders render identically, which is why
the difference is invisible on the page and fatal to a byte comparison.  See
``CLAUDE.md``'s opening section.

``give_std_mark_order`` reorders marks only within one letter's cluster, so it
neither changes a string's length nor moves any index.  That is what lets this
module search the chapter in std-order space and then slice the ORIGINAL text
at the index it found, which is how every ``old`` string here is obtained: the
wikitext's own bytes, located by the record rather than retyped from it.

THE TWO CLASSES OF RECORD THAT NEED MORE THAN A SLICE

1. ``{{מ:ירושלם}}``.  Four records -- M3, M20, M21 and M25 -- name an atom the
   wikitext writes across a template call, the meteg sitting in the plain-text
   part before it.  The whole call is inside the span, because the span runs to
   the next space, so ``old`` covers the word as written.
2. ``{{מ:קמץ}}``.  One record, M13, names an atom the wikitext writes as both
   parameters of a qamats-variant call, and the meteg is in each.  Removing it
   from ``ד`` alone would leave the two forms differing in something other than
   the qamats, which is the only thing that template exists to vary, so M13
   becomes two entries.  ``doc/holman-meteg-m13-qamats-template.md`` is the
   finding.

AND ONE RECORD THAT IS ALREADY DONE

M18, 2 Kings 21:12, was applied on Hebrew Wikisource before this file was
built: the meteg is gone from the resh of ירושלם in the live text, along with
one on the vav of ויהודה that no Holman record covers.  A ``meteg-removal``
entry for it would abort the whole bot run, since ``ws_bot_edit.edit_page_text``
asserts its ``old`` occurs exactly once.  So M18 is excluded by name, loudly:
``_ALREADY_APPLIED`` records it, and the check fails if the meteg comes back.

THIS CHECK IS ONE-SHOT, AND IS MEANT TO STOP PASSING

Every ``old`` describes the corpus BEFORE the edit, so once item 3 has saved to
Wikisource and item 4 has downloaded the result, ``_locate_target_meteg`` finds
nothing and the check raises.  That is the designed end state and not a defect
to repair: the twenty-nine metegs are the point, and a spec that still applied
afterwards would mean they were still there.  ``ws_bot_edit_history.md`` says
the same of the sigil ב2 bot.  Archive the two specs with item 6 rather than
keeping the check green.
"""

import json
import os
import re

import hkq_paths
from mb_cmn import bib_locales as tbn
from mb_cmn import file_io
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import uni_denorm
from ws import ws_fmt_2_back_to_wikitext as btw
from ws import ws_get_bk_in_both_fmts as wsin

METEG = hpo.MTGOSLQ

_WS_IN_PATH = "in/mam-ws"
_SPEC_DIR = "in/mam-ws-bot-edits"
_REMOVAL_SPEC = f"{_SPEC_DIR}/holman-meteg-removal.json"
_ADDITION_SPEC = f"{_SPEC_DIR}/holman-meteg-add-isaiah-23-12.json"

# Case numbers whose suggestion the live wiki already satisfies, so no entry is
# written for them.  The value is why, for the report.
_ALREADY_APPLIED = {
    18: (
        "the resh meteg of ירושלם is already gone from 2 Kings 21:12 on Hebrew"
        " Wikisource, together with a vav meteg on ויהודה that no Holman record"
        " covers; observed 2026-09-03 in a fresh fr-wikisource download"
    ),
}

# A span ends at a space, a newline, or a wiki tag's angle bracket.  Everything
# else -- letters, marks, maqaf, sof pasuq, and a whole {{...}} call -- is part
# of the word as the wikitext writes it.
_SPAN_STOP = set(" \t\n<>")

# Every comment opens with the case number, which is how an entry is traced back
# to the record it came from; ``_entry`` is the one place that writes it.
_COMMENT_CASE = re.compile(r"M(?P<number>\d+)\b")

# The qamats-variant template, whose two parameters carry the same word.
_QAMATS_CALL = re.compile(r"\{\{מ:קמץ\|ד=(?P<dalet>[^|}]*)\|ס=(?P<samekh>[^|}]*)\}\}")

# {{מ:פסוק|<book>|<chapter>|<verse>}} opens each verse of a chapter.  A fourth
# parameter is optional and has to be allowed for: 2 Samuel 15:37's anchor reads
# {{מ:פסוק|שמואל ב|טו|לז|סדר=כט}}, carrying its seder number, and a pattern
# demanding }} right after the verse silently attributes that verse's words to
# verse 36.
_VERSE_ANCHOR = re.compile(
    r"\{\{מ:פסוק\|[^|}]*\|[^|}]*\|(?P<verse>[^|}]*)(?:\|[^}]*)?\}\}"
)


class SpecProblem(Exception):
    """A record the corpus no longer supports; never worked around, always raised."""


def add_args(parser) -> None:
    """Register this subcommand's own options."""
    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            f"Rebuild {_REMOVAL_SPEC} and {_ADDITION_SPEC} from the suggestions"
            " JSON and the current in/mam-ws text (default: check only)"
        ),
    )
    parser.add_argument(
        "--selector-dir",
        help=(
            "Write into this directory, one file per spec, the"
            " --book-chapters-json selector naming exactly that spec's chapters."
            " A proto or real run needs one: a bare --book39 selects the whole"
            " book, and assert_book_plans_within_target_set then refuses every"
            " chapter the spec does not name.  Use a gitignored directory such"
            " as .novc"
        ),
    )


def run(args, _extra_args=None) -> None:
    """Check the two specs, and rebuild them first when asked."""
    cases = _load_meteg_cases()
    chapters = _load_chapters(cases)
    removals, additions = _partition(cases)
    print(
        f"Holman meteg records: {len(cases)}"
        f" ({len(removals)} removal, {len(additions)} addition)"
    )
    _check_arithmetic(cases)
    built = _build_specs(removals, additions, chapters)
    if args.write:
        for path, spec in built.items():
            file_io.json_dump_to_file_path(spec, path)
            print(f"wrote {path}")
    _check_specs_on_disk(built, cases, chapters)
    if args.selector_dir:
        _write_selectors(built, args.selector_dir)
    print("Holman meteg pre-flight: all checks passed.")


def _write_selectors(built, selector_dir):
    """Per spec, the book/chapter list that scopes a run to exactly its chapters."""
    for path, spec in built.items():
        pairs = sorted(
            (bk39id, hvn.STR_TO_INT_DIC[entry["ch"]])
            for bk39id, entries in spec["edits"].items()
            for entry in entries
        )
        entries = [
            {"book39": bk39id, "chapter": chapter}
            for bk39id, chapter in dict.fromkeys(pairs)
        ]
        stem = os.path.splitext(os.path.basename(path))[0]
        out_path = f"{selector_dir}/{stem}-chapters.json"
        file_io.json_dump_to_file_path(entries, out_path)
        print(f"  wrote {out_path}: {len(entries)} book/chapter pairs")


# ---------------------------------------------------------------- loading


def _read_json(path):
    with open(path, "r", encoding="utf-8") as json_in_fp:
        return json.load(json_in_fp)


def _load_meteg_cases():
    """The 30 cases whose MAM and comparison forms differ by one meteg."""
    all_cases = _read_json(hkq_paths.mam_suggestions_json_path())["cases"]
    cases = [case for case in all_cases if _direction(case) is not None]
    cases.sort(key=lambda case: case["case_number"])
    return cases


def _direction(case):
    """Say "removal" or "addition", or None for a record that is not about a meteg."""
    mam, comparison = case["mam_form"], case["comparison_form"]
    if METEG in mam and mam.replace(METEG, "", 1) == comparison:
        return "removal"
    if METEG in comparison and comparison.replace(METEG, "", 1) == mam:
        return "addition"
    return None


def _partition(cases):
    removals = [case for case in cases if _direction(case) == "removal"]
    additions = [case for case in cases if _direction(case) == "addition"]
    return removals, additions


def _load_chapters(cases):
    """Per book, per Hebrew chapter key, the raw text and the format-2 round trip.

    The raw text is what ``main_ws_bot.py real`` edits, fetched live; the round
    trip is what ``proto`` edits, rebuilt from the local mirror.  An ``old``
    string has to occur exactly once in each, so both are carried.
    """
    chapters = {}
    for bk39id in sorted({case["std_book_name"] for case in cases}):
        osdf = tbn.ordered_short_dash_full_39(bk39id)
        raw_book = _read_json(f"{_WS_IN_PATH}/{osdf}.json")
        cif2_book = wsin.get_bk_in_fmt_2(_WS_IN_PATH, bk39id)
        chapters[bk39id] = {
            he_chnu: {
                "raw": "\n".join(lines),
                "big": btw.big_str(he_chnu, cif2_book[he_chnu]),
            }
            for he_chnu, lines in raw_book.items()
        }
    return chapters


def _chapter_of(chapters, case):
    return chapters[case["std_book_name"]][hvn.INT_TO_STR_DIC[case["chapter"]]]


# ------------------------------------------------------- the arithmetic gate


def _check_arithmetic(cases):
    """The programme's pre-flight: one meteg is the whole of every difference."""
    problems = []
    for case in cases:
        mam, comparison = case["mam_form"], case["comparison_form"]
        if _direction(case) == "removal":
            got, want = mam.replace(METEG, "", 1), comparison
        else:
            got, want = comparison.replace(METEG, "", 1), mam
        if got != want:
            problems.append(f"M{case['case_number']} {case['ref']}")
        if not uni_denorm.has_std_mark_order(mam):
            problems.append(f"M{case['case_number']} {case['ref']}: mam_form is not")
    if problems:
        raise SpecProblem(
            "stripping one meteg does not reproduce the comparison form for: "
            + ", ".join(problems)
        )
    print(f"  arithmetic gate: {len(cases)}/{len(cases)} records reproduce exactly")


# ---------------------------------------------------------------- locating


def _locate_target_meteg(case, text):
    """Index in ``text`` of the meteg this record is about.

    ``give_std_mark_order`` moves marks only inside one letter's cluster, so it
    preserves every index: a match found in std-order space slices the original.
    A record whose atom the wikitext splits across a template call -- the four
    ``{{מ:ירושלם}}`` records -- matches on the longest prefix of its form that
    still reaches past the meteg.
    """
    form = case["mam_form"]
    std_text = uni_denorm.give_std_mark_order(text)
    meteg_at = form.index(METEG)
    for length in range(len(form), meteg_at, -1):
        prefix = form[:length]
        count = std_text.count(prefix)
        if count == 1:
            return std_text.index(prefix) + meteg_at, prefix
        if count > 1:
            raise SpecProblem(
                f"M{case['case_number']} {case['ref']}: the longest prefix of its"
                f" MAM form that the chapter holds occurs {count} times, so no"
                " unique target can be named"
            )
    raise SpecProblem(
        f"M{case['case_number']} {case['ref']}: no prefix of its MAM form reaching"
        " past the meteg occurs in the chapter at all -- either the wiki has moved"
        " on, or the suggestion is already applied"
    )


def _span_around(text, index):
    """The wikitext word containing ``index``: bounded by space and by wiki tags."""
    start = index
    while start > 0 and text[start - 1] not in _SPAN_STOP:
        start -= 1
    end = index
    while end < len(text) and text[end] not in _SPAN_STOP:
        end += 1
    return start, end


def _verse_of(text, index):
    """The Hebrew verse numeral of the verse ``index`` falls in, or None."""
    found = None
    for match in _VERSE_ANCHOR.finditer(text):
        if match.start() > index:
            break
        found = match.group("verse")
    return found


# ---------------------------------------------------------------- building


def _removal_entries(case, chapter):
    """The one or two ``meteg-removal`` entries this record needs."""
    text = chapter["raw"]
    meteg_at, matched = _locate_target_meteg(case, text)
    _assert_in_its_own_verse(case, text, meteg_at)
    start, end = _span_around(text, meteg_at)
    span = text[start:end]
    qamats_call = _QAMATS_CALL.fullmatch(span.rstrip(hpu.SOPA))
    if qamats_call is not None:
        return _qamats_entries(case, qamats_call)
    return [
        _entry(
            case,
            span,
            meteg_at - start,
            f"M{case['case_number']} {case['ref']}"
            + ("" if matched == case["mam_form"] else "; atom spans a template call"),
        )
    ]


def _qamats_entries(case, qamats_call):
    """M13's two entries, one per parameter of its ``{{מ:קמץ}}`` call.

    The Ashkenazic ``ד`` form and the Sephardic ``ס`` form differ only in the
    qamats, and both carry the meteg, so both lose it or the template starts
    varying something it does not exist to vary.
    """
    entries = []
    for param, hebrew_param in (("dalet", "ד"), ("samekh", "ס")):
        value = qamats_call.group(param)
        entries.append(
            _entry(
                case,
                value,
                value.index(METEG),
                f"M{case['case_number']} {case['ref']};"
                f" the {hebrew_param} parameter of its מ:קמץ call",
            )
        )
    return entries


def _entry(case, old, meteg_at, comment):
    if old.index(METEG) != meteg_at:
        raise SpecProblem(
            f"M{case['case_number']} {case['ref']}: the first meteg of {old!r} is not"
            " the one the record names, so the bot would remove the wrong mark"
        )
    return {
        "ch": hvn.INT_TO_STR_DIC[case["chapter"]],
        "old": old,
        "comment": comment,
    }


def _assert_in_its_own_verse(case, text, index):
    want = hvn.INT_TO_STR_DIC[case["verse"]]
    got = _verse_of(text, index)
    if got != want:
        raise SpecProblem(
            f"M{case['case_number']} {case['ref']}: its form was located in verse"
            f" {got!r} rather than the {want!r} the record names"
        )


def _addition_entry(case, chapter):
    """M23's single ``explicit-replacement`` entry."""
    old, new = case["mam_form"], case["comparison_form"]
    text = chapter["raw"]
    if text.count(old) != 1:
        raise SpecProblem(
            f"M{case['case_number']} {case['ref']}: its MAM form occurs"
            f" {text.count(old)} times in the chapter, not once"
        )
    _assert_in_its_own_verse(case, text, text.index(old))
    if new.replace(METEG, "", 1) != old:
        raise SpecProblem(
            f"M{case['case_number']} {case['ref']}: its replacement does not differ"
            " from its MAM form by exactly one added meteg"
        )
    return {
        "ch": hvn.INT_TO_STR_DIC[case["chapter"]],
        "old": old,
        "new": new,
        "comment": f"M{case['case_number']} {case['ref']}",
    }


def _build_specs(removals, additions, chapters):
    """Both specs, keyed by the path each belongs at."""
    removal_edits, acted_on = {}, []
    for case in removals:
        number = case["case_number"]
        if number in _ALREADY_APPLIED:
            _assert_still_applied(case, chapters)
            print(f"  M{number} {case['ref']}: excluded -- {_ALREADY_APPLIED[number]}")
            continue
        entries = _removal_entries(case, _chapter_of(chapters, case))
        removal_edits.setdefault(case["std_book_name"], []).extend(entries)
        acted_on.append(case)
    addition_edits = {}
    for case in additions:
        entry = _addition_entry(case, _chapter_of(chapters, case))
        addition_edits.setdefault(case["std_book_name"], []).append(entry)
    entry_count = sum(len(entries) for entries in removal_edits.values())
    print(
        f"  removal spec: {len(acted_on)} records -> {entry_count} entries"
        f" across {len(removal_edits)} books"
    )
    return {
        _REMOVAL_SPEC: {
            "summary": _removal_summary(acted_on, entry_count),
            "edit-kind": "meteg-removal",
            "edits": removal_edits,
        },
        _ADDITION_SPEC: {
            "summary": _addition_summary(additions),
            "edit-kind": "explicit-replacement",
            "edits": addition_edits,
        },
    }


def _assert_still_applied(case, chapters):
    """An excluded record has to stay excluded for the reason given."""
    text = _chapter_of(chapters, case)["raw"]
    std_text = uni_denorm.give_std_mark_order(text)
    form = case["mam_form"]
    if std_text.count(form[: form.index(METEG) + 1]) > 0:
        raise SpecProblem(
            f"M{case['case_number']} {case['ref']} is listed as already applied on"
            " Wikisource, but its meteg is back in the local text: either the wiki"
            " was reverted, or the exclusion is wrong"
        )


def _case_number_ranges(cases):
    """ "1-16, 19-22" for a run of case numbers, so a summary cannot drift."""
    numbers = sorted(case["case_number"] for case in cases)
    ranges, start, previous = [], numbers[0], numbers[0]
    for number in numbers[1:]:
        if number == previous + 1:
            previous = number
            continue
        ranges.append((start, previous))
        start = previous = number
    ranges.append((start, previous))
    return ", ".join(f"M{lo}" if lo == hi else f"M{lo}-M{hi}" for lo, hi in ranges)


def _removal_summary(cases, entry_count):
    return (
        f"Remove {entry_count} metegs per Daniel Holman's MAM suggestions"
        f" {_case_number_ranges(cases)}"
    )


def _addition_summary(cases):
    case = cases[0]
    return (
        f"Add a meteg at {case['ref']} per Daniel Holman's MAM suggestion"
        f" M{case['case_number']}"
    )


# ---------------------------------------------------------------- checking


def _check_specs_on_disk(built, cases, chapters):
    """The tracked files must equal what today's corpus builds, and must apply."""
    for path, spec in built.items():
        on_disk = _read_json(path)
        if on_disk != spec:
            raise SpecProblem(
                f"{path} differs from what the suggestions JSON and the current"
                " in/mam-ws text build; re-run with --write and read the diff"
            )
        print(f"  {path}: matches what today's corpus builds")
    _check_entries_apply(built, chapters)
    _check_coverage(built, cases)


def _check_entries_apply(built, chapters):
    """Every ``old`` occurs exactly once in both texts the bot may be handed."""
    problems, checked = [], 0
    for path, spec in built.items():
        for bk39id, entries in spec["edits"].items():
            for entry in entries:
                checked += 1
                chapter = chapters[bk39id][entry["ch"]]
                for which in ("raw", "big"):
                    count = chapter[which].count(entry["old"])
                    if count != 1:
                        problems.append(
                            f"{path} {bk39id} {entry['comment']}: occurs {count}"
                            f" times in the {which} text"
                        )
    if problems:
        raise SpecProblem(
            "an edit's old string is not unique:\n  " + "\n  ".join(problems)
        )
    print(f"  uniqueness: {checked} entries occur exactly once in both texts")


def _check_coverage(built, cases):
    """Each record reaches exactly one spec, or is excluded by name."""
    covered = {}
    for spec in built.values():
        for entries in spec["edits"].values():
            for entry in entries:
                matched = _COMMENT_CASE.match(entry["comment"])
                if matched is None:
                    raise SpecProblem(
                        f"an entry's comment {entry['comment']!r} does not open with"
                        " the case number it came from"
                    )
                number = int(matched.group("number"))
                covered.setdefault(number, 0)
                covered[number] += 1
    expected = {case["case_number"] for case in cases} - set(_ALREADY_APPLIED)
    if set(covered) != expected:
        raise SpecProblem(
            f"records covered {sorted(covered)} but expected {sorted(expected)}"
        )
    print(f"  coverage: {len(expected)} records, {sum(covered.values())} entries")
