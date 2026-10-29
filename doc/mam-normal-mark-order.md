# MAM-normal order for Hebrew marks

This current reference carries the detailed repository-specific evidence and scope. The always-loaded rule remains in `AGENTS.md`.

## Hebrew marks go in MAM-normal order, not Unicode-normal order

Two orders exist for the combining marks of one base-letter cluster, and they differ on where the
dagesh sits:

- **MAM-normal order**, the one this repo uses. Shin dot, sin dot, dagesh/mapiq/shuruq dot
  (U+05BC) and dagesh ḥazaq (U+05C9) at the same priority, rafe, then every
  other mark in the relative order it already had. Spelled out and implemented in
  `py/mb_cmn/uni_denorm.py` — `give_std_mark_order` is the authority, `has_std_mark_order` the
  predicate. The code calls it "(our) standard mark order", and `py/check_mark_order.py` calls it
  "SBL2", after the SBL Hebrew Font recommendation to which the combining-class table's comment
  attributes the order, so grep for **std mark order** and **SBL2** as well as for this section's
  heading.
- **Unicode-normal order**, what `unicodedata.normalize` produces from the canonical combining
  classes (qamats 18, holam 19, dagesh 21, meteg 22). It puts the dagesh **after** the vowel.

`unicodedata.normalize` puts Hebrew marks in Unicode's order, not MAM's. So don't use it to
produce Hebrew that belongs in MAM's order, or to hide a mark-order mismatch that matters;
`give_std_mark_order` is the tool for both. A call that only asks what normalization would do,
as the fragility test in `py/mb_cmn/uni_norm_fragile.py` does, is fine. The two orders render
identically, so nothing looks wrong on the page and the defect surfaces only where something
compares bytes.

MAM's shipped data is entirely in MAM-normal order — checked 2026-08-04, `has_std_mark_order` true
for all 63 files now retained under `MAM-parsed/plus/` and `MAM-for-Sefaria/csv/`. So a cluster
in the other order is either hand-authored — and **the way in is a paste through anything that
normalizes, a browser above all** — or it sits upstream of the denormalizing step and belongs
exactly as it is. Hebrew you did not lift from the data is the thing to suspect. That includes
Hebrew an agent types, even when copying it from tool output: on 2026-10-14, all eight forms that
two Claude sessions typed with a dagesh, shin dot or sin dot beside a vowel came out in
Unicode-normal order. Build such text from the data by lookup, or pass it through
`give_std_mark_order`.

**Never "repair" the second kind, and know which clusters are the second kind.** A scan of every
tracked file on 2026-09-11, at review-branch commit `2bb94060`, counted **699,940** clusters in the
other order, a cluster counting when `give_std_mark_order` changes it. Two groups, 692,693
clusters between them, are known to be expected:

- **688,072 are the Wikisource download and three faithful intermediates of it**, 172,018 in each
  tree. `in/mam-ws/` is a download that is inherently normalized (Ben, 2026-09-09);
  `out/mam-ws-bot/proto/`, `out/mam-ws-bot/proto-fmt-2/` and `out/mam-ws-parsed-fmt-2/` are
  written from it, and their per-book counts match it exactly. The pipeline denormalizes
  downstream, which is why `MAM-parsed/` and `MAM-for-Sefaria/` come out clean.
- **4,621 are byte-verbatim captures of external sources**: `in/mam-ws-intro/`, `in/UXLC-39/`,
  `aleppo/aleppo-wiki/Wikisource-manual-*.txt`, `misc/zarqa-table-diff/`, `misc/*/img-sources/`.

A capture tracked after that scan belongs with the second group: `hbce-psalms/in/transcriptions/`,
HBCE's TEI transcriptions of Psalms, added 2026-09-26 with 126 clusters in the other order. The
TSV and `.txt` outputs under `hbce-psalms/out/` quote those forms in HBCE's order by design, 60
clusters on the same date; `hbce-psalms/README.md` describes both trees.

