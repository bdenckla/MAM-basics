"""Pull the Hebrew example words for the versification-and-cantillation doc
straight from the upstream MAM-parsed-plus data, so the generated doc is
byte-faithful to the source (nothing hand-typed).

The Decalogue verses carry the מ:כפול (dual-trope) template, whose named params
are ["כפול","א","ב"] = (combined, taxton/lower, elyon/upper). Where the two
cantillations agree (e.g. the 4th short commandment), the text is a plain string,
not a מ:כפול. See MAM-basics/py/author_misc/mp_dualcant_common.py.
"""

from functools import partial

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accent_strip as has
from mb_cmn import hebrew_punctuation as hpunc
from mb_cmn import template_names as tmpln
from mb_cmn import ws_tmpl2 as wtp

_DUALCANT = "מ:כפול"
_TAXTON = "א"  # lower / תחתון
_ELYON = "ב"  # upper / עליון

# A ketiv/qere (כו״ק) template stores the ketiv (written form) as arg "1" and the qere
# (the pointed *read* form) as arg "2"; every strand here reads a verse the way it is
# chanted, so it always takes the qere — see _el_text and issue #199. (This matches how
# py_misc/wt_qere.py resolves the read form: recurse on the kq template's 2nd argument.)
_KQ_QERE = "2"


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
        elif isinstance(wtel, str):
            if wtel.strip():
                cells.append(wtel.strip())
        else:
            # Same gap the audit in issue #199 closed for _strand_word_text: a top-level
            # ketiv/qere is neither a מ:כפול nor a plain run, so it fell through and was silently
            # dropped, losing its word; contribute its qere instead (see _word_template_text,
            # which — like the old skip — still yields nothing for a non-word template such as a
            # נוסח petuxah wrapper, so Num 26:1 stays two cells). No current caller feeds _cells
            # a verse with a top-level kq, so this is latent-correctness only, but it keeps
            # _cells consistent with the flat word text.
            text = _word_template_text(wtel).strip()
            if text:
                cells.append(text)
    return cells


def _el_text(el):
    """Best-effort plain text of one strand element, for reading off word boundaries.
    A plain run is itself; a ketiv/qere (כו״ק) template contributes its *qere* — the
    pointed read form the cantillation strands display, never the ketiv (issue #199); a
    nested qamats (מ:קמץ) template contributes its word variant; a paseq/legarmeh separator
    contributes only a space (a word break)."""
    if isinstance(el, str):
        return el
    if wtp.is_template_with_name_in(el, tmpln.STD_KQ_TMPL_NAMES):
        return "".join(_el_text(sub) for sub in wtp.template_param_val(el, _KQ_QERE))
    if wtp.is_template(el):
        for val in wtp.template_param_vals(el):
            if len(val) == 1 and isinstance(val[0], str):
                return val[0]
        return " "
    return ""


def _word_template_text(wtel):
    """The word text a *top-level* template (one sitting directly in EP, neither a מ:כפול
    strand unit nor a plain string) contributes to a strand. Only a ketiv/qere carries one —
    its qere, the read form the strands display; issue #199 is that dropping such a top-level
    כו״ק deleted Deut 5:9's last word מִצְוֺתָֽי and left first/last-word extraction seeing the
    bare ׃ that follows it. Every other top-level template contributes no word and is dropped,
    exactly as before this branch existed: e.g. a נוסח documentation/scroll-difference wrapper
    whose payload is only a petuxah separator (Num 26:1). This is deliberately narrower than
    _el_text — routing a נוסח through _el_text's generic first-plain-string heuristic would
    wrongly splice its description text into the strand."""
    if wtp.is_template_with_name_in(wtel, tmpln.STD_KQ_TMPL_NAMES):
        return "".join(_el_text(sub) for sub in wtp.template_param_val(wtel, _KQ_QERE))
    return ""


