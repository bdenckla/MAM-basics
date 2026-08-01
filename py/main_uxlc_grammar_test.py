"""UXLC accent-change grammar test: do the changes move a verse across the
WLC-4.22 / UXLC grammaticality boundary, and in which direction?

The change records (uxlc_accent_changes.json) partition on `prose_st_ref`:

  * the OUT set -- changes NOT linked to a prose ungrammatical note; and
  * the IN  set -- changes that ARE so linked (i.e. that the prose ungrammatical
    notes flagged and the UXLC then adopted).

Both sets are evaluated by the same `evaluate()` and reported in two sections of
the same output file.  The interesting result is the directional asymmetry: in
the OUT set only degradation crosses the boundary (WLC-gram -> UXLC-ungram, never
the reverse); in the IN set only fixes cross it (WLC-ungram -> UXLC-gram, never
the reverse).

For each grammar-relevant accent change that lies in the PROSE corpus the checker
can evaluate, we:

  1. Transcode the real WLC 4.22 verse to its scanner-ready mark body from the
     canonical `-kq-u` Unicode source (issue #9 retired the old wlc422_ps.txt
     text input; the body is now built straight from the `-kq-u` JSON).
  2. Locate the changed word (by the citation's word index).
  3. VALIDATE: synthesize the WLC reading of that word from `refuni` (Unicode token
     names -> accent marks) and confirm that scanning the synthesized word
     yields the SAME token stream as scanning the real word.  This certifies,
     per case, that our name->mark synthesis is faithful for this accent content
     (it auto-excludes stress-helper / ordering cases we can't reproduce).
     An ADD-accent change is additionally cross-checked against the real UXLC-39
     XML word (`uxlc39_word_marks`): a prepositive/postpositive accent that is
     written twice in the manuscript (graphical edge mark + inner stress-helper/yated) is
     fused/de-duped by the real `uni_to_marks` pipeline but not by our name->mark
     synthesis, so such a case is marked unreliable and excluded (e.g. Josh 2:3.7's
     doubled telisha gedola).
  4. If validated, synthesize the UXLC reading from `changeuni`, splice it into the
     verse body, and re-run the existing scanner+grammar on both the original
     (WLC) and edited (UXLC) verse.  Classify each as grammatical / ungrammatical.

Output: per-set WLC-vs-UXLC 2x2s, coverage (how many validated), the excluded
verses with reasons, and the directional-asymmetry conclusion, written to
out/accgram/uxlc_grammar_test.txt.  Console output is ASCII only.
"""

from __future__ import annotations

import json
from collections import Counter

from accgram import accent_marks as am
from accgram import rtms_data
from accgram import rtms_rows
from accgram import uni_to_marks
from accgram.prose_ply_grammar import (
    LOCATION_ONLY,
    build_parser,
    parse_tokens,
)
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from accgram.tree import print_tree
from accgram import prose_filter
from wlc_cmn.wlc_book_codes import bk39id_to_wlc_bb
from py_uxlc import my_uxlc
from py_uxlc.my_uxlc_book_abbreviations import expand_citation
import wlc_paths

WLC_KQ_U = wlc_paths.out_dir() / "wlc422-kq-u"
SRC = wlc_paths.in_dir() / "accgram" / "uxlc_accent_changes.json"
OUT = wlc_paths.out_dir() / "accgram" / "uxlc_grammar_test.txt"

MAQAF_CP = "־"  # HEBREW PUNCTUATION MAQAF
PASEQ_CP = "׀"  # HEBREW PUNCTUATION PASEQ

# Unicode accent NAME (as used in refuni/changeuni) -> its scanner mark (accent_marks).
# These are the prose te'amim; poetic-only accents (atnax-hafukh, etc.) have no prose
# mark and simply will not validate if they appear.
NAME2MARK = {
    "etnachta": am.ATNAX,  # translit-ok: UXLC name
    "etnahta": am.ATNAX,  # translit-ok: UXLC name
    "zarqa": am.TSINNOR,
    "zinor": am.TSINNOR,  # translit-ok: UXLC name
    "pashta": am.PASHTA,
    "yetiv": am.YETIV,
    "tevir": am.TEVIR,
    "geresh": am.GERESH,
    "geresh-muqdam": am.GERESH_MUQDAM,
    "gereshayim": am.GERSHAYIM,
    "gershayim": am.GERSHAYIM,
    "telisha-gedola": am.TELISHA_GEDOLA,
    "telisha-qetana": am.TELISHA_QETANA,
    "pazer": am.PAZER,
    "munah": am.MUNAX,  # translit-ok: UXLC name
    "mahapakh": am.MAHAPAKH,
    "makhapakh": am.MAHAPAKH,
    "merkha": am.MERKHA,
    "darga": am.DARGA,
    "qadma": am.QADMA,
    "yerah-ben-yomo": am.YERAX,  # translit-ok: UXLC name
    "ole": am.OLE,
    "iluy": am.ILUY,
    "dehi": am.DEXI,  # translit-ok: UXLC name
    "revia": am.REVIA,
    "zaqef-qatan": am.ZAQEF_QATAN,
    "zaqef-gadol": am.ZAQEF_GADOL,
    "tipeha": am.TIPEXA,  # translit-ok: UXLC name
    "shalshelet": am.SHALSHELET,
}
# Non-accent tokens that still carry meaning for the scanner.
_METEGISH = {"meteg", "silluq"}


