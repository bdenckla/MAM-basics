"""Compute documentation figures not held in the build-population snapshot.

Figures come from the dataset, current MAM-parsed-plus and the Aleppo coverage
index. Counts must agree with the build's classifications. Template walks use
the closed phase-2 rule table and fail on unknown structures. Coverage ranges
include both endpoints; books absent from the index have no surviving leaf.
Generated page differences expose changes in computed figures.
"""

import copy
import json
from near_aleppo import frozen_ketiv
from near_aleppo import editorial_ketiv
from near_aleppo import reviewed_ketiv
import unicodedata
from collections import Counter
from typing import NamedTuple

from near_aleppo import build_paths
from near_aleppo import consumer_notice
from near_aleppo import phase2_templates as phase2
from near_aleppo import phase3_policies as phase3
from near_aleppo import phase5_readings as phase5
from near_aleppo import phase6_flags
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER
from near_aleppo.phase6_rename import RENAMED_NOTES

# Each book as main_build.py names it, with the name the codex index gives it, as the
# census's aleppo_extant_conventions.py spells the index's names. A book whose name
# the index does not list has no surviving leaf.
_INDEX_BOOK = {
    "A1-Genesis": "Gen",
    "A2-Exodus": "Exod",
    "A3-Levit": "Lev",
    "A4-Numbers": "Num",
    "A5-Deuter": "Deut",
    "B1-Joshua": "Josh",
    "B2-Judges": "Judg",
    'BA-Samuel שמ"א': "1 Sam",
    'BA-Samuel שמ"ב': "2 Sam",
    'BC-Kings מל"א': "1 Kgs",
    'BC-Kings מל"ב': "2 Kgs",
    "C1-Isaiah": "Isa",
    "C2-Jeremiah": "Jer",
    "C3-Ezekiel": "Ezek",
    "CA-The-12-Minor-Prophets הושע": "Hos",
    "CA-The-12-Minor-Prophets יואל": "Joel",
    "CA-The-12-Minor-Prophets עמוס": "Amos",
    "CA-The-12-Minor-Prophets עבדיה": "Obad",
    "CA-The-12-Minor-Prophets יונה": "Jonah",
    "CA-The-12-Minor-Prophets מיכה": "Mic",
    "CA-The-12-Minor-Prophets נחום": "Nah",
    "CA-The-12-Minor-Prophets חבקוק": "Hab",
    "CA-The-12-Minor-Prophets צפניה": "Zeph",
    "CA-The-12-Minor-Prophets חגי": "Hag",
    "CA-The-12-Minor-Prophets זכריה": "Zech",
    "CA-The-12-Minor-Prophets מלאכי": "Mal",
    "D1-Psalms": "Ps",
    "D2-Proverbs": "Prov",
    "D3-Job": "Job",
    "E1-Song of Songs": "Song",
    "E2-Ruth": "Ruth",
    "E3-Lamentations": "Lam",
    "E4-Ecclesiastes": "Eccl",
    "E5-Esther": "Esth",
    "F1-Daniel": "Dan",
    "FA-Ezra-Nexemiah עזרא": "Ezra",
    "FA-Ezra-Nexemiah נחמיה": "Neh",
    'FC-Chronicles דה"א': "1 Chron",
    'FC-Chronicles דה"ב': "2 Chron",
}

# The chapters holding the two Decalogues and Genesis 35, where the page says no leaf
# of the codex survives.
_DECALOGUES_AND_GENESIS_35 = (
    ("A1-Genesis", "35"),
    ("A2-Exodus", "20"),
    ("A5-Deuter", "5"),
)

_C, _D, _E = 0, 1, 2
_TARGET = "1"
_BODY = "2"
_FLAGS = frozenset((phase2.APPLIED_AND_FLAGGED, phase2.FLAGGED_NOT_APPLIED))
_MAM_NAMES = {renamed: name for name, renamed in RENAMED_NOTES.items()}
# The templates a special-letter word's parameter 1 has round its special letter, each
# with one parameter, the letter and its marks.
_SPECIAL_LETTERS = frozenset(("מ:אות-ג", "מ:אות-ק", "מ:אות תלויה"))
_INVERTED_NUN = "מ:נו״ן הפוכה"

_VARIKA = "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"
_UPPER_DOT = "\N{HEBREW MARK UPPER DOT}"
_LOWER_DOT = "\N{HEBREW MARK LOWER DOT}"
# The marks the page says the dataset keeps as MAM has them.
_KEPT_MARKS = {
    "rafe": "\N{HEBREW POINT RAFE}",
    "holam_haser_for_vav": "\N{HEBREW POINT HOLAM HASER FOR VAV}",
    "deḥi": "\N{HEBREW ACCENT DEHI}",
}
# Rule 4's testimony to the codex's lost parts, and the photographs of its pages,
# which rule 4 counts as readings of its text.
_TESTIMONY = frozenset(("א(ו)", "א(ס)", "א(ע)", "א(ק)", "א(ר)"))
_PHOTOGRAPH = "א(צילום)"