def _strand_word_text(minirow, param):
    """The flat plain text of one cantillation strand across a whole verse, resolving
    nested strand templates (see _el_text). Unlike _cells (which yields verse-internal
    'cells' and can only take a strand that is a single plain string), this tolerates the
    nested paseq/legarmeh/qamats markup the elyon strand carries — it is used only to read
    a verse's first and last *word*, so word breaks, not exact punctuation, are what matter.
    """
    parts = []
    for wtel in minirow.EP:
        if wtp.is_template_with_name(wtel, _DUALCANT):
            parts.extend(_el_text(el) for el in wtp.template_param_val(wtel, param))
        elif isinstance(wtel, str):
            parts.append(wtel)
        else:
            # A top-level template that is *not* a dual-cant unit — most notably a ketiv/qere —
            # can still carry a word both strands read; append its qere (see _word_template_text).
            # Dropping it here silently deleted a word from the flat strand (issue #199): Deut
            # 5:9's top-level כו״ק held the verse's last word מִצְוֺתָֽי, so first/last-word
            # extraction saw the bare ׃ that follows it.
            parts.append(_word_template_text(wtel))
    return "".join(parts)


def _last_word(text):
    return text.split()[-1]


def _first_word(text):
    return text.split()[0]


# Diacritic-stripping for the early-split ("taxton / elyon / MAM / BHS") table cells.
# The table is about *where each cantillation ends its verse*, so it keeps only the
# marks that carry that signal — the cantillation accents (te'amim) and the
# accent-coupled punctuation (maqaf, sof pasuq, legarmeh) — and drops the rest (vowel
# points, dagesh, shin/sin dots, rafe, and ordinary meteg). The keep-sets and the
# silluq-vs-meteg rule live in the vendorable mb_cmn.hebrew_accent_strip kernel.
def _strip_pointing(word):
    """Reduce a byte-faithful Hebrew word to letters + accents + accent-coupled
    punctuation. A word's U+05BD is *silluq* (an accent, kept) only when the word is
    verse-final, i.e. carries sof pasuq; otherwise every U+05BD is an ordinary meteg
    (a ga'ya, e.g. on אָנֹכִי here) and is dropped."""
    keep_meteg = has.METEG_SILLUQ if hpunc.SOPA in word else has.METEG_DROP
    return has.strip_to_accents(word, keep_meteg=keep_meteg)


# The one chanted-verse coloring primitive: wrap a word in the CSS class for its role
# (start=green, stop=red, mid=neutral interior), all three defined once in the stylesheet
# so they adapt to light/dark mode. The optional ``agree`` modifier adds vc-agree, which
# washes the word out — used only by the Deuteronomy appendix's "anti-highlighting", where
# a Deut word identical to its Exodus counterpart is dimmed so the eye lands on the words
# that differ. The Exodus tables and prose need only the plain (agree=False) roles, which
# _green/_red below name; both paths share this palette, so there is no second, inline set.
def _shade(word, role, agree):
    cls = {"start": "vc-start", "stop": "vc-stop", "mid": "vc-mid"}[role]
    if agree:
        cls += " vc-agree"
    return f'<span class="{cls}">{word}</span>'


def _green(word):  # first word of a chanted verse — "start"
    return _shade(word, "start", agree=False)


def _red(word):  # last word of a chanted verse — "stop"
    return _shade(word, "stop", agree=False)


def _paint_range(first_words, last_words, *, start, stop):
    """A 'firstword(s)…lastword(s)' range label for a transposed strand table, each word
    stripped to letters + accents + accent-coupled punctuation (see _strip_pointing).

    ``first_words``/``last_words`` are the (already letter-balanced, see balanced_pair)
    word lists shown at the range's two ends — normally one word each, but two or more when
    a boundary was pulled inward to letter-match the paired strand (issue #201). Only the
    genuine chanted-verse edges carry color: the verse-initial word (``first_words[0]``)
    green when ``start``, the verse-final word (``last_words[-1]``) red when ``stop``; any
    word pulled in purely for letter-alignment renders plain."""
    fw = [_strip_pointing(w) for w in first_words]
    lw = [_strip_pointing(w) for w in last_words]
    if start:
        fw[0] = _green(fw[0])
    if stop:
        lw[-1] = _red(lw[-1])
    return f"{' '.join(fw)}…{' '.join(lw)}"


