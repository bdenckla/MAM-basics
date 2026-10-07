# History of ws_bot_edit.py

The file `ws_bot_edit.py` is overwritten for each new Wikisource bot run.
This document records the distinct bot eras found in the git history of
the predecessor repo (`trope.old.use-mam-basics-instead`), since this
repo's history starts from a single squashed commit.

None of the old versions have been resurrected as files because the
infrastructure has changed enough to make them misleading examples:

- **Import paths changed.** Old bots import from `py.ws_bot_edit_wsf2_chap`
  or `py.bot_edit_wsf2_chap`, modules that no longer exist. The helper
  functions they provided (dispatcher, pass-thru, recurse-on-args) were
  consolidated into `ws_bot_edit.py` itself during the YBY era.
- **Package structure changed.** Old bots use `import py.ws_tmpl1`,
  `import py.hebrew_accents`, etc. Current code uses `from mb_cmn import ...`
  and `from ws import ...`.
- **Signature changed.** Some old bots have
  `edit_page_text(summary, he_chnu, page_text)` (summary as first arg).
  Current callers pass `(he_chnu, page_text)`.

## Bot eras (oldest first)

### Pass-through / newline standardization
- **Commit:** `4a5bb227`
- **Purpose:** No-op edit — ran the full parse-and-unparse pipeline to
  normalize newlines without changing content. Baseline for verifying the
  roundtrip.

### עלייה (aliyah) handling
- **Commits:** `2039cb08` .. `f23a13ac`
- **Purpose:** Rewrote how Torah reading divisions (עלייה) are represented
  in the `{{מ:פסוק}}` (verse) template. Removed the old `עלייה ראשונה`
  named parameter and replaced `עלייה` with a new `{{אןאןאן}}` template
  placeholder (later finalized as `{{מ:עלייה}}`).
- **Edit level:** Location templates (the `_VANDLERS["location"]` slot),
  not verse-body text.

### Legarmeh upgrade (groundwork only)
- **Commits:** `5bca7b05` .. `0d4ce058`
- **Purpose:** Preparatory work for upgrading legarmeh representation.
  Never reached a complete bot edit in this era.

### Trivial ketiv/qere
- **Commit:** `82f55adc`
- **Purpose:** Added explicit `2=` prefix to the second argument of
  `{{קו"כ-אם}}` (trivial ketiv/qere) templates, disambiguating
  positional from named parameters.
- **Edit level:** Verse-body templates via the wandler dispatch table.

### x-velo-y (ketiv-velo-qere / qere-velo-ketiv)
- **Commits:** `948dc89b` .. `dfb8744f`
- **Purpose:** Reformatted `{{כתיב ולא קרי}}` and `{{קרי ולא כתיב}}`
  templates to add an explicit stripped-punctuation argument (removing
  parentheses / brackets from the display text).
- **Edit level:** Verse-body templates.

### Dexnor (dehi / tsinor accent templates)
- **Commit:** `881408b6`
- **Purpose:** Handled `{{מ:דחי}}` and `{{מ:צינור}}` accent templates.
  When a template had only 2 elements (no explicit extra arg), unwrapped
  it to inline the content.
- **Edit level:** Verse-body templates.

### GLGL (galal template confinement)
- **Commit:** `e927225d`
- **Purpose:** Confined the `{{גלגל}}` template into `{{גלגל-2}}`, using
  the same confinement pattern later used for YBY. Essentially a precursor
  / sibling of the YBY bot.
- **Edit level:** Verse-body wikitext sequence (`_edit_wtseq_2`).

