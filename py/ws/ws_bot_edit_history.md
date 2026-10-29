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

### Holman meteg rollout: 29 meteg marks removed, one added
- **Purpose:** Apply the thirty MAM suggestions Daniel Holman sent that differ
  from their Aleppo Codex comparison form in meteg marks alone. Twenty-nine take a
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

### Post-maqaf ketiv/qere: four calls given the qere-first template
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
  The two ketiv-first `{{מ:כו"ק מיוחד}}` calls between two maqaf marks, at Isaiah 26:20
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

### Explicit silluq position: two source annotations, 2026-10-12

- **Purpose:** Wrap the existing `נוסח` targets at 1 Kings 7:37 and Job 4:12
  with `מ:סילוק לפני געיה`. Parameter 1 preserves the full marked atom;
  parameter 2 gives its letters with one U+05BD identifying silluq. Sof pasuq
  remains outside both wrappers. The existing detailed source notes are unchanged.
- **Authorization and sequencing:** Ben told Codex to proceed on 2026-10-12,
  confirmed removing later meteg marks in Sefaria/AJF, and then confirmed that the
  post-stress-meteg survey should follow both explicit annotations. Public support
  was pushed at `efb2c407` before the template or chapter annotations were saved.
  The template and its documentation were created at revision 3088395; the
  introduction appendix's roster entry was added at revision 3088396. Exact live
  expansion of both calls equalled the original atoms, including marks and spacing.
- **Saving run:** 1 Kings 7, revision 3084789 → 3088397; Job 4, revision
  3084788 → 3088398. Each chapter has exactly one new call. The saving artifacts
  and downloaded chapter mirrors equal the two `--no-save` previews exactly.
- **Source scope:** The two existing notes identify the earlier stroke as silluq
  and the later stroke as meteg. This run encodes those source-note readings and
  makes no new manuscript judgment.
- **Post-run download:** Refetched the two chapters and all 36 declared special
  pages. The special-page mirror had no tracked difference. The observed-template
  documentation guard then required adding the new name to its actual corpus
  inventory; all 57 MAM-parsed claims passed after that update.
- **One-shot:** The exactly-once `old` guards describe the pre-edit text. Verify
  this run through its saved artifacts and mirror equality, rather than re-running
  the replacement specification after its targets have changed.
- **Specification:** `in/mam-ws-bot-edits/silluq-before-meteg.json`;
  run artifacts `.novc/mam-ws-bot-real-runs/20261012-155640-850657-0400/`.

### Exodus note links: 17:16 unbolded and given JSTOR's public address, 26:7 templated again, 2026-10-13

- **Purpose:** Let MAM-parsed read two notes that the Wikisource user Dovi had edited.
  Exodus 17:16's note, extended on 2026-10-12 with a paragraph citing Yuval Weiss's
  article in Leshonenu, gave that link's text as `'''לשוננו'''`. The template parser
  rejects raw `'''` (`py/ws/ws_tmpl_parser.py`), so that day's refresh stopped there. The
  parser's advice, `{{מודגש}}`, cannot be followed inside the link: both templates have
  rank 7 in the nesting normal form, which never nests one rank-7 template in another. So
  the bolding was removed. The same link went through a library proxy,
  `https://www-jstor-org.mgs.oranim.ac.il/journal/lesonenu`; it now gives JSTOR's public
  address, `https://www.jstor.org/journal/lesonenu`. Exodus 26:7's note, reworded on
  2026-09-29, had gone back to the bare `[URL text]` link that the note-link run of
  2026-09-27 templated. MAM-parsed keeps such a link as plain text, so MAM-with-doc would
  show its brackets and URL; the note is `{{מ:קישור בהערה|URL|text}}` again, exactly as
  that run's `new` wrote it.
- **Authorization:** Ben asked for all three changes, and for the bot to make them, on
  2026-10-13. A Claude Code session wrote the file and ran it the same day.
- **Saving run:** Exodus 17, revision 3088235 → 3088583; Exodus 26, revision 3085723 →
  3088584.