def _paint_deut_range(ex_first, ex_last, de_first_words, de_last_words, *, start, stop):
    """The Deuteronomy-appendix counterpart of _paint_range: a shaded 'first…last' range of a
    Deuteronomy chanted verse, laid against its Exodus counterpart's endpoints (ex_first,
    ex_last) so each end is marked agree/differ. Endpoints are stripped exactly as the Exodus
    tables strip them (see _strip_pointing), so "agree" means the two Decalogues' *displayed*
    forms are byte-identical — vowel-only differences, being invisible after stripping,
    correctly read as agreement, while an accent difference (which the strip keeps, because
    these tables are about accents) reads as a difference. The Deuteronomy columns are already
    letter-equal at every boundary, so ``de_*_words`` are single-word lists today; they are
    joined for symmetry with _paint_range should a future divergence ever pull a word in.
    """
    df = " ".join(_strip_pointing(w) for w in de_first_words)
    dl = " ".join(_strip_pointing(w) for w in de_last_words)
    ef, el = _strip_pointing(ex_first), _strip_pointing(ex_last)
    first = _shade(df, "start" if start else "mid", df == ef)
    last = _shade(dl, "stop" if stop else "mid", dl == el)
    return f"{first}…{last}"


# ── Letter-equalizing the paired taxton/elyon boundary cells (issue #201) ──────────────
# Each transposed table column shows one underlying text span read by both cantillation
# strands, so the two cells *should* share a letter skeleton at each boundary. They can
# still tokenize a boundary word differently — most visibly the leading לֹא of a negative
# commandment, which the taxton maqaf-joins to the next word (one token לֹא־תַעֲשֶׂה) while
# the elyon leaves free (לֹא as its own word). balanced_pair pulls extra boundary words
# inward, word by word, until the two sides' letter skeletons match, then *asserts* they
# do — a document-wide guard that fires loudly on any column it cannot reconcile (a
# reintroduced #200, a brand-new divergence, or a Numbers/Deuteronomy data change).


def _skel(word):
    """The letter skeleton of a word (or several words joined): only the Hebrew letters
    U+05D0–U+05EA, dropping points, accents, maqaf, sof pasuq and legarmeh. This — *not*
    has.strip_to_accents, which keeps maqaf and accents — is the letter-equality key of
    issue #201: a maqaf-joined לֹא־תַעֲשֶׂה and a space-separated לֹא תַעֲשֶׂה must compare
    equal. Bounds come from the hebrew_accent_strip kernel (private today; see #198)."""
    return "".join(ch for ch in word if has._LETTER_LO <= ord(ch) <= has._LETTER_HI)


def _balance_boundary(t_words, e_words, *, grow_backward, label):
    """How many boundary words each strand must show so their letter skeletons match at
    one end of a column. Compares the taxton's and elyon's leading (or, with ``grow_backward``,
    trailing) run of words; grows the shorter-skeleton side inward one word at a time while it
    stays a prefix/suffix of the longer. Returns ``(t_take, e_take)``. Raises loudly — with the
    column ``label`` and both word lists — the moment the skeletons diverge irreconcilably or a
    side runs out of words, which is the whole point of the guard."""

    def seg(words, take):
        chosen = words[-take:] if grow_backward else words[:take]
        return "".join(_skel(w) for w in chosen)

    t_take = e_take = 1
    while True:
        ts, es = seg(t_words, t_take), seg(e_words, e_take)
        if ts == es:
            return t_take, e_take
        short, long_ = (ts, es) if len(ts) < len(es) else (es, ts)
        aligned = long_.endswith(short) if grow_backward else long_.startswith(short)
        grow_t = len(ts) < len(es)
        room = (t_take < len(t_words)) if grow_t else (e_take < len(e_words))
        if not aligned or not room:
            raise AssertionError(
                f"balanced_pair: cannot letter-equalize the {label} boundary — "
                f"taxton skeleton {ts!r} vs elyon skeleton {es!r}; "
                f"taxton words={t_words!r}, elyon words={e_words!r}"
            )
        if grow_t:
            t_take += 1
        else:
            e_take += 1