# The zones of a cell that a walk meets: the text, and the three kinds of parameter
# that are not the dataset's Scripture.
_TEXT = "text"
_NOTE_BODY = "note body"
_MAM_TARGET = "MAM's target"
_FLAG_VALUE = "flag value"
# The two sides a walk reads.
_DATASET = "dataset"
_MAM = "MAM-parsed-plus"

# Phase 5's populations that direct_clauses repeats, and the snapshot's names for
# them.
_READ = "codex readings: "
_PHASE5_TOTALS = {
    "elements": _READ + "direct codex siglum elements",
    "clauses": _READ + "direct differing clauses",
    "verses": _READ + "verses with a direct differing clause",
}
# The snapshot's lists of the verses where phase 5 writes a reading, which may bring a
# mark MAM's text lacks.
_PHASE5_WRITES = (
    _READ + "applied, the form replacing the whole of a plain target",
    _READ + "applied, the form replacing named atoms of a plain target",
    _READ + "applied, the form written into the selected parameter of the one kept "
    "template that is the target",
    _READ + "pointed ketiv written as the form stands",
    _READ + "pointed ketiv written with a named adjustment",
)


def figures(snapshot):
    """Every computed figure of the page, by name.

    ``snapshot`` is the build's population snapshot, as build_expectations.load()
    returns it, against which the readings repeated here from the build are checked.
    """
    corpus = _Corpus()
    index = _CodexIndex()
    out = {}
    out.update(_cells(corpus))
    out.update(_survival(corpus, index))
    out.update(_testimony(corpus, index, snapshot))
    out.update(_varika(corpus))
    out.update(_kept_marks(corpus, snapshot))
    out.update(_dots(corpus))
    out.update(_pointed_ketiv(corpus))
    out.update(_rule8(corpus))
    out.update(_new_characters(corpus))
    out.update(_silence(corpus))
    out.update(_deferred_qere_maqaf(corpus))
    out.update(_inverted_nuns(corpus))
    out.update(_absent_in_copies(corpus))
    return out


def _deferred_qere_maqaf(corpus):
    """Require the source note's special ketiv/qere target and qere-side clause.

    The page names 2 Samuel 8:3 as deferred maqaf work. Phase 3 deliberately does
    not apply its qere-side clause; verify the source with the closed template walk.
    """
    ref = ('BA-Samuel שמ"ב', "8", "3")
    verses = [verse for verse in corpus.verses if verse.ref == ref]
    if len(verses) != 1:
        raise AssertionError(f"{ref}: expected one source verse")
    matches = []
    for _, template in _templates(verses[0].mam[_E], ref, _MAM):
        if template["tmpl_name"] != "נוסח":
            continue
        params = template["tmpl_params"]
        target = params[_TARGET]
        if not isinstance(target, dict) or target["tmpl_name"] != "מ:כו״ק מיוחד":
            continue
        if target["tmpl_params"]["1"] != "בנהר":
            continue
        clauses = phase3._clauses(params[_BODY], ref)
        qere_clauses = [clause for clause in clauses if clause.startswith("א-קרי=")]
        if len(qere_clauses) != 1:
            raise AssertionError(f"{ref}: expected one source א-קרי clause")
        if phase3.MAQAF not in phase3._selected_text(target["tmpl_params"]["2"], ref):
            raise AssertionError(f"{ref}: the source qere lacks the described maqaf")
        matches.append(template)
    if len(matches) != 1:
        raise AssertionError(f"{ref}: expected one source special ketiv/qere note")
    return {"deferred_qere_maqaf_sites": [ref]}


class _Verse(NamedTuple):
    """One verse: its name as main_build.py gives it, and the two sides' three cells."""

    ref: tuple
    mam: list
    data: list