- **Safety rule:** each `old` string occurred exactly once in the page text that the
  stopped download had captured at revisions 3088235 and 3085723. The `--no-save` dry
  run's edited chapters equalled that capture with the replacements applied, codepoint
  for codepoint. The saving run's chapters equalled the dry run's, and the post-run
  download equalled both.
- **Post-run download:** Refetched the two chapters and all 36 declared special pages.
  The special-page mirror had no tracked difference, and the reparse of Exodus passed all
  59 MAM-parsed claims.
- **One-shot:** every `old` describes the pre-edit text. Confirmed 2026-10-13, immediately
  after the run: a `--no-save` re-run raised on Exodus 17.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/exodus-17-26-note-links.json` and its selector,
  `exodus-17-26-note-links.chapters.json`; run artifacts
  `.novc/mam-ws-bot-real-runs/20261013-102232-324529-0400/`.

### Introduction note templates: every `נוסח` call given `2=`, 2026-10-18

- **Purpose:** Ben asked on 2026-10-18 for every `{{נוסח}}` call in MAM's introduction to
  take the form MAM's chapter pages use, the note as parameter 2 written `2=`, as a
  uniform policy "rather than be 'clever'" about which notes need it. The template reads
  only parameters 1 and 2, and shows parameter 2 only in the note-display edition; the
  chapter pages took this form in the note-display edits of May 2024, and the
  introduction's calls predated them. Of its six calls, four gave the note as one
  argument, two positional and two named `א=`. Two split one note over several
  arguments, chapter 2's Job 11:6 example and chapter 3's Genesis 35:22 example; the run
  joined their arguments in order with `{{ש}}`, the chapter pages' separator, and the
  joined Job 11:6 call equals MAM's own note at that verse.
- **New mode:** the chapter bot selects only chapters, so this run added
  `main_ws_bot.py intro` (`py/subcommands/ws_bot_intro.py`), which selects introduction
  pages by their `in/mam-ws-intro/manifest.json` keys and has the chapter bot's login
  check, dry run and post-run download (`fr-ws-intro`).
- **Saving run:** chapter 2, revision 3087893 → 3090585 (four calls); chapter 3, 3087744 →
  3090586 (one); chapter 4, 3088866 → 3090587 (one).
- **Safety rule:** a script cut each `old` from the live wikitext of all 13 pages, read
  just before the run; each occurs exactly once, and each `new` parses as exactly
  parameter 1 and `2=`. The `--no-save` dry run's pages equalled that capture with the
  replacements applied, codepoint for codepoint; the saving run's pages equalled the dry
  run's, and the refreshed mirror's pages equalled both.
- **Post-run download:** the refresh also brought in four of Avi's edits made since the
  previous mirror commit: a dagesh in a ketiv-list form at Ecclesiastes 9:4 (chapter 4,
  revision 3088866), nun's dagesh in the ketiv forms at Ezekiel 14:14 and 14:20, as
  MAM-basics#307 asked (chapter 5, revision 3088859), and a phrase after the Heidenheim
  Psalms entry (appendices, revision 3089143).
- **One-shot:** every `old` describes the pre-edit text. Confirmed 2026-10-18,
  immediately after the run: a `--no-save` re-run raised on chapter 2's first `old`.
- **Follow-up:** MAM-basics#323's before and after now show the `2=` form.
- **Edit level:** Raw page text string replacement, page-targeted.
- **JSON file:** `in/mam-ws-bot-edits/intro-nusach-2-prefix.json`; run artifacts
  `.novc/mam-ws-bot-intro-runs/20261018-121729-392296-0400/`, dry run
  `.novc/mam-ws-bot-intro-runs/20261018-121701-421342-0400/`.

### Ketiv forms with two vowels on one letter: a CGJ between the vowels, 2026-10-28

- **Purpose:** Give a CGJ (U+034F, COMBINING GRAPHEME JOINER) to nine atoms whose letter had
  two vowels with no CGJ between them: five ketiv forms in four documentation notes, and the
  four entries of chapter 5 of MAM's introduction that quote them. MAM's Scripture text has a
  CGJ between the two vowels of every such letter. At Ezekiel 14:14, 14:20 (two forms) and 28:3
  the notes' א-כתיב forms of דנאל and מדנאל have a ḥiriq and a tsere on the nun, and the notes
  give that order: "חיריק, צירה, ... בסדר הזה". At 2 Kings 18:27 the note's combined form has a
  sheva and a tsere on its yod. Each CGJ follows the ḥiriq or the sheva, and nothing else
  changed.
- **Framing:** Ben asked on 2026-10-28 that the change be framed "as making fragile words
  robust", not as a font fix. Normalization is not what reorders these four atoms: Unicode's
  combining classes already put sheva (10) and ḥiriq (14) before tsere (15), so NFC and NFD leave
  them as they are, and `is_fragile` in `py/mb_cmn/uni_norm_fragile.py` calls them robust.
  HarfBuzz's own order for Hebrew points puts tsere first, so Taamey D 1.1, adopted in
  `229ce922`, showed the tsere to the right of the ḥiriq, against the notes. A CGJ keeps the
  stated order under any normalization or shaping engine.
- **Authorization:** On 2026-10-28 Ben chose the CGJ, asked that BdencklaBot insert it from a
  top-level session, and accepted a literal CGJ with nothing else changed: "Yes, given your
  survey, that seems like the best course of (non-precedent-changing) action." A Claude Code
  session wrote the files and ran them the same day, after his go-ahead for the saves.
- **Literal code point:** every CGJ already in a documentation note, on five note lines of
  `in/mam-ws/`, and in the mirrored introduction is the literal code point; templates insert
  CGJs only into the Scripture text.
- **Saving runs:** 2 Kings 18, revision 3010616 → 3098808; Ezekiel 14, 2988050 → 3098809 (three
  CGJs); Ezekiel 28, 3001796 → 3098811; introduction chapter 5, 3088859 → 3098815 (four CGJs).
- **Safety rule:** a script cut each `old` from the live wikitext of the four pages, read before
  the dry runs and again, byte for byte the same, just before the saves; each `old` occurs
  exactly once, and each `new` is its `old` with one CGJ. The `--no-save` dry runs' pages
  equalled that capture with the replacements applied, code point for code point, and differed
  from it by the nine CGJs alone. The saving runs' pages equalled the dry runs', and the post-run
  downloads equalled both. In MAM-parsed the nun now has dagesh, ḥiriq, CGJ, tsere and its
  accent, and the yod sheva, CGJ and tsere.
- **Post-run downloads:** the chapter run refetched the three chapters and all 36 declared special
  pages, and the reparse of Kings and Ezekiel passed all 59 MAM-parsed claims. Three special
  pages, none of them saved by this run, brought in edits by others since the previous download:
  `decalogue`, revision 952886 → 3088871 (2026-10-15), which now points to the introduction's
  chapters 2 and 3, links the English page and changes six Onkelos link anchors; `decalogue-en`,
  2980688 → 3088722 (2026-10-14), which links the Hebrew page and drops three header links; and
  `deuteronomy-32`, 3079372 → 3092658 (2026-10-19), whose note at 32:34 now says the full
  spelling has a vav, not a yod. The chapter mirror of Deuteronomy 32 keeps the earlier note,
  since this run downloaded only the chapters it saved. The introduction run's refresh brought in
  five pages' edits by others: chapter 1, revision 3095761 (2026-10-23), which rewords the
  chapter's opening and corrects a Job reference and an mgketer link; chapters 2 and 3 and the
  Westminster page, 3092676, 3092677 and 3092678 (2026-10-19), which correct the spelling
  וסטמינסטר; and the appendices, 3092644 (2026-10-19), which correct a date.
- **One-shot:** every `old` describes the pre-edit text. Confirmed 2026-10-28, immediately after
  the runs: `--no-save` re-runs raised on 2 Kings 18 and on chapter 5's first `old`.
- **Near-Aleppo:** two near-Aleppo records quote these notes, so the refresh's mega stopped at
  its near-Aleppo build. `acbb7b5f` gave the three Ezekiel guards of `_REVIEWED_ORPHAN_VALUES`,
  in `py/near_aleppo/phase5_readings.py`, their source forms with the CGJ, and carried four
  reviewed rows of `in/near-aleppo/doc-note-review.json` across, those of 2 Kings 18:27's
  second note and the three Ezekiel notes, their quoted clauses gaining the CGJ. Ben's
  representations and the rows' dispositions are unchanged.
- **Left as they are:** `doc/near-aleppo-avi-ketiv-investigation.html`, which quotes the
  introduction's earlier forms verbatim; and chapter 5's six other letters with two vowels and
  no CGJ, outside the scope Ben confirmed: Proverbs 6:24's lamed, and five ḥataf-ḥiriq forms, a
  sheva then a ḥiriq, at 1 Kings 17:11, Psalms 14:1 (two) and Psalms 53:2 (two).
- **Edit level:** Raw page text string replacement, chapter- and page-targeted.
- **JSON files:** `in/mam-ws-bot-edits/note-ketiv-two-vowels-cgj.json` and its selector,
  `note-ketiv-two-vowels-cgj.chapters.json`, and
  `in/mam-ws-bot-edits/intro-ketiv-two-vowels-cgj.json`; run artifacts
  `.novc/mam-ws-bot-real-runs/20261028-153831-542909-0400/`, dry run
  `.novc/mam-ws-bot-real-runs/20261028-152208-478727-0400/`, and
  `.novc/mam-ws-bot-intro-runs/20261028-154221-003122-0400/`, dry run
  `.novc/mam-ws-bot-intro-runs/20261028-152218-893094-0400/`.

### A CGJ that separated no marks, removed from the note on Numbers 7:60, 2026-10-29

- **Purpose:** Remove one CGJ (U+034F, COMBINING GRAPHEME JOINER) that separated no marks.
  MAM's documentation note on Numbers 7:60 gives two forms of the atom בנימן. In the Leningrad
  Codex's form, after `ל!=`, the mem has an atnaḥ, a CGJ and a ḥiriq, and that CGJ keeps the
  order the note states. The next form, for the sigil ש, which the note says lacks the ḥiriq
  ("חסר חיריק"), had the same atnaḥ and CGJ followed directly by the final nun: a copy of the
  first form with its ḥiriq deleted. That CGJ stood between a mark and a letter, so it did
  nothing, and removing it changes nothing visible.
- **Framing:** a code point that does nothing. Ben, 2026-10-28, on hearing of it: "Is it about a
  dangling CGJ not separating any marks? If so, horrendous!" A census of the repository found
  it the only CGJ in MAM's text without a mark on each side. `py/tests/test_cgj_between_marks.py`,
  committed after this run's refresh, checks the mirrors and the products for any other.
- **Authorization:** Ben said on 2026-10-29 to carry out the plan that included this run ("Yes,
  after Phase 3"). He then chose to run this edit alone ("Numbers 7:60 only"), holding back a
  change to the note on Deuteronomy 3:22, which Dovi had revised that morning, and gave the
  go-ahead for the save: "Yes, save it". A Claude Code session wrote the files and ran them the
  same day.
- **Saving run:** Numbers 7, revision 2987710 → 3099098.
- **Safety rule:** a script cut `old` from the live wikitext of revision 2987710, checking that
  it occurs exactly once and holds exactly one CGJ, between HEBREW ACCENT ETNAHTA and HEBREW
  LETTER FINAL NUN; `new` is `old` without it. The `--no-save` dry run's page equalled that
  capture with the replacement applied, code point for code point, and differed from it on one
  line by the CGJ alone. Just before the save the live page was byte for byte the capture. The
  saved revision and the post-run download equal the dry run's page.
- **Post-run download:** refetched Numbers 7 and all 36 declared special pages, none of which
  had changed since the previous download, and the reparse of Numbers passed all 59 MAM-parsed
  claims. In the mirror, `out/mam-ws-parsed-fmt-2/` and MAM-parsed, the note's ש form lost the
  CGJ and nothing else changed. The note's Leningrad Codex form keeps its CGJ, now the only one
  in Numbers.
- **One-shot:** confirmed 2026-10-29, immediately after the run: a `--no-save` re-run raised
  "Expected 1 occurrence".
- **Near-Aleppo:** no record of `in/near-aleppo/doc-note-review.json` quotes this note.
- **Left as they are:** `doc/intro-doc-audit/notes.json`, a record pinned to its source commit,
  which quotes the note with the CGJ; and the held change to Deuteronomy 3:22's note.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/note-numbers-7-60-dangling-cgj.json` and its selector,
  `note-numbers-7-60-dangling-cgj.chapters.json`; run artifacts
  `.novc/mam-ws-bot-real-runs/20261029-103358-664928-0400/`, dry run
  `.novc/mam-ws-bot-real-runs/20261029-100909-255431-0400/`, and the one-shot re-run
  `.novc/mam-ws-bot-real-runs/20261029-103519-818386-0400/`.