def _balanced_sides(t_words, e_words, *, label):
    """Letter-balance both ends of a column. Returns the four displayed word lists
    ``(t_first, t_last, e_first, e_last)`` — each the boundary word(s) whose letter
    skeletons the taxton and elyon share, after any pulling."""
    t_first_n, e_first_n = _balance_boundary(
        t_words, e_words, grow_backward=False, label=f"{label} first-word"
    )
    t_last_n, e_last_n = _balance_boundary(
        t_words, e_words, grow_backward=True, label=f"{label} last-word"
    )
    return (
        t_words[:t_first_n],
        t_words[-t_last_n:],
        e_words[:e_first_n],
        e_words[-e_last_n:],
    )


def balanced_pair(t_words, e_words, *, label, t_render, e_render):
    """Build a column's taxton and elyon cells from their whole-span word lists, having first
    pulled each boundary inward until the two strands are letter-equal there (or raised).
    ``t_render``/``e_render`` map ``(first_words, last_words)`` to the strand's cell string —
    _paint_range for an Exodus column, _paint_deut_range (bound to its Exodus twin) for a
    Deuteronomy-appendix column. Balancing and the equality assert are inseparable: no caller
    can emit a T/E column pair without the check having passed."""
    t_first, t_last, e_first, e_last = _balanced_sides(t_words, e_words, label=label)
    return t_render(t_first, t_last), e_render(e_first, e_last)


def _verse(vp, bk, chnu, vrnu):
    return vp[tbn.mk_bcvtmam(bk, chnu, vrnu)]


def _strand_words(vp, bk, chnu, vrnu, param):
    """The flat whole-verse word list of one cantillation strand (see _strand_word_text)."""
    return _strand_word_text(_verse(vp, bk, chnu, vrnu), param).split()


