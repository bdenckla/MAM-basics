# CLAUDE.md

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
in the other order is always something hand-authored, and **the way in is a paste through anything
that normalizes, a browser above all**. Hebrew you did not lift from the data is the thing to
suspect. There is no lint over hand-authored source here — `py/py_misc/uni_check.py` and
`py/py_misc/check_mpplus.py` check data, and `py/foi/foiz_wt_unicode.py` reports
`NON_STANDARD_MARK_ORDER` as a feature of interest — so the check is yours to run.

Scope: only those four marks have a declared place. A vowel and an accent pass in either order, so
`has_std_mark_order` says nothing about which of them comes first.

**This section is back, not new.** It stood in `CLAUDE.md` and `.github/copilot-instructions.md`
until both were disabled on 2026-05-19 and deleted in `b1fa115` on 2026-08-03. `codex-index-aleppo`
and `codex-index-cam1753` carry near-verbatim copies of the deleted wording, both pointing back at
`uni_denorm.py` in this repo — so the rule survived everywhere except the repo that hosts its
implementation. On 2026-08-04, one day after the deletion, three NFC-ordered clusters were found in
a hand-authored file here. That is why it is worth the tokens.

## Invoke the `hebrew-prose` skill before writing or editing prose about accentuation

That user-level skill (`~/.claude/skills/hebrew-prose/`, tracked in `github-misc` at
`dot-claude/skills/`) is the canonical, single home for the rules the sections below and
`printed_decalogue_strands.py`'s docstring state — atom vs chanted word, the one-scale maqaf rule,
which corpus a claim takes, the banned verbs and framings, where Yeivin and Breuer live, how to
verify a page's numbers. It loads on demand rather than every session, so it can hold the full
statement; the sections here stay as pointers, and **a rule change goes into the skill first**.

## Rendered-prose conventions: `py/accgram/printed_decalogue_strands.py`'s module docstring

That docstring is where the editorial conventions for accgram's **rendered prose** are recorded
— strand names in Hebrew letters and never transliterated, the two signal-word sets, atom vs
chanted word, the single-sourced `ROM_*` romanizations and their italic wrapper, "the Simanim
Tiqqun" and never a bare "Simanim", real em dashes, no English sentence opening on a Hebrew word.
It lives in the printed-Decalogue trio because that is where each rule was settled, but the rules
are not all trio-specific — its SCOPE paragraph says which are which: read it before writing or
editing prose on **any** accgram page. Nothing referenced it for a long time, so it was
discoverable only by already editing the file it governs.

