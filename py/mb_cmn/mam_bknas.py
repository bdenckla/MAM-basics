"""
Exports 1 function & a bunch of BS_.* pairs.
The 1 function is he_bk39_name.
A BS_.* pair is a book/sub-book pair.
The 1st part of a BS_.* pair is a bk24 string.
The 2nd part of a BS_.* pair is either None or a sub-book string.
"""

# BS: Hebrew book name (B) and Hebrew sub-book name (S).
#
# There are 24 books, for this definition of "book".
#
# 4 of these books are divided into 2 sub-books.
# 1 of these books is divided into 12 sub-books.
# 24 - 4 - 1 + 8 + 12 = 39 "chapter spans"
#
# Some other systems consider chapter spans to be books.
# In such systems, there are 39 books. Thus we sometimes refer to a book of
# this type as a "bk39", and we sometimes refer to the other kind of book as
# a "bk24".
#
# The chapter numbers of a chapter span always range from 1 to N.
# The 5 divisions of the Psalms are not chapter spans since their chapter
# numbers do not range from 1 to N. (Psalm chapter numbers aren't really
# chapter numbers, they are Psalm numbers, but that is a separate issue.)
#
BS_GENESIS = "ספר בראשית", None
BS_EXODUS = "ספר שמות", None
BS_LEVIT = "ספר ויקרא", None
BS_NUMBERS = "ספר במדבר", None
BS_DEUTER = "ספר דברים", None
BS_JOSHUA = "ספר יהושע", None
BS_JUDGES = "ספר שופטים", None
BS_FST_SAM = str("ספר שמואל"), str('שמ"א')  # str used to solve RTL issues
BS_SND_SAM = str("ספר שמואל"), str('שמ"ב')
BS_FST_KGS = str("ספר מלכים"), str('מל"א')
BS_SND_KGS = str("ספר מלכים"), str('מל"ב')
BS_ISAIAH = "ספר ישעיהו", None
BS_JEREM = "ספר ירמיהו", None
BS_EZEKIEL = "ספר יחזקאל", None
BS_HOSEA = str("ספר תרי עשר"), str("הושע")
BS_JOEL = str("ספר תרי עשר"), str("יואל")
BS_AMOS = str("ספר תרי עשר"), str("עמוס")
BS_OBADIAH = str("ספר תרי עשר"), str("עבדיה")
BS_JONAH = str("ספר תרי עשר"), str("יונה")
BS_MICAH = str("ספר תרי עשר"), str("מיכה")
BS_NAXUM = str("ספר תרי עשר"), str("נחום")
BS_XABA = str("ספר תרי עשר"), str("חבקוק")
BS_TSEF = str("ספר תרי עשר"), str("צפניה")
BS_XAGGAI = str("ספר תרי עשר"), str("חגי")
BS_ZEKHAR = str("ספר תרי עשר"), str("זכריה")
BS_MALAKHI = str("ספר תרי עשר"), str("מלאכי")
BS_PSALMS = "ספר תהלים", None
BS_PROV = "ספר משלי", None
BS_JOB = "ספר איוב", None
BS_SONG = "מגילת שיר השירים", None
BS_RUTH = "מגילת רות", None
BS_LAMENT = "מגילת איכה", None
BS_QOHELET = "מגילת קהלת", None
BS_ESTHER = "מגילת אסתר", None
BS_DANIEL = "ספר דניאל", None
BS_EZRA = str("ספר עזרא"), str("עזרא")
BS_NEXEM = str("ספר עזרא"), str("נחמיה")
BS_FST_CHR = str("ספר דברי הימים"), str('דה"א')
BS_SND_CHR = str("ספר דברי הימים"), str('דה"ב')
_BOOK24_AND_SUB_TO_BOOK39 = {
    BS_FST_SAM: "שמואל א",
    BS_SND_SAM: "שמואל ב",
    BS_FST_KGS: "מלכים א",
    BS_SND_KGS: "מלכים ב",
    BS_FST_CHR: "דברי הימים א",
    BS_SND_CHR: "דברי הימים ב",
}


def he_bk39_name(bk24na, sub_bkna):
    """
    Given bk24 name bk24na & sub-book name sub_bkna, return the
    corresponding bk39 name. Output and both inputs are expected to be
    Hebrew.
    """
    if sub_bkna is None:
        return _strip_sfr_or_mgylt(bk24na)
    if bk24na in ("ספר תרי עשר", "ספר עזרא"):
        # Unfortunately Ovadiah is spelled xaser-style (without a vav)
        # as a sub-book and it is spelled malei-style (i.e. with a vav)
        # as an argument to the מ:פסוק template.
        if sub_bkna == "עבדיה":
            return "עובדיה"
        return sub_bkna
    return _BOOK24_AND_SUB_TO_BOOK39[(bk24na, sub_bkna)]


def _strip_sfr_or_mgylt(bkna):
    for prefix in ("ספר", "מגילת"):
        prefix_sp = prefix + " "
        if bkna.startswith(prefix_sp):
            return bkna[len(prefix_sp) :]
    return bkna
