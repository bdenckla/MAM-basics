"""Refinements of analyze.py's breakdown.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run(work_dir, out_dir) reads the work
directory's 10-atoms.jsonl and writes 22-refine.txt and 23-lists.json in the output directory.

1. The Tetragrammaton's holam, with or without a prefix.
2. Differences that the vowel key hides in class A1: qamats qatan and holam haser, by the
   morph part of the piece that holds them.
3. Where the 2026-11-13 study's nine corrections fall.
4. Full lists: A2 and B contradicted; MAM ketiv/qere against a plain morphhb word.
5. A screen for a difference in the place of the stress accent within A1.
"""

import collections
import json
from pathlib import Path

from morphhb_on_mam import align as AL
from morphhb_on_mam import analyze as AN
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths

YHWH = AN.YHWH
CORRECTIONS = "01oc4 02ubY 03caE 057a3 05ENP 06Umo 07HwX 242CG 28sYk".split()

# Accents whose place says nothing about stress: prepositive and postpositive ones.
NON_STRESS = {
    "\N{HEBREW ACCENT SEGOL}",  # postpositive
    "\N{HEBREW ACCENT PASHTA}",  # postpositive (a second one marks the stress)
    "\N{HEBREW ACCENT TELISHA QETANA}",  # postpositive
    "\N{HEBREW ACCENT TELISHA GEDOLA}",  # prepositive
    "\N{HEBREW ACCENT YETIV}",  # prepositive
    "\N{HEBREW ACCENT DEHI}",  # prepositive
    "\N{HEBREW ACCENT ZARQA}",  # tsinnorit's code point in MAM and WLC; not on the stress
    "\N{HEBREW ACCENT ZINOR}",  # postpositive zarqa
    "\N{HEBREW MARK MASORA CIRCLE}",
}


def accent_places(text):
    """Letter indices that carry an accent whose place marks the stress."""
    out, n = set(), -1
    for ch in text.replace("/", ""):
        if AL.is_letter(ch):
            n += 1
        elif "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW ACCENT OLE}" or ch in (
            "\N{HEBREW ACCENT ILUY}",
            "\N{HEBREW ACCENT DEHI}",
            "\N{HEBREW ACCENT ZINOR}",
        ):
            if ch not in NON_STRESS:
                out.add(n)
    return out


def piece_of_letter(w_text, k):
    """The index of the slash-separated piece of a morphhb word that holds letter k."""
    piece, n = 0, -1
    for ch in w_text:
        if ch == "/":
            piece += 1
        elif AL.is_letter(ch):
            n += 1
            if n == k:
                return piece
    raise ValueError("letter %d beyond %r" % (k, w_text))


