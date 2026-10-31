"""Differential: each override copy of a UXLC change list differs from its original exactly
as uxlc/in/UXLC-misc-fixed/corrections.json says.

``py/uxlc_changes/uxlc_misc_path.py`` reads a change list's copy in
uxlc/in/UXLC-misc-fixed/ in place of the original in uxlc/in/UXLC-misc/, which
``py/main_uxlc_download_changes.py`` refreshes. A copy is the original with corrected
values, and corrections.json lists each one: its list, its record, its field, the UXLC's
value and MAM-basics' value. Without this test a copy would silently hide any later edit
the UXLC makes to its list, as the UXLC has made to lists after MAM-basics copied them.

The test parses each copy and its original, and asserts that they have the same records,
in the same order, with the same elements, and the same text in every element but the
manifest's. A failure says which of two things happened. If the original now holds
MAM-basics' value, the UXLC has adopted the correction: retire the entry, and delete a copy
that no longer holds any. If the original differs anywhere else, the UXLC has edited the
list: rebuild the copy from the new original and reapply the manifest's entries.

The folder holds two files that are not copies, each named below: the location estimator's
fixture, which has no original, and corrections.json. Any other file fails, as does a
copy of a list that py/uxlc_misc/my_uxlc_changes.py does not name, which nothing reads.
The manifest's fields and values are closed sets, so that an entry cannot claim a
correction this test does not check.
"""

import json
import unittest
import xml.etree.ElementTree as ET

import uxlc_misc.my_uxlc_changes as my_uxlc_changes
import uxlc_paths

_FIXTURE = "2000.01.01 - Changes fake.xml"
_MANIFEST = "corrections.json"

# The elements an entry may correct, by their path within a <change>.
_CORRECTABLE = {"column": "lc/column", "line": "lc/line"}
_KINDS = ("reading", "estimate")
_COMMON_KEYS = {
    "list",
    "record",
    "field",
    "uxlc",
    "mam_basics",
    "kind",
    "date",
    "evidence",
}


def _expected_keys(entry):
    """A line entry also gives the line counted including blank lines; a column entry
    does not."""
    if entry["field"] == "line":
        return _COMMON_KEYS | {"line_ib"}
    if entry["field"] == "column":
        return _COMMON_KEYS
    raise ValueError(f"unknown field {entry['field']!r} in {entry['record']}")


def _entry_problems(entry):
    problems = []
    if not isinstance(entry, dict) or "field" not in entry or "record" not in entry:
        return [f"not an entry with a field and a record: {entry!r}"]
    if entry["field"] not in _CORRECTABLE:
        return [
            f"{entry['record']}: field {entry['field']!r} is not one of {sorted(_CORRECTABLE)}"
        ]
    if set(entry) != _expected_keys(entry):
        problems.append(f"{entry['record']} {entry['field']}: keys {sorted(entry)}")
    if entry.get("kind") not in _KINDS:
        problems.append(
            f"{entry['record']} {entry['field']}: kind {entry.get('kind')!r}"
        )
    if not (isinstance(entry.get("mam_basics"), str) and entry["mam_basics"].isdigit()):
        problems.append(
            f"{entry['record']} {entry['field']}: value {entry.get('mam_basics')!r}"
        )
    if entry["field"] == "line":
        line_ib = entry.get("line_ib")
        if entry.get("kind") == "estimate":
            if line_ib is not None:
                problems.append(f"{entry['record']}: an estimate counts no lines")
        elif not (isinstance(line_ib, str) and line_ib.isdigit()):
            problems.append(f"{entry['record']}: a reading's line_ib {line_ib!r}")
    return problems


def _changes(path):
    """{record: {path within the change: [text, ...]}} in document order, for one change
    list. A path holds a list because a change can repeat an element, such as <note>."""
    root = ET.parse(path).getroot()
    result = {}
    for changeset in root.find("dates").findall("date"):
        date = changeset.findtext("date")
        for change in changeset.findall("change"):
            record = f"{date}-{change.findtext('n').strip()}"
            assert record not in result, f"{path.name}: {record} twice"
            fields = {}
            for elem_path, elem in _walk(change, ""):
                fields.setdefault(elem_path, []).append(elem.text or "")
            result[record] = fields
    return result


def _walk(elem, prefix):
    for child in elem:
        child_path = prefix + child.tag
        yield child_path, child
        yield from _walk(child, child_path + "/")


