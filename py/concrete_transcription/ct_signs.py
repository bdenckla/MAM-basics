"""The trial's groups and their regions' seeds: Claude's reading, by eye, of the
image with the UXLC's text in hand.  Coordinates are the image's pixels.

Data of the concrete-transcription trial, 2026-11-03.  Each group is
(id, kind, owner, label, regions), each region (id, seeds).  The kinds are those
of the tracked py/pen_stroke/level5.py; the owners those of stroke_svg.INK_OWNERS.
"""

GROUPS = [
    (
        "g1",
        "yod letter",
        "this-word",
        "yod, the first letter",
        [("rg1", [(468, 62), (487, 112)])],
    ),
    (
        "g2",
        "pataḥ vowel",
        "this-word",
        "pataḥ under the first yod",
        [("rg2", [(482, 153)])],
    ),
    (
        "g3",
        "ayin letter",
        "this-word",
        "ayin",
        [("rg3", [(320, 64), (414, 76), (336, 118), (300, 168), (370, 135)])],
    ),
    (
        "g4",
        "ḥataf pataḥ vowel",
        "this-word",
        "ḥataf pataḥ under the ayin",
        [("rg4", [(376, 177)]), ("rg5", [(428, 147)]), ("rg6", [(434, 168)])],
    ),
    ("g5", "zayin letter", "this-word", "zayin", [("rg7", [(262, 64), (270, 128)])]),
    (
        "g6",
        "sheva mark",
        "this-word",
        "sheva under the zayin",
        [("rg8", [(275, 189)]), ("rg9", [(278, 210)])],
    ),
    ("g7", "resh letter", "this-word", "resh", [("rg10", [(205, 70), (232, 150)])]),
    (
        "g8",
        "qubuts vowel",
        "this-word",
        "qubuts under the resh",
        [("rg11", [(208, 199)]), ("rg12", [(224, 214)]), ("rg13", [(240, 230)])],
    ),
    (
        "g9",
        "silluq accent",
        "this-word",
        "silluq under the resh",
        [("rg14", [(177, 210)])],
    ),
    (
        "g10",
        "nun letter",
        "this-word",
        "nun",
        [("rg15", [(140, 62), (152, 140), (110, 180)])],
    ),
    (
        "g11",
        "ḥiriq vowel",
        "this-word",
        "ḥiriq under the nun",
        [("rg16", [(113, 215)])],
    ),
    (
        "g12",
        "yod letter",
        "this-word",
        "yod, the last letter",
        [("rg17", [(85, 76), (95, 115)])],
    ),
    (
        "g13",
        "sof pasuq mark",
        "this-word",
        "sof pasuq",
        [("rg18", [(36, 92)]), ("rg19", [(45, 130)])],
    ),
    (
        "g14",
        "stray mark",
        "this-word",
        "the stray stroke from within the resh through the nun",
        [("rg20", [(178, 102), (124, 106)])],
    ),
    (
        "g15",
        "unidentified letter",
        "other-word",
        "a letter of the atom before, cut by the image's edge",
        [("rg21", [(522, 60)]), ("rg22", [(525, 125)])],
    ),
    (
        "g16",
        "unidentified letter",
        "line-above",
        "a letter of the line above, cut by the image's edge",
        [("rg23", [(62, 30)])],
    ),
    (
        "g17",
        "masora circle mark",
        "this-line",
        "a masora circle",
        [("rg24", [(186, 20)])],
    ),
    (
        "g18",
        "unidentified letter",
        "line-below",
        "a letter of the line below, cut by the image's edge",
        [("rg25", [(502, 237)])],
    ),
    (
        "g19",
        "unidentified letter",
        "line-below",
        "ink of the line below, cut by the image's edge",
        [("rg26", [(91, 247)])],
    ),
]

# The atom's letter-and-mark clusters, by group, numbered from the right, as Ben
# gave them on 2026-11-04: "yod-patax, ayin-xpatax, zayin-sheva,
# resh-qubuts-silluq, nun-xiriq, yod, sof_pasuq".  The page can colour them in two
# colours by turns.
CLUSTERS = {
    "g1": 1,
    "g2": 1,
    "g3": 2,
    "g4": 2,
    "g5": 3,
    "g6": 3,
    "g7": 4,
    "g8": 4,
    "g9": 4,
    "g10": 5,
    "g11": 5,
    "g12": 6,
    "g13": 7,
}

