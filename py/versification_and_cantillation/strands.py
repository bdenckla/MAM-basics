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


def _el_text(el):
    """Best-effort plain text of one strand element, for reading off word boundaries.
    A plain run is itself; a nested qamats (מ:קמץ) template contributes its word
    variant; a paseq/legarmeh separator contributes only a space (a word break)."""
    if isinstance(el, str):
        return el
    if wtp.is_template(el):
        for val in wtp.template_param_vals(el):
            if len(val) == 1 and isinstance(val[0], str):
                return val[0]
        return " "
    return ""


def _strand_word_text(minirow, param):
    """The flat plain text of one cantillation strand across a whole verse, resolving
    nested strand templates (see _el_text). Unlike _cells (which yields verse-internal
    'cells' and can only take a strand that is a single plain string), this tolerates the
    nested paseq/legarmeh/qamats markup the elyon strand carries — it is used only to read
    a verse's first and last *word*, so word breaks, not exact punctuation, are what matter."""
    parts = []
    for wtel in minirow.EP:
        if wtp.is_template_with_name(wtel, _DUALCANT):
            parts.extend(_el_text(el) for el in wtp.template_param_val(wtel, param))
        elif isinstance(wtel, str):
            parts.append(wtel)
    return "".join(parts)


def _last_word(text):
    return text.split()[-1]


def _first_word(text):
    return text.split()[0]


def _green(word):  # first word of a chanted verse — "start"
    return f'<span style="color:green">{word}</span>'


def _red(word):  # last word of a chanted verse — "stop"
    return f'<span style="color:red">{word}</span>'


# Diacritic-stripping for the early-split ("taxton / elyon / MAM / BHS") table cells.
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


# Deuteronomy-appendix coloring. The document's main tables are Exodus-only; the appendix
# re-shows the Sabbath and late-split points with Deuteronomy's own words, "anti-
# highlighting" every word that is identical to its Exodus counterpart (a washed-out CSS
# variant) so the eye lands on the words that differ. Hue still encodes chanted-verse role
# (start=green, stop=red, interior=neutral); the .vc-* rules live in the stylesheet.
def _shade(word, role, agree):
    cls = {"start": "vc-start", "stop": "vc-stop", "mid": "vc-mid"}[role]
    if agree:
        cls += " vc-agree"
    return f'<span class="{cls}">{word}</span>'


def _deut_range(ex_ends, de_ends, *, start, stop):
    """A shaded 'first…last' range of a Deuteronomy chanted verse, laid against its Exodus
    counterpart's endpoints (ex_ends) so each end can be marked agree/differ. Endpoints are
    stripped exactly as the Exodus tables strip them (see _strip_pointing), so "agree" means
    the two Decalogues' *displayed* forms are byte-identical — vowel-only differences, being
    invisible after stripping, correctly read as agreement, while an accent difference (which
    the strip keeps, because these tables are about accents) reads as a difference."""
    (ex_first, ex_last), (de_first, de_last) = ex_ends, de_ends
    ef, el = _strip_pointing(ex_first), _strip_pointing(ex_last)
    df, dl = _strip_pointing(de_first), _strip_pointing(de_last)
    first = _shade(df, "start" if start else "mid", df == ef)
    last = _shade(dl, "stop" if stop else "mid", dl == el)
    return f"{first}…{last}"