def run(work_dir, out_dir):
    """Write the refinements and the full lists."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    recs = [
        json.loads(line) for line in open(work_dir / "10-atoms.jsonl", encoding="utf-8")
    ]
    L = [
        "analyze2.py on 10-atoms.jsonl; written by Claude (Opus 5.5), 2026-11-15; not reviewed by a human",
        "",
    ]
    lists = collections.defaultdict(list)

    # 1
    a2 = [r for r in recs if r["class"] == "A2"]
    hol = collections.Counter()
    for r in a2:
        sc = AN.sig_class(r)
        if sc.startswith("holam in MAM only"):
            letters = C.letters(r["text"])
            hol[
                (
                    "Tetragrammaton, bare"
                    if letters == YHWH
                    else (
                        "Tetragrammaton with a prefix"
                        if letters.endswith(YHWH)
                        else "other"
                    )
                )
            ] += 1
    L.append("== 1. A2 'holam in MAM only': %s" % dict(hol))
    others = [
        r
        for r in a2
        if AN.sig_class(r).startswith("holam in MAM only")
        and not C.letters(r["text"]).endswith(YHWH)
    ]
    for r in others[:12]:
        lists["holam other"].append(
            {
                "vid": r["vid"],
                "mam": r["text"],
                "morphhb": r["w"]["text"],
                "lemma": r["w"]["lemma"],
                "morph": r["w"]["morph"],
                "cons": r["cons"],
            }
        )
    L.append(
        "   non-Tetragrammaton examples in 23-lists.json 'holam other' (%d in all)"
        % len(others)
    )

    # 2
    L.append("")
    L.append(
        "== 2. A1 atoms whose strict marks differ (the vowel key folds qamats qatan into qamats and holam haser into holam)"
    )
    hidden = collections.Counter()
    qatan_parts = collections.Counter()
    for r in recs:
        if r["class"] != "A1":
            continue
        sig = AL.signature(r["w"]["text"], r["text"])
        if not sig:
            continue
        kinds = set()
        for k, _l, wm, mm in sig:
            change = (
                tuple(sorted(set(wm) - set(mm))),
                tuple(sorted(set(mm) - set(wm))),
            )
            kinds.add(change)
            if change == (("qamats",), ("qamats-qatan",)):
                part = r["w"]["morph"][1:].split("/")[
                    piece_of_letter(r["w"]["text"], k)
                ]
                tag = part[:2] if part[0] != "V" else part[:3]
                qatan_parts[tag] += 1
                if part[0] == "V" and part[2] in "pqr":
                    if len(lists["qatan with a perfect or participle morph"]) < 40:
                        lists["qatan with a perfect or participle morph"].append(
                            {
                                "vid": r["vid"],
                                "mam": r["text"],
                                "morphhb": r["w"]["text"],
                                "lemma": r["w"]["lemma"],
                                "morph": r["w"]["morph"],
                                "id": r["w"]["id"],
                            }
                        )
                    hidden[
                        "qamats qatan where morphhb's morph part is a perfect or participle"
                    ] += 1
        hidden[
            " + ".join(
                "%s->%s" % ("+".join(a) or "none", "+".join(b) or "none")
                for a, b in sorted(kinds)
            )
        ] += 1
    for k, n in hidden.most_common():
        L.append("  %7d  %s" % (n, k))
    L.append(
        "  qamats qatan in MAM, qamats in morphhb, by the morph part of the piece holding it:"
    )
    for k, n in qatan_parts.most_common():
        L.append("    %-6s %6d" % (k, n))

    # 3
    L.append("")
    L.append("== 3. The 2026-11-13 study's nine corrections, by morphhb id")
    for r in recs:
        ids = []
        if "w" in r:
            ids = [r["w"]["id"]]
        elif "ws" in r:
            ids = [w["id"] for s in r["ws"] for w in r["ws"][s]]
        hit = [i for i in ids if i in CORRECTIONS]
        if hit:
            L.append(
                "  %s %s class %s; cons %s" % (r["vid"], hit, r["class"], r.get("cons"))
            )

    # 4
    for r in recs:
        if r["class"] in ("A2", "B") and r["cons"]["n"] > 0 and r["cons"]["pair"] == 0:
            lists["%s contradicted" % r["class"]].append(
                {
                    "vid": r["vid"],
                    "mam": r["text"],
                    "morphhb": r["w"]["text"],
                    "lemma": r["w"]["lemma"],
                    "morph": r["w"]["morph"],
                    "id": r["w"]["id"],
                    "cons": r["cons"],
                }
            )
        if (
            r["class"] in ("K", "B")
            and r["on"] in ("k", "q")
            and r["w"]["type"] != "x-ketiv"
            and not r["w"]["in_qere"]
        ):
            lists["MAM ketiv or qere against a plain morphhb word"].append(
                {
                    "vid": r["vid"],
                    "on": r["on"],
                    "mam": r["text"],
                    "class": r["class"],
                    "morphhb": r["w"]["text"],
                    "lemma": r["w"]["lemma"],
                    "morph": r["w"]["morph"],
                    "id": r["w"]["id"],
                }
            )
    L.append("")
    L.append("== 4. Lists in 23-lists.json: %s" % {k: len(v) for k, v in lists.items()})
    kqv = collections.Counter(
        x["vid"] for x in lists["MAM ketiv or qere against a plain morphhb word"]
    )
    L.append(
        "   MAM ketiv/qere against a plain morphhb word: %d atoms in %d verses"
        % (sum(kqv.values()), len(kqv))
    )

    # 5
    L.append("")
    L.append(
        "== 5. A1 pairs whose stress accents sit on different letters (each form has exactly one such letter)"
    )
    stress = collections.Counter()
    for r in recs:
        if r["class"] != "A1":
            continue
        a, b = accent_places(r["w"]["text"]), accent_places(r["text"])
        if len(a) == 1 and len(b) == 1:
            if a != b:
                stress["differ"] += 1
                if len(lists["stress differs"]) < 60:
                    lists["stress differs"].append(
                        {
                            "vid": r["vid"],
                            "mam": r["text"],
                            "morphhb": r["w"]["text"],
                            "lemma": r["w"]["lemma"],
                            "morph": r["w"]["morph"],
                            "id": r["w"]["id"],
                        }
                    )
                part = r["w"]["morph"]
                stress["differ, morph has a verb"] += "V" in [
                    p[0] for p in part[1:].split("/")
                ]
            else:
                stress["same"] += 1
        else:
            stress["not comparable (none or several)"] += 1
    for k, n in stress.most_common():
        L.append("  %-40s %7d" % (k, n))

    refine = out_dir / "22-refine.txt"
    refine.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    lists_path = out_dir / "23-lists.json"
    with open(lists_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lists, f, ensure_ascii=False, indent=1)
    print(
        "wrote %s and %s" % (record_paths.shown(refine), record_paths.shown(lists_path))
    )
