"""Convert faithful Wikisource format 2 into the plain-product schema.

Format-2 line boundaries become plain's // notation. An isolated line boundary
in a verse prefix becomes __ unless a spacing template already supplies the
separation. Explicit spaces in prefixes use __ too. The inverted-nun template's
trailing space uses __, as required by render_wikitext_handlers.

Hebrew strings use give_std_mark_order and the existing product spelling of an
adjacent geresh muqdam/revia pair, geresh muqdam first. Latin composition and
all remaining relative mark order are retained. The input book is never modified.
"""

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import template_names
from mb_cmn import uni_denorm
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn.minirow import Minirow
from mb_cmn.shrink import shrink


def convert_book(wsf2_book):
    """Return numeric-keyed chapters, including the plain boundary rows."""
    return {_numeric(ch): _convert_chapter(data) for ch, data in wsf2_book.items()}


def _numeric(he_num):
    return str(hvn.STR_TO_INT_DIC[he_num])


def _convert_chapter(chapter):
    expected = {
        "ws-chap-noinclude-header",
        "ws-chap-body",
        "ws-chap-noinclude-footer",
        "ws-chap-category",
    }
    assert set(chapter) in (expected, expected | {"ws-chap-good-ending"})
    prefix = _noinclude(chapter["ws-chap-noinclude-header"])
    rows = {"0": Minirow(prefix, (), ())}
    for he_vrnu, verse in chapter["ws-chap-body"].items():
        assert set(verse) == {"prefix", "location", "verse-body"}
        rows[_numeric(he_vrnu)] = Minirow(
            _verse_prefix(verse["prefix"]),
            _sequence([verse["location"]]),
            _sequence(verse["verse-body"]),
        )
    suffix = []
    if good_ending := chapter.get("ws-chap-good-ending"):
        suffix = [
            "////",
            {"custom_tag": "קטע התחלה=סיום בטוב/"},
            *_sequence(good_ending),
            {"custom_tag": "קטע סוף=סיום בטוב/"},
        ]
    suffix.extend(_noinclude(chapter["ws-chap-noinclude-footer"]))
    rows["תתת"] = Minirow(tuple(suffix), (), ())
    # The category identifies the source page; it is not a plain-product row.
    return rows


def _noinclude(contents):
    return (
        {"custom_tag": "noinclude"},
        *_sequence(contents),
        {"custom_tag": "/noinclude"},
    )


def _verse_prefix(contents):
    converted = _sequence(contents, prefix=True)
    if "//" in converted and not any(map(_is_spacing_template, converted)):
        return tuple("__" if element == "//" else element for element in converted)
    return converted


def _is_spacing_template(element):
    if not wtp1.is_template(element):
        return False
    if wtp1.is_doc_template(element):
        target = wtp1.template_element(element, 1)
        return target in ([" "], ["__"]) or any(map(_is_spacing_template, target))
    return _PREFIX_TEMPLATE_SPACING[wtp1.template_name(element)]


_PREFIX_TEMPLATE_SPACING = {
    "קק": False,
    "עוגן בשורה": False,
    "סס": True,
    "ססס": True,
    "פפ": True,
    "פפפ": True,
    "מ:ששש": True,
    "ר4": True,
    "ר1": True,
}


def _sequence(contents, *, prefix=False):
    return tuple(shrink([_element(el, prefix=prefix) for el in contents]))


def _element(element, *, prefix):
    if isinstance(element, str):
        if element == "¶":
            return "//"
        if element == "&#32;":
            return "__" if prefix else " "
        ordered = uni_denorm.give_std_mark_order(element)
        return ordered.replace(ha.REV + ha.GER_M, ha.GER_M + ha.REV)
    if wtp1.is_abtag(element):
        return {"custom_tag": uni_denorm.give_std_mark_order(element["custom_tag"])}
    elements = [
        list(_sequence(el, prefix=prefix)) for el in wtp1.template_elements(element)
    ]
    if wtp1.template_name(element) == template_names.INVERTED_NUN:
        assert len(elements) == 2
        if elements[1] == [hpu.NUN_HAF + " "]:
            elements[1] = [hpu.NUN_HAF + "__"]
        assert elements[1] in ([hpu.NUN_HAF], [hpu.NUN_HAF + "__"])
    return wtp1.mktmpl(elements)