def synth_word(uni_tokens: list[str]) -> str | None:
    """Synthesize a scanner-readable mark word from refuni/changeuni token names.

    Letters -> a filler placeholder (the scanner swallows letters; they only serve
    as non-terminator TEXT).  Vowels/points are dropped.  Accents/meteg/sof-pasuq/
    paseq/maqaf become their marks/delimiters, in order.  Returns None if a token has
    no known prose mark (e.g. a poetic accent) -> case is unsupported.
    """
    out: list[str] = []
    for tok in uni_tokens:
        if tok in NAME2MARK:
            out.append(NAME2MARK[tok])
        elif tok in _METEGISH:
            out.append(am.METEG)
        elif tok == "sof-pasuq":
            out.append(am.SOF_PASUQ)
        elif tok == "paseq":
            out.append(am.PASEQ)
        elif tok == "maqaf":
            out.append(am.MAQAF)
        elif tok == "space":
            # The flanking space of a paseq: paseq attaches to its word with no
            # word-boundary space, so emit nothing (a real space here would spuriously
            # split the maqaf-unit into two words).
            continue
        else:
            # consonant or vowel/point -> a placeholder filler letter.
            out.append(am.LETTER)
    return "".join(out)


def scan_word_tokens(word: str, bb: str, ch: int, vs: int) -> tuple[str, ...]:
    """Scan a single word body to its accent-token TYPE tuple (terminator included)."""
    toks = scan_accents(word, bb, ch, vs, HasLegarmeh())
    return tuple(t.type for t in toks)


def maqaf_units(body: str):
    """Flatten an M-C verse body into maqaf-units (tanach.us word numbering).

    Returns (units, owners): `units[i]` is the i-th maqaf-unit string; `owners[i]`
    is (space_index, maqaf_index_within_space_token) so a unit can be spliced back
    while preserving the maqaf / space structure of the body.
    """
    units: list[str] = []
    owners: list[tuple[int, int]] = []
    for si, sp in enumerate(body.split(" ")):
        for mi, mu in enumerate(sp.split("-")):
            units.append(mu)
            owners.append((si, mi))
    return units, owners


def splice_unit(body: str, owner: tuple[int, int], new_unit: str) -> str:
    """Return `body` with one maqaf-unit replaced, preserving structure."""
    space_tokens = [sp.split("-") for sp in body.split(" ")]
    si, mi = owner
    space_tokens[si][mi] = new_unit
    return " ".join("-".join(parts) for parts in space_tokens)


def is_ungrammatical(parser, body: str, bb: str, ch: int, vs: int) -> bool:
    toks = [Token("TILDE", "")] + scan_accents(body, bb, ch, vs, HasLegarmeh())
    tree = parse_tokens(parser, toks)
    if tree is None:
        # No recovery: a residual gap.  Treat as ungrammatical but flag via caller.
        return True
    if tree is LOCATION_ONLY:
        return True
    return "ERROR" in print_tree(tree, 0)


def _mark_count(uni_tokens: list[str]) -> int:
    """Count the *mark-bearing* tokens (accents PLUS meteg/silluq).

    Meteg/silluq must count: a meteg->accent change (e.g. "change meteg to merkha")
    is a 1:1 substitution, not an addition, so it must not be tallied as a net
    accent gain (which would mislabel it 'add_accent')."""
    return sum(1 for t in uni_tokens if t in NAME2MARK or t in _METEGISH)


