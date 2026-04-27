from mb_cmn import bib_locales as tbn
from mb_cmn import my_utils
from mb_cmn import provenance
from py_misc import mwd_utils as mwdu
from mb_misc import mb_html
from mb_misc import ws_urls


def write_index_dot_html(edition, css_hrefs, out_path):
    foi_anchor = mb_html.anchor_h("Features of interest", "foi/index.html")
    sigil_anchor = mb_html.anchor_h("Sigil decoding", "sigil-decoding.html")
    aliyot_anchor = mb_html.anchor_h("Notes on aliyot", "misc/notes_on_aliyot.html")
    changelog_anchor = mb_html.anchor_h("Change log", "change-log/index.html")
    body_contents = (
        *_cc_by_sa_license(),
        _unordered_list_of_sections(),
        mb_html.horizontal_rule(),
        foi_anchor,
        mb_html.horizontal_rule(),
        sigil_anchor,
        mb_html.horizontal_rule(),
        aliyot_anchor,
        mb_html.horizontal_rule(),
        changelog_anchor,
    )
    write_ctx = mb_html.WriteCtx(
        edition + ": Book Links",
        out_path,
        css_hrefs=css_hrefs,
        html_comment=provenance.generated_html_comment(__file__),
    )
    mb_html.write_html_to_file(body_contents, write_ctx)


def _cc_by_sa_license():
    eng_title = "Miqra according to the Masorah (MAM)"
    heb_title = "מקרא על פי המסורה"
    anchor_cc_by_sa = mb_html.anchor_h(
        "CC-BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/"
    )
    anchor_he_wikisource = mb_html.anchor_h("Hebrew Wikisource", ws_urls.HEBREW)
    return (
        mb_html.heading_level_1((f"{eng_title} ({heb_title})")),
        mb_html.para(
            (
                "License: ",
                anchor_cc_by_sa,
                " ",
                "Source attribution: ",
                anchor_he_wikisource,
            )
        ),
    )


def _licont_for_section(secid):  # licont: list item contents
    anchors = tuple(map(mwdu.mk_anchor_with_link_to_book, tbn.bk39s_of_sec(secid)))
    book_list = my_utils.intersperse(" ", anchors)
    return secid, ": ", *book_list


def _unordered_list_of_sections():
    liconts_for_sections = tuple(map(_licont_for_section, tbn.ALL_SECIDS))
    return mb_html.unordered_list(liconts_for_sections)
