# Plurals of romanized Hebrew words

Use a context-specific English plural noun in authored prose: "maqaf marks", "meteg marks",
"three alef letters", "pointed ketiv forms", "qere readings", or "aliyah portions".
This preference includes apparatus and other Hebrew nouns, not just letter/mark names.
The rule lives in the `hebrew-prose` skill's
[terminology reference](../dot-claude/skills/hebrew-prose/references/terminology.md).
Ben's 2026-10-13 exception preserves the entire Yeivin ITM adaptation's plural conventions,
including his adapted prose and footnotes; the
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
ketiv/qere, masorah, aliyah, parashah, setumah/petuḥah, and ḥilluf. Suggested nouns are
editorial defaults, not automatic substitutions; the sentence decides forms, readings, words,
notes, portions, sections, or another appropriate noun.
Matching recognizes Latin diacritic variants, English `s`/`es` and appended Hebrew `im`/`ot`,
as well as suffixes separated from italic names by inline tags or thin/hair spaces. Latin
folding is for lookup only; no source or Hebrew text is normalized. Suggestions preserve the
spelling of the found name. Ordinary English tails such as "dots", "vowels" and "helpers"
are allowed. Ambiguous English words such as "sins", "bets" and "nuns" require a nearby
explicit Hebrew/letter context to be flagged.
Names with an intrinsic ending, such as `gershayim`, `qamats`, or `qubuts`, are left alone;
the check detects an appended ending, not any word ending in those letters.

The lint checks visible prose and `alt`, `title`, `aria-label` and `aria-description` text.
It excludes code/preformatted examples, scripts/styles, Hebrew and phonetic transcription
content tagged `lang="hbo..."`, and quotation elements (`q` and `blockquote`). English
prose attributes remain checked even on a Hebrew element. IDs, classes, URLs and data
attributes are outside the prose scan; standalone path/identifier forms are also ignored.
The whole `gh-pages/yeivin-itm/` directory and `gh-pages/yeivin_itm.html` are exempt.

An unmarked verbatim source phrase can have a narrow path-and-phrase exception in
`_QUOTATIONS`. Its entries preserve UXLC's "five yods" note in `gh-pages/clc/Proverbs.html`
and Holman's five "Merekhas/MEREKHAS" passages without exempting other prose on those pages.
New local quotations may instead use
`data-hebrew-plural-ok="reason"` on their containing element; a reason is required. Use
these for actual source wording or an established exception, not to suppress authored prose.

This is a vocabulary lint, not a universal detector of romanized Hebrew. Unlisted spellings or
irregular plural forms, arbitrarily split names, and unrendered Python
comments/docstrings are outside its coverage. Unmarked source quotations still need human
classification. Generated pages are covered after regeneration, including by the normal
mega/nightly workflow; no generator strings or technical identifiers are rewritten by lint.

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

The broader follow-up removes an unintended letter/mark-only scope restriction. It changes
69 additional plural-word occurrences across ten pages. These counts are individual plural
words; for example, one `parashot setumot` phrase contributes two words. Across both passes,
83 authored occurrences change on eighteen distinct pages.

| Before | After in context | Additional HTML occurrences | Authoritative source |
| --- | --- | ---: | --- |
| ketivs | pointed ketiv forms | 5 | `py/near_aleppo/doc_choices.py` |
| ketivs | pointed ketiv forms | 1 | `py/near_aleppo/doc_page.py` |
| qeres | qere forms | 1 | `py/near_aleppo/doc_changes.py` |
| qeres | qere readings | 1 | `py/near_aleppo/doc_genesis_ketiv.py` |
| masorot | masorah notes | 1 | `py/accgram/almost_errors_oddities.py` |
| aliyot / Aliyot | aliyah portions / Aliyah Portions | 15 | `py/mb_author/author.py` substitutions and `py/author_misc/notes_on_aliyot.py` title |
| aliyot | aliyah portions | 1 | `py/author_misc/mp_body_shared.py`, through `py/mb_author/author.py` |
| aliyot | aliyah portions | 1 | `py/mwd/mwd_write_index_dot_html.py` |
| aliyot | aliyah portions | 1 | `py/author_site/site_data.py` |
| parashiyot | parashah sections | 18 | `py/mb_author/author.py` substitutions, consumed by `py/author_misc/notes_on_aliyot.py` |
| parashot / Parashot | parashah, in parashah setumah/petuḥah sections | 11 | `py/osis/osis_index_html.py` |
| setumot | setumah, in the same compound noun phrases | 6 | `py/osis/osis_index_html.py` |
| petuḥot | petuḥah, in the same compound noun phrases | 7 | `py/osis/osis_index_html.py` |

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

Other raw candidate matches are syllables in the unchanged `gh-pages/phonetic-mam/tnkh/`
transcription data, not plural names. Their term counts are below (Latin diacritics retained as
found; fragments can coincide with a name plus an ending):

| Raw fragment | Occurrences in `gh-pages/phonetic-mam/tnkh/` |
| --- | ---: |
| ḥés | 52 |
| ḥets | 44 |
| béts | 20 |
| pés | 16 |
| ḥéts | 6 |
| ḥes | 5 |
| mémim | 4 |
| bets | 4 |
| nunim | 3 |
| vaus | 2 |
| pes | 1 |
| ḥetim | 1 |
| téts | 1 |

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
Only the eighteen intended HTML pages differ across both passes; generated JSON, Scripture,
other outputs, HTML tags/attributes, links and anchors remain unchanged. English nouns added
after romanized spans remain outside those spans, while the tag/attribute sequence stays intact.
