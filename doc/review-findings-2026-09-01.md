# Findings of the 2026-09-01 review of the public repos since 2026-08-26

State: acted on 2026-09-01

**This is the last review to file a tracking issue. The series is doc-only from here** — Ben's
decision, 2026-09-01: *"are the (thin?) github issues corresponding to doc/review-findings-*.md
serving any purpose? I'm not looking at them."* The seven issues the series filed (wlc-utils#87,
then MAM-basics #219, #228, #231, #232, #261, #263) carried nothing the doc beside them did not,
every comment on all seven was written by an agent from Ben's account, and only #219 was ever
adopted as a short citation handle — its five successors are cited from nowhere in any repo. The
open/closed state was the one thing an issue held that the doc did not, and the `State:` line
above is the replacement, the same line the plans got on 2026-08-29 (`4f3fed2`). **A review that
finds real work still files a real issue with a real body** — #233 is the shape, spun out of the
2026-08-22 review; what is retired is the thin pointer, not issue-filing. The reasoning is
recorded with the doc/ standard, in `py/repo_util/check_repo_standards.py`. #261 and #263 were
closed the same day with a comment saying so; the five already-closed issues were left alone.

Filed as [#263](https://github.com/bdenckla/MAM-basics/issues/263), which is a thin pointer to
this doc. Second review under the public-repos-only scope: it covered every public clone directly
under `~/GitRepos` — committed work from the 2026-08-26 review's anchors (MAM-basics `363fe41`,
codex-index-aleppo `1c12a8e`, codex-index-cam1753 `7309882`, codex-index-leningrad `2abd7f6`,
holman-ketiv-qere `94cab4a`, book-of-job `3f096b9`, UXLC-utils `b7b4eb9`; elsewhere the previous
review's start time, 2026-08-26T19:05 local) through 2026-09-01 ~10:30 local, when this review
started. That is **96 commits across 5 public repos with activity**: MAM-basics 84
(`363fe41..4cc0c33`; 76 non-merge + 8 merges; 78 authored Ben Denckla + 6 authored Claude, the
first Claude-authored commits in this repo), MAM-with-doc 7, MAM-simple 3, MAM-parsed 1,
book-of-job 1 — re-measurable per repo with `git log <anchor>..<head> --oneline`, or `git log
--since=2026-08-26T19:05 --oneline` where no anchor was recorded. Ten public clones were quiet:
the codex-index trio, UXLC-utils, holman-ketiv-qere, diffable-pointed-hebrew, MAM-for-Sefaria,
MAM-OSIS, phonetic-hbo, and Taamey_D — the roster's newest member, cloned 2026-08-31 08:56 (its
reflog's one `clone:` entry), added to `all-repos.code-workspace` and the visibility map by
`af77984` as hbofonts' public release target. Three clones are private and fall to the private
series: MAM-private (18 in-window commits), github-misc (9), hbofonts (9). The deliberate
exception again: this review verified github-misc's instruction-file plumbing — the tracked
`dot-claude/CLAUDE.md` (81,024 bytes) and both tracked skills (hebrew-prose, prune-claude-state;
six files) are **byte-identical** to the live `~/.claude/` copies, zero drift.

Anchors: HEADs at review start were MAM-basics `4cc0c33`, MAM-parsed `46209cd`, MAM-simple
`cd2bef8`, MAM-with-doc `999a437`, book-of-job `d09b966`, and the seven quiet repos' anchors
above. Every tree was clean with HEAD = origin/main, and no session was live in any public repo
(MAM-private's same-morning commits are Ben's, on the private side). The review ran in five agent
streams plus the main session: the b2→t451 sigil programme; the 2026-08-27 maintenance, guards
and the 2026-08-29 doc sweep; the 2026-08-31 roster and sync work; the gist evacuations and the
accent correction; and the document-index unification with the landing-page work. The series'
standing regeneration limitation was **partly lifted this time**: the landing page, the
unicode-proposals page, the MAM-simple doc-only targets and the spelling checker's two frequency
reports were all regenerated in place and came back **byte-identical**; the rest of the tracked
outputs had blob-level checks as before.

## Tree health: the suite grew 941 → 969 and every lint is clean

At `4cc0c33`: **969 passed, 5 skipped, 65 subtests** (`.venv/Scripts/python.exe py/main_test.py
-q`, 150s), collect-only 974 = 969 + 5; `ruff check py` clean; `black --check py` clean at 1,147
files; `git ls-files` = 2,305; zero `sys.path` mutations in tracked source; the
`--check-repo-standards` sweep over all 15 public workspace repos reports no new problem (its
NFC and hex-escape rows are all pre-existing data-file or legacy-source sites, the Sheet's five
decomposed template-documentation lines among them, expected since `bf8886a`). The suite chain
from the previous review's 941, each step attributed: +10 (`6cb65ef`,
`test_repo_visibility_declared.py`) = 951 at `87d37b7`; +15 (`52aa7b8`, the 13 ws-bot payload
tests and the 2-test b2 lint) = 966, of which the b2 lint was **deliberately red from `52aa7b8`
(11:18) to `8fe3dff` (12:58) as the plan's completion criterion** — a designed red, unlike the
accidental one the previous review found; 966 green at `8fe3dff`; +1 (`b4a1211`) = 967; +2
(`616f140`, `test_site_index_links.py`) = 969. The 6 new subtests are the payload test's loop
over the six Daniel chapters. After this review's fixes the suite was re-run and is green at the
same figures.