class _Corpus:
    """Every verse of the dataset, in its order, with MAM-parsed-plus's beside it."""

    def __init__(self):
        mam_paths = sorted(build_paths.mam_parsed_plus_dir().glob("*.json"))
        data_paths = sorted(build_paths.dataset_dir().glob("*.json"))
        if [p.name for p in mam_paths] != [p.name for p in data_paths]:
            raise AssertionError("the dataset's book files are not MAM-parsed-plus's")
        self.files = len(data_paths)
        self.verses = []
        for mam_path, data_path in zip(mam_paths, data_paths):
            mam_book = json.loads(mam_path.read_text(encoding="utf-8"))
            data_book = json.loads(data_path.read_text(encoding="utf-8"))
            if len(mam_book["book39s"]) != len(data_book["book39s"]):
                raise AssertionError(f"{data_path.name}: the books differ")
            for mam39, data39 in zip(mam_book["book39s"], data_book["book39s"]):
                if mam39["sub_book_name"] != data39["sub_book_name"]:
                    raise AssertionError(f"{data_path.name}: the sub-books differ")
                book = data_path.stem
                if data39["sub_book_name"] is not None:
                    book += " " + data39["sub_book_name"]
                if book not in _INDEX_BOOK:
                    raise AssertionError(f"{book!r} has no entry in _INDEX_BOOK")
                if list(mam39["chapters"]) != list(data39["chapters"]):
                    raise AssertionError(f"{book}: the chapters differ")
                for chapter, data_verses in data39["chapters"].items():
                    mam_verses = mam39["chapters"][chapter]
                    if list(mam_verses) != list(data_verses):
                        raise AssertionError(f"{book} {chapter}: the verses differ")
                    for number, cells in data_verses.items():
                        self.verses.append(
                            _Verse((book, chapter, number), mam_verses[number], cells)
                        )
        self._resolved = {}

    def resolved_mam_e(self, verse):
        """MAM-parsed-plus's E cell of ``verse`` as phase 2 resolves it."""
        if verse.ref not in self._resolved:
            self._resolved[verse.ref] = phase2.Resolver().resolve_e_cell(
                copy.deepcopy(verse.mam[_E]), verse.ref
            )
        return self._resolved[verse.ref]


def _with_mam_names(value, verse):
    """A deep copy of the dataset's ``value`` with each renamed note given MAM's name.

    The walk is phase6_rename.py's: a note's target, every parameter of a ketiv/qere
    template but a flag, and nothing else. A note has MAM_TARGET_PARAMETER exactly
    where it has one of RENAMED_NOTES's names, or this raises.
    """
    value = copy.deepcopy(value)
    _rename_back(value, verse)
    return value


def _rename_back(value, verse):
    if isinstance(value, str):
        return
    if isinstance(value, list):
        for item in value:
            _rename_back(item, verse)
        return
    name = value["tmpl_name"]
    params = value.get("tmpl_params", {})
    mam_name = _MAM_NAMES.get(name, name)
    rule = phase2._RULES.get(mam_name)
    if rule is None:
        raise AssertionError(f"{verse}: {name!r}, which phase 2 has no rule for")
    if rule.action == phase2._KEEP_NOTE:
        if (name != mam_name) != (MAM_TARGET_PARAMETER in params):
            raise AssertionError(
                f"{verse}: note {name!r} has MAM's target where it is not renamed, or "
                "lacks it where it is"
            )
        value["tmpl_name"] = mam_name
        _rename_back(params[_TARGET], verse)
    elif rule.action == phase2._KEEP_KQ:
        for key, item in params.items():
            if key not in _FLAGS:
                _rename_back(item, verse)
    elif rule.action not in (phase2._VERBATIM, phase2._COLLAPSE_WORD, phase2._CARRIERS):
        raise AssertionError(f"{verse}: {name!r}, which phase 2 does not keep")