**A table cell holding Hebrew is declared `dir="rtl"`.** Every such cell of every table on a page,
unless the whole table already is, and without waiting to be asked — right-justification then
follows from having said what the cell holds, which is why the declaration beats a literal
`text-align`. Blank cells in the column included; the English heading left alone; no class and no
stylesheet rule. `maqaf_nonfinal_accents_page`'s `_HEBREW_CELL`, spliced through each table's one
`*_CELL_ATTRS` tuple, is the pattern. This is here as well as in the skill because Ben has had to
say it repeatedly (2026-07-29: "something I find myself telling you about frequently … this should
just be sort of obvious"), and `CLAUDE.md` loads whether or not the skill fires. The fuller
statement, with the companion rule about abbreviating a long accent name in a cell, is the
`hebrew-prose` skill's `references/rendered-prose.md`.

Two of those conventions are claims about Hebrew accentuation rather than about this repo:

**Never a loose "word"** (wlc-utils#81). An **atom** is one written word, between spaces or maqafs
— the thing a maqaf joins to the next. A **chanted word** is a lone atom *or* a whole maqaf
compound: the unit cantillation operates on, normally bearing one accent. Say which you mean, and
name a compound whole (על־פני, לא־תעשה), never a bare half of one. Plain "word" survives for an
ordinary English word, inside quoted or translated source material (which keeps whatever it says),
**and wherever the context already settles which sense is meant** — what wlc-utils#81 bans is a
loose "word" the reader must resolve from nothing, so the qualifier is owed where the sense is in
doubt and is noise where it is not. A table heading is read with its column, so `Word` over a
column of Hebrew forms is right whether they are simple, compound or mixed (Ben, 2026-07-29); the
sense can still go in the heading's hover text, as the one-letter appendix's does.
`MAQAF_IS_THE_LAST_RUNG` is where "atom" is glossed for the reader; that gloss is what licenses
the bare term on the pages. Note that the two senses come apart exactly where the rung below
matters, so the two rules are best read together.

**Maqaf is the last rung of one scale.** Disjunctives, then conjunctives, then maqaf — a maqaf
separates the atom it sits on from the next even less than a conjunctive does, so it carries the
weakest *separating* force on the scale. (Never write a bare "weakest": a maqaf *binds* tightest,
so unqualified it reads as backwards.) There is no second ledger for "word division". A maqaf
difference is counted **once**, at the atom whose marking changed, never as a regrouping plus an
accent; and it is stated as an **exchange with both marks named** — "a maqaf where its Wikisource
strand has a merkha" — never as the absent maqaf alone. Do not define a maqaf as "the atom left
blank of an accent": that is only the normal case, and `koren_dt_elyon`'s `mun-mun` on לא־תעשה is
a maqaf compound whose joined atom keeps its munaḥ — as are the Simanim Tiqqun's two munaḥ-on-לא.
But do not swing the other way either: in the **prose** system a second accent on a compound is
rare, and is largely just a consequence of the compound being one chanted word — the accents found
there are the ones that can be the first of two on an atomic word, which is also Yeivin's short
list of prose "secondary accents" (munaḥ-zaqef, metigah-zaqef, rare merkha/mehuppakh on a tevir
word). The separate case is a maqaf written after a word that keeps its own conjunctive: a
manuscript habit, and one **L is specifically named for** (Yeivin ITM §293). The **poetic** system
is far more willing to put two accents on one chanted word; that asymmetry is a major difference
between the systems, not a detail. `edition_transcription`'s "HOW RARE THAT IS IN PROSE" paragraph
has it with its Yeivin and Breuer citations.

**Yeivin lives in two places and they are not the same.**
`../MAM-private/al-hatorah/py/itm/` is Ben's
*adaptation* — partial, with sections still untranscribed.
`../MAM-private/masorah-books/books/itm/md-export-of-docx/` is
the *full* OCR of the book. That repo was `yeivin-itm` until 2026-07-31, when it was renamed and
Breuer's *Cantillation of Scripture* was merged into it from `breuer-cos`; CoS is the sibling
`../MAM-private/masorah-books/books/cos/md-export-of-docx/`, so both books are still one clone
away, that clone being MAM-private since 2026-08-10. **The `../masorah-books/…` spellings that
remain in `py/accgram/` docstrings and comments are stale by exactly that one directory** — eight
sites in `breuer_word_length.py`, `chanted_word_accents.py`, `edition_transcription.py`,
`maqaf_nonfinal_accents.py` and `maqaf_nonfinal_accents_page.py`, each naming a path that now
reads `../MAM-private/masorah-books/…`. Ben chose this sentence over editing the eight, 2026-08-10,
as he chose the same answer for UXLC.

**The `al-hatorah` citations in `py/accgram/` are stale the same way, and Ben chose the same
answer, 2026-08-11.** That tree moved to `../MAM-private/al-hatorah/` on 2026-08-10 and its clone
came off the disk on 2026-08-11, so `../al-hatorah/…` names nothing on either count. **Seven
sites**, named here so nobody re-derives them: `chanted_word_accents.py:638`, `final_stress.py:5`
and `maqaf_nonfinal_accents.py:112` write `../al-hatorah/py/itm/` and
`../al-hatorah/py/aht_phon…`, which want `../MAM-private/al-hatorah/…`; `breuer_word_length.py:37`,
`:43`, `:106` and `py/tests/test_final_stress_vs_phonetic_mam.py:4` write "al-hatorah's
`io/a01-phonetic-std-set`" and "al-hatorah's `py/aht_phon`", which want `MAM-private/al-hatorah/`
in front of the in-repo path. Two further mentions name the repo with no path in them —
`edition_transcription.py:67` and `final_stress.py:16` — and read correctly as written.
Search the full OCR before concluding Yeivin is silent on something;
a first pass at wlc-utils#76 searched only the adaptation and wrongly reported the maqaf material
absent. The verbatim reader-facing statement is
`MAQAF_IS_THE_LAST_RUNG`; its guardrail comment records the convention it replaced (a 2026-07-25
audit fix that made maqaf differences non-differences) and why that one was wrong, so it does not
get reinstated. Issue wlc-utils#76.

## Two issue trackers: a bare `#NN` here means MAM-basics

wlc-utils' issues were **not** transferred when its Python moved here on 2026-08-01. They keep
their numbers and stay in `bdenckla/wlc-utils`, which is still where they are read, commented on
and closed — 93 of them as of 2026-08-17 (this paragraph long said 88, a count that was already
five short when it was written: #89–#93 were filed 2026-07-31). The trackers unify *going forward* only: **every new issue, including new work on the
moved code, is filed in MAM-basics.**

So in this repo a bare `#NN` names a MAM-basics issue, and a citation of a wlc-utils issue is
written **`wlc-utils#NN`**. The prefix is not decoration: both trackers have issues in the 1-88
range, and several numbers name quite unrelated things in each — wlc-utils#52 is the printed
Decalogue where MAM-basics #52 asks about a meteg in Ezekiel, wlc-utils#69 the hand transcriptions
where MAM-basics #69 is a CSS URL, wlc-utils#75 making maqaf a token of its own where MAM-basics
#75 is the `mb_cmn/paths.py` convention. The moved code's 326 bare citations were prefixed on
2026-08-02.

Two things a blind sweep gets wrong, so read the surrounding sentence before adding a prefix:

- **Not every `#NN` is an issue.** Yeivin's *ITM* is cited by section number in exactly the same
  shape (`#194`, `#221`, `#246`, and the `#325`–`#391` poetic run), CSS carries hex colours, and
  `poetic_ply_grammar.py` numbers the accents of Ps 17:14 as `#7`–`#10`. None of those take a
  prefix.
- **`wlc_issue_edit.py` is what keeps the split safe, and its own `#69` is deliberate.** `gh`
  resolves which tracker `issue <number>` names from the checkout it runs in, so `repo` is a
  required argument there rather than an inherited cwd; the bare `#69` in its docstring is the
  worked example of the ambiguity and must stay bare.

wlc-utils' own `doc/`, `in/` and `CLAUDE.md` were left alone — a bare `#NN` read there still means
a wlc-utils issue, and qualifying those would imply they were ambiguous.

## There is no `wlc-koren-12th` repo

`~/GitRepos/wlc-koren-12th` was never a repo of its own. It was a **worktree of wlc-utils** on
branch `claude/koren-12th-site`, which is why it sat flat among the siblings and answered
`git remote -v` with `bdenckla/wlc-utils`; its copies of files such as
`py/accgram/poetic_ply_grammar.py` were the same files on an older branch, never duplicates to
reconcile or keep in sync. Repeated sessions read it as a twin repo and burned a turn
"reconciling" it — that is the whole reason for this note. Deleted 2026-07-27, along with the
fully-merged leftover branches `claude/koren-12th-site` and `claude/festive-napier-38d58d`, both
accepted by `git branch -d` (never `-D`), which is the record that nothing was lost. The only
place the name survives is old session transcripts under `~/.claude/projects/`, which is exactly
where the wrong conclusion kept being copied from.

**General lesson:** a directory sitting flat under `~/GitRepos` is not necessarily a repo. Run
`git -C <dir> rev-parse --git-common-dir` (or `git worktree list` from the repo you suspect)
before treating one as a peer whose files need syncing.

(Moved here from wlc-utils' `CLAUDE.md` on 2026-08-17, when Phase 10 of
`doc/PLAN-evacuate-the-rest-of-wlc-utils.md` shrank that file to redirect-host facts — the
disposition that plan's Phase 0 recorded for it. The note lives on because the transcripts do,
and because all wlc work now happens in this repo.)

## Running tests — always from the repo root

Run tests via the canonical entrypoint, from the repo root (`~/GitRepos/MAM-basics`), never from `py/`:

```bash
.venv/Scripts/python.exe py/main_test.py
```

Sibling-repo paths (MAM-parsed, MAM-simple, MAM-with-doc, MAM-OSIS, MAM-for-Sefaria)
are built from `mb_cmn.paths.repo_root()` / `repos_root()` / `sibling_repo(name)` — a
single `__file__`-relative utility (issue #75), not cwd-relative `"../MAM-parsed"`
literals or ad hoc `Path(__file__).resolve().parents[N]` chains. New path-construction
code should use it too. Exception: a handful of files that get vendored/copied verbatim
into sibling repos (`mb_cmn/read_books_from_mam_parsed_plus.py`, `mb_cmn/provenance.py`,
`mb_misc/write_utils.py`, `mb_sefaria/mam4sef_or_ajf.py`) intentionally keep their
existing cwd-relative or self-contained `__file__`-relative logic instead, so they stay
portable when copied elsewhere without also requiring `mb_cmn/paths.py` to travel with them.

Even so, still run from the repo root, never from `py/`: some in-repo paths (e.g.
`in/mam-ws-bot-edits/...`) remain cwd-relative by design, and the venv itself
(`.venv/Scripts/python.exe`) is a repo-root-relative path. Running pytest from `py/`
(e.g. `cd py && pytest tests/`) breaks these with a plain `FileNotFoundError`, which reads
as a real test failure rather than a wrong-invocation-directory error. On 2026-07-01 this
exact mistake produced 17 misleading test failures that got misdiagnosed as
pre-existing/unrelated bugs.

If a shell has already `cd`'d into `py/` from an earlier command, explicitly `cd` back to
the repo root before running tests — a persistent-cwd shell keeps resolving
repo-root-relative paths wrong otherwise.

**`py/main_test.py` is the only runner — a bare `pytest` is not supported from anywhere,
including the repo root.** `fd2241a` migrated this repo onto that single entrypoint on
purpose. It needs no path configuration because CPython prepends a script's own directory
to `sys.path`, which is exactly why the entrypoint lives in `py/` and not at the root. So
`pytest py/tests` failing with ~34 `ModuleNotFoundError` collection errors (`No module
named 'mb_author'`, ...) is the designed state, not a defect: **do not "fix" it** with a
`pytest.ini` `pythonpath`, a root `conftest.py`, a `.pth`, or `PYTHONPATH`. Each re-creates
the second entrypoint the migration removed. This was reported as a bug on 2026-07-30 and
the report was wrong. The cross-repo rule is user-level CLAUDE.md's "No `sys.path` surgery"
section, which this repo is the worked example for — it is what settled the standard at zero
inserts per repo rather than one. `py/versification_and_cantillation/doc.py`'s module
docstring says the same thing.

**There is no test registry any more, and no file to add a new test to.** `main_test.py`
was a hand-maintained `TEST_MODULE_SPECS` tuple plus a `unittest` loader until 2026-08-01;
it is now a `pytest.main()` wrapper, so pytest discovers `py/tests/` itself. The registry
is gone because of the failure mode it had: an unregistered file does not skip, it reports
nothing at all — worse than the silent-green skip the global rules warn about — and two
files went unrun that way here from the 2026-05-03 migration until 2026-07-30, one of them
edited four times meanwhile.

**Drop a new test file in and it runs, so long as it is named `test_*.py` or `*_test.py`.**
Those two patterns are pytest's default `python_files` and both are in use under
`py/tests/`: this repo's own tests are prefix-named, and the CLC tests that arrived from
UXLC-utils on 2026-08-01 are suffix-named. A file matching neither is the registry's failure
mode back again — nothing collects it and nothing says so. `py/tests/mc_marks.py` is the one
file there matching neither, and rightly so: it is a helper four test modules import
`mc_to_marks` from, not a test.

Arguments pass straight through to pytest, so `-k`, `-x`, `-q`, `--lf` and `--collect-only`
all work; naming a file replaces the default target of the whole `py/tests` tree:

```bash
.venv/Scripts/python.exe py/main_test.py --collect-only -q
```

Both test styles collect natively — this repo's `unittest.TestCase` classes and the
module-level `def test_` functions that arrived with the wlc-utils code — so no test file
was rewritten in either direction.

## Writing tests — differential and lint-shaped only

An audit of git history, comments, and issues across all of Ben's repos (2026-07-25) found
four occasions where a test demonstrably found something, and **zero** recorded cases of a
pre-existing example-based unit test failing later and thereby catching a regression. All
four have one of two shapes. Do not add a test unless it is one of them, or Ben asks.

- **A differential check against an independent oracle** — regenerate the corpus and compare
  against a frozen reference or a second derivation of the same fact. The accgram code that
  arrived from wlc-utils on 2026-08-01 brought two of the four: the PLY parity comparator against
  the frozen C `accents` checker, and the printed-Decalogue transcriptions against their vendored
  strands.
- **A mechanical lint over the tree** — a decidable property of the *source text* rather than
  of behavior (`py/tests/test_h_dot_below_nfc.py`, `py/tests/test_transliterations.py`
  (wlc-utils#26), and the `check_repo_standards.py` scans are this shape).

Otherwise the generated, git-tracked artifact is the test: regenerate it with the real command
and read the diff. Unexplained diffs are failures until explained. This is how the real bugs
here were actually found — `1ef8f51` (#199, a top-level ketiv/qere silently dropped from a
strand) surfaced as wrong text in generated output, not as a red test.

Do not write an example-based unit test that pins one hand-picked case, a string, or a name.
Nothing in the record shows one catching anything, and they have to be dragged through every
terminology rename.

**A missing input must FAIL, never skip.** wlc-utils' `25a7800` removed twenty-one skip guards
that reported green having verified nothing. Skips are a *semantic* channel in the accgram tests
(a skip reports that a page diverges from its strand), so an environment skip mixed in corrupts
the signal. An empty `@parametrize` list also reports as a skip — hence the
`or ["(none committed)"]` fallbacks, which are the failure mechanism and must stay. Reach for
`require_sibling` rather than a "sibling repo not present" skip.

**The `ws_bot` tests are a deliberate exception.** A Wikisource edit is an irreversible,
outward-facing action against a live wiki, and there is no regeneratable artifact to diff
after the fact — so pinning an edit payload before it is sent is worth its cost on those
grounds, not because the general rule has an escape hatch.

The fullest statement of this rule, with the evidence behind it, is in the sibling repo:
`wlc-utils/doc/agent-planning-principles.md` §"Generated Outputs Are the Tests".

**This file is the only instruction file this repo has.** `CLAUDE-disabled.md` and
`.github/copilot-instructions-disabled.md` were deleted on 2026-08-03, when GitHub Copilot
stopped being used; nothing in either was moved here, because it was stale or already said
better in `~/.claude/CLAUDE.md`, in `doc/`, or in the docstring of the module it described.
Both are in git history if a claim in them ever needs checking.
