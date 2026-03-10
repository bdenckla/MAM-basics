"""
Exports 2 functions and 1 constant:
    mark_doc_targets
    extract_docs
    DOC_TARGET_STR_TO_DOC_LEMMA
    DOC_TARGET_TMPL_TO_DOC_LEMMA_TMPL
"""

from pycmn import shrink
from py_misc import uni_heb_char_classes as uhc
from pyrender import render_element as renel
from pycmn import hebrew_punctuation as hpu
from pycmn import template_names as tmpln
from py_misc import hebrew_letter_words as hlw


def mark_doc_targets(renseq):
    """
    In the given renseq, mark each doc target by either:
        making it a ren_el with tag "mam-doc-target-without-callout"
        putting an asterisk after it
    """
    mapres = map(_mark_doc_targets_in_ren_el, renseq)
    return shrink.shrink(sum(mapres, tuple()))


def extract_docs(renseq):
    """Extract documentation notes from the given renseq"""
    return sum(map(_extract_doc_from_ren_el, renseq), tuple())


def _extract_doc_from_ren_el(ren_el):
    if not isinstance(ren_el, dict):
        return tuple()
    if "doc_parts" in ren_el:
        assert renel.get_ren_el_tag(ren_el) == "mam-doc"
        extract = {"doc_lemma": ren_el["doc_lemma"], "doc_parts": ren_el["doc_parts"]}
        return (extract,)
    if contents := renel.get_ren_el_contents(ren_el):
        return extract_docs(contents)
    assert renel.ren_el_is_tag_only(ren_el)
    return tuple()


def _mark_doc_target_in_doc_ren_el(doc_ren_el):
    return _mark_doc_target(
        renel.get_ren_el_contents(doc_ren_el), doc_ren_el["doc_lemma"]
    )


def _mark_doc_target(doc_target, doc_lemma):
    # Mark the doc target by either:
    #    making it a ren_el with tag "mam-doc-target-without-callout"
    #    putting an asterisk after it
    if _does_not_need_callout(doc_lemma):
        dtib = renel.mk_ren_el_tc("mam-doc-target-without-callout", doc_target)
        return (dtib,)
    return *doc_target, _MAM_DOC_NOTE_CALLOUT


def _does_not_need_callout(doc_lemma):
    if _has_pointed_string_within(doc_lemma):
        return True
    if doc_lemma in _LEMMAS_FOR_WHICH_TARGET_DOES_NOT_NEED_CALLOUT:
        return True
    if doc_lemma in _LEMMAS_FOR_WHICH_TARGET_NEEDS_CALLOUT:
        return False
    assert False, doc_lemma


def _has_pointed_string_within(ren_els):
    pointed_sum = _pointed_sum(ren_els)
    pointed_letters = hlw.letters_and_maqafs(pointed_sum)
    return len(pointed_letters) > 0


def _pointed_sum(ren_els):
    assert isinstance(ren_els, (tuple, list))
    pointed_sum = ""
    for ren_el in ren_els:
        if isinstance(ren_el, str):
            if _VOW_AND_ACC.intersection(ren_el):
                pointed_sum += ren_el
            continue
        if renel.ren_el_is_tag_only(ren_el):
            continue
        _tag, contents = renel.get_ren_el_tc(ren_el)
        pointed_sum += _pointed_sum(contents)
    return pointed_sum


def _mark_doc_targets_in_ren_el(ren_el):
    if not isinstance(ren_el, dict):
        return (ren_el,)
    if "doc_parts" in ren_el:
        assert renel.get_ren_el_tag(ren_el) == "mam-doc"
        return _mark_doc_target_in_doc_ren_el(ren_el)
    if contents := renel.get_ren_el_contents(ren_el):
        new_ren_el = dict(ren_el, contents=mark_doc_targets(contents))
        return (new_ren_el,)
    assert renel.ren_el_is_tag_only(ren_el)
    return (ren_el,)


_VOW_AND_ACC = set(uhc.VOWEL_POINTS) | set(uhc.ACCENTS)
_MAM_DOC_NOTE_CALLOUT = renel.mk_ren_el_tc("mam-doc-callout", ("*",))
LEMMA_FROM_STR = {
    " ": ("__",),
    "__": ("__",),
    hpu.SOPA: ("סוף פסוק",),
}
LEMMA_FROM_TMPL = {
    # When the doc target is a template, in some cases we want to
    # show the template name (or something like it) as the doc lemma.
    # Note that this is only for when the template is the one and only thing
    # that the doc-note targets. I.e. this does not include just being used
    # in the doc target, i.e. this does not include cases where the doc
    # target has other stuff before and/or after one of these templates.
    "מ:פסק": ("פסק",),  # strip מ: (mem-colon)
    "ססס": ("ססס",),
    "סס": ("סס",),
    "פפפ": ("פפפ",),
    "פפ": ("פפ",),
    "ר0": ("ר0",),
    "ר1": ("ר1",),  # See note on resh-n paragraph divisions below
    # ר2 (resh-2) does not appear in this context
    "ר3": ("ר3",),  # See note on resh-n paragraph divisions below
    "ר4": ("ר4",),  # See note on resh-n paragraph divisions below
    tmpln.NO_PAR_AT_STA_OF_CHAP21: ("אין פרשה בתחילת פרק",),
    # The mapping above means we strip mem-colon when we display.
    # I.e. we don't literally display the template name.
    tmpln.NO_PAR_AT_STA_OF_CHAP03: ("אין פרשה בתחילת פרק בספרי אמ״ת",),
    # The mapping above means we strip mem-colon and use true gershayim when we display.
    # I.e. we don't literally display the template name.
}
# Note on resh-n paragraph divisions
#
# In תהלים and only in תהלים there are doc-notes about resh-n functioning as a
# paragraph division, i.e. functioning as פרשה סתומה or פרשה פתוחה. There are
# 115 such notes. For example:
#
#     {{נוסח|{{ר3}}|פרשה פתוחה}}
#     {{נוסח|{{ר1}}|פרשה סתומה}}
#
# These notes only occur for resh-n where n=1, 3, or 4.
# I.e., these notes only occur for ר1 or ר3 or ר4.
# I.e., these notes never occur for ר0 or ר2.
_LEMMAS_FOR_WHICH_TARGET_NEEDS_CALLOUT = (
    *tuple(LEMMA_FROM_STR.values()),
    *tuple(LEMMA_FROM_TMPL.values()),
    #
    (renel.mk_ren_el_tc("mam-spi-invnun", ("׆",)),),
    (renel.mk_ren_el_tc("mam-kq-k-velo-q", ("(אם)",)),),  # See note below
)
_LEMMAS_FOR_WHICH_TARGET_DOES_NOT_NEED_CALLOUT = (
    ("והיה ... יהוה",),
    ("הנה ... והנורא",),
    ("השיבנו ... כקדם",),
    ("סוף ... האדם",),
)
#
# Note on why "(אם)" is listed in _LEMMAS_FOR_WHICH_TARGET_NEEDS_CALLOUT
#
# (This occurs only in Ruth 3:12.)
#
# I'm not sure why, above, I "ask for" a callout (red asterisk) for (אם)
# rather than letting the normal mechanism of target identification apply
# (blue color).
#
# Perhaps I ask for a callout because I wanted to leave open the option of
# coloring (אם) gray, as in Wikisource?
#
# If CSS rules existed to color (אם) both blue and gray, it is unclear to me
# who would "win".
#
# (I think who would win is well-defined, but it is not obvious to me.)
#
# Perhaps that situation would call for a special CSS selector "asking" for
# light blue!
