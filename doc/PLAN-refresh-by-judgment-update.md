# Updates to the refresh-by-judgment plan

State: open; first entries 2026-10-07.

Every entry here supplements `doc/PLAN-refresh-by-judgment.md`, which is left as written apart
from its line-4 pointer to this file.

## Noticed items 3 and 4 resolved, 2026-10-07

1. **Item 4, the good-ending template: resolved in `c17312be`.** Asked whether that template
   should join a declared group, Ben replied that he would rather not spend his time on "being
   bothered with questions like this". The session then did what wave 6, item 2 says: the
   verifiers read the books' good endings as well as the verses, and the good-ending template
   joins `mp.plus.templates.other.set`'s declared list, so `all-groups-cover-all-observed`
   covers the whole corpus. No page changed.
2. **Item 3, the transcriptions' comments: corrected in the commit that adds this entry, on
   Ben's instruction ("sure, go ahead and correct this").** The comments of
   `simtiq_dt_elyon.txt`, `koren_ex_taxton.txt` and `koren_dt_taxton.txt` now say that the
   reference states each vertical stroke's kind, since its faithful form has kept the legarmeh
   and narrow-sense paseq templates apart from wlc-utils#74 on. The Simanim Tiqqun's seven
   stated kinds are checked against the reference and agree with it, and the Koren pages'
   "[pasoleg]" states no kind, so the check has nothing there to compare. Those comments and
   the ones in `koren_ex_elyon.txt` and `koren_dt_elyon.txt` call the strands Wikisource
   strands rather than vendored ones.

## Noticed item 1, 2 Kings 14:7: resolved by Ben's decision, 2026-10-08

Recorded by Claude (Claude Opus 5.5, in the Claude desktop app) on 2026-10-08, New York time, in
the full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, in the commit that adds this entry, whose
parent is `ebaae10f`.

1. **The item.** The plan's "Noticed, not acted on" item 1 reads "**2 Kings 14:7** is outside this
   plan (Coordination, item 1)", and Coordination item 1 begins "Near-Aleppo's stored pointed
   ketiv at 2 Kings 14:7". The executing session wrote the promised prompt in its chat after
   pushing wave 2 (`9972e6c0`), but no session ran it, and the entry above, which resolved items 3
   and 4, left item 1 unmentioned.
2. **What the edition showed.** The pointed ketiv in the frozen record `BD-2Kings:14:7:0` was
   the form המֶ֙לַח֙, with a pashta on the last letter and a second pashta, the stress helper, on
   the mem of the stressed first syllable. The frozen inference took both pashtas from MAM's
   qere, מֶ֙לַח֙. MAM's note at this verse says that the Aleppo Codex has the form מֶלַח֙, with
   the final pashta alone, and near-Aleppo's phase 5 applies that reading to the qere and flags
   it. The edition therefore showed the two-pashta pointed ketiv as its main text and the
   one-pashta qere in ruby above it. Nobody in this work has consulted the codex image, so the
   one-pashta form rests on MAM's note.
3. **Ben's decision**, in this session: "Please make the pointed ketiv only have one pashta, the
   real pashta, i.e. the final one, not the stress helper."
4. **The change.** The record's value is now המֶלַח֙, the ketiv's unpointed he followed by
   near-Aleppo's qere exactly. Its `tmpl_params` are unchanged, since that qere did not change.
   `py/main_near_aleppo.py --refresh-note-review` gave the ledger entry of the note at this verse,
   in `in/near-aleppo/doc-note-review.json`, a new evidence hash and reset its review to pending.
   That entry's framed-mam review was then restored unchanged: its three clauses remain MAM
   context, and none of its reasons depends on the pointed ketiv's marks. The dataset changes only
   in this pointed ketiv in `out/near-aleppo/plus/BC-Kings.json`, and the edition only in its two
   copies in `gh-pages/near-aleppo/edition/BD-2Kings.html`; `in/near-aleppo/build-populations.json`
   is unchanged. `py/main_near_aleppo.py --check` and `--punctuation-review --check` pass, and so
   do the six tests of `py/tests/test_near_aleppo.py`, `py/tests/test_near_aleppo_note_content.py`
   and `py/tests/test_near_aleppo_clc_style.py`.
5. **Ezekiel 36:15: kept as it is, by Ben's decision the same day.** A read-only scan of all 964
   stored pointed ketivs (723 frozen, 236 reviewed, 5 editorial) for the five stress-helper
   configurations that `in/near-aleppo/census/stress_helper_census.txt` counts, run with this
   change applied, found no pointed ketiv with a stress helper that its qere lacks. At Ezekiel 36:15
   the mismatch runs the other way: the qere וְגוֹיַ֙יִךְ֙ has a pashta stress helper on its first
   yod, and the reviewed pointed ketiv, which has the patah on the yod and the hiriq on an
   artificial carrier, has only the final pashta. Ben read the codex image: "there's only one
   pashta in the manuscript. It is, of course, the word-final one, i.e. the real pashta." He
   decided: "So, in summary, I stand by near-aleppo's choices. this is one case where the pointed
   qere, justifiably, has a mark not present in the pointed ketiv." His reason is that
   near-Aleppo's pointed qere shows the qere as the naqdan would point it if it stood in the body
   text, an editorial decision on which, he notes, reasonable people could differ.

   Both forms follow the codex's convention as Yeivin §239 describes it, which phase 3's sub-rule
   1 applies to MAM's text: the pashta is repeated only where a letter stands between the two
   letters that would carry it. In the qere the second yod stands between them; in the ketiv only
   the letterless hiriq does. No body-text occurrence of this word can test the qere's form, since
   MAM has this plural only as the qere at Ezekiel 36:13, 36:14 and 36:15. In MAM's text, 20
   body-text pashta atoms have penultimate stress and end in a yod carrying the stressed vowel, a
   second yod and a final letter, as Song of Songs 1:10's לְחָיַ֙יִךְ֙ does, and all 20 have the
   helper on the first yod; the 15 other body-text pashta atoms ending in two yods and a letter
   have final stress and no helper. Ten of the 20 are in surviving parts of the codex, and MAM's
   notes report no missing helper at any of those ten, though they report the codex without the
   helper, a letter standing between, at the seven places that phase 3's
   `_PASHTA_STRESS_HELPER_FOR_PHASE_5` names, among them 2 Kings 14:7. At Song of Songs 3:5, where
   a letterless hiriq stands between the two letters as in this ketiv, MAM's note says that the
   codex writes יְרוּשָׁלַ͏ִם֙ with a single pashta, which it calls the codex's method.

   Nobody has yet checked the 20 against the codex images. The ten in surviving parts of the codex
   are Deuteronomy 30:20, Joshua 9:4 and 9:13, 1 Samuel 25:37, 2 Samuel 13:28, Isaiah 58:11,
   Jeremiah 35:8 and 48:33, Song of Songs 1:10, and 2 Chronicles 2:14; the ten in lost parts are
   Genesis 49:11 and 49:26, Exodus 26:3, Deuteronomy 5:14, 14:26, 15:15, 24:18 and 28:13, and
   Nehemiah 2:1 and 5:15. These figures come from a throwaway scan on 2026-10-08 of MAM-parsed-plus
   at `9a456f5b`, through the edition projection of `py/near_aleppo/census/`, with coverage from
   its `nusach_codex_extant`, which counts a partly surviving verse as surviving.
   `py/main_verse_links.py <book> <c:v>` prints a verse's links, including its Aleppo Codex
   links at mgketer.org and masoretica.org.
