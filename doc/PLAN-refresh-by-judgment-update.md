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
5. **Not investigated: Ezekiel 36:15.** A read-only scan of all 964 stored pointed ketivs (723
   frozen, 236 reviewed, 5 editorial) for the five stress-helper configurations that
   `in/near-aleppo/census/stress_helper_census.txt` counts, run with this change applied, found no
   pointed ketiv with a stress helper that its qere lacks. At Ezekiel 36:15 the mismatch runs the
   other way: the qere וְגוֹיַ֙יִךְ֙ has a pashta stress helper, and the reviewed pointed ketiv
   has none.
