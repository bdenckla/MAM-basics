"""Differential check: each Holman meteg suggestion against a live mgketer diff card.

Phase 3 of ``doc/PLAN-post-stress-meteg-page-and-holman-m23.md``.  Holman's page and
the mgketer comparison are two independent routes to the same thirty differences
between MAM and the Aleppo Codex, so each is an oracle for the other.  This module
matches them mechanically, where ``doc/holman-meteg-vs-mgketer.md`` matched them by
hand.

THE RUN IS ONE-TIME, AND IS MEANT TO STOP PASSING.  Items 3 through 7 of
``doc/PLAN-holman-meteg-rollout-programme.md`` apply all thirty suggestions to MAM and
then refresh mgketer, which is precisely what removes the thirty diff cards this check
reads.  Afterwards it finds no card for any of the thirty and fails for all thirty.
That is the designed end state.  Ben Denckla's decision, 2026-09-03: *"run it once as a
one-time check and don't wire it into the renderer."*  So nothing in a pipeline, a test
or a rendering command may depend on this module.  Had it been a required argument of
``py/main_verify_and_render_table.py``, the programme would have left the public Holman
pages unrenderable rather than merely unverified.

WHERE THE RESULT LIVES.  In the plan's phase-state section, and nowhere else.  The
check writes nothing into ``holman/docs-not-served/mam_suggestions.json``: the ingest
owns that file and rewrites it whole, so a summary parked there would disappear at the
next ingest without anyone being told.  A run that cannot be repeated has to leave its
result somewhere a rewrite cannot reach.

WHAT A MATCH REQUIRES

The check matches the complete atom and its accentuation, never consonants alone.  Per
record it takes the mgketer cards at that verse and keeps the ones whose MAM side
equals Holman's MAM form and whose mgketer side equals Holman's comparison form,
character for character.  Exactly one card must survive.

Matching whole forms is what tells 2 Samuel 18:3's two look-alike compounds apart.
That verse has לא־ישימו twice, and the two are filed in OPPOSITE mgketer categories:
Holman's M22 is the compound with a darga, where MAM has a meteg the Aleppo Codex
lacks, and the compound with a mahapakh is one where the Aleppo Codex has a meteg MAM
lacks and no Holman record covers it.  Only the accent separates them, so anything
matching on letters alone conflates them.

DIRECTION IS DERIVED THREE TIMES, FROM THREE SOURCES

1. From Holman's two forms, by ``mam_meteg_suggestions.direction``.
2. From the matched card's two forms, by the same arithmetic.
3. From the card's own category, ``mam-adds-meteg`` or ``mgketer-adds-meteg``.

All three must agree.  The tally to expect, measured 2026-09-03, is 29 removals and
one addition: M23 at Isaiah 23:12, where the Aleppo Codex has the meteg and MAM does
not.  M23 therefore passes only when the mgketer side, rather than the MAM side, has
the meteg.

EVERYTHING FAILS; NOTHING WARNS.  Missing, ambiguous and mismatched records are
collected and raised together at the end of the run rather than on first sight, so one
run enumerates every offender.  A missing input is a failure too: ``--mgketer-root`` is
required, and a by-book report the check cannot open raises.
"""

from __future__ import annotations

import html.parser
import re
from dataclasses import dataclass
from pathlib import Path

from hkq_cmn import mam_meteg_suggestions as mms
from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_points as hpo

_REPORTS_DIR = "out-reports"
_BY_BOOK_DIR = "by-book"
_BY_TYPE_DIR = "by-type"
_DIFFS_FILE = "diffs.html"

# mgketer files a diff under one of these two categories according to which side has
# the meteg, which is the third independent reading of a record's direction.
_CATEGORY_OF_DIRECTION = {
    mms.REMOVAL: "mam-adds-meteg",
    mms.ADDITION: "mgketer-adds-meteg",
}

# The roster as it stood on 2026-09-03: M1-M16, M18-M23, M25-M31 and M33, being all 34
# M records except the four accent-placement ones, M17, M24, M32 and M34.  The roster
# the run actually uses is DERIVED from the suggestions data; this table is only what
# the derived roster is compared against, so that a changed roster is reported rather
# than silently absorbed.
_BASELINE_ADDITIONS = (23,)
# fmt: off
_BASELINE_REMOVALS = (
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
    18, 19, 20, 21, 22,
    25, 26, 27, 28, 29, 30, 31,
    33,
)
# fmt: on
_BASELINE_ROSTER = {
    **{number: mms.REMOVAL for number in _BASELINE_REMOVALS},
    **{number: mms.ADDITION for number in _BASELINE_ADDITIONS},
}

