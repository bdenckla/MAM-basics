"""Chapter counts for the MAM pages on Hebrew Wikisource.

This declaration lets a first download run without Google CSVs, parsed products,
or previous Wikisource downloads. Book order, sections, names, and numeral spelling
remain in the existing metadata modules. The corpus comparison in
``tests/test_wikisource_plan_corpus.py`` checks every planned chapter against the
committed raw Wikisource chapter keys.
"""

from mb_cmn import bib_locales as tbn

BOOK39_CHAPTER_COUNTS = {
    tbn.BK_GENESIS: 50,
    tbn.BK_EXODUS: 40,
    tbn.BK_LEVIT: 27,
    tbn.BK_NUMBERS: 36,
    tbn.BK_DEUTER: 34,
    tbn.BK_JOSHUA: 24,
    tbn.BK_JUDGES: 21,
    tbn.BK_FST_SAM: 31,
    tbn.BK_SND_SAM: 24,
    tbn.BK_FST_KGS: 22,
    tbn.BK_SND_KGS: 25,
    tbn.BK_ISAIAH: 66,
    tbn.BK_JEREM: 52,
    tbn.BK_EZEKIEL: 48,
    tbn.BK_HOSHEA: 14,
    tbn.BK_JOEL: 4,
    tbn.BK_AMOS: 9,
    tbn.BK_OVADIAH: 1,
    tbn.BK_JONAH: 4,
    tbn.BK_MIKHAH: 7,
    tbn.BK_NAXUM: 3,
    tbn.BK_XABA: 3,
    tbn.BK_TSEF: 3,
    tbn.BK_XAGGAI: 2,
    tbn.BK_ZEKHAR: 14,
    tbn.BK_MALAKHI: 3,
    tbn.BK_PSALMS: 150,
    tbn.BK_PROV: 31,
    tbn.BK_JOB: 42,
    tbn.BK_SONG: 8,
    tbn.BK_RUTH: 4,
    tbn.BK_LAMENT: 5,
    tbn.BK_QOHELET: 12,
    tbn.BK_ESTHER: 10,
    tbn.BK_DANIEL: 12,
    tbn.BK_EZRA: 10,
    tbn.BK_NEXEM: 13,
    tbn.BK_FST_CHR: 29,
    tbn.BK_SND_CHR: 36,
}