def _walk(value, verse, side, visit, path=(), zone=_TEXT):
    """Call ``visit(zone, path, item)`` for each string and template of ``value``.

    ``value`` is an E cell of ``side``, the dataset or MAM-parsed-plus, or part of one.
    The walk dispatches on phase 2's rule table, a renamed note by MAM's name for it.
    Each parameter it enters is of the zone it is in, or of a zone the parameter opens:
    a note's parameter other than its target is a note body, MAM_TARGET_PARAMETER a
    copy of MAM's target, and a flag a flag value. A note body and a flag value are
    read with phase 3's _clauses and visited as clause strings; a copy of MAM's target
    is walked as MAM's text, in its own zone. A template phase 2 has no rule for
    raises, and so does one that phase 2 removes, met in the dataset's own text.
    """
    if isinstance(value, str):
        visit(zone, path, value)
        return
    if isinstance(value, list):
        for item in value:
            _walk(item, verse, side, visit, path, zone)
        return
    visit(zone, path, value)
    name = value["tmpl_name"]
    params = value.get("tmpl_params", {})
    mam_name = _MAM_NAMES.get(name, name) if side == _DATASET else name
    rule = phase2._RULES.get(mam_name)
    if rule is None:
        raise AssertionError(
            f"{verse}: {name!r} at {path}, which phase 2 has no rule for"
        )
    keys = frozenset(params)
    in_dataset_text = side == _DATASET and zone == _TEXT

    def enter(key, item, sub_zone=None, sub_side=None):
        _walk(
            item,
            verse,
            sub_side or side,
            visit,
            path + (f"{name}/{key}",),
            sub_zone if zone == _TEXT and sub_zone else zone,
        )

    def read(key, item, sub_zone):
        for clause in phase3._clauses(item, verse):
            visit(
                sub_zone if zone == _TEXT else zone, path + (f"{name}/{key}",), clause
            )

    if rule.action == phase2._KEEP_NOTE:
        added = keys & ({MAM_TARGET_PARAMETER} | _FLAGS)
        if side == _MAM and added:
            raise AssertionError(f"{verse}: MAM's {name!r} has {sorted(added)}")
        renamed_right = (name != mam_name) == (MAM_TARGET_PARAMETER in keys)
        if (
            keys - added not in rule.keysets
            or len(added & _FLAGS) > 1
            or (in_dataset_text and not renamed_right)
        ):
            raise AssertionError(
                f"{verse}: note {name!r} has parameters {sorted(keys)}"
            )
        for key, item in params.items():
            if key == _TARGET:
                enter(key, item)
            elif key == MAM_TARGET_PARAMETER:
                enter(key, item, _MAM_TARGET, _MAM)
            elif key in _FLAGS:
                read(key, item, _FLAG_VALUE)
            else:
                read(key, item, _NOTE_BODY)
    elif rule.action == phase2._KEEP_KQ:
        phase2.selected_keys(value, verse)  # raises on an unexpected parameter set
        for key, item in params.items():
            if key in _FLAGS:
                read(key, item, _FLAG_VALUE)
            else:
                enter(key, item)
    elif rule.action in (phase2._DISSOLVE, phase2._MARK, phase2._VERBATIM):
        if in_dataset_text and rule.action != phase2._VERBATIM:
            raise AssertionError(f"{verse}: {name!r}, which phase 2 removes, at {path}")
        if keys not in rule.keysets:
            raise AssertionError(f"{verse}: {name!r} has parameters {sorted(keys)}")
        for key, item in params.items():
            enter(key, item)
    elif rule.action == phase2._COLLAPSE_WORD:
        if keys not in rule.keysets:
            raise AssertionError(f"{verse}: {name!r} has parameters {sorted(keys)}")
        for key, item in params.items():
            if key == "1":
                _special_letter_word_1(
                    item, verse, side, visit, path + (f"{name}/1",), zone
                )
            elif isinstance(item, str):
                visit(zone, path + (f"{name}/{key}",), item)
            else:
                raise AssertionError(f"{verse}: {name!r}'s parameter {key} is not text")
    elif rule.action == phase2._CARRIERS:
        if side != _DATASET:
            raise AssertionError(f"{verse}: {name!r} in MAM's text")
        phase2.carriers_text(
            value, verse
        )  # raises unless it has the near-Aleppo dataset's rule-8 shape
        enter("1", params["1"])
    else:
        raise AssertionError(f"{verse}: no walk for phase 2's action {rule.action!r}")


def _special_letter_word_1(value, verse, side, visit, path, zone):
    """A special-letter word's parameter 1: text, the templates of _SPECIAL_LETTERS,
    and any other template by phase 2's rule table, as _walk dispatches it."""
    for item in value if isinstance(value, list) else [value]:
        if isinstance(item, str):
            visit(zone, path, item)
            continue
        if item["tmpl_name"] not in _SPECIAL_LETTERS:
            _walk(item, verse, side, visit, path, zone)
            continue
        params = item.get("tmpl_params", {})
        if set(params) != {"1"} or not isinstance(params["1"], str):
            raise AssertionError(
                f"{verse}: {item['tmpl_name']!r} in a special-letter word"
            )
        visit(zone, path, item)
        visit(zone, path + (f"{item['tmpl_name']}/1",), params["1"])


def _templates(value, verse, side, zone=_TEXT):
    """(path, template) for each template of ``value`` that a walk meets in ``zone``."""
    found = []

    def visit(where, path, item):
        if where == zone and isinstance(item, dict):
            found.append((path, item))

    _walk(value, verse, side, visit)
    return found


def _mam_name(tmpl):
    """A template's name as phase 2's rule table knows it: MAM's, for a renamed note."""
    return _MAM_NAMES.get(tmpl["tmpl_name"], tmpl["tmpl_name"])


def _selected_text(verse):
    """The dataset's E cell of ``verse`` along its selected parameters."""
    return phase3._selected_text(_with_mam_names(verse.data[_E], verse.ref), verse.ref)


def _mam_selected_text(corpus, verse):
    """MAM-parsed-plus's E cell of ``verse``, as phase 2 resolves it, along its selected
    parameters."""
    return phase3._selected_text(corpus.resolved_mam_e(verse), verse.ref)


def _cells(corpus):
    """The book files, the verses, and the verses whose cells differ from
    MAM-parsed-plus's, compared as JSON values."""
    differing = Counter()
    for verse in corpus.verses:
        for label, column in (("c", _C), ("d", _D), ("e", _E)):
            if verse.mam[column] != verse.data[column]:
                differing[label] += 1
    return {
        "dataset_files": corpus.files,
        "verses": len(corpus.verses),
        "c_cells_changed": differing["c"],
        "d_cells_changed": differing["d"],
        "e_cells_changed": differing["e"],
    }


