"""Add near-Aleppo's two evidence flags as template parameters.

The public build guide is ``doc/near-aleppo-build.md``. A flag is the last parameter of the note or ketiv/qere template it
concerns. ``flagged-not-applied`` marks a doubtful codex reading the dataset does
not take, a named site where MAM's apparatus is silent about the codex, or the one
codex reading that its note itself outweighs, Numbers 22:5's.
``applied-and-flagged`` marks a manifestly erroneous, bang-marked codex reading
that the dataset nevertheless reproduces. A clause-backed value is copied from
the note body, with its structure intact. A site with no such clause gets one of
the two fixed explanations below.

The doubt rule covers every differing clause whose codex siglum carries ``?``,
and every unqualified codex clause whose first quoted form ends in ``?``. A
reading already present in the target is not flagged; this excludes Deuteronomy
5:23. The question and answer at Leviticus 10:4 is not a doubt mark. Proverbs
19:26 is named separately because a built policy rests on its doubtful agreeing
clause. The bang rule covers differing clauses only when their reading is already
in the target, plus the three agreeing clauses named below. Whether a reading is in
the target is phase5_readings.in_place, the one in-place test, which phase 5 uses
to decide what it applies. It compares a clause's forms with the side of the target
that phase5_readings.reading_side names: the ketiv side for a clause headed א-כתיב,
and for a reading under a plain א that phase 5 writes as a pointed ketiv; the qere
side for a clause headed א-קרי; and the selected text for every other clause. So a
doubt-marked clause headed א-כתיב is compared with the consonantal ketiv and is never
in place, and stays flagged. Phase 5 applies the bang-marked codex readings that were
not in place, so
this rule flags them, with no further table; the two headed א-כתיב! are written as
their template's pointed ketiv. Numbers 22:5's א(ר) reading, which phase 5 does not
apply because its note prefers the conflicting explicit testimony, is
flagged by a separate rule, which takes its site from
phase5_readings.NOT_APPLIED_READINGS.

The step runs after MAM's-target copying. It adds parameters only, changes no
text, and never puts a flag inside a note's target.
"""

import copy
from collections import Counter
from collections import defaultdict

from mb_cmn import template_names
from near_aleppo import phase2_templates as phase2
from near_aleppo import phase3_policies as phase3
from near_aleppo import phase5_readings as phase5
from near_aleppo.phase6_mam_targets import MAM_TARGET_PARAMETER

# The flags' names are phase 2's, whose selected_keys tells a flag from a parameter
# nothing adds.
APPLIED_AND_FLAGGED = phase2.APPLIED_AND_FLAGGED
FLAGGED_NOT_APPLIED = phase2.FLAGGED_NOT_APPLIED

# ``census/nusach_aleppo_readings.py`` is the census authority for the qualified
# clause populations, and MAM-private's near-Aleppo research has the authority for
# the unqualified clauses whose quoted form ends in a question mark. The build
# records both their counts and their exact verse sites in
# in/near-aleppo/build-populations.json, pinning neither.

_QERE_SILENCE = "MAM's apparatus does not say whether the codex has a qere note here"
_MAQAF_SILENCE = "MAM's apparatus does not say whether the codex has the maqaf here"

_NOTE = "נוסח"
_TARGET = "1"
_BODY = "2"
# The clause separator that joins two copied clauses, written as MAM has each of
# its ש, with no tmpl_params key; until 2026-09-25 it had an empty one, which MAM
# never writes.
_SEPARATOR = {"tmpl_name": "ש"}

_DOUBT_SIGLUM = "qualification 2: doubt-marked clauses by codex siglum"
_DOUBT_FORM = "qualification 2: doubt-marked clauses by quoted form"
_DOUBT_IN_PLACE = "qualification 2: clauses whose reading is already in the target"
_QUALIFICATION_NOTES = "qualification 2: notes flagged"
_QUALIFICATION_CLAUSES = "qualification 2: clauses flagged"
_NAMED_DOUBT = "named doubtful agreeing clause"
_SILENT_APPARATUS = "named apparatus-silence sites"
_BANG_DIFFERING = "qualification 3: differing clauses already applied"
_BANG_AGREEING = "qualification 3: named agreeing clauses"
_NOT_APPLIED_READING = "named codex reading phase 5 does not apply"

