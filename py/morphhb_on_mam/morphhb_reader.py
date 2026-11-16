"""morphhb's wlc/<OSIS>.xml files, and the form keys that the alignment compares.

Written by Claude (Opus 5.5) as the 2026-11-13 study's mhb_common.py, which the 2026-11-15
morphhb-on-MAM study copied unchanged, and trimmed on 2026-11-16, when that study was put on
ice (morphhb-on-mam/README.md), to what the study's pipeline uses: its readers of WLC 4.18,
4.20 and 4.22 went, with every path into another checkout or into .novc/, and morphhb_path
now names a book's file in a flat wlc/ directory, as a morphhb checkout has it.

The reader dispatches explicitly on the elements its census found and raises on any other.

- morphhb's wlc/<OSIS>.xml at db6c5c9b (OSIS 2.1.1), whose files are d4265dfa's:
  read_morphhb_book.
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from author_misc import israel_bible_review_index as ib_review
from mb_cmn.uni_denorm import give_std_mark_order

NS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
CGJ = "\N{COMBINING GRAPHEME JOINER}"

# (OSIS id = morphhb file stem, tanach.us file name, Michigan-Claremont abbreviation)
BOOKS = [
    ("Gen", "Genesis", "gn"),
    ("Exod", "Exodus", "ex"),
    ("Lev", "Leviticus", "lv"),
    ("Num", "Numbers", "nu"),
    ("Deut", "Deuteronomy", "dt"),
    ("Josh", "Joshua", "js"),
    ("Judg", "Judges", "ju"),
    ("1Sam", "Samuel_1", "1s"),
    ("2Sam", "Samuel_2", "2s"),
    ("1Kgs", "Kings_1", "1k"),
    ("2Kgs", "Kings_2", "2k"),
    ("Isa", "Isaiah", "is"),
    ("Jer", "Jeremiah", "je"),
    ("Ezek", "Ezekiel", "ek"),
    ("Hos", "Hosea", "ho"),
    ("Joel", "Joel", "jl"),
    ("Amos", "Amos", "am"),
    ("Obad", "Obadiah", "ob"),
    ("Jonah", "Jonah", "jn"),
    ("Mic", "Micah", "mi"),
    ("Nah", "Nahum", "na"),
    ("Hab", "Habakkuk", "hb"),
    ("Zeph", "Zephaniah", "zp"),
    ("Hag", "Haggai", "hg"),
    ("Zech", "Zechariah", "zc"),
    ("Mal", "Malachi", "ma"),
    ("Ps", "Psalms", "ps"),
    ("Prov", "Proverbs", "pr"),
    ("Job", "Job", "jb"),
    ("Song", "Song_of_Songs", "ca"),
    ("Ruth", "Ruth", "ru"),
    ("Lam", "Lamentations", "lm"),
    ("Eccl", "Ecclesiastes", "ec"),
    ("Esth", "Esther", "es"),
    ("Dan", "Daniel", "da"),
    ("Ezra", "Ezra", "er"),
    ("Neh", "Nehemiah", "ne"),
    ("1Chr", "Chronicles_1", "1c"),
    ("2Chr", "Chronicles_2", "2c"),
]
HEB_LETTER = re.compile("[\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")


def local(tag):
    return tag[len(NS) :] if tag.startswith(NS) else tag


def letters(s):
    """The letters alone, final forms kept."""
    return "".join(HEB_LETTER.findall(s))


def skey(s):
    """The review's comparison key (israel_bible_review_index.key): accents, meteg, rafeh,
    paseq, sof pasuq, the dots and invisible marks stripped, qamats qatan read as qamats and
    holam haser for vav as holam, then each letter's marks sorted.  '/' is dropped first.
    """
    return ib_review.key(s.replace("/", ""))


def fkey(s):
    """A full key: every mark kept, each letter's marks sorted, '/' and CGJ dropped."""
    s = s.replace("/", "").replace(CGJ, "")
    out, cluster = [], []
    for ch in s:
        if ib_review.is_mark(ch):
            cluster.append(ch)
        else:
            out.extend(sorted(cluster))
            cluster = []
            out.append(ch)
    out.extend(sorted(cluster))
    return "".join(out)


def mnorm(s):
    """A form in MAM-normal mark order, for display."""
    return give_std_mark_order(s)


# ------------------------------------------------------------------ morphhb


def morphhb_path(wlc_dir, osis):
    """A book's file in a flat wlc/ directory, as a morphhb checkout has it."""
    return Path(wlc_dir) / (osis + ".xml")


LETTER_SEG_TYPES = {"x-large", "x-small", "x-suspended"}


def _w_record(el, where, in_qere):
    for name in el.attrib:
        if name not in ("lemma", "morph", "id", "n", "type"):
            raise ValueError("%s: unknown w attribute %r" % (where, name))
    if el.get("type") not in (None, "x-ketiv"):
        raise ValueError("%s: unknown w type %r" % (where, el.get("type")))
    for c in el:
        if local(c.tag) != "seg" or c.get("type") not in LETTER_SEG_TYPES or list(c):
            raise ValueError("%s: w child %r %r" % (where, local(c.tag), c.attrib))
    return {
        "kind": "w",
        "text": "".join(el.itertext()),
        "lemma": el.get("lemma"),
        "morph": el.get("morph"),
        "id": el.get("id"),
        "n": el.get("n"),
        "type": el.get("type"),
        "in_qere": in_qere,
        "maqaf_after": False,
        "letter_segs": [c.get("type") for c in el],
        "notes_after": [],
    }