class _CodexIndex:
    """The codex index's leaves, each a range of verses including both its ends."""

    def __init__(self):
        data = json.loads(build_paths.aleppo_index().read_text(encoding="utf-8"))
        self.rank = {name: i for i, name in enumerate(data["header"]["books"])}
        unknown = set(self.rank) - set(_INDEX_BOOK.values())
        if unknown:
            raise AssertionError(
                f"the codex index names books _INDEX_BOOK lacks: {unknown}"
            )
        self.intervals = []
        for row in data["body"]:
            if not row.get("de_text_range"):
                continue
            (b0, c0, v0), (b1, c1, v1) = row["de_text_range"]
            start = (self.rank[b0], int(c0), int(v0))
            end = (self.rank[b1], int(c1), int(v1))
            if start > end:
                raise AssertionError(f"leaf {row['de_leaf']}'s range runs backwards")
            self.intervals.append((start, end))

    def extant(self, ref):
        """Whether a leaf of the codex covers the verse ``ref``, as the build names it."""
        book, chapter, verse = ref
        name = _INDEX_BOOK[book]
        if name not in self.rank:
            return False
        key = (self.rank[name], int(chapter), int(verse))
        return any(start <= key <= end for start, end in self.intervals)


def _survival(corpus, index):
    """Where a leaf of the codex survives: the verses, the books lost entire and in
    part, and each partly lost book's lost verses as runs, first to last."""
    by_book = {}
    for verse in corpus.verses:
        by_book.setdefault(verse.ref[0], []).append(
            (verse.ref, index.extant(verse.ref))
        )
    lost_entire, partly = [], []
    for book, rows in by_book.items():
        lost = sum(1 for _, alive in rows if not alive)
        if lost == len(rows):
            lost_entire.append(book)
        elif lost:
            runs, current = [], None
            for ref, alive in rows:
                if alive:
                    current = None
                elif current is None:
                    current = [ref, ref]
                    runs.append(current)
                else:
                    current[1] = ref
            partly.append(
                {"book": book, "lost": lost, "runs": [tuple(r) for r in runs]}
            )
    extant = sum(1 for verse in corpus.verses if index.extant(verse.ref))
    decalogues_lost = all(
        not index.extant(verse.ref)
        for verse in corpus.verses
        if verse.ref[:2] in _DECALOGUES_AND_GENESIS_35
    )
    return {
        "extant_verses": extant,
        "lost_verses": len(corpus.verses) - extant,
        "books_lost_entire": lost_entire,
        "books_partly_lost": partly,
        "decalogues_and_genesis_35_lost": decalogues_lost,
    }


class _Clause(NamedTuple):
    """A direct differing clause of a note, as phase 5 classifies it."""

    site: object
    sigla: tuple


def _direct_clauses(note, number, verse):
    """Each direct differing clause of the נוסח ``note``, note ``number`` of ``verse``.

    This repeats the reading of phase5_readings.Readings._note, which classifies and
    applies in one pass and so cannot be asked of the dataset: a clause differs where
    it has a head before its "="; a prose head is not direct, whether or not it ends
    in a siglum of the codex; a head naming שיטת-א is not direct either, and one that
    also cites the codex raises, as in the build; any other head with sigla of the
    codex, as phase 3's _qualified_codex_sigla reads them, is direct, and phase 5's
    _classified classifies it. _testimony checks the totals against phase 5's.
    """
    found = []
    position = 0
    for text in phase3._clauses(note["tmpl_params"][_BODY], verse):
        if not text:
            continue
        position += 1
        head, equals, rest = text.partition("=")
        if not equals or not head:
            continue
        stripped = head.strip()
        prose = phase3._first_space_outside_brackets(stripped) < len(stripped)
        codex_led = (
            prose
            and stripped.split()[-1].rstrip("!?") in phase3._STRESS_HELPER_CODEX_SIGLA
        )
        sigla = () if prose else tuple(phase3._qualified_codex_sigla(head))
        if phase5._SHITAT_ALEF in head:
            if codex_led or sigla:
                raise AssertionError(f"{verse}: a שיטת-א head that cites the codex too")
            continue
        if codex_led or not sigla:
            continue
        site = phase5.Site(number, position)
        phase5._classified(site, sigla, rest, verse)  # raises where phase 5 would
        found.append(_Clause(site, sigla))
    return found


