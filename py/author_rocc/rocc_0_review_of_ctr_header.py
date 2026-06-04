from mb_misc import mb_html
from mb_author import author


def anchor():
    return author.std_anchor(short_anchor("document"), H1_CONTENTS)


def short_anchor(contents):
    return mb_html.anchor_h(contents, f"./{FNAME}")


TITLE = "Review of Chabad’s CTR"
H1_CONTENTS = "Review of Chabad’s $CTR"
FNAME = "rocc_0_review_of_ctr.html"