### The tav's ḥiriq before its sheva in the note on Deuteronomy 3:22, 2026-10-29 — current

- **Purpose:** Clause 2 of MAM's documentation note on Deuteronomy 3:22 gives the Leningrad
  Codex's form of תיראום, after `ל?!=`, with a ḥataf-ḥiriq, its tav having a sheva and then a
  ḥiriq. Ben read the codex's page F100B on 2026-10-28, as the dangling-CGJ plan records him:
  "the xiriq comes before the sheva. So that is what MAM should have (with CGJ) in its note,
  and it should also express this in plus notation, and it should also mention it in Hebrew
  prose". The edit gives the form in plus notation, `תִּ+תְּירָא֑וּם`, and in a packed form
  whose tav has a ḥiriq, a dagesh, a CGJ and a sheva, and calls the mark a reversed
  ḥataf-ḥiriq, with the prose "דהיינו החיריק מימין לשווא". The rest of the clause is Dovi's
  revision 3099093 of that morning, unchanged, including his conclusion that the sheva-like
  mark is a blurred meteg stroke.
- **Authorization:** Ben held this edit back from the Numbers 7:60 run and then dropped it,
  having taken Dovi's revision to abandon the ḥataf-ḥiriq. Once he saw that clause 2 keeps it,
  he chose to revive the edit as prepared, and gave the go-ahead for the save: "Yes, complete
  the task, edit wikisource, then download it, whatever you need to do, get this task done!"
  A Claude Code session wrote the files and ran them the same day.
- **Saving run:** Deuteronomy 3, revision 3099093 → 3099130.
- **Safety rule:** the edit's `old` occurs exactly once in revision 3099093. Two `--no-save`
  dry runs, the second just before the save, gave the same page: the mirrored chapter with the
  replacement applied, differing from it on verse 22's line alone. The saving run's page and
  the post-run download equal the dry runs'.
- **Post-run download:** refetched Deuteronomy 3 and all 36 declared special pages, none of
  which had changed since the previous download, and the reparse of Deuteronomy passed all 59
  MAM-parsed claims.
- **Edit level:** Raw page text string replacement, chapter-targeted.
- **JSON files:** `in/mam-ws-bot-edits/note-deuteronomy-3-22-reversed-hataf-hiriq.json` and its
  selector, `note-deuteronomy-3-22-reversed-hataf-hiriq.chapters.json`; run artifacts
  `.novc/mam-ws-bot-real-runs/20261029-150031-401070-0400/`, dry runs
  `.novc/mam-ws-bot-real-runs/20261029-145140-988360-0400/` and
  `.novc/mam-ws-bot-real-runs/20261029-150007-117426-0400/`.

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