def _testimony(corpus, index, snapshot):
    """The citations of testimony to the codex's lost parts, and of the photographs of
    its pages, in the direct differing clauses of MAM's notes, and the clauses citing
    them, all at verses where the codex is lost.

    The census's "differ codex-testimony 44" counts such citations, a head's
    א(ע,ק,ר) being three, not clauses. The totals of every direct differing clause are
    checked against phase 5's, which the build asserts.
    """
    totals = {"elements": 0, "clauses": 0, "verses": set()}
    citations = clauses = 0
    for verse in corpus.verses:
        cell = _with_mam_names(verse.data[_E], verse.ref)
        for number, note in enumerate(phase5.notes(cell, verse.ref), 1):
            for clause in _direct_clauses(note, number, verse.ref):
                totals["elements"] += len(clause.sigla)
                totals["clauses"] += 1
                totals["verses"].add(verse.ref)
                cited = sum(
                    1
                    for siglum, _ in clause.sigla
                    if siglum in _TESTIMONY or siglum == _PHOTOGRAPH
                )
                if not cited:
                    continue
                if index.extant(verse.ref):
                    raise AssertionError(
                        f"{verse.ref}: testimony to the codex where it survives; the "
                        "page says there is none"
                    )
                citations += cited
                clauses += 1
    totals["verses"] = len(totals["verses"])
    for label, key in _PHASE5_TOTALS.items():
        if totals[label] != snapshot["phase5_counts"][key]:
            raise AssertionError(
                f"_direct_clauses gives {totals[label]} for {key!r}, and the build "
                f"{snapshot['phase5_counts'][key]}: phase 5's reading has changed"
            )
    return {
        "testimony_citations_at_lost_verses": citations,
        "testimony_clauses_at_lost_verses": clauses,
    }


def _hataf_heads(target, body, verse):
    """For each varika of a note's target, the heads of the note's clauses whose forms
    give it a vowel, as phase 3's Policies._hataf_decisions reads them, which that
    method does not return; the sigla of any agreeing clause that gives it instead; and
    the vowels given."""
    text = phase3._selected_text(target, verse)
    letters = phase3._letters_and_marks(text)
    spelling = "".join(letter for letter, _ in letters).translate(phase3._NON_FINAL)
    places = [
        ("".join(text[index] for index, _ in atom), position)
        for atom in phase3._atoms(text)
        for position in range(len(atom))
    ]
    quoting, _ = phase3._hataf_forms(body, verse)
    result = []
    for index, (_, marks) in enumerate(letters):
        if _VARIKA not in marks:
            continue
        site = (places[index], spelling, index)
        by_clause = [
            (head, phase3._vowels_given(forms, *site)) for head, forms in quoting
        ]
        heads = [head for head, pairs in by_clause if pairs]
        vowels = {vowel for _, pairs in by_clause for vowel, _ in pairs}
        agreeing = []
        if not heads and verse in phase3._HATAF_FROM_AGREEING_VERSES:
            for clause in phase3._clauses(body, verse):
                if not clause.startswith("="):
                    continue
                given = phase3._vowels_given(phase3._ANGLE_RUN.findall(clause), *site)
                if given:
                    agreeing.append(phase3._clause_sigla(clause))
                    vowels |= {vowel for vowel, _ in given}
        result.append({"heads": heads, "agreeing": agreeing, "vowels": vowels})
    return result


def _varika(corpus):
    """The notes whose target, in MAM-parsed-plus, holds a varika, and those that give
    the hataf's vowel under no siglum beginning with א, the sigla read by phase 3's
    _head_sigla. The vowels read here are checked against the build's own decisions."""
    policies = phase3.Policies()
    notes = without_alef = 0
    for verse in corpus.verses:
        if _VARIKA not in json.dumps(verse.mam[_E], ensure_ascii=False):
            continue
        for note in phase5.notes(corpus.resolved_mam_e(verse), verse.ref):
            target, body = note["tmpl_params"][_TARGET], note["tmpl_params"][_BODY]
            if _VARIKA not in phase3._selected_text(target, verse.ref):
                continue
            varikas = _hataf_heads(target, body, verse.ref)
            decisions = policies._hataf_decisions(target, body, verse.ref)
            if [decision[1] for decision in decisions] != [
                next(iter(v["vowels"])) if len(v["vowels"]) == 1 else None
                for v in varikas
            ] and verse.ref not in phase3._HATAF_FROM_LENINGRAD_VERSES:
                raise AssertionError(
                    f"{verse.ref}: the heads' vowels are not the build's"
                )
            sigla = [
                s for v in varikas for h in v["heads"] for s in phase3._head_sigla(h)
            ]
            sigla += [s for v in varikas for group in v["agreeing"] for s in group]
            notes += 1
            if not any(siglum.startswith("א") for siglum in sigla):
                without_alef += 1
    return {"varika_notes": notes, "varika_notes_without_codex_siglum": without_alef}


