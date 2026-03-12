"""Bot edit: remove specific meteg marks from Joshua.

Removes 48 meteg (U+05BD) marks from specific words in Joshua on
Wikisource, aligning Wikisource with mgketer where MAM-parsed-plus
previously added a meteg that mgketer does not have.

Each edit is a (chapter_key, old_string) pair.  The old_string appears
exactly once in its chapter; the replacement is old_string with the
first meteg removed.  Some old_strings include trailing context (a
maqaf or following word) to ensure uniqueness.

See ws_bot_edit_history.md for a record of previous bots that occupied
this file.  The immediately preceding bot is preserved as
ws_bot_edit_old_yby_confine.py.
"""

from pyws import ws_get_bk_in_both_fmts as wsin
from pyws import ws_fmt_2_back_to_wikitext as btw

_METEG = "\u05bd"

# fmt: off
_EDITS_JOSHUA = [
    ("א", "אֱלֹֽהֵיכֶ֔ם"),                    # 1:11
    ("ג", "וַיֵּֽלְכ֖וּ"),                      # 3:6
    ("ג", "נֹֽשְׂאֵ֥י"),                        # 3:8
    ("ג", "לַֽעֲבֹ֖ר"),                         # 3:14
    ("ג", "וַיַּֽעַמְד֡וּ"),                    # 3:16
    ("ג", "מֵֽאָדָ֤ם"),                         # 3:16 qere in template
    ("ד", "הָֽאֲבָנִ֥ים"),                      # 4:6
    ("ד", "בְּנֵֽי־יִשְׂרָאֵל֮"),              # 4:8
    ("ד", "הָֽאָר֗וֹן"),                        # 4:10
    ("ד", "כַּֽאֲשֶׁר־"),                       # 4:11
    ("ו", "וְתָֽקְע֖וּ"),                      # 6:8
    ("ז", "וַיִּֽחַר־"),                        # 7:1
    ("ז", "הָֽאֲנָשִׁ֔ים"),                    # 7:2
    ("ז", "אָֽנֹכִ֤י"),                         # 7:20
    ("ח", "אַֽחֲרֵ֣י"),                         # 8:16
    ("ח", "הָֽרוֹדֵֽף׃"),                       # 8:20 two metegs; remove first
    ("ח", "כַּֽאֲשֶׁ֣ר"),                       # 8:31
    ("ט", "וַיַּֽעֲשׂ֤וּ"),                    # 9:4
    ("י", "יְרֽוּשָׁל"),                        # 10:5 string before {{מ:ירושלם}} template
    ("יב", "מֶֽלֶךְ־"),                         # 12:5
    ("יב", "יְרֽוּשָׁל"),                       # 12:10 string before {{מ:ירושלם}} template
    ("יג", "הָֽעַזָּתִ֤י"),                     # 13:3
    ("יג", "וַֽחֲצִ֖י"),                        # 13:7
    ("יג", "מֶֽלֶךְ־"),                         # 13:30
    ("טו", "הֶֽעָרִ֗ים"),                       # 15:21
    ("טו", "וַֽעֲדֻלָּ֔ם"),                     # 15:35
    ("טו", "וַֽעֲדִיתַ֔יִם"),                   # 15:36
    ("טז", "בְנֵֽי־יוֹסֵ֖ף"),                  # 16:4
    ("יז", "הֽוֹרִישֽׁוֹ׃"),                    # 17:13 two metegs; remove first
    ("יח", "לִגְבֽוּלֹתֶ֛יהָ"),                 # 18:20
    ("יח", "הֶֽעָרִ֗ים"),                       # 18:21
    ("יט", "בְנֵֽי־שִׁמְע֖וֹן בְּת"),          # 19:8
    ("יט", "נַֽחֲלַ֥ת"),                        # 19:16
    ("יט", "הֶֽעָרִ֖ים"),                       # 19:39
    ("כ", "וְאָֽסְפ֨וּ"),                       # 20:4
    ("כא", "הַנּֽוֹתָרִ֗ים"),                   # 21:5
    ("כא", "אַֽהֲרֹ֣ן"),                        # 21:13
    ("כא", "בְנֵֽי־אַהֲרֹ֖ן"),                 # 21:19
    ("כא", "הַנּֽוֹתָרִ֖ים"),                   # 21:20
    ("כא", "גֵֽרְשׁוֹן֮"),                      # 21:27
    ("כב", "כַּֽאֲשֶׁ֖ר"),                      # 22:4
    ("כב", "עֶֽבֶד־"),                          # 22:5
    ("כב", "וְלַֽחֲצִ֣י"),                      # 22:7
    ("כב", "יֹֽאמְר֨וּ"),                       # 22:24
    ("כג", "אֱלֹֽהֵיכֶֽם׃"),                    # 23:11 two metegs; remove first
    ("כד", "וַיֶּֽאֱסֹ֧ף"),                     # 24:1
    ("כד", "וָֽאוֹלֵ֥ךְ"),                      # 24:3
    ("כד", "וָֽאֶתֵּ֨ן"),                       # 24:4
]
# fmt: on


def _build_edits_by_book_and_chapter(all_edits):
    """Group (old, new) pairs by (bk39id, chapter_key)."""
    result = {}
    for bk39id, edit_list in all_edits.items():
        by_chap = {}
        for chap_key, old in edit_list:
            new = old.replace(_METEG, "", 1)
            by_chap.setdefault(chap_key, []).append((old, new))
        result[bk39id] = by_chap
    return result


_ALL_EDITS = {
    "Joshua": _EDITS_JOSHUA,
}
_EDITS_BY_BK_CH = _build_edits_by_book_and_chapter(_ALL_EDITS)


def _get_chapter_edits(bk39id, he_chnu):
    return _EDITS_BY_BK_CH.get(bk39id, {}).get(he_chnu, [])


def edit_page_text(bk39id, he_chnu, page_text):
    """Apply meteg-removal edits to a chapter's raw page text."""
    for old, new in _get_chapter_edits(bk39id, he_chnu):
        count = page_text.count(old)
        assert count == 1, (
            f"Expected 1 occurrence of {old!r} in {bk39id} chapter {he_chnu},"
            f" found {count}"
        )
        page_text = page_text.replace(old, new)
    return page_text


def edit_cif2(bk39id, he_chnu, cif2):
    """Apply meteg-removal edits via the format-2 roundtrip."""
    big = btw.big_str(he_chnu, cif2)
    edited = edit_page_text(bk39id, he_chnu, big)
    edited_cif2 = wsin.get_chap_in_fmt_2(edited.splitlines())
    return edited_cif2, edited
