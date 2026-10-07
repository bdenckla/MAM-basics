"""Differential publication checks and claim/source-shape lints for Yeivin ITM."""

import ast
from collections import Counter
from hashlib import sha256
import json
import re
import subprocess
import sys
from types import MappingProxyType
from urllib.parse import urlsplit

from lxml import html
import pytest

from mb_cmn import paths as repo_paths
from mb_misc.osis_book_abbrevs import BOOK_ABBREVS
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks
from yeivin_itm import claims, claim_schema, paths, publication, renderer, source_lint
from yeivin_itm.content import my_yeivin_amisc_helpers_for_locales as locales


@pytest.fixture(scope="module")
def rendered_pages():
    """Share one immutable rendering; each check keeps its own comparison."""
    return MappingProxyType(renderer.page_texts())


def test_complete_rendering_matches_tracked_pages(rendered_pages):
    pages = rendered_pages
    assert len(pages) == 17
    for name, text in pages.items():
        assert (paths.pages_dir() / name).read_bytes() == text.encode("utf-8")
        refuse_forbidden_phonetic_marks(text, name)
        assert "{{meteg:" not in text


def test_identifiers_favicon_links_and_fragments_resolve(rendered_pages):
    pages = rendered_pages
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


def test_every_published_fragment_identifier_remains(rendered_pages):
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
    pages = rendered_pages
    for name, identifiers in recorded.items():
        current = set(html.fromstring(pages[name]).xpath("//@id"))
        missing = [
            identifier for identifier in identifiers if identifier not in current
        ]
        assert not missing, (name, missing)


_REFERENCE = re.compile(r"@(\S+) (\d+):(\d+)")


def _verse_osis_ids():
    """Every verse osisID in the three versifications that MAM-simple ships."""
    root = repo_paths.repo_root() / "MAM-simple"
    files = [
        path
        for name in ("json-vtrad-mam", "json-vtrad-bhs", "json-vtrad-sef")
        for path in sorted((root / name).glob("*.json"))
    ]
    assert files, "MAM-simple's verse lists are missing"
    verses = set()

    def collect(node):
        if isinstance(node, dict):
            osis = node.get("osisID")
            if isinstance(osis, str) and osis.count(".") == 2:
                verses.add(osis)
            for value in node.values():
                collect(value)
        elif isinstance(node, list):
            for value in node:
                collect(value)

    for path in files:
        collect(json.loads(path.read_text(encoding="utf-8")))
    assert len(verses) >= 23000, len(verses)
    return verses


def test_every_biblical_reference_names_an_existing_verse():
    """A lint: each reference that it reads names a verse MAM has.

    It reads the references in the pages' data-bk-ch-vr and data-bk-ch-vr-2 attributes
    and each source string that is wholly a reference, not a reference written only in
    a page's visible text.

    It proves that the verse exists in one of MAM-simple's versifications, not that
    the verse holds the form the adaptation cites there.
    """
    counts = Counter(ybkid for ybkid, _bkid in locales.YBKID_AND_STD_BKID_PAIRS)
    books = {
        ybkid: bkid
        for ybkid, bkid in locales.YBKID_AND_STD_BKID_PAIRS
        if counts[ybkid] == 1
    }
    references = set()
    pages = sorted(paths.pages_dir().glob("*.html"))
    assert len(pages) == 17
    for path in pages:
        document = html.fromstring(path.read_text(encoding="utf-8"))
        references.update(document.xpath("//@data-bk-ch-vr | //@data-bk-ch-vr-2"))
    source_root = repo_paths.repo_root() / "py" / "yeivin_itm"
    for path in sorted(source_root.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and _REFERENCE.fullmatch(node.value)
            ):
                references.add(node.value)
    assert len(references) >= 700, len(references)
    verses = _verse_osis_ids()
    unknown = []
    for reference in sorted(references):
        match = _REFERENCE.fullmatch(reference)
        assert match, reference
        bkid = books.get(match[1])
        osis = bkid and f"{BOOK_ABBREVS[bkid]}.{int(match[2])}.{int(match[3])}"
        if osis not in verses:
            unknown.append(reference)
    assert not unknown, unknown


def test_approved_claim_schema_matches_the_tracked_data_and_named_pins():
    data = claims.read()
    schema = json.loads(
        (paths.product_dir() / "schema/meteg-claims-v2.schema.json").read_text("utf-8")
    )
    assert set(data) == set(schema["required"]) == set(schema["properties"])
    assert schema["additionalProperties"] is False
    assert data["schema"] == schema["properties"]["schema"]["const"]
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
