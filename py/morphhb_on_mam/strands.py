"""Compare MAM's three strands of the 24 verses with a dual cantillation.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run(work_dir, out_dir) reads the work
directory's 10-atoms.jsonl (cant-combined), 10-atoms-cant-alef.jsonl and
10-atoms-cant-bet.jsonl and writes 25-strands.txt in the output directory.
For each verse with a cant-all-three, the atoms of each strand are compared in order:
letters, maqaf after, vowel key, and the class of the atom's match with morphhb.
"""

import collections
import json
from pathlib import Path

from morphhb_on_mam import align as AL
from morphhb_on_mam import mam_reader as M
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths


def load(path, vids):
    out = collections.defaultdict(list)
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r["vid"] in vids:
            out[r["vid"]].append(r)
    return out


def run(work_dir, out_dir):
    """Write the comparison of the three strands."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    mam = M.read_mam("cant-combined")
    vids = [v for v, x in mam.items() if x.has_cant3]
    st = {
        s: load(
            work_dir / ("10-atoms%s.jsonl" % ("" if s == "cant-combined" else "-" + s)),
            set(vids),
        )
        for s in M.STRANDS
    }
    L = [
        "strands.py; written by Claude (Opus 5.5), 2026-11-15; not reviewed by a human",
        "",
    ]
    c = collections.Counter()
    for vid in vids:
        rows = {s: st[s][vid] for s in M.STRANDS}
        n = {s: len(rows[s]) for s in M.STRANDS}
        if len(set(n.values())) != 1:
            L.append("%s: atom counts differ %s" % (vid, n))
            c["verses whose strands differ in atom count"] += 1
            continue
        c["verses compared"] += 1
        for k in range(n["cant-combined"]):
            rs = {s: rows[s][k] for s in M.STRANDS}
            c["atoms compared"] += 1
            letters = {C.letters(r["text"]) for r in rs.values()}
            if len(letters) != 1:
                c["atoms whose letters differ between strands"] += 1
                L.append("  %s atom %d letters differ" % (vid, k))
            if len({r["maqaf_after"] for r in rs.values()}) != 1:
                c["atoms whose maqaf after differs between strands"] += 1
                L.append(
                    "  %s atom %d maqaf: %s"
                    % (
                        vid,
                        k,
                        {
                            s: (C.mnorm(r["text"]), r["maqaf_after"])
                            for s, r in rs.items()
                        },
                    )
                )
            if len({AL.vkey(r["text"]) for r in rs.values()}) != 1:
                c["atoms whose vowel key differs between strands"] += 1
                L.append(
                    "  %s atom %d vowels: %s"
                    % (
                        vid,
                        k,
                        {s: (C.mnorm(r["text"]), r["class"]) for s, r in rs.items()},
                    )
                )
            if len({r["text"] for r in rs.values()}) != 1:
                c["atoms whose text (accents included) differs between strands"] += 1
            if len({r["class"] for r in rs.values()}) != 1:
                c["atoms whose class differs between strands"] += 1
            for s, r in rs.items():
                c["class %s in %s" % (r["class"], s)] += 1
            ids = {r.get("w", {}).get("id") for r in rs.values()}
            if len(ids) != 1:
                c["atoms matched to different morphhb words in different strands"] += 1
    L.insert(2, "verses with a dual cantillation: %d" % len(vids))
    for k, v in sorted(c.items()):
        L.insert(3, "%-70s %5d" % (k, v))
    path = out_dir / "25-strands.txt"
    path.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("wrote %s" % record_paths.shown(path))
