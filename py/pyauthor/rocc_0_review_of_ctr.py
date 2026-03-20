"""Exports main"""

from py_misc import my_html
from pyauthor_util import author
from pyauthor_rocc import rocc_0_part_1
from pyauthor_rocc import rocc_0_part_2
from pyauthor_rocc import rocc_0_review_of_ctr_header as hdr

# XXX TODO find other uses of non-bent lamed in JP
# XXX TODO find other uses of qadma/azla on (presumably non-bent) lamed in JP
# XXX TODO document other below-marks are aligned below ayin in JP (images already extracted)

_X_CPARA_CONCLUSION = """I hope this review of $CTR’s Psalm 32 has shown the reader
why I consider $CTR to be the weirdest Tanakh on the web, and possibly the worst.
Whether or not the reader is convinced of the same, I hope that at least my reasons
for these judgments are now clear.""".replace("\n", " ")


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(hdr.H1_CONTENTS),
        *rocc_0_part_1.BODY_ELEMENTS_1,
        my_html.heading_level_2("Use and abuse of Unicode"),
        *rocc_0_part_1.BODY_ELEMENTS_2,
        my_html.heading_level_2("Substantive differences"),
        *rocc_0_part_1.BODY_ELEMENTS_3,
        *rocc_0_part_2.BODY_ELEMENTS,
        my_html.heading_level_2("Conclusion"),
        author.para(_X_CPARA_CONCLUSION),
    ]
    author.help_gen_html_file(__file__, tdm_ch, hdr.FNAME, hdr.TITLE, cbody)
