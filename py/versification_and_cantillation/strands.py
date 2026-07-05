"""Pull the Hebrew example words for the versification-and-cantillation doc
straight from the upstream MAM-parsed-plus data, so the generated doc is
byte-faithful to the source (nothing hand-typed).

The Decalogue verses carry the מ:כפול (dual-trope) template, whose named params
are ["כפול","א","ב"] = (combined, taxton/lower, elyon/upper). Where the two
cantillations agree (e.g. the 4th short commandment), the text is a plain string,
not a מ:כפול. See MAM-basics/py/author_misc/mp_dualcant_common.py.
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import ws_tmpl2 as wtp

_DUALCANT = "מ:כפול"
_TAXTON = "א"  # lower / תחתון
_ELYON = "ב"  # upper / עליון


def _strand_str(unit, param):
    """The strand string of a מ:כפול unit, or None when that strand is not a plain
    string — e.g. a pisqah-be'emtsa-pasuq separator unit whose strand is a template."""
    val = wtp.template_param_val(unit, param)
    if len(val) == 1 and isinstance(val[0], str):
        return val[0]
    return None


def _cells(minirow, param):
    """The ordered 'cells' of one cantillation strand across a verse: each מ:כפול
    unit contributes its strand string; each plain text run contributes itself;
    separators and whitespace-only runs are skipped."""
    cells = []
    for wtel in minirow.EP:
        if wtp.is_template_with_name(wtel, _DUALCANT):
            strand = _strand_str(wtel, param)
            if strand is not None:
                cells.append(strand)
        elif isinstance(wtel, str) and wtel.strip():
            cells.append(wtel.strip())
    return cells


def _last_word(text):
    return text.split()[-1]


def _first_word(text):
    return text.split()[0]


def gather_examples(books_mpu):
    """Return the dict of byte-faithful Hebrew example strings the doc splices in."""
    exo = books_mpu[tbn.BK_EXODUS]["verses_plus"]
    num = books_mpu[tbn.BK_NUMBERS]["verses_plus"]

    def verse(vp, bk, chnu, vrnu):
        return vp[tbn.mk_bcvtmam(bk, chnu, vrnu)]

    tax_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _TAXTON)
    ely_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _ELYON)
    tax_203 = _cells(verse(exo, tbn.BK_EXODUS, 20, 3), _TAXTON)
    tax_205 = _cells(verse(exo, tbn.BK_EXODUS, 20, 5), _TAXTON)
    ely_2012 = _cells(verse(exo, tbn.BK_EXODUS, 20, 12), _ELYON)
    tax_2012 = _cells(verse(exo, tbn.BK_EXODUS, 20, 12), _TAXTON)
    num_261 = _cells(verse(num, tbn.BK_NUMBERS, 26, 1), _TAXTON)

    # The early split's verse (Exod 20:2) has exactly two dual-trope units:
    # unit 0 = "I am the LORD … house of bondage"; unit 1 = "no other gods … before Me".
    assert len(tax_202) == 2 and len(ely_202) == 2, (len(tax_202), len(ely_202))
    # The late split (Exod 20:12) reads as four cells in the upper cantillation.
    assert len(ely_2012) == 4, len(ely_2012)
    # Numbers 26:1 is a single chanted verse split by a mid-verse petuxah into two runs.
    assert len(num_261) == 2, len(num_261)

    return {
        # early split — boundary words of the two dual-trope units
        "early_taxton_avadim": _last_word(tax_202[0]),   # …עֲבָדִ֑ים  (etnachta, mid-verse)
        "early_taxton_panai": _last_word(tax_202[1]),    # …עַל־פָּנָֽי׃ (sof pasuq)
        "early_elyon_avadim": _last_word(ely_202[0]),    # …עֲבָדִֽים׃  (sof pasuq)
        "early_elyon_panai": _last_word(ely_202[1]),     # …עַל־פָּנַ֗י (revia, runs on)
        "early_taxton_laarets": _last_word(tax_203[-1]),  # …לָאָֽרֶץ׃ (end of MAM 20:3)
        "early_mitsvotai": _last_word(tax_205[-1]),      # …מִצְוֺתָֽי׃ (end of MAM 20:5)
        # late split — the four upper cells end in sof pasuq; the last is shared
        "late_elyon_ends": [_last_word(cell) for cell in ely_2012],
        "late_taxton_end": _last_word(tax_2012[-1]),     # …שָֽׁקֶר׃ (shared outer end)
        # Numbers 25/26
        "num_seg0": num_261[0],                          # וַיְהִ֖י אַחֲרֵ֣י הַמַּגֵּפָ֑ה
        "num_seg0_last": _last_word(num_261[0]),         # הַמַּגֵּפָ֑ה (etnachta)
        "num_seg1_first": _first_word(num_261[1]),       # וַיֹּ֤אמֶר
        "num_seg1_last": _last_word(num_261[1]),         # לֵאמֹֽר׃ (sof pasuq)
    }