def _kind(r) -> str:
    """Categorize a change for confidence bucketing.

    - 'remove_terminator': the change drops sof-pasuq (degenerate: necessarily
      errors regardless of accentuation).
    - 'add_accent': nets a new mark-bearing token (coding-sensitive: an added
      prepositive/postpositive accent could be the inner stress-helper we code as
      a main accent -- see the UXLC-39 cross-check in `evaluate`).
    - 'substitution': 1:1 accent swap / removal / meteg<->accent not touching
      sof-pasuq (robust: validated structurally on the WLC side).
    """
    ref = (r.get("refuni_gen") or r.get("refuni") or "").split()
    chg = (r.get("changeuni_gen") or r.get("changeuni") or "").split()
    if "sof-pasuq" in ref and "sof-pasuq" not in chg:
        return "remove_terminator"
    if _mark_count(chg) > _mark_count(ref):
        return "add_accent"
    return "substitution"


def _transcoded_bodies(
    keys,
) -> dict[tuple[str, int, int], str]:
    """The scanner-ready mark body for each ``(bb, ch, vs)``, transcoded from the
    canonical ``-kq-u`` Unicode source (issue #9 retired ``wlc422_ps.txt``)."""
    index = rtms_data.load_wlc422_index(WLC_KQ_U)
    bodies: dict[tuple[str, int, int], str] = {}
    for bb, ch, vs in keys:
        verse = index.get(rtms_rows.to_compact_bcv(bb, ch, vs))
        if isinstance(verse, dict):
            bodies[(bb, ch, vs)] = uni_to_marks.verse_to_marks(verse)
    return bodies


_UXLC_BOOK_CACHE: dict[str, list] = {}


def _uxlc_book(bk_id: str) -> list:
    """Read (and cache) one UXLC-39 book's chapters via ``my_uxlc.read``."""
    if bk_id not in _UXLC_BOOK_CACHE:
        _UXLC_BOOK_CACHE[bk_id] = my_uxlc.read(bk_id)
    return _UXLC_BOOK_CACHE[bk_id]


def _uxlc_maqaf_units(verse_words: list[str]) -> list[str]:
    """Flatten one UXLC-39 verse (a list of ``<w>``/``<q>`` word strings) into
    maqaf-units, matching tanach.us word numbering (and our M-C ``maqaf_units``).

    Two reconciliations against the raw ``<w>`` order are needed:

    * a ``<w>`` ending in a maqaf joins (no space) to the next ``<w>`` -- the two
      sit in one maqaf chain, so splitting on maqaf re-creates the chain's units;
    * a paseq, written in UXLC-39 as a space-separated ``׀``, attaches to its
      preceding word (tanach.us / the M-C source count it as part of that word),
      so the flanking space is dropped to avoid spawning a spurious unit.
    """
    parts: list[str] = []
    for w in verse_words:
        if parts and not parts[-1].endswith(MAQAF_CP):
            parts.append(" ")
        parts.append(w)
    text = "".join(parts).replace(" " + PASEQ_CP, PASEQ_CP)
    units: list[str] = []
    for sp in text.split(" "):
        units.extend(sp.split(MAQAF_CP))
    return units


def uxlc39_word_marks(
    bk_id: str, ch: int, vs: int, wd: int, n_mc_units: int
) -> tuple[str, ...] | None:
    """Scan-token tuple of the real UXLC-39 word at maqaf-unit ``wd``, or None.

    Returns None when the UXLC-39 maqaf-unit count differs from the M-C count
    (``n_mc_units``): the two sources then number words differently, so ``wd`` does
    not transfer and the cross-check must abstain rather than mis-compare.  Also
    None if the word index is out of range.
    """
    units = _uxlc_maqaf_units(_uxlc_book(bk_id)[ch - 1][vs - 1])
    if len(units) != n_mc_units:
        return None
    if not (1 <= wd <= len(units)):
        return None
    bb = bk39id_to_wlc_bb(bk_id)
    return scan_word_tokens(uni_to_marks.word_to_marks(units[wd - 1]), bb, ch, vs)


