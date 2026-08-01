"""Find accent changes in UXLC-misc/all_changes.json.

An "accent change" (per request) is a change that involves any of:
  - changing an accent (te'am) to a different accent
  - adding or removing an accent
  - adding or removing a maqaf

Silluq vs meteg: Unicode METEG (U+05BD) encodes both the narrow meteg (secondary
stress) and silluq (the verse-final disjunctive accent). We are NOT interested in
narrow meteg, but silluq IS an accent (silluq added / removed / changed to another
accent all count). Operationally, silluq = the LAST U+05BD in the verse-final word,
i.e. the last `meteg` token in the space-delimited segment that contains
`sof-pasuq`. That one token is relabelled `silluq` and treated as a te'am; every
other `meteg` is narrow meteg and ignored entirely.

Marks in the refuni/changeuni token fields attach to their preceding letter.
We therefore anchor each accent to its base letter, align the two letter
sequences, and compare the accent marks per letter. This is robust to
difflib's arbitrary choice of which token "moved" in a pure reorder, and to
letter insertions/deletions shifting positions.

Notes / deliberate scope decisions:
  - `segol` is treated as the VOWEL, not the accent segolta: in this corpus the
    accent name segolta is never spelled out, and `segol` is always the vowel
    (verified: accent-typed records containing `segol` always change a different,
    distinctly-named te'am).
  - `paseq` / `sof-pasuq` are punctuation/dividers, not te'amim -> excluded.
  - Narrow `meteg` changes (add/remove/move a meteg that is NOT the verse-final
    silluq) are EXCLUDED.
  - The curated refuni/changeuni are sometimes stale (== each other) while the
    real change is in *_gen; we use `*_gen or *` for each side.
"""

import json
import collections
import sys

from accgram import prose_ob_notes

import wlc_paths

ACC = {
    "etnachta",  # translit-ok: UXLC accent names
    "etnahta",  # translit-ok: UXLC accent names
    "atnah-hafukh",  # translit-ok: UXLC accent names
    "zarqa",
    "zinor",  # translit-ok: UXLC accent names
    "pashta",
    "yetiv",  # translit-ok: UXLC accent names
    "tevir",
    "geresh",
    "geresh-muqdam",
    "gereshayim",
    "gershayim",
    "telisha-gedola",
    "telisha-qetana",
    "pazer",
    "munah",  # translit-ok: UXLC accent names
    "mahapakh",  # translit-ok: UXLC accent names
    "makhapakh",
    "merkha",
    "darga",
    "qadma",
    "yerah-ben-yomo",  # translit-ok: UXLC accent names
    "ole",
    "iluy",  # translit-ok: UXLC accent names
    "dehi",  # translit-ok: UXLC accent names
    "revia",
    "zaqef-qatan",
    "zaqef-gadol",
    "tipeha",  # translit-ok: UXLC accent names
    "shalshelet",  # translit-ok: UXLC accent names
}
CONS = {
    "alef",
    "ayin",
    "bet",
    "dalet",
    "final-kaf",
    "final-mem",
    "final-nun",
    "final-pe",
    "final-tsadi",
    "gimel",
    "gimelt",
    "he",
    "het",
    "kaf",
    "lamed",
    "mem",
    "nun",
    "pe",
    "qof",
    "resh",
    "samekh",
    "shin",
    "tav",
    "tet",
    "tsadi",
    "vav",
    "yod",
    "zayin",
}


def relabel_silluq(tokens):
    """Rename the verse-final silluq (last `meteg` in the sof-pasuq segment) to
    `silluq`; leave all other `meteg` tokens (narrow meteg) untouched."""
    toks = list(tokens)
    if "sof-pasuq" not in toks:
        return toks
    sp = max(i for i, t in enumerate(toks) if t == "sof-pasuq")
    left = max([i for i in range(sp) if toks[i] == "space"], default=-1) + 1
    metegs = [i for i in range(left, sp + 1) if toks[i] == "meteg"]
    if metegs:
        toks[metegs[-1]] = "silluq"
    return toks


def ref_chg(d):
    r = d.get("refuni_gen") or d.get("refuni") or ""
    c = d.get("changeuni_gen") or d.get("changeuni") or ""
    return relabel_silluq(r.split()), relabel_silluq(c.split())


# silluq is a te'am for our purposes; narrow meteg is ignored.
ACC_S = ACC | {"silluq"}


def units(tokens):
    """Split into letter-units: [letter, [te'am marks in order]].

    Te'am = ACC_S (accents + silluq); narrow meteg is ignored. A leading '^'
    sentinel holds any marks before the first letter."""
    us = [["^", []]]
    for t in tokens:
        if t in CONS:
            us.append([t, []])
        elif t in ACC_S:
            us[-1][1].append(t)
    return us


