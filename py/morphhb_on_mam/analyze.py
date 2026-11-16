"""Break down align.py's classes for the feasibility questions.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run(work_dir, out_dir, suffix) reads
10-atoms<suffix>.jsonl and 11-unmatched-morphhb<suffix>.jsonl in the work directory and
writes 20-coverage<suffix>.txt and 21-examples<suffix>.json in the output directory.  Forms
in the outputs are copied from the inputs by script; the text file shows them in MAM-normal
mark order (give_std_mark_order), the JSON keeps them as the sources have them.
"""

import collections
import difflib
import json
from pathlib import Path

from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths

YHWH = (
    "\N{HEBREW LETTER YOD}\N{HEBREW LETTER HE}\N{HEBREW LETTER VAV}\N{HEBREW LETTER HE}"
)
MATRES = {"\N{HEBREW LETTER VAV}", "\N{HEBREW LETTER YOD}"}


def disp(s):
    return C.mnorm(s)


def sig_class(rec):
    """A coarse class of a letters-equal pointing difference."""
    sig = rec["sig"]
    letters = C.letters(rec["text"])
    changes = []
    for _k, _l, wm, mm in sig:
        added = sorted(set(mm) - set(wm))
        removed = sorted(set(wm) - set(mm))
        changes.append((tuple(removed), tuple(added)))
    if all(r == () and a == ("holam",) for r, a in changes):
        return (
            "holam in MAM only, Tetragrammaton"
            if letters == YHWH
            else "holam in MAM only, other"
        )
    if all(r == ("holam",) and a == () for r, a in changes):
        return "holam in morphhb only"
    if all(set(r) | set(a) == {"dagesh"} for r, a in changes):
        return "dagesh or mappiq only"
    if all(set(r) | set(a) <= {"shin-dot", "sin-dot"} for r, a in changes):
        return "shin or sin dot only"
    if len(changes) == 1:
        r, a = changes[0]
        return "one letter: %s -> %s" % ("+".join(r) or "none", "+".join(a) or "none")
    return "several letters"


def cons_class(c):
    if c["n"] == 0:
        return "MAM's form not elsewhere in morphhb"
    if c["pair"] > 0:
        return "supported: MAM's form has this lemma and morph elsewhere"
    if c["lemma"] > 0:
        return "contradicted in morph: same lemma elsewhere, never this morph"
    if c["morph"] > 0:
        return "contradicted in lemma: same morph elsewhere, never this lemma"
    return "contradicted in both"


def letters_diff_class(w_text, m_text):
    a, b = C.letters(w_text), C.letters(m_text)
    ops = [
        op
        for op in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
        if op[0] != "equal"
    ]
    kinds = set()
    for tag, i1, i2, j1, j2 in ops:
        removed, added = a[i1:i2], b[j1:j2]
        if tag in ("insert", "delete") and set(removed + added) <= MATRES:
            kinds.add("mater added in MAM" if added else "mater missing in MAM")
        else:
            kinds.add("other letters")
    if kinds == {"mater added in MAM"} or kinds == {"mater missing in MAM"}:
        return next(iter(kinds))
    if kinds <= {"mater added in MAM", "mater missing in MAM"}:
        return "matres both ways"
    return "other letters"


def example(rec, **extra):
    out = {"vid": rec["vid"], "mam": rec["text"], "class": rec["class"]}
    if "w" in rec:
        out.update(
            {
                "morphhb": rec["w"]["text"],
                "lemma": rec["w"]["lemma"],
                "morph": rec["w"]["morph"],
                "id": rec["w"]["id"],
            }
        )
    if "ws" in rec:
        out["ws"] = rec["ws"]
    out.update(extra)
    return out