def _kept_marks(corpus, snapshot):
    """The rafe, holam haser for vav and deḥi of MAM's text and of the dataset's.

    The page says that the dataset keeps every one of MAM's and has others only where
    phase 5 writes a reading of the codex, and that MAM's deḥi is the poetic deḥi; each
    is checked verse by verse.
    """
    writes = {
        tuple(site) for key in _PHASE5_WRITES for site in snapshot["phase5_sites"][key]
    }
    mam, data = Counter(), Counter()
    for verse in corpus.verses:
        data_text = _selected_text(verse)
        mam_text = _mam_selected_text(corpus, verse)
        for label, mark in _KEPT_MARKS.items():
            m, d = mam_text.count(mark), data_text.count(mark)
            if d < m:
                raise AssertionError(
                    f"{verse.ref}: the dataset lacks one of MAM's {label}"
                )
            if d > m and verse.ref not in writes:
                raise AssertionError(
                    f"{verse.ref}: the dataset has a {label} that no reading of phase 5 "
                    "brings"
                )
            if label == "deḥi" and m and not phase3._is_poetic(verse.ref):
                raise AssertionError(f"{verse.ref}: MAM has U+05AD in a prose verse")
            mam[label] += m
            data[label] += d
    out = {}
    for label in _KEPT_MARKS:
        out[f"{label}_mam"] = mam[label]
        out[label] = data[label]
    return out


def _dots(corpus):
    """The atoms of the dataset's selected text with an extraordinary dot, U+05C4
    HEBREW MARK UPPER DOT or U+05C5 HEBREW MARK LOWER DOT, atoms as phase 3's _atoms
    finds them."""
    atoms, verses = 0, set()
    for verse in corpus.verses:
        text = _selected_text(verse)
        for atom in phase3._atoms(text):
            marks = {text[i] for _, indices in atom for i in indices}
            if marks & {_UPPER_DOT, _LOWER_DOT}:
                atoms += 1
                verses.add(verse.ref)
    return {"dots_atoms": atoms, "dots_verses": len(verses)}


def _pointed_ketiv(corpus):
    """The ketiv/qere templates of the families that can have the pointed ketiv, in the
    dataset's own text: those with it, by family, and the verses they are in; and those
    without it, whose text follows MAM's pointed qere."""
    families, verses = Counter(), set()
    without = 0
    for verse in corpus.verses:
        for _, tmpl in _templates(verse.data[_E], verse.ref, _DATASET):
            name = tmpl["tmpl_name"]
            if name not in phase2.POINTED_KETIV_FAMILIES:
                continue
            if phase2.POINTED_KETIV_PARAMETER in tmpl["tmpl_params"]:
                families[name] += 1
                verses.add(verse.ref)
            else:
                without += 1
    return {
        "pointed_ketiv_by_family": dict(families),
        "pointed_ketiv_templates": sum(families.values()),
        "inferred_pointed_ketiv_templates": len(frozen_ketiv.load()["records"]),
        "editorial_pointed_ketiv_templates": len(editorial_ketiv.load()["records"]),
        "reviewed_pointed_ketiv_templates": len(reviewed_ketiv.load()["records"]),
        "note_pointed_ketiv_templates": sum(families.values())
        - len(frozen_ketiv.load()["records"])
        - len(editorial_ketiv.load()["records"])
        - len(reviewed_ketiv.load()["records"]),
        "pointed_ketiv_verses": len(verses),
        "kq_without_pointed_ketiv": without,
    }


def _rule8(corpus):
    """The verses of each of the near-Aleppo dataset's two rule-8 templates.

    The walk finds phase2.MARKS_WITHOUT_LETTER wherever it is; phase 2 has no rule for
    the other, which no site uses, and the walk would raise on it. A count of each name
    in the book files' serialized text, every zone and column included, checks that
    the walk saw every occurrence.
    """
    names = (phase2.MARKS_WITHOUT_LETTER, consumer_notice.MARKS_WITHOUT_LETTER_OR_SPACE)
    sites = {name: [] for name in names}
    for verse in corpus.verses:
        for _, tmpl in _templates(verse.data[_E], verse.ref, _DATASET):
            if tmpl["tmpl_name"] in names:
                sites[tmpl["tmpl_name"]].append(verse.ref)
    serialized = Counter()
    for path in sorted(build_paths.dataset_dir().glob("*.json")):
        text = path.read_text(encoding="utf-8")
        for name in names:
            serialized[name] += text.count(
                json.dumps({"tmpl_name": name}, ensure_ascii=False)[1:-1]
            )
    for name in names:
        if serialized[name] != len(sites[name]):
            raise AssertionError(f"{name!r} is in the files where the walk misses it")
    return {"rule8_sites": sites}


def _characters(cell, verse, side):
    """{zone: {character: [(path, count)]}} for the strings of ``cell``."""
    found = {}

    def visit(zone, path, item):
        if isinstance(item, str):
            for char, count in Counter(item).items():
                found.setdefault(zone, {}).setdefault(char, []).append((path, count))

    _walk(cell, verse, side, visit)
    return found


