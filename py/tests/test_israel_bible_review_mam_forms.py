"""Lint: every MAM form that the review of the Israel Bible shows occurs in MAM-simple.

Ben's decision of 2026-11-10: MAM's forms on the page
gh-pages/israel-bible-review/index.html are "Stored as quotations and checked".
They are stored in in/israel-bible-review/forms.json (the tour's 43 rows whose notes
py/author_misc/israel_bible_review_index.py holds) and in in/israel-bible-review/review.md's
two data tables (the tour's rows whose notes are Markdown, and the Decalogues' rows).  This lint
checks each of them against MAM-simple, the tracked extract of MAM's text: the form, stripped
as the page strips it (the module's own stripped), must occur in MAM-simple's text of its
verse, stripped alike, beginning and ending at the boundaries of atoms.  A miss fails, naming
the row.  A missing input fails, and so does an empty one: forms() and data_table_rows raise
on a missing file or table, and each of the three sources must yield rows.

THE VERSE'S TEXT is read as MAM-simple's consumer notice asks
(gh-pages/MAM-simple/reading-mam-simple.html, "Consumer notice"):

* from the book group's file in the BHS versification, falling back to the MAM folder by the
  incremental-folder rule (mb_cmn.mam_simple_book_group).  The page's verses are the Israel
  Bible's, whose text is WLC's (review.md), and WLC's references take BHS's versification, as
  for this repository's surveys of them (mb_cmn.paths.mam_simple_dir).  At the early
  Decalogues, for example, the page's Exod 20:3 and Deut 5:7 are BHS's, where MAM's own
  numbering has 20:2 and 5:6;
* by explicit dispatch on every element type that MAM-simple documents
  (gh-pages/MAM-simple/reading-mam-simple-json.html), raising on any other;
* choosing one branch of each alternative: of a dual cantillation, the strand the page shows,
  and of a scroll-difference note, its target alone.  The page's Decalogue table shows
  MAM's עליון strand (its MAM column says so), which MAM-simple has as cant-bet, the תחתון
  being cant-alef (reading-mam-simple-json.html, "Dual cantillation").  A row elsewhere
  declares no strand, so a dual cantillation in its verse raises;
* with every ketiv/qere pair read on one side throughout: the ketiv, written words, or the
  qere, read ones.  The notice lets an edition show either, and a row's form may be either: a
  word written but not read is a ketiv, and 2 Kings 18:27's form is a qere.  A row passes if
  its form occurs in either reading;
* with an element that has no text supplying what the notice says it stands for: a legarmeh
  or a paseq its mark, which the page strips, a gray maqaf a maqaf, and a parashah break or a
  song's space a space, so that no two atoms fuse;
* byte for byte, since MAM-simple keeps MAM-normal mark order, as forms.json and review.md do.

The rows that the page shows with a rafeh on an alef, the module's RAFEH_REFS, are stripped
with that rafeh kept, form and verse alike, as the page strips them.
"""

import re

from author_misc import israel_bible_review_index as ib_review
from mb_cmn import mam_simple_json
from mb_cmn import paths
from mb_cmn.mam_simple_book_group import resolve_book_group_path
from mb_misc import osis_book_abbrevs as oba

_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
_PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
_NUN_HAFUKHA = "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
_VTRAD = "bhs"
_SIDES = ("ketiv", "qere")
# MAM-simple's strand of the page's Decalogue table, its עליון.
_DECALOGUE_STRAND = "cant-bet"
_CANT_STRANDS = ("cant-combined", "cant-alef", "cant-bet")
# The page's short book names, as its Where column has them, are OSIS's with no space; checked
# for every book in test_every_short_book_name_is_an_osis_book.
_OSIS = {short: short.replace(" ", "") for short in ib_review.SHORT.values()}


def test_every_short_book_name_is_an_osis_book():
    unknown = sorted(osis for osis in _OSIS.values() if osis not in oba.BK39ID_FROM_OBA)
    assert len(_OSIS) == 39 and not unknown, unknown


def _rows():
    """Every MAM form the page shows, as (row, short book name, chapter, verse, form, whether
    to keep its rafeh, strand)."""
    lines = ib_review.review_lines()
    assert ib_review.DECALOGUE_ROW_HEADERS[3] == f"MAM's {ib_review.ELYON}", (
        "the Decalogue table no longer shows MAM's עליון; choose its strand anew",
        ib_review.DECALOGUE_ROW_HEADERS,
    )
    rows = []
    json_rows = ib_review.forms()
    assert json_rows, "forms.json holds no rows"
    for row in json_rows:
        book, chapter, verse = ib_review.bcv(row["reference"])
        keep = row["reference"] in ib_review.RAFEH_REFS
        where = f"forms.json, {row['reference']}"
        rows.append(
            (where, ib_review.SHORT[book], chapter, verse, row["mam"], keep, None)
        )
    for headers, table_name, strand in (
        (ib_review.TOUR_ROW_HEADERS, "the tour's data table", None),
        (
            ib_review.DECALOGUE_ROW_HEADERS,
            "the Decalogues' data table",
            _DECALOGUE_STRAND,
        ),
    ):
        body = ib_review.data_table_rows(lines, headers)
        assert body, f"review.md's {table_name} has no rows"
        for k, cells in enumerate(body, 1):
            m = re.fullmatch(r"(.+) (\d+):(\d+)", cells[0])
            assert m and m.group(1) in _OSIS, (table_name, cells[0])
            where = f"review.md, {table_name}, row {k}, {cells[0]}"
            book, chapter, verse = m.group(1), int(m.group(2)), int(m.group(3))
            # The page strips every rafeh from the forms of review.md's tables (data_items).
            rows.append((where, book, chapter, verse, cells[3], False, strand))
    return rows


