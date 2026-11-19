"""
Credits in the MAM change logs for contributors other than Ben Denckla and Avi Kadish.

``in/mam-change-log-credits.json`` is hand-maintained, and a credit is recorded there only on
Ben's word: his decisions of 2026-11-19, which ``doc/PLAN-change-log-credits.md`` records. A
record names a contributor, a verse, exactly one selector of the change it credits, its
evidence, and when and on what basis it was recorded. The selectors are ``change``, equal to
one of a change-log entry's ``changes`` pairs, and ``templates``, equal to a structural entry's
``templates_added`` and ``templates_removed``. The keys, the selectors and the evidence kinds
are closed: anything else raises.

``generate_report`` gives each diff the records at its verse, whatever the entry point, so
that a standalone report and the published one agree. ``mpplus_json`` then lists on an entry
each record whose selector the entry holds, and ``mpplus_html`` puts a line on the card of
each credited pair and gives that card an id, ``card_id``. ``run_all`` calls
``require_each_record_matched_once`` after it writes every report and before it writes
contributors.html and the index: it reads the reports' JSON back, stops unless each record
matched exactly one entry across them, and returns the matches, from which
``mpplus_contributors`` writes contributors.html.

Exports:
    Credit                           — one validated record, with its contributor's name
    CreditError                      — a broken rule of the file, or an unmatched record
    Match                            — a record and the one entry it matched
    load_credits                     — read and validate the credits file
    give_diffs_their_records         — give each diff the records at its verse
    entry_records                    — the records whose selector a serialized entry holds
    serialize                        — a record as a change log's JSON lists it
    card_id                          — the id of the card that shows a record's change
    user_page_url                    — a contributor's Hebrew Wikisource user page, or None
    require_each_record_matched_once — the completeness check of ``run_all``, which returns
                                       each record's match
"""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re

from mb_cmn import paths
from mb_cmn.he_wikisource_url import (
    he_diff_url,
    he_page_url,
    he_permanent_section_url,
)
from mb_cmn.mam_google_sheet_url import changes_tab_row_url

CREDITS_JSON = paths.repo_root() / "in" / "mam-change-log-credits.json"

_TOP_KEYS = frozenset({"_header", "contributors", "credits"})
_CONTRIBUTOR_KEYS = frozenset({"name", "user_page"})
_RECORD_KEYS = frozenset(
    {"contributor", "book", "chapter", "verse", "evidence", "recorded"}
)
_SELECTORS = frozenset({"change", "templates"})
_RECORDED_KEYS = frozenset({"on", "basis"})
_EVIDENCE_KEYS = {
    "he-wikisource-section": frozenset({"kind", "page", "oldid", "section"}),
    "he-wikisource-diff": frozenset({"kind", "page", "diff", "oldid"}),
    "mam-sheet-changes-row": frozenset({"kind", "row"}),
}
_CONTRIBUTOR_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Hebrew Wikisource's name for its User namespace.
_USER_NAMESPACE = "משתמש"


class CreditError(ValueError):
    """The credits file breaks a rule of its format, or a record matches no single entry
    or card."""


@dataclass(frozen=True)
class Credit:
    """One record of the credits file, validated, with its contributor's name and user page.

    ``number`` is the record's one-based position in the file. ``evidence`` holds, for each
    piece of evidence, its kind, the label of its link on a card, and its URL.
    """

    number: int
    contributor: str
    name: str
    user_page: str | None
    book: str
    chapter: int
    verse: int
    change: tuple[str, str] | None
    templates: tuple[tuple[str, ...], tuple[str, ...]] | None
    evidence: tuple[tuple[str, str, str], ...]

    def describe(self):
        """Name the record for a message."""
        if self.change is not None:
            selector = f"change {self.change[0]} to {self.change[1]}"
        else:
            added, removed = self.templates
            selector = f"templates added {list(added)}, removed {list(removed)}"
        return (
            f"record {self.number} ({self.contributor}, {self.book}"
            f" {self.chapter}:{self.verse}, {selector})"
        )


@dataclass(frozen=True)
class Match:
    """A record and the one entry it matched.

    ``report`` is the name of the entry's report, such as ``2026-09-17`` or
    ``unpinned-latest``, and ``entry`` the entry's one-based position in that report's JSON.
    """

    credit: Credit
    report: str
    entry: int


def _require(condition, message):
    if not condition:
        raise CreditError(f"{CREDITS_JSON.name}: {message}")


def _require_keys(obj, keys, where):
    _require(isinstance(obj, dict), f"{where} is not an object")
    _require(
        set(obj) == set(keys),
        f"{where} has the keys {sorted(obj)}, not {sorted(keys)}",
    )


def _is_text(value):
    return isinstance(value, str) and bool(value) and value.strip() == value


