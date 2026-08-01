from __future__ import annotations

from mb_cmn import bib_locales as tbn

"""Extant BHQ fascicles as (volume, book, bk24id, year) tuples.

Source: user-provided table snippet.
Dropped columns: editor, affiliation, and country.
"""

EXTANT_BHQ: list[tuple[int, str, str, int]] = [
    # fascicle number, book label, bk24id, year
    (18, "Ruth", tbn.BK24_RUTH, 2004),
    (18, "Canticles", tbn.BK24_SONG, 2004),
    (18, "Qoheleth", tbn.BK24_QOHELET, 2004),
    (18, "Lamentations", tbn.BK24_LAMENT, 2004),
    (18, "Esther", tbn.BK24_ESTHER, 2004),
    (20, "Ezra and Nehemiah", tbn.BK24_EZ_NE, 2006),
    (5, "Deuteronomy", tbn.BK24_DEUTER, 2007),
    (17, "Proverbs", tbn.BK24_PROV, 2008),
    (13, "Twelve Prophets", tbn.BK24_THE_12, 2010),
    (7, "Judges", tbn.BK24_JUDGES, 2011),
    (1, "Genesis", tbn.BK24_GENESIS, 2016),
    (3, "Leviticus", tbn.BK24_LEVIT, 2020),
    (16, "Job", tbn.BK24_JOB, 2024),
]
