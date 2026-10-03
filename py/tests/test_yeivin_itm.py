"""Differential publication checks and claim/source-shape lints for Yeivin ITM."""

import ast
from hashlib import sha256
import json
import subprocess
import sys
from urllib.parse import urlsplit

from lxml import html
import pytest

from mb_cmn import paths as repo_paths
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks
from yeivin_itm import claims, claim_schema, paths, publication, renderer, source_lint


def test_complete_rendering_matches_tracked_pages():
    pages = renderer.page_texts()
    assert len(pages) == 17
    for name, text in pages.items():
        assert (paths.pages_dir() / name).read_bytes() == text.encode("utf-8")
        refuse_forbidden_phonetic_marks(text, name)
        assert "{{meteg:" not in text


def test_identifiers_favicon_links_and_fragments_resolve():
    pages = renderer.page_texts()
    documents = {name: html.fromstring(text) for name, text in pages.items()}
    for name, document in documents.items():
        identifiers = document.xpath("//@id")
        assert len(identifiers) == len(set(identifiers))
        icons = document.xpath("/html/head/link[@rel='icon']")
        assert len(icons) == 1
        icon = icons[0]
        assert dict(icon.attrib) == {"rel": "icon", "href": "../favicon.svg"}
        assert (paths.pages_dir() / icon.attrib["href"]).resolve().is_file()
        icon.getparent().remove(icon)
        for target in document.xpath("//@href"):
            url = urlsplit(target)
            if url.scheme or url.netloc:
                continue
            if url.path and not url.path.endswith(".html"):
                assert (paths.pages_dir() / url.path).is_file()
                continue
            destination = documents[url.path or name]
            if url.fragment:
                assert url.fragment in destination.xpath("//@id")


def test_every_published_fragment_identifier_remains():
    """phonetic-hbo's redirect pages forward old addresses, fragments included, here.

    in/yeivin_itm_published_anchors.json records the fragment identifiers that the
    pages had at the end of the migration; an edit may add identifiers but may not
    remove a recorded one.
    """
    path = repo_paths.in_dir() / "yeivin_itm_published_anchors.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    assert record["schema"] == "yeivin-itm-published-anchors-v1"
    recorded = record["pages"]
    assert sum(map(len, recorded.values())), "the published-anchor record is empty"
    pages = renderer.page_texts()
    for name, identifiers in recorded.items():
        current = set(html.fromstring(pages[name]).xpath("//@id"))
        missing = [
            identifier for identifier in identifiers if identifier not in current
        ]
        assert not missing, (name, missing)


def test_approved_claim_schema_matches_the_tracked_data_and_named_pins():
    data = claims.read()
    schema = json.loads(
        (paths.product_dir() / "schema/meteg-claims-v1.schema.json").read_text("utf-8")
    )
    assert set(data) == set(schema["required"]) == set(schema["properties"])
    assert schema["additionalProperties"] is False
    assert data["schema"] == schema["properties"]["schema"]["const"]
    assert data["input"]["sha256"] == claim_schema.APPROVED_INPUT_SHA256
    for name in ("populations", "measurements"):
        spec = schema["properties"][name]
        assert (
            set(data[name])
            == set(spec["required"])
            == set(spec["propertyNames"]["enum"])
        )
    for name, values in data["measurements"].items():
        assert set(values) == set(schema["$defs"]["fraction"]["required"])
        assert (
            values["numerator"],
            values["denominator"],
        ) == claim_schema.APPROVED_FRACTIONS[name]
        assert values["percentage"] == 100 * values["numerator"] / values["denominator"]
    assert data == claims.from_analysis()


def test_footnote_numerical_claims_have_no_literal_duplicates():
    source_lint.check()
    content = repo_paths.repo_root() / "py" / "yeivin_itm" / "content"
    for filename in source_lint.FOOTNOTE_MODULES:
        tree = ast.parse((content / filename).read_text("utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "claim_text"
            ):
                name = ast.literal_eval(node.args[0])
                assert name in claims.read()["measurements"]


def test_assets_and_output_allowlist_match_generation():
    publication.check()
    for name, expected in publication.assets().items():
        assert (repo_paths.gh_pages_dir() / name).read_bytes() == expected


def test_real_check_command_is_write_neutral():
    roots = (
        repo_paths.repo_root() / "py" / "yeivin_itm",
        paths.product_dir(),
        paths.pages_dir(),
    )

    def snapshot():
        return {
            str(path): (path.stat().st_mtime_ns, sha256(path.read_bytes()).hexdigest())
            for root in roots
            for path in root.rglob("*")
            if path.is_file()
        }

    before = snapshot()
    subprocess.run(
        [sys.executable, "py/main_yeivin_itm.py", "check"],
        cwd=repo_paths.repo_root(),
        check=True,
    )
    assert snapshot() == before


@pytest.mark.parametrize("filename", source_lint.FOOTNOTE_MODULES)
def test_duplicate_claim_lint_rejects_a_restored_literal(filename):
    path = repo_paths.repo_root() / "py" / "yeivin_itm" / "content" / filename
    source = path.read_text("utf-8")
    with pytest.raises(ValueError, match="Hard-coded claim"):
        source_lint.check_source(source + "\n_EXTRA_CLAIM = 3583\n", filename)
