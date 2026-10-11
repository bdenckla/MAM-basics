"""Apply recorded body encodings beside unchanged qere-without-ketiv calls.

Each record names its whole qere and one body template. The walk selects only
Scripture fields, excluding note bodies and apparatus alternatives. The additional
template immediately precedes the original call in the same sequence, without an
inserted separator. Artificial carriers describe marks, never ketiv letters.
"""

import copy
import json
from collections import Counter, defaultdict

from mb_cmn import bib_locales as tbn
from mb_cmn import mam_bknas_and_std_bknas
from near_aleppo import build_paths
from near_aleppo import phase2_templates as phase2
from py_misc import orphan_marks

QERE_TEMPLATE = "קרי ולא כתיב"
BODY_NAMES = {
    "marks-with-space": orphan_marks.MARKS_WITHOUT_LETTER,
    "marks-without-space": orphan_marks.MARKS_WITHOUT_LETTER_OR_SPACE,
    "space-without-marks": orphan_marks.SPACE_WITHOUT_MARKS,
}


def build_reference(reference):
    book, chapter, verse = reference
    ref_book = tbn.ordered_short_dash_full_24(tbn.bk24id(book))
    pairs = {
        value: key for key, value in mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID.items()
    }
    sub_book = pairs[book][1]
    if sub_book is not None:
        ref_book += " " + sub_book
    return ref_book, str(chapter), str(verse)


def validate_encoding(row):
    """Validate the stored body shape independently of the qere's marks."""
    encoding = row["intended_encoding"]
    if encoding is None:
        return
    if set(encoding) != {"kind", "explanation", "template"}:
        raise AssertionError(f"{row['id']}: unexpected body-encoding fields")
    if encoding["kind"] not in BODY_NAMES:
        raise AssertionError(f"{row['id']}: unknown body classification")
    template = encoding["template"]
    if template is None:  # An explicitly pending manuscript-reading decision.
        return
    if template["tmpl_name"] != BODY_NAMES[encoding["kind"]]:
        raise AssertionError(
            f"{row['id']}: body template disagrees with classification"
        )
    orphan_marks.validate_body(template, row["id"])


def records():
    path = build_paths.input_dir() / "qere-without-ketiv-readings.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"format", "cases"} or data["format"] != (
        "near-aleppo-qere-without-ketiv-readings-v4"
    ):
        raise AssertionError(f"{path}: unsupported body-record format")
    rows = data["cases"]
    if not isinstance(rows, list) or not rows:
        raise AssertionError(f"{path}: no body records")
    for row in rows:
        validate_encoding(row)
    return rows


class BodyEncodings:
    """Apply each authored body encoding once and record its population."""

    def __init__(self):
        self.by_verse = {}
        self.used = set()
        self.counts = Counter()
        self.sites = defaultdict(set)
        for row in records():
            ref = build_reference(row["reference"])
            if ref in self.by_verse:
                raise AssertionError(f"Duplicate body record: {ref}")
            self.by_verse[ref] = row

    def apply(self, cell, ref):
        row = self.by_verse.get(ref)
        if row is None or row["intended_encoding"] is None:
            return cell
        template = row["intended_encoding"]["template"]
        if template is None:
            return cell
        found = 0

        def walk(value):
            nonlocal found
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                return [child for item in value for child in expand(item)]
            return phase2._simplify(expand(value))

        def expand(value):
            nonlocal found
            if isinstance(value, (str, list)):
                return [walk(value)]
            name = value["tmpl_name"]
            rule = phase2._RULES.get(name)
            if rule is None:
                raise AssertionError(f"{ref}: unknown template {name!r}")
            if name == QERE_TEMPLATE:
                qere = row["reading"]["qere"]
                if value != {
                    "tmpl_name": QERE_TEMPLATE,
                    "tmpl_params": {"1": "[" + qere + "]", "2": qere},
                }:
                    raise AssertionError(
                        f"{ref}: reconcile the whole qere call with {qere!r}"
                    )
                found += 1
                return [copy.deepcopy(template), value]
            if rule.action in (phase2._KEEP_NOTE, phase2._KEEP_KQ):
                for key in phase2.selected_keys(value, ref):
                    value["tmpl_params"][key] = walk(value["tmpl_params"][key])
            elif rule.action == phase2._CARRIERS:
                phase2.carriers_text(value, ref)
            elif name == orphan_marks.SPACE_WITHOUT_MARKS:
                orphan_marks.validate_space(value, ref)
            elif rule.action in (phase2._VERBATIM, phase2._COLLAPSE_WORD):
                if frozenset(value.get("tmpl_params", {})) not in rule.keysets:
                    raise AssertionError(f"{ref}: unexpected {name!r} parameters")
            else:
                raise AssertionError(f"{ref}: unresolved template {name!r}")
            return [value]

        cell = walk(cell)
        if found != 1 or ref in self.used:
            raise AssertionError(f"{ref}: expected one unused qere site, found {found}")
        self.used.add(ref)
        label = "qere-without-ketiv body: " + row["intended_encoding"]["kind"]
        self.counts[label] += 1
        self.sites[label].add(ref)
        return cell

    def finish(self):
        expected = {
            ref
            for ref, row in self.by_verse.items()
            if row["intended_encoding"] is not None
            and row["intended_encoding"]["template"] is not None
        }
        if self.used != expected:
            raise AssertionError(
                f"Unapplied body records: {sorted(expected - self.used)}"
            )