VERSE_SEG_TYPES = {
    "x-maqqef",
    "x-sof-pasuq",
    "x-paseq",
    "x-pe",
    "x-samekh",
    "x-reversednun",
}


def read_morphhb_book(path):
    """{osisID: verse} where a verse is {"toks": [...], "ketiv_side": [...], "qere_side":
    [...]}.  toks are every child in document order: w, seg and note records.  ketiv_side is
    every w outside a qere's rdg; qere_side replaces each run of x-ketiv words with the
    following variant note's qere words.  maqaf_after is set on a w that a maqqef seg follows:
    a seg of subType x-ketiv marks the ketiv side only."""
    root = ET.parse(path).getroot()
    verses = {}
    for verse in root.iter(NS + "verse"):
        osis_id = verse.get("osisID")
        toks, ketiv_side, qere_side, pending = [], [], [], []
        for child in verse:
            tag = local(child.tag)
            where = "%s %s" % (osis_id, tag)
            if tag == "w":
                rec = _w_record(child, where, False)
                toks.append(rec)
                ketiv_side.append(rec)
                if rec["type"] == "x-ketiv":
                    pending.append(rec)
                else:
                    if pending:
                        raise ValueError("%s: ketiv without its qere note" % where)
                    qere_side.append(rec)
            elif tag == "seg":
                st, sub = child.get("type"), child.get("subType")
                if st not in VERSE_SEG_TYPES or list(child):
                    raise ValueError("%s: seg %r" % (where, child.attrib))
                if sub not in (None, "x-ketiv") or (sub and st != "x-maqqef"):
                    raise ValueError("%s: seg subType %r" % (where, sub))
                if st == "x-maqqef":
                    ketiv_side[-1]["maqaf_after"] = True
                    if sub is None:
                        if pending:
                            raise ValueError("%s: maqqef inside a ketiv run" % where)
                        qere_side[-1]["maqaf_after"] = True
                toks.append(
                    {"kind": "seg", "type": st, "subType": sub, "text": child.text}
                )
            elif tag == "note":
                rec = _note_record(child, where)
                toks.append(rec)
                if rec["type"] != "variant":
                    if ketiv_side:
                        ketiv_side[-1]["notes_after"].append(rec)
                    if qere_side and qere_side[-1] is not (
                        ketiv_side[-1] if ketiv_side else None
                    ):
                        qere_side[-1]["notes_after"].append(rec)
                if rec["type"] == "variant":
                    if bool(pending) != (rec["catchWord"] is not None):
                        raise ValueError("%s: ketiv run and catchWord disagree" % where)
                    qere_side.extend(rec["qere"])
                    pending = []
            else:
                raise ValueError("%s: unknown verse child %r" % (where, tag))
        if pending:
            raise ValueError("%s: ketiv without its qere note at verse end" % osis_id)
        verses[osis_id] = {
            "toks": toks,
            "ketiv_side": ketiv_side,
            "qere_side": qere_side,
        }
    return verses


def _note_record(el, where):
    ntype = el.get("type")
    rec = {
        "kind": "note",
        "n": el.get("n"),
        "type": ntype,
        "text": "".join(el.itertext()).strip(),
        "qere": [],
        "accent": None,
        "catchWord": None,
        "rdg": None,
    }
    kids = [local(c.tag) for c in el]
    if ntype is None:
        if kids:
            raise ValueError("%s: plain note with children %r" % (where, kids))
        return rec
    if ntype == "exegesis":
        if kids not in ([], ["rdg"]):
            raise ValueError("%s: exegesis note children %r" % (where, kids))
        for c in el:
            if c.get("type") is not None or list(c):
                raise ValueError("%s: exegesis rdg %r" % (where, c.attrib))
            rec["rdg"] = c.text
        return rec
    if ntype == "variant" and kids == ["rdg"]:
        # A qere velo ketiv: a qere with no ketiv, so no catchWord.
        catch, rdg = None, el[0]
    elif ntype in ("variant", "alternative") and kids == ["catchWord", "rdg"]:
        catch, rdg = list(el)
        if list(catch):
            raise ValueError("%s: catchWord with children" % where)
        rec["catchWord"] = catch.text
    else:
        raise ValueError("%s: note %r children %r" % (where, ntype, kids))
    if ntype == "alternative":
        if rdg.get("type") != "x-accent" or list(rdg):
            raise ValueError("%s: alternative rdg %r" % (where, rdg.attrib))
        rec["accent"] = rdg.text
        return rec
    if rdg.get("type") != "x-qere":
        raise ValueError("%s: variant rdg type %r" % (where, rdg.get("type")))
    for g in rdg:
        gtag = local(g.tag)
        if gtag == "w":
            rec["qere"].append(_w_record(g, where + " rdg", True))
        elif gtag == "seg" and g.get("type") == "x-maqqef" and not list(g):
            rec["qere"][-1]["maqaf_after"] = True
        elif gtag == "seg" and g.get("type") == "x-paseq" and not list(g):
            pass
        else:
            raise ValueError("%s: rdg child %r %r" % (where, gtag, g.attrib))
    return rec


def w_atom(t):
    return t["text"].replace("/", "") + (MAQAF if t["maqaf_after"] else "")