def _header(path):
    """The text of each element outside <dates>, such as <filedate>."""
    root = ET.parse(path).getroot()
    return [(child.tag, child.text or "") for child in root if child.tag != "dates"]


class UxlcMiscFixedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixed_dir = uxlc_paths.uxlc_misc_fixed_dir()
        manifest = json.loads((fixed_dir / _MANIFEST).read_text(encoding="utf-8"))
        cls.entries = manifest["corrections"]
        cls.names = sorted(p.name for p in fixed_dir.iterdir())
        cls.copies = [n for n in cls.names if n not in (_FIXTURE, _MANIFEST)]
        cls.fixed_dir = fixed_dir

    def test_the_folder_holds_copies(self):
        """So that finding no difference cannot mean reading nothing."""
        self.assertTrue(self.copies)
        self.assertTrue(self.entries)

    def test_the_folder_holds_only_copies_the_fixture_and_the_manifest(self):
        unread = [n for n in self.copies if n not in my_uxlc_changes.FILENAMES]
        self.assertEqual(
            unread,
            [],
            "these files are neither the fixture, nor corrections.json, nor a copy of a"
            " list that py/uxlc_misc/my_uxlc_changes.py names, so nothing reads them",
        )

    def test_every_entry_is_well_formed(self):
        problems = [p for entry in self.entries for p in _entry_problems(entry)]
        self.assertEqual(problems, [], "corrections.json has malformed entries")

    def test_every_entry_names_a_copy_and_every_copy_has_an_entry(self):
        listed = {entry["list"] for entry in self.entries}
        self.assertEqual(sorted(listed - set(self.copies)), [], "entries name no copy")
        self.assertEqual(sorted(set(self.copies) - listed), [], "copies have no entry")

    def test_each_copy_differs_from_its_original_exactly_as_the_manifest_says(self):
        failures = []
        for name in self.copies:
            original_path = uxlc_paths.uxlc_misc_dir() / name
            if not original_path.exists():
                failures.append(f"{name}: no original in uxlc/in/UXLC-misc/")
                continue
            failures.extend(self._differences(name, original_path))
        self.assertEqual(
            failures, [], "copies and originals disagree with the manifest"
        )

    def _differences(self, name, original_path):
        copy_path = self.fixed_dir / name
        failures = []
        if _header(original_path) != _header(copy_path):
            failures.append(f"{name}: the header outside <dates> differs")
        original, copy = _changes(original_path), _changes(copy_path)
        if list(original) != list(copy):
            return failures + [f"{name}: the records or their order differ"]
        expected = {
            (entry["record"], _CORRECTABLE[entry["field"]]): entry
            for entry in self.entries
            if entry["list"] == name
        }
        for record, original_fields in original.items():
            copy_fields = copy[record]
            if list(original_fields) != list(copy_fields):
                failures.append(f"{name}: {record}'s elements differ")
                continue
            for elem_path, original_texts in original_fields.items():
                entry = expected.pop((record, elem_path), None)
                copy_texts = copy_fields[elem_path]
                if entry is None:
                    if original_texts != copy_texts:
                        failures.append(
                            f"{name}: {record} {elem_path} is {original_texts!r} in the"
                            f" original and {copy_texts!r} in the copy, and"
                            " corrections.json has no entry for it: the UXLC may have"
                            " edited the list"
                        )
                    continue
                if len(original_texts) != 1 or len(copy_texts) != 1:
                    failures.append(f"{name}: {record} has more than one {elem_path}")
                    continue
                original_text, copy_text = original_texts[0], copy_texts[0]
                if original_text == entry["mam_basics"]:
                    failures.append(
                        f"{name}: {record} {elem_path}: the original now holds MAM-basics'"
                        f" value {entry['mam_basics']!r}, so the UXLC has adopted the"
                        " correction; retire the entry"
                    )
                elif original_text != entry["uxlc"]:
                    failures.append(
                        f"{name}: {record} {elem_path}: the original holds"
                        f" {original_text!r}, not the UXLC value {entry['uxlc']!r} that"
                        " corrections.json gives: the UXLC may have edited the list"
                    )
                if copy_text != entry["mam_basics"]:
                    failures.append(
                        f"{name}: {record} {elem_path}: the copy holds {copy_text!r}, not"
                        f" MAM-basics' value {entry['mam_basics']!r}"
                    )
        failures.extend(
            f"{name}: {record} has no {elem_path} for its entry"
            for record, elem_path in expected
        )
        return failures


if __name__ == "__main__":
    unittest.main()
