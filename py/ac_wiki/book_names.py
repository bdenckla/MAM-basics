from mb_cmn import mam_bknas as mbn

LATIN_TO_HEBREW = {
    # BS_GENESIS
    # BS_EXODUS
    # BS_LEVIT
    # BS_NUMBERS
    "Deut": mbn.BS_DEUTER[0],
    "Josh": mbn.BS_JOSHUA[0],
    "Judg": mbn.BS_JUDGES[0],
    "1 Sam": mbn.he_bk39_name(*mbn.BS_FST_SAM),
    "2 Sam": mbn.he_bk39_name(*mbn.BS_SND_SAM),
    "1 Kgs": mbn.he_bk39_name(*mbn.BS_FST_KGS),
    "2 Kgs": mbn.he_bk39_name(*mbn.BS_SND_KGS),
    "Isa": mbn.BS_ISAIAH[0],
    "Jer": mbn.BS_JEREM[0],
    "Ezek": mbn.BS_EZEKIEL[0],
    "Hos": mbn.BS_HOSEA[1],
    "Joel": mbn.BS_JOEL[1],
    "Amos": mbn.BS_AMOS[1],
    # BS_OBADIAH
    # BS_JONAH
    "Mic": mbn.BS_MICAH[1],
    "Nah": mbn.BS_NAXUM[1],
    "Hab": mbn.BS_XABA[1],
    "Zeph": mbn.BS_TSEF[1],
    # BS_XAGGAI
    "Zech": mbn.BS_ZEKHAR[1],
    "Mal": mbn.BS_MALAKHI[1],
    "1 Chron": mbn.he_bk39_name(*mbn.BS_FST_CHR),
    "2 Chron": mbn.he_bk39_name(*mbn.BS_SND_CHR),
    "Ps": mbn.BS_PSALMS[0],
    "Job": mbn.BS_JOB[0],
    "Prov": mbn.BS_PROV[0],
    "Ruth": mbn.BS_RUTH[0],
    "Song": mbn.BS_SONG[0],
    # BS_LAMENT
    # BS_QOHELET
    # BS_ESTHER
    # BS_DANIEL
    # BS_EZRA
    # BS_NEXEM
}