### YBY (yerah-ben-yomo template confinement)
- **Commit:** `a17ddd6d` (old repo), `d86e577` (this repo's initial import)
- **Purpose:** Confined `{{ירח בן יומו}}` into `{{ירח בן יומו-2}}`.
  The template is replaced by a new version whose single argument contains
  the preceding and following text that "belongs" to the accent.
- **Edit level:** Verse-body wikitext sequence (`_edit_wtseq_2`).
- **Preserved as:** `ws_bot_edit_old_yby_confine.py`

### Joshua meteg removal (48 edits)
- **Purpose:** Removed 48 meteg (U+05BD) marks from specific words in
  Joshua, aligning Wikisource with another edition where MAM-parsed-plus
  previously added a meteg that edition does not have (private annex §3).
- **Edit level:** Raw page text string replacement.
- **Preserved as:** `ws_bot_edit_old_joshua_meteg.py`

### JSON-driven meteg removal
- **Purpose:** Generalized the bot to read edit specifications from a JSON
  file rather than hard-coding them. The JSON file provides the edit summary,
  edit kind (e.g. "meteg-removal"), and per-book/chapter edit entries.
  First use: remove 7 meteg marks from Deuteronomy (private annex §3).
- **Edit level:** Raw page text string replacement (same as Joshua era).
- **JSON files:** `in/mam-ws-bot-edits/`
- **Preserved as:** `ws_bot_edit_old_deuter_meteg.py`

### Trivial k/q template upgrade
- **Purpose:** Replace all `{{קו"כ-אם}}` calls (old 2-param style) with
  `{{מ:קו"כ-אם-2}}` calls (new 5-param style), per MAM-basics#55.
  New params: pointed ketiv, unpointed ketiv, pointed qere, optional
  `מקורות=` (source), optional `סוג=` (type, deferred to follow-up).
- **Edit level:** Full cif2 AST traversal via candlers/vandlers/wandlers.
- **JSON files:** `in/mam-ws-bot-edits/kq-trivial-to-2.json`
- **Preserved as:** `ws_bot_edit_old_kq_triv_to_2.py`

### Trivial k/q subtype tagging
- **Purpose:** Add `סוג=` labels to `{{מ:קו"כ-אם-2}}` for five named
  trivial k/q subtypes (`QyV`, `extra-alef`, `hi-spelled-hu`,
  `n3rh-spelled-n3r`, `xolam-he`) while leaving subtype `misc` untagged,
  with fail-fast FOI concordance checks.
- **Edit level:** Full cif2 AST traversal via candlers/vandlers/wandlers.
- **JSON files:** `in/mam-ws-bot-edits/kq-trivial-2-add-type-tags.json`
- **Preserved as:** `ws_bot_edit_old_kq_triv_add_type.py`

### Rename extra-alef סוג label
- **Purpose:** Rename the trivial-k/q extra-alef סוג label from
  `אל"ף מיותרת` to `אל"ף נחה באמצע תיבה ולא נקראת` per MAM-basics#70.
- **Edit level:** Raw page text global replacement on
  `{{מ:קו"כ-אם-2|...|סוג=...}}` values.
- **JSON files:** `in/mam-ws-bot-edits/kq-trivial-2-rename-extra-alef-sug.json`

### Add rafeh to three יראו forms
- **Purpose:** Add rafeh (U+05BF) to the three remaining no-rafeh
  occurrences among the four issue-56 יראו words, leaving 2Sam 11:24 as-is
  because it already has rafeh.
- **Edit level:** Chapter-targeted raw page text string replacement.
- **JSON files:** `in/mam-ws-bot-edits/issue-56-add-rafeh-to-yireu.json`

### Issue 67: migrate deprecated כו"ק call sites to מ:כו"ק מיוחד
- **Purpose:** Migrate call sites of nine deprecated issue-67 כו"ק template
  names to `{{מ:כו"ק מיוחד|...|סוג=...}}`, where `סוג` is derived from the old
  template name without the `מ:` prefix.
- **Safety rule:** Hard preflight for `רווח=כן`; fail fast for manual handling.
- **Edit level:** Full cif2 AST traversal via candlers/vandlers/wandlers.
- **JSON files:**
  `in/mam-ws-bot-edits/issue-67-kuk-special-callsite-migration.json`

### Issue 260: replace the sigil ב2 with ת451
- **Purpose:** Replace the manuscript sigil ב2 with ת451 in Daniel's
  documentation notes. The two are two sigils for one manuscript: the MAM
  editor chose ב2 first, abandoned it, and switched to the number the
  manuscript had when Meir Benayahu held it, without updating the uses
  already written. 32 occurrences over six chapters of Daniel, measured
  2026-08-27: chapter 7 has 17, chapter 8 has 2, chapter 9 has 3, chapter 10
  has 3, chapter 11 has 6, and chapter 12 has 1.
- **Safety rule:** A per-chapter expected-count table doubles as a skip list,
  so a book or chapter it does not name passes through untouched; a chapter it
  does name must hold exactly the counted number of occurrences. Separately,
  a page carrying the aliyah template's `|ב2=` named parameter — the same two
  characters, 216 of them in the Torah, and never a sigil — is an error rather
  than a skip.
- **One-shot:** the count table describes the pre-edit corpus, so re-running
  after the live edit's re-download raises rather than doing nothing.
- **Edit level:** Raw page text global replacement, counted per chapter.
- **JSON files:** `in/mam-ws-bot-edits/sigil-b2-to-t451.json`
- **Plan:** `doc/PLAN-replace-sigil-b2-with-t451.md`

### Holman meteg rollout: 29 metegs removed, one added
- **Purpose:** Apply the thirty MAM suggestions Daniel Holman sent that differ
  from their Aleppo Codex comparison form in metegs alone. Twenty-nine take a
  meteg off an atom of MAM; one, M23 at Isaiah 23:12.11, puts one on. Ben
  accepted all thirty on 2026-09-03 and gave the go-ahead for the live save the
  same day. Run 2026-09-03: 23 chapters saved over seven book-sized slices —
  1 Kings 7, 11, 12, 15, 17, 18 and 22; Judges 1, 5, 6 and 21; 2 Chronicles 6,
  18, 24 and 32; 2 Samuel 11, 12, 15 and 18; 1 Samuel 18 and 27; 2 Kings 7; and
  Isaiah 23.
- **Two files, because `edit-kind` is file-level:** the 29 removals are
  `meteg-removal` and M23's addition is `explicit-replacement`, so one file
  cannot hold both.
- **Safety rule:** every `old` string is the wikitext's own bytes, located by
  the record rather than retyped from `mam_form`, which is in MAM-normal mark
  order where the wikitext is not. `edit_page_text` asserts each `old` occurs
  exactly once in its chapter, and the removal kind strips the FIRST U+05BD in
  `old` — which is what keeps the silluq of a verse-final ירושלם, whose
  `{{מ:ירושלם}}` call has a second U+05BD as its second parameter.
- **A selector is mandatory:** a bare `--book39` selects a whole book, and
  `assert_book_plans_within_target_set` then refuses every chapter the spec does
  not name, exiting before a page is fetched.
  `main_ws_bot.py holman-meteg-spec --selector-dir .novc` wrote the selector,
  one file per spec.
- **One record was already applied:** M18, 2 Kings 21:12, whose meteg was gone
  from Hebrew Wikisource before the files were built. `_ALREADY_APPLIED`
  excludes it by name, which is why the removal file has 29 entries for 28
  records — M13 being the one record with two, its `{{מ:קמץ}}` call's ד and ס
  parameters each holding the atom.
- **One-shot:** every `old` describes the pre-edit corpus, so
  `holman-meteg-spec` raised after the live edit's re-download rather than doing
  nothing. Confirmed 2026-09-03, immediately after the run: it raised on M1.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/holman-meteg-removal.json`,
  `in/mam-ws-bot-edits/holman-meteg-add-isaiah-23-12.json`
- **Plan:** `doc/PLAN-holman-meteg-rollout-programme.md`, item 3
- **Removed 2026-09-10:** the `holman-meteg-spec` subcommand and
  `py/ws/holman_meteg_edit_spec.py`, by phase 6a of `doc/PLAN-mega-coverage.md`. The
  two JSON files stay as records, and
  `git show c3417599:py/ws/holman_meteg_edit_spec.py` recovers the builder.

### Note links: one link template renamed, four bare links templated
- **Purpose:** Fix five links in documentation notes that MAM-with-doc
  rendered wrongly. Leviticus 10:6 cited an archive.org page through the
  internal-link template `{{מ:קישור פנימי בהערה}}`, whose first parameter
  names a Wikisource page, so MAM-with-doc linked to
  `https://he.wikisource.org/wiki/https://archive.org/...`; the call became
  the external-link template `{{מ:קישור בהערה}}`. Four notes, at Exodus 26:7,
  1 Samuel 13:21 and Job 6:10 (two), used MediaWiki's bare `[URL text]`
  syntax, which MAM-parsed keeps as plain text, so MAM-with-doc showed the
  brackets and the URL; each became `{{מ:קישור בהערה|URL|text}}`. A Claude
  Code cloud session wrote both files on 2026-09-27, and Ben gave the
  go-ahead for each save the same day. Run 2026-09-27: 4 chapters saved —
  Leviticus 10, then Exodus 26, 1 Samuel 13 and Job 6.
- **Two files, one per problem,** each with its own edit summary; both are
  `explicit-replacement`.
- **Safety rule:** every `old` string was cut from the page text rebuilt from
  `in/mam-ws/` as refreshed by 97c4aff5, and `edit_page_text` asserts each
  occurs exactly once in its chapter. Each `--no-save` dry run's edited
  chapter equalled that capture with the file's replacements applied,
  codepoint for codepoint.
- **Parameter form:** the new calls give the URL and the text as parameters 1
  and 2 without `1=` and `2=`, as 13 of the 29 earlier calls did; none of the
  five URLs or texts contains `=` or `|`.
- **One-shot:** every `old` describes the pre-edit text, so a re-run raises
  on its first `old` rather than doing nothing.
- **Guard:** `_check_note_link_tmpl` in `py/py_misc/check_mpplus.py`, added
  the same day, stops parse-ws when a `{{מ:קישור בהערה}}` target is not an
  http(s) URL or a `{{מ:קישור פנימי בהערה}}` target is one.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/lev-10-6-external-link-template.json`,
  `in/mam-ws-bot-edits/bare-links-to-external-link-template.json` and its
  selector, `bare-links-to-external-link-template.chapters.json`

### Post-maqaf ketiv/qere: four calls given the qere-first template — current
- **Purpose:** Give the template `קו"כ` to the four ketiv/qere whose qere directly
  follows a maqaf but whose call was `כו"ק`: 2 Samuel 20:23, Jeremiah 48:21,
  Ezekiel 39:25 and 2 Chronicles 13:19. MAM's introduction prescribes `קו"כ` where
  the qere directly follows a maqaf: `in/mam-ws-intro/ch2.mediawiki`, line 75, with
  line 64, and `appendices.mediawiki`, line 366. Both templates take the ketiv as
  parameter 1 and the qere as parameter 2, so each call kept its arguments and
  changed only its name, and MAM's rendered pages now have the qere first at the
  four. A read-only Claude Code session found the four on 2026-10-06 and wrote the
  prompt for the session that wrote the file and ran it the same day, after Ben's
  go-ahead for the save. Run 2026-10-06: 4 chapters saved — 2 Samuel 20, revision
  3008002 → 3087504; Jeremiah 48, 3010625 → 3087505; Ezekiel 39, 2988075 → 3087506;
  and 2 Chronicles 13, 2988488 → 3087507.
- **The four were an artifact of a 2015–16 automatic update,** according to the four
  pages' histories, read through the API on 2026-10-06. The 2011 import by Erel
  Import Bot wrote all four as `{{כתיב וקרי|…|אחרי מקף=1}}`, as it wrote the same
  ketiv/qere pair after a maqaf at Ezekiel 16:53. The same bot's automatic update
  gave the four `כו"ק`: 2 Samuel 20 on 2015-10-02, Ezekiel 39 and Jeremiah 48 on
  2015-11-08, and 2 Chronicles 13 on 2016-01-04. In the 2015-11-08 sweep it gave
  Ezekiel 16:53 the template `קו"כ` at 06:03:48 UTC and, 58 seconds later, gave
  Ezekiel 39:25 the template `כו"ק`, with 27 other Ezekiel chapters edited in
  between. No later edit touched the four calls.
- **Scope:** a call counted if its opening braces directly followed a maqaf, or if
  it began the first parameter of a `{{נוסח}}` call that directly followed one. By
  that definition, `in/mam-ws/` as of 298958d3 had these four `כו"ק` and no others.
  The two ketiv-first `{{מ:כו"ק מיוחד}}` calls between two maqafs, at Isaiah 26:20
  and 1 Chronicles 9:4, which the introduction prescribes, were left alone.
- **Safety rule:** a script cut each `old` string from the page text rebuilt from
  `in/mam-ws/`: the atom before the maqaf, the maqaf and the whole call, so
  `edit_page_text`'s exactly-once assertion also checked that the call still
  followed the maqaf. The `--no-save` dry run's edited chapters equalled that
  capture with the replacements applied, codepoint for codepoint. The saving run's
  chapters equalled the dry run's, and the post-run download equalled both.
- **One-shot:** every `old` describes the pre-edit text. Confirmed 2026-10-06,
  immediately after the run: a `--no-save` re-run raised on 2 Samuel 20.
- **Near-Aleppo seals:** `in/near-aleppo/frozen-pointed-ketiv.json` seals Jeremiah
  48:21, Ezekiel 39:25 and 2 Chronicles 13:19, and `reviewed-pointed-ketiv.json`
  seals 2 Samuel 20:23, each with digests of a target whose template name is part
  of what is hashed, and both pin every MAM-parsed plus book's file hash. Ben chose
  on 2026-10-06 to re-seal them mechanically, in a commit of its own after this
  run's record, which proves that each target changed in its name alone.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/post-maqaf-ketiv-qere-to-qere-first.json` and
  its selector, `post-maqaf-ketiv-qere-to-qere-first.chapters.json`

## How to look up the original code

All old versions live in the predecessor repo, `bdenckla/trope`. No forest keeps a clone of it
(`in/repo_maintenance_policy.json`, `repos_to_keep_absent`), so read them from a disposable clone
in a scratch directory outside every forest:

```
gh repo clone bdenckla/trope <scratch-directory>/trope
git -C <scratch-directory>/trope show <commit>:py/ws_bot_edit.py        # post-move
git -C <scratch-directory>/trope show <commit>:dir-for-pywikibot/ws_bot_edit.py  # pre-move (earliest)
```

The move from `dir-for-pywikibot/` to `py/` happened at commit `fe60fa6c`,
and from `py/` to `py/ws/` at commit `02f78e90`.
