"""Taamey D's corpus refresh, which py/main_taamey_d.py corpus runs.

This module was restructured on 2026-10-29 from hbofonts'
main_bible_words_update_fr_mam_n_uxlc.py.  It refreshes the
Taamey-D/qa-in/bible_words_*.testcases.json test cases from MAM's and the UXLC's word
lists in this repository, out/mam-qere-words.json and uxlc/out/uxlc-words.json.
hbofonts read them from its forest's MAM-basics clone, which it found through Git's
common directory; this module reads them under paths.repo_root(), the top level of this
checkout, so a linked worktree reads its own lists.  New test cases have no expected
outputs, so a refresh is followed by a Taamey D baseline acceptance, py/main_taamey_d.py
accept-baseline, which needs Ben's approval.

With --check (check=True), it computes the same refresh and reports it, but writes
nothing.  The mega's taamey-d-corpus step runs it that way.  It then reads the word lists
in the working tree, committed or not, so that a mega run after a MAM refresh reports a
pending refresh, which the report's last line calls REFRESH PENDING, rather than failing.
Without --check, it refuses to run while either word list has uncommitted changes.  In
either mode, an error that would stop a refresh, such as an unrecognized ZWJ or an SLH
word that the multirun check cannot split, raises.
"""

import collections
import functools
import json
import re
import subprocess

from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn.git_process import git_command
from mb_cmn.provenance import this_repo_name
from taamey_d.qa import check_mrun as mrun
from taamey_d.qa.check_helpers import word_chars, xform_word_chars

# Paths within this repository, whose mega writes them in its wordlist and
# uxlc-word-list steps, before its taamey-d-corpus step reads them
_WORDLIST_PATH_FOR_MAM = "out/mam-qere-words.json"
_WORDLIST_PATH_FOR_UXLC = "uxlc/out/uxlc-words.json"
_QA_IN = paths.repo_root() / "Taamey-D" / "qa-in"


def _shown(path):
    # A path as printed: relative to the repository root, Taamey-D/qa-in/..., rather
    # than one machine's absolute path.
    return path.relative_to(paths.repo_root()).as_posix()


def _dump(fc, fp):
    json.dump(fc, fp, indent=0, ensure_ascii=False)
    fp.write("\n")


def _refresh(tcases_fnas, provenance):
    # Computes every bible_words file's new contents before any is written, so
    # that --check reports exactly what a real run writes, and an error stops a
    # real run before it has written anything. Returns (fna, fc, out_fc) triples.
    fcs = []
    for tcases_fna in tcases_fnas:
        with open(tcases_fna, encoding="utf-8") as infp:
            fcs.append(json.load(infp))  # fc: file contents
    # _remove_outdated deletes from provenance each word that a file keeps, so
    # what is left is new. New test cases go to the highest-numbered file.
    out_tcases = [_remove_outdated(fc["testcases"], provenance) for fc in fcs]
    out_tcases[-1] = _add_new(out_tcases[-1], provenance)
    return [
        (tcases_fna, fc, dict(fc, testcases=tcases))
        for tcases_fna, fc, tcases in zip(tcases_fnas, fcs, out_tcases)
    ]


def _counts(testcases, out_tcases):
    # How a refresh changes one file: its test cases before and after, and how
    # many it drops, adds and relabels (gives a new provenance). Of a file's test
    # cases with the same input, _remove_outdated keeps only the first.
    before = {}
    for testcase in testcases:
        before.setdefault(_make_hashable2(testcase["input"]), testcase)
    kept = relabelled = 0
    for testcase in out_tcases:
        old = before.get(_make_hashable2(testcase["input"]))
        if old is not None:
            kept += 1
            if old.get("provenance") != testcase["provenance"]:
                relabelled += 1
    return collections.Counter(
        before=len(testcases),
        after=len(out_tcases),
        drop=len(testcases) - kept,
        add=len(out_tcases) - kept,
        relabel=relabelled,
    )


def _print_counts(name, counts):
    print(
        f"{name}: {counts['before']} -> {counts['after']} test cases"
        f" (drop {counts['drop']}, add {counts['add']}, relabel {counts['relabel']})"
    )


def _remove_outdated(testcases, provenance):
    # Here "remove outdated" is really short for
    # "re-add all that have not become outdated".
    out_tcases = []
    for testcase in testcases:
        tinput = _make_hashable2(testcase["input"])
        if tinput in provenance:  # if tinput is not outdated
            # Below, we possibly update provenance of the test case.
            new_tcase = dict(testcase, provenance=provenance[tinput])
            out_tcases.append(new_tcase)
            del provenance[tinput]
    return out_tcases