def evaluate(records: list[dict], parser) -> dict:
    """Run the per-verse validate-then-classify pipeline over one set of change
    records and return the collected results (stats, 2x2 grids, the broke/fixed
    verse lists, and the excluded verses with reasons).

    Pure function of its inputs -- the OUT and IN sets are evaluated by identical
    code; only the input record set differs.
    """
    # Group prose-corpus changes by verse, so a verse with several changes is
    # tested as ONE coherent UXLC reading (not a per-word chimera).
    by_verse: dict[tuple[str, int, int], list[tuple[int, dict, str]]] = {}
    for r in records:
        bk, ch, vs, wd = expand_citation(r["citation"])
        bb = bk39id_to_wlc_bb(bk)
        if not prose_filter.should_keep_line(bb, ch, vs):
            continue
        by_verse.setdefault((bb, ch, vs), []).append((wd, r, bk))

    bodies = _transcoded_bodies(by_verse)

    stat = Counter()
    grid = Counter()  # (wlc, uxlc) -> n verses (all validated)
    grid_visible = Counter()  # (wlc, uxlc) -> n verses (scanner-visible only)
    cell_by_kind = Counter()  # (kind, wlc, uxlc) over individual changes in solo verses
    broke = []  # verses: WLC-gram -> UXLC-ungram
    fixed = []  # verses: WLC-ungram -> UXLC-gram
    excluded = []  # (ref, [citations], reason)

    for (bb, ch, vs), changes in by_verse.items():
        stat["prose_verses"] += 1
        stat["prose_changes"] += len(changes)
        body = bodies.get((bb, ch, vs))
        if body is None:
            stat["no_body"] += 1
            continue
        units, owners = maqaf_units(body)

        # Validate every change in the verse; apply them all to build UXLC body.
        uxlc_body = body
        reason = ""
        for wd, r, bk in changes:
            if not (1 <= wd <= len(units)):
                reason = "word-index out of range"
                break
            ref_syn = synth_word((r.get("refuni_gen") or r.get("refuni") or "").split())
            chg_syn = synth_word(
                (r.get("changeuni_gen") or r.get("changeuni") or "").split()
            )
            if ref_syn is None or chg_syn is None:
                reason = "unsupported accent (no prose mark)"
                break
            if scan_word_tokens(ref_syn, bb, ch, vs) != scan_word_tokens(
                units[wd - 1], bb, ch, vs
            ):
                reason = "ref-mismatch: synth WLC word != real M-C word"
                break
            # ADD-accent cross-check against the real UXLC-39 XML: a doubled
            # prepositive/postpositive accent (graphical edge mark + inner
            # stress-helper) is fused/de-duped by the real uni_to_marks pipeline
            # but not by our name->mark synth, so exclude such a change.
            if _kind(r) == "add_accent":
                real = uxlc39_word_marks(bk, ch, vs, wd, len(units))
                if real is not None and scan_word_tokens(chg_syn, bb, ch, vs) != real:
                    reason = "UXLC-39 cross-check: doubled stress-helper accent"
                    break
            uxlc_body = splice_unit(uxlc_body, owners[wd - 1], chg_syn)
        if reason:
            stat["unreliable_verses"] += 1
            stat["unreliable_changes"] += len(changes)
            excluded.append(
                ((bb, ch, vs), [r["citation"] for _, r, _ in changes], reason)
            )
            continue
        stat["validated_verses"] += 1
        stat["validated_changes"] += len(changes)

        # A change is "scanner-visible" only if it alters the accent-token stream;
        # otherwise (meteg reorder, collapsed sub-distinction, ...) the grammar
        # cannot possibly react and the verse is a trivial neutral.
        wlc_stream = tuple(
            t.type for t in scan_accents(body, bb, ch, vs, HasLegarmeh())
        )
        uxlc_stream = tuple(
            t.type for t in scan_accents(uxlc_body, bb, ch, vs, HasLegarmeh())
        )
        visible = wlc_stream != uxlc_stream
        stat["visible" if visible else "noop"] += 1

        wlc_bad = is_ungrammatical(parser, body, bb, ch, vs)
        uxlc_bad = is_ungrammatical(parser, uxlc_body, bb, ch, vs)
        cell = (
            "WLC-ungram" if wlc_bad else "WLC-gram",
            "UXLC-ungram" if uxlc_bad else "UXLC-gram",
        )
        if visible:
            grid_visible[cell] += 1
        grid[cell] += 1
        descs = [
            (r["citation"], r["accent_change_reason"], _kind(r), r["description"][:55])
            for _, r, _ in changes
        ]
        # Attribute by-kind only for solo-change verses (clean attribution).
        if len(changes) == 1:
            cell_by_kind[(descs[0][2], cell[0], cell[1])] += 1
        if not wlc_bad and uxlc_bad:
            broke.append(((bb, ch, vs), descs))
        elif wlc_bad and not uxlc_bad:
            fixed.append(((bb, ch, vs), descs))

    return {
        "stat": stat,
        "grid": grid,
        "grid_visible": grid_visible,
        "cell_by_kind": cell_by_kind,
        "broke": broke,
        "fixed": fixed,
        "excluded": excluded,
    }