def _is_positive_int(value):
    # A bool is an int to Python, and is no number here.
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _evidence_link(item, where):
    """Return one piece of evidence as its kind, its link's label and its URL."""
    _require(isinstance(item, dict) and "kind" in item, f"{where} has no kind")
    kind = item["kind"]
    _require(kind in _EVIDENCE_KEYS, f"{where} has the unknown kind {kind!r}")
    _require_keys(item, _EVIDENCE_KEYS[kind], where)
    if kind == "he-wikisource-section":
        _require(
            _is_text(item["page"])
            and _is_text(item["section"])
            and _is_positive_int(item["oldid"]),
            f"{where} needs a page, a section and a revision number",
        )
        url = he_permanent_section_url(item["page"], item["oldid"], item["section"])
        return kind, "report", url
    if kind == "he-wikisource-diff":
        _require(
            _is_text(item["page"])
            and _is_positive_int(item["diff"])
            and _is_positive_int(item["oldid"]),
            f"{where} needs a page and two revision numbers",
        )
        return kind, "fix", he_diff_url(item["page"], item["diff"], item["oldid"])
    if kind == "mam-sheet-changes-row":
        _require(_is_positive_int(item["row"]), f"{where} needs a row number")
        return kind, f"Sheet row {item['row']}", changes_tab_row_url(item["row"])
    raise AssertionError(f"no handler for the evidence kind {kind!r}")


def _string_list(value):
    return isinstance(value, list) and all(_is_text(name) for name in value)


def _credit(number, record, contributors):
    where = f"credit {number}"
    _require(isinstance(record, dict), f"{where} is not an object")
    selectors = _SELECTORS & set(record)
    _require(
        len(selectors) == 1, f"{where} must have exactly one of change and templates"
    )
    _require_keys(record, _RECORD_KEYS | selectors, where)
    ident = record["contributor"]
    _require(ident in contributors, f"{where} names {ident!r}, which is no contributor")
    _require(_is_text(record["book"]), f"{where} has no book")
    _require(
        _is_positive_int(record["chapter"]) and _is_positive_int(record["verse"]),
        f"{where} needs a chapter number and a verse number",
    )
    change = None
    templates = None
    if "change" in record:
        pair = record["change"]
        _require_keys(pair, ("old", "new"), f"{where}'s change")
        _require(
            _is_text(pair["old"]) and _is_text(pair["new"]),
            f"{where}'s change needs two forms",
        )
        _require(pair["old"] != pair["new"], f"{where}'s change changes nothing")
        change = (pair["old"], pair["new"])
    else:
        named = record["templates"]
        _require_keys(named, ("added", "removed"), f"{where}'s templates")
        _require(
            _string_list(named["added"]) and _string_list(named["removed"]),
            f"{where}'s templates need two lists of template names",
        )
        _require(named["added"] or named["removed"], f"{where}'s templates name none")
        templates = (tuple(named["added"]), tuple(named["removed"]))
    evidence = record["evidence"]
    _require(isinstance(evidence, list) and evidence, f"{where} has no evidence")
    links = tuple(
        _evidence_link(item, f"{where}'s evidence {index}")
        for index, item in enumerate(evidence, start=1)
    )
    recorded = record["recorded"]
    _require_keys(recorded, _RECORDED_KEYS, f"{where}'s recorded")
    _require(
        isinstance(recorded["on"], str) and _DATE.fullmatch(recorded["on"]),
        f"{where} was recorded on no date of the form YYYY-MM-DD",
    )
    _require(_is_text(recorded["basis"]), f"{where} was recorded on no basis")
    contributor = contributors[ident]
    return Credit(
        number=number,
        contributor=ident,
        name=contributor["name"],
        user_page=contributor["user_page"],
        book=record["book"],
        chapter=record["chapter"],
        verse=record["verse"],
        change=change,
        templates=templates,
        evidence=links,
    )


def load_credits():
    """Read and validate the credits file; return its records as ``Credit``, in file order."""
    with open(CREDITS_JSON, "r", encoding="utf-8") as in_fp:
        data = json.load(in_fp)
    _require_keys(data, _TOP_KEYS, "the file")
    header = data["_header"]
    _require(
        isinstance(header, list) and header and _string_list(header),
        "_header is not a list of lines",
    )
    contributors = data["contributors"]
    _require(isinstance(contributors, dict), "contributors is not an object")
    for ident, contributor in contributors.items():
        where = f"contributor {ident!r}"
        _require(
            _CONTRIBUTOR_ID.fullmatch(ident),
            f"{where}: an id is lowercase ASCII letters and digits, joined by hyphens",
        )
        _require_keys(contributor, _CONTRIBUTOR_KEYS, where)
        _require(_is_text(contributor["name"]), f"{where} has no name")
        _require(
            contributor["user_page"] is None or _is_text(contributor["user_page"]),
            f"{where}'s user_page is neither a user name nor null",
        )
    records = data["credits"]
    _require(isinstance(records, list), "credits is not a list")
    credits = [
        _credit(number, record, contributors)
        for number, record in enumerate(records, start=1)
    ]
    seen = {}
    for credit in credits:
        key = (
            credit.contributor,
            credit.book,
            credit.chapter,
            credit.verse,
            credit.change,
            credit.templates,
        )
        _require(
            key not in seen,
            f"credits {seen.get(key)} and {credit.number} credit one contributor"
            " for one change",
        )
        seen[key] = credit.number
    uncredited = sorted(set(contributors) - {credit.contributor for credit in credits})
    _require(not uncredited, f"the contributors {uncredited} have no credit")
    return credits


