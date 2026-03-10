""" Exports main """

from py_misc import my_html
from pyauthor_util import author


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_CONT_PARA_01),
        author.para(_CONT_PARA_03),
    ]
    author.assert_stem_eq(__file__, _FNAME)
    author.help_gen_html_file(tdm_ch, _FNAME, _TITLE, cbody)


_TITLE = "On the Provenance of Chabad’s CTR"
_H1_CONTENTS = "On the Provenance of Chabad’s $CTR"
_FNAME = "rocc_1_on_the_provenance_of_ctr.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")
_CONT_PARA_01 = """The $anc_Chabad_website has an edition of the Hebrew Bible
called $anc_Chabad_CTR ($CTR).
(This edition also goes by other similar names such as
The Complete Jewish Bible with Rashi Commentary.)
Perhaps Chabad’s $CTR is derived from a $CD_ROM version of $CTR
that was a collaboration between Judaica Press and the software company Davka.
(See, e.g., the $anc_record_ctr_cdrom_nli for this $CD_ROM at the $NLI.)""".replace("\n", " ")
_CONT_PARA_03 = """Further, perhaps this $CD_ROM version of $CTR
has some relationship to the Hebrew Bible
found on another Davka $CD_ROM known as the Soncino Classics Collection.""".replace("\n", " ")

###############################################################################
# From https://en.wikipedia.org/wiki/Soncino_Press#Second_edition:
#
# A second edition of all [Soncino Books of the Bible] other than the Soncino
# Chumash appeared in the 1990s, edited by Rabbi Abraham J. Rosenberg [...],
# who had previously done a Bible commentary for Judaica Press [...].

###############################################################################
# Soncino Books of the Bible: Psalms (1945)
# https://archive.org/details/psalmshebrewtext0000unse/

###############################################################################
# https://archive.org/details/mikraot-gedolot-warsaw-1874-1885-full-images/page/n3057/mode/2up

###############################################################################
# From JCL 2.2 Manual.PDF
# (JCL: Judaic Classics Libraries)
#
# Institute for Computers in Jewish Life
# Davka Corporation
# David Mandel
# Judaica Press
#
# חמישה חומשי תורה, רש״י לתורה, רמב״ן, אור
# החיים ובעל הטורים על התורה, ותרגום
# אונקלוס. מקראות גדולות, וורשא, 1893
#
# נביאים, כתובים. מקראות גדולות, וורשא, 1893
#
# The text of the Tanach is based on the 1895 Warsaw edition of the Mikraot
# Gedolot which has been carefully compared with other versions such as the
# Jerusalem Koren Tanach. In some instances (involving mainly Ken and Ketiv
# and Chaser and Malay) the text has been modified to conform to the Koren
# edition. However, the responsibility for such decisions is solely that of
# the CD ROM publishers.
#
# Comments on the above:
#
#    * Is "Kere" (aka Qere) meant instead of "Ken"?
#    * There seems to be an 1893 vs 1895 contradiction regarding the Warsaw
#      Mikraot Gedolot (מקראות גדולות)
