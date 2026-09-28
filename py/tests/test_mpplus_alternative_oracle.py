"""Compare all registered reports with an independent source-role projection.

The oracle reads the real stored/Git inputs and never calls the extractor's role
collector, flattened-text helpers, expansion policy, or serializer. Its expected
values therefore test detection, suppression, and serialization together.
"""

from collections import Counter, defaultdict
from functools import lru_cache
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from mb_cmn import retired_kq_special_templates as retired
from mb_cmn import template_names as names
from mb_cmn import unicode_data
from mb_cmn.hebrew_punctuation import NU_GMAQ, PASOLEG
from mb_cmn.str_defs import DOUB_VERT_LINE
from mb_cmn.uni_denorm import give_std_mark_order
from mb_diff_mpu import mpplus_revisions
from mb_diff_mpu.mpplus_file_matching import (
    book39_ids_for_stem,
    get_he_to_int,
    matched_plus_file_pairs,
)
from subcommands import diff_mpplus

_OLD_QERE = "קו״כ-אם"
_QERE_FAMILY = "מ:קו״כ-אם-2"
_SOURCE_KEYS = "קרי|א-קרי|א,ל-קרי|אל-קרי|ל-קרי|ל-קרי,ק13-קרי|ל1,ק3-קרי"
_QERE_TEXT = re.compile(rf"(?:(?:{_SOURCE_KEYS})=)?([^=()]+?)(?: \([^()]*\))?$")
_NOTE_QERE = re.compile(r"ל=יתיר י' \(קרי=([^=()]+)\)$")
_BODY_KEYS = {
    **{name: "1" for name in names.IN_WORD_TMPL_NAMES},
    **{name: "1" for name in names.STRESS_HELPER_TMPL_NAMES},
    **{name: "2" for name in names.STD_KQ_TMPL_NAMES},
    "נוסח": "1",
    "מודגש": "1",
    "מ:סיום בטוב": "1",
    names.SCRDFF_TAR: "1",
    _OLD_QERE: "1",
    _QERE_FAMILY: "1",
    names.QAMATS_VARIANT: "ד",
    names.DUAL_CANTILLATION: "כפול",
}
_LITERALS = {
    **{name: " " for name in names.NO_ATOM_TMPL_NAMES},
    "ש": " ",
    "מ:לגרמיה": PASOLEG,
    "מ:לגרמיה-2": PASOLEG,
    "מ:פסק": DOUB_VERT_LINE,
    "מ:מקף אפור": NU_GMAQ,
    names.INVERTED_NUN: "",
    names.SCRDFF_NO_TAR: "",
    "מ:קישור בהערה": "",
    "מ:קישור פנימי בהערה": "",
    "כתיב ולא קרי": "",
}


def _arg_value(value, written_key):
    """Decode a named argument; explicit positional roles do not parse source keys."""
    if isinstance(value, str):
        return value.removeprefix(written_key + "=")
    if isinstance(value, list) and value and isinstance(value[0], str):
        if value[0].startswith(written_key + "="):
            head = value[0][len(written_key) + 1 :]
            rest = value[1:]
            return (
                rest[0]
                if not head and len(rest) == 1
                else ([head] if head else []) + rest
            )
    return value


def _source_template(node):
    assert isinstance(node, dict) and isinstance(node.get("tmpl_name"), str), node
    name = node["tmpl_name"].replace('"', "\N{HEBREW PUNCTUATION GERSHAYIM}")
    assert set(node) <= {"tmpl_name", "tmpl_args", "tmpl_params", "tmpl_args_dic"}, node
    mapping_keys = [key for key in ("tmpl_params", "tmpl_args_dic") if key in node]
    if mapping_keys:
        parameters = node[mapping_keys[0]]
        assert isinstance(parameters, dict), node
        assert all(node[key] == parameters for key in mapping_keys), node
    else:
        args = node.get("tmpl_args", [])
        assert isinstance(args, list), node
        parameters = {}
        if name in {_OLD_QERE, "נוסח"}:
            assert len(args) == 2, node
            parameters = {
                str(i): _arg_value(value, str(i)) for i, value in enumerate(args, 1)
            }
        else:
            position = 0
            for value in args:
                head = (
                    value
                    if isinstance(value, str)
                    else value[0] if isinstance(value, list) and value else None
                )
                if isinstance(head, str) and "=" in head:
                    key = head.partition("=")[0]
                    decoded = _arg_value(value, key)
                else:
                    position += 1
                    key, decoded = str(position), value
                assert key not in parameters, node
                parameters[key] = decoded
    if name == _OLD_QERE or retired.is_old_special_kq_template_name(name):
        required = allowed = {"1", "2"}
    elif name == "מ:לגרמיה":
        required = allowed = set()
    elif name == names.SCRDFF_NO_TAR:
        required, allowed = {"1"}, {"1", "שם"}
    elif not mapping_keys and name in names.STRESS_HELPER_TMPL_NAMES:
        required, allowed = {"1"}, {"1", "2"}
    elif not mapping_keys and name == "קרי ולא כתיב":
        required, allowed = {"1"}, {"1", "2"}
    elif not mapping_keys and name == "כתיב ולא קרי":
        required, allowed = {"1"}, {"1", "2", "3"}
    else:
        assert (
            name in names.CURRENT_PLUS_PARAM_POLICY
        ), f"unknown oracle template {name!r}"
        required, allowed = names.CURRENT_PLUS_PARAM_POLICY[name]
    assert set(required) <= parameters.keys() <= set(allowed), (name, parameters)
    if retired.is_special_kq_template_name(name):
        kind = parameters.get("סוג")
        if isinstance(kind, list):
            assert len(kind) == 1 and isinstance(kind[0], str), node
            kind = kind[0]
        retired.canonical_special_kq_type_from_name_and_sug(name, kind)
    return name, parameters