def build_columns(books_mpu):
    """Every transposed-table taxton/elyon column, as a spec the balancer drives: a ``label``
    (for guard messages), the doc placeholder names ``key_t``/``key_e``, the two strands'
    whole-span word lists, and each side's cell renderer. gather_examples routes all of these
    through balanced_pair, making the letter-equality assert a document-wide guard; the
    umbrella test walks this same list. Also asserts the structural invariants (cell counts,
    Sabbath-merge span) the columns rely on."""
    exo = books_mpu[tbn.BK_EXODUS]["verses_plus"]
    deu = books_mpu[tbn.BK_DEUTER]["verses_plus"]  # for the Deuteronomy appendix
    ex, de = tbn.BK_EXODUS, tbn.BK_DEUTER

    # Early split's verse (Exod 20:2) has exactly two dual-trope units:
    # unit 0 = "I am the LORD … house of bondage"; unit 1 = "no other gods … before Me".
    tax_202 = _cells(_verse(exo, ex, 20, 2), _TAXTON)
    ely_202 = _cells(_verse(exo, ex, 20, 2), _ELYON)
    assert len(tax_202) == 2 and len(ely_202) == 2, (len(tax_202), len(ely_202))
    # The late split (Exod 20:12) and its Deut twin (5:16) each read as four cells per
    # cantillation; _cells and _strand_word_text agree for their clean single-string מ:כפול
    # units. Assert taxton/elyon stay cell-aligned so a future nested template silently
    # dropping a cell fails loudly here instead of misaligning the columns.
    tax_2012 = _cells(_verse(exo, ex, 20, 12), _TAXTON)
    ely_2012 = _cells(_verse(exo, ex, 20, 12), _ELYON)
    tax_516 = _cells(_verse(deu, de, 5, 16), _TAXTON)
    ely_516 = _cells(_verse(deu, de, 5, 16), _ELYON)
    assert len(tax_2012) == len(ely_2012) == 4, (len(tax_2012), len(ely_2012))
    assert len(tax_516) == len(ely_516) == 4, (len(tax_516), len(ely_516))
    n_late = len(tax_2012)  # 4 short commandments
    # Sabbath merge: the elyon runs unbroken (no sof pasuq) across Exod 20:7-20:9 / Deut
    # 5:11-5:13 and closes only at 20:10 / 5:14, so what each taxton reads as four verses is
    # one elyon verse. This validates the doc's merge claim (balanced_pair checks the strands'
    # letters, not the elyon span itself), and that Deut keeps Exodus's verse structure.
    for vr in (7, 8, 9):
        assert hpunc.SOPA not in _strand_word_text(_verse(exo, ex, 20, vr), _ELYON), vr
    assert hpunc.SOPA in _strand_word_text(_verse(exo, ex, 20, 10), _ELYON)
    for vr in (11, 12, 13):
        assert hpunc.SOPA not in _strand_word_text(_verse(deu, de, 5, vr), _ELYON), vr
    assert hpunc.SOPA in _strand_word_text(_verse(deu, de, 5, 14), _ELYON)

    cols = []

    def col(key_t, key_e, label, t_words, e_words, t_render, e_render):
        cols.append(
            {
                "label": label,
                "key_t": key_t,
                "key_e": key_e,
                "t_words": t_words,
                "e_words": e_words,
                "t_render": t_render,
                "e_render": e_render,
            }
        )

    R = _paint_range  # Exodus renderer: (first_words, last_words) -> cell, bound to flags
    D = _paint_deut_range  # Deut renderer: also bound to its Exodus twin's endpoints

    # Early split (Exod 20:2-20:5), five columns. The taxton reads 20:2 as one verse spanning
    # columns 202a+202b (green start on 202a, red stop on 202b); the elyon breaks after avadim,
    # so its long verse spans 202b-205 (green start on 202b's לא, red stop on 205's מצותי,
    # 203/204 wholly interior). Columns 202b and 203 are where the leading לֹא of a negative
    # commandment tokenizes differently — taxton maqaf-joins it, elyon leaves it free — so
    # balanced_pair pulls one word inward on each side there; the rest already letter-match.
    col(
        "early_taxrow_202a",
        "early_elyrow_202a",
        "early 20:2a",
        tax_202[0].split(),
        ely_202[0].split(),
        partial(R, start=True, stop=False),
        partial(R, start=True, stop=True),
    )
    col(
        "early_taxrow_202b",
        "early_elyrow_202b",
        "early 20:2b",
        tax_202[1].split(),
        ely_202[1].split(),
        partial(R, start=False, stop=True),
        partial(R, start=True, stop=False),
    )
    # 203/204/205 draw the whole-verse word list via _strand_word_text, not _cells[0]/[-1]:
    # _cells silently drops a מ:כפול unit whose strand isn't a single plain string (e.g. MAM
    # 20:4's opening clause, whose qamats-qatan carries a nested מ:קמץ template), which once
    # made 20:4's taxton cell start at כי instead of its true initial לא־תשתחוה. See #200 —
    # now guarded, since balanced_pair asserts each column's taxton/elyon are letter-equal.
    for vr, e_start, e_stop in ((3, False, False), (4, False, False), (5, False, True)):
        col(
            f"early_taxrow_20{vr}",
            f"early_elyrow_20{vr}",
            f"early 20:{vr}",
            _strand_words(exo, ex, 20, vr, _TAXTON),
            _strand_words(exo, ex, 20, vr, _ELYON),
            partial(R, start=True, stop=True),
            partial(R, start=e_start, stop=e_stop),
        )

    # Sabbath merge (Exod 20:7-20:10), transposed like the early split: each taxton cell is a
    # whole verse (green start / red stop); the elyon is one verse spanning all four — green on
    # 20:7's start, red on 20:10's end, 20:8/20:9 wholly plain. Words use _strand_word_text
    # (not _cells): 20:9's taxton strand is all nested markup, so _cells would yield nothing.
    sab_ely_flags = {
        7: (True, False),
        8: (False, False),
        9: (False, False),
        10: (False, True),
    }
    for vr, (e_start, e_stop) in sab_ely_flags.items():
        col(
            f"sab_taxrow_{vr}",
            f"sab_elyrow_{vr}",
            f"sab 20:{vr}",
            _strand_words(exo, ex, 20, vr, _TAXTON),
            _strand_words(exo, ex, 20, vr, _ELYON),
            partial(R, start=True, stop=True),
            partial(R, start=e_start, stop=e_stop),
        )

    # Late split (Exod 20:12), transposed but mirrored: here the taxton is the single verse
    # spanning all four columns (green on the first commandment's start, red on שקר, its two
    # interior cells plain) and each of the four elyon commandments is its own verse (green
    # start / red stop). tax_2012[i]/ely_2012[i] are the two strands' readings of commandment i.
    for i in range(n_late):
        col(
            f"late_taxrow_{i}",
            f"late_elyrow_{i}",
            f"late 20:12 cell {i}",
            tax_2012[i].split(),
            ely_2012[i].split(),
            partial(R, start=(i == 0), stop=(i == n_late - 1)),
            partial(R, start=True, stop=True),
        )

    # Deuteronomy appendix — Sabbath (Deut 5:11-5:14 mirrors Exod 20:7-20:10). Each Deut
    # endpoint is shaded against its Exodus twin (see _paint_deut_range): identical words wash
    # out, differing words stay full-strength, so זכור→שמור and Deut's longer text stand out
    # while ששת ימים… (5:12), which matches Exodus end-to-end, is all pale. The Deut Sabbath
    # keeps Exodus's elyon-spans-four-taxton-verses structure, so it reuses sab_ely_flags.
    for dvr in (11, 12, 13, 14):
        evr = dvr - 4  # Deut 5:v mirrors Exod 20:(v-4)
        ex_t = _strand_words(exo, ex, 20, evr, _TAXTON)
        ex_e = _strand_words(exo, ex, 20, evr, _ELYON)
        e_start, e_stop = sab_ely_flags[evr]
        col(
            f"deut_sab_taxrow_{dvr}",
            f"deut_sab_elyrow_{dvr}",
            f"deut-sab 5:{dvr}",
            _strand_words(deu, de, 5, dvr, _TAXTON),
            _strand_words(deu, de, 5, dvr, _ELYON),
            partial(D, ex_t[0], ex_t[-1], start=True, stop=True),
            partial(D, ex_e[0], ex_e[-1], start=e_start, stop=e_stop),
        )

    # Deuteronomy appendix — the same late split (Deut 5:16), shaded against its Exodus twin.
    # Deut differs in two ways here — a connective וְ on the 2nd-4th commandments (וְלֹא vs
    # Exodus's asyndetic לֹא) and the ninth's end-word (שָׁוְא vs שָׁקֶר) — so those are the
    # only forms left at full strength. (These are non-letter differences, so the columns are
    # still letter-equal taxton-to-elyon within Deut, and the pass is a no-op here.)
    for i in range(n_late):
        ex_t = tax_2012[i].split()
        ex_e = ely_2012[i].split()
        col(
            f"deut_late_taxrow_{i}",
            f"deut_late_elyrow_{i}",
            f"deut-late 5:16 cell {i}",
            tax_516[i].split(),
            ely_516[i].split(),
            partial(D, ex_t[0], ex_t[-1], start=(i == 0), stop=(i == n_late - 1)),
            partial(D, ex_e[0], ex_e[-1], start=True, stop=True),
        )

    return cols