def run(work_dir, out_dir, suffix=""):
    """Write the breakdown of one strand's records and its examples."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    recs = [
        json.loads(line)
        for line in open(work_dir / ("10-atoms%s.jsonl" % suffix), encoding="utf-8")
    ]
    unm = [
        json.loads(line)
        for line in open(
            work_dir / ("11-unmatched-morphhb%s.jsonl" % suffix), encoding="utf-8"
        )
    ]
    L = []
    ex = collections.defaultdict(list)

    def add_ex(key, rec, limit=6, **extra):
        if len(ex[key]) < limit:
            ex[key].append(example(rec, **extra))

    total = len(recs)
    cls = collections.Counter(r["class"] for r in recs)
    on = collections.Counter((r["class"], r["on"]) for r in recs)
    L.append(
        "analyze.py on 10-atoms%s.jsonl; written by Claude (Opus 5.5), 2026-11-15; not reviewed by a human"
        % suffix
    )
    L.append("")
    L.append(
        "== 1. MAM atoms by class (each atom once; on = the sides it is on: kq both, k ketiv, q qere)"
    )
    for k in ("A1", "A2", "K", "AX", "B", "C"):
        parts = ", ".join(
            "%s %d" % (s, on[(k, s)]) for s in ("kq", "k", "q") if on[(k, s)]
        )
        L.append(
            "  %-3s %7d  %6.2f%%   (%s)" % (k, cls[k], 100.0 * cls[k] / total, parts)
        )
    L.append("  all %7d" % total)

    # A2: pointing differs
    L.append("")
    L.append(
        "== 2. A2, letters equal and pointing differs: by kind of difference, then by how morphhb analyses MAM's form elsewhere"
    )
    a2 = [r for r in recs if r["class"] == "A2"]
    by_sig = collections.Counter(sig_class(r) for r in a2)
    by_sig_cons = collections.Counter((sig_class(r), cons_class(r["cons"])) for r in a2)
    for s, n in by_sig.most_common():
        L.append("  %6d  %s" % (n, s))
        for (s2, c), m in sorted(by_sig_cons.items(), key=lambda kv: -kv[1]):
            if s2 == s:
                L.append("          %6d  %s" % (m, c))
    L.append("")
    L.append("  A2 by consistency alone:")
    for c, n in collections.Counter(cons_class(r["cons"]) for r in a2).most_common():
        L.append("    %6d  %s" % (n, c))
    strong = [r for r in a2 if r["cons"]["n"] >= 5 and r["cons"]["pair"] == 0]
    L.append(
        "  A2 contradicted with MAM's form at least 5 times elsewhere in morphhb: %d"
        % len(strong)
    )
    for r in a2:
        sc, cc = sig_class(r), cons_class(r["cons"])
        add_ex("A2 " + sc + " / " + cc, r, limit=4, cons=r["cons"], sig=r["sig"])

    # K: ketiv
    L.append("")
    L.append(
        "== 3. K, MAM's ketiv (unpointed) with the letters of morphhb's ketiv word: %d"
        % cls["K"]
    )
    kt = collections.Counter(
        (
            "x-ketiv"
            if r["w"]["type"] == "x-ketiv"
            else ("qere" if r["w"]["in_qere"] else "plain")
        )
        for r in recs
        if r["class"] == "K"
    )
    L.append("  morphhb partner kinds: %s" % dict(kt))
    for r in recs:
        if r["class"] == "K":
            add_ex("K", r, limit=3)

    # kq structure
    L.append("")
    L.append(
        "== 4. Ketiv and qere: MAM atoms' kinds against their morphhb partners' kinds"
    )

    def wkind(w):
        return (
            "x-ketiv"
            if w["type"] == "x-ketiv"
            else ("qere" if w["in_qere"] else "plain")
        )

    kq = collections.Counter()
    for r in recs:
        mk = "+".join(r["kinds"]) + "[" + r["on"] + "]"
        if "w" in r:
            kq[(r["class"], mk, wkind(r["w"]))] += 1
        elif r["class"] in ("AX", "C"):
            pk = sorted({wkind(w) for s in r["ws"] for w in r["ws"][s]}) or ["none"]
            kq[(r["class"], mk, "+".join(pk))] += 1
    for (c, mk, wk), n in sorted(kq.items(), key=lambda kv: (kv[0][0], -kv[1])):
        if mk == "plain[kq]" and wk == "plain":
            continue
        L.append("  %-3s MAM %-28s morphhb %-16s %6d" % (c, mk, wk, n))
    L.append(
        "  (plain MAM atoms with plain morphhb partners are left out of this table)"
    )
    for r in recs:
        if (
            r["class"] in ("A1", "A2", "B")
            and r["on"] == "kq"
            and "w" in r
            and wkind(r["w"]) != "plain"
        ):
            add_ex("kq MAM plain, morphhb " + wkind(r["w"]), r, limit=4)
        if "kq-trivial" in r["kinds"]:
            add_ex("kq-trivial " + r["class"], r, limit=4)

    # AX
    L.append("")
    L.append(
        "== 5. AX (letters equal, different morphhb word on each side): %d" % cls["AX"]
    )
    for r in recs:
        if r["class"] == "AX":
            L.append(
                "  %s MAM %s; morphhb k %s, q %s"
                % (
                    r["vid"],
                    disp(r["text"]),
                    [
                        (disp(w["text"]), w["id"], w["type"], w["in_qere"])
                        for w in r["ws"].get("k", [])
                    ],
                    [
                        (disp(w["text"]), w["id"], w["type"], w["in_qere"])
                        for w in r["ws"].get("q", [])
                    ],
                )
            )
            add_ex("AX", r, limit=4)

    # B
    L.append("")
    L.append(
        "== 6. B, one-to-one and letters differ: by kind of letter difference, then by consistency"
    )
    b = [r for r in recs if r["class"] == "B"]
    L.append(
        "  of the %d, paired word by word inside a larger block of equal size on both texts: %d"
        % (len(b), sum(1 for r in b if r.get("paired_in_block")))
    )
    by_b = collections.Counter(letters_diff_class(r["w"]["text"], r["text"]) for r in b)
    by_b_cons = collections.Counter(
        (letters_diff_class(r["w"]["text"], r["text"]), cons_class(r["cons"]))
        for r in b
    )
    for s, n in by_b.most_common():
        L.append("  %6d  %s" % (n, s))
        for (s2, c), m in sorted(by_b_cons.items(), key=lambda kv: -kv[1]):
            if s2 == s:
                L.append("          %6d  %s" % (m, c))
    for r in b:
        add_ex(
            "B "
            + letters_diff_class(r["w"]["text"], r["text"])
            + " / "
            + cons_class(r["cons"]),
            r,
            limit=4,
            cons=r["cons"],
        )

    # C
    L.append("")
    L.append("== 7. C, no one-to-one partner: blocks")
    blocks = collections.OrderedDict()
    for r in recs:
        if r["class"] != "C":
            continue
        key = (
            r["vid"],
            tuple(sorted((s, tuple(w["id"] for w in r["ws"][s])) for s in r["ws"])),
        )
        blocks.setdefault(key, []).append(r)
    shapes = collections.Counter()
    for key, rs in blocks.items():
        ws_all = {}
        for s, ids in key[1]:
            for r in rs:
                if s in r["ws"]:
                    ws_all[s] = r["ws"][s]
        n_w = max((len(v) for v in ws_all.values()), default=0)
        m_letters = "".join(C.letters(r["text"]) for r in rs)
        w_letter_sets = {
            "".join(C.letters(w["text"]) for w in v) for v in ws_all.values()
        }
        w_kq = any(
            w["type"] == "x-ketiv" or w["in_qere"] for v in ws_all.values() for w in v
        )
        if any("kq-trivial" in r["kinds"] for r in rs):
            shape = (
                "MAM's trivial ketiv/qere (one form) where morphhb has a ketiv and a qere"
                if w_kq
                else "MAM's trivial ketiv/qere, other"
            )
        elif all(r["on"] == "kq" for r in rs) and w_kq:
            shape = "MAM plain where morphhb has a ketiv and a qere"
        elif any(len(r["on"]) == 1 for r in rs):
            shape = "MAM ketiv/qere with another structure in morphhb"
        elif n_w == 0:
            shape = "MAM atom(s) with no morphhb word"
        elif len(w_letter_sets) == 1 and m_letters in w_letter_sets:
            shape = "division into atoms differs (same letters)"
        else:
            shape = "letters and division differ"
        if any(r["boundary_added"] for r in rs):
            shape += ", MAM-simple ketiv boundary"
        shapes[shape] += 1
        if len(ex["C " + shape]) < 6:
            ex["C " + shape].append(
                {
                    "vid": key[0],
                    "mam": [r["text"] for r in rs],
                    "mam_on": [r["on"] for r in rs],
                    "morphhb": {
                        s: [
                            (
                                w["text"],
                                w["id"],
                                w["lemma"],
                                w["morph"],
                                w["type"],
                                w["in_qere"],
                            )
                            for w in v
                        ]
                        for s, v in ws_all.items()
                    },
                }
            )
    L.append("  blocks: %d, holding %d MAM atoms" % (len(blocks), cls["C"]))
    for s, n in shapes.most_common():
        L.append("  %6d  %s" % (n, s))

    # unmatched morphhb words
    L.append("")
    L.append(
        "== 8. morphhb words that no MAM atom matches (difflib delete blocks), side words: %d"
        % len(unm)
    )
    uv = collections.Counter((u["vid"], u["w"]["id"]) for u in unm)
    L.append(
        "  distinct morphhb words: %d; in verses MAM lacks: %d"
        % (len(uv), len({(u["vid"], u["w"]["id"]) for u in unm if u["absent_verse"]}))
    )
    for (vid, wid), n in uv.items():
        u = next(x for x in unm if x["vid"] == vid and x["w"]["id"] == wid)
        L.append(
            "  %s %s %s %s %s sides %d"
            % (vid, wid, disp(u["w"]["text"]), u["w"]["lemma"], u["w"]["morph"], n)
        )
        if len(ex["unmatched"]) < 8:
            ex["unmatched"].append(u)

    # maqaf
    L.append("")
    L.append(
        "== 9. Maqaf after an atom, MAM against morphhb, two-sided atoms with a one-to-one plain partner"
    )
    mq = collections.Counter()
    for r in recs:
        if (
            r["class"] in ("A1", "A2", "B")
            and r["on"] == "kq"
            and wkind(r["w"]) == "plain"
        ):
            k = (
                "MAM %s"
                % (
                    "implicit maqaf"
                    if r["implicit_maqaf"]
                    else ("maqaf" if r["maqaf_after"] else "none")
                ),
                "morphhb %s" % ("maqaf" if r["w"]["maqaf_after"] else "none"),
            )
            mq[k] += 1
            if (
                k[0] != "MAM none"
                and k[1] == "morphhb none"
                or k[0] == "MAM none"
                and k[1] == "morphhb maqaf"
            ):
                add_ex("maqaf %s / %s" % k, r, limit=4)
    for k, n in mq.most_common():
        L.append("  %-22s %-16s %7d" % (k[0], k[1], n))

    # slashes
    L.append("")
    L.append(
        "== 10. morphhb's morpheme slashes carried into MAM's text (classes A1, A2, K, B)"
    )
    sl = collections.Counter()
    for r in recs:
        if "slash" not in r:
            continue
        s = r["slash"]
        c = r["class"]
        sl[(c, "words")] += 1
        if s["n"]:
            sl[(c, "with slashes")] += 1
            sl[(c, "slashes")] += s["n"]
            sl[(c, "slashes placed")] += s["mapped"]
            if s["mapped"] < s["n"]:
                sl[(c, "words with an unplaced slash")] += 1
                add_ex("slash unplaced " + c, r, limit=6, slash=s)
        if not s["at_letter"]:
            sl[(c, "words with a slash not directly before a letter")] += 1
            add_ex("slash not before a letter " + c, r, limit=6, slash=s)
        if s["morph_parts"] != s["n"] + 1:
            sl[(c, "words whose morph parts differ from text pieces")] += 1
            add_ex("morph parts differ " + c, r, limit=6, slash=s)
        if "Rd" in [p[:2] for p in r["w"]["morph"][1:].split("/")]:
            sl[(c, "words with an Rd segment")] += 1
            if c == "A2":
                touched = sorted({k for k, _l, _a, _b in r["sig"]})
                sl[
                    (c, "Rd words whose difference touches the first two letters")
                ] += any(k < 2 for k in touched)
                if any(k < 2 for k in touched):
                    add_ex(
                        "Rd A2 first two letters",
                        r,
                        limit=6,
                        sig=r["sig"],
                        cons=r["cons"],
                    )
    for k in sorted(sl):
        L.append("  %-3s %-60s %7d" % (k[0], k[1], sl[k]))
    for r in recs:
        if r["class"] == "A1" and r.get("slash", {}).get("n", 0) >= 2:
            add_ex("slash A1 example", r, limit=3, slash=r["slash"])
        if (
            r["class"] == "B"
            and r.get("slash", {}).get("n", 0) >= 1
            and "mam" in r["slash"]
        ):
            add_ex("slash B example", r, limit=3, slash=r["slash"])

    coverage = out_dir / ("20-coverage%s.txt" % suffix)
    coverage.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    examples = out_dir / ("21-examples%s.json" % suffix)
    with open(examples, "w", encoding="utf-8", newline="\n") as f:
        json.dump(ex, f, ensure_ascii=False, indent=1)
    print(
        "wrote %s and %s" % (record_paths.shown(coverage), record_paths.shown(examples))
    )
