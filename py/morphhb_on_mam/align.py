"""Align morphhb's words with MAM's atoms and classify every MAM atom.

Written by Claude (Opus 5.5) on 2026-11-15 for the morphhb-on-MAM feasibility study, and moved
into this package on 2026-11-16, when the study was put on ice (morphhb-on-mam/README.md).

Inputs:
- morphhb's wlc/<book>.xml at db6c5c9b (identical to d4265dfa's), from the flat wlc/
  directory given to run(), which py/main_morphhb_on_mam.py verify-morphhb checks blob by
  blob against morphhb-on-mam/in/fetched/morphhb-wlctree-1.json; read by morphhb_reader.py,
  whose closed dispatch raises on any unknown element.
- MAM: MAM-simple's JSON in the BHS versification, read by mam_reader.py (closed dispatch on
  MAM-simple's element types), strand cant-combined unless another is asked for.

The alignment is the 2026-11-13 study's "Method 2": per verse and per side (ketiv side, qere
side), difflib's opcodes over the letters of whole atoms (final forms distinct).  Each MAM
atom is classified once, from the sides it is on:
  A1  letters equal, one morphhb word, and the vowel key equal (accents, meteg, rafeh and
      invisible marks ignored; qamats qatan read as qamats, holam haser as holam)
  A2  letters equal, one morphhb word, the vowel key differs
  K   a MAM ketiv (unpointed) whose letters equal one morphhb ketiv word's
  AX  letters equal on each side, but a different morphhb word on each side
  B   one-to-one with one morphhb word whose letters differ
  C   anything else: an n-to-m block, or no morphhb word at all
Morphhb words that no MAM atom matches (difflib "delete" blocks) are listed separately.

run(wlc_dir, work_dir, out_dir, strand) writes <work_dir>/10-atoms<suffix>.jsonl and
11-unmatched-morphhb<suffix>.jsonl, and <out_dir>/12-align-summary<suffix>.txt, where suffix
is "" for cant-combined and "-<strand>" otherwise.
"""

import collections
import difflib
import json
import re
import time
from pathlib import Path

from morphhb_on_mam import mam_reader as M
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths

IB = C.ib_review
SLASH = "/"

# A lemma: prefix letters, each with "/", then the main word (p2_lemma_lib.LEMMA_RE, copied).
LEMMA_RE = re.compile(r"((?:[bcdiklms]/)*)(?:(\d+)( [a-f])?(\+)?|([bklmi]))")


def lemma_number(lemma):
    m = LEMMA_RE.fullmatch(lemma)
    if not m:
        raise ValueError("unknown lemma shape %r" % lemma)
    return m.group(2) if m.group(2) else m.group(5)


def morph_parts(morph):
    if not morph or morph[0] not in "HA":
        raise ValueError("unknown morph %r" % morph)
    parts = morph[1:].split("/")
    for p in parts:
        if not p or p[0] not in "NVRCTSAPD":
            raise ValueError("unknown morph part %r in %r" % (p, morph))
    return parts


def is_letter(ch):
    return "\N{HEBREW LETTER ALEF}" <= ch <= "\N{HEBREW LETTER TAV}"


def vkey(text):
    """The 2026-11-13 study's form key: israel_bible_review_index.key, '/' dropped."""
    return C.skey(text)


def strict_clusters(text):
    """[(letter, sorted kept marks)]: accents, meteg, rafeh, dots and invisible marks
    stripped as the key strips them, but qamats qatan and holam haser kept distinct."""
    s = IB.STRIP.sub("", text.replace(SLASH, ""))
    out = []
    for ch in s:
        if is_letter(ch):
            out.append([ch, []])
        elif IB.is_mark(ch):
            if not out:
                raise ValueError("mark before a letter in %r" % text)
            out[-1][1].append(ch)
        else:
            raise ValueError("unexpected %r in %r" % (ch, text))
    return [(l, tuple(sorted(m))) for l, m in out]