# Short names for the page's labels and lists, by group.
SHORT = {
    "g1": "yod 1",
    "g2": "pataḥ",
    "g3": "ayin",
    "g4": "ḥataf pataḥ",
    "g5": "zayin",
    "g6": "sheva",
    "g7": "resh",
    "g8": "qubuts",
    "g9": "silluq",
    "g10": "nun",
    "g11": "ḥiriq",
    "g12": "yod 2",
    "g13": "sof pasuq",
    "g14": "stray stroke",
    "g15": "atom before",
    "g16": "line above",
    "g17": "masora circle",
    "g18": "line below",
    "g19": "line below",
}

# The names of the written parts of the groups of several, by region.
PART_NAMES = {
    "rg4": "bar",
    "rg5": "upper dot",
    "rg6": "lower dot",
    "rg8": "upper dot",
    "rg9": "lower dot",
    "rg11": "upper dot",
    "rg12": "middle dot",
    "rg13": "lower dot",
    "rg18": "upper dot",
    "rg19": "lower dot",
    "rg21": "upper piece",
    "rg22": "lower piece",
}

# The stray stroke, as a stroke: its centerline, by eye, from a point inside the
# resh's roof, through the ink between the resh and the nun, to the ink that
# shows left of the nun; and one width.  Its start inside the resh is a guess.
STROKE = {
    "id": "st1",
    "group": "g14",
    "centerline": [(212, 85), (182, 94), (163, 103), (128, 106)],
    "width": 14,
    "caps": ["flat", "round"],
}
# The draft region that the stroke replaces: the stroke's ink that shows.
STROKE_REGION = "rg20"

# Cuts, by eye, where the stray stroke's ink meets the letters' ink, so that the
# draft gives the stroke the ink it shows outside them.  Each runs from vellum to
# vellum along the edge that Claude infers a letter has under the stroke.
CUTS = [
    (
        "c1",
        "M 212 98 L 172 90 L 161 90 L 161 117",
        "the resh's roof's underside, and the nun's right edge, under the stroke",
    ),
    ("c2", "M 126 85 L 136 122", "the nun's left edge under the stroke's left end"),
]

# Judgments of level 1's residual pieces, by id, with Claude's reason.
JUDGMENTS = {
    "r1": ("speck", "a dark dot above the resh's roof, apart from every sign"),
    "r2": ("speck", "a dark dot of a few pixels above the last yod"),
    "r3": ("ink", "the left tip of the ḥataf pataḥ's bar, broken off by the threshold"),
}

# The page.  Its draft's name, which also names where the page keeps Ben's edits;
# a note on the draft, HTML that follows the page's introduction; the file that
# Download saves; and where Claude is least sure: each question's letter, a ring
# (x, y, r) and the letter's place, in vellum beside it, in the image's pixels;
# the questions' text, HTML; and the letters as the page's checkbox names them.
DRAFT_VERSION = "draft 1, Claude, 2026-11-03"
DRAFT_NOTE = ""
DOWNLOAD_NAME = "concrete-transcription-2026-11-03-edits.json"
QUESTIONS = [
    {"letter": "A", "ring": [212, 85, 7], "text": [216, 119]},
    {"letter": "B", "ring": [127, 106, 8], "text": [114, 93]},
    {"letter": "C", "ring": [161, 101, 8], "text": [175, 126]},
]
QUESTION_ITEMS = [
    (
        "A",
        "Where the stray stroke begins inside the resh is a guess. Drag the stroke's"
        " right end to where you think it begins.",
    ),
    (
        "B",
        "Is the stroke's left end where its ink shows left of the nun? Drag its end,"
        " or its width.",
    ),
    (
        "C",
        "Under the stroke, the resh's roof and the nun's head and stem are drawn"
        " straight across, Claude's guess at their edges. Drag their outlines where you"
        " see or infer the edges.",
    ),
]
QUESTION_LETTERS = "A to C"
