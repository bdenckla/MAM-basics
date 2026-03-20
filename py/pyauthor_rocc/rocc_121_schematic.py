from pyauthor_util import author
from py_misc import hebrew_letter_words as hlw
from pyauthor_rocc import rocc_util as ru

from pycmn.my_utils import sl_map
from py_misc import my_html


def _bg(s):
    """bg = background"""
    words = s.split(" ")
    words_lm = sl_map(hlw.letters_and_maqafs, words)
    new_str = " ".join(words_lm)
    return my_html.span(new_str, {"class": "gray"})


def _fg(contents):
    """fg = foreground"""
    return author.hbo(contents, {"lt-space-okay": "true"})


_NJVY_PJ3 = _fg([" ", ru.gray_abg_njvy("פֶּ֗שַׁע", whbo=False), " "])
_AJRY_ADM_LA_YXJB = _fg(
    [
        ru.gray_abg_adm("אַ֥שְֽׁרֵי־", whbo=False),
        " ",
        ru.gray_abg_yxjb("לֹ֤א ", whbo=False),
        " ",
    ]
)
_CY_HXRJTY = _fg([ru.gray_abg_hxrjty("כִּֽי־", whbo=False), " "])
_AL_THYV = _fg([" ", ru.gray_abg_al("תִּהְי֤וּ ׀", whbo=False), " "])

VERSES = [
    [_bg("לְדָוִ֗ד מַ֫שְׂכִּ֥יל אַשְׁרֵ֥י"), _NJVY_PJ3, _bg("כְּס֣וּי חֲטָאָֽה׃")],
    [_AJRY_ADM_LA_YXJB, _bg("יְהֹוָ֣ה ל֣וֹ עָוֺ֑ן וְאֵ֖ין בְּרוּח֣וֹ רְמִיָּֽה׃")],
    [_CY_HXRJTY, _bg("בָּל֣וּ עֲצָמָ֑י בְּ֝שַׁאֲגָתִ֗י כׇּל־הַיּֽוֹם׃")],
    [
        _bg("כִּ֤י ׀"),
        _fg(" יוֹמָ֣ם וָלַיְלָה֮ תִּכְבַּ֥ד "),
        _bg("עָלַ֗י יָ֫דֶ֥ךָ נֶהְפַּ֥ךְ לְשַׁדִּ֑י בְּחַרְבֹ֖נֵי קַ֣יִץ סֶֽלָה׃"),
    ],
    [
        _bg("חַטָּאתִ֨י אוֹדִ֪יעֲךָ֡"),
        _fg(" וַעֲוֺ֘נִ֤י "),
        _bg("לֹֽא־כִסִּ֗יתִי אָמַ֗רְתִּי אוֹדֶ֤ה עֲלֵ֣י פְ֭שָׁעַי לַיהֹוָ֑ה וְאַתָּ֨ה"),
        _fg(" נָ֘שָׂ֤אתָ "),
        _bg("עֲוֺ֖ן חַטָּאתִ֣י סֶֽלָה׃"),
    ],
    [
        _bg(
            "עַל־זֹ֡את יִתְפַּלֵּ֬ל כׇּל־חָסִ֨יד ׀ אֵלֶיךָ֮ לְעֵ֢ת מְ֫צֹ֥א רַ֗ק לְ֭שֵׁטֶף"
        ),
        _fg(" מַ֣יִם "),
        _bg("רַבִּ֑ים אֵ֝לָ֗יו לֹ֣א יַגִּֽיעוּ׃"),
    ],
    [
        _bg(
            "אַתָּ֤ה ׀ סֵ֥תֶר לִי֮ מִצַּ֢ר תִּ֫צְּרֵ֥נִי רׇנֵּ֥י פַלֵּ֑ט תְּס֖וֹבְﬞבֵ֣נִי סֶֽלָה׃"
        )
    ],
    [
        _bg(
            "אַשְׂכִּֽילְךָ֨ ׀ וְֽאוֹרְךָ֗ בְּדֶֽרֶךְ־ז֥וּ תֵלֵ֑ךְ אִיעֲצָ֖ה עָלֶ֣יךָ עֵינִֽי׃"
        )
    ],
    [
        _AL_THYV,
        _bg("כְּס֥וּס כְּפֶרֶד֮"),
        _fg(" אֵ֤ין "),
        _bg("הָ֫בִ֥ין"),
        _fg(" בְּמֶתֶג־וָרֶ֣סֶן "),
        _bg("עֶדְי֣וֹ לִבְל֑וֹם בַּ֝֗ל"),
        _fg(" קְרֹ֣ב "),
        _bg("אֵלֶֽיךָ׃"),
    ],
    [
        _bg("רַבִּ֥ים מַכְאוֹבִ֗ים"),
        _fg(" לָ֫רָשָׁ֥ע "),
        _bg("וְהַבּוֹטֵ֥חַ בַּֽיהֹוָ֑ה חֶ֝֗סֶד יְסוֹבְﬞבֶֽנּוּ׃"),
    ],
    [
        _fg("שִׂמְח֬וּ "),
        _bg("בַיהֹוָ֣ה וְ֭גִילוּ צַדִּיקִ֑ים וְ֝הַרְנִ֗ינוּ כׇּל־יִשְׁרֵי־לֵֽב׃"),
    ],
]