# Each silence site is (verse, template family, identifying parameter and value,
# placement). ``note`` puts the flag on the enclosing note; ``template`` puts it
# on the ketiv/qere template itself. The table has the 10 מ:קו״כ-אם-2 sites left
# after Ezekiel 40:26 joined the ketiv/qere apparatus on 2026-09-18, and Joshua 3:4
# and Ezekiel 40:24's second site on 2026-09-24, their notes giving the codex's
# masorah note there, which is not a qere note; plus Deuteronomy 29:22 and
# 2 Samuel 13:33.
_NOTE_PLACEMENT = "note"
_TEMPLATE_PLACEMENT = "template"
_SILENCE_SITES = (
    (
        ('BA-Samuel שמ"ב', "11", "24"),
        "מ:קו״כ-אם-2",
        "2",
        "ויראו",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ('BA-Samuel שמ"ב', "11", "24"),
        "מ:קו״כ-אם-2",
        "2",
        "המוראים",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ('BC-Kings מל"ב', "14", "12"),
        "מ:קו״כ-אם-2",
        "2",
        "לאהלו",
        _TEMPLATE_PLACEMENT,
    ),
    (("C2-Jeremiah", "2", "3"), "מ:קו״כ-אם-2", "2", "תבואתה", _NOTE_PLACEMENT),
    (
        ("C2-Jeremiah", "32", "35"),
        "מ:קו״כ-אם-2",
        "2",
        "החטי",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ("C2-Jeremiah", "51", "9"),
        "מ:קו״כ-אם-2",
        "2",
        "רפאנו",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ("C3-Ezekiel", "40", "37"),
        "מ:קו״כ-אם-2",
        "2",
        "מעלו",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ("C3-Ezekiel", "47", "8"),
        "מ:קו״כ-אם-2",
        "2",
        "ונרפאו",
        _TEMPLATE_PLACEMENT,
    ),
    (
        ("C3-Ezekiel", "48", "18"),
        "מ:קו״כ-אם-2",
        "2",
        "תבואתה",
        _NOTE_PLACEMENT,
    ),
    (
        ("C3-Ezekiel", "48", "21"),
        "מ:קו״כ-אם-2",
        "2",
        "בתוכה",
        _TEMPLATE_PLACEMENT,
    ),
    (("A5-Deuter", "29", "22"), "כו״ק", "2", "וּצְבוֹיִ֔ם", _NOTE_PLACEMENT),
    (
        ('BA-Samuel שמ"ב', "13", "33"),
        "כתיב ולא קרי",
        "1",
        "(אם)־",
        _TEMPLATE_PLACEMENT,
    ),
)

_NAMED_DOUBT_VERSES = (("D2-Proverbs", "19", "26"),)
_AGREEING_BANG_VERSES = (
    ('BA-Samuel שמ"א', "23", "17"),
    ("D1-Psalms", "25", "21"),
    ("D1-Psalms", "35", "14"),
)
# Each verse these two tables name must have exactly one note to which its rule
# applies, as each silence site must be found once.
_NAMED_TABLES = {
    _NAMED_DOUBT: _NAMED_DOUBT_VERSES,
    _BANG_AGREEING: _AGREEING_BANG_VERSES,
}


