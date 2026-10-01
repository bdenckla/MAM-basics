"""Lint the complete frozen legacy mapping against the two-product URL contract.

This reads the authored manifest directly, independently of the redirect parser or
renderer. Every legacy path must belong to a named family; both pronunciation
families must cover exactly the same suffixes and retain their fixed selection.
"""

import json

from mb_cmn import paths


def test_complete_legacy_mapping_obeys_the_public_url_contract():
    manifest = paths.repo_root() / "in/phonetic_hbo_redirect_pages.json"
    pages = json.loads(manifest.read_text(encoding="utf-8"))["pages"]
    assert pages, "the frozen legacy set must not be empty"
    suffixes = {"sephardic": set(), "ashkenazic": set()}
    plain_families = {"phonetic": set(), "yeivin": set()}
    for old, target in pages.items():
        if old.startswith("tnkh/"):
            suffix = old.removeprefix("tnkh/")
            pronunciation = "sephardic"
        elif old.startswith("tnkh-ashkenaz/"):
            suffix = old.removeprefix("tnkh-ashkenaz/")
            pronunciation = "ashkenazic"
        else:
            assert "/" not in old, f"unclassified old path: {old}"
            if old.startswith("yeivin_itm") and old.endswith(".html"):
                family, prefix = "yeivin", "yeivin-itm/"
            elif old in {"index.html", "testsuites.html"} or (
                old.startswith("testsuite-") and old.endswith(".html")
            ):
                family, prefix = "phonetic", "phonetic-mam/"
            else:
                raise AssertionError(f"unclassified old path: {old}")
            assert target == {"kind": "path", "path": prefix + old}, old
            plain_families[family].add(old)
            continue
        assert target == {
            "kind": "path-with-fixed-query",
            "path": "phonetic-mam/tnkh/" + suffix,
            "query": {"pronunciation": pronunciation},
        }, old
        suffixes[pronunciation].add(suffix)
    assert suffixes["sephardic"]
    assert suffixes["sephardic"] == suffixes["ashkenazic"]
    assert all(plain_families.values())