## The b2→t451 sigil programme of 2026-08-27 verifies end to end

MAM's sigils ב2 and ת451 name one Yemenite Ketuvim manuscript; the replacement Avi Kadish asked
for on 2026-04-10 (#259, #260) ran as a seven-phase plan (`doc/PLAN-replace-sigil-b2-with-t451.md`,
deleted as spent by the 2026-08-29 sweep, in history at `f6173fe^`). Re-derived: the pre-edit
`in/mam-ws/F1-Daniel.json` blob holds exactly 32 sigil-shaped ב2 (chapters 7–12: 17, 2, 3, 3, 6,
1; all comma-preceded, none digit-followed), and `replace(old blob) == new blob` byte-for-byte at
both rehearsal artifacts — the diffs hold the 32 replacements and nothing else. The live
Wikisource edit (`a31d0ec`, six `/טעמים` pages of Daniel, bot BDencklaBot, edit summary citing
MAM-basics#260) verifies from the re-downloaded book JSON (ת451 now at 37 = 5 + 32, ב2 at 0), from
one live diff link, and independently from the 2026-08-31 `in/mam-ws-intro/appendices.mediawiki`
mirror (zero ב2, two ת451). The Sheet round trip (`8fe3dff`) took `out/diff_mamws_mamgo-auto-edits.json`
through exactly 32 entries (`1aa95ff`, every `replace_str` the mechanical substitution) back to
`[]` at HEAD. Scripted scans of all six data repos find **zero sigil-shaped ב2 anywhere**: the
432 `|ב2=` aliyah parameters of the two `in/` trees, the 648 of `out/` (216 × 3 Torah
serializations, confirming the plan's correction of its "648" baseline), and MAM-parsed's
`"ב2"` JSON keys are all the parameter, not the sigil; MAM-simple, MAM-OSIS and MAM-for-Sefaria
have zero ב2 and zero ת451. MAM-parsed `46209cd` and MAM-with-doc `c4dd986` are confined to
Daniel with matching counts; `80f4a3f`'s rendered sigil-page row reads as recorded. The lint
`test_sigil_b2_not_a_sigil_anywhere.py` (2 tests, ≥216-parameter floor so an empty scan cannot
pass) is green; `e37b8ad`'s inventory rewiring claims verify including "stale since April"
(`out/sigil-inventory.json` has exactly three commits: 2026-04-07, `e37b8ad`, `8fe3dff`).
`doc/sigil-decoding.md`'s re-measured figures re-derive **exactly** against MAM-parsed `46209cd`:
the מסורת row (ל 140, א 30, ש1 8, ד 6, ש 2, ק 2, מ"ג 1, ק-מ 1), the מסורות row (א 78, ל 78,
ש1 6, ק 2, ק-מ 2, ב 1, ש 1, ד 1), all eleven ד sites in their claimed files, `93ee8e6`'s five
moved inventory figures, the ט3 references, and the vav ranking (sixth: א 1378, ל 1148, ש1 1023,
ק3 706, ש 704, ו 589). `4cb3f20`'s UTF-8 reconfigure is the first statement of `main_ws_bot.py`'s
`main()`. On the trackers: #260 was closed 2026-08-27 11:19 by bdenckla **with no comment near the
event** — the worked case behind the user-level "Never change an issue's state without a comment"
rule, confirmed — and the 15:20 comment four hours later carries the six diff links oldid-for-oldid;
#262's thread says exactly what `c691af8` acts on, and the worked-examples comment opens by
marking Claude authorship, as Ben directed.

## The rest of the window verifies sound, stream by stream

**The 2026-08-27 morning follow-up and maintenance.** `97b559b`'s tracker-consolidation record
matches today's remote state (all five emptied source trackers hold 0 open; closed counts exactly
as CLAUDE.md says); the six `MAM-with-doc#6` sites read #257; `5da49fd`'s distributed qualifier
rows re-derive cell-for-cell, direct-only reproducing the old cells first; `d7df398`'s eleven
"On:" runways are all present. The visibility guard (`6cb65ef`) does what its records claim
(refuses a private-covering report into a public tracked tree; the map ↔ workspace sets are equal,
18 = 18), `b89fe68`/`b4a1211` resolve repo NAMES so worktrees stop mislabeling, and `0314c6e`
moved the plain MAM-parsed reader's sibling resolution to call time with exactly one caller and
the vendored-copy exception intact. MAM-simple's vendored `provenance.py` is byte-identical to
the source again (blob `1d659d3`, re-vendored by MAM-simple `59b0776` after the `b4a1211` split
left it four days stale — a window the design accepts, since the content compare runs only in the
vendoring compare and the mega; but see finding 5).

**The 2026-08-29 doc sweep.** All six surviving `doc/PLAN-*.md` carry a line-3 `State:` (executed
×2, paused, pointer, live, runbook); the seven deleted plans each carried `State: executed` with
the recorded dates; the two kept plans are cited 9 and 6 times by the paused three-repos plan;
the runbook's step 6 census (MAM-basics 6, MAM-private 4) is right now, at both recorded moments,
and across the 2026-08-31 add-then-delete of the document-index plan.

**The 2026-08-31 roster and sync day.** The three origin/main merges (and hbofonts' two, the same
hour) show empty combined diffs — two machines racing pushes, cleanly auto-merged, nothing
dropped. The fr-ws-intro mirror: 13 files + manifest matching CLAUDE.md's table; two pages
fetched at their recorded revids are **byte-identical** to the mirror; no BOM, no CRLF, sizes
equal the manifest's; nothing downstream parses it. `d9b6021`'s three requirement declarations
match imports exactly (numpy 5 files, pygments 3, pyspellchecker 1) and the venv has all three.
All six frozen repos are archived on GitHub; `FrozenRepos` is absent; issue #211 is open and says
what the location_comment cites it for; the 30 → 24 workspace history re-derives. The 27-clone
arithmetic of the roster rule re-derives from today's remote state, and today's `GitRepos` holds
**exactly the 18 roster folders and nothing else** (`-Force` shows nothing extra) — the
extras-are-residue era is fully cleaned on this machine. The gists: each holds exactly its stub,
pointing at the right rendered page and source module; Gist-ArtScroll's `.gitattributes` left at
its `95c8039`, as the gists key records. Taamey_D's entry is accurate down to the release
script's three wiped destinations and the reduced `sources/` set; `bdenckla.github.io/Taamey_D/`
answers 200.

**The gist evacuations and the accent correction.** The two authored pages
(`py/author_misc/review_of_hebrew_worlds_phonetic_bible.py`,
`review_of_artscroll_transliterated_linear_siddur.py`) match the author_misc idiom, pass black,
have no orphan combining marks and no decomposed Latin, and their rendered pages exist in
MAM-with-doc with the eleven screenshots referenced one-to-one (two of the eleven re-fetched from
the gist CDN today, byte-identical). **The accent correction `43a07d5` is right against both data
sources**: in Exodus 20:1 the fourth chanted word, the maqaf compound כׇּל־הַדְּבָרִ֥ים, has
merkha (U+05A5, on its second atom), and the next chanted word הָאֵ֖לֶּה has tipeha (U+0596) —
MAM-parsed plus and `in/mam-ws` agree atom for atom, and four further accent claims on the pages
spot-verify, including the meteg/silluq treatment, which applies the verse-final rule exactly.
`e55b6dc`'s mid-dot (U+00B7, count 10 → 11 in the rendered page) and mark-order repair verify
byte-level against the pre-stub gist; all rendered-page Hebrew now passes `has_std_mark_order`,
with the new `_hbo_checked` assertion guarding generation (but see finding 6 for the docstring it
cannot see). The stylesheet fix is blob-identical (`f7cc6a7`) in source and deploy, and its
scoping account (twelve pointed Hebrew-bearing h2 headings, all on the ArtScroll page)
re-derives. Both pages' prose keeps Ben's gist wording verbatim by charter; the romanized
*taḥton*/*ʿelyon* and the inline 17-item list are the source's, recorded here as adjudicated
source-faithful rather than as defects.

**The document-index unification, the landing page, and the MAM-simple index.** The "two
identical merges" (`3658798`, `1af10e4`) carry the same tree with the same parents in opposite
order; `34a8eec`'s reconciliation diff against `3e582cc` is empty and no commit is unreachable —
nothing lost (but see finding 8 on the message's chronology). The two moved documents are
generated pages (`gh-pages/index.html`, `gh-pages/unicode-proposals.html`, via
`py/main_authored.py gen-site`, also a mega step); regeneration is byte-identical; `2f81ecb`'s
link accounting re-derives exactly (25 + 14 source links all mapped, the 7 extra hrefs each
deliberate); every one of the 15 remaining `document-index` mentions is a deliberate historical
record and zero live citations survive. document-index itself is **archived**, PUBLIC, its README
the prescribed stub, its one issue closed; `c0b3195`'s de-listing is exactly its claimed 6 lines
(roster and visibility map both 18, equal in both directions). The landing-page sequence
verifies at the artifact level, and a crawl from `gh-pages/index.html` confirms the claims figure
for figure: **155 of 156 tracked gh-pages pages reachable, the one unreachable page being
`wlc/index.html`** — precisely the strandedness `6d5671c` records as settled — and the two Misc
entries are exactly the pages with no other inbound link. Today's HTML sanity run (202 issues,
orphan line exactly `wlc\index.html`) closes the arithmetic from `2f81ecb`'s 203 with no
unexplained movement. The spelling-dictionary story closes end to end ("readme" gone from
dictionary and corpus, checker exit 0, both frequency reports regenerate byte-identical, and
book-of-job `d09b966`'s three-file diff is exactly the predicted repoint). MAM-simple: the
gh-pages index and README link are as recorded, and `4cc0c33`'s "all twelve GitRepos folders with
a gh-pages/ dir now have a top-level index.html" re-derives exactly.

## Findings

In rough order of consequence. Findings 2–4, 6, 7 and parts of 9 were fixed in the commit that
lands this doc; findings 1 and 5 are Ben's; the rest are immutable-message records.

1. **Three finished cloud commits sit unmerged on `origin/claude/main-mega-cloud-test-859r4h`,
   nothing records their disposition, and the defect one of them fixes is live on main.** The
   branch (based at `67116e9`, pushed 2026-08-31 14:32 local by a cloud session, the first cloud
   run of the mega) holds `205c64a` (OSIS validation silently depended on fetching `xml.xsd` from
   w3.org — undeclared network dependency, vendored and resolved locally), `b403e6d` (diff-mpp
   treated an unresolvable git revision as an empty release, so a shallow clone yields falsified
   "0 changes" change-log reports — five were written into MAM-with-doc's working tree during
   that cloud run before an unrelated failure stopped it; the fix raises with a deepening hint),
   and `86c87d2` (four machine-absolute `C:\Users\BenDe\...` paths in
   `out/accgram/research-oddballs.json` — still there at `4cc0c33`, lines 5–8 — replaced by
   repo-qualified paths via a new `paths.display_path`, plus a standing lint
   `test_no_machine_paths_in_artifacts.py`). All three carry full trailers and read as work Ben
   would want; the same day's other cloud branch (docs-unification) was merged by Ben, and no
   commit, doc, or issue mentions this one — it reads as forgotten rather than rejected. Nothing
   on main supersedes any of the three (main has no `display_path`, no vendored `in/xml.xsd`, no
   such lint). Ben's decision: merge (`git -C C:\Users\BenDe\GitRepos\MAM-basics merge
   origin/claude/main-mega-cloud-test-859r4h`, then regenerate/verify and push) or reject with a
   recorded reason; either way the remote branch then wants deleting, which is also his call.

2. **The al-hatorah register entry "corrected" two figures that were right, and the correction
   inverted them.** `03739c6`'s text said the stash's base "is 273 lines, not 315" and the stash's
   version "was 292 lines, not 334", citing the blob sha `3734afc5...` as its evidence — but that
   very blob (fetched at ref `40fe97b4` and counted, twice independently, during this review)
   holds **315** newline-terminated lines, so the original save note's 315 and 334 stood and the
   "correction" was the error. Its third correction survives with its count adjusted: `cb-qamats`
   appears in **ten** modules under al-hatorah/py/, not nine. Fixed in
   `in/repo_maintenance_policy.json` with dated text; the same entry's neighbor got its off-by-one
   fixed too (trope's closed issues were already 383 on 2026-08-31, not 382, the newest closure
   dating 2026-08-26).

3. **The fr-ws-intro mirror's two headline figures described a superseded fetch, contradicted by
   the manifest committed beside them — and by `d061fad`'s message itself.** The downloader
   docstring said 1,852,439 bytes where the committed manifest sums to **1,852,837** (the figure
   the commit message verified), and the docstring and CLAUDE.md both said "four of the thirteen
   pages were edited in August 2026" where the manifest records **five** — the drafting-time
   fetch predated upstream edits of 2026-08-30 and -31 to ch4 and the appendices (the 398-byte
   gap decomposes exactly into those two edits). Both sites fixed with dated text.

4. **`gitrepos_setup_rule`'s folder count went stale the same evening the rule was written, with
   no note.** Clauses 1 and 5 said 19 (and 20 earlier that day) while `c0b3195` (2026-08-31
   16:35) took the roster to **18** by de-listing document-index — and though that commit edited
   this very JSON, and four later commits edited it again, none touched the counts, so the
   reproducible clone rule disagreed with the roster it defines. Fixed with dated notes in both
   clauses. Related, immutable: `c0b3195`'s message attributes the quotation "the only thing that
   actually keeps a repo off this disk" to the policy file's location_comment; the phrase was
   never in that file — it sat in CLAUDE.md and in the document-index plan, and both sites were
   rewritten or deleted within nine minutes of the commit. Also fixed with dated text, smaller:
   the gists key's "HELD ONLY GIST-HEBREW-WORLD UNTIL 2026-08-31" implied a longer-standing
   arrangement than the three hours of its first day that it actually describes.

5. **The second vendored `provenance.py` destination is still stale, and the tracked compare
   artifact still calls it identical.** MAM-private's copy (at the al-hatorah tree path the
   public vendoring inventory names) has the pre-`b4a1211` content, five days behind its source,
   while `out/vendoring_compare_out.txt` — last regenerated 2026-08-25 — still reads "identical
   2026-08-11" for that row. The next `py/main_vendoring.py --compare` or mega run will flag it;
   until one runs, nothing will. Left to Ben (or the private series): MAM-private was active this
   morning, so this review wrote nothing there.

6. **The Hebrew World module's docstring held three clusters in Unicode-normal mark order at
   HEAD — the defect class `e55b6dc` repaired in the same file's literals, surviving one screen
   above the repair.** In the docstring's כׇּל־הַדְּבָרִ֥ים the kaf and dalet clusters had the
   dagesh after the vowel, and in its הָאֵ֖לֶּה the lamed cluster did; `_hbo_checked` guards only
   the rendered literals and no test reads docstrings, so the porting session's normalizing paste
   survived exactly where the guard cannot see. Fixed in the commit landing this doc by applying
   `give_std_mark_order` to the docstring (6 character positions moved; rendered output
   unaffected, since docstrings do not render; every string constant in the file now passes
   `has_std_mark_order`). The companion mislabel in the ArtScroll module's docstring is fixed
   too: the gist's five wrong clusters were called "Unicode-normal mark order", which fits only
   the dagesh-less cluster of u-vin'cho — in the clusters of had'vorim and t'muna the gist had
   the dagesh first, an order that is neither Unicode-normal nor MAM-normal (so those clusters
   cannot have come from a normalizing paste, unlike the Hebrew World case). The operative fact,
   the rafe after the sheva, was right throughout.

7. **Three smaller record errors, fixed with dated text in the commit landing this doc.** The
   maintenance runbook said mgketer was "archived on GitHub on 2026-08-10"; GraphQL `archivedAt`
   is 2026-08-27T00:28:51Z (= 2026-08-26 20:28 EDT, the evening of the previous review) — the
   private-evacuation date had stood in for the archive date, in the runbook and in `e563041`'s
   immutable message. `doc/sigil-decoding.md`'s stated rule for its 151 documented-token figure
   omitted one arm — the combined strip (prefix letter *and* trailing `?`), which decides exactly
   one token, `(א?` — so the rule as written yields 150; the rule sentence now names the arm. The
   same doc's "129 of the 139 on ל" kept its old denominator when the לד correction took the
   row's total to 140; now 140. And `py/author_site/site_index.py`'s strandedness paragraph
   claimed `wlc/index.html` "lists exactly the seven pages `_WLC` already names" — true for three
   hours, until the same evening's Misc trim cut `_WLC` to four of the seven; the paragraph now
   records the trim and rests the unchanged conclusion on the measured reachability of the other
   three. `DATA-LICENSES.md`'s landing-page row likewise still described the manifest section
   that was deleted 36 minutes after the row was written; now dated.

8. **Immutable-message figure and phrasing slips, the window's full census, recorded only.**
   (a) `e37b8ad` attributes the inventory header-string change to `d205dbb` on 2026-05-21; it was
   `cd73a0a` on 2026-05-08 (`git log -S` settles it), so the artifact was ~3.7 months stale on
   that string, slightly more than claimed. (b) `34a8eec` narrates Ben's merge as "a few minutes
   later" than the cloud's; the timestamps run the other way (20:25:35 vs 20:28:33 UTC) — what
   came later was Ben's rejected push, and the plan's Phase 4 record has the sequence right.
   (c) `f6173fe`'s "83 prose citations name the seven by filename" does not reproduce under any
   plausible aggregation (measured 96 citing lines / 101 occurrences / 75 file-name pairs at that
   commit); the claim's direction is right, the figure is not re-derivable. (d) `4f3fed2`'s
   "cited from 31 modules" measures 32 at its parent and 33 at itself. (e) `266f63f`'s "twelve
   plan files including the seven f6173fe deleted" is twelve including six of the seven — the
   leftover worktree predated the b2 plan, so no tree ever held twelve including all seven.
   (f) `52aa7b8` contains a genuine "the latter" — the window's one banned-construction instance
   (the plan's parallel sentence names both sides). (g) `cd2bef8`'s "The README gains a link to
   that page" leaves its antecedent two sentences back, and the natural reading (the site root)
   is not the link added (versification-and-cantillation.html). (h) `e55b6dc`'s census of the
   source's h-dot-below spelling ("decomposed twice and precomposed once") fits one word, not the
   source, which has 3 decomposed and 6 precomposed sites. (i) `e563041`'s "four sites" for
   `sibling_repo("UXLC-utils")` is two call sites (four consuming modules). (j) `241ebcc`'s
   whole story — a clone that "returned" and "will again" — was superseded within four hours by
   the reflog reading `0d36560` records (one `clone:` entry, 2024-02-20, so the sweep pulled a
   survivor rather than re-cloning); the tree documents its correction, the message stays as the
   superseded account, and its 95.6 MB disagrees unresolvably with the section's 97.4 (the clone
   is deleted). (k) `93812e1` and the b2 plan quote "witness" only to report the two pre-existing
   MAM-with-doc sigil-page rows that have it — quotations, not violations; those two rows still
   have it.

9. **Trailer hygiene inverted from last window's finding: one commit of 96 lacks the trailer.**
   `87d37b7` (the b2 plan-tracking commit) is the only non-merge in-window commit without
   `Co-Authored-By`, against eleven last window; every other commit across all five active repos
   carries one, the six cloud commits adding a `Claude-Session:` trailer and Claude authorship —
   self-identifying at the author level for the first time in this repo. Branch-ref hygiene is
   the flip side: besides finding 1's live branch, the merged-and-stale refs
   `origin/claude/docs-unification-plan-ip01h5`, `origin/copilot/fix-issue-127` (2026-05), the
   local copy of the docs-unification branch, three May-era local `feat/`/`feature/` branches in
   MAM-basics, and one merged `feature/provenance-sidecar-booklists-underscore` each in
   MAM-for-Sefaria and MAM-simple all linger; deleting any of them is Ben's call under the
   ask-before-branch-deletion rule (`git branch -d` and `git push origin --delete` would refuse
   nothing that matters — every one is fully merged).

## How the review was acted on (2026-09-01, during the review)

Findings 2–4, 6 and 7 (and finding 4's gists sentence) were fixed in the commit that lands this
doc: dated corrections in `in/repo_maintenance_policy.json`, `CLAUDE.md`,
`doc/PLAN-repo-maintenance-across-GitRepos.md`, `doc/sigil-decoding.md`, `DATA-LICENSES.md`,
`py/subcommands/download_wikisource_intro.py` and `py/author_site/site_index.py`, plus the
mark-order repair in `py/author_misc/review_of_hebrew_worlds_phonetic_bible.py` and the label
correction in `py/author_misc/review_of_artscroll_transliterated_linear_siddur.py`. black is
clean over the four touched Python files; `py/main_authored.py gen-site` still regenerates both
site pages byte-identically (the docstring edits reach no output); the full suite was re-run
after the fixes and is green at 969 / 5 / 65. Findings 1 and 5 are Ben's: the stranded cloud
branch wants a merge-or-reject decision, and the MAM-private vendored copy belongs to the
private series. Findings 8 and 9 are recorded only.

**Finding 1 was acted on 2026-09-01, hours after this doc landed.** Ben unarchived the cloud
session that had cut the branch and had it complete its work: it merged
`origin/claude/main-mega-cloud-test-859r4h` into main as `81fac84` (12:33 EDT, Claude-authored
with full trailers). The merge message records that main had moved 45 commits since the branch
was cut (exact: `git rev-list --count 67116e9..251b287` = 45), that of the branch's eight files
main had touched only `DATA-LICENSES.md` — where the branch adds the `in/xml.xsd` row — and that
the suite-and-mega verification of the combined tree was deferred to another session by Ben's
instruction. This session did the suite half the same afternoon: **971 passed, 5 skipped, 65
subtests** — 969 + 2, the 2 being `test_no_machine_paths_in_artifacts.py`'s — with ruff clean and
black clean at 1,148 files. The four machine-absolute paths are gone from
`out/accgram/research-oddballs.json`, `in/xml.xsd` is tracked, and the new lint is green over
`out/` and `gh-pages/` with its one named exclusion. **The mega against the combined tree has not
been run and is the open half of that deferred verification.** The remote branch stood at
`86c87d2`, fully merged, until later that same day, when Ben had the stale refs cleaned up —
that branch and finding 9's whole list: the three MAM-basics remote branches
(`claude/main-mega-cloud-test-859r4h`, `claude/docs-unification-plan-ip01h5`, and
`copilot/fix-issue-127`, whose one attached PR, #129, was already MERGED, so nothing was
closed), the four merged local branches here, and the merged
`feature/provenance-sidecar-booklists-underscore` in MAM-for-Sefaria and in MAM-simple. Every
tip was verified an ancestor of its repo's main first, every local deletion was accepted by
plain `branch -d`, and a fresh sweep of all 18 clones reports only main, locally and on origin.

**The mega half was discharged later that same day, in the worktree forest's first use, and the
State line above lost its "except" clause with it.** The forest — worktrees at
`C:\Users\BenDe\Forests\review-2026-09-01\`, one per repo the mega or the suite resolves, each on
branch `forest/review-2026-09-01`, every command run with the primary clone's venv by absolute
path — was commissioned by Ben for this run. Built with ten members, it taught its first lesson
before the mega started: membership had been derived from what the suite *collects*, and
`test_h_dot_below_nfc.py` resolves four more siblings at *run* time — book-of-job and the three
codex-index repos — so those joined as worktrees eleven through fourteen, and the baseline then
reproduced the suite half exactly (971 passed, 5 skipped, 65 subtests). `py/main_0_mega.py` then
ran end to end, exit 0, the near-aleppo census 90 of 90 with Ben's same-day ktiv/qere census
scripts included. The diff surface across all fourteen worktrees, read file by file, decomposed
into three real diffs and two kinds of machine-skew noise. The three real diffs, each committed
with its cause: (1) the vendoring artifacts' three row moves — finding 5's re-vendor date
2026-09-01, MAM-simple `59b0776`'s 2026-08-31 date arriving, and diffable-pointed-hebrew's
`cantsys.py` cell going eol-only → identical, the old cell having been measured against a working
copy still CRLF on disk from before that repo's LF normalization (all four on-disk copies hash to
the committed LF blob today); (2) MAM-simple's vendored `osis_runner.py` taking `205c64a`'s
offline-xml.xsd change — the one content ripple of `81fac84`'s merge, and the kind of diff this
mega existed to absorb; (3) MAM-with-doc's `unpinned-latest.html` end date moving to `46209cd`'s
day, its "0 changes found" remaining truthful because the sigil replacement rewrote doc notes,
not body text. The two kinds of noise, read and then restored rather than committed: (1) fifteen
CRLF phantoms — generators that write without `newline=""` met the forest's fresh LF checkout,
and `git diff` shows zero content hunks in every one; (2) MAM-parsed's twelve call-graph SVGs,
which this machine's graphviz 14.1.2 lays out differently than the committed 15.1.1 renders
(`0128e69`) — an SVG diff from this machine is renderer skew until its graphviz is upgraded.
(That upgrade happened later on 2026-09-01: winget took this machine from 14.1.2 to 16.0.0
(20260814.1018), and MAM-parsed `b9c8a77` is the one-time re-render under 16.0.0, verified
layout-only — node and edge identities, labels, tooltips, colors and fonts all unchanged. The
skew now runs the other way: any machine still on an older graphviz, the 15.1.1 machine that
rendered `0128e69`'s SVGs included, will see layout-only SVG diffs until it upgrades. `dot` is
still not on this machine's PATH in shells predating the install; the renderer is found via
`survey_dot.py`'s `_DOT_FALLBACK`, `C:\Program Files\Graphviz\bin\dot.exe`, which is where
16.0.0 landed.)
**Byte-identical everywhere else**, including `out/accgram/research-oddballs.json` — this run is
the Windows half of the cross-machine proof of `86c87d2`'s display_path fix, the 2026-08-31 cloud
run having been the Linux half — plus `out/sigil-inventory.json`, the MAM-simple / MAM-OSIS /
MAM-for-Sefaria corpus trees, and every near-aleppo golden. Ben answered the session's four
decisions live: (1) **no** to folding the Wikisource corpus refresh into this run, so Avi
Kadish's 2026-08-27 edits remain the next refresh's known-cause diff and that refresh will want a
mega of its own; (2) **yes** to aligning `misc/requirements-venv-setup-windows.ps1`'s body to the
repo-root `.venv` (`5f3d7f4`); (3) **delete** `out/accgram/goerwitz-stderr/_summary.stderr.json`
and its lint carve-out (`4386f4a`); (4) the Taamey_D exclusion **belongs in
`in/vendoring_policy.json`**, which gained a `foreign_vendored` section for copies whose source
repo is not MAM-basics (`1761d5c`). Alongside, the two qere-search modules stopped resolving
holman-ketiv-qere at import time (`297f7e5`, in `0314c6e`'s shape; the suite now collects all 976
tests with that sibling pointed at nothing). Closing state: 971 / 5 / 65 again over the finished
work, ruff clean, black clean at 1,148 files; all fourteen forest branches merged into their
primaries' mains and pushed — MAM-private's merge met three newer same-day commits of Ben's and
produced a true merge commit (`dc08041`), after which the census's own diff mode still reports
90 of 90 matched. One process note, since this series audits its own history: three MAM-basics
commits were re-cut before any push when an already-staged deletion rode into the venv-script
commit — the never-pushed originals were soft-reset and recommitted with the same messages and
content, nothing lost.

## Open ends the window itself declares (not findings)

Avi Kadish's same-evening Wikisource edits (Genesis 43:28 rewritten twice, adjustments at two
further sites, one corrected large-letter note) postdate the window's last download, so the next
fr-wikisource/fr-google refresh will move `in/mam-ws`, the wsgo outputs and eventually the
qualifier-table counts — a known-cause future diff. Taamey_D's six tracked `.py` are stale copies
of hbofonts build scripts that black would reformat, now sweep-reachable; where the exclusion
belongs is Ben's open decision (`af77984` records it). `misc/requirements-venv-setup-windows.ps1`'s
body still creates `venv` and says to run from `py/`, against every other doc's repo-root
`.venv` — hbofonts did its rename the same day; whether this file follows is Ben's.
`out/mam-ws-bot/proto-misc/warnings.json` keeps its six "sigil-replaced" records as a stable
fossil of the one-shot era, and `out/accgram/goerwitz-stderr/_summary.stderr.json` names the
departed wlc-utils clone (nothing writes it any more; `86c87d2`'s unmerged lint excludes it by
name — its disposition rides on finding 1). MAM-with-doc's `misc/index.html` is linked from
nothing, which `1b040d7`'s two-page Misc calculus leans on ("it rescues neither"); if it ever
gets linked, that calculus changes silently. The visibility lint enforces workspace ⊆ map only;
the reverse direction is currently true but unenforced. skadish1's 2026-08-19 question on #185 is
still unanswered in-thread, still Ben's to post — and his 2026-08-27 answers on #176, #182, #183
and #262 (worked examples answered; the readings inconsistent site by site) may likewise want
Ben's follow-through. The three-repos evacuation stays PAUSED after Phase 0; the scan-pages
undertaking is parked at Phase 0 for a fifth quiet window; the hcanat.us /Notes/ template
question is unanswered as long. MAM-basics #225, #226, #227, #229 and #230 are open and untouched
in-window, and the transferred #234–#260's bodies remain un-claim-checked. The Sheet's decomposed
h-with-dot-below arrived again with `d0328d5`'s successor downloads and is harmless under
`bf8886a`'s exclusion, exactly as the previous review said it would be.
