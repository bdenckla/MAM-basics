"""Compact views that the study's page links, and the verses it shows side by side.

Written by Claude (Opus 5.5) on 2026-11-15 as the study's show_list.py, show_examples.py and
show_pair.py, and moved here on 2026-11-16, when the study was put on ice
(morphhb-on-mam/README.md). The page links the four list views (28-) and reads 29-, the order
of morphhb's words in the two verses whose runs of atoms it shows, so these are among the
page's inputs. Hebrew is shown in MAM-normal mark order; lemma and morph as morphhb has them.
"""

import json
from pathlib import Path

from morphhb_on_mam import mam_reader as M
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths

# (a list in 23-lists.json, the file that shows it)
LIST_VIEWS = (
    ("A2 contradicted", "28-show-a2-contradicted.txt"),
    ("B contradicted", "28-show-b-contradicted.txt"),
    ("qatan with a perfect or participle morph", "28-show-qatan.txt"),
    ("stress differs", "28-show-stress.txt"),
)
# The verses whose runs of atoms build_page.py shows, in 29-show-pairs.txt's order.
PAIR_VIDS = ("Dan.5.19", "2Sam.7.22")
PAIRS_NAME = "29-show-pairs.txt"


def fmt(x):
    """A value compactly, its Hebrew strings in MAM-normal mark order."""
    if isinstance(x, str):
        return C.mnorm(x) if any("\U00000590" <= ch <= "\U000005ff" for ch in x) else x
    if isinstance(x, list):
        return "[" + ", ".join(fmt(y) for y in x) + "]"
    if isinstance(x, dict):
        return "{" + ", ".join("%s: %s" % (k, fmt(v)) for k, v in x.items()) + "}"
    return str(x)


def write_list_views(out_dir):
    """Write each list of LIST_VIEWS whole, one item per line."""
    out_dir = Path(out_dir)
    data = json.loads((out_dir / "23-lists.json").read_text(encoding="utf-8"))
    for key, name in LIST_VIEWS:
        items = data[key]
        lines = ["## %s (%d of %d)" % (key, len(items), len(items))]
        for e in items:
            e = dict(e)
            e.pop("sig", None)
            if "cons" in e and isinstance(e["cons"], dict):
                c = e["cons"]
                e["cons"] = "n %d, pair %d, lemma %d, morph %d, top %s" % (
                    c["n"],
                    c["pair"],
                    c["lemma"],
                    c["morph"],
                    c["top"],
                )
            lines.append("  " + fmt(e))
        path = out_dir / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print("wrote %s" % record_paths.shown(path))


def write_pairs(wlc_dir, out_dir):
    """Write MAM's atoms and morphhb's words, with their ids, of the qere side of each verse
    of PAIR_VIDS."""
    mam = M.read_mam("cant-combined")
    lines = []
    for vid in PAIR_VIDS:
        book = C.read_morphhb_book(C.morphhb_path(wlc_dir, vid.split(".")[0]))
        words = book[vid]["qere_side"]
        atoms = mam[vid].sides["q"]
        lines.append(
            "%s  MAM: %s" % (vid, " | ".join(C.mnorm(a["text"]) for a in atoms))
        )
        lines.append(
            "%s  morphhb: %s"
            % (vid, " | ".join("%s %s" % (C.mnorm(w["text"]), w["id"]) for w in words))
        )
    path = Path(out_dir) / PAIRS_NAME
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("wrote %s" % record_paths.shown(path))