`doc/wikisource-dagesh-discussion-2026-10-01.mediawiki` is another capture tracked after that
scan: the exact UTF-8 section text that the MediaWiki revisions API returned on 2026-10-01 for a
Hebrew Wikisource Village Pump discussion, with 5 clusters in the other order. Its translation,
`doc/wikisource-dagesh-discussion-translation.md`, says not to reorder the capture's marks, and
gives its own Hebrew examples in MAM-normal order.

`in/mam-ws-special/`, the declared special pages that every Wikisource chapter download mirrors
byte for byte, was added 2026-09-27 with 5,369 clusters in the other order in 25 of its 36
`.mediawiki` files.

`Taamey-D/qa-in/`, the corpus of Taamey D's shaping checks, moved here from hbofonts on
2026-10-29 with 16 of its 556,525 clusters in the other order: 5 in five words from the UXLC's
word list, in `bible_words_21.testcases.json`, and 11 in six test cases quoting MAM's
documentation notes, in `mam_doc_notes.testcases.json`. A shaping test's input is its exact code
points, so by Ben's decision of 2026-10-28 the corpus keeps them, deliberately constructed
alternative orders included, and stays outside `py/check_mark_order.py`'s scope.

**The other 7,247 clusters, in 152 files, are unclassified.** Nobody has established, file by
file, whether each is a capture, an upstream intermediate, or a paste that should have been in
MAM-normal order. The largest shares are in `uxlc/in/` and `uxlc/out/` (3,890), `in/accgram/`
(1,431), `out/accgram/` (702), files under `py/` (656 in 65 files, 369 of those in 51 `.py`
files) and `gh-pages/` (334). So do not repair one of them, and do not cite one as expected,
without first finding out which it is. `py/repo_scopes.py` records why a repo-wide mark-order
sweep has no meaning here.

**The lint over hand-authored prose is `py/tests/test_prose_mark_order.py`** — every tracked `.md`,
the `.html` under `doc/`, and the `.txt` under `in/accgram/edition_transcriptions/`, the last by
Ben's decision of 2026-09-09, which the lint's docstring records. It was added 2026-09-09, when a
scan someone chose to run found 132 such clusters in 16 prose files that no existing check
covered. Source outside its scope is still yours to check: `py/check_mark_order.py` covers the
`.py` and the Ben-authored `.json` of the three repos `py/repo_scopes.py` names, and
`py/tests/test_mam_simple_mark_order.py` covers MAM-simple's non-corpus tree, but any other
`.txt` is covered by nothing, and
`py/tests/test_aleppo_page_mark_order.py` covers generated pages rather than source. Separately
`py/py_misc/uni_check.py` and `py/py_misc/check_mpplus.py` check data, and
`py/foi/foiz_wt_unicode.py` reports `NON_STANDARD_MARK_ORDER` as a feature of interest.

The frozen `doc/yod-holam-review-20261007.html` preserves the original historical
review's exact source and comparison readings at Ben's explicit request. Its bytes,
including original mark order, remain unchanged; the integration receipt records its
source commit, byte count and SHA-256. It is excluded by exact path from the authored
prose lint, rather than normalized or treated as current authored examples.

The Introduction/doc-note research also preserves original quotation order, as
`doc/intro-doc-audit/RUNBOOK.md` requires. Its generated `review.html` is excluded
by exact path; the review renderer validates the literal passages and proposals.
In the maintained Deuteronomy comparison, Jeremiah adjudication and Lamentations
proposal notes, only their named literal-quotation containers are exempt. Their
authored prose remains checked. Neither exception changes the preserved strings.

Scope: only those five code points have a declared priority. A vowel and an accent pass in either order, so
`has_std_mark_order` says nothing about which of them comes first.

