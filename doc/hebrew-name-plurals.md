# Plurals of romanized Hebrew words

Use a context-specific English plural noun in authored prose: "maqaf marks", "meteg marks",
"three alef letters", "two tsinnor accents", "two qere words", or "aliyah portions".
This preference includes apparatus and other Hebrew nouns, not just letter/mark names.
The rule, with the table of default nouns that Ben approved on 2026-10-14, lives in the
`hebrew-prose` skill's
[terminology reference](../dot-claude/skills/hebrew-prose/references/terminology.md).
Ben's 2026-10-13 exception preserves the entire Yeivin ITM adaptation's plural conventions,
including his adapted prose and footnotes. His technical-page exception also preserves
`aliyot` throughout `notes_on_aliyot.html`. His later clarification chooses `parashot` over
`parashiyot` in our own prose, while preserving quotations and adaptations; the
[repository reference](../dot-claude/skills/hebrew-prose/references/mam-basics.md) owns its scope.

## Regular lint

`test_no_plural_inflections_of_hebrew_names` in `py/tests/test_prose_conventions.py` reads
every tracked `gh-pages/**/*.html`, including HTML at the deploy root. It is automatically
discovered by the normal `py/main_test.py` suite, which the existing nightly review runs.
No separate schedule or test registry is needed. To run this check alone from a full clone:

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_prose_conventions.py -k plural -q
```

A linked worktree uses its home clone's interpreter by absolute path. Failures give the
file, original HTML line and suggested noun phrase. Correct a generated page's authoritative
source and regenerate it; hand-maintained HTML is edited directly.

`py/mb_cmn/hebrew_name_plurals.py` derives its vocabulary from the maintained short Unicode
names in `pydiff_mm.diff_mm_uni_name`, the letter/point/accent and poetic names in
`mb_diff_mpu.describe_diff`, and full Hebrew Unicode names, plus explicit spelling aliases.
Small noun and irregular-plural tables cover the additional words found in this audit:
ketiv/qere, masorah, aliyah, parashah, setumah/petuḥah, and ḥilluf. The aliases ḥataf,
pasoleg and ta'am were added on 2026-10-14, after the previous day's sweep of authored prose
outside the pages had found their plurals by hand.
Suggested nouns follow the terminology reference's table: "letters" for a letter, "accents"
for an accent, "vowels" for a vowel point, "dots" for ḥolam, "words" for ketiv and qere, and
"marks" for any other mark, including legarmeh, ole and yored. Ḥiriq suggests both "vowels"
and "dots", which Ben accepts equally, and the homonyms segol, geresh and gershayim suggest
the noun of each sense. A compound's final component never overrides a full name's noun, so
"vavs" suggests "vav letters" rather than the noun of `ḥolam-ḥaser-for-vav`. Suggested nouns
are editorial defaults, not automatic substitutions; the sentence decides the noun.
Matching recognizes Latin diacritic variants, English `s`/`es` and appended Hebrew `im`/`ot`,
as well as suffixes separated from italic names by inline tags or thin/hair spaces. Latin
folding is for lookup only; no source or Hebrew text is normalized. Suggestions preserve the
spelling of the found name. Ordinary English tails such as "dots", "vowels" and "helpers"
are allowed. Ambiguous English words such as "sins", "bets" and "nuns" require a nearby
explicit Hebrew/letter context to be flagged.
Names with an intrinsic ending, such as `gershayim`, `qamats`, or `qubuts`, are left alone;
the check detects an appended ending, not any word ending in those letters.

The lint checks visible prose and `alt`, `title`, `aria-label` and `aria-description` text.
It excludes code/preformatted examples, scripts/styles, content tagged `lang="hbo..."`, and
quotation elements (`q` and `blockquote`). English
prose attributes remain checked even on a Hebrew element. IDs, classes, URLs and data
attributes are outside the prose scan; standalone path/identifier forms are also ignored.
The whole `gh-pages/yeivin-itm/` directory and `gh-pages/yeivin_itm.html` are exempt.
Phonetic MAM's chapter pages under `gh-pages/phonetic-mam/tnkh/` are exempt too: their only
English is navigation and the pronunciation controls, and their transcriptions carry no `lang`
attribute. Phonetic MAM's testsuite pages stay checked for their authored notes, although their
transcriptions are untagged too.
`_PAGE_TERM_EXCEPTIONS` permits only `aliyot` (case-insensitively) in
`gh-pages/MAM-with-doc/misc/notes_on_aliyot.html`. Other unwanted plurals on that page still
fail, and `aliyot` still fails on other pages. The source uses an explicit technical
substitution for it. `Parashot`/`parashot` are accepted in our own prose; `parashiyot`, like an
English plural of parashah, suggests `parashot` unless in a quotation or adaptation. The legacy
`$parashiyot` key renders the chosen `parashot` spelling without changing technical identifiers.

An unmarked verbatim source phrase can have a narrow path-and-phrase exception in
`_QUOTATIONS`. Its entries preserve UXLC's "five yods" note in `gh-pages/clc/Proverbs.html`
and Holman's five "Merekhas/MEREKHAS" passages without exempting other prose on those pages.
New local quotations may instead use
`data-hebrew-plural-ok="reason"` on their containing element; a reason is required. Use
these for actual source wording or an established exception, not to suppress authored prose.

The existing `py/tests/test_transliterations.py` separately checks the four approved rendered
spellings: `qeri` -> `qere`, `aliya` -> `aliyah`, `parasha` -> `parashah`, and `masora` ->
`masorah`. Those four aliases no longer belong to the plural vocabulary. Both checks share
the same HTML extraction and quotation/adaptation/technical-reference boundaries. The spelling
check flags singular forms and appended plural endings, with original file/line diagnostics;
its scope does not broaden the existing Python transliteration denylist. Five exact external
work-title phrases in `_SOURCE_TITLES` and the imported UXLC Genesis Masora-circle note in
`_QUOTATIONS` retain their source spellings without exempting other prose on those pages.
The exact maintained Unicode name `HEBREW MARK MASORA CIRCLE` also remains literal vocabulary.

All three retained `Ketib` uses in `urwotm_2_saying_the_quiet_part_out_loud.html` now have explicit
source-preservation markers in its generator: the apparatus transcription's paragraph, the
quoted reduction's span, and only the Latin term's emphasis in our explanatory gloss. The
third use is our gloss retaining a source term, not a verbatim quotation of the whole gloss.
The surrounding authored explanation remains checked. A focused test injects both a plural
and a nonstandard spelling inside and outside each of these actual marked regions.

This is a vocabulary lint, not a universal detector of romanized Hebrew. Unlisted spellings or
irregular plural forms, arbitrarily split names, and unrendered Python
comments/docstrings are outside its coverage. Unmarked source quotations still need human
classification. Generated pages are covered after regeneration, including by the normal
mega/nightly workflow; no generator strings or technical identifiers are rewritten by lint.
The separate spelling check is deliberately narrower: its four literal spellings and appended
endings are checked, but arbitrarily split names or unlisted spelling variants are not covered.

The recognition aliases are not prescribed house spellings. Pre-sweep whole-word HTML counts
were `ketib` three and `masora` nine; `qeri`, `aliya`, and `parasha` had no observed usage and
were speculative aliases. The three `ketib` occurrences remain in the BHS source contexts
described above. The final follow-up standardizes three authored `masora` occurrences: one
hand-maintained sigil explanation and the two generated Latin `masorah parva/magna` phrases.
The remaining six `masora` occurrences are five edition/chapter-title references and one
imported UXLC quotation. No replacement prose introduces the three speculative spellings.
Unicode names and technical `MASORA_CIRCLE`/`masora-circle` forms are separate from these
visible-prose counts and retain their exact values.

## Audit coverage and changes, 2026-10-13

The sweep used `fb5660216b38f2ad93fdfba50eaec9b6940dd6c9` as its committed baseline and
covered all 1,668 tracked gh-pages HTML files. It also inspected raw text/attributes/scripts,
actual Latin word and inline-suffix inventories, and traced authored matches to their sources.
The initial letter/mark pass changed fourteen authored occurrences across nine pages:

| Before | After | HTML occurrences | Authoritative source |
| --- | --- | ---: | --- |
| maqafs | maqaf marks | 1 | `gh-pages/MAM-simple/reading-mam-simple-json.html` (hand-maintained) |
| maqafs | maqaf marks | 3 | `py/accgram/printed_decalogue_strands.py` (one source occurrence, three Decalogue pages) |
| maqafs | maqaf marks | 3 | `py/accgram/maqaf_nonfinal_accents_page.py` |
| metegs | meteg marks | 4 | `py/foi/mtgmtg_explanations.py` |
| lameds | lamed letters | 1 | `py/author_site/post_stress_meteg_post_silluq_images.py` |
| oles | ole marks | 1 | `py/near_aleppo/doc_changes.py` |
| ga’yas | ga’ya marks | 1 | `py/accgram/ps17v14_mam_doc_notes_body.py` (authored English translation/gloss; original Hebrew retained) |

The broader follow-up removes an unintended letter/mark-only scope restriction. After Ben's
technical-page and preferred-plural clarifications, 54 additional word occurrences change
across ten pages: 36 English-noun corrections and 18 `parashiyot` → `parashot` substitutions.
These counts are individual plural words; for example, one `parashot setumot` phrase contributes
two words. Across both passes, 68 authored occurrences change on eighteen distinct pages.
The approved spelling follow-up adds three `masora` -> `masorah` changes, for 71 word
corrections on nineteen pages. The separate BHS source annotations change a twentieth HTML
file's markup without changing its visible text. Final verification compares against current
main `c0bd297bbaff781b8eeebd0fc9dfc03f750e3975`, preserving its independently restored
"Meteg after silluq" link; that owner's change is outside the sweep counts.
The extensive English-noun rephrasing of `notes_on_aliyot.html` was reversed at its authoritative
source. Its original `aliyot` wording and surrounding prose are preserved; the only difference
from its pre-sweep text is the chosen `parashiyot` → `parashot` spelling and incidental line
wrapping. Its technical context and the scale of editorial churn both motivated Ben's exception.

| Before | After in context | Additional HTML occurrences | Authoritative source |
| --- | --- | ---: | --- |
| ketivs | pointed ketiv forms | 5 | `py/near_aleppo/doc_choices.py` |
| ketivs | pointed ketiv forms | 1 | `py/near_aleppo/doc_page.py` |
| qeres | qere forms | 1 | `py/near_aleppo/doc_changes.py` |
| qeres | qere readings | 1 | `py/near_aleppo/doc_genesis_ketiv.py` |
| masorot | masorah notes | 1 | `py/accgram/almost_errors_oddities.py` |
| aliyot | aliyah portions | 1 | `py/author_misc/mp_body_shared.py`, through `py/mb_author/author.py` |
| aliyot | aliyah portions | 1 | `py/mwd/mwd_write_index_dot_html.py` |
| aliyot | aliyah portions | 1 | `py/author_site/site_data.py` |
| parashiyot | parashot | 18 | Existing `py/mb_author/author.py` placeholder, consumed by `py/author_misc/notes_on_aliyot.py` |
| parashot / Parashot | parashah, in parashah setumah/petuḥah sections | 11 | `py/osis/osis_index_html.py` |
| setumot | setumah, in the same compound noun phrases | 6 | `py/osis/osis_index_html.py` |
| petuḥot | petuḥah, in the same compound noun phrases | 7 | `py/osis/osis_index_html.py` |

| Approved spelling follow-up | After | HTML occurrences | Authoritative source |
| --- | --- | ---: | --- |
| masora qetannah | masorah qetannah | 1 | `gh-pages/MAM-with-doc/sigil-decoding.html` (hand-maintained) |
| masora parva / masora magna | masorah parva / masorah magna | 2 | `py/near_aleppo/doc_registers.py` |

Intentional remaining plural-name matches:

| Scope/source | Term | Occurrences | Disposition |
| --- | --- | ---: | --- |
| `gh-pages/yeivin-itm/yeivin_itm-318_344.html` / `py/yeivin_itm/substitutions.py` and content | gaʿyas | 5 | Entire adaptation exempt |
| Same page/source | methegs | 1 | Entire adaptation exempt |
| `gh-pages/yeivin-itm/yeivin_itm-345_357.html` / same adaptation sources | gaʿyas | 4 | Entire adaptation exempt |
| `gh-pages/yeivin-itm/yeivin_itm-376_393.html` / same adaptation sources | shewas | 6 | Entire adaptation, including Ben's footnotes, exempt |
| `gh-pages/clc/Proverbs.html` / imported UXLC note at Proverbs 8:35 | yods | 1 | Verbatim source note preserved |
| `gh-pages/holman/uxlc_corrections.html` / Holman source notes, suggestion and email | Merekhas | 4 | Literal source wording preserved |
| Same page/source | MEREKHAS | 1 | Literal source wording preserved |
| `gh-pages/yeivin-itm/yeivin_itm-318_344.html` / adaptation sources | ḥillufim | 2 | Entire adaptation exempt |
| `gh-pages/yeivin-itm/yeivin_itm-345_357.html` / adaptation sources | ḥillufim | 1 | Entire adaptation exempt |
| `gh-pages/yeivin-itm/yeivin_itm-376_393.html` / adaptation sources | ḥillufim | 1 | Entire adaptation exempt |
| `gh-pages/MAM-with-doc/misc/notes_on_aliyot.html` / explicit technical substitutions and original title | aliyot / Aliyot | 15 | Ben's technical-page exception; original prose preserved |

The audit's text extraction also found candidate matches in the unchanged Phonetic MAM
transcriptions under `gh-pages/phonetic-mam/tnkh/`: transcription syllables, and strings that
run the end of a Sephardic transcription into the start of the Ashkenazic one beside it. None
is a plural name, and the lint now exempts those pages, as “Regular lint” describes.

Ordinary English plurals and literal Unicode-name strings also remain unchanged. These
distinctions are why a blanket text replacement is inappropriate. No remaining authored prose
matches were found with this vocabulary; that is not a claim to detect every possible spelling.
The cited title's singular "Dages" and "Dageš", Hebrew book titles and the publisher name
Simanim keep their source forms. Ordinary English words such as Masoretes, rabbis and Levites
also remain unchanged. Filenames, placeholder keys (including `$aliyot` and `$parashiyot`),
CSS names and technical `ketivs`/`qeres` identifiers remain intact.

Focused regeneration used `py/main_accgram.py generate-html-printed-decalogue`,
`generate-html-printed-decalogue-simanim`, `generate-html-printed-decalogue-koren`,
`generate-html-maqaf-nonfinal-accents`, and `generate-html-ps17v14-mam-doc-notes`;
`py/main_foi_features_of_interest.py --foi args-foi-mtgmtg --single-threaded`;
`py/main_authored.py gen-site --trust-surveys` (unchanged tracked survey for this prose edit);
and `py/main_near_aleppo.py --html`. The follow-up also used `py/main_authored.py gen-misc`,
`py/main_authored.py gen-mam-parsed-docs` (all 59 claim checks passed),
`py/main_mam_with_doc.py`, and `py/main_accgram.py generate-html-almost-errors`.
The maintained `osis.osis_runner.almost_main` rendered the OSIS index with its XML export paths
redirected to ignored scratch, where the export was validated; the intentionally lagging
distributed OSIS files were not refreshed. No new command or prose framework was added.
Only the twenty intended HTML files differ in the final sweep. Generated JSON, Scripture,
other outputs, Hebrew marks, links, anchors and classes remain unchanged. Nineteen pages have
only the intended word corrections and incidental line wrapping, with identical tag/attribute
sequences. English nouns added after romanized spans remain outside those spans. The twentieth
page adds exactly three reason attributes and one neutral span for the BHS source protections;
its visible text and all existing tags/attributes are preserved. Both lints pass over the full
tracked HTML scope, with the acknowledged vocabulary and quotation-classification limits above.

Final focused verification: `py/main_test.py py/tests/test_prose_conventions.py
py/tests/test_transliterations.py py/tests/test_prose_mark_order.py -q` passed all ten checks.
After the exact Unicode-name exception, the three rendered-spelling/source-region checks were
rerun and passed. Black and `git diff --check` passed. A cumulative comparison against current
main verified all 71 intended word substitutions, exact Hebrew codepoint streams and HTML
structures/attributes, allowing only the three stated source markers and their neutral span.
The full mega and suite were intentionally deferred under the approved review/testing trial:
this prose-only change received focused regeneration and comparison while Ben worked.
