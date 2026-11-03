"""Lint the tracked scan-pages indexes. See doc/scan-pages.md.

This is the mechanical-lint shape the repo's test rules allow: a decidable property of
tracked data, checked against an independent derivation of the same fact, with no
hand-picked example pinned anywhere.  It needs no scans folder -- the indexes are
self-contained -- but it does need MAM-parsed, and it FAILS rather than skips without
it, per the repo's missing-input rule.
"""

from scan_pages import check
from scan_pages import editions
from scan_pages import index_io
from scan_pages import lookup
from scan_pages import text
from mb_cmn import paths
from mb_cmn import mam_simple_json
from accgram import mam_simple_verse
from mb_misc import osis_book_abbrevs
import re


def test_tracked_indexes_pass_every_lint():
    """Every check in scan_pages.check, over all five tracked indexes."""
    counts = check.check_all()
    # Guard against a green run that verified nothing: the five indexes exist and hold
    # thousands of pages, so a run reporting a handful means the data went missing.
    assert counts["editions"] == len(editions.ALL_EDITION_IDS)
    assert counts["pages"] > 5000, counts


def test_every_edition_has_a_tracked_index():
    """A new edition must arrive with its index, not merely with its folder name."""
    for edition_id in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition_id)
        assert index["edition"] == edition_id
        assert index["pages"], edition_id


def test_censused_books_agree_with_independent_simple_export():
    """Compare every adopted book's atom stream with the separate simple product."""
    checked = set()
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for segment in index["segments"]:
            for book in segment["bkids"]:
                if book in checked:
                    continue
                simple_path = mam_simple_verse.mam_simple_json_path(
                    paths.repo_root() / "MAM-simple" / "json-vtrad-mam", book
                )
                root = mam_simple_json.read_book_group(simple_path)
                expected = {}
                prefix = osis_book_abbrevs.BOOK_ABBREVS[book] + "."
                for verse in mam_simple_json.verses(root):
                    if not verse["osisID"].startswith(prefix):
                        continue
                    _, c, v = verse["osisID"].split(".")
                    # The separate export carries its chosen main form explicitly.
                    if "text" in verse:
                        source_text = verse["text"]
                    else:
                        parts = []
                        for node in verse["contents"]:
                            if node["type"] in {"text", "kq-trivial"}:
                                parts.append(node["text"])
                            elif node["type"] == "slh-word":
                                for child in node["contents"]:
                                    assert child["type"] in {
                                        "text",
                                        "letter-small",
                                        "letter-large",
                                    }
                                    parts.append(child["text"])
                            elif node["type"] == "kq":
                                assert sorted(
                                    child["type"] for child in node["contents"]
                                ) == ["kq-k", "kq-q"]
                                qere = next(
                                    child
                                    for child in node["contents"]
                                    if child["type"] == "kq-q"
                                )
                                parts.append(qere["text"])
                            elif node["type"] == "good-ending":
                                assert set(node) == {"type", "text"}
                                assert isinstance(node["text"], str)
                                # The maintained simple reader excludes the
                                # repeated ending from the final verse's atoms.
                                parts.append(" ")
                            else:
                                assert node in (
                                    {"type": "lp-legarmeih"},
                                    {"type": "lp-paseq"},
                                    {"type": "spi-pe2"},
                                )
                                parts.append(" ")
                        source_text = "".join(parts)
                    expected[int(c), int(v)] = tuple(
                        letters
                        for token in re.split(r"[\s־]+", source_text)
                        if (letters := "".join(ch for ch in token if "א" <= ch <= "ת"))
                    )
                assert expected == text.book_atoms(book), (edition, book)
                checked.add(book)
    assert checked, "No adopted book was cross-checked"


def test_every_record_edge_resolves_to_its_observed_page():
    """Each handwritten source cue is an independent oracle for public lookup."""
    count = 0
    for edition in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition)
        for rec in index["recs"]:
            if rec["stopc"] is None:
                continue
            for end in ("start", "stop"):
                first, _ = text.locate_phrase_span(
                    text.book_atoms(rec["bkid"]),
                    rec[f"{end}c"],
                    rec[f"{end}v"],
                    rec[f"{end}_phrase"],
                    anchor=end,
                )
                hits = lookup.resolve(
                    index,
                    rec["bkid"],
                    first[0],
                    first[1],
                    rec[f"{end}_phrase"],
                )
                assert [hit["page"] for hit in hits] == [rec["page"]]
                count += 1
    assert count, "No observed page edges were queried"