def _add_new(testcases, provenance):
    out_tcases = testcases
    # Sorted, because the dict's order comes from a set's, which varies from run to
    # run: two runs on the same word lists must write the same file.
    for word in sorted(provenance, key=_sort_key):
        new_tcase = dict(input=word, provenance=provenance[word])
        out_tcases.append(new_tcase)
    return out_tcases


def _sort_key(word):
    # An SLH word sorts by its characters, then by its other three elements.
    if isinstance(word, str):
        return (word,)
    return tuple(word)


_ATNAX_ZWJ_XIRIQ = (
    "\N{HEBREW ACCENT ETNAHTA}" + "\N{ZERO WIDTH JOINER}" + "\N{HEBREW POINT HIRIQ}"
)
_ATNAX_CGJ_XIRIQ = (
    "\N{HEBREW ACCENT ETNAHTA}"
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT HIRIQ}"
)
_MERKHA_ZWJ_XIRIQ = (
    "\N{HEBREW ACCENT MERKHA}" + "\N{ZERO WIDTH JOINER}" + "\N{HEBREW POINT HIRIQ}"
)
_MERKHA_CGJ_XIRIQ = (
    "\N{HEBREW ACCENT MERKHA}"
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT HIRIQ}"
)
_REVIA_ZWJ_GERESH_MUQDAM = (
    "\N{HEBREW ACCENT REVIA}"
    + "\N{ZERO WIDTH JOINER}"
    + "\N{HEBREW ACCENT GERESH MUQDAM}"
)
_REVIA_GERESH_MUQDAM = "\N{HEBREW ACCENT REVIA}" + "\N{HEBREW ACCENT GERESH MUQDAM}"
# Ben, 2026-10-27, of the UXLC's zero-width joiner (ZWJ) between atnax and xiriq
# in Job 32:6, where a combining grapheme joiner (CGJ) belongs: "We don't need to
# (and should not) bend over backwards to support incorrectly encoded words in
# Taamey D." So a word with one of this closed table's encoding errors enters the
# corpus in its correct encoding instead, with a provenance suffix saying so.
# Each row is (wrong sequence, correct sequence, provenance suffix). The rows
# correct UXLC 2.6's three wacky ZWJs (see _reject_wacky_zwjs), each in one atom
# of Job, as section 8 of MAM-basics' doc/uxlc-potential-corrections.md
# recommends by Ben's decision of 2026-10-27.
_ENCODING_CORRECTIONS = (
    (_ATNAX_ZWJ_XIRIQ, _ATNAX_CGJ_XIRIQ, "-cgj"),  # Job 32:6
    (_MERKHA_ZWJ_XIRIQ, _MERKHA_CGJ_XIRIQ, "-cgj"),  # Job 10:15
    (_REVIA_ZWJ_GERESH_MUQDAM, _REVIA_GERESH_MUQDAM, "-nozwj"),  # Job 19:16
)


def _correct_encoding(word, prov):
    chars = word_chars(word)
    for wrong, right, suffix in _ENCODING_CORRECTIONS:
        if wrong in chars:
            new_word = xform_word_chars(word, lambda wc: wc.replace(wrong, right))
            return new_word, prov + suffix
    return word, prov


def _correct_encodings(provenance):
    out_provenance = {}
    for word, prov in provenance.items():
        new_word, new_prov = _correct_encoding(word, prov)
        assert new_word not in out_provenance, f"correction collides: {new_word}"
        out_provenance[new_word] = new_prov
    return out_provenance


_MEDIAL_METEG_REQUESTS = tuple(
    xataf + "\N{ZERO WIDTH JOINER}" + "\N{HEBREW POINT METEG}"
    for xataf in (
        "\N{HEBREW POINT HATAF SEGOL}",
        "\N{HEBREW POINT HATAF PATAH}",
        "\N{HEBREW POINT HATAF QAMATS}",
    )
)


def _reject_wacky_zwjs(provenance):
    # Ben, 2026-10-27: "add a check that will reject future wacky uses of ZWJ".
    # The Unicode Standard's Hebrew section uses the ZWJ only to request a meteg
    # in the middle of a xataf vowel, which the UXLC encodes xataf vowel, ZWJ,
    # meteg. Any other ZWJ that _ENCODING_CORRECTIONS leaves is wacky, and it
    # stops the update until someone decides the word's correct encoding.
    for word, prov in provenance.items():
        chars = word_chars(word)
        for request in _MEDIAL_METEG_REQUESTS:
            chars = chars.replace(request, "")
        if "\N{ZERO WIDTH JOINER}" in chars:
            raise ValueError(
                f"wacky ZWJ in {word!r} ({prov}): add a row to _ENCODING_CORRECTIONS"
            )


