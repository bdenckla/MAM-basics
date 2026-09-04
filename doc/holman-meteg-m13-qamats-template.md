# Notes: 2 Chronicles 18:33 word 21 הׇֽחֳלֵֽיתִי׃ is inside a `מ:קמץ` template call

Evidence for the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md). Its finding is
what turns M13 into two entries of that programme's item 2 rather than one.

Captured 2026-09-03 in a plan-mode session of MAM-basics (`C:/Users/BenDe/GitRepos/MAM-basics`,
HEAD `3829585`, clean tree), one of a set of six notes written under
`C:/Users/BenDe/.claude/plans/` because concurrent work in git-tracked areas had not concluded.
All six were moved into `doc/` on 2026-09-03, which settles the "where they land" question the
closing section of this note leaves open.

## Finding: implementing suggestion M13 means removing the meteg from BOTH parameters of a `מ:קמץ` call — DONE 2026-09-03

**Status, 2026-09-04: M13 HAS BEEN IMPLEMENTED, and this heading said "not yet
done; no edit made" until now.** The Wikisource bot removed both metegs on
2026-09-03 as item 3 of
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md),
and item 5's Google Sheet round trip and mega run carried the change into
MAM-parsed and the generated repositories on 2026-09-04. **The finding below is
what made the two-parameter shape matter, and it held**: M13's two bot entries
are the two parameters of one call and so land in a single verse, which is why
the programme's 35 auto-edit rows touch 33 verses rather than 35. M13 is
archived as item 6 of that programme, its disposition in
`py/hkq_cmn/mam_suggestion_dispositions.py` keyed `2Ch 18:33.21`.

Suggestion M13 of `MAM-basics/gh-pages/holman/table_data_findings.html` (record `#mam013`,
kind "meteg", message dated 2026-08-31) concerns 2 Chronicles 18:33 atom 21 of 21,
הׇֽחֳלֵֽיתִי׃. Holman's note there reads "Aleppo has no Meteg under Hey", and the page's
comparison table gives MAM הׇֽחֳלֵֽיתִי׃ against Aleppo Codex הׇחֳלֵֽיתִי׃. So the suggestion is
to drop the meteg under the he from MAM's word.

**That word is not plain text in MAM's Wikisource source. It is the `ד` parameter of a
`מ:קמץ` template call**, and the same meteg is carried again in the `ס` parameter. The mirrored
wikitext for the verse, at `in/mam-ws/FD-2Chronicles.json` line 641 (searchable anchor:
`{{מ:פסוק|דברי הימים ב|יח|לג}}`), ends:

```
כִּ֥י {{מ:קמץ|ד=הׇֽחֳלֵֽיתִי|ס=הָֽחֳלֵֽיתִי}}׃
```

1. The `ד` parameter is הׇֽחֳלֵֽיתִי, with qamats qatan (U+05C7) under the he. That is the
   spelling the findings page shows as MAM's.
2. The `ס` parameter is הָֽחֳלֵֽיתִי, with plain qamats (U+05B8) under the he.
3. The sof pasuq is outside the template, immediately after the closing braces.
4. The meteg under the he (U+05BD) is present in **both** parameters, and the findings page
   shows only the `ד` form, so the page understates what the edit touches.

**To implement M13, the meteg under the he has to be removed from both the `ד` (dalet)
and the `ס` (samekh) parameter.** Removing it from `ד` alone would leave the Sephardic form
still carrying the meteg the Ashkenazic form had lost, so the two forms would then differ in
something other than the qamats, which is the only thing the template exists to vary. The
edited call would read:

```
כִּ֥י {{מ:קמץ|ד=הׇחֳלֵֽיתִי|ס=הָחֳלֵֽיתִי}}׃
```

The meteg under the lamed stays in both parameters; M13 says nothing about it and the
findings page's Aleppo reading keeps it.

**What the two parameters mean, per this repo's code**: `py/hkq_cmn/qere_projection.py` line 41
glosses `ד` as the Ashkenazic form, the one that distinguishes qamats gadol from qamats qatan,
and `ס` as the Sephardic form. `py/accgram/printed_decalogue_fetch.py` line 42 calls the `ד`
form the default display form. Every consumer in `py/foi/` resolves a `מ:קמץ` call to its `ד`
parameter (`wt_qere.hnd_recurse_on_param_dalet`).