# A card's ``diff-hash`` reads like ``1K7:24#8701a1ff``: mgketer's own book letters,
# then the chapter, verse and a content hash.  The book letters are not read here --
# the by-book report the card came from already settles the book -- so the pattern
# takes them non-greedily and only the chapter and verse are used.
_DIFF_HASH = re.compile(
    r"^(?P<book>.*?)(?P<chapter>\d+):(?P<verse>\d+)#(?P<hash>[0-9a-f]+)$"
)


class VerificationProblem(Exception):
    """A record the mgketer reports no longer bear out; raised, never worked around."""


@dataclass(frozen=True)
class Normalization:
    """One record-specific reading permitted before two forms are compared.

    ``why`` is reported with every run, so a normalization can never be applied
    without a reader of the output being told which record used it and on what
    grounds.
    """

    name: str
    why: str
    replacements: tuple[tuple[str, str], ...]

    def applied_to(self, form: str) -> str:
        for before, after in self.replacements:
            form = form.replace(before, after)
        return form


# Named, record-specific, and reported.  Nothing here is a general normalization: a
# rule applied to every record could hide a different reading, which is the one thing
# this check exists to catch.
_ALLOWED_NORMALIZATIONS = {
    13: Normalization(
        name="qamats qatan read as qamats",
        why=(
            "2 Chronicles 18:33's atom has a qamats qatan on the he in Holman's two"
            " forms.  mgketer's card displays a plain qamats on both sides, for two"
            " different reasons: its MAM string has the qamats qatan and its massaging"
            " pass rewrites it, which the card says in a tooltip and shows in its"
            " original-form span, while its Aleppo transcription has the plain qamats"
            " with no massaging at all.  The meteg claim, which is the whole of what"
            " this check reads, agrees on both sides."
        ),
        replacements=((hpo.QAMATS_Q, hpo.QAMATS),),
    ),
}


@dataclass(frozen=True)
class Card:
    """One mgketer diff card, reduced to what this check reads."""

    diff_hash: str
    chapter: int | None
    verse: int | None
    categories: frozenset[str]
    subcategory: str
    mam: str
    mgketer: str
    mam_original: str
    mgketer_original: str
    massaging: str | None

    def direction(self) -> str | None:
        """The edit that would make the MAM side agree with the mgketer side."""
        meteg = mms.METEG
        if meteg in self.mam and self.mam.replace(meteg, "", 1) == self.mgketer:
            return mms.REMOVAL
        if meteg in self.mgketer and self.mgketer.replace(meteg, "", 1) == self.mam:
            return mms.ADDITION
        return None


class _CardParser(html.parser.HTMLParser):
    """Pull the diff cards out of one mgketer report.

    The two sides are read by class rather than by position: a side's own label, and
    the ``original``/``massaged`` labels a massaged side has, are dropped, and the
    original form is kept apart from the displayed one.  Everything else inside a side
    -- the highlighted letters and the surrounding context alike -- is the form as
    mgketer displays it.
    """

    def __init__(self) -> None:
        super().__init__()
        self.cards: list[Card] = []
        self._stack: list[tuple[str, frozenset[str]]] = []
        self._card: dict | None = None

    def handle_starttag(self, tag, attrs) -> None:
        attrs_dict = dict(attrs)
        classes = frozenset((attrs_dict.get("class") or "").split())
        self._stack.append((tag, classes))
        if "diff-card" in classes:
            self._card = {
                "categories": frozenset(
                    (attrs_dict.get("data-categories") or "").split()
                ),
                "diff_hash": "",
                "subcategory": "",
                "mam": "",
                "mgketer": "",
                "mam_original": "",
                "mgketer_original": "",
                "massaging": None,
            }
        if self._card is not None and "massage-mask" in classes:
            self._card["massaging"] = attrs_dict.get("title")

    def handle_endtag(self, tag) -> None:
        while self._stack:
            popped, classes = self._stack.pop()
            if "diff-card" in classes and self._card is not None:
                self.cards.append(_card_of(self._card))
                self._card = None
            if popped == tag:
                break

    def handle_data(self, data) -> None:
        if self._card is None:
            return
        classes: set[str] = set()
        for _tag, tag_classes in self._stack:
            classes |= tag_classes
        if "side-label" in classes or "orig-label" in classes:
            return
        key = _collected_key(classes)
        if key is not None:
            self._card[key] += data