VOWELS = {
    "\N{HEBREW POINT SHEVA}": "shewa",
    "\N{HEBREW POINT HATAF SEGOL}": "hataf-segol",
    "\N{HEBREW POINT HATAF PATAH}": "hataf-patah",
    "\N{HEBREW POINT HATAF QAMATS}": "hataf-qamats",
    "\N{HEBREW POINT HIRIQ}": "hiriq",
    "\N{HEBREW POINT TSERE}": "tsere",
    "\N{HEBREW POINT SEGOL}": "segol",
    "\N{HEBREW POINT PATAH}": "patah",
    "\N{HEBREW POINT QAMATS}": "qamats",
    "\N{HEBREW POINT HOLAM}": "holam",
    "\N{HEBREW POINT HOLAM HASER FOR VAV}": "holam-haser",
    "\N{HEBREW POINT QUBUTS}": "qubuts",
    "\N{HEBREW POINT QAMATS QATAN}": "qamats-qatan",
}
OTHER_MARKS = {
    "\N{HEBREW POINT DAGESH OR MAPIQ}": "dagesh",
    "\N{HEBREW POINT SHIN DOT}": "shin-dot",
    "\N{HEBREW POINT SIN DOT}": "sin-dot",
}


def mark_name(ch):
    if ch in VOWELS:
        return VOWELS[ch]
    if ch in OTHER_MARKS:
        return OTHER_MARKS[ch]
    raise ValueError("unnamed kept mark %r" % ch)


def signature(w_text, m_text):
    """For two forms with the same letters: [(letter index, letter, morphhb's marks, MAM's
    marks)] at each letter whose kept marks differ (strict clusters)."""
    a, b = strict_clusters(w_text), strict_clusters(m_text)
    if [l for l, _ in a] != [l for l, _ in b]:
        raise ValueError("letters differ: %r %r" % (w_text, m_text))
    out = []
    for k, ((l, ma), (_l, mb)) in enumerate(zip(a, b)):
        if ma != mb:
            out.append((k, l, [mark_name(c) for c in ma], [mark_name(c) for c in mb]))
    return out


def slash_positions(w_text):
    """The letter counts before each '/' of a morphhb word, and whether every '/' is
    followed directly by a letter."""
    pos, n, ok = [], 0, True
    for idx, ch in enumerate(w_text):
        if is_letter(ch):
            n += 1
        elif ch == SLASH:
            nxt = w_text[idx + 1] if idx + 1 < len(w_text) else ""
            if not is_letter(nxt):
                ok = False
            pos.append(n)
    return pos, ok


def insert_slashes(m_text, pos):
    """MAM's text with '/' before its letter number p (0-based) for each p in pos."""
    want = collections.Counter(pos)
    out, n = [], 0
    for ch in m_text:
        if is_letter(ch):
            out.extend(SLASH * want.pop(n, 0))
            n += 1
        out.append(ch)
    if want:
        raise ValueError("slash positions %r beyond %r" % (dict(want), m_text))
    return "".join(out)