def _child(name, parameters):
    if name in _BODY_KEYS:
        return parameters[_BODY_KEYS[name]]
    if retired.is_old_special_kq_template_name(name):
        return parameters["2"]
    if name == "קרי ולא כתיב":
        return parameters.get("2", parameters["1"])
    if name in _LITERALS:
        return None
    raise ValueError(f"unknown oracle Scripture template {name!r}")


def _scripture(node):
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return "".join(map(_scripture, node))
    name, parameters = _source_template(node)
    if name in _LITERALS:
        return _LITERALS[name]
    text = _scripture(_child(name, parameters))
    return text.replace("[", "").replace("]", "") if name == "קרי ולא כתיב" else text


def _role_value(node, *, historical=False):
    # The oracle decodes metadata after projecting a source value. Production
    # decodes metadata before projecting the source value.
    text = _scripture(node)
    if historical:
        match = _NOTE_QERE.fullmatch(text) or _QERE_TEXT.fullmatch(text)
        assert match is not None, f"unrecognized historical qere role {text!r}"
        text = match[1]
    return give_std_mark_order(text).replace(" " + PASOLEG, PASOLEG)


def _source_roles(ep):
    counts = Counter()
    roles = defaultdict(list)

    def traverse(node):
        if isinstance(node, str) or node is None:
            return
        if isinstance(node, list):
            for item in node:
                traverse(item)
            return
        name, parameters = _source_template(node)
        if name in {_OLD_QERE, _QERE_FAMILY, "מ:דחי"}:
            family = _QERE_FAMILY if name == _OLD_QERE else name
            counts[family] += 1
            parameter = "2" if name in {_OLD_QERE, "מ:דחי"} else "3"
            raw = parameters.get(parameter, [])
            roles[family].append(
                (
                    counts[family],
                    _role_value(parameters["1"]),
                    _role_value(raw, historical=name == _OLD_QERE),
                )
            )
        traverse(_child(name, parameters))

    traverse(ep)
    return roles


def _number(key, lookup):
    if key in {"0", "תתת"}:
        return None
    return int(key) if isinstance(key, int) or key.isdigit() else lookup[key]


@lru_cache(maxsize=None)
def _revision_roles(revision):
    source = mpplus_revisions.resolve(revision)
    records = {}
    for stem, filename, _unused in matched_plus_file_pairs(source.filenames(), []):
        data = json.loads(source.read(filename))
        book_ids = book39_ids_for_stem(stem)
        assert len(book_ids) == len(data["book39s"]), (revision, stem)
        lookup = get_he_to_int(data)
        for book, block in zip(book_ids, data["book39s"]):
            for raw_chapter, chapter in block["chapters"].items():
                ch = _number(raw_chapter, lookup)
                if ch is None:
                    continue
                for raw_verse, columns in chapter.items():
                    vr = _number(raw_verse, lookup)
                    if vr is None:
                        continue
                    key = book, ch, vr
                    assert key not in records, (revision, key)
                    records[key] = _source_roles(columns[2])
    assert records, f"empty oracle input population for {revision}"
    return records


def _paired_roles(before, after):
    if len(before) == len(after):
        return list(zip(before, after))
    # For a changed population the oracle uses unique Scripture-target anchors,
    # rather than production's sequence matcher. Unmatched template additions and
    # removals belong to the existing structural comparison, not a new role.
    old_targets = Counter(item[1] for item in before)
    new_targets = Counter(item[1] for item in after)
    common = old_targets.keys() & new_targets.keys()
    assert all(old_targets[target] == new_targets[target] == 1 for target in common), (
        "ambiguous changed alternative population",
        before,
        after,
    )
    new_by_target = {item[1]: item for item in after if item[1] in common}
    return [(item, new_by_target[item[1]]) for item in before if item[1] in common]