_UZARQA = "\N{HEBREW ACCENT ZARQA}"  # either zarqa helper or tsinorrit
_UZINOR = "\N{HEBREW ACCENT ZINOR}"  # either true zarqa or tsinor
_QUCPO_QMCPR = (
    "\N{HEBREW POINT QAMATS}"
    + "\N{HEBREW POINT METEG}"  # U (undermark) is M (meteg)
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT PATAH}"
    + "\N{HEBREW ACCENT REVIA}"
)  # O (overmark) is R (revia)
_QUCPO_QECPG = (
    "\N{HEBREW POINT QAMATS}"
    + "\N{HEBREW ACCENT ETNAHTA}"  # U (undermark) is E (etnachta)  # translit-ok
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT PATAH}"
    + "\N{HEBREW ACCENT GERESH}"
)  # O (overmark) is G (geresh)
_QUOCP_QMRCP = (
    "\N{HEBREW POINT QAMATS}"
    + "\N{HEBREW POINT METEG}"  # U (undermark) is M (meteg)
    + "\N{HEBREW ACCENT REVIA}"  # O (overmark) is R (revia)
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT PATAH}"
)
_QUOCP_QEGCP = (
    "\N{HEBREW POINT QAMATS}"
    + "\N{HEBREW ACCENT ETNAHTA}"  # U (undermark) is E (etnachta)  # translit-ok
    + "\N{HEBREW ACCENT GERESH}"  # O (overmark) is G (geresh)
    + "\N{COMBINING GRAPHEME JOINER}"
    + "\N{HEBREW POINT PATAH}"
)


def _extra(word, prov):
    chars = word_chars(word)
    # Below, we return early, on the assumption that a word never satisfies
    # more than one of these criteria for requiring an extra.
    if _UZARQA in chars and _UZINOR in chars:
        return _make_extra(word, prov + "-zizi", _UZARQA, _UZINOR)
    if _QUCPO_QMCPR in chars:
        return _make_extra(word, prov + "-quocp", _QUCPO_QMCPR, _QUOCP_QMRCP)
    if _QUCPO_QECPG in chars:
        return _make_extra(word, prov + "-quocp", _QUCPO_QECPG, _QUOCP_QEGCP)
    return None


def _make_extra(word, new_prov, repl0, repl1):
    new_word = xform_word_chars(word, lambda wc: wc.replace(repl0, repl1))
    return new_word, new_prov


def _um_provenance(word, wordset_mam, wordset_uxlc):
    provenance = ""
    if word in wordset_mam:
        provenance += "M"
    if word in wordset_uxlc:
        provenance += "U"
    return provenance


_STRIP_SET = set(
    (
        "\N{HEBREW PUNCTUATION SOF PASUQ}",
        "\N{HEBREW PUNCTUATION PASEQ}",
        "\N{HEBREW PUNCTUATION MAQAF}",
        "\N{SPACE}",
    )
)


def _strip_punc(word):
    assert isinstance(word, str)
    retword = word
    while retword[-1] in _STRIP_SET:
        retword = retword[:-1]
    return retword


def _make_hashable2(foo):
    if isinstance(foo, list):
        return tuple(map(_make_hashable2, foo))
    return foo


def _make_hashable(word_records):
    return map(_make_hashable2, word_records)


_PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"


def _without_slh_paseq(word):
    # MAM-basics' word list splits its other words at a PASEQ, but it takes an SLH
    # (small, large or hung letter) word whole. So since its regeneration of
    # 2026-03-16 (MAM-basics 1a954cc2), two SLH words, in Esther 1:6 and Ruth 3:13,
    # end in a PASEQ, with a spine position for it, which the multirun check cannot
    # split. Drop both, as the list does for its other words.
    if isinstance(word, str):
        return word
    chars, spine, kinds, summary = word
    if not chars.endswith(_PASEQ):
        return word
    if not spine.endswith("."):
        raise ValueError(f"SLH spine marks a final PASEQ: {word!r}")
    return chars[:-1], spine[:-1], kinds, summary


def _check_slh_words(provenance):
    # The multirun check splits an SLH word into one letter cluster per position of
    # its spine. Split every SLH word here first, so that a change in MAM-basics'
    # SLH words stops the update rather than the shaping checks.
    for word, prov in provenance.items():
        if not isinstance(word, str):
            try:
                mrun.mrun_split(word)
            except ValueError as error:
                raise ValueError(f"SLH word {word!r} ({prov}): {error}") from error