def map_slashes_by_letters(w_letters, m_letters, pos):
    """Positions in MAM's letters for slash positions in morphhb's, through an alignment of
    the letters; None for a slash whose two neighbours are not both matched letters."""
    sm = difflib.SequenceMatcher(None, w_letters, m_letters, autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                amap[i] = j1 + (i - i1)
    out = []
    for p in pos:
        left, right = amap.get(p - 1), amap.get(p)
        if left is not None and right is not None and right == left + 1:
            out.append(right)
        else:
            out.append(None)
    return out


def w_summary(w):
    return {
        "id": w["id"],
        "text": w["text"],
        "lemma": w["lemma"],
        "morph": w["morph"],
        "type": w["type"],
        "in_qere": w["in_qere"],
        "maqaf_after": w["maqaf_after"],
    }


def build_index(books):
    """Every morphhb word (ketiv side and qere words) by its vowel key: Counters of the
    lemma's main number, the morph, and the two together."""
    idx = {
        k: collections.defaultdict(collections.Counter)
        for k in ("lemma", "morph", "pair")
    }
    for book in books.values():
        for verse in book.values():
            seen = set()
            for w in verse["ketiv_side"] + [
                x for x in verse["qere_side"] if x["in_qere"]
            ]:
                if w["id"] in seen:
                    continue
                seen.add(w["id"])
                f = vkey(w["text"])
                ln = lemma_number(w["lemma"])
                idx["lemma"][f][ln] += 1
                idx["morph"][f][w["morph"]] += 1
                idx["pair"][f][ln + " | " + w["morph"]] += 1
    return idx


def consistency(idx, m_text, w):
    """How morphhb analyses MAM's form elsewhere: n occurrences, and how many of them carry
    this word's lemma number, morph and both."""
    f = vkey(m_text)
    ln = lemma_number(w["lemma"])
    pair = idx["pair"].get(f, collections.Counter())
    return {
        "n": sum(pair.values()),
        "pair": pair.get(ln + " | " + w["morph"], 0),
        "lemma": idx["lemma"].get(f, collections.Counter()).get(ln, 0),
        "morph": idx["morph"].get(f, collections.Counter()).get(w["morph"], 0),
        "top": pair.most_common(1)[0] if pair else None,
    }


def run(wlc_dir, work_dir, out_dir, strand="cant-combined"):
    """Align one strand of MAM with morphhb, writing the records and the summary."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    suffix = "" if strand == "cant-combined" else "-" + strand
    t0 = time.time()
    books = {
        osis: C.read_morphhb_book(C.morphhb_path(wlc_dir, osis))
        for osis, _t, _m in C.BOOKS
    }
    print("read morphhb (%.0fs)" % (time.time() - t0))
    mam = M.read_mam(strand)
    print("read MAM (%.0fs)" % (time.time() - t0))
    idx = build_index(books)
    m_vids = set(mam)
    w_vids = {vid for b in books.values() for vid in b}
    counts = collections.Counter()
    counts["verses in morphhb"] = len(w_vids)
    counts["verses in MAM-simple (BHS)"] = len(m_vids)
    counts["verses in morphhb only"] = len(w_vids - m_vids)
    counts["verses in MAM-simple only"] = len(m_vids - w_vids)
    if w_vids - m_vids or m_vids - w_vids:
        print(
            "verse sets differ:",
            sorted(w_vids - m_vids)[:10],
            sorted(m_vids - w_vids)[:10],
        )
    recs_out = open(
        work_dir / ("10-atoms%s.jsonl" % suffix), "w", encoding="utf-8", newline="\n"
    )
    unm_out = open(
        work_dir / ("11-unmatched-morphhb%s.jsonl" % suffix),
        "w",
        encoding="utf-8",
        newline="\n",
    )
    by_class = collections.Counter()
    for osis, _t, _m in C.BOOKS:
        for vid, verse in books[osis].items():
            if vid not in mam:
                counts["morphhb verses skipped: not in MAM-simple"] += 1
                continue
            mv = mam[vid]
            recs = {}
            order = []
            words = {"k": verse["ketiv_side"], "q": verse["qere_side"]}
            for side in ("k", "q"):
                atoms = mv.sides[side]
                ws = words[side]
                ops = difflib.SequenceMatcher(
                    None,
                    [C.letters(w["text"]) for w in ws],
                    [a["letters"] for a in atoms],
                    autojunk=False,
                ).get_opcodes()
                for tag, i1, i2, j1, j2 in ops:
                    if tag == "delete":
                        for i in range(i1, i2):
                            unm_out.write(
                                json.dumps(
                                    {
                                        "vid": vid,
                                        "side": side,
                                        "i": i,
                                        "w": w_summary(ws[i]),
                                        "absent_verse": mv.absent,
                                    },
                                    ensure_ascii=False,
                                )
                                + "\n"
                            )
                            counts[
                                "morphhb side words with no MAM atom (%s)" % side
                            ] += 1
                        continue
                    for j in range(j1, j2):
                        a = atoms[j]
                        key = a["span"]
                        if key not in recs:
                            recs[key] = {"atom": a, "sides": {}}
                            order.append(key)
                        w_is = (
                            [i1 + (j - j1)] if tag == "equal" else list(range(i1, i2))
                        )
                        recs[key]["sides"][side] = {
                            "j": j,
                            "op": tag,
                            "n_w": i2 - i1,
                            "n_m": j2 - j1,
                            "w": w_is,
                            "pos": i1 + (j - j1) if i2 - i1 == j2 - j1 else None,
                        }
            for key in order:
                r = recs[key]
                a = r["atom"]
                sides = r["sides"]
                rec = {
                    "vid": vid,
                    "on": "".join(sorted(sides)),
                    "j": {s: sides[s]["j"] for s in sides},
                    "text": a["text"],
                    "kinds": a["kinds"],
                    "flags": a["flags"],
                    "maqaf_after": a["maqaf_after"],
                    "implicit_maqaf": a["implicit_maqaf"],
                    "boundary_added": a.get("boundary_added", False),
                    "ops": {
                        s: [sides[s]["op"], sides[s]["n_w"], sides[s]["n_m"]]
                        for s in sides
                    },
                }
                partners = {}
                for s, info in sides.items():
                    partners[s] = [words[s][i] for i in info["w"]]
                ops_set = {sides[s]["op"] for s in sides}
                one_to_one = all(
                    sides[s]["n_w"] == 1 and sides[s]["n_m"] == 1 for s in sides
                ) or ops_set == {"equal"}
                ids = {tuple(w["id"] for w in partners[s]) for s in sides}
                if ops_set == {"equal"}:
                    if len(ids) == 1:
                        (w,) = next(iter(partners.values()))
                        rec["w"] = w_summary(w)
                        if rec["on"] == "k":
                            cls = "K"
                        elif vkey(w["text"]) == vkey(a["text"]):
                            cls = "A1"
                        else:
                            cls = "A2"
                            rec["sig"] = signature(w["text"], a["text"])
                            rec["cons"] = consistency(idx, a["text"], w)
                    else:
                        cls = "AX"
                        rec["ws"] = {
                            s: [w_summary(w) for w in partners[s]] for s in partners
                        }
                elif one_to_one and "equal" not in ops_set and len(ids) == 1:
                    (w,) = next(iter(partners.values()))
                    rec["w"] = w_summary(w)
                    cls = "B"
                    rec["cons"] = consistency(idx, a["text"], w)
                elif (
                    ops_set == {"replace"}
                    and all(sides[s]["pos"] is not None for s in sides)
                    and len({words[s][sides[s]["pos"]]["id"] for s in sides}) == 1
                    and difflib.SequenceMatcher(
                        None,
                        C.letters(
                            words[next(iter(sides))][sides[next(iter(sides))]["pos"]][
                                "text"
                            ]
                        ),
                        a["letters"],
                        autojunk=False,
                    ).ratio()
                    >= 0.5
                ):
                    # An n-to-n block, paired word by word: each pair's letters differ.
                    w = words[next(iter(sides))][sides[next(iter(sides))]["pos"]]
                    rec["w"] = w_summary(w)
                    rec["paired_in_block"] = max(sides[s]["n_m"] for s in sides)
                    cls = "B"
                    rec["cons"] = consistency(idx, a["text"], w)
                else:
                    cls = "C"
                    rec["ws"] = {
                        s: [w_summary(w) for w in partners[s]] for s in partners
                    }
                rec["class"] = cls
                if cls in ("A1", "A2", "K", "B"):
                    w = rec["w"]
                    pos, ok = slash_positions(w["text"])
                    n_parts = len(morph_parts(w["morph"]))
                    sl = {"n": len(pos), "at_letter": ok, "morph_parts": n_parts}
                    if pos:
                        if cls == "B":
                            mapped = map_slashes_by_letters(
                                C.letters(w["text"]), C.letters(a["text"]), pos
                            )
                            sl["mapped"] = sum(p is not None for p in mapped)
                            if all(p is not None for p in mapped):
                                sl["mam"] = insert_slashes(a["text"], mapped)
                        else:
                            sl["mapped"] = len(pos)
                            sl["mam"] = insert_slashes(a["text"], pos)
                    rec["slash"] = sl
                by_class[cls] += 1
                recs_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("  %s (%.0fs)" % (osis, time.time() - t0))
    recs_out.close()
    unm_out.close()
    lines = [
        "align.py, strand %s; written by Claude (Opus 5.5), 2026-11-15; not reviewed by a human"
        % strand,
        "",
    ]
    for k, v in sorted(counts.items()):
        lines.append("%-55s %8d" % (k, v))
    lines.append("")
    lines.append("MAM atoms by class (each atom once):")
    for k in ("A1", "A2", "K", "AX", "B", "C"):
        lines.append("  %-4s %8d" % (k, by_class[k]))
    lines.append("  all  %8d" % sum(by_class.values()))
    summary = out_dir / ("12-align-summary%s.txt" % suffix)
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(lines))
    print(
        "wrote %s; records in %s"
        % (record_paths.shown(summary), record_paths.shown(work_dir))
    )