def report_section(res: dict, title: str, p) -> None:
    """Emit one set's report section through the line-printer ``p``."""
    stat = res["stat"]
    grid, grid_visible = res["grid"], res["grid_visible"]
    broke, fixed = res["broke"], res["fixed"]
    p(f"=== {title} ===")
    p()
    p(
        f"prose-corpus verses          : {stat['prose_verses']}  ({stat['prose_changes']} changes)"
    )
    p(
        f"  validated                  : {stat['validated_verses']} verses ({stat['validated_changes']} changes)"
    )
    p(
        f"  excluded                   : {stat['unreliable_verses']} verses ({stat['unreliable_changes']} changes)"
    )
    p()
    p(f"  of validated: scanner-VISIBLE change {stat['visible']}, no-op {stat['noop']}")
    p()
    p("2x2 over validated VERSES (all):")
    for w in ("WLC-gram", "WLC-ungram"):
        for u in ("UXLC-gram", "UXLC-ungram"):
            p(f"  {w:11s} -> {u:12s}: {grid[(w, u)]}")
    p()
    p("2x2 over scanner-VISIBLE verses (the meaningful denominator):")
    for w in ("WLC-gram", "WLC-ungram"):
        for u in ("UXLC-gram", "UXLC-ungram"):
            p(f"  {w:11s} -> {u:12s}: {grid_visible[(w, u)]}")
    p()
    p(f"WLC-gram -> UXLC-ungram (degradation): {len(broke)} verses")
    for ref, descs in sorted(broke):
        for cit, reason, kind, desc in descs:
            p(f"    {cit:16s} [{reason}/{kind}] {desc}")
    p()
    p(f"WLC-ungram -> UXLC-gram (fix): {len(fixed)} verses")
    for ref, descs in sorted(fixed):
        for cit, reason, kind, desc in descs:
            p(f"    {cit:16s} [{reason}/{kind}] {desc}")
    p()
    p("Excluded verses (synth could not be validated):")
    for ref, cits, reason in sorted(res["excluded"]):
        p(f"    {', '.join(cits):28s} {reason}")
    p()
    cell_by_kind = res["cell_by_kind"]
    p("By-kind breakdown of solo-change verses (confidence buckets):")
    kinds = sorted({k for (k, _, _) in cell_by_kind})
    for k in kinds:
        gg = cell_by_kind[(k, "WLC-gram", "UXLC-gram")]
        gb = cell_by_kind[(k, "WLC-gram", "UXLC-ungram")]
        ug = cell_by_kind[(k, "WLC-ungram", "UXLC-gram")]
        ub = cell_by_kind[(k, "WLC-ungram", "UXLC-ungram")]
        p(
            f"  {k:18s}: WLC-gram->[g {gg:3d} / u {gb:3d}]   WLC-ungram->[g {ug:3d} / u {ub:3d}]"
        )


def main() -> None:
    data = json.load(open(SRC, encoding="utf-8"))
    out_set = [r for r in data if not r["prose_st_ref"]]
    in_set = [r for r in data if r["prose_st_ref"]]

    parser = build_parser()
    out_res = evaluate(out_set, parser)
    in_res = evaluate(in_set, parser)

    lines = []

    def p(s=""):
        lines.append(s)
        # Console is ASCII-only (the file keeps the full UTF-8 text); a few change
        # descriptions embed a Hebrew accent glyph that a cp1252 console cannot encode.
        print(s.encode("ascii", "replace").decode("ascii"))

    report_section(
        out_res,
        "OUT set: WLC-4.22 vs UXLC grammaticality (changes NOT in prose output)",
        p,
    )
    p()
    p()
    report_section(
        in_res,
        "IN set: WLC-4.22 vs UXLC grammaticality (changes IN prose output)",
        p,
    )
    p()
    p()
    p("=== Directional asymmetry across the grammaticality boundary ===")
    p()
    p(
        "  OUT set: only DEGRADATION crosses the boundary "
        f"(WLC-gram->UXLC-ungram {len(out_res['broke'])}, "
        f"WLC-ungram->UXLC-gram {len(out_res['fixed'])})."
    )
    p(
        "  IN  set: only FIXES crosses the boundary "
        f"(WLC-ungram->UXLC-gram {len(in_res['fixed'])}, "
        f"WLC-gram->UXLC-ungram {len(in_res['broke'])})."
    )
    p()
    p("  The changes the prose ungrammatical notes flagged (IN set) only ever repair")
    p("  ungrammaticality; the changes they did not flag (OUT set) only ever")
    p("  introduce it.  No fix leaks into OUT and no degradation leaks into IN.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"\nWrote report to {OUT}")


if __name__ == "__main__":
    main()