def _git(repo, *args):
    # Trust exactly this repository, as git_process.git_command does. Take no
    # optional lock, so that a status refreshes no index: the mega's taamey-d-corpus
    # step runs --check, which must write nothing, while this checkout may be in use.
    command = git_command(repo, "--no-optional-locks", *args)
    result = subprocess.run(
        command, stdout=subprocess.PIPE, check=True, encoding="utf-8"
    )
    return result.stdout


def _word_lists_root(check):
    # This repository's root, the top level of this checkout, so that a linked
    # worktree reads its own word lists rather than its home clone's. Without
    # --check, its word lists must be committed, so that a refresh's commit message
    # can name the commit the refresh came from. With --check, they may have
    # uncommitted changes, as they do when the mega has just regenerated them after
    # a MAM refresh, and the line naming the commit then says so.
    root = paths.repo_root()
    wordlists = _WORDLIST_PATH_FOR_MAM, _WORDLIST_PATH_FOR_UXLC
    changes = _git(root, "status", "--porcelain", "-z", "--", *wordlists)
    if changes and not check:
        raise RuntimeError(f"uncommitted word lists in {this_repo_name()}: {changes!r}")
    head = _git(root, "rev-parse", "HEAD").strip()
    uncommitted = ", with uncommitted changes" if changes else ""
    print(f"word lists from {this_repo_name()} at {head}{uncommitted}")
    return root


_BIBLE_WORDS_FNA = re.compile(r"bible_words_(\d+)\.testcases\.json")


def _bible_words_fnas():
    # Only the bible_words_<n> files are this updater's. The other test case files
    # in Taamey-D/qa-in, such as mam_doc_notes and near_aleppo_ketiv, are written by
    # hand, and their inputs are in neither word list, so _remove_outdated would empty
    # them. Ordered by number, so that new test cases go to the highest-numbered.
    numbered = []
    for fna in _QA_IN.glob("bible_words_*.testcases.json"):
        match = _BIBLE_WORDS_FNA.fullmatch(fna.name)
        if not match:
            raise ValueError(f"unexpected Bible words file name: {_shown(fna)}")
        numbered.append((int(match.group(1)), fna))
    if not numbered:
        raise FileNotFoundError("no Taamey-D/qa-in/bible_words_*")
    return [fna for _, fna in sorted(numbered)]


def _provenance(root):
    # Maps each word that the corpus should have to its provenance: M (MAM), U (the
    # UXLC) or MU (both), with a suffix for a corrected encoding or an extra.
    with open(root / _WORDLIST_PATH_FOR_MAM, encoding="utf-8") as infp:
        hashable = _make_hashable(json.load(infp))
        wordset_mam = set(map(_without_slh_paseq, hashable))
    with open(root / _WORDLIST_PATH_FOR_UXLC, encoding="utf-8") as infp:
        no_punc = map(_strip_punc, json.load(infp))
        wordset_uxlc = set(no_punc)

    provenance = {}
    for word in wordset_mam | wordset_uxlc:
        provenance[word] = _um_provenance(word, wordset_mam, wordset_uxlc)
    provenance = _correct_encodings(provenance)
    _reject_wacky_zwjs(provenance)
    extras = []
    for word, prov in provenance.items():
        extra = _extra(word, prov)
        if extra:
            extras.append(extra)
    for extra in extras:
        extraword, extraprov = extra
        if extraword not in provenance:
            provenance[extraword] = extraprov
    _check_slh_words(provenance)
    return provenance


def refresh_corpus(check=False):
    """Refresh the Bible-words test cases, or with check only report the refresh.

    Print the commit the word lists come from, then how many test cases each file and
    all of them together drop, add and relabel.  Without check, write every
    bible_words file and return None.  With check, write nothing, and return True if a
    refresh is pending, which the last line printed calls REFRESH PENDING, or False if
    none is.
    """
    tcases_fnas = _bible_words_fnas()
    root = _word_lists_root(check)
    refreshed = _refresh(tcases_fnas, _provenance(root))
    totals = collections.Counter()
    for tcases_fna, fc, out_fc in refreshed:
        counts = _counts(fc["testcases"], out_fc["testcases"])
        _print_counts(_shown(tcases_fna), counts)
        totals.update(counts)
    _print_counts("total", totals)
    if not check:
        for tcases_fna, _, out_fc in refreshed:
            file_io.with_tmp_openw(
                tcases_fna, {"newline": ""}, functools.partial(_dump, out_fc)
            )
        return None
    if totals["drop"] or totals["add"] or totals["relabel"]:
        print(
            "check only, nothing written: REFRESH PENDING"
            " (Taamey-D/README.md says how to refresh)"
        )
        return True
    print("check only, nothing written: no refresh pending")
    return False