def _expected_changes(old_revision, new_revision):
    before = _revision_roles(old_revision)
    after = _revision_roles(new_revision)
    expected = {}
    for verse in before.keys() | after.keys():
        old_roles = before.get(verse, {})
        new_roles = after.get(verse, {})
        for family in (_QERE_FAMILY, "מ:דחי"):
            for old, new in _paired_roles(
                old_roles.get(family, []), new_roles.get(family, [])
            ):
                if old[2] == new[2]:
                    continue
                role = "qere" if family == _QERE_FAMILY else "stress-helper-alternative"
                old_letters = "".join(c for c in old[2] if not unicode_data.is_mark(c))
                new_letters = "".join(c for c in new[2] if not unicode_data.is_mark(c))
                kind = (
                    "pointing-migration"
                    if role == "qere"
                    and old_letters == old[2]
                    and old_letters == new_letters
                    else "content"
                )
                key = (*verse, family, new[0], role)
                assert key not in expected, key
                expected[key] = kind, old[2], new[2]
    return expected


def _serialized_changes(report_path):
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["diff_count"] == len(data["diffs"]), report_path
    actual = {}
    for diff in data["diffs"]:
        if "alternative_changes" not in diff:
            continue
        changes = diff["alternative_changes"]
        assert isinstance(changes, list) and changes, (report_path, diff)
        for change in changes:
            assert set(change) == {
                "template",
                "occurrence",
                "role",
                "kind",
                "old",
                "new",
            }, change
            assert (
                isinstance(change["occurrence"], int) and change["occurrence"] > 0
            ), change
            assert isinstance(change["old"], str) and isinstance(
                change["new"], str
            ), change
            assert change["old"] != change["new"], change
            key = (
                diff["book"],
                diff["chapter"],
                diff["verse"],
                change["template"],
                change["occurrence"],
                change["role"],
            )
            assert (
                key not in actual
            ), f"duplicated serialized alternative in {report_path}: {key!r}"
            actual[key] = change["kind"], change["old"], change["new"]
    return actual


def _assert_registered_alternatives(report_root):
    releases = json.loads(Path(diff_mpplus.RELEASES_JSON).read_text(encoding="utf-8"))[
        "releases"
    ]
    assert releases, "empty registered release population"
    continued = {entry["old"] for entry in releases}
    terminal = [entry for entry in releases if entry["new"] not in continued]
    assert len(terminal) == 1, "registered releases must form a single chain"
    pairs = [
        *releases,
        {"name": "unpinned-latest", "old": terminal[0]["new"], "new": "HEAD"},
    ]
    alternative_count = 0
    for pair in pairs:
        expected = _expected_changes(pair["old"], pair["new"])
        actual = _serialized_changes(report_root / f"{pair['name']}.json")
        missing = expected.keys() - actual.keys()
        extra = actual.keys() - expected.keys()
        different = {
            key
            for key in expected.keys() & actual.keys()
            if expected[key] != actual[key]
        }
        assert not (missing or extra or different), (
            f"{pair['name']}: missing alternatives {sorted(missing)!r}; "
            f"extra alternatives {sorted(extra)!r}; values differ {[(key, expected[key], actual[key]) for key in sorted(different)]!r}"
        )
        alternative_count += len(expected)
    assert (
        alternative_count
    ), "registered inputs produced an empty alternative-change population"


def test_registered_alternatives_match_independent_source_values():
    _assert_registered_alternatives(Path(diff_mpplus.CHANGE_LOG_DIR))


class _ClusterHighlightLint(HTMLParser):
    """Check every real Hebrew cluster across highlight/pointed-span boundaries."""

    def __init__(self):
        super().__init__()
        self.stack = []
        self.serial = 0
        self.base_context = None
        self.problems = []

    def handle_starttag(self, tag, attrs):
        self.serial += 1
        if tag in {"br", "hr", "img", "meta", "link", "input"}:
            if tag in {"br", "hr"}:
                self.base_context = None
            return
        attrs = dict(attrs)
        highlight = tag == "mark" or (
            tag == "span" and "pointed-heb" in attrs.get("class", "").split()
        )
        self.stack.append((tag, self.serial, highlight))

    def handle_endtag(self, tag):
        assert self.stack and self.stack[-1][0] == tag, (tag, self.stack)
        self.stack.pop()

    def handle_data(self, text):
        if any(tag in {"script", "style"} for tag, _serial, _highlight in self.stack):
            return
        context = tuple(serial for _tag, serial, highlight in self.stack if highlight)
        for character in text:
            if unicode_data.is_mark(character):
                if self.base_context is not None and context != self.base_context:
                    self.problems.append((self.getpos(), ord(character)))
            elif "\u05d0" <= character <= "\u05ea":
                self.base_context = context
            else:
                self.base_context = None


def _assert_report_clusters(report_root):
    releases = json.loads(Path(diff_mpplus.RELEASES_JSON).read_text(encoding="utf-8"))[
        "releases"
    ]
    assert releases, "empty registered report population"
    problems = []
    for name in [*(entry["name"] for entry in releases), "unpinned-latest"]:
        report = report_root / f"{name}.html"
        lint = _ClusterHighlightLint()
        lint.feed(report.read_text(encoding="utf-8"))
        problems.extend((name, *problem) for problem in lint.problems)
    assert not problems, f"Hebrew clusters split across highlight spans: {problems!r}"


def test_registered_report_marks_keep_their_base_highlight():
    _assert_report_clusters(Path(diff_mpplus.CHANGE_LOG_DIR))
