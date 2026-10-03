# Verifying prose that makes claims

## The generated artifact is the test

`MAM-basics/doc/agent-planning-principles.md` §"Generated Outputs Are the Tests" is the full rule.
In short:

- Edit the declared generator, then regenerate its output. Preserve declared hand-authored exceptions.
- Regenerate the relevant JSON and HTML with the **real CLI command**.
- Inspect the generated files for the expected changes.
- Confirm that files expected to be unchanged **are** unchanged.
- Treat any unexplained diff in generated JSON or HTML as a failure until explained.

One run writes both the page and its data, so the two cannot drift.

## Commands

All of accgram runs from the selected **MAM-basics** checkout's repository root and
writes into that checkout's own `out/` and `gh-pages/wlc/` — the code moved on 2026-08-01 and the
corpus followed on 2026-08-12:

The active examples below show a Windows full clone's interpreter. A Linux cloud checkout
uses `.venv/bin/python` from its own hydrated environment; a linked worktree names its home
clone's interpreter by absolute path. Hydration follows the checkout's tracked requirements
and constraints. Preserve dated historical commands as evidence about those earlier runs.

```bash
.venv/Scripts/python.exe py/main_accgram.py generate-html
```

One page at a time — `generate-html-<name>`, where `<name>` is the output file's basename:

```bash
.venv/Scripts/python.exe py/main_accgram.py generate-html-maqaf-nonfinal-accents
```

Others: `generate-html-poetic`, `-goerwitz`, `-almost-errors`, `-supplied-marks`,
`-printed-decalogue-simanim`, and so on.

**Two accgram subcommands write outside `gh-pages/wlc/`, and the first of the two is where the
post-stress-meteg work lives**, so do not go looking for those pages under `accgram/`:

1. **`survey-post-stress-meteg` writes only its JSON, `out/accgram/post-stress-meteg.json`. Its
   nine pages are at the DEPLOY ROOT** — `gh-pages/post-stress-meteg.html` and eight of its
   `gh-pages/post-stress-meteg-*.html` sub-documents — and no accgram subcommand renders them.
   `py/main_authored.py gen-site` does. It also writes `gh-pages/index.html`,
   `gh-pages/unicode-proposals.html`, and one post-silluq case page per entry of
   `site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES`; the case pages render from
   `in/meteg_after_silluq_cases.json`, not from the survey. The survey reads the
   tracked public `Phonetic-MAM/` release and public MAM. `--trust-surveys` lets
   `gen-site` read its tracked JSON instead of calculating the same survey twice;
   the mega runs the public survey in cloud sessions too.
2. **`survey-breuer-zaqef-units` writes `.novc/breuer-zaqef-units.json` and nothing tracked at
   all** — it is a measurement, so it touches neither `out/` nor `gh-pages/`.

`Phonetic-MAM/README.md` and `Yeivin-ITM/README.md` own their current command
contracts. Only the Phonetic exporter requires the private source adapter;
rendering, the independent pre-stress analysis and the Yeivin claim/render/check
commands consume public data. The full Yeivin OCR remains a private research
source, distinct from the selected public adaptation.

The `gh-pages/post-stress-meteg*.html` pages, those nine and the case pages alike, are also the
one place the skill's "never a loose word" rule is suspended: `references/mam-basics.md`
§'The post-stress-meteg pages say plain "word"' records Ben's decision of 2026-09-08, and
`py/tests/test_post_stress_meteg_plain_word.py` enforces it by forbidding "chanted" in every one.

From a MAM-basics worktree, follow `AGENTS.md`, “Running tests”, and, for ChatGPT-Codex, the
worktree runtime reference of `codex-worktree-tasks`. Siblings normally resolve through Git's
common-directory metadata; `REPOS_ROOT` is an override for an unusual layout. The worktree ban
withdrawn on 2026-09-09 had named a loud failure and a silent provenance failure; their
historical dispositions follow.