def give_diffs_their_records(diffs, credits):
    """Give each diff at a credited verse, as ``credit_records``, the records at its verse."""
    by_verse = {}
    for credit in credits:
        by_verse.setdefault((credit.book, credit.chapter, credit.verse), []).append(
            credit
        )
    for diff in diffs:
        records = by_verse.get((diff["book"], diff["chapter"], diff["verse"]))
        if records:
            diff["credit_records"] = tuple(records)


def _at_verse(credit, entry):
    return (credit.book, credit.chapter, credit.verse) == (
        entry["book"],
        entry["chapter"],
        entry["verse"],
    )


def entry_records(records, entry):
    """The records whose selector this serialized change-log entry holds.

    A ``change`` record is held by an entry with a pair equal to its change, and a
    ``templates`` record by a structural entry, one without ``changes``, whose
    ``templates_added`` and ``templates_removed`` equal its templates.
    """
    records = [credit for credit in records if _at_verse(credit, entry)]
    if "changes" in entry:
        pairs = {(pair["old"], pair["new"]) for pair in entry["changes"]}
        return [credit for credit in records if credit.change in pairs]
    templates = (
        tuple(entry.get("templates_added", ())),
        tuple(entry.get("templates_removed", ())),
    )
    return [credit for credit in records if credit.templates == templates]


def serialize(credit):
    """A credit as a change log's JSON lists it on the entry it credits."""
    out = {"contributor": credit.contributor, "name": credit.name}
    if credit.change is not None:
        out["change"] = {"old": credit.change[0], "new": credit.change[1]}
    else:
        added, removed = credit.templates
        out["templates"] = {"added": list(added), "removed": list(removed)}
    out["evidence"] = [{"kind": kind, "url": url} for kind, _, url in credit.evidence]
    return out


def card_id(credit):
    """The HTML id of the card that shows the change a record credits.

    The id is ``credit-<book>-<chapter>-<verse>-<digest>``, the digest being the first 8 hex
    digits of the SHA-256 of the record's selector, ``{"change": ...}`` or
    ``{"templates": ...}`` as the file has it, written as compact JSON with sorted keys and
    encoded in UTF-8. It depends on the record's verse and selector alone, so adding records
    or reordering them changes no other card's id, and the records that credit one change
    give its card one id. A book's spaces become hyphens, since an id holds no space; Song of
    Songs is the one book whose name has any. ``mpplus_html`` gives a credited card the id of
    its first credit; a later card of the same report whose id would repeat an earlier
    card's gets -2, -3 and so on after it.
    """
    if credit.change is not None:
        selector = {"change": {"old": credit.change[0], "new": credit.change[1]}}
    elif credit.templates is not None:
        added, removed = credit.templates
        selector = {"templates": {"added": list(added), "removed": list(removed)}}
    else:
        raise AssertionError(f"record {credit.number} has neither change nor templates")
    encoded = json.dumps(
        selector, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    digest = hashlib.sha256(encoded).hexdigest()[:8]
    book = credit.book.replace(" ", "-")
    return f"credit-{book}-{credit.chapter}-{credit.verse}-{digest}"


def user_page_url(credit):
    """The contributor's user page on Hebrew Wikisource, or None when there is none."""
    if credit.user_page is None:
        return None
    return he_page_url(f"{_USER_NAMESPACE}:{credit.user_page}")


def require_each_record_matched_once(change_log_dir, report_names):
    """Stop unless each record of the credits file matched exactly one entry.

    It reads the JSON of the named reports in ``change_log_dir`` back, so that it checks
    what was written rather than a second computation of it. A record matched no entry when
    a refresh changed the form it credits, or when it was mistyped; it matched more than one
    when the same change was made twice. It returns each record's ``Match``, in the file's
    order, for ``mpplus_contributors.write_contributors``.
    """
    credits = load_credits()
    expected = [serialize(credit) for credit in credits]
    found = [[] for _ in credits]
    for name in report_names:
        with open(Path(change_log_dir) / f"{name}.json", "r", encoding="utf-8") as fp:
            entries = json.load(fp)["diffs"]
        for position, entry in enumerate(entries, start=1):
            for listed in entry.get("credits", ()):
                for index, credit in enumerate(credits):
                    if _at_verse(credit, entry) and listed == expected[index]:
                        found[index].append((name, position))
    problems = [
        f"  {credit.describe()} matched "
        + (
            "; ".join(f"{name}.json, entry {position}" for name, position in where)
            if where
            else "no entry"
        )
        for credit, where in zip(credits, found)
        if len(where) != 1
    ]
    if problems:
        raise CreditError(
            "Each record of"
            f" {CREDITS_JSON.relative_to(paths.repo_root()).as_posix()} must match"
            " exactly one entry of the change log, and these do not:\n"
            + "\n".join(problems)
            + "\nMend each record, then restore gh-pages/MAM-with-doc/change-log/ with"
            " git restore and run py/main_diff.py mpplus --all again."
        )
    return [
        Match(credit=credit, report=where[0][0], entry=where[0][1])
        for credit, where in zip(credits, found)
    ]