def _collected_key(classes: set[str]) -> str | None:
    """Which field of a part-built card this run of text belongs to, if any."""
    if "diff-hash" in classes:
        return "diff_hash"
    if "subcat-text" in classes:
        return "subcategory"
    original = "orig-text" in classes
    if "mam-side" in classes:
        return "mam_original" if original else "mam"
    if "mgk-side" in classes:
        return "mgketer_original" if original else "mgketer"
    return None


def _card_of(collected: dict) -> Card:
    diff_hash = collected["diff_hash"].strip()
    matched = _DIFF_HASH.match(diff_hash)
    return Card(
        diff_hash=diff_hash,
        chapter=int(matched.group("chapter")) if matched else None,
        verse=int(matched.group("verse")) if matched else None,
        categories=collected["categories"],
        subcategory=collected["subcategory"].strip(),
        mam=collected["mam"].strip(),
        mgketer=collected["mgketer"].strip(),
        mam_original=collected["mam_original"].strip(),
        mgketer_original=collected["mgketer_original"].strip(),
        massaging=collected["massaging"],
    )


def cards_in(path: Path) -> list[Card]:
    """Every diff card in one mgketer report.  A report that is absent RAISES."""
    if not path.is_file():
        raise VerificationProblem(
            f"no mgketer report at {path.as_posix()}; --mgketer-root must name a"
            " checkout of MAM-private/mgketer whose out-reports/ has been generated"
        )
    parser = _CardParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.cards


def _by_book_path(mgketer_root: Path, std_book_name: str) -> Path:
    ordered = tbn.ordered_short_dash_full_39(std_book_name)
    return mgketer_root / _REPORTS_DIR / _BY_BOOK_DIR / ordered / _DIFFS_FILE


def _cards_with(cards: list[Card], mam: str, mgketer: str) -> list[Card]:
    """The cards displaying exactly these two forms, one per side."""
    return [card for card in cards if card.mam == mam and card.mgketer == mgketer]


def _matching_cards(
    case, at_verse: list[Card]
) -> tuple[list[Card], Normalization | None]:
    """The cards this record names, and the normalization it took to see them.

    Holman's forms are tried verbatim first, so a record whose allowlist entry has
    stopped being needed reports that rather than going on quietly using it.
    """
    matched = _cards_with(at_verse, case["mam_form"], case["comparison_form"])
    if matched:
        return matched, None
    normalization = _ALLOWED_NORMALIZATIONS.get(case["case_number"])
    if normalization is None:
        return [], None
    normalized = _cards_with(
        at_verse,
        normalization.applied_to(case["mam_form"]),
        normalization.applied_to(case["comparison_form"]),
    )
    return (normalized, normalization) if normalized else ([], None)


def _forms_line(label: str, mam: str, mgketer: str) -> str:
    return f"      {label}: MAM {mam} / mgketer {mgketer}"


def _describe_candidates(cards: list[Card]) -> list[str]:
    return [
        f"      {card.diff_hash} [{','.join(sorted(card.categories))}]"
        f" {card.subcategory}: MAM {card.mam} / mgketer {card.mgketer}"
        for card in cards
    ]


def _check_roster(cases, lines: list[str], problems: list[str]) -> None:
    """The derived roster against the baseline the plan and the evidence note name."""
    derived = {case["case_number"]: mms.direction(case) for case in cases}
    removals = sorted(n for n, d in derived.items() if d == mms.REMOVAL)
    additions = sorted(n for n, d in derived.items() if d == mms.ADDITION)
    lines.append(
        f"roster derived from the suggestions data: {len(derived)} meteg records"
        f" ({len(removals)} removal, {len(additions)} addition)"
    )
    lines.append("  removals: " + ", ".join(f"M{n}" for n in removals))
    lines.append("  additions: " + ", ".join(f"M{n}" for n in additions))
    if derived == _BASELINE_ROSTER:
        lines.append(
            f"  matches the 2026-09-03 baseline of {len(_BASELINE_ROSTER)} records"
        )
        return
    gained = sorted(set(derived) - set(_BASELINE_ROSTER))
    lost = sorted(set(_BASELINE_ROSTER) - set(derived))
    turned = sorted(
        number
        for number in set(derived) & set(_BASELINE_ROSTER)
        if derived[number] != _BASELINE_ROSTER[number]
    )
    problems.append(
        "the derived roster differs from the 2026-09-03 baseline:"
        f" gained {[f'M{n}' for n in gained]},"
        f" lost {[f'M{n}' for n in lost]},"
        f" changed direction {[f'M{n}' for n in turned]}"
    )