def gather_examples(books_mpu):
    """Return the dict of byte-faithful Hebrew example strings the doc splices in. Every
    taxton/elyon table column is built through balanced_pair (see build_columns), so its
    letter-skeleton equality assert guards the whole document; the remaining keys are
    single boundary words spliced into prose captions and the Numbers table."""
    exo = books_mpu[tbn.BK_EXODUS]["verses_plus"]
    num = books_mpu[tbn.BK_NUMBERS]["verses_plus"]

    out = {}
    for c in build_columns(books_mpu):
        t_cell, e_cell = balanced_pair(
            c["t_words"],
            c["e_words"],
            label=c["label"],
            t_render=c["t_render"],
            e_render=c["e_render"],
        )
        out[c["key_t"]] = t_cell
        out[c["key_e"]] = e_cell

    # Prose-caption boundary words — single words spliced into the running text, not T/E
    # column pairs, so they are not balanced: the two dual-trope units' end-words and the
    # two MAM verse ends. Then three colored "first…last" verse abbreviations for the "not
    # contained nicely" list — the elyon's short first verse (anokhi…avadim), the taxton
    # verse it splits (anokhi…al-panai), and the elyon's long verse spanning 20:2b-20:5
    # (lo yihyeh-lkha…mitsvotai) — each rendered through _paint_range exactly like the table
    # cells, so the prose echoes the table byte-for-byte and cannot drift from the source.
    # The long verse passes its first two words: only the verse-initial lo is colored (green
    # start), the second word riding along uncolored as recognizable context.
    tax_202 = _cells(_verse(exo, tbn.BK_EXODUS, 20, 2), _TAXTON)
    ely_202 = _cells(_verse(exo, tbn.BK_EXODUS, 20, 2), _ELYON)
    tax_203 = _cells(_verse(exo, tbn.BK_EXODUS, 20, 3), _TAXTON)
    tax_205 = _cells(_verse(exo, tbn.BK_EXODUS, 20, 5), _TAXTON)
    ely_205_last = _strand_words(exo, tbn.BK_EXODUS, 20, 5, _ELYON)[-1]
    out.update(
        {
            "early_taxton_avadim": _last_word(
                tax_202[0]
            ),  # …עֲבָדִ֑ים (etnachta, mid-verse)
            "early_taxton_panai": _last_word(tax_202[1]),  # …עַל־פָּנָֽי׃ (sof pasuq)
            "early_elyon_avadim": _last_word(ely_202[0]),  # …עֲבָדִֽים׃ (sof pasuq)
            "early_elyon_panai": _last_word(
                ely_202[1]
            ),  # …עַל־פָּנַ֗י (revia, runs on)
            "early_taxton_laarets": _last_word(
                tax_203[-1]
            ),  # …לָאָֽרֶץ׃ (end of MAM 20:3)
            "early_mitsvotai": _last_word(
                tax_205[-1]
            ),  # …מִצְוֺתָֽי׃ (end of MAM 20:5)
            "early_elyon_short_verse": _paint_range(
                [_first_word(ely_202[0])],
                [_last_word(ely_202[0])],
                start=True,
                stop=True,
            ),
            "early_taxton_split_verse": _paint_range(
                [_first_word(tax_202[0])],
                [_last_word(tax_202[1])],
                start=True,
                stop=True,
            ),
            "early_elyon_long_verse": _paint_range(
                ely_202[1].split()[:2], [ely_205_last], start=True, stop=True
            ),
        }
    )

    # Numbers 25/26 — a single chanted verse split by a mid-verse petuxah into two runs.
    # Like the Exodus tables, this section is about *where each cantillation ends*, so the
    # words are shown stripped to their accent signal (letters + accents + accent-coupled
    # punctuation; see _strip_pointing) rather than fully pointed. None of these words but the
    # sof-pasuq one carries SOPA, so _strip_pointing correctly reads a U+05BD as silluq only in
    # the verse-final לֵאמֹֽר׃ and as an ordinary (dropped) meteg elsewhere.
    num_261 = _cells(_verse(num, tbn.BK_NUMBERS, 26, 1), _TAXTON)
    assert len(num_261) == 2, len(num_261)

    def _strip_seg(text):
        return " ".join(_strip_pointing(w) for w in text.split())

    out.update(
        {
            "num_seg0": _strip_seg(
                num_261[0]
            ),  # וַיְהִ֖י אַחֲרֵ֣י הַמַּגֵּפָ֑ה (three words)
            "num_seg0_last": _strip_pointing(
                _last_word(num_261[0])
            ),  # הַמַּגֵּפָ֑ה (etnachta)
            "num_seg1_first": _strip_pointing(_first_word(num_261[1])),  # וַיֹּ֤אמֶר
            "num_seg1_last": _strip_pointing(
                _last_word(num_261[1])
            ),  # לֵאמֹֽר׃ (silluq + sof pasuq)
        }
    )
    return out