1. **The loud one, `mb_cmn/read_books_from_mam_parsed_plus.py`'s cwd-relative `"../MAM-parsed"`
   default, no longer tells a worktree from the repo root, because it is dead in both.** The
   default is still on `read_parsed_plus_bk39s` and `read_parsed_plus_bk24`, kept for the
   external vendored consumers that `mb_cmn/paths.py`'s `mam_parsed_path()` docstring names:
   "Callers supply this path explicitly. The portable reader's legacy default remains for
   external vendored consumers; MAM-basics does not use that default." Every MAM-basics caller
   does pass it — fourteen call sites, `git grep -n read_parsed_plus_bk39s`. And MAM-parsed is a
   landed product inside MAM-basics, `MAM-parsed/` under the repo root, so
   `C:/Users/BenDe/GitRepos/MAM-parsed` does not exist and that default resolves to nothing from
   the repo root either.
2. **The silent one, the worktree's directory name written into the provenance breadcrumb, has
   been fixed** — by MAM-basics `0008eb8d` (2026-08-11, "Derive the repo name from git's own
   files, not the checkout directory"). The bug was real and is worth keeping on the record: it
   was found on 2026-08-07, when `MAM-simple/doc/versification-differences.md` regenerated from a
   worktree as "generated by busy-chebyshev-613a3b/py/...". `mb_cmn/provenance.py`'s
   `this_repo_name()` and `repo_name_of()` docstrings hold both that bug and the chain that
   replaced it — the common git dir, then the basename of `remote.origin.url`, then that dir's
   parent when it is literally named `.git`, then `root.name` — under the rule those docstrings
   state in capitals, that a worktree is the same repo and a breadcrumb from one must name the
   repo.

**So what is left to check in a worktree is neither of those two: it is that the breadcrumb says
`MAM-basics/...` and not the worktree's directory name.** Regenerate on a clean tree and read
`git status`; an empty status is the whole verification, and it leaves nothing to revert.

Measured 2026-09-09 in the worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/verify-worktree-regeneration`,
at commit `20ebbac1`, tree clean, with `REPOS_ROOT=C:/Users/BenDe/GitRepos`: `py/main_accgram.py
survey-post-stress-meteg` (51s), `py/main_authored.py gen-site` (53s, all eleven deploy-root
pages) and `py/main_accgram.py generate-html-maqaf-nonfinal-accents` (6s) each rewrote their
tracked artifacts byte-identically, `git status --porcelain` staying empty throughout. The suite
in that same worktree passed **983 with 5 skipped** (114s). `MAM-basics/CLAUDE.md` §"Running
tests — always from the repo root" documents the same `REPOS_ROOT` setting for the suite, so
while this reference carried the worktree ban withdrawn on 2026-09-09, which read “Never from a
git worktree, only from that repo root”, the skill contradicted the repo's own instruction file.

**Outside MAM-basics this is advice rather than a measured result**, Ben's decision of
2026-09-09: both fixes above are MAM-basics' own — `mb_cmn/paths.py`'s override chain and
`mb_cmn/provenance.py`'s repo-name derivation — and nobody has established that another tree,
`masorah-books` above all, derives its breadcrumbs the same way. Check the breadcrumb and the
diff there before trusting a worktree regeneration. Reinstating the old ban for those trees was
considered and rejected the same day, as a claim of breakage with no measurement behind it.

Tests run from the verified repository root with the full clone's own interpreter, or a
linked worktree's home-clone interpreter by absolute path, following
`AGENTS.md`, “Running tests”, and, for ChatGPT-Codex, the worktree runtime reference of
`codex-worktree-tasks`:

```bash
./.venv/Scripts/python.exe py/main_test.py
```

`py/main_test.py` is the only runner — a bare `pytest` failing to collect is the designed state,
not a defect. A 2026-07-01 run from `py/` produced 17 misleading failures.

In `masorah-books`, the eighteen OCR passes over Yeivin and Breuer are subcommands of one entry
point, run with the cwd at that tree's own root —
`<forest>/MAM-private/masorah-books` since the tree moved into `MAM-private` on
2026-08-10, never MAM-private's root — and on that tree's own `.venv`:

```bash
.venv/Scripts/python.exe py/main_ocr.py <subcommand>
```

`<forest>` is the directory holding the invoking checkout's home clone, `$HOME/GitRepos` or
`$HOME/GitRepos<N>`.

Since 2026-08-01 **no module there is runnable on its own**, and this is by design:
`python py/cos/check_cos_claims.py` puts `py/cos/` on `sys.path[0]` and cannot find the shared
`ocr_cmn` layer. `cos-convert` takes a `.docx` path, one invocation per file, and is the only one
of the eighteen with a positional argument at all; the other seventeen take none.

Each pass has a gate, and the gates stand in for a test suite: re-run and require the same result.
**Those gates and their figures have exactly one home, `MAM-private/masorah-books/README.md`
§"The tooling and its gates"**, which tables all eighteen subcommands against their modules, what
each one does, and the result to require of it. Read them there. Do not copy any of them back
into this file.

**A six-row copy of that table stood here until 2026-09-09, when Ben had it deleted, because it
went stale twice.** github-misc `1925699` corrected its `cos-check-claims` figure in
`references/sources-and-corpora.md` on 2026-09-07 and missed this file's copy of the same figure;
that commit's message says "The whole file was checked for a second statement of the figure and
there is none", which was true of the one file it searched. Two days later the copy here was
stale in two of its six rows: `cos-check-claims` still read 19 of 19 and `cos-fillin-probe` still
read 22 numbers, both figures the README had long since moved past. Naming what the README says
today would restart the same clock, so this paragraph names only the two retired figures, which
cannot go stale. Correcting those two a third time would have
kept the two-copy arrangement that produced both, and the README was already this paragraph's
declared authority, so the table added nothing but a second place to go wrong. This is
§"Never quote a number you have not read back"'s corollary — do not restate a survey's numbers,
keep a pointer — turned on the skill itself.

## Never quote a number you have not read back

On **2026-07-26** a figure restated from memory instead of read out of the regenerated file
reached Ben wrong. Every count, frequency and "N of M" in prose must be read out of the artifact
that the committed command just wrote — not from a plan, not from a docstring, not from an
earlier turn in the session. If the number is in the page because it was spliced from the survey,
it cannot drift; if it is in the prose as words, it can, which is what `pin_claims` is for.

Corollary: **do not restate a survey's numbers in another module's docstring.** Keep a pointer.

## `pin_claims`: keeping stated-in-words claims honest

A page's counts can be spliced from the data; its **argument** cannot. So the handful of facts
every sentence rests on get pinned in code that re-derives them from the survey and **raises** on
drift:

- `maqaf_nonfinal_accents_page.pin_claims` — asserts the page's stated facts against the data and
  fails the build.
- `printed_decalogue_strands.resolve_readings` — pins each derived strand against `READING_SPECS`
  / `STRUCTURE`; `resolve_pausal` and `check_tirtsax` do the same for the appendix's vowels.

**Never soften one of these to a warning:** a warning in a generator's output is a warning nobody
reads. Add a pin whenever you write a sentence whose truth a re-vendoring or a corpus bump could
quietly overturn.

Prior art for a fuller claim/verifier scheme is **MAM-basics**: `py/mb_author/claim.py`
(`ClaimCollection.claim(id, payload, kind=, subject=, data=)`, dot-segmented kebab ids),
`py/verify_mp/` (one verifier per id in a module-level `REGISTRY`), and the generated index
`doc/mp-claims.md`. Copy those id/subject/verifier conventions rather than inventing new ones.

## Test-policy authority and dated rationale

The common body, “Tests are differential or lint-shaped”, owns the current test-shape rule.
Follow the repository's declared exceptions, including MAM-basics' `ws_bot` and cloud-only
test declarations. `doc/agent-planning-principles.md`, “Generated Outputs Are the Tests”,
preserves the rationale; this reference does not add another test policy.

The 2026-07-25 audit recorded four occasions where a test demonstrably found something and
zero recorded cases of a pre-existing example-based unit test later catching a regression.
Its differential examples included the PLY parity comparator against the frozen Goerwitz C
checker and the Decalogue checks against vendored strands. Its lint examples included the
transliteration and NFC checks. Those are dated audit observations, not a current census.
The historical removal of twenty-one missing-input guards by `25a7800` explains the fail-loud
rule; it does not override the repository's subsequently declared cloud exception.

## Mechanics that bite while editing this prose

- **Run black on every Python file you touch**, before committing — mandatory. Default settings,
  no config anywhere, so the limit is **88**. Long lines you see inside triple-quoted strings and
  comments are not evidence of a laxer limit; black never reformats those. Format only the files
  you changed, in a single invocation:

  ```bash
  .venv/Scripts/python.exe -m black <files>
  ```

  Repo-wide reformatting is its own commit.
- **No inline scripts.** No `python -c`, no heredocs, no PowerShell here-strings — write a real
  temp file (a repo's gitignored `.novc/`, the session scratchpad, or `/tmp`) and run it. Same for
  multi-line CLI *arguments*: `git commit -F <file>`, `gh ... --body-file <file>`. Piping into
  `python -c` makes Python decode stdin with surrogateescape, and with Hebrew text a lone
  surrogate then throws on re-encode — that once silently pushed an empty body to a GitHub issue.
- **UTF-8 stdio.** On Windows, redirected stdout encodes with cp1252 and the first Hebrew
  `print()` dies. Reconfigure at the top of `main()`:
  `sys.stdout.reconfigure(encoding="utf-8")`, and for stderr
  `sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")`, since an encoding given
  without `errors` resets stderr's handler to `strict`. Better still, keep non-ASCII off stdout
  entirely — write it to a file opened with `encoding="utf-8"` and read it back.
- **No orphan combining marks in source.** Never a bare diacritic in a string literal; use
  `"\N{HEBREW POINT METEG}"`, `"\N{COMBINING GRAPHEME JOINER}"`. A mark anchored on a base letter,
  and real Hebrew text data, are fine.
- **Edit-match hazard.** The decomposed-ḥ problem is gone since #49 (the repo is precomposed NFC,
  so a typed ḥ matches). Still live: **curly apostrophe U+2019** and **em dash U+2014**. After
  **one** failed match, stop retyping the glyph — either re-scope the Edit to pure-ASCII anchors,
  or write a temp `.py` that builds each needle from `chr(0x2019)` / `chr(0x2014)` and does
  `read_bytes()` → `replace(OLD, NEW, 1)` → `write_bytes()` with a `count == 1` assertion (bytes
  I/O preserves LF endings and normalization).
- **Files change under you mid-session.** Ben edits the same file in parallel — re-diff before
  staging, and commit only your own work.
- **Sibling paths and test invocation follow the repository's instructions.** MAM-basics'
  `AGENTS.md`, “Running tests”, owns the current procedure, with
  `codex-worktree-tasks/references/worktree-runtime.md` for ChatGPT-Codex; do not copy an
  override recipe here.
- **Committing and pushing: follow the common `~/.codex/AGENTS.md` body, section "Git and
  commits", imported by Claude Code through `~/.claude/CLAUDE.md`.** This bullet cites that
  section rather than restating it. It read
  "Commit only when Ben asks, directly to `main` (he works solo, no feature branches), and do not
  push unless asked" until 2026-09-09. That section reversed it on 2026-09-07: finished work is
  committed without asking; a secondary worktree commits to its own non-`main` branch rather than
  to `main`; and the branch is merged into `main`, verified in the worktree, and `main`
  fast-forwarded and pushed just before the session is archived. **Restating that section here is
  how this bullet went stale**, so it names the section and states no rule of its own.