**Path note, 2026-09-03:** the Holman review moved out of the separate `holman-ketiv-qere`
repo into `MAM-basics/holman/` (data) and `MAM-basics/gh-pages/holman/` (rendered pages)
during this session, in a concurrent session. That repo's clone is gone from `GitRepos`
entirely (not just emptied to a breadcrumb); `bdenckla/holman-ketiv-qere` on GitHub is now a
redirect host pointing at `bdenckla.github.io/MAM-basics/holman/`. Every path in these four
notes has been repointed accordingly; a citation elsewhere naming the old repo is stale.

**The same difference is mgketer's record `2C18:33#8e58aa4c`**, in
`../MAM-private/mgketer/out-reports/by-type/mam-adds-meteg.html` and
`by-book/FD-2Chronicles/diffs.html`, subcategory "MAM adds meteg on he". The card displays
the he with plain qamats because of mgketer's "qamats qatan → qamats" massaging step, not
because of any disagreement about the reading. The lineup of all 30 M records against those
reports is the sibling note [`holman-meteg-vs-mgketer.md`](holman-meteg-vs-mgketer.md); the M23
note is [`holman-meteg-m23-isaiah-23-12.md`](holman-meteg-m23-isaiah-23-12.md).

## The parallel verse, 1 Kings 22:34, has the same template, differing only by one meteg

`in/mam-ws/BC-1Kings.json` line 1132 (anchor `{{מ:פסוק|מלכים א|כב|לד}}`) ends:

```
כִּ֥י {{מ:קמץ|ד=הׇחֳלֵֽיתִי|ס=הָחֳלֵֽיתִי}}׃
```

The 1 Kings word has **no meteg under the he**; the 2 Chronicles word has one. Both verses
have the meteg under the lamed. Nothing else in the two template calls differs. (This is a
statement about MAM's Wikisource text, not about any manuscript. No manuscript was consulted.)

**After M13 is implemented, the two verses' template calls will be byte-identical.** The
edited 2 Chronicles call written out above is exactly the 1 Kings call as it stands. That is
a useful check on the edit: a diff of the two calls after the change should be empty.

## How to re-establish the finding

From the repo root, search the mirror for the shared stem (the lamed-onward part, which both
verses spell identically):

```
Grep pattern חֳלֵֽיתִי in C:/Users/BenDe/GitRepos/MAM-basics/in/mam-ws
```

Expected: exactly two hits, `BC-1Kings.json:1132` and `FD-2Chronicles.json:641`, both inside
`{{מ:קמץ|ד=…|ס=…}}`. A third hit, or either hit outside a template, is a finding. Line numbers
will drift if `in/mam-ws/` is refreshed (`py/main_download.py fr-wikisource`); the `מ:פסוק`
anchors above will not.

The `qamats_var` feature of interest (`py/foi/foiz_wt_qamats_var.py`, explanations in
`py/foi/qamats_var_explanations.py`) collects every `מ:קמץ` use in the corpus, so its rendered
output is the place to see both verses listed among their peers rather than in isolation.

## Open item for Ben: where these notes belong

**This HAS BEEN SETTLED, and the candidate list below is the record of the choice rather than
an open question.** Ben's decision, 2026-09-03: the third candidate. The six notes are `doc/`
files of MAM-basics, cross-linked to the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md),
which is where the implementation of the M-series suggestions is tracked — so the first and
third candidates were taken together rather than one instead of the other. No issue was filed
for M13, the second candidate.

The candidates as the session that wrote this note recorded them:

- wherever the implementation of the M-series suggestions from
  `MAM-basics/gh-pages/holman/table_data_findings.html` is being tracked, since the note is
  a caveat on how M13 in particular has to be carried out;
- an issue in MAM-basics (bare `#NN`), if M13 gets an issue of its own;
- a `doc/` file, if the note is context for other work rather than a question.