def _check_case(case, cards: list[Card], lines: list[str], problems: list[str]) -> bool:
    """One record against its book's cards.  True when a normalization was needed."""
    number, ref = case["case_number"], case["ref"]
    at_verse = [
        card
        for card in cards
        if card.chapter == case["chapter"] and card.verse == case["verse"]
    ]
    if not at_verse:
        problems.append(f"M{number} {ref}: no mgketer card at this verse at all")
        return False
    matched, normalization = _matching_cards(case, at_verse)
    if not matched:
        problems.append(
            f"M{number} {ref}: none of the {len(at_verse)} mgketer card(s) at this"
            " verse has both of Holman's forms\n"
            + _forms_line("Holman", case["mam_form"], case["comparison_form"])
            + "\n"
            + "\n".join(_describe_candidates(at_verse))
        )
        return False
    if len(matched) > 1:
        problems.append(
            f"M{number} {ref}: {len(matched)} mgketer cards have both of Holman's"
            " forms, so no single card can be named\n"
            + "\n".join(_describe_candidates(matched))
        )
        return False
    card = matched[0]
    holman_direction = mms.direction(case)
    card_direction = card.direction()
    wanted_category = _CATEGORY_OF_DIRECTION[holman_direction]
    if card_direction != holman_direction:
        problems.append(
            f"M{number} {ref}: Holman's forms give direction {holman_direction!r}"
            f" but {card.diff_hash}'s forms give {card_direction!r}"
        )
    elif wanted_category not in card.categories:
        problems.append(
            f"M{number} {ref}: {card.diff_hash} is filed under"
            f" {sorted(card.categories)} rather than under {wanted_category!r}"
        )
    else:
        lines.append(
            f"M{number} {ref}: {card.diff_hash} {holman_direction}"
            f" [{card.subcategory}] MAM {card.mam} / mgketer {card.mgketer}"
        )
        if normalization is not None:
            lines.append(f"    normalization applied: {normalization.name}")
        if card.massaging is not None:
            lines.append(f"    mgketer massaging on this card: {card.massaging}")
    return normalization is not None


def _by_type_totals(mgketer_root: Path, lines: list[str]) -> None:
    """The two Tanakh-wide meteg totals, as context for the programme's item 7.

    Reported rather than asserted: they count every meteg difference in the whole
    comparison, not the thirty records this check is about, and item 7 expects both to
    fall once the suggestions have been applied.
    """
    for category in sorted(set(_CATEGORY_OF_DIRECTION.values())):
        path = mgketer_root / _REPORTS_DIR / _BY_TYPE_DIR / f"{category}.html"
        lines.append(f"mgketer by-type total, {category}: {len(cards_in(path))} diffs")


def verify(mgketer_root: Path) -> list[str]:
    """Check every derived meteg record, and raise with every offender it found."""
    cases = mms.load_meteg_cases()
    lines = [f"mgketer reports read from {mgketer_root.as_posix()}"]
    problems: list[str] = []
    _check_roster(cases, lines, problems)
    lines.append("")
    cards_by_book: dict[str, list[Card]] = {}
    normalized: set[int] = set()
    for case in cases:
        book = case["std_book_name"]
        if book not in cards_by_book:
            cards_by_book[book] = cards_in(_by_book_path(mgketer_root, book))
        if _check_case(case, cards_by_book[book], lines, problems):
            normalized.add(case["case_number"])
    lines.append("")
    _report_normalizations(normalized, lines, problems)
    lines.append("")
    _by_type_totals(mgketer_root, lines)
    if problems:
        lines.append("")
        lines.append(f"FAILED with {len(problems)} problem(s):")
        lines.extend(f"  {problem}" for problem in problems)
        raise VerificationProblem("\n".join(lines))
    lines.append("")
    lines.append(
        f"PASSED: all {len(cases)} Holman meteg records match one mgketer diff card"
    )
    return lines


def _report_normalizations(
    normalized: set[int], lines: list[str], problems: list[str]
) -> None:
    """Say which allowlist entries fired, and fail on one that did not.

    A stale entry is the failure this repository's rule against silent green names: it
    would go on permitting a reading nothing needs any more, and no run would say so.
    """
    lines.append(f"display-artifact allowlist: {len(_ALLOWED_NORMALIZATIONS)} entry(s)")
    for number, normalization in sorted(_ALLOWED_NORMALIZATIONS.items()):
        fired = "applied" if number in normalized else "NOT NEEDED"
        lines.append(f"  M{number} {normalization.name}: {fired}")
        lines.append(f"    {normalization.why}")
    unused = sorted(set(_ALLOWED_NORMALIZATIONS) - normalized)
    if unused:
        problems.append(
            "allowlisted normalization(s) that no record needed, so the allowlist is"
            f" stale: {[f'M{n}' for n in unused]}"
        )
