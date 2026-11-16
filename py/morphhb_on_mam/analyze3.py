"""Ketiv/qere structure, new ids and slash placement.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run(work_dir, out_dir) reads the work
directory's 10-atoms.jsonl and 11-unmatched-morphhb.jsonl and writes 26-kq-ids-slashes.txt and
27-kq-ids-slashes.json in the output directory.

1. Where MAM has one form (a plain atom or a kq-trivial) and morphhb a ketiv and a qere: do
   morphhb's two analyses agree?  If not, MAM's form needs a choice.
2. Where MAM has a ketiv and a qere and morphhb one plain word.
3. MAM atoms with no morphhb word of their own (they would need new ids) and morphhb words
   with no MAM atom (their ids would go unused).
4. Slashes that align.py left unplaced (class B): a fallback rule that puts a slash next to its
   one matched neighbour, and what stays ambiguous.
"""

import collections
import difflib
import json
from pathlib import Path

from morphhb_on_mam import align as AL
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths


def analysis(w):
    return AL.lemma_number(w["lemma"]) + " | " + w["morph"]


def fallback_slashes(w_text, m_text):
    """Slash positions in MAM's letters: a slash goes before the mapped right neighbour, or
    after the mapped left neighbour; ambiguous when both are mapped but not adjacent, or
    neither is mapped."""
    wl, ml = C.letters(w_text), C.letters(m_text)
    pos, _ok = AL.slash_positions(w_text)
    sm = difflib.SequenceMatcher(None, wl, ml, autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for i in range(i1, i2):
                amap[i] = j1 + (i - i1)
    out = []
    for p in pos:
        left, right = amap.get(p - 1), amap.get(p)
        if left is not None and right is not None:
            out.append(right if right == left + 1 else None)
        elif right is not None:
            out.append(right)
        elif left is not None:
            out.append(left + 1)
        else:
            out.append(None)
    return out


def run(work_dir, out_dir):
    """Write the ketiv/qere, id and slash breakdowns and their lists."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    recs = [
        json.loads(line) for line in open(work_dir / "10-atoms.jsonl", encoding="utf-8")
    ]
    unm = [
        json.loads(line)
        for line in open(work_dir / "11-unmatched-morphhb.jsonl", encoding="utf-8")
    ]
    L = [
        "analyze3.py; written by Claude (Opus 5.5), 2026-11-15; not reviewed by a human",
        "",
    ]
    J = collections.defaultdict(list)

    # 1
    L.append(
        "== 1. MAM one form, morphhb a ketiv and a qere (class C blocks of one MAM atom)"
    )
    c1 = collections.Counter()
    for r in recs:
        if r["class"] != "C" or r["on"] != "kq" or "ws" not in r:
            continue
        ket = [w for s in r["ws"] for w in r["ws"][s] if w["type"] == "x-ketiv"]
        qer = [w for s in r["ws"] for w in r["ws"][s] if w["in_qere"]]
        if not ket or not qer:
            continue
        kind = "kq-trivial" if "kq-trivial" in r["kinds"] else "plain"
        ket = list({w["id"]: w for w in ket}.values())
        qer = list({w["id"]: w for w in qer}.values())
        if len(ket) == 1 and len(qer) == 1:
            same = analysis(ket[0]) == analysis(qer[0])
            same_lemma = AL.lemma_number(ket[0]["lemma"]) == AL.lemma_number(
                qer[0]["lemma"]
            )
            mam_l, k_l, q_l = (
                C.letters(r["text"]),
                C.letters(ket[0]["text"]),
                C.letters(qer[0]["text"]),
            )
            letters = (
                "MAM's letters are the ketiv's"
                if mam_l == k_l
                else ("the qere's" if mam_l == q_l else "neither's")
            )
            key = (
                kind,
                (
                    "analyses agree"
                    if same
                    else (
                        "same lemma, morphs differ" if same_lemma else "lemmas differ"
                    )
                ),
                letters,
            )
            c1[key] += 1
            if not same:
                J["one form, analyses differ"].append(
                    {
                        "vid": r["vid"],
                        "mam": r["text"],
                        "kind": kind,
                        "ketiv": [
                            ket[0]["text"],
                            ket[0]["id"],
                            ket[0]["lemma"],
                            ket[0]["morph"],
                        ],
                        "qere": [
                            qer[0]["text"],
                            qer[0]["id"],
                            qer[0]["lemma"],
                            qer[0]["morph"],
                        ],
                    }
                )
        else:
            c1[(kind, "several ketiv or qere words", "")] += 1
    for k, n in sorted(c1.items(), key=lambda kv: -kv[1]):
        L.append("  %5d  %s" % (n, "; ".join(x for x in k if x)))

    # 2
    L.append("")
    L.append("== 2. MAM a ketiv and a qere, morphhb one plain word")
    c2 = collections.Counter()
    verses = collections.defaultdict(dict)
    for r in recs:
        if (
            r["on"] in ("k", "q")
            and "w" in r
            and r["w"]["type"] != "x-ketiv"
            and not r["w"]["in_qere"]
        ):
            verses[r["vid"]][r["on"]] = r
            c2[
                "MAM %s atoms, class %s"
                % ({"k": "ketiv", "q": "qere"}[r["on"]], r["class"])
            ] += 1
    for k, n in sorted(c2.items()):
        L.append("  %5d  %s" % (n, k))
    L.append("  verses: %d" % len(verses))
    for vid, d in list(verses.items()):
        J["MAM kq, morphhb plain"].append(
            {
                "vid": vid,
                **{
                    s: [
                        d[s]["text"],
                        d[s]["class"],
                        d[s]["w"]["text"],
                        d[s]["w"]["id"],
                        d[s]["w"]["lemma"],
                        d[s]["w"]["morph"],
                    ]
                    for s in d
                },
            }
        )

    # 3
    L.append("")
    L.append(
        "== 3. ids: MAM atoms with no morphhb word of their own, and morphhb words with no MAM atom"
    )
    c3 = collections.Counter()
    for r in recs:
        if r["class"] in ("A1", "A2", "K", "B"):
            continue
        if r["class"] == "AX":
            c3["AX: MAM one atom, morphhb a ketiv and a qere of the same letters"] += 1
            continue
        n_ws = {s: len(r["ws"][s]) for s in r["ws"]}
        if not any(n_ws.values()):
            c3["C: no morphhb word at all"] += 1
        else:
            c3[
                "C: in a block with %s morphhb word(s) per side"
                % "/".join(str(n_ws[s]) for s in sorted(n_ws))
            ] += 1
    for k, n in sorted(c3.items(), key=lambda kv: -kv[1]):
        L.append("  %5d  %s" % (n, k))
    ids_unm = {(u["vid"], u["w"]["id"]) for u in unm}
    used = set()
    for r in recs:
        if "w" in r:
            used.add(r["w"]["id"])
        for s in r.get("ws", {}):
            for w in r["ws"][s]:
                used.add(w["id"])
    never = {(v, i) for v, i in ids_unm if i not in used}
    L.append(
        "  morphhb words in a delete block on some side: %d; of them matched on no side: %d"
        % (len(ids_unm), len(never))
    )

    # 4
    L.append("")
    L.append("== 4. Slashes in class B: the fallback rule")
    c4 = collections.Counter()
    for r in recs:
        if r["class"] != "B" or not r["slash"]["n"]:
            continue
        if r["slash"]["mapped"] == r["slash"]["n"]:
            c4["words placed by align.py"] += 1
            continue
        fb = fallback_slashes(r["w"]["text"], r["text"])
        if all(p is not None for p in fb):
            c4["words placed by the fallback rule"] += 1
            if len(J["fallback placed"]) < 12:
                J["fallback placed"].append(
                    {
                        "vid": r["vid"],
                        "mam": AL.insert_slashes(r["text"], fb),
                        "morphhb": r["w"]["text"],
                        "morph": r["w"]["morph"],
                    }
                )
        else:
            c4["words still ambiguous"] += 1
            J["still ambiguous"].append(
                {
                    "vid": r["vid"],
                    "mam": r["text"],
                    "morphhb": r["w"]["text"],
                    "morph": r["w"]["morph"],
                }
            )
    for k, n in sorted(c4.items()):
        L.append("  %5d  %s" % (n, k))

    text_path = out_dir / "26-kq-ids-slashes.txt"
    text_path.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    json_path = out_dir / "27-kq-ids-slashes.json"
    with open(json_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(J, f, ensure_ascii=False, indent=1)
    print(
        "wrote %s and %s"
        % (record_paths.shown(text_path), record_paths.shown(json_path))
    )
