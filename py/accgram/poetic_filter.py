"""Genre filter for the poetic (Three Books) accent grammar.

The inverse of accgram.prose_filter: where the prose filter *excludes* every verse
that uses poetic cantillation so it never reaches the prose parser, this filter
*keeps* exactly those verses and drops everything else.  The poetic corpus is
Psalms and Proverbs wholesale plus the poetically-cantillated verses of Job (Job's
prose frame -- 1:1-3:1, 42:7-17, and a few scattered lines -- uses the prose
system and is handled by the prose grammar instead).

``is_poetcant`` is reused exactly as prose_filter uses it, so the two filters
agree verse-for-verse on the prose/poetic boundary in Job; the BHS-coordinate
hard exclusions prose_filter carries (the Decalogue ranges, Gn 35:22) are prose
verses outside ps/pr/Job and so are simply never kept here.
"""

from __future__ import annotations

from mb_cmn import bib_locales as tbn
from wlc_cmn.wlc_book_codes import wlc_bb_to_bk39id


def should_keep_line(bb: str, chnu: int, vrnu: int) -> bool:
    # Psalms and Proverbs are wholly poetic.
    if bb in ("ps", "pr"):
        return True

    # Job: keep only the poetically-cantillated verses (the inverse of the test
    # prose_filter applies to drop them).
    bk39id = wlc_bb_to_bk39id(bb)
    if bk39id == tbn.BK_JOB:
        bcvtmam = tbn.mk_bcvtmam(bk39id, chnu, vrnu)
        return tbn.is_poetcant(bcvtmam)

    return False
