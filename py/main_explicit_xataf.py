"""Extract explicit-xataf words from נוסח notes that target varika words.

For (nearly) every word with varika (U+FB1E), creates a verse-tagged mapping
of that word to its "explicit xataf" version — the word as it appears in
manuscripts that write the ḥataf vowel explicitly instead of shewa+varika.
"""

import json
import sys

from pycmn import bib_locales as tbn
from pycmn import read_books_from_mam_parsed_plus as plus
from pycmn import ws_tmpl2 as wtp
from pycmn import file_io

from py_explicit_xataf import extract as ext
from py_explicit_xataf import extras
from py_explicit_xataf import infer
from py_explicit_xataf.entries import make_entries


def _bcvt_to_ref(bcvt):
    """Convert a bcvt tuple to a human-readable reference string."""
    bk39id, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvt)
    return f"{bk39id} {chnu}:{vrnu}"


def _process_one_book(bkid, book_mpp):
    """Process one book, returning (mappings, failures, extras)."""
    mappings = []
    failures = []
    extra_list = []
    verses = book_mpp["verses_plus"]
    for bcvt, minirow in verses.items():
        ref = _bcvt_to_ref(bcvt)
        for column in (minirow.CP, minirow.EP):
            nusach_tmpls = ext.find_nusach_tmpls(column)
            for tmpl in nusach_tmpls:
                arg0 = wtp.template_param_val(tmpl, "1")
                arg1 = wtp.template_param_val(tmpl, "2")
                if ext.has_varika(arg0):
                    varika_word = ext.flatten_text(arg0)
                    xataf_word, match_kind, sigla_detail = ext.extract_xataf_word(arg1)
                    if xataf_word is not None:
                        entries = make_entries(
                            ref, varika_word, xataf_word, match_kind, sigla_detail
                        )
                        mappings.extend(entries)
                    else:
                        failures.append(
                            {
                                "ref": ref,
                                "varika_word": varika_word,
                                "reason": ext.classify_failure(arg1),
                                "arg1_strings": ext.flatten_arg1_strings(arg1),
                            }
                        )
                else:
                    joined = ext.join_arg1_strings(arg1)
                    if "חטף" in joined:
                        extra_list.append(
                            {
                                "ref": ref,
                                "target_word": ext.flatten_text(arg0),
                                "nusach_comment": joined,
                            }
                        )
    return mappings, failures, extra_list


def _read_manual_overrides():
    """Read manual xataf mappings for cases too complex to extract automatically."""
    path = "in/explicit-xataf-manual.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _apply_manual_overrides(all_mappings, all_failures):
    """Merge manual overrides: add to mappings, remove from failures."""
    manual = _read_manual_overrides()
    manual_by_ref_word = {(m["ref"], m["varika_word"]): m for m in manual}
    remaining_failures = []
    for failure in all_failures:
        key = (failure["ref"], failure["varika_word"])
        if key in manual_by_ref_word:
            all_mappings.append(manual_by_ref_word.pop(key))
        else:
            remaining_failures.append(failure)
    for m in manual_by_ref_word.values():
        all_mappings.append(m)
    return remaining_failures


def _flag_non_inferrable(entries):
    """Flag entries where the inferred ḥataf vowel doesn't match the actual one."""
    n = 0
    for entry in entries:
        if not infer.is_inferrable(entry["varika_word"], entry["xataf_word"]):
            entry["non-inferrable"] = True
            n += 1
    return n


def _compute_counts(mappings):
    """Compute counts of flagged entries."""
    suffixed = {}
    n_ni = 0
    n_neither = 0
    n_multi_varika = 0
    for entry in mappings:
        sigla = entry.get("sigla", "")
        for s in sigla.split(","):
            if s.endswith("?") or s.endswith("!"):
                suffixed[s] = suffixed.get(s, 0) + 1
        if entry.get("non-inferrable"):
            n_ni += 1
        if entry.get("neither-lc-nor-ac-mentioned"):
            n_neither += 1
        if entry.get("varika-count"):
            n_multi_varika += 1
    counts = {}
    for s, n in sorted(suffixed.items()):
        counts[f"siglum {s}"] = n
    counts["varika-count > 1"] = n_multi_varika
    counts["non-inferrable"] = n_ni
    counts["neither-lc-nor-ac-mentioned"] = n_neither
    return counts


def almost_main():
    sys.stdout.reconfigure(encoding="utf-8")
    books_mpp = plus.read_parsed_plus_bk39s()
    all_mappings = []
    all_failures = []
    all_extras = []
    for bkid in tbn.ALL_BK39_IDS:
        if bkid not in books_mpp:
            continue
        mappings, failures, extra_list = _process_one_book(bkid, books_mpp[bkid])
        all_mappings.extend(mappings)
        all_failures.extend(failures)
        all_extras.extend(extra_list)
    all_failures = _apply_manual_overrides(all_mappings, all_failures)
    n_ni = _flag_non_inferrable(all_mappings)
    counts = _compute_counts(all_mappings)
    result = {
        "header": {
            "mapping_fields": {
                "ref": "Verse reference (e.g. 'Genesis 1:18')",
                "varika_word": "The word as it appears in MAM, with shewa+varika",
                "xataf_word": "The word with the explicit ḥataf vowel",
                "match_kind": "How the extraction matched: 'sigla=word', 'bare-word', or with '+joined' suffix",
                "sigla": "Manuscript sigla before the = sign (e.g. 'א', 'ל,ל1', 'א(ס),ל,ק3'). Individual sigla may have ? (uncertain) or ! (surprising) suffixes (e.g. 'ל,ק3?' means ק3 is uncertain).",
                "neither-lc-nor-ac-mentioned": "Present (true) only when sigla mentions neither LC (ל) nor AC (א).",
                "varika-count": "Present only when the word has more than one varika (implicit default: 1). E.g. Judges 7:7 has 2.",
                "non-inferrable": "Present (true) only when the xataf vowel cannot be inferred from the varika word by standard rules.",
            },
            "failure_fields": {
                "ref": "Verse reference",
                "varika_word": "The word as it appears in MAM, with shewa+varika",
                "reason": "Short classification of why extraction failed",
                "arg1_strings": "Raw string fragments from the nusach note's second argument",
            },
        },
        "counts": counts,
        "failures": all_failures,
        "mappings": all_mappings,
    }
    out_path = "out/explicit-xataf.json"
    file_io.json_dump_to_file_path(result, out_path)
    n_m, n_f = len(all_mappings), len(all_failures)
    print(f"Wrote {n_m} mappings and {n_f} failures to {out_path}")
    counts_str = json.dumps(counts, ensure_ascii=False, indent=2)
    print(f"  Counts: {counts_str}")
    extras.write_extras(all_extras)


def main():
    almost_main()


if __name__ == "__main__":
    main()