class Flags:
    """Add flags verse by verse and record every population."""

    def __init__(self):
        self.counts = Counter()
        self.sites = defaultdict(list)
        self._silence_found = Counter()
        # How many notes each rule of _NAMED_TABLES applied to, by (rule, verse).
        self._named_found = Counter()
        # Each נוסח of the current verse by its identity, with its position among the
        # verse's notes as phase 5 numbers them, which the in-place test takes.
        self._note_numbers = {}

    def add_to_e_cell(self, cell, verse, *, evidence_cell=None):
        """Add flags using note-reading evidence before any frozen branch is added.

        The new selected branch must not reclassify an already-applied qere note.
        Only the in-place comparison uses the optional post-Readings evidence;
        flags and their other guards still apply to the actual output templates.
        """
        actual_notes = phase5.notes(cell, verse)
        self._note_numbers = {
            id(note): number for number, note in enumerate(actual_notes, 1)
        }
        self._evidence_targets = {}
        if evidence_cell is not None:
            for note, evidence in zip(
                actual_notes, phase5.notes(evidence_cell, verse), strict=True
            ):
                if (
                    note["tmpl_name"] != evidence["tmpl_name"]
                    or note["tmpl_params"][_BODY] != evidence["tmpl_params"][_BODY]
                ):
                    raise AssertionError(
                        f"{verse}: note identity changed before flagging"
                    )
                self._evidence_targets[id(note)] = evidence["tmpl_params"][_TARGET]
        self._walk(cell, verse, note_depth=0)
        for site in _SILENCE_SITES:
            if site[0] == verse and self._silence_found[site] != 1:
                raise AssertionError(
                    f"{verse}: silence table site {site[1:4]} was found "
                    f"{self._silence_found[site]} times, not 1"
                )
        for label, verses in _NAMED_TABLES.items():
            if verse in verses and self._named_found[label, verse] != 1:
                raise AssertionError(
                    f"{verse}: the {label!r} rule applied to "
                    f"{self._named_found[label, verse]} notes, not 1"
                )
        return cell

    def _walk(self, value, verse, note_depth):
        if isinstance(value, str):
            return
        if isinstance(value, list):
            for item in value:
                self._walk(item, verse, note_depth)
            return
        name = value["tmpl_name"]
        rule = phase2._RULES.get(name)
        if rule is None:
            raise AssertionError(
                f"{verse}: flags met {name!r}, which phase 2 has no rule for"
            )
        params = value.get("tmpl_params", {})
        if rule.action == phase2._KEEP_NOTE:
            flags = self._note_flags(value, verse)
            if flags and note_depth:
                raise AssertionError(f"{verse}: a flagged note is inside a note target")
            self._add_flags(value, flags, verse)
            self._walk(params[_TARGET], verse, note_depth + 1)
        elif rule.action == phase2._KEEP_KQ:
            flags = self._template_silence_flags(value, verse, note_depth)
            self._add_flags(value, flags, verse)
            for key, item in list(params.items()):
                if key not in (APPLIED_AND_FLAGGED, FLAGGED_NOT_APPLIED):
                    self._walk(item, verse, note_depth)
        elif rule.action == phase2._DISSOLVE:
            self._walk(params[rule.keys[0]], verse, note_depth)

    def _note_flags(self, note, verse):
        params = note["tmpl_params"]
        if note["tmpl_name"] != _NOTE:
            return {}
        number = self._note_numbers.get(id(note))
        if number is None:
            raise AssertionError(
                f"{verse}: the flags step met a נוסח that phase 5's walk does not"
            )
        clauses = _clauses_with_values(params[_BODY], verse)
        doubt_values = []
        bang_values = []
        # Each clause's 1-based position among the note's non-empty clauses, which is
        # how phase 5 numbers them.
        position = 0
        for clause, value in clauses:
            if clause:
                position += 1
            head, equals, rest = clause.partition("=")
            if not equals or not head:
                continue
            sigla = _qualified_codex_sigla(head)
            if not sigla:
                continue
            forms = phase3._quoted_forms(rest)
            side = phase5.reading_side(sigla, verse, phase5.Site(number, position))
            in_place = any(
                phase5.in_place(
                    form,
                    self._evidence_targets.get(id(note), params[_TARGET]),
                    verse,
                    number,
                    side,
                )
                for form in forms
            )
            doubt_kind = None
            if any("?" in qualifier for _, qualifier in sigla):
                doubt_kind = _DOUBT_SIGLUM
            elif (
                all(not qualifier for _, qualifier in sigla)
                and forms
                and forms[0].endswith("?")
            ):
                doubt_kind = _DOUBT_FORM
            if doubt_kind is not None:
                self._found(doubt_kind, verse)
                if in_place:
                    self._found(_DOUBT_IN_PLACE, verse)
                else:
                    doubt_values.append(value)
                continue
            if any(qualifier == "!" for _, qualifier in sigla) and in_place:
                bang_values.append(value)

        flags = {}
        if doubt_values:
            self._found(_QUALIFICATION_NOTES, verse)
            self._found(_QUALIFICATION_CLAUSES, verse, len(doubt_values))
            flags[FLAGGED_NOT_APPLIED] = _joined_clauses(doubt_values)
        if bang_values:
            self._found(_BANG_DIFFERING, verse, len(bang_values))
            flags[APPLIED_AND_FLAGGED] = _joined_clauses(bang_values)

        if verse in _NAMED_DOUBT_VERSES:
            value = _one_agreeing_clause(clauses, verse, "?")
            self._found(_NAMED_DOUBT, verse)
            self._named_found[_NAMED_DOUBT, verse] += 1
            _merge_flag(flags, FLAGGED_NOT_APPLIED, value, verse)
        if verse in _AGREEING_BANG_VERSES:
            if MAM_TARGET_PARAMETER in params:
                raise AssertionError(
                    f"{verse}: a named agreeing bang note has MAM's target"
                )
            value = _one_agreeing_clause(clauses, verse, "!")
            self._found(_BANG_AGREEING, verse)
            self._named_found[_BANG_AGREEING, verse] += 1
            _merge_flag(flags, APPLIED_AND_FLAGGED, value, verse)
        not_applied = phase5.NOT_APPLIED_READINGS.get(verse)
        if not_applied is not None and not_applied.note == number:
            value = _numbered_clause(clauses, not_applied.clause, verse)
            self._found(_NOT_APPLIED_READING, verse)
            _merge_flag(flags, FLAGGED_NOT_APPLIED, value, verse)

        sites = [
            site
            for site in _SILENCE_SITES
            if site[0] == verse and site[4] == _NOTE_PLACEMENT
        ]
        for site in sites:
            matches = _matching_templates(params[_TARGET], site[1], site[2], site[3])
            if not matches:
                continue
            if len(matches) != 1:
                raise AssertionError(
                    f"{verse}: note silence site {site[1:4]} matched {len(matches)} templates, not 1"
                )
            self._silence_found[site] += 1
            self._found(_SILENT_APPARATUS, verse)
            _merge_flag(flags, FLAGGED_NOT_APPLIED, _QERE_SILENCE, verse)
        return flags

    def _template_silence_flags(self, template, verse, note_depth):
        flags = {}
        for site in _SILENCE_SITES:
            if site[0] != verse or site[4] != _TEMPLATE_PLACEMENT:
                continue
            if _matches(template, site[1], site[2], site[3]):
                if note_depth:
                    raise AssertionError(
                        f"{verse}: a silence flag assigned to a template inside a note target"
                    )
                self._silence_found[site] += 1
                self._found(_SILENT_APPARATUS, verse)
                value = (
                    _MAQAF_SILENCE
                    if template["tmpl_name"] == "כתיב ולא קרי"
                    else _QERE_SILENCE
                )
                flags[FLAGGED_NOT_APPLIED] = value
        return flags

    def _add_flags(self, template, flags, verse):
        if len(flags) > 1:
            raise AssertionError(f"{verse}: one template would get both flag kinds")
        params = template["tmpl_params"]
        for name, value in flags.items():
            if name in params:
                raise AssertionError(f"{verse}: template already has {name!r}")
            params[name] = copy.deepcopy(value)
            self._found(name, verse)

    def _found(self, label, verse, number=1):
        self.counts[label] += number
        self.sites[label] += [verse] * number


