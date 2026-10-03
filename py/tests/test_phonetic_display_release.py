"""Complete-corpus differential and mechanical lints for the public display."""

import json

from lxml import html

from mb_cmn import bib_locales, paths
from phonetic_mam import display_schema, example_display, projection_check, release
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks


def test_complete_release_and_unified_projection():
    release.validate_complete_release()
    root = paths.repo_root()
    oracle = json.loads(
        (root / "in/phonetic_mam_legacy_projection_sha256.json").read_text(
            encoding="utf-8"
        )
    )
    inputs = json.loads(
        (root / "in/phonetic_mam_legacy_projection_inputs.json").read_text(
            encoding="utf-8"
        )
    )
    projection_check.verify_site(
        root / "gh-pages/phonetic-mam",
        oracle,
        inputs,
        projection_check.input_fingerprints(paths.mam_parsed_plus_dir()),
    )


def test_unified_site_controls_and_public_output_boundary():
    site = paths.gh_pages_dir() / "phonetic-mam"
    pages = list(site.rglob("*.html"))
    assert len(pages) == 974
    assert not (site / "tnkh-ashkenaz").exists()
    for path in pages:
        text = path.read_text(encoding="utf-8")
        refuse_forbidden_phonetic_marks(text, str(path))
        document = html.fromstring(text)
        ids = document.xpath("//@id")
        assert len(ids) == len(set(ids)), path
        if path.name in example_display.PAGE_NAMES:
            continue
        assert [
            value.strip() for value in document.xpath("//fieldset/legend/text()")
        ] == ["Pronunciation"]
        radios = document.xpath('//input[@name="pronunciation"]')
        assert [node.get("value") for node in radios] == list(
            display_schema.PRONUNCIATIONS
        )
        assert all(node.get("type") == "radio" for node in radios)
        assert document.xpath("//label/@for") == [node.get("id") for node in radios]
        assert document.xpath("//input[@checked]/@value") == ["sephardic"]
        assert "</input>" not in text
        for link in document.xpath("//a[@data-pronunciation-link]"):
            assert "?pronunciation=sephardic" in link.get("href"), path


def test_example_pages_match_their_display_input():
    expected = example_display.page_texts(release.read_examples())
    site = paths.gh_pages_dir() / "phonetic-mam"
    for name, text in expected.items():
        assert (site / name).read_text(encoding="utf-8") == text


def test_no_public_record_quality_layer():
    root = paths.phonetic_mam_dir()
    allowed = {
        root / "README.md",
        root / "schema/phonetic-mam-public-v1.schema.json",
        root / "examples/display.json",
    }
    allowed.update(release.data_path(book) for book in bib_locales.ALL_BK39_IDS)
    assert {path for path in root.rglob("*") if path.is_file()} == allowed
    schema = json.loads(
        (root / "schema/phonetic-mam-public-v1.schema.json").read_text(encoding="utf-8")
    )
    assert schema["additionalProperties"] is False
    assert schema["properties"]["schema"]["const"] == display_schema.SCHEMA_ID
    assert (
        tuple(schema["$defs"]["readingLabel"]["enum"]) == display_schema.READING_LABELS
    )
    # The schema's text pattern refuses exactly the marks the validator refuses.
    forbidden = "".join(
        f"\\u{ord(mark):04x}" for mark in sorted(display_schema._FORBIDDEN)
    )
    assert schema["$defs"]["text"]["pattern"] == f"^[^<>{forbidden}]+$"