_BOOK_GROUPS = {}


def _verse(short_book, chapter, verse):
    """MAM-simple's verse, in the BHS versification."""
    osis = _OSIS[short_book]
    bk39id = oba.BK39ID_FROM_OBA[osis]
    (group,) = oba.bk24_bkgs([bk39id])
    path = resolve_book_group_path(
        paths.repo_root() / "MAM-simple",
        fmt="json",
        vtrad=_VTRAD,
        stems=(group["bkg-name"],),
    )
    if path not in _BOOK_GROUPS:
        root = mam_simple_json.read_book_group(path)
        _BOOK_GROUPS[path] = {v["osisID"]: v for v in mam_simple_json.verses(root)}
    osis_id = f"{osis}.{chapter}.{verse}"
    assert osis_id in _BOOK_GROUPS[path], (osis_id, path)
    return _BOOK_GROUPS[path][osis_id]


def _own_text(node, side, strand, where):
    """A node's text: its text field, or its children's text in order."""
    attrs = mam_simple_json.attributes(node)
    if "text" in attrs:
        return attrs["text"]
    return "".join(
        _text(child, side, strand, where) for child in mam_simple_json.children(node)
    )


def _only_child(node, kind, where):
    matches = [c for c in mam_simple_json.children(node) if c["type"] == kind]
    assert len(matches) == 1, (where, node["type"], kind)
    return matches[0]


def _text(node, side, strand, where):
    """What one element contributes to its verse's text, read on `side` of every ketiv/qere
    pair and in `strand` of a dual cantillation.  Closed dispatch on MAM-simple's documented
    element types."""
    kind = node["type"]
    attrs = mam_simple_json.attributes(node)
    if kind in ("text", "silluq-before-meteg"):
        return attrs["text"]
    if kind in ("kq-trivial", "sdt-target", "kq-k", "kq-q", *_CANT_STRANDS):
        return _own_text(node, side, strand, where)
    if kind == "lp-legarmeih":
        return _PASEQ
    if kind == "lp-paseq":
        # MAM encodes no space on either side of a narrow-sense paseq.
        return f" {_PASEQ} "
    if kind == "implicit-maqaf":
        return _MAQAF
    if kind == "kq":
        kids = [c["type"] for c in mam_simple_json.children(node)]
        assert sorted(kids) == ["kq-k", "kq-q"], (where, kids)
        chosen = "kq-k" if side == "ketiv" else "kq-q"
        return _own_text(_only_child(node, chosen, where), side, strand, where)
    if kind == "kq-k-velo-q":
        return attrs["text"] if side == "ketiv" else " "
    if kind == "kq-k-velo-q-maq":
        return _MAQAF if side == "ketiv" else ""
    if kind == "kq-q-velo-k":
        return attrs["text"] if side == "qere" else " "
    if kind == "slh-word":
        return attrs["slhw-desc-0"]
    if kind == "scrdfftar":
        return _own_text(_only_child(node, "sdt-target", where), side, strand, where)
    if kind == "cant-all-three":
        kids = [c["type"] for c in mam_simple_json.children(node)]
        assert kids == list(_CANT_STRANDS), (where, kids)
        if strand is None:
            raise ValueError(f"{where}: a dual cantillation, and the row has no strand")
        return _own_text(_only_child(node, strand, where), side, strand, where)
    if kind in ("shirah-space", "spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"):
        return " "
    if kind == "spi-invnun":
        trailing = attrs.get("class") == "including-trailing-space"
        return _NUN_HAFUKHA + (" " if trailing else "")
    if kind == "good-ending":
        # A repetition added after the book's last verse, not its running text.
        return ""
    raise ValueError(f"{where}: unhandled MAM-simple element {kind!r}")


def _verse_text(verse, side, strand, where):
    attrs = mam_simple_json.attributes(verse)
    if "text" in attrs:
        return attrs["text"]
    return "".join(
        _text(child, side, strand, where) for child in mam_simple_json.children(verse)
    )


def _occurs_at_atoms(form, text):
    """Whether form occurs in text beginning and ending at the boundaries of atoms."""
    for m in re.finditer(re.escape(form), text):
        before = text[m.start() - 1] if m.start() else " "
        after = text[m.end()] if m.end() < len(text) else " "
        if before in (" ", _MAQAF) and (
            form.endswith(_MAQAF) or after in (" ", _MAQAF)
        ):
            return True
    return False


def test_every_mam_form_occurs_in_mam_simple():
    rows = _rows()
    misses = []
    for where, book, chapter, verse, form, keep, strand in rows:
        node = _verse(book, chapter, verse)
        shown = ib_review.stripped(form, keep)
        assert shown, where
        texts = [
            ib_review.stripped(_verse_text(node, side, strand, where), keep)
            for side in _SIDES
        ]
        if not any(_occurs_at_atoms(shown, text) for text in texts):
            misses.append(f"{where}: {shown}")
    assert not misses, (
        "MAM forms on the review of the Israel Bible that MAM-simple's text of their verse"
        " does not have: " + "; ".join(misses)
    )