**This section is back, not new.** It stood in `CLAUDE.md` and `.github/copilot-instructions.md`
until both were disabled on 2026-05-19 and deleted in `b1fa115` on 2026-08-03. When this section
was restored on 2026-08-04, `codex-index-aleppo` and `codex-index-cam1753` carried near-verbatim
copies of the deleted wording that pointed back at `uni_denorm.py` here; both repositories
replaced those copies with evacuation breadcrumbs on 2026-09-04. On 2026-08-04, one day after the
deletion, three NFC-ordered clusters were found in a hand-authored file here. That is why it is
worth the tokens.

## HarfBuzz hands a font a third order

HarfBuzz, the shaping engine that its `README.md` lists in Android, Chrome, Firefox and many
other systems, sorts the marks after each letter before a font sees them. It sorts by a
permutation of Unicode's combining classes for the Hebrew points, in `src/hb-unicode.hh`,
unchanged from HarfBuzz 0.9.1 (2012) through 15.0.0 (2026): shin dot, sin dot, dagesh or mapiq,
rafeh, ḥolam, the three ḥataf vowels, tsere, segol, pataḥ, qamats, sheva, ḥiriq, qubuts, meteg
and varika, then the accents in Unicode's order. Since 5.0.0 (2022), at Ben's request in
https://github.com/harfbuzz/harfbuzz/issues/2947, it also puts a meteg, or an accent of class
220 below the letter, before a sheva or ḥiriq that follows a pataḥ or qamats.

HarfBuzz orders shin dot, sin dot, dagesh and rafeh as MAM-normal order does, and from the same
source: Appendix B of the SBL Hebrew Font User Manual gives them the classes 10, 11, 21 and 23
that `_NS_COMB_CLASSES` uses (manual version 1.5, June 2007, pp. 21–22,
https://www.unicode.org/L2/L2019/19183-sbl-hebrew-man-v1-5.pdf). HarfBuzz 15.0.0 also sorts
dagesh ḥazaq (U+05C9) with the dagesh, since Unicode 18 gives it the dagesh's class. The order
of the vowels is not the manual's, which gives every below vowel, meteg and below accent one
class. Mozilla bug 662055 moved sheva and ḥiriq after pataḥ and qamats in 2012, so that the
Biblical spelling of Jerusalem would render without a CGJ, and judged the order of any other
pair of vowels immaterial because none was known to share a letter (comments 30, 38 and 39). So
HarfBuzz hands a font tsere before ḥiriq and before sheva even where Unicode normalization keeps
the stored order. That happened to the ketiv atoms of דנאל and מדנאל that the notes quote at
Ezekiel 14:14, 14:20 and 28:3, and to the combined atom in the note on 2 Kings 18:27, until the
bot run of 2026-10-28 put a CGJ between the two vowels of each (“Ketiv forms with two vowels on
one letter” in `py/ws/ws_bot_edit_history.md`). A CGJ between two vowels keeps their stored
order in HarfBuzz, as it does under normalization.

Since 2026-10-28, `is_fragile` in `py/mb_cmn/uni_norm_fragile.py` has checked a string against
both orders. After dropping the marks in its `_DROP_TABLE`, it calls the string fragile when
normalization to NFC or HarfBuzz's reordering would change the order of the marks below any
letter, or of the marks above it. A change that only moves a mark below a letter past a mark
above that letter does not count, because fonts position the marks below a letter independently
of the marks above it. Its `hb_mark_order` models HarfBuzz 15.0.0's reordering, and
`py/tests/test_uni_norm_fragile_harfbuzz.py` checks that model against HarfBuzz itself.

Fragility is therefore stricter than MAM-normal order, which lets a vowel and an accent pass in
either order (the scope note above). A vowel or meteg must come before an accent in the same
zone, below the letter or above it, since NFC and HarfBuzz both put it first, while a mark below
the letter and a mark above it may come in either order. And since NFC puts sheva and ḥiriq
before the other vowels and HarfBuzz puts them after, two vowels on one letter have no robust
order without a CGJ between them when one is sheva and the other is a ḥataf vowel, tsere,
segol, pataḥ, qamats or qamats qatan, or when one is ḥiriq and the other is tsere, segol, pataḥ,
qamats or qamats qatan.