def _raw_clauses(body):
    clauses = [[]]
    for item in body if isinstance(body, list) else [body]:
        if isinstance(item, dict):
            template_names.validate_current_plus_template(item)
        if isinstance(item, dict) and item["tmpl_name"] == "ש":
            clauses.append([])
        else:
            clauses[-1].append(item)
    return [phase2._simplify(items) for items in clauses]


def _clauses_with_values(body, verse):
    texts = phase3._clauses(body, verse)
    values = _raw_clauses(body)
    if len(texts) != len(values):
        raise AssertionError(
            f"{verse}: note body has {len(texts)} read clauses and {len(values)} structural clauses"
        )
    return list(zip(texts, values))


def _qualified_codex_sigla(head):
    found = []
    for element in phase3._split_outside_brackets(head):
        qualifier = element[len(element.rstrip("!?")) :]
        base = element.rstrip("!?")
        for siglum in phase3._head_sigla(base):
            if siglum in phase3._STRESS_HELPER_CODEX_SIGLA:
                found.append((siglum, qualifier))
    return found


def _one_agreeing_clause(clauses, verse, qualifier):
    found = []
    for clause, value in clauses:
        if not clause.startswith("="):
            continue
        rest = clause[1:]
        head = rest[: phase3._first_space_outside_brackets(rest)]
        sigla = _qualified_codex_sigla(head)
        if any(qualifier in mark for _, mark in sigla):
            found.append(value)
    if len(found) != 1:
        raise AssertionError(
            f"{verse}: expected one agreeing codex clause marked {qualifier!r}, found {len(found)}"
        )
    return found[0]


def _numbered_clause(clauses, number, verse):
    """The structural value of the ``number``th non-empty clause, numbered from 1 as
    phase 5 numbers them."""
    values = [value for text, value in clauses if text]
    if not 1 <= number <= len(values):
        raise AssertionError(
            f"{verse}: the note has {len(values)} non-empty clauses, not a clause "
            f"{number}"
        )
    return values[number - 1]


def _joined_clauses(values):
    items = []
    for value in values:
        if items:
            items.append(copy.deepcopy(_SEPARATOR))
        items += copy.deepcopy(phase2._as_list(value))
    return phase2._simplify(phase2._merge_strings(items))


def _merge_flag(flags, name, value, verse):
    if name in flags:
        raise AssertionError(f"{verse}: two independent rules assign {name!r}")
    flags[name] = value


def _matches(template, family, key, value):
    return template["tmpl_name"] == family and template["tmpl_params"].get(key) == value


def _matching_templates(value, family, key, expected):
    found = []
    if isinstance(value, str):
        return found
    if isinstance(value, list):
        for item in value:
            found += _matching_templates(item, family, key, expected)
        return found
    if _matches(value, family, key, expected):
        found.append(value)
    rule = phase2._RULES.get(value["tmpl_name"])
    if rule is None:
        return found
    params = value.get("tmpl_params", {})
    if rule.action == phase2._DISSOLVE:
        found += _matching_templates(params[rule.keys[0]], family, key, expected)
    elif rule.action == phase2._KEEP_NOTE:
        found += _matching_templates(params[_TARGET], family, key, expected)
    elif rule.action == phase2._KEEP_KQ:
        for item in params.values():
            found += _matching_templates(item, family, key, expected)
    return found
