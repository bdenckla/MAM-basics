"""Unicode normalization for fragile characters."""

import unicodedata

from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu

__all__ = ["get_fragile_comps", "is_fragile"]


_DROP_TABLE = str.maketrans(
    {
        hpo.DAGOMOSD: None,
        hpo.RAFE: None,
        hpo.SHIND: None,
        hpo.SIND: None,
        hpu.LODOT: None,  # See "Note on lower dot"
        "\N{COMBINING ACUTE ACCENT}": None,
        # COMBINING ACUTE ACCENT is used in í in Martín in a documentation note.
        # We drop it because otherwise the string is fragile, since we define
        # fragile to mean "changed by normalization to NFC".
    }
)


def get_fragile_comps(string):
    """Get the pair of strings used in fragile comparison."""
    dropped = string.translate(_DROP_TABLE)
    dropped_n = unicodedata.normalize("NFC", dropped)
    return dropped, dropped_n


def is_fragile(string):
    """Return whether the string is fragile."""
    fcs = get_fragile_comps(string)
    return fcs[0] != fcs[1]


###########################################################
# Note on lower dot:
#
# For the one word that uses lower dot, in Ps27:13, MAM uses
# a "Unicode-abnormal" order on one letter:
#
#    lamed, tsere, revia, lower dot, upper dot
#
# This has a certain logic to it:
#
#    letter, vowel, accent, [really weird stuff]
#
# i.e.
#
#    letter, vowel, accent, lower dot, upper dot
#
# But both Unicode and SBL normal orders specify that all lower
# marks, including lower dot, should appear before any upper accents.
# This would make the order:
#
#    lamed, tsere, lower dot, revia, upper dot
#
# Below, we sidestep the issue by dropping lower dot.
# This "admits" that our ordering of lower dot is abnormal.
# This puts lower dot in the same category as dagesh, rafeh, shin dot,
# and sin dot.
# That category being, marks for which we "admit" that our ordering
# is Unicode-abnormal.
# Note that Unicode normal order is not *insane* for lower dot, as it is
# for the other four marks.
# We just happen to not want to use Unicode order for lower dot.
#
###########################################################
# Note on QUPO, LAOI, and LAOE
#
# We encode QUPO as QUcPO so that,
# even in the face of Unicode normalization,
# the Q, U, P, & O marks appear in QUPO order, albeit with a CGJ in the middle.
#
# We prefer QUPO order because it obeys the general principle:
#
#    Undermarks first, in RTL order (QUP), followed by overmark(s) (O).
#
# That's why the underlying spreadsheet sources are encoded in QUPO order.
#
# Note that, despite our preference for QUPO, we prefer LAOI & LAOE.
#
# I.e., despite the fact that LAOI & LAOE violate the principle above,
# we prefer them.
#
# LAOI & LAOE violate the principle above because they have "O" (an overmark)
# between two undermarks. Those undermarks are:
#
#    1. "A", meaning qamats or patax
#    2. "I" or "E", meaning hiriq or sheva
#
# We prefer LAOI & LAOE for two reasons:
#
#    1. Analogy with LAUI & LAUE
#    2. "Implicit yod" interpretation, e.g. LAOI "stands for" LAO[Y]I where
#       "[Y]" represents an implicit yod.
