"""One-off focused differential checks for the authorized October 26 window."""

from collections import Counter
import json
from pathlib import Path
import subprocess
import sys
import time

import pytest

from mb_cmn import bib_locales as locales
from mb_cmn import mam_bknas_and_std_bknas as book_names
from mb_cmn import paths
from mb_cmn.minirow import MinirowExt
from mb_cmn.template_names import CURRENT_PLUS_TMPL_NAMES
from foi import foiz_wt_doc_note_notation as subject
from foi import foi_finals, foi_struct

ROOT = paths.repo_root()
OUTPUT = ROOT / "gh-pages/MAM-with-doc/foi"
EVIDENCE = ROOT / ".novc/hourly"
RESULT = {}


def in_core(char):
    cp = ord(char)
    return (
        0x05D0 <= cp <= 0x05EA
        or 0x0591 <= cp <= 0x05C7
        or cp in {0x034F, 0x200C, 0x200D}
    )


def scan_text(text):
    """Independent character scanner: no production regex or traversal helper."""
    token = []
    for char in text + " ":
        if in_core(char) or char in "[]+«»":
            token.append(char)
            continue
        form = "".join(token)
        token = []
        if any(
            char == "+" and in_core(form[i - 1]) and in_core(form[i + 1])
            for i, char in enumerate(form)
            if 0 < i < len(form) - 1
        ):
            yield "plus", form
        if "«" in form or "»" in form:
            yield "double-guillemets", form


def walk_raw(value, inside_body=False, notes=None):
    if isinstance(value, str):
        if inside_body:
            yield from scan_text(value)
    elif isinstance(value, list):
        for child in value:
            yield from walk_raw(child, inside_body, notes)
    else:
        name = value["tmpl_name"].replace('"', "\N{HEBREW PUNCTUATION GERSHAYIM}")
        assert name in CURRENT_PLUS_TMPL_NAMES, name
        if name == "נוסח" and notes is not None:
            notes.append(value)
        for key, child in value.get("tmpl_params", {}).items():
            yield from walk_raw(
                child, inside_body or (name == "נוסח" and key == "2"), notes
            )


def snapshot():
    return {p.name: p.read_bytes() for p in OUTPUT.iterdir() if p.is_file()}


def run_cli(label, *args):
    command = [sys.executable, "py/main_foi_features_of_interest.py", *args]
    start = time.monotonic()
    proc = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8"
    )
    (EVIDENCE / f"{label}.log").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    RESULT[label] = {
        "command": command,
        "exit_code": proc.returncode,
        "seconds": round(time.monotonic() - start, 3),
    }
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_raw_corpus_and_real_cli_outputs():
    oracle = Counter()
    notes = []
    files = sorted((ROOT / "MAM-parsed/plus").glob("*.json"))
    assert len(files) == 24
    for path in files:
        for book in json.loads(path.read_text(encoding="utf-8"))["book39s"]:
            bkid = book_names.MAM_HBNP_TO_BK39ID[
                book["book24_name"], book["sub_book_name"]
            ]
            for chapter, verses in book["chapters"].items():
                for verse, cells in verses.items():
                    if verse in {"0", "תתת"}:
                        continue
                    bcv = locales.short_bcv_of_bcvt(
                        locales.mk_bcvtmam(bkid, int(chapter), int(verse))
                    )
                    for cell in cells:
                        oracle.update(
                            (bcv, cat, form)
                            for cat, form in walk_raw(cell, notes=notes)
                        )
            if ending := book["good_ending_plus"]:
                chapter, verse = ending["last_chapnver"]
                bcv = locales.short_bcv_of_bcvt(
                    locales.mk_bcvtmam(bkid, int(chapter), int(verse))
                )
                oracle.update(
                    (bcv, cat, form)
                    for cat, form in walk_raw(ending["wikitext_element"], notes=notes)
                )
    before = snapshot()
    run_cli("all-foi", "--single-threaded")
    after = snapshot()
    assert before == after, sorted(
        k for k in before.keys() | after.keys() if before.get(k) != after.get(k)
    )
    rows = json.loads(
        (OUTPUT / "foi-doc-note-notation.json").read_text(encoding="utf-8")
    )
    assert oracle == Counter((r["bcv_short"], r["fp"], r["r"]) for r in rows)
    assert len(rows) == 8 and all(r["fp"] == "plus" for r in rows)
    html = (OUTPUT / "foi-doc-note-notation.html").read_text(encoding="utf-8")
    assert 'id="intro-double-guillemets"' in html
    empty_section = html.split('id="intro-double-guillemets"', 1)[1].split(
        'id="intro-plus"', 1
    )[0]
    assert (
        "None are" in empty_section
        and "found." in empty_section
        and "<table" not in empty_section
    )
    assert (
        html.count("<tr>") == 8 and html.count('<table class="border-collapse">') == 1
    )
    RESULT["corpus"] = {
        "books": len(files),
        "note_bodies": len(notes),
        "plus_rows": len(rows),
        "double_guillemet_rows": 0,
        "rows": rows,
    }
    RESULT["output_comparison"] = {
        "files_reproduced_byte_for_byte": len(before),
        "unexpected_differences": [],
        "existing_files_unchanged": len(before) - 2,
    }