def maqaf_count(tokens):
    return sum(1 for t in tokens if t == "maqaf")


def classify(d):
    """Return a reason label ('maqaf', 'accent', 'silluq', or '+'-joined combo)
    or None if the record is not an accent change."""
    a, b = ref_chg(d)
    reasons = set()
    if maqaf_count(a) != maqaf_count(b):
        reasons.add("maqaf")
    # A change to the letter skeleton (qere/ketiv orthography) where an accent
    # merely re-anchors to a neighbouring letter is not an accent-layer change.
    if [t for t in a if t in CONS] == [t for t in b if t in CONS]:
        ua, ub = units(a), units(b)
        for ka, kb in zip(ua, ub):
            ma, mb = ka[1], kb[1]
            if ma != mb:
                reasons.add("silluq" if "silluq" in set(ma) | set(mb) else "accent")
    if not reasons:
        return None
    return "+".join(sorted(reasons))


def record_key(d):
    """Identity of a change record: (release, changeset, n)."""
    return (d.get("release"), d.get("changeset"), d.get("n"))


def _parse_uxlc_change(compact):
    """Parse a compact UXLC change ref into a (release, changeset, n) key.

    The compact ref "2021.04.01/2020.12.06-2" is release/changeset-n (the same
    form `rtms_report.expand_uxlc_change_ref` expands to a tanach.us URL).
    Returns None for anything that is not a well-formed compact ref."""
    if not isinstance(compact, str):
        return None
    release, sep, changeset_n = compact.partition("/")
    if not sep:
        return None
    changeset, sep, n_str = changeset_n.rpartition("-")
    if not sep or not n_str.isdigit():
        return None
    return (release, changeset, int(n_str))


def prose_st_uxlc_change_keys():
    """Map (release, changeset, n) -> (structured-text ref, is_pending) for every
    `uxlc_change` / `pending_uxlc_change` named by a prose structured-text
    entry. `is_pending` is True when the ref came from `pending_uxlc_change`
    (a change accepted upstream but not yet in a stable release)."""
    keys = {}
    for ref, entry in prose_ob_notes.STRUCTURED_TEXT_BY_REF.items():
        for field, pending in (("uxlc_change", False), ("pending_uxlc_change", True)):
            key = _parse_uxlc_change(entry.get(field))
            if key is not None:
                keys[key] = (ref, pending)
    return keys


def main():
    src = wlc_paths.in_dir() / "UXLC-misc" / "all_changes.json"
    out = wlc_paths.in_dir() / "accgram" / "uxlc_accent_changes.json"
    data = json.load(open(src, encoding="utf-8"))
    prose_st_keys = prose_st_uxlc_change_keys()
    result = []
    for d in data:
        reason = classify(d)
        if reason:
            rec = dict(d)
            rec["accent_change_reason"] = reason
            ref, pending = prose_st_keys.get(record_key(d), (None, None))
            rec["prose_st_ref"] = ref
            rec["prose_st_pending"] = pending
            result.append(rec)
    if "--audit" in sys.argv:
        print("total records:", len(data))
        print("flagged:", len(result))
        print(
            "by reason:", collections.Counter(r["accent_change_reason"] for r in result)
        )
        # bug check: no flagged record may have identical ref/chg representations
        bug = [
            r
            for r in result
            if ref_chg(r)[0] == ref_chg(r)[1] and r["accent_change_reason"] != "maqaf"
        ]
        print("BUG (identical ref/chg yet flagged non-maqaf):", len(bug))
        # prose structured-text coverage
        matched = {record_key(r) for r in result if r["prose_st_ref"]}
        pending = sum(1 for r in result if r["prose_st_pending"])
        print("prose uxlc_change refs:", len(prose_st_keys))
        print(
            "  matched to a flagged accent change:",
            len(matched),
            f"({pending} pending)",
        )
        unmatched = {k: v for k, v in prose_st_keys.items() if k not in matched}
        if unmatched:
            print("  NOT matched (ref not an accent change / not in data):")
            for k, (ref, is_pending) in sorted(
                unmatched.items(), key=lambda kv: kv[1][0]
            ):
                tag = " [pending]" if is_pending else ""
                print(f"    {ref}{tag}: {k[0]}/{k[1]}-{k[2]}")
        return
    with open(out, "w", encoding="utf-8", newline="") as out_fp:
        json.dump(result, out_fp, ensure_ascii=False, indent=2)
    print(f"Wrote {len(result)} accent-change records to {out}")


if __name__ == "__main__":
    main()
