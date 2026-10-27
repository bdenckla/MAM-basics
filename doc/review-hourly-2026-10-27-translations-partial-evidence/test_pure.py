"""Pure note/serializer checks; no FOI collection or generator execution."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from lxml import html
import pytest

from foi import dexi_stress_meteg_explanations as explanation
from foi import dexi_stress_meteg_translations as translation
from foi import foi_finals
from mb_cmn import paths
from mb_misc import mb_html

ROOT = paths.repo_root()
OUT = ROOT / ".novc/hourly"
OLD = "076198c8a4469d08204b9e33c510d5ff02ae7e48"
PAGE = "gh-pages/MAM-with-doc/foi/foi-dexi-stress-meteg"
ROWS = json.loads((ROOT / (PAGE + ".json")).read_text())


def old_blob(path):
    return subprocess.check_output(["git", "show", f"{OLD}:{path}"], cwd=ROOT)


def signature(node):
    spaced = lambda text: " ".join((text or "").split())
    return (
        node.tag,
        sorted(node.attrib.items()),
        spaced(node.text),
        [(signature(child), spaced(child.tail)) for child in node],
    )


def render(elements):
    return mb_html.html_text(
        elements, mb_html.WriteCtx("pure fixture", "not-written.html")
    )


def test_committed_page_preserves_notes_forms_and_other_content():
    assert (ROOT / (PAGE + ".json")).read_bytes() == old_blob(PAGE + ".json")
    previous = html.fromstring(old_blob(PAGE + ".html"))
    current = html.fromstring((ROOT / (PAGE + ".html")).read_bytes())
    old_rows, new_rows = previous.xpath("//table/tr"), current.xpath("//table/tr")
    assert len(old_rows) == len(new_rows) == len(ROWS) == 9
    scripts = current.xpath("//script")
    assert len(scripts) == 1 and scripts[0].text.strip() == explanation.SCRIPT.strip()
    assert (
        scripts[0].getparent().tag == "body"
        and scripts[0] is scripts[0].getparent()[-1]
    )
    buttons, quotations = 0, 0
    for before, after in zip(old_rows, new_rows):
        a, b = before.xpath("./td")[0], after.xpath("./td")[0]
        button, hebrew, english = b
        assert (
            button.tag == "button"
            and button.get("type") == "button"
            and button.get("class") == "translation-toggle"
        )
        assert (
            " ".join(button.text_content().split())
            == "click to show English translation"
        )
        assert hebrew.tag == english.tag == "div"
        assert (
            hebrew.get("lang") == "hbo"
            and hebrew.get("dir") == "rtl"
            and "hidden" not in hebrew.attrib
        )
        assert (
            "hidden" in english.attrib
            and "lang" not in b.attrib
            and "dir" not in b.attrib
        )
        assert english.xpath("./p/em/text()") == [
            "AI-generated translation, not yet reviewed by a human."
        ]
        assert [signature(node) for node in a] == [signature(node) for node in hebrew]
        assert [signature(node) for node in before.xpath("./td")[1:]] == [
            signature(node) for node in after.xpath("./td")[1:]
        ]
        buttons += 1
        quotations += len(english.xpath('.//span[@lang="hbo"][@dir="rtl"]'))
        children = [deepcopy(node) for node in hebrew]
        text = hebrew.text
        b.clear()
        b.attrib.update(a.attrib)
        b.text = text
        b.extend(children)
    paragraphs = current.xpath("/html/body/div/p")
    caveat = paragraphs[2]
    assert "not yet reviewed by a human" in caveat.text_content()
    caveat.getparent().remove(caveat)
    scripts[0].getparent().remove(scripts[0])
    assert signature(previous) == signature(current)
    (OUT / "committed-page-result.json").write_text(
        json.dumps(
            {
                "rows": buttons,
                "pointed_hebrew_quote_spans": quotations,
                "original_notes_and_forms_preserved": True,
                "only_added_page_structures": "translation controls/blocks, caveat paragraph and final script",
                "initial_hebrew_visible_english_hidden": True,
            },
            indent=2,
        )
        + "\n"
    )
    (OUT / "toggle-input.json").write_text(
        json.dumps({"script": explanation.SCRIPT, "buttons": buttons}) + "\n"
    )


def test_all_current_translation_parts_and_quoted_codepoints():
    original = deepcopy(ROWS)
    parts = quoted = 0
    for row in ROWS:
        lemma, source_parts = translation._lemma_and_parts(row["note"])
        english_parts = translation._BY_NOTE[lemma, source_parts]
        assert len(source_parts) == len(english_parts)
        for source, english in zip(source_parts, english_parts):
            result = translation._with_hebrew_spans(english, source)
            for item in result:
                if isinstance(item, dict):
                    assert item["attr"] == {"lang": "hbo", "dir": "rtl"}
                    assert len(item["contents"]) == 1 and item["contents"][0] in source
                    quoted += 1
            parts += 1
        document = html.fromstring(render(translation.english_note(row["note"])))
        assert len(document.xpath("//li")) == len(source_parts) - 1
        assert document.xpath("//em/text()") == [
            "AI-generated translation, not yet reviewed by a human."
        ]
    assert ROWS == original
    (OUT / "translation-parts-result.json").write_text(
        json.dumps(
            {
                "source_notes": len(ROWS),
                "parts": parts,
                "exact_quoted_hebrew_runs": quoted,
                "source_data_unmodified": True,
                "human_review_claim": False,
            },
            indent=2,
        )
        + "\n"
    )


@pytest.mark.parametrize(
    "mutation", ("lemma", "part", "attribute", "nontext", "foreign_quote", "duplicate")
)
def test_stale_or_malformed_notes_and_quotations_reject(mutation):
    note = deepcopy(ROWS[0]["note"])
    with pytest.raises(ValueError):
        if mutation == "lemma":
            note[0]["contents"][0] += "X"
            translation.english_note(note)
        elif mutation == "part":
            note[2]["contents"][0] += "X"
            translation.english_note(note)
        elif mutation == "attribute":
            note[0]["attr"]["unexpected"] = "value"
            translation.english_note(note)
        elif mutation == "nontext":
            note[2]["contents"] = [mb_html.span("inner")]
            translation.english_note(note)
        elif mutation == "foreign_quote":
            translation._with_hebrew_spans("A quote: תָּו", "א")
        else:
            translation._by_note(
                (translation._TRANSLATIONS[0], translation._TRANSLATIONS[0])
            )


def test_shared_serializer_parent_controls_and_script():
    path = OUT / "parent_mb_html.py"
    path.write_bytes(old_blob("py/mb_misc/mb_html.py"))
    spec = importlib.util.spec_from_file_location("review_parent_mb_html", path)
    parent = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = parent
    spec.loader.exec_module(parent)
    controls = [
        mb_html.para("alpha & beta < gamma > delta"),
        mb_html.div((mb_html.span("א֑", {"lang": "hbo", "dir": "rtl"}), " tail")),
        mb_html.unordered_list(("first", "second")),
        mb_html.table((mb_html.table_row_of_data(("alpha", "beta")),)),
        mb_html.htel_mk("style", flex_contents="\n x > y { width: 1px; }\n"),
    ]
    for control in controls:
        assert render([control]) == parent.html_text(
            [control], parent.WriteCtx("pure fixture", "not-written.html")
        )
    script = "\n const comparison = 1 < 2 && 3 > 0;\n"
    document = render(
        [mb_html.script(script), mb_html.button("toggle", {"type": "button"})]
    )
    assert (
        script.strip() in document
        and "&lt;" not in document
        and "&amp;" not in document
    )
    assert (
        html.fromstring(document).xpath("//script/text()")[0].strip() == script.strip()
    )
    with pytest.raises(AssertionError):
        mb_html.para(" leading")
    with pytest.raises(AssertionError):
        mb_html.button(" trailing ")
    (OUT / "serializer-controls-result.json").write_text(
        json.dumps(
            {
                "parent_controls_equal": len(controls),
                "verbatim_script_operators_preserved": True,
                "normal_space_guards_preserved": True,
            }
        )
        + "\n"
    )


def test_script_hook_is_targeted_and_after_table(monkeypatch):
    writes = []
    monkeypatch.setattr(
        foi_finals,
        "_get_html_body1_and_2",
        lambda *_: ([mb_html.table((mb_html.table_row_of_data(("body",)),))], []),
    )
    monkeypatch.setattr(foi_finals, "_overall_head", lambda *_: [])
    monkeypatch.setattr(
        mb_html,
        "write_html_to_file",
        lambda body, context: writes.append(deepcopy(body)),
    )
    foi_finals._write_html("selected", "dexi-stress-meteg", {}, {})
    foi_finals._write_html("selected", "doc-note-notation", {}, {})
    assert len(writes[0]) == 2 and writes[0][-1]["_htel_tag"] == "script"
    assert len(writes[1]) == 1 and writes[1][0]["_htel_tag"] == "div"
    assert writes[0][0]["_htel_tag"] == "div"
    (OUT / "mocked-hook-result.json").write_text(
        json.dumps(
            {
                "target_only_script": True,
                "after_table_wrapper": True,
                "actual_file_writes": False,
            }
        )
        + "\n"
    )
