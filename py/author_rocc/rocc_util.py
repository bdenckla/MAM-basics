from mb_author import author
from mb_misc import mb_html
from mb_misc import ws_urls


def aeq(edition):
    return "$almost_equal_to$thinsp" + edition


def eq(edition):
    return "=$thinsp" + edition


def edition_kct_full():
    return "Koren Classic Tanakh"


def edition_jp_full():
    return "Judaica Press Mikraoth Gedoloth: Psalms: Volume 1"


def edition_wmg_full():
    return ["Warsaw Miqraot Gedolot, 1874 ", _anc_ia(_IA_URL_WMG)]


def edition_sbb_full():
    return ["Soncino Books of the Bible: The Psalms ", _anc_ia(_IA_URL_SBB)]


def gray_abg_njvy(normal_part, whbo=True):
    return _gray_10("נשוי־", normal_part, whbo)


def gray_abg_al(normal_part, whbo=True):
    return _gray_10("אל־", normal_part, whbo)


def gray_abg_adm(normal_part, whbo=True):
    return _gray_01(normal_part, "אדם", whbo)


def gray_abg_hxrjty(normal_part, whbo=True):
    return _gray_01(normal_part, "החרשתי", whbo)


def gray_abg_yxjb(normal_part, whbo=True):
    return _gray_01(normal_part, "יחשב", whbo)


def to_encode(mark_or_marks, prep, letter, ccv, s_word, f_word):
    """
    prep: preposition, e.g. "under" preceding the letter
    s_word: non-fully-pointed word
    f_word: fully-pointed word
    ccv: chapter:verse
    """
    return [
        [f"to encode the {mark_or_marks}"],
        [f" {prep} the letter {letter} in ", author.hbo(s_word)],
        [f" in Psalm {ccv} (fully: ", author.hbo(f_word), "$thinsp),"],
    ]


def instead(normal, weird):
    return _instead_f("instead", normal, weird)


def codes_both_summary(foo, bar, baz):
    return f"The code point {foo} means either {bar} or {baz}."


def _instead_f(instead, normal, weird):
    return f"{instead} of ", normal, ", $CTR uses ", weird, "."


def _gray_10(gray_part, normal_part, whbo):
    inner = [author.span_gray(gray_part), normal_part]
    return author.hbo(inner) if whbo else inner


def _gray_01(normal_part, gray_part, whbo):
    inner = [normal_part, author.span_gray(gray_part)]
    return author.hbo(inner) if whbo else inner


def _anc_ia(url):
    return author.paren(mb_html.anchor_h("Internet Archive", url))


_IA_URL_WMG = "https://archive.org/details/mikraot-gedolot-warsaw-1874-1885-full-images/page/n3057/mode/2up"
_IA_URL_SBB = "https://archive.org/details/psalmshebrewtext0000unse/page/n109/mode/2up"
_Y_30_SECTION_TITLE = "“תיבה הראויה להיות מוקפת (מקף אפור)”"
_Y_30_CHAP_2_ANC = mb_html.anchor_h(
    "Chapter 2",
    ws_urls.he_url(
        "ויקיטקסט:מבוא_למקרא_על_פי_המסורה/פרק_ב",
        "הסבר_קצר_על_עיצוב_המקרא_במהדורתנו",
    ),
)
MAM_SPECIAL_MAQAF = [
    ["This kind of $maqaf is special because it (like many features of $MAM)"],
    [" is an aid to reading that is not supplied by the authoritative manuscripts."],
    [" (Other such features include $qq and most non-$pashta stress helpers.)"],
    [" For more information,"],
    [" see the section ", _Y_30_SECTION_TITLE],
    [" in ", _Y_30_CHAP_2_ANC, " of the $MAM documentation."],
]
