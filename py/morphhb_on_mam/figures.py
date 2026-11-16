"""The headline figures of the feasibility study, computed from the outputs.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run(work_dir, out_dir) reads the work
directory's 10-atoms.jsonl and 11-unmatched-morphhb.jsonl and writes 30-figures.json and
30-figures.txt in the output directory.  Every figure on the page is read from
30-figures.json or from the outputs it names.

Tiers (each MAM atom once):
  same      A1, and K with a morphhb ketiv partner: morphhb's lemma, morph and id apply as they are
  supported A2 and B whose form morphhb analyses the same way elsewhere (lemma and morph)
  untested  A2 and B whose form occurs nowhere else in morphhb
  flagged   A2 and B whose form occurs elsewhere in morphhb, never with this lemma and morph
  structural AX, C, and K whose morphhb partner is a plain word (MAM's ketiv/qere where
            morphhb has none)
"""

import collections
import json
from pathlib import Path

from morphhb_on_mam import analyze as AN
from morphhb_on_mam import morphhb_reader as C
from morphhb_on_mam import record_paths


def tier(r):
    c = r["class"]
    if c == "A1":
        return "same"
    if c == "K":
        return "same" if r["w"]["type"] == "x-ketiv" else "structural"
    if c in ("A2", "B"):
        cons = r["cons"]
        if cons["n"] == 0:
            return "untested"
        return "supported" if cons["pair"] > 0 else "flagged"
    return "structural"


def run(work_dir, out_dir):
    """Write the headline figures as JSON and as text."""
    work_dir, out_dir = Path(work_dir), Path(out_dir)
    recs = [
        json.loads(line) for line in open(work_dir / "10-atoms.jsonl", encoding="utf-8")
    ]
    unm = [
        json.loads(line)
        for line in open(work_dir / "11-unmatched-morphhb.jsonl", encoding="utf-8")
    ]
    F = {}
    F["mam_atoms"] = len(recs)
    F["mam_atoms_by_sides"] = dict(collections.Counter(r["on"] for r in recs))
    F["classes"] = dict(collections.Counter(r["class"] for r in recs))
    tiers = collections.Counter(tier(r) for r in recs)
    F["tiers"] = dict(tiers)
    F["tiers_percent"] = {k: round(100.0 * v / len(recs), 2) for k, v in tiers.items()}
    F["tier_by_class"] = {
        "%s/%s" % k: v
        for k, v in collections.Counter((tier(r), r["class"]) for r in recs).items()
    }
    yh = collections.Counter()
    for r in recs:
        if r["class"] == "A2" and AN.sig_class(r).startswith("holam in MAM only"):
            letters = C.letters(r["text"])
            yh[
                (
                    "bare"
                    if letters == AN.YHWH
                    else ("prefixed" if letters.endswith(AN.YHWH) else "other")
                )
            ] += 1
    F["a2_holam_only"] = dict(yh)
    F["a2_holam_only_supported"] = sum(
        1
        for r in recs
        if r["class"] == "A2"
        and AN.sig_class(r).startswith("holam in MAM only")
        and tier(r) == "supported"
    )
    F["a2_other_than_holam"] = sum(
        1
        for r in recs
        if r["class"] == "A2" and not AN.sig_class(r).startswith("holam in MAM only")
    )
    F["a2_other_than_holam_by_tier"] = dict(
        collections.Counter(
            tier(r)
            for r in recs
            if r["class"] == "A2"
            and not AN.sig_class(r).startswith("holam in MAM only")
        )
    )
    F["b_by_letters"] = dict(
        collections.Counter(
            AN.letters_diff_class(r["w"]["text"], r["text"])
            for r in recs
            if r["class"] == "B"
        )
    )
    F["b_by_tier"] = dict(
        collections.Counter(tier(r) for r in recs if r["class"] == "B")
    )
    F["b_paired_in_block"] = sum(
        1 for r in recs if r["class"] == "B" and r.get("paired_in_block")
    )
    F["morphhb_side_words_unmatched"] = len(unm)
    F["morphhb_words_unmatched_distinct"] = len({(u["vid"], u["w"]["id"]) for u in unm})
    F["morphhb_words_unmatched_in_absent_verses"] = len(
        {(u["vid"], u["w"]["id"]) for u in unm if u["absent_verse"]}
    )
    sl = collections.Counter()
    for r in recs:
        s = r.get("slash")
        if not s:
            continue
        sl["words"] += 1
        sl["words with a slash"] += bool(s["n"])
        sl["slashes"] += s["n"]
        sl["slashes placed by letter count or letter alignment"] += s.get("mapped", 0)
        sl["slash not directly before a letter"] += not s["at_letter"]
        sl["morph parts differ from text pieces"] += s["morph_parts"] != s["n"] + 1
        if r["class"] in ("A1", "A2", "K"):
            sl["letters-equal words with a slash"] += bool(s["n"])
            sl["letters-equal slashes"] += s["n"]
    F["slashes"] = dict(sl)
    F["rd_words_by_class"] = dict(
        collections.Counter(
            r["class"]
            for r in recs
            if "w" in r and "Rd" in [p[:2] for p in r["w"]["morph"][1:].split("/")]
        )
    )
    mq = collections.Counter()
    for r in recs:
        if (
            r["class"] in ("A1", "A2", "B")
            and r["on"] == "kq"
            and r["w"]["type"] != "x-ketiv"
            and not r["w"]["in_qere"]
        ):
            m = (
                "implicit maqaf"
                if r["implicit_maqaf"]
                else ("maqaf" if r["maqaf_after"] else "none")
            )
            mq[
                "MAM %s / morphhb %s"
                % (m, "maqaf" if r["w"]["maqaf_after"] else "none")
            ] += 1
    F["maqaf"] = dict(mq)
    F["notes"] = (
        "Computed by py/morphhb_on_mam/figures.py from the work directory's 10-atoms.jsonl and 11-unmatched-morphhb.jsonl; Claude (Opus 5.5), 2026-11-15."
    )
    json_path = out_dir / "30-figures.json"
    json_path.write_text(
        json.dumps(F, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    lines = []
    for k, v in F.items():
        lines.append("%s: %s" % (k, v))
    text_path = out_dir / "30-figures.txt"
    text_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(
        "wrote %s and %s"
        % (record_paths.shown(json_path), record_paths.shown(text_path))
    )
