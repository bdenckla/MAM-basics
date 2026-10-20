"""Compare the complete native FOI against the distributed MAM-simple text.

The independent MAM-simple loader supplies the corpus, while a lookahead regex
supplies pair boundaries. Exact accented atoms, repeated occurrences and vav
mark hosts must agree with the FOI's plus projection and cluster traversal.
"""

from collections import Counter
import re

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
                    foi_path[1] == "With an above-mark on vav",
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
                if re.sub(_MARK, "", atom).endswith("יהוה"):
                    continue
                for match in _PAIR.finditer(atom):
                    if hp.XOLAM in match[2]:
                        expected[
                            bcv,
                            atom,
                            match[3],
                            bool(set(match[3]) & ha.UNI_OVER_ACCENTS),
                        ] += 1
    assert actual, "The FOI found no occurrences"
    assert actual == expected
