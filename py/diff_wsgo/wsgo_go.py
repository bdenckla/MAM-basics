"""Exports massage_go_book"""

import unicodedata

from mb_cmn.my_utils import dv_map
from mb_cmn.my_utils import dv_dispatch
from mb_cmn import ws_tmpl1 as wtp1
from mb_cmn import plain_template_schema


def massage_go_book(go_book):
    """
    Massage a Google book
    into a format suitable for comparison with a Wikisource book.
    """
    return dv_dispatch(_BDISPATCH, go_book)


def massage_go_book_for_google_edit(go_book):
    """Expose exact Google Wikitext for auto-edit search strings."""
    return dv_dispatch(_EDIT_BDISPATCH, go_book)


def _massage_go_verses(go_verses):
    return dv_map(_massage_minirow, go_verses)


def _massage_minirow(minirow):
    """
    This function massages the Google verse, preparing it for
    comparison with a Wikisource verse.
    """
    return {
        "prefix": _massage_wt_tuple(minirow.CP),
        "location": _massage_wt_tuple(minirow.DP),
        "verse-body": _massage_wt_tuple(minirow.EP),
    }


def _minirow_for_google_edit(minirow):
    return {
        "prefix": minirow.CP,
        "location": minirow.DP,
        "verse-body": minirow.EP,
    }


def _massage_wt_list(wt_list, *, allow_mark_only=False):
    """
    This function massages a list of Google Wikitext elements,
    preparing that list for comparison with its Wikisource counterpart.
    """
    # wt list: list of wt els
    # wt el: Wikitext element
    # Wikitext element: one of the following:
    #     a str
    #     a singleton dict with key 'custom_tag' or 'tmpl'
    assert isinstance(wt_list, list)
    return [_massage_wtel(wtel, allow_mark_only=allow_mark_only) for wtel in wt_list]


def _massage_wt_tuple(wt_tuple):
    assert isinstance(wt_tuple, tuple)
    return tuple(map(_massage_wtel, wt_tuple))


def _massage_wtel(wtel, *, allow_mark_only=False):
    if isinstance(wtel, str):
        norm = _make_comparison_equivalent_clusters(
            wtel, allow_mark_only=allow_mark_only
        )
        if norm == "׆__":  # inverted nun then double underscore
            norm = "׆ "
        return norm
    if wtp1.is_abtag(wtel):
        plain_template_schema.validate_current_plain_custom_tag(wtel)
        return wtel
    plain_template_schema.validate_current_plain_template(wtel)
    tels = wtp1.template_elements(wtel)
    assert isinstance(tels, list)
    new_tels = list(_massage_wt_list(tel, allow_mark_only=True) for tel in tels)
    return wtp1.mktmpl(new_tels)


def _make_comparison_equivalent_clusters(text, *, allow_mark_only=False):
    """Derive the comparator's established composition and mark-order equivalence.

    NFC makes composed and decomposed non-Hebrew text equivalent. Hebrew clusters,
    including presentation forms, keep their source code points and are ordered
    directly by combining class. A mark-only template argument is ordered as marks
    attached to the letter supplied by that template. Standalone text beginning with
    a combining mark fails rather than being repaired. No call to
    ``unicodedata.normalize`` receives a cluster containing Hebrew.
    """
    if text and unicodedata.combining(text[0]):
        assert allow_mark_only and all(map(unicodedata.combining, text)), (
            "standalone comparison text begins with a combining mark",
            text,
        )
        return "".join(sorted(text, key=unicodedata.combining))
    clusters = []
    cluster = []
    for char in text:
        if cluster and unicodedata.combining(char) == 0:
            clusters.append(_make_comparison_equivalent_cluster("".join(cluster)))
            cluster = []
        cluster.append(char)
    if cluster:
        clusters.append(_make_comparison_equivalent_cluster("".join(cluster)))
    return "".join(clusters)


def _make_comparison_equivalent_cluster(cluster):
    assert not unicodedata.combining(cluster[0]), (
        "standalone comparison text begins with a combining mark",
        cluster,
    )
    contains_hebrew = any(
        "\u0590" <= char <= "\u05ff" or "\ufb1d" <= char <= "\ufb4f" for char in cluster
    )
    if contains_hebrew:
        starter = cluster[:1]
        marks = cluster[1:]
        return starter + "".join(sorted(marks, key=unicodedata.combining))
    return unicodedata.normalize("NFC", cluster)


_BDISPATCH = {
    "verses_plain": _massage_go_verses,
    "good_ending_plain": lambda x: x,
    "chapter_prefixes": lambda x: x,
    "chapter_suffixes": lambda x: x,
}

_EDIT_BDISPATCH = {
    "verses_plain": lambda verses: dv_map(_minirow_for_google_edit, verses),
    "good_ending_plain": lambda x: x,
    "chapter_prefixes": lambda x: x,
    "chapter_suffixes": lambda x: x,
}
