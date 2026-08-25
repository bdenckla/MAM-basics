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

### Issue 67: migrate deprecated כו"ק call sites to מ:כו"ק מיוחד — current
- **Purpose:** Migrate call sites of nine deprecated issue-67 כו"ק template
  names to `{{מ:כו"ק מיוחד|...|סוג=...}}`, where `סוג` is derived from the old
  template name without the `מ:` prefix.
- **Safety rule:** Hard preflight for `רווח=כן`; fail fast for manual handling.
- **Edit level:** Full cif2 AST traversal via candlers/vandlers/wandlers.
- **JSON files:**
  `in/mam-ws-bot-edits/issue-67-kuk-special-callsite-migration.json`

## How to look up the original code

All old versions live in the predecessor repo:

```
cd ~/GitRepos/trope.old.use-mam-basics-instead
git show <commit>:py/ws_bot_edit.py        # post-move
git show <commit>:dir-for-pywikibot/ws_bot_edit.py  # pre-move (earliest)
```

The move from `dir-for-pywikibot/` to `py/` happened at commit `fe60fa6c`,
and from `py/` to `py/ws/` at commit `02f78e90`.
