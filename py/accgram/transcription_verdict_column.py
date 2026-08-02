r"""The grammaticality column both satellite verdict tables carry (issue wlc-utils#52).

``printed_decalogue_simanim_page`` and ``printed_decalogue_koren_page`` each render a
per-Decalogue verdict table saying how far a printed Decalogue follows the Wikisource strand it
was diffed against (issue wlc-utils#69).  That is a token-IDENTITY claim.  This module supplies those
tables' last column, which asks the different question this repo's printed-Decalogue work started
from: fed through accgram's prose checker, is what the page prints GRAMMATICAL -- and is it as
grammatical as the Wikisource strand it follows?  ``transcription_parse`` computes the verdicts;
here they become a table cell.

WHY THE COLUMN IS AGAINST THE WIKISOURCE STRAND AND NOT ABSOLUTE.  Four of the twelve transcribed
Decalogues follow the p-trad עליון, whose opening chanted verse merges the first two
commandments and is ungrammatical -- the companion page's headline finding.  Those four print
that verse, so each is "ungrammatical somewhere" while departing from its Wikisource strand
nowhere.  A
column that only counted failures would put them beside the one page that really does depart,
and the two facts are not the same fact.

SHARED, SO IT CANNOT DRIFT.  The two pages must say this identically -- the same reason
``printed_decalogue_strands`` single-sources ``MOST_STRIKING`` and the Shabbat signal-word
shorthand -- and the cell is derived from the checker's own result rather than written out per
row, so no row can claim a verdict the checker does not give.  Each page keeps its own table:
the other four columns are that page's material.

WHAT A REJECTION SAYS, AND WHAT IT DOES NOT.  It says the chanted verse is ungrammatical, and
the pages say that without qualification: it is a fact about the accent sequence, not an
artifact of this checker, and one an internal study of the edition would reach on its own, since
the rest of that edition's accentuation is grammatical.  It does NOT say the edition is in
error, or that the passage should not be chanted as printed; the pages must not say either.  A
clean rate is not the objective (issue wlc-utils#52).
"""

from __future__ import annotations

from accgram import transcription_parse as tp

from py_html import wlc_utils_html as H

# The column heading, lower-case to match its siblings ("pages", "strand", "how far it follows
# it").  "the prose checker" rather than a module name: both Decalogues are prose, and the page
# has already introduced the checker by that description.
HEADER = "under the prose checker"


def by_stem(results: list[tp.TranscriptionResult]) -> dict[str, tp.TranscriptionResult]:
    return {r.stem: r for r in results}


def cell(result: tp.TranscriptionResult) -> object:
    """One transcription's grammar verdict, as the table cell for it.

    Three shapes, one per thing that can be true: the page and its Wikisource strand are clean
    throughout; the page has its Wikisource strand's verdicts including a chanted verse both
    reject; or the page's verdict departs from its Wikisource strand's somewhere, which is the
    finding worth having and is therefore the one shape that announces itself.
    """
    n = len(result.chanted_verses)
    if not result.departures:
        bad = [cv.index for cv in result.ungrammatical]
        if not bad:
            return f"Clean at all {n} chanted verses, as its Wikisource strand is."
        return (
            f"Its Wikisource strand's verdicts: {_verses(bad)} ungrammatical,"
            f" the other {n - len(bad)} clean."
        )
    return (
        H.bold("Not as grammatical as its Wikisource strand"),
        ": " + "; ".join(_departure(d) for d in result.departures) + ".",
    )


def _departure(departure: tuple[int, str, str]) -> str:
    index, strand_status, status = departure
    return f"chanted verse {index} is {status} where that strand is {strand_status}"


def _verses(indices: list[int]) -> str:
    """``chanted verse 1`` / ``chanted verses 1 and 4`` / ``chanted verses 1, 4 and 9``."""
    if len(indices) == 1:
        return f"chanted verse {indices[0]}"
    head = ", ".join(str(i) for i in indices[:-1])
    return f"chanted verses {head} and {indices[-1]}"
