"""The attribution link that the MAM statement prescribes outside Hebrew, and its licence.

DATA-LICENSES.md, "The MAM statement, repeated verbatim", prescribes for attribution
in English and every language other than Hebrew a direct link to this page, and
gives the CC-BY-SA 4.0 licence's link.
"""

ENGLISH_ATTRIBUTION_URL = (
    "https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning"
)
LICENSE_URL = "https://creativecommons.org/licenses/by-sa/4.0/"
# The credit line that an English page has after its own credit when it quotes MAM, as
# (text, link or None) parts, so that each generator renders it with its own HTML builder.
ENGLISH_ATTRIBUTION_PARTS = (
    ("Source attribution: ", None),
    ("Hebrew Wikisource", ENGLISH_ATTRIBUTION_URL),
    (", under ", None),
    ("CC-BY-SA 4.0", LICENSE_URL),
    (".", None),
)
