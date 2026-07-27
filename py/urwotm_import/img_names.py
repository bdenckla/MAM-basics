"""HAND-AUTHORED: positional image stem -> descriptive filename.

Positional stems (``p1-01``) are what the downloader can know on its own.
Descriptive names are what the repo actually uses, and they can only be
proposed after a human has looked at the images -- hence the contact sheets
at ``.novc/urwotm_cache/contact_sheet_pN.html``.

Names follow the existing ``misc/img/`` convention, e.g.

    "Deut 12v30 לאמר -- BHS.png"
    "Psalm 32v5 ועוני -- BHS.png"       (from tsinnorit_and_the_xxd_in_bhs)
    "rocc Judaica Press Psalm 32v5 ועוני.png"

Book, chapter``v``verse, the Hebrew word at issue, then ``--`` and the
source. The extension must match the downloaded format in the manifest;
``check_names`` enforces that.

Values are relative to ``misc/img/urwotm/``, which is what
``author.para_for_img`` gets prefixed with ``img/``.
"""

# Proposed from the prose around each image (the contact sheets, and the
# wider block window behind them). Where a run of images sits between two
# paragraphs with nothing said between them, the image itself was opened to
# settle the order; those are marked below.
#
# Each part turns out to be about one passage, so the book/chapter/verse
# prefix repeats and the source is what actually distinguishes the files:
#   Part 1  Deut 12:30 לאמר      Part 3  Josh 21:34-38
#   Part 2  2Sam 13:33, 15:21 אם Part 4  Psalm 5:10
NAMES = {
    # Part 1 -- Deut 12:30 לאמר, across manuscripts and editions.
    "p1-01": "Deut 12v30 לאמר -- L color.png",
    "p1-02": "Deut 12v30 לאמר -- BHS.png",
    "p1-03": "Deut 12v30 לאמר -- L black and white.png",
    "p1-04": "Deut 12v30 לאמר -- BHQ.png",
    "p1-05": "Deut 12v30 לאמר -- JPS HET.png",
    "p1-06": "Deut 12v30 לאמר -- Sassoon 507.png",
    "p1-07": "Deut 12v30 לאמר -- Sassoon 1053.png",
    "p1-08": "Deut 12v30 לאמר -- URJ ḥumash.png",
    #
    # Part 2 -- the two 2 Samuel kq cases. Every pair runs 13:33 then 15:21,
    # confirmed by opening p2-02 (כי־אם־אמנון) and p2-16 (כי אם).
    "p2-01": "2Sam 13v33 and 15v21 אם -- WLC qere ketiv.png",
    "p2-02": "2Sam 13v33 כי־אם־אמנון -- UXLC.png",
    "p2-03": "2Sam 15v21 אם־במקום -- UXLC.png",
    "p2-04": "2Sam 15v21 אם -- BHS masorah qetanah.png",
    # p2-05 is the ל marginal note אם כתׄ ולא קרי, given as an example of the
    # form; the prose does not say which of the two verses it is from.
    "p2-05": "2Sam אם -- L masorah qetanah.png",
    "p2-06": "Jer 51v3 ידרך -- L masorah gedolah page 274B.png",
    # p2-07..p2-10: body text then note, for each verse in turn. Opened
    # p2-07 (כי־אם*) and p2-08 (v. 33 כתיב ולא קריא) to fix the pattern.
    "p2-07": "2Sam 13v33 כי־אם -- JPS HET.png",
    "p2-08": "2Sam 13v33 כי־אם -- JPS HET note.png",
    "p2-09": "2Sam 15v21 אם־במקום -- JPS HET.png",
    "p2-10": "2Sam 15v21 אם־במקום -- JPS HET note.png",
    "p2-11": "2Sam 15v21 אם -- BHS masorah circles.png",
    "p2-12": "2Sam 15v21 -- BHS masorah qetanah notes.png",
    "p2-13": "2Sam 15v21 ויאמר -- BHS masorah circle.png",
    "p2-14": "2Sam 3v33 ויאמר -- BHS masorah qetanah.png",
    "p2-15": "Jer 22v12 -- BHS masorah qetanah.png",
    "p2-16": "2Sam 13v33 כי אם -- Aleppo.png",
    "p2-17": "2Sam 15v21 אם -- Aleppo.png",
    "p2-18": "2Sam 13v33 כי־אם־אמנון -- MAM Wikisource.png",
    "p2-19": "2Sam 15v21 אם־במקום -- MAM Wikisource.png",
    "p2-20": "2Sam 13v33 כי־אם־אמנון -- long maqaf alternative.png",
    #
    # Part 3 -- Joshua 21:34-38 and the two verses ל does not have.
    "p3-01": "Josh 21v34-38 -- WLC schematic.png",
    "p3-02": "Josh 21v34-38 -- L page 133B.png",
    "p3-03": "Josh 21v34-38 -- L schematic.png",
    "p3-04": "Josh 21v34-38 -- BHS small type.jpg",
    "p3-05": "Josh 21v34-38 -- Aleppo.png",
    "p3-06": "Josh 21v35 את־דמנה -- Aleppo missing sof pasuq.png",
    "p3-07": "Josh 21v34-38 -- Sassoon 1053 page 212.png",
    "p3-08": "Josh 21v34-38 -- Sassoon 1053 page 213.png",
    "p3-09": "Josh 21v34 זבולן -- Sassoon 1053 cut off nun.png",
    "p3-10": "Josh 21v36-37 -- UXLC gray setumah.png",
    "p3-11": "Josh 21v36 -- JPS HET asterisk.png",
    "p3-12": "Josh 21v36 -- JPS HET note.png",
    "p3-13": "Josh 21v35 -- BHL note.png",
    "p3-14": "Josh 21v36-37 -- Zondervan RHB.png",
    #
    # Part 4 -- Psalm 5:10, then the two BHS accent sub-tables and Ben's
    # "galfukh" rewrite of each. p4-02 and p4-03 are two lines of the one
    # Aleppo excerpt, not two manuscripts; p4-07/p4-09 are the prose
    # sub-table's item 26 and p4-08/p4-10 the poetic sub-table's item 17
    # (opened to confirm).
    "p4-01": "Psalm 5v10 -- MAM with doc.png",
    "p4-02": "Psalm 5v10 -- Aleppo line 1.png",
    "p4-03": "Psalm 5v10 -- Aleppo line 2.png",
    "p4-04": "Psalm 5v10 -- L.png",
    "p4-05": "Psalm 5v10 -- Sassoon 1053.png",
    "p4-06": "Psalm 5v10 -- BHS.jpg",
    "p4-07": "BHS table of accents 26 galgal -- prose.png",
    "p4-08": "BHS table of accents 17 galgal -- poetic.png",
    "p4-09": "BHS table of accents 26 galfukh -- prose.png",
    "p4-10": "BHS table of accents 17 galfukh -- poetic.png",
}


def descriptive(stem: str, fallback_file: str) -> str:
    """The name to use for one image, positional until Ben has named it."""
    return NAMES.get(stem, fallback_file)


def check_names(refs):
    """Every named image exists in the manifest with a matching extension."""
    by_stem = {ref["stem"]: ref for ref in refs}
    problems = []
    for stem, name in NAMES.items():
        ref = by_stem.get(stem)
        if ref is None:
            problems.append(f"{stem}: named but not in the manifest")
            continue
        if not name.lower().endswith("." + ref["format"]):
            problems.append(f"{stem}: name {name!r} is not a .{ref['format']}")
    unnamed = sorted(set(by_stem) - set(NAMES))
    return problems, unnamed
