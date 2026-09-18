# MAM-normal order for Hebrew marks

This current reference carries the detailed repository-specific evidence and scope. The always-loaded rule remains in `AGENTS.md`.

## Hebrew marks go in MAM-normal order, not Unicode-normal order — never run NFC over them

Two orders exist for the combining marks of one base-letter cluster, and they differ on where the
dagesh sits:

- **MAM-normal order**, the one this repo uses. Shin dot, sin dot, dagesh/mapiq, rafe, then every
  other mark in the relative order it already had. Spelled out and implemented in
  `py/mb_cmn/uni_denorm.py` — `give_std_mark_order` is the authority, `has_std_mark_order` the
  predicate. The code calls it "(our) standard mark order" and its combining-class table "SBL2",
  after the appendix to the SBL Hebrew Font manual, so grep for **std mark order** and **SBL2** as
  well as for this section's heading.
- **Unicode-normal order**, what `unicodedata.normalize` produces from the canonical combining
  classes (qamats 18, holam 19, dagesh 21, meteg 22). It puts the dagesh **after** the vowel.

**Never call `unicodedata.normalize` (NFC, NFD, any form) on Hebrew.** When two strings that should
match do not, put both through `give_std_mark_order`; do not paper over it by normalizing. The two
orders render identically, so nothing looks wrong on the page and the defect surfaces only where
something compares bytes.

MAM's shipped data is entirely in MAM-normal order — checked 2026-08-04, `has_std_mark_order` true
for all 87 files of `MAM-parsed/plus/`, `MAM-parsed/plain/` and `MAM-for-Sefaria/csv/`. So a cluster
in the other order is either hand-authored — and **the way in is a paste through anything that
normalizes, a browser above all** — or it sits upstream of the denormalizing step and belongs
exactly as it is. Hebrew you did not lift from the data is the thing to suspect.

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

Scope: only those four marks have a declared place. A vowel and an accent pass in either order, so
`has_std_mark_order` says nothing about which of them comes first.

**This section is back, not new.** It stood in `CLAUDE.md` and `.github/copilot-instructions.md`
until both were disabled on 2026-05-19 and deleted in `b1fa115` on 2026-08-03. When this section
was restored on 2026-08-04, `codex-index-aleppo` and `codex-index-cam1753` carried near-verbatim
copies of the deleted wording that pointed back at `uni_denorm.py` here; both repositories
replaced those copies with evacuation breadcrumbs on 2026-09-04. On 2026-08-04, one day after the
deletion, three NFC-ordered clusters were found in a hand-authored file here. That is why it is
worth the tokens.