def _new_characters(corpus):
    """The characters of the dataset's own text that MAM-parsed-plus's text lacks, with
    the verses the dataset has each at, and the zones MAM-parsed-plus has it in.

    The dataset's own text is its E cells less the note bodies, the copies of MAM's
    target and the flag values; MAM's text is its E cells less the note bodies. The C
    and D cells, the same on both sides, are left out.
    """
    data_chars, mam_chars = {}, set()
    mam_zones = {}
    for verse in corpus.verses:
        for char, places in (
            _characters(verse.data[_E], verse.ref, _DATASET).get(_TEXT, {}).items()
        ):
            data_chars.setdefault(char, []).extend([verse.ref] * len(places))
        for zone, chars in _characters(verse.mam[_E], verse.ref, _MAM).items():
            for char in chars:
                mam_zones.setdefault(char, set()).add(zone)
                if zone == _TEXT:
                    mam_chars.add(char)
    return {
        "new_characters": [
            {
                "code_point": f"U+{ord(char):04X}",
                "name": unicodedata.name(char),
                "verses": data_chars[char],
                "mam_zones": sorted(mam_zones.get(char, ())),
            }
            for char in sorted(set(data_chars) - mam_chars)
        ]
    }


def _ketiv_qere_in(value, verse):
    """The ketiv/qere templates a walk meets in the dataset's text of ``value``."""
    return [
        tmpl
        for _, tmpl in _templates(value, verse, _DATASET)
        if tmpl["tmpl_name"] not in _SPECIAL_LETTERS
        and phase2._RULES[_mam_name(tmpl)].action == phase2._KEEP_KQ
    ]


def _silence(corpus):
    """The sites flagged flagged-not-applied with one of phase6_flags.py's two fixed
    values, found in the dataset: each with its verse, the family of its ketiv/qere
    template and the value. Each is matched to a row of phase6_flags._SILENCE_SITES."""
    values = (phase6_flags._QERE_SILENCE, phase6_flags._MAQAF_SILENCE)
    sites = []
    for verse in corpus.verses:
        for _, tmpl in _templates(verse.data[_E], verse.ref, _DATASET):
            value = tmpl.get("tmpl_params", {}).get(phase2.FLAGGED_NOT_APPLIED)
            if not isinstance(value, str) or value not in values:
                continue
            action = phase2._RULES[_mam_name(tmpl)].action
            if action == phase2._KEEP_KQ:
                placement, held = phase6_flags._TEMPLATE_PLACEMENT, [tmpl]
            elif action == phase2._KEEP_NOTE:
                placement = phase6_flags._NOTE_PLACEMENT
                held = _ketiv_qere_in(tmpl["tmpl_params"][_TARGET], verse.ref)
            else:
                raise AssertionError(f"{verse.ref}: a flag on {tmpl['tmpl_name']!r}")
            if len(held) != 1:
                raise AssertionError(
                    f"{verse.ref}: a silence flag over {len(held)} templates"
                )
            sites.append(
                {
                    "verse": verse.ref,
                    "family": held[0]["tmpl_name"],
                    "value": value,
                    "placement": placement,
                    "params": held[0]["tmpl_params"],
                }
            )
    rows = list(phase6_flags._SILENCE_SITES)
    for site in sites:
        matches = [
            row
            for row in rows
            if row[0] == site["verse"]
            and row[1] == site["family"]
            and site["params"].get(row[2]) == row[3]
            and row[4] == site["placement"]
        ]
        if len(matches) != 1:
            raise AssertionError(
                f"{site['verse']}: a silence flag the build's table lacks"
            )
        rows.remove(matches[0])
    if rows:
        raise AssertionError(f"silence sites of the build's table not found: {rows}")
    return {
        "silence_sites": [
            {"verse": s["verse"], "family": s["family"], "value": s["value"]}
            for s in sites
        ]
    }


def _inverted_nuns(corpus):
    """The template מ:נו״ן הפוכה in the dataset's own text."""
    count = 0
    for verse in corpus.verses:
        for _, tmpl in _templates(verse.data[_E], verse.ref, _DATASET):
            if tmpl["tmpl_name"] == _INVERTED_NUN:
                count += 1
    return {"inverted_nuns": count}


def _absent_in_copies(corpus):
    """The templates of phase2.TEMPLATES_ABSENT_FROM_DATASET that the copies of MAM's
    target hold, in the order of that tuple."""
    found = set()
    for verse in corpus.verses:
        for _, tmpl in _templates(verse.data[_E], verse.ref, _DATASET, _MAM_TARGET):
            found.add(tmpl["tmpl_name"])
    return {
        "absent_in_copies": [
            name for name in phase2.TEMPLATES_ABSENT_FROM_DATASET if name in found
        ]
    }
