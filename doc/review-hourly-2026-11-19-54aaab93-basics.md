# Bounded MAM-basics hourly review, 2026-11-19 00:00 UTC

State: completed 2026-11-19; review only

Exact endpoint `63ee193d6ce4c23217c76be81c00df0aad8ddf43` -> `54aaab9300e1559c891275a547dd516a84207354` (32 paths).
Owned isolated committed checkout, home interpreters, sequential commands. Local slots and
processes were clear at admission; cross-machine ownership is unverified. Full commands,
logs, diagnostics and probes: [evidence ZIP](review-hourly-2026-11-19-54aaab93-basics-evidence.zip).

| Actual maintained command | Exit; wall time |
| --- | --- |
| `git diff --check 63ee193d6ce4c23217c76be81c00df0aad8ddf43 54aaab9300e1559c891275a547dd516a84207354` | 0; 0.017257 s |
| `owning Python -m black --check py/accgram/maqaf_nonfinal_accents_page.py py/accgram/printed_decalogue_koren_page.py py/accgram/ps17v14_mam_doc_notes_body.py py/accgram/telg_doc_notes.py py/author_site/stress_helper_comparison.py py/foi/dexi_stress_meteg_explanations.py py/foi/dexi_stress_meteg_translations.py py/foi/foi_finals.py py/intro_doc_audit/human_review.py py/mb_misc/printed_tradition.py py/near_aleppo/doc_choices.py py/near_aleppo/doc_daniel_sheva.py py/near_aleppo/doc_genesis_ketiv.py py/near_aleppo/doc_investigation.py` | 0; 0.614613 s |
| `owning Python py/main_near_aleppo.py --html` | 0; 26.287257 s |
| `owning Python py/main_foi_features_of_interest.py --foi args-foi-dexi-stress-meteg` | 0; 1.114872 s |
| `owning Python py/main_accgram.py generate-html-telg-doc-notes` | 0; 0.336267 s |
| `owning Python py/main_accgram.py generate-html-ps17v14-mam-doc-notes` | 0; 0.362287 s |
| `owning Python py/main_intro_doc_audit.py review` | 0; 2.192078 s |
| `owning Python py/main_authored.py gen-site --trust-surveys` | 0; 5.921199 s |
| `owning Python py/main_accgram.py generate-html-printed-decalogue-koren` | 0; 1.012199 s |
| `owning Python py/main_accgram.py generate-html-maqaf-nonfinal-accents` | 0; 5.856094 s |
| `owning Python py/main_test.py (12 modules in commands.json) -q -ra` | 0; 125.067070 s |

All maintained commands above pass and leave exact committed output, including the
hand-run Introduction review at its unchanged historical source pin. Black covers 14 changed
Python files. The repository selection passes **40 tests, no skips, in 124.83 s pytest /
125.067070 s wall**. It covers prose/mark order/NFC/transliteration, shared styles/links,
near-Aleppo note behavior and the Koren/maqaf pages. No broad mega or full suite ran.

Additional probes use the prescribed runner from this source root: **12 passed**, exit0,
1.260786 s wall. They compare both helper rendering routes, literal markup/quote escaping,
capitalization, multiline text, part/most qualifications and exact Hebrew/title values;
preserve trusted surrounding markup; and verify the concrete tree caller does not double-wrap.
The shared hover is byte-identical to the old stress helper's constant. The stress-page bytes
are unchanged, and gen-site reproduces all its other authored pages. All nine published pages
using the class have one-level shared hovers and the same rule through their actual inline or
imported stylesheets. No visual/browser result is inferred from these checks.

A synthetic survey change shows the narrowed Koren pin ignores a poetic-only mun-mun case,
while the maqaf-page pin rejects that exact case; a prose mutation still fails Koren's pin.
The committed survey and all MAM/stress-helper source inputs remain unchanged. This verifies
the precise implemented boundary, not manuscript precedent or new corpus research.

The independent preservation helper passes **67 assertions** (0.286962 s): all 12 changed
HTML documents retain their non-hover element/attribute structure, pointed display text,
Hebrew table contents and scripts. All data changes in human-review.json are confined to ten
translations, with quoted Hebrew, IDs, disposition, order and all other fields exact. Within
the hover sweep, 50 visible term occurrences have49 hovers and one explicit definition without
one. The Koren page's own title/heading are outside this translation scope. Original reviewer
serializer/wrapping/scope diagnostics are retained; no product restoration or repair needed.

No consequential introduced defect established. Concrete-noun wording, publisher-title
Haketer/k exception and Introduction-sigil interpretation are recorded owner choices, preserved
without new editorial/source adjudication. Owner 67/25/20/32 checks remain attributed, not added
to our counts. No source acquisition, configuration deployment, browser/Windows, fonts,
baseline acceptance or frozen research work ran; historical gaps and HTML findings remain.

Frozen sources: [shared helper](https://github.com/bdenckla/MAM-basics/blob/54aaab9300e1559c891275a547dd516a84207354/py/mb_misc/printed_tradition.py), [Koren pin](https://github.com/bdenckla/MAM-basics/blob/54aaab9300e1559c891275a547dd516a84207354/py/accgram/printed_decalogue_koren_page.py).

Parent `373010a0162ad19332f4a6fd37925c8abf95eaed` and every previous status byte/finished receipt remain intact.
Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; last independent broad-tested stays
November 18 nightly `8c2c3378487c9587659cd0b4a8f3db4690dbcf08`. All historical gaps and source/browser/native/font
limits remain. Only the established isolated receipt branch changes; no main/shared
integration, PR, deployment/dispatch, schedule or installed configuration change. Remote
parent/scope/bytes and owned-worktree/slot cleanup are verified at closeout.