def tmpl(name, **params):
    return {"tmpl_name": name, "tmpl_params": params}


def note(body):
    return tmpl("נוסח", **{"1": "ת+ת", "2": body})


@pytest.mark.parametrize("column", range(3))
def test_note_body_in_each_verse_column(column):
    cells = [[], [], []]
    cells[column] = ["ח+ח", note("א+א")]
    minirow = MinirowExt(*cells, [note("ק+ק")])
    assert subject.find_fois_wt({"mroge-minirow": minirow}) == [
        (subject.FOI_PATHS[1], "א+א")
    ]


def test_nested_notes_alternatives_and_scroll_note_selection():
    nested = note(["א+א ", tmpl("מודגש", **{"1": "ב+ב"}), note("ג+ג")])
    scroll = tmpl("מ:הערה-2", **{"1": "ד+ד", "2": "ה+ה", "3": "ו+ו"})
    dual = tmpl("מ:כפול", **{"כפול": note("ז+ז"), "א": note("ח+ח"), "ב": note("ט+ט")})
    qamats = tmpl("מ:קמץ", **{"ד": note("י+י"), "ס": note("כ+כ")})
    tree = [nested, scroll, dual, qamats, note(scroll)]
    # A nested note's target is still text within its outer note's body.
    actual = Counter(
        (path[1], form)
        for path, form in subject.find_fois_wt(
            {"mroge-minirow": MinirowExt([], [], tree, [note("ק+ק")])}
        )
    )
    assert actual == Counter(walk_raw(tree))
    assert sum(actual.values()) == 12


def test_good_ending_and_notation_character_selection():
    tree = note("א+א «ב» ג+ג «ד+ד» ‹ה› + ו+ +ז A+B ח+ A+ט [י+י]")
    actual = Counter(
        (path[1], form)
        for path, form in subject.find_fois_wt(
            {"mroge-good-ending": {"wikitext_element": tree}}
        )
    )
    assert actual == Counter(walk_raw(tree))
    assert actual["double-guillemets", "«ד+ד»"] == 1
    assert actual["plus", "«ד+ד»"] == 1
    assert sum(actual.values()) == 6


def test_empty_declared_stem_and_selected_cli_isolation(tmp_path, monkeypatch):
    monkeypatch.setattr(foi_finals, "_OUT_DIR_PATH", str(tmp_path))
    all_fois = foi_struct.make_empty_all_fois()
    foi_struct.declare_foi_paths(all_fois, subject.FOI_PATHS)
    foi_finals.write("args-foi-doc-note-notation", all_fois)
    assert (
        json.loads(
            (tmp_path / "foi-doc-note-notation.json").read_text(encoding="utf-8")
        )
        == []
    )
    html = (tmp_path / "foi-doc-note-notation.html").read_text(encoding="utf-8")
    assert " ".join(html.split()).count("None are found.") == 2 and "<table" not in html
    before = snapshot()
    run_cli("selected-note", "--foi", "args-foi-doc-note-notation", "--single-threaded")
    assert before == snapshot()
    # Timestamps detect writes even when identical output bytes are rewritten.
    protected = [
        OUTPUT / "index.html",
        OUTPUT / "foi-doc-note-notation.html",
        OUTPUT / "foi-doc-note-notation.json",
    ]
    times = {p.name: p.stat().st_mtime_ns for p in protected}
    run_cli("selected-other", "--foi", "args-foi-kq-2", "--single-threaded")
    assert times == {p.name: p.stat().st_mtime_ns for p in protected}
    assert before == snapshot()
    RESULT["isolation"] = (
        "Selected note run reproduces all files; selected kq-2 run leaves note HTML/JSON and index bytes and nanosecond mtimes unchanged."
    )
    (EVIDENCE / "result.json").write_text(
        json.dumps(RESULT, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
