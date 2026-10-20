"""Compare the complete native FOI against the distributed MAM-simple text.

The independent MAM-simple loader supplies the corpus, while a lookahead regex
supplies pair boundaries. Exact accented atoms, repeated occurrences and vav
mark hosts must agree with the FOI's plus projection and cluster traversal.
"""

from collections import Counter
from html.parser import HTMLParser
import json
import re
import pytest

from accgram.mam_simple_verse import load_mam_simple_for_refs, mam_simple_refs
from foi import foi_struct as fct
from foi import foiz_wt_holam_before_vav as foi
from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id

_MARK = r"[\u034f\u0591-\u05bd\u05bf\u05c1\u05c2\u05c4\u05c5\u05c7-\u05c9\ufb1e]"
_ATOM = re.compile(r"[א-ת](?:[א-ת]|" + _MARK + r")*")
_PAIR = re.compile(r"(?=([א-הז-ת])(" + _MARK + r"*)ו(" + _MARK + r"*))")
_HASER_PAIR = re.compile(r"(?=(ו)(" + _MARK + r"*)ו(" + _MARK + r"*))")


def _text(node):
    if isinstance(node, str):
        return node
    if isinstance(node, (tuple, list)):
        return "".join(map(_text, node))
    return _text(node["contents"])


def test_complete_foi_matches_mam_simple():
    actual = Counter()
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    for book in books.values():
        for bcvt, minirow in book["verses_plus"].items():
            mroge = {"mroge-bcvt": bcvt, "mroge-minirow": minirow}
            for foi_path, target in foi.find_fois_wt(mroge):
                actual[
                    tbn.short_bcv_of_bcvt(bcvt),
                    _text(fct.qtar_proper(target)),
                    fct.qtar_qual(target)["vav_marks"],
                    foi_path[1],
                ] += 1

    directory = paths.repo_root() / "MAM-simple" / "json-vtrad-mam"
    simple = load_mam_simple_for_refs(directory, mam_simple_refs(directory))
    assert simple, "The independent MAM-simple corpus was empty"
    expected = Counter()
    for reference, record in simple.items():
        bb, chapter, verse = re.fullmatch(r"(.{2})(\d+):(\d+)", reference).groups()
        bcv = tbn.short_bcv((wlc_bb_to_bk39id(bb), int(chapter), int(verse)))
        for token in record["mam_simple_verse"]["vels"]:
            for atom in _ATOM.findall(token):
                for match in _PAIR.finditer(atom):
                    if hp.XOLAM in match[2] and not re.sub(_MARK, "", atom).endswith(
                        "יהוה"
                    ):
                        expected[
                            bcv,
                            atom,
                            match[3],
                            (
                                "With an above-mark on vav"
                                if set(match[3]) & ha.UNI_OVER_ACCENTS
                                else "Without an above-mark on vav"
                            ),
                        ] += 1
                for match in _HASER_PAIR.finditer(atom):
                    if hp.XOLAM_XFV in match[2]:
                        expected[
                            bcv, atom, match[3], "Holam haser for vav before vav"
                        ] += 1
    assert actual, "The FOI found no occurrences"
    assert actual == expected


@pytest.mark.parametrize(
    "atom",
    (
        "ו" + hp.XOLAM_XFV + "ה",
        "ו" + hp.XOLAM_XFV,
        "ו" + hp.XOLAM_XFV + "הו",
        "ה" + hp.XOLAM_XFV + "ו",
    ),
)
def test_haser_requires_vav_as_next_base_letter(atom):
    assert list(foi.haser_pairs(atom)) == []


def test_haser_allows_an_intervening_accent():
    atom = "ו" + hp.XOLAM_XFV + ha.REV + "ו" + hp.SEGOL_V
    assert list(foi.haser_pairs(atom)) == [(0, len(atom), hp.SEGOL_V)]


class _SpacingPage(HTMLParser):
    """Read Scripture spans in the two adjacent Hebrew cells of every row."""

    def __init__(self):
        super().__init__()
        self.examples = []
        self.current = None
        self.span_depth = 0
        self.cell_counts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "tr":
            self.cell_counts.append(0)
        if tag == "td":
            self.cell_counts[-1] += 1
        if tag == "span" and attributes.get("class") in {
            "holam-normal-spacing",
            "holam-expanded-spacing",
        }:
            self.current = [attributes["class"], ""]
            self.span_depth = 1
        elif tag == "span" and self.current is not None:
            assert attributes == {"class": "mam-doc-target-without-callout"}
            self.span_depth += 1

    def handle_data(self, text):
        if self.current is not None:
            self.current[1] += text

    def handle_endtag(self, tag):
        if tag == "span" and self.current is not None:
            self.span_depth -= 1
            if self.span_depth == 0:
                self.examples.append((self.current[0], self.current[1].strip()))
                self.current = None


def test_rendered_spacing_versions_preserve_every_occurrence():
    directory = paths.gh_pages_dir() / "MAM-with-doc" / "foi"
    rows = json.loads(
        (directory / "foi-holam-before-vav.json").read_text(encoding="utf-8")
    )
    source = (directory / "foi-holam-before-vav.html").read_text(encoding="utf-8")
    assert rows, "The generated FOI was empty"
    page = _SpacingPage()
    page.feed(source)
    assert page.examples == [
        (spacing, row["r"])
        for row in rows
        for spacing in ("holam-normal-spacing", "holam-expanded-spacing")
    ]
    assert page.cell_counts == [3] * len(rows)
    assert not any("bhl" in row for row in rows)
    assert "BHL" not in source
    assert "The marks column" not in source
    assert "Normal spacing" not in source
    assert "Expanded spacing" not in source
    assert re.search(r"\.holam-normal-spacing\s*\{\s*letter-spacing: normal;", source)
    assert re.search(r"\.holam-expanded-spacing\s*\{\s*letter-spacing: 0\.1em;", source)
