"""Censuses of MAM's atoms as mam_reader reads them, in the cant-combined strand.

Written by Claude (Opus 5.5) on 2026-11-15 as the study's census_mam.py, find_mixed.py and
check_fused_ketiv.py, and moved here on 2026-11-16, when the study was put on ice
(morphhb-on-mam/README.md). run(out_dir) reads MAM once and writes the three files:

- 01-mam-census.txt: the atoms' sides, kinds, flags and separators, and the verses with a
  dual cantillation;
- 03-mixed-atoms.txt: the atoms whose characters come from more than one kind of segment,
  none since mam_reader ends an atom where a one-sided segment meets a two-sided one;
- 31-check-fused-ketiv.txt: for each ketiv atom that mam_reader ends at a segment boundary,
  how its pair's qere ends.
"""

import collections
from pathlib import Path

from morphhb_on_mam import mam_reader as M
from morphhb_on_mam import record_paths


def census_lines(mam):
    """The census of MAM's atoms (census_mam.py)."""
    c = collections.Counter()
    kinds = collections.Counter()
    flags = collections.Counter()
    unique = collections.Counter()
    cant3 = []
    for vid, v in mam.items():
        c["verses"] += 1
        if v.has_cant3:
            cant3.append(vid)
        spans = {}
        for side in ("k", "q"):
            for a in v.sides[side]:
                c["side atoms " + side] += 1
                spans.setdefault(a["span"], set()).add(side)
                if a["maqaf_after"]:
                    c["maqaf after (%s)" % side] += 1
                if a["implicit_maqaf"]:
                    c["implicit maqaf after (%s)" % side] += 1
                if a["legarmeh"]:
                    c["legarmeh (%s)" % side] += 1
                if a["paseq_after"]:
                    c["paseq after (%s)" % side] += 1
                if a.get("boundary_added"):
                    c["boundary added after (%s)" % side] += 1
        for span, sides in spans.items():
            unique["".join(sorted(sides))] += 1
        for side in ("k", "q"):
            for a in v.sides[side]:
                sides = spans[a["span"]]
                if side == "q" and sides == {"k", "q"}:
                    continue  # count a two-sided atom once
                kinds[" + ".join(a["kinds"]) + " [" + "".join(sorted(sides)) + "]"] += 1
                for k, val in a["flags"].items():
                    flags["%s=%s" % (k, val)] += 1
        if not v.sides["k"] and not v.sides["q"]:
            c["verses with no atoms"] += 1
    lines = [
        "census of MAM-simple (BHS versification, cant-combined strand) by mam_reader.py",
        "",
    ]
    for k, v in sorted(c.items()):
        lines.append("%-40s %8d" % (k, v))
    lines.append("")
    lines.append("distinct atoms by the sides they are on: %s" % dict(unique))
    lines.append("total distinct atoms: %d" % sum(unique.values()))
    lines.append("")
    lines.append("atom kinds (each atom once):")
    for k, v in kinds.most_common():
        lines.append("  %-50s %8d" % (k, v))
    lines.append("")
    lines.append("atom flags:")
    for k, v in flags.most_common():
        lines.append("  %-50s %8d" % (k, v))
    lines.append("")
    lines.append(
        "verses with a dual cantillation: %d: %s" % (len(cant3), " ".join(cant3))
    )
    return lines


def find_mixed(mam):
    """The atoms whose characters come from more than one kind of segment (find_mixed.py),
    after a line that counts them."""
    lines = []
    for vid, v in mam.items():
        for side in ("k", "q"):
            for a in v.sides[side]:
                if len(a["kinds"]) > 1:
                    segs = sorted({s for s, _o in a["span"]})
                    lines.append(
                        "%s %s atom %d %s kinds %s; segments %s"
                        % (
                            vid,
                            side,
                            a["i"],
                            ascii(a["text"]),
                            a["kinds"],
                            [
                                (s, v.segments[s]["kind"], v.segments[s]["text"])
                                for s in segs
                            ],
                        )
                    )
    lines.insert(
        0,
        "census.py, find_mixed: %d atoms whose characters come from more than one kind"
        " of segment" % len(lines),
    )
    return lines


def check_fused_ketiv(mam):
    """How the qere ends where a ketiv atom ends at a segment boundary
    (check_fused_ketiv.py)."""
    c = collections.Counter()
    lines = []
    for vid, v in mam.items():
        for a in v.sides["k"]:
            if not a.get("boundary_added"):
                continue
            last_seg = a["span"][-1][0]
            # The qere of the same pair: the nearest q-only segment around the ketiv's segment.
            q = [
                s
                for s in range(max(0, last_seg - 2), min(len(v.segments), last_seg + 3))
                if v.segments[s]["sides"] == "q"
            ]
            if not q:
                c["no qere segment found nearby"] += 1
                lines.append("%s: no qere segment nearby" % vid)
                continue
            qtext = v.segments[q[-1]]["text"].rstrip(" ")
            end = (
                "maqaf"
                if qtext.endswith(M.MAQAF)
                else ("space" if v.segments[q[-1]]["text"].endswith(" ") else "other")
            )
            c["qere ends with " + end] += 1
            if end != "maqaf":
                lines.append(
                    "%s: qere ends with %s: %s"
                    % (vid, end, ascii(v.segments[q[-1]]["text"]))
                )
    lines.insert(0, "census.py, check_fused_ketiv: %s" % dict(c))
    return lines


def run(out_dir):
    """Read MAM once and write the three censuses."""
    mam = M.read_mam("cant-combined")
    for name, lines in (
        ("01-mam-census.txt", census_lines(mam)),
        ("03-mixed-atoms.txt", find_mixed(mam)),
        ("31-check-fused-ketiv.txt", check_fused_ketiv(mam)),
    ):
        path = Path(out_dir) / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print("wrote %s" % record_paths.shown(path))