def gather_examples(books_mpu):
    """Return the dict of byte-faithful Hebrew example strings the doc splices in."""
    exo = books_mpu[tbn.BK_EXODUS]["verses_plus"]
    num = books_mpu[tbn.BK_NUMBERS]["verses_plus"]
    deu = books_mpu[tbn.BK_DEUTER]["verses_plus"]  # for the Deuteronomy appendix

    def verse(vp, bk, chnu, vrnu):
        return vp[tbn.mk_bcvtmam(bk, chnu, vrnu)]

    tax_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _TAXTON)
    ely_202 = _cells(verse(exo, tbn.BK_EXODUS, 20, 2), _ELYON)
    tax_203 = _cells(verse(exo, tbn.BK_EXODUS, 20, 3), _TAXTON)
    tax_204 = _cells(verse(exo, tbn.BK_EXODUS, 20, 4), _TAXTON)
    tax_205 = _cells(verse(exo, tbn.BK_EXODUS, 20, 5), _TAXTON)

    # The elyon reading of the three interior verses. Unlike the taxton strand, the
    # elyon strand of these verses carries nested paseq/legarmeh/qamats templates, so
    # _cells can't grab it as a plain cell; _strand_word_text flattens the whole verse's
    # elyon strand to read off its first and last *word*. The long elyon verse runs
    # mid-verse through 20:3–20:4 (no sof pasuq) and ends only at 20:5's מצותי.
    def strand_ends(vrnu, param):
        words = _strand_word_text(verse(exo, tbn.BK_EXODUS, 20, vrnu), param).split()
        return words[0], words[-1]

    def ely_ends(vrnu):
        return strand_ends(vrnu, _ELYON)

    def deut_strand_ends(vrnu, param):
        """strand_ends for the Deuteronomy Decalogue (chapter 5). The Deut counterpart of
        Exodus 20:v is Deut 5:(v+4), but the appendix's Sabbath verses are addressed by
        their own Deut numbers (5:11–5:14), so this takes the concrete Deut verse."""
        words = _strand_word_text(verse(deu, tbn.BK_DEUTER, 5, vrnu), param).split()
        return words[0], words[-1]

    ely_203_first, ely_203_last = ely_ends(3)
    ely_204_first, ely_204_last = ely_ends(4)
    ely_205_first, ely_205_last = ely_ends(5)
    ely_2012 = _cells(verse(exo, tbn.BK_EXODUS, 20, 12), _ELYON)
    tax_2012 = _cells(verse(exo, tbn.BK_EXODUS, 20, 12), _TAXTON)
    num_261 = _cells(verse(num, tbn.BK_NUMBERS, 26, 1), _TAXTON)
    # Deuteronomy appendix, late split: Deut 5:16 mirrors Exod 20:12.
    ely_516_deut = _cells(verse(deu, tbn.BK_DEUTER, 5, 16), _ELYON)
    tax_516_deut = _cells(verse(deu, tbn.BK_DEUTER, 5, 16), _TAXTON)

    # The early split's verse (Exod 20:2) has exactly two dual-trope units:
    # unit 0 = "I am the LORD … house of bondage"; unit 1 = "no other gods … before Me".
    assert len(tax_202) == 2 and len(ely_202) == 2, (len(tax_202), len(ely_202))
    # The late split (Exod 20:12) reads as four cells in the upper cantillation.
    assert len(ely_2012) == 4, len(ely_2012)
    # The Deuteronomy late split (5:16) shares that structure — four upper cells.
    assert len(ely_516_deut) == 4, len(ely_516_deut)
    # Numbers 26:1 is a single chanted verse split by a mid-verse petuxah into two runs.
    assert len(num_261) == 2, len(num_261)
    # Sabbath merge: the elyon runs unbroken across 20:7-20:9 (no sof pasuq) and closes
    # only at 20:10, so what the taxton reads as four verses is one elyon verse.
    for _sab in (7, 8, 9):
        assert hpunc.SOPA not in _strand_word_text(
            verse(exo, tbn.BK_EXODUS, 20, _sab), _ELYON
        ), _sab
    assert hpunc.SOPA in _strand_word_text(verse(exo, tbn.BK_EXODUS, 20, 10), _ELYON)
    # The Deuteronomy Sabbath merges the same way: the elyon runs unbroken across
    # 5:11-5:13 (no sof pasuq) and closes only at 5:14. This validates the appendix's
    # claim that Deut's much longer Sabbath keeps Exodus's taxton/elyon verse structure.
    for _sabd in (11, 12, 13):
        assert hpunc.SOPA not in _strand_word_text(
            verse(deu, tbn.BK_DEUTER, 5, _sabd), _ELYON
        ), _sabd
    assert hpunc.SOPA in _strand_word_text(verse(deu, tbn.BK_DEUTER, 5, 14), _ELYON)

    def _range(first_word, last_word, *, start, stop):
        """A 'firstword…lastword' range label for the early-split table, each word
        stripped to consonants + accents + accent-coupled punctuation (see
        _strip_pointing). It feeds only that table (and its prose caption), so stripping
        here leaves the surrounding byte-faithful prose untouched.

        ``start``/``stop`` color the range's endpoints as a chanted verse's first
        (green) and last (red) word. Suppress an endpoint (start=False / stop=False)
        when the range is only part of a chanted verse, or wholly interior to one."""
        first = _strip_pointing(first_word)
        last = _strip_pointing(last_word)
        if start:
            first = _green(first)
        if stop:
            last = _red(last)
        return f"{first}…{last}"

    def rng(first_cell, last_cell, *, start=True, stop=True):
        """`_range` over a first cell's first word and a last cell's last word."""
        return _range(_first_word(first_cell), _last_word(last_cell), start=start, stop=stop)

    def cell_ends(cell):
        return _first_word(cell), _last_word(cell)

    # Late split (Exod 20:12), transposed like the Sabbath table but with the roles
    # mirrored. There, the taxton read four verses and the elyon was the one spanning
    # verse; here the taxton is the single spanning verse (green on the first
    # commandment's start, red on שקר, its two interior cells plain) and each of the
    # four elyon commandments is its own verse (green start / red stop). The four
    # columns are those commandments in scripture order; tax_2012[i]/ely_2012[i] are the
    # two strands' readings of commandment i, so each column shows both. The four upper
    # verses all close in sof pasuq; the last shares its שקר with the taxton's outer end.
    n_late = len(ely_2012)  # 4 short commandments
    late_taxrows = {
        f"late_taxrow_{i}": rng(c, c, start=(i == 0), stop=(i == n_late - 1))
        for i, c in enumerate(tax_2012)
    }
    late_elyrows = {f"late_elyrow_{i}": rng(c, c) for i, c in enumerate(ely_2012)}
    # Deuteronomy appendix — the same late split (Deut 5:16), shaded against its Exodus
    # twin like the appendix Sabbath (see _deut_range): words matching Exodus wash out,
    # words that differ stay full strength. Deut differs in two ways here — a connective
    # וְ on the 2nd–4th commandments (וְלֹא vs Exodus's asyndetic לֹא) and the ninth's
    # end-word (שָׁוְא vs שָׁקֶר) — so those are the only forms left at full strength.
    deut_late_taxrows = {
        f"deut_late_taxrow_{i}": _deut_range(
            cell_ends(ex), cell_ends(de), start=(i == 0), stop=(i == n_late - 1)
        )
        for i, (ex, de) in enumerate(zip(tax_2012, tax_516_deut))
    }
    deut_late_elyrows = {
        f"deut_late_elyrow_{i}": _deut_range(cell_ends(ex), cell_ends(de), start=True, stop=True)
        for i, (ex, de) in enumerate(zip(ely_2012, ely_516_deut))
    }

    return {
        # early split — boundary words of the two dual-trope units
        "early_taxton_avadim": _last_word(tax_202[0]),   # …עֲבָדִ֑ים  (etnachta, mid-verse)
        "early_taxton_panai": _last_word(tax_202[1]),    # …עַל־פָּנָֽי׃ (sof pasuq)
        "early_elyon_avadim": _last_word(ely_202[0]),    # …עֲבָדִֽים׃  (sof pasuq)
        "early_elyon_panai": _last_word(ely_202[1]),     # …עַל־פָּנַ֗י (revia, runs on)
        "early_taxton_laarets": _last_word(tax_203[-1]),  # …לָאָֽרֶץ׃ (end of MAM 20:3)
        "early_mitsvotai": _last_word(tax_205[-1]),      # …מִצְוֺתָֽי׃ (end of MAM 20:5)
        # early split — assembled first…last ranges for the overlapping-boundaries
        # table. Each end-word carries its own strand's mark, and the first/last word
        # of a chanted verse is colored green (start) / red (stop). A verse that spans
        # multiple table rows colors only its outer endpoints (interior rows plain):
        #  - taxton 20:2 spans rows 202a+202b: green on 202a's start, red on 202b's end.
        #  - the long elyon verse spans rows 202b–205: green on 202b's start (לא), red on
        #    205's end (מצותי); rows 203/204 are wholly interior, so entirely plain.
        "early_taxrow_202a": rng(tax_202[0], tax_202[0], stop=False),
        "early_elyrow_202a": rng(ely_202[0], ely_202[0]),
        "early_taxrow_202b": rng(tax_202[1], tax_202[1], start=False),
        "early_elyrow_202b": rng(ely_202[1], ely_202[1], stop=False),
        "early_elyrow_203": _range(ely_203_first, ely_203_last, start=False, stop=False),
        "early_elyrow_204": _range(ely_204_first, ely_204_last, start=False, stop=False),
        "early_elyrow_205": _range(ely_205_first, ely_205_last, start=False, stop=True),
        # plain (uncolored) label spliced into the prose caption for the long elyon verse
        "early_elyrow_long": _range(
            _first_word(ely_202[1]), ely_205_last, start=False, stop=False
        ),
        "early_taxrow_203": rng(tax_203[0], tax_203[-1]),
        "early_taxrow_204": rng(tax_204[0], tax_204[-1]),
        "early_taxrow_205": rng(tax_205[0], tax_205[-1]),
        # Sabbath merge, transposed like the early-split table: the taxton row's four
        # cells are each a whole verse (green start / red stop); the elyon row is one
        # verse spanning all four — green on 20:7's start, red on 20:10's end, the two
        # interior cells (20:8, 20:9) wholly plain. Words use _strand_word_text (not
        # _cells): 20:9's taxton strand is all nested markup, so _cells yields nothing.
        "sab_taxrow_7": _range(*strand_ends(7, _TAXTON), start=True, stop=True),
        "sab_taxrow_8": _range(*strand_ends(8, _TAXTON), start=True, stop=True),
        "sab_taxrow_9": _range(*strand_ends(9, _TAXTON), start=True, stop=True),
        "sab_taxrow_10": _range(*strand_ends(10, _TAXTON), start=True, stop=True),
        "sab_elyrow_7": _range(*strand_ends(7, _ELYON), start=True, stop=False),
        "sab_elyrow_8": _range(*strand_ends(8, _ELYON), start=False, stop=False),
        "sab_elyrow_9": _range(*strand_ends(9, _ELYON), start=False, stop=False),
        "sab_elyrow_10": _range(*strand_ends(10, _ELYON), start=False, stop=True),
        # (The Sabbath table's MAM/BHS number rows — MAM 20:7–20:10, BHS 20:8–20:11 — are
        # static Exodus verse numbers, so they are hardcoded in the table template.)
        # late split — the taxton spanning verse and the four upper commandments (built above)
        **late_taxrows,
        **late_elyrows,
        # Deuteronomy appendix — Sabbath (Deut 5:11-5:14 mirrors Exod 20:7-20:10), each
        # Deut endpoint shaded against its Exodus twin (see _deut_range): identical words
        # wash out, differing words stay full-strength, so זכור→שמור and Deut's longer text
        # stand out while ששת ימים… (5:12), which matches Exodus end-to-end, is all pale.
        "deut_sab_taxrow_11": _deut_range(strand_ends(7, _TAXTON), deut_strand_ends(11, _TAXTON), start=True, stop=True),
        "deut_sab_taxrow_12": _deut_range(strand_ends(8, _TAXTON), deut_strand_ends(12, _TAXTON), start=True, stop=True),
        "deut_sab_taxrow_13": _deut_range(strand_ends(9, _TAXTON), deut_strand_ends(13, _TAXTON), start=True, stop=True),
        "deut_sab_taxrow_14": _deut_range(strand_ends(10, _TAXTON), deut_strand_ends(14, _TAXTON), start=True, stop=True),
        "deut_sab_elyrow_11": _deut_range(strand_ends(7, _ELYON), deut_strand_ends(11, _ELYON), start=True, stop=False),
        "deut_sab_elyrow_12": _deut_range(strand_ends(8, _ELYON), deut_strand_ends(12, _ELYON), start=False, stop=False),
        "deut_sab_elyrow_13": _deut_range(strand_ends(9, _ELYON), deut_strand_ends(13, _ELYON), start=False, stop=False),
        "deut_sab_elyrow_14": _deut_range(strand_ends(10, _ELYON), deut_strand_ends(14, _ELYON), start=False, stop=True),
        # Deuteronomy appendix — late split (Deut 5:16), taxton and elyon rows (built above)
        **deut_late_taxrows,
        **deut_late_elyrows,
        # Numbers 25/26
        "num_seg0": num_261[0],                          # וַיְהִ֖י אַחֲרֵ֣י הַמַּגֵּפָ֑ה
        "num_seg0_last": _last_word(num_261[0]),         # הַמַּגֵּפָ֑ה (etnachta)
        "num_seg1_first": _first_word(num_261[1]),       # וַיֹּ֤אמֶר
        "num_seg1_last": _last_word(num_261[1]),         # לֵאמֹֽר׃ (sof pasuq)
    }
