"""Pull the Hebrew example words for the versification-and-cantillation doc
straight from the upstream MAM-parsed-plus data, so the generated doc is
byte-faithful to the source (nothing hand-typed).

The Decalogue verses carry the מ:כפול (dual-trope) template, whose named params
are ["כפול","א","ב"] = (combined, taxton/lower, elyon/upper). Where the two
cantillations agree (e.g. the 4th short commandment), the text is a plain string,
not a מ:כפול. See MAM-basics/py/author_misc/mp_dualcant_common.py.
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accent_strip as has
from mb_cmn import hebrew_punctuation as hpunc
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


# Diacritic-stripping for the early-split ("taḥton / elyon / MAM / BHS") table cells.
# The table is about *where each cantillation ends its verse*, so it keeps only the
# marks that carry that signal — the cantillation accents (te'amim) and the
# accent-coupled punctuation (maqaf, sof pasuq, legarmeh) — and drops the rest (vowel
# points, dagesh, shin/sin dots, rafe, and ordinary meteg). The keep-sets and the
# silluq-vs-meteg rule live in the vendorable mb_cmn.hebrew_accent_strip kernel.
def _strip_pointing(word):
    """Reduce a byte-faithful Hebrew word to consonants + accents + accent-coupled
    punctuation. A word's U+05BD is *silluq* (an accent, kept) only when the word is
    verse-final, i.e. carries sof pasuq; otherwise every U+05BD is an ordinary meteg
    (a ga'ya, e.g. on אָנֹכִי here) and is dropped."""
    keep_meteg = has.METEG_SILLUQ if hpunc.SOPA in word else has.METEG_DROP
    return has.strip_to_accents(word, keep_meteg=keep_meteg)


def gather_examples(books_mpu):
    """Return the dict of byte-faithful Hebrew example strings the doc splices in."""
    exo = books_mpu[tbn.BK_EXODUS]["verses_plus"]
    num = books_mpu[tbn.BK_NUMBERS]["verses_plus"]

    def verse(vp, bk, chnu, vrnu):
        return vp[tbn.mk_bcvtmam(bk, chnu, vrnu)]

    tax_201 = _cells(verse(exo, tbn.BK_EXODUS, 20, 1), _TAXTON)
    tax_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _TAXTON)
    ely_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _ELYON)
    tax_203 = _cells(verse(exo, tbn.BK_EXODUS, 20, 3), _TAXTON)
    tax_204 = _cells(verse(exo, tbn.BK_EXODUS, 20, 4), _TAXTON)
    tax_205 = _cells(verse(exo, tbn.BK_EXODUS, 20, 5), _TAXTON)
    tax_2011 = _cells(verse(exo, tbn.BK_EXODUS, 20, 11), _TAXTON)
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

    def rng(first_cell, last_cell):
        """A 'firstword…lastword' range label for the early-split table, each word
        stripped to consonants + accents + accent-coupled punctuation (see
        _strip_pointing). rng feeds only that table (and its merged-cell caption),
        so stripping here leaves the surrounding byte-faithful prose untouched."""
        first = _strip_pointing(_first_word(first_cell))
        last = _strip_pointing(_last_word(last_cell))
        return f"{first}…{last}"

    return {
        # early split — boundary words of the two dual-trope units
        "early_taxton_avadim": _last_word(tax_202[0]),   # …עֲבָדִ֑ים  (etnachta, mid-verse)
        "early_taxton_panai": _last_word(tax_202[1]),    # …עַל־פָּנָֽי׃ (sof pasuq)
        "early_elyon_avadim": _last_word(ely_202[0]),    # …עֲבָדִֽים׃  (sof pasuq)
        "early_elyon_panai": _last_word(ely_202[1]),     # …עַל־פָּנַ֗י (revia, runs on)
        "early_taxton_laarets": _last_word(tax_203[-1]),  # …לָאָֽרֶץ׃ (end of MAM 20:3)
        "early_mitsvotai": _last_word(tax_205[-1]),      # …מִצְוֺתָֽי׃ (end of MAM 20:5)
        # early split — assembled first…last ranges for the overlapping-boundaries
        # table (each end-word carries its own strand's mark; the elyon "long" range
        # is the one verse that spans MAM 20:2b–20:5, past פני to מצותי)
        "early_row_201": rng(tax_201[0], tax_201[0]),
        "early_taxrow_202a": rng(tax_202[0], tax_202[0]),
        "early_elyrow_202a": rng(ely_202[0], ely_202[0]),
        "early_taxrow_202b": rng(tax_202[1], tax_202[1]),
        "early_elyrow_long": rng(ely_202[1], tax_205[-1]),
        "early_taxrow_203": rng(tax_203[0], tax_203[-1]),
        "early_taxrow_204": rng(tax_204[0], tax_204[-1]),
        "early_taxrow_205": rng(tax_205[0], tax_205[-1]),
        "early_row_2011": rng(tax_2011[0], tax_2011[0]),
        # late split — the four upper cells end in sof pasuq; the last is shared
        "late_elyon_ends": [_last_word(cell) for cell in ely_2012],
        "late_taxton_end": _last_word(tax_2012[-1]),     # …שָֽׁקֶר׃ (shared outer end)
        # Numbers 25/26
        "num_seg0": num_261[0],                          # וַיְהִ֖י אַחֲרֵ֣י הַמַּגֵּפָ֑ה
        "num_seg0_last": _last_word(num_261[0]),         # הַמַּגֵּפָ֑ה (etnachta)
        "num_seg1_first": _first_word(num_261[1]),       # וַיֹּ֤אמֶר
        "num_seg1_last": _last_word(num_261[1]),         # לֵאמֹֽר׃ (sof pasuq)
    }
