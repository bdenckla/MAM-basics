"""Yeivin's book abbreviations, one per bk39 id, kept as the mapping of record.

NOTHING CALLS THIS MODULE SINCE 2026-09-12, and that is deliberate rather than an
oversight.  Its two callers were py/mb_xml/xml_root_from_bksams.py and
py/mb_json/json_root_from_bksams.py, which wrote a "yeivinID" attribute on every verse
of MAM-simple's vtmam files: Yeivin's spelling of the very chapter and verse the
osisID already gave, so "Rut 1:1" beside "Ruth.1.1".  Ben retired the attribute that
day, having had it written only so that he could search the corpus for references in
the form his Yeivin ITM adaptation uses, and having no plans to resume that work.

The table stays because it is the whole of what a yeivinID added to an osisID.  All
23,202 pairs in the shipped corpus were checked that day: the chapter and verse always
matched, and the book map below is one-to-one over all 39 books in both directions.  So
a yeivinID is reconstructible from an osisID and this table alone, and nothing was lost
by ceasing to write 23,202 copies of that derivation into the corpus.
"""

from mb_cmn import bib_locales as tbn

# As a regex: (Gen|Ex|Lev|Nu|Dt|Jos|Jud|1S|2S|1K|2K|Is|Jer|Ez|Hos|Joel|Amos|Ob|Jon|Mic|Nah|Hab|Zeph|Hag|Zech|Mal|Ps|Prov|Job|Song|Rut|Lam|Qoh|Est|Dan|Ezra|Neh|1C|2C)

BOOK_ABBREV_FROM_BK39ID = {
    tbn.BK_GENESIS: "Gen",
    tbn.BK_EXODUS: "Ex",
    tbn.BK_LEVIT: "Lev",
    tbn.BK_NUMBERS: "Nu",
    tbn.BK_DEUTER: "Dt",
    tbn.BK_JOSHUA: "Jos",
    tbn.BK_JUDGES: "Jud",
    tbn.BK_FST_SAM: "1S",
    tbn.BK_SND_SAM: "2S",
    tbn.BK_FST_KGS: "1K",
    tbn.BK_SND_KGS: "2K",
    tbn.BK_ISAIAH: "Is",
    tbn.BK_JEREM: "Jer",
    tbn.BK_EZEKIEL: "Ez",  # "Ez" would seem to collide with Ezra but full "Ezra" is used for Ezra
    tbn.BK_HOSHEA: "Hos",
    tbn.BK_JOEL: "Joel",
    tbn.BK_AMOS: "Amos",
    tbn.BK_OVADIAH: "Ob",
    tbn.BK_JONAH: "Jon",
    tbn.BK_MIKHAH: "Mic",
    tbn.BK_NAXUM: "Nah",
    tbn.BK_XABA: "Hab",
    tbn.BK_TSEF: "Zeph",
    tbn.BK_XAGGAI: "Hag",
    tbn.BK_ZEKHAR: "Zech",
    tbn.BK_MALAKHI: "Mal",
    tbn.BK_PSALMS: "Ps",
    tbn.BK_PROV: "Prov",
    tbn.BK_JOB: "Job",
    tbn.BK_SONG: "Song",
    tbn.BK_RUTH: "Rut",
    tbn.BK_LAMENT: "Lam",
    tbn.BK_QOHELET: "Qoh",
    tbn.BK_ESTHER: "Est",
    tbn.BK_DANIEL: "Dan",
    tbn.BK_EZRA: "Ezra",
    tbn.BK_NEXEM: "Neh",
    tbn.BK_FST_CHR: "1C",
    tbn.BK_SND_CHR: "2C",
}
