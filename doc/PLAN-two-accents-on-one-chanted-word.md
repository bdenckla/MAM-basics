# PLAN — two accents on one chanted word (prose)

**FROZEN 2026-08-11 by Ben's decision, with Phase 4 unstarted — and the freeze LIFTED 2026-08-17,
at `MAM-basics\doc\PLAN-evacuate-the-rest-of-wlc-utils.md`'s Phase 11, exactly where its own terms
said it would. This plan may be executed again; Phase 4 is still the next phase, parked until
someone runs it.** The reason for the freeze was outside this plan rather than in it: this plan
generates accgram pages, and the evacuation plan proved each of its own phases by regenerating
those same pages and requiring a zero diff — so a page edit landing mid-evacuation was
indistinguishable from a bug in the move. That plan named this one as its Precondition 1, "land or
freeze", and Ben chose freeze on 2026-08-11 while its Phase 0 was running; wlc-utils was fully
evacuated, and the whole evacuation plan closed, on 2026-08-17.

**Nothing is abandoned, and nothing needs re-deciding when this resumes.** Phase 4 is down to two
chanted words, and §10 settled how the exception for each is spelled:

- **ca8:6 שלה֥בתיה** — a merkha and a silluq on one atomic chanted word, the silluq being a silluq
  because the chanted word is the verse's last and stands immediately before sof pasuq. Ready to
  write: the search §10 waited on ran 2026-08-03 and found both Yeivin's ITM and Breuer's CoS
  silent, so the entry rests on a measured silence rather than on an assumed one.
- **ne8:7 ושר֥בי֣ה** — a merkha and a munaḥ, held on MAM-basics#215, a defect that leaves MAM with
  no legarmeh token anywhere. Still held, and the freeze changes nothing about it.

Read the rest of this file as it stands. §0 is still the right resume point and its instructions
are still correct.

---

Teach the prose checker that a chanted word normally has exactly one accent, and flag a chanted
word with two unless the pair matches a known, very restrictive pattern. The same rules apply to
an **atomic** chanted word as to a **maqaf compound**; this is a chanted-word rule, not a maqaf
feature.

Planning session 2026-07-28. **Phases 1 and 2 are implemented; Phase 3 was built and withdrawn.**
§7, §8 and §9 at the foot of this file are the three phase states, each saying what changed, what
was verified, which generated outputs moved and which deliberately did not. §9 is the current
one, and it is where **Phase 4 — promotion, the plan's actual goal —** starts from. (The pointer
here said "Phase 1" through the whole of Phase 2; a phase-end write-back has to update it or the
reader lands two phases back.)

**The deliverable of this plan is a rule in the checker, not a page.** Phase 3 rendered the
survey and was dropped for exactly that reason, along with a neighbouring page having widened
onto the same ground. §5's struck Phase 3 entry has the full account; read it before proposing
another rendering.

Every number below marked *(probe)* came from a scratch script run during planning, **not** from
a regenerated tracked artifact. Phase 1 re-derived all of them in
`py/accgram/chanted_word_accents.py`; the tables below are now annotated with what the real
module measures, and §7 lists every place the probe was wrong.

**The code this plan changes is in `../MAM-basics`, not in the repo this file sits in.** On
2026-08-01 the whole of `py/accgram/` moved to `~/GitRepos/MAM-basics/py/accgram/`, and wlc-utils
kept `in/`, `out/`, `gh-pages/`, `data/` and `doc/`. So **every `py/...` path below names a file in
MAM-basics** — the modules, `prose_scanner`, `lexical_validation`, `classify.py`, the PLY grammar
file, `main_accgram.py`, `py/tests/` — while every `in/`, `out/`, `gh-pages/` and `data/` path still
names one here. `MAM-basics/py/wlc_paths.py` is the resolver, and it is deliberately two-rooted:
the code root is `mb_cmn.paths.repo_root()` (MAM-basics), the data root is `wlc_data_root()`
(wlc-utils). The move has a plan of its own,
`MAM-basics/doc/PLAN-evacuate-python-from-wlc-utils.md`. **§0's resume instructions and §9's
closing "The exact next phase" are rewritten to say `MAM-basics/py/...`**, those being the parts a
reader actions; the hundred paths elsewhere are left as they were written, since rewriting history
to a spelling it never had buys no reader anything.

**A bare `#NN` in this file means a wlc-utils issue** — #82, #85, #86 and #87 all do. MAM-basics
has a tracker of its own now, with numbers overlapping wlc-utils' 1–88, and this plan is read by
people working in MAM-basics, so the citations are ambiguous where they were not. They are
deliberately not mass-prefixed: MAM-basics' `CLAUDE.md` records that wlc-utils' `doc/` was left
alone on purpose.

---

## 0. Where to resume (updated 2026-08-03; before that 2026-07-29, after Phase 3's withdrawal)

**Read the freeze notice at the top of this file first — this section is accurate but does not run
yet.** Everything below says what Phase 4 does; the freeze of 2026-08-11 says when.

**Next phase: Phase 4**, as `§9`'s closing "The exact next phase" states it — but **Phase 4 is no
longer promotion.** Ben settled the promotion question on 2026-08-03 (`§6` decision 5): MAM's
divergences from Yeivin's and Breuer's rules keep being recorded, and are grammatical for the time
being, so the 13 chanted words a promotion would have flagged become whitelist entries instead.
`§5`'s Phase 4 entry and `§9`'s closing section are both rewritten to that. **A Phase 5 was added
the same day — WLC's residue as an unlinked page — and was built the same morning**:
`gh-pages/accgram/wlc-chanted-word-residue.html` (wlc-utils `43890f8`; the generator is MAM-basics
`5fb9a69`). The residue it shows is **28 chanted words in 19 distinct pairs**, not the figure this
file was first written with: ITM §256 joined the inventory later that morning (MAM-basics
`007e708`, regenerated in `d3d656e` and `2302605`) and took the six `qadma darga` rows out. `§5`'s
Phase 5 entry has the execution record. Nothing else in this file is a pending instruction.

**`§10` was added later the same day and Phase 4 must not be started without it.** It settles how a
per-verse exception is spelled — on the chanted word's mark run plus its token sequence, never on a
verse reference — and it takes Phase 4's list of 13 down to **two chanted words, both taking a
per-verse exception**: ne8:7 ושר֥בי֣ה is held on MAM-basics#215, a defect
that leaves MAM with no legarmeh token anywhere and 1,610 lone bars counted as chanted words, and
ca8:6 שלה֥בתיה was held on a search of Yeivin's ITM and Breuer's CoS for a secondary merkha with
silluq — **run 2026-08-03 (`521e8dc`), and both books are silent, so Phase 4 may write ca8:6's
entry**; `§10` carries the search itself. (Until 2026-08-03 this paragraph called the search one
nobody had yet run; `521e8dc` updated `§10` and left this sentence behind, which the same day's
review, MAM-basics#219, caught.) `§5`'s Phase 4 entry and `§6` decision 1 both carry
the correction; the lists they were first written with are superseded, not merely narrowed, and
decision 5's parenthesis calling `merkha silluq` a multiple-timer is corrected there too.

**`§8`'s closing "The exact next phase" is spent, and must not be actioned.** It named Phase 3,
the rendered page; that page was built on 2026-07-29 and withdrawn the same day. `§5`'s struck
Phase 3 entry has the reasoning and `§9` has the state. Both of the two things `§8` told Phase 3
to settle with Ben were settled before it ran, and both answers are recorded there.

**`§8`'s opening subsection is stale, and reads as work to finish.** Written against `957113f`,
it describes edits to `maqaf_nonfinal_accents.py`, `maqaf_nonfinal_accents_page.py`,
`printed_decalogue_strands.py` and `wlc_utils_html.py` as sitting uncommitted in Ben's working
tree; all of it is committed, through `7aeeeb0`, as is the further `maqaf_nonfinal_accents.py`
edit that `§9` reports uncommitted. Read that subsection as history, and finish or reconcile
nothing it names.

**`§8`'s first open-question bullet, the mark-versus-token count reconciliation, is settled for
this plan's purposes.** Ben ruled it off the rendered page on 2026-07-29, and it is recorded in
issue #86. The `135` half of it is closed by issue #85 and must not be reopened.

**THIS PLAN DOES NOT COVER THE EDITING OF `maqaf-nonfinal-accents.html`.** That is a separate,
free-form track — Ben requesting edits interactively, not a plan — whose state is its own commit
messages, `829d1f6..` on `main`. (It kept a `doc/maqaf-nonfinal-accents-page-editing.md` until
2026-07-31, when that file was deleted as spent: everything durable in it had migrated to the
`hebrew-prose` skill, to this repo's `CLAUDE.md`, or to the docstrings of the page module it
governed, and its structural description of the page had gone stale.) It is named here only
because its widening onto the same
question is half of why Phase 3 went. **Do not read that track's state out of this file, and do
not record that track's state in this file.** A round of it was written into `§0` on 2026-07-29
(`b57f8b9`) and taken back out: a summary of what that page currently looks like, and a pointer
to `829d1f6..7aeeeb0` for its account. Both are that track's to keep, and both survive in that
commit for whoever moves them to where they belong.

### Before starting: two primaries, and the current commands

**A phase here touches two repos, so check both.** The code primary is
`C:\Users\BenDe\GitRepos\MAM-basics` (`py/accgram/...`, `py/tests/`) and the artifact primary is
`C:\Users\BenDe\GitRepos\wlc-utils` (`out/`, `gh-pages/`). Run `git log --oneline -3` and
`git status` in **both** before starting, not only at the end. `§9` states that guardrail against a
single primary because on 2026-07-29 there was only one, and a parallel edit in it is what killed
Phase 3.

Regenerate from the MAM-basics root, with MAM-basics' interpreter — whatever `.venv` is left in
wlc-utils has nothing to run:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_accgram.py --help
```

Tests are one entry point, run from the MAM-basics root:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\MAM-basics\py\main_test.py
```

`§9` records `.venv/Scripts/pytest.exe py/tests` with a `WLC_SIBLINGS_ROOT` in the environment.
That is how Phase 3 was verified in July, and it stays there as history; it is not the command to
run now.

---

## 1. What the checker can and cannot see today

`prose_scanner.scan_accents` reads a **mark body** in which maqaf (`-`) and space survive as
structural filler beside the opaque `LETTER` placeholder, so the boundaries are all there. But it
returns `list[Token]`, and a `Token` is `(type, leaf)` — no position. The PLY grammar therefore
consumes accent types alone and cannot see a chanted-word boundary at all.

A few scanner rules already read the filler locally, and each of them is load-bearing for this
work because each **fuses two written marks into one token**:

| rule | what it fuses | crosses a maqaf? |
| --- | --- | --- |
| `METHIGAZAQEF` | qadma … zaqef qatan | yes, deliberately — and it stops at a space (2026-08-03) |
| `PASHTA` | stress-helper pashta + main pashta | no (`TEXT` stays in one atom) |
| `ZARQA` | tsinnorit + tsinnor | no |
| `TELISHAQETANNA` | helper telisha + main telisha | no |
| `MAHAPAKHQADMA` | the same-letter bang cluster | n/a (one letter) |
| `LEGARMEH` | munaḥ + U+05C0 | no |
| `AZLA` (lookahead only) | nothing — it renames a qadma | crosses a word boundary |

**This is the key design fact.** Counting *tokens* rather than *marks* disposes of four of the
five confounds for free:

1. a stress helper written twice is already one token;
2. a fused impositive cluster (`mahapakh!qadma`, `merkha!azla`) is already one token;
3. meteg emits no token, and U+05BD becomes `SILLUQ` only immediately before sof pasuq;
4. legarmeh is one token, and a narrow-sense paseq is swallowed.

It also disposes of metigah-zaqef, which is *already* one `METHIGAZAQEF` token and so never
presents as two accents on one chanted word — 324 of them in WLC prose *(probe)*, 319 since the
fuse was stopped at a space on 2026-08-03 (§7's bullet).

The fifth confound survives and must be handled by hand: **a repeated geresh or gershayim is one
accent written twice, and the scanner does not fuse it.** MAM's Lev 10:4 and Ezek 48:10 come out
as three tokens apiece (`gershayim+telishagedola+gershayim`, `geresh+telishagedola+geresh`)
*(probe)*.

### Two consumer paths, and only one of them runs the word-level layer

- `prose_run._verse_record` → `lexical_validation.lexical_ungrammatical(body)`, then the grammar.
- `printed_decalogue.parse_marks_body` → the grammar **only**. The Wikisource strands and all
  twelve hand transcriptions reach the grammar through this path, so `lexical_validation` never
  sees them — including `koren_dt_elyon`, the case that motivates the whole exercise.

`lexical_validation` also **short-circuits**: a verse with a hit gets a fixed one-leaf ERROR tree
and the grammar is skipped entirely. Routing a chanted-word rule through it would discard the
parse tree of every affected verse and would overwrite, rather than sit beside, the verdict
SimTiq's Exodus appendix taḥton already has for an unrelated reason.

---

## 2. What is actually out there — the measurement nobody had

The compound half was surveyed by `maqaf_nonfinal_accents` (WLC prose 139 hits, MAM prose 233).
That survey asks a **narrower** question than this one: it counts an accent on a **non-final**
atom, so it never sees two accents that both sit on a compound's last atom, and it counts marks
rather than tokens, so its 202 MAM `qad-zaq` compounds are one token each here.

The atomic half had never been measured at all. It is the larger half.

### Chanted words with two or more accent tokens *(probe)*

| | chanted words | with ≥2 accent tokens | distinct token sequences |
| --- | --- | --- | --- |
| WLC prose | 233,238 (196,418 atomic + 36,820 compound) | **1,602** (1,107 atomic, 495 compound) | 33 |
| MAM prose | 234,985 (198,199 atomic + 36,786 compound) | **1,644** (1,160 atomic, 484 compound) | 19 |

*(Re-derived. The hit counts and their atomic/compound splits are the probe's exactly; the WLC
chanted-word totals are not, because the probe counted the swallowed ketiv of a ketiv-qere and
the petuhah/setumah markers as chanted words and the module does not. Both sequence counts were
wrong in the probe.)*

Of WLC's 495 compounds, 450 have both tokens on the **final atom** and only 45 split across
atoms — which is why the existing maqaf-non-final survey sees so few of them.

MAM is markedly the more regular corpus, as the 33-vs-47 sequence count says: every one of WLC's
odd shapes (`munax+munax`, `pashta+zaqef`, `zaqef+tipexa`, `darga+tevir`, `tipexa+munax`,
`telishagedola+revia`, `merkha+legarmeh`, `mahapakh+tipexa`) is absent from MAM. A grammatical
claim takes MAM, so **MAM is the corpus the whitelist must be closed against**, and WLC's residue
is then a statement about the Westminster transcription of L rather than about the accentuation.

### MAM prose, every sequence *(probe)*

| tokens | atomic | compound | total |
| --- | --- | --- | --- |
| munaḥ + zaqef | 959 | 415 | 1374 |
| azla + geresh | 99 | 27 | **126** |
| merkha + tevir | 61 | 8 | 69 |
| merkha + tipeḥa | 4 | 8 | 12 |
| mayela + etnaḥta | 3 | 8 | 11 |
| mahapakh + pashta | 3 | 5 | 8 |
| qadma + merkha | 3 | 3 | 6 |
| qadma + mahapakh | 4 | 2 | 6 |
| qadma + darga | 5 | 1 | 6 |
| mayela + silluq | 4 | 1 | 5 |
| munaḥ + revia | 4 | 1 | 5 |
| merkha + silluq | 1 | 4 | 5 |
| gershayim/geresh with telisha gedola | 5 | 0 | 5 |
| munaḥ + etnaḥta | 2 | 0 | 2 |
| munaḥ + pazer | 1 | 0 | 1 |
| munaḥ + mahapakh | 1 | 0 | 1 |
| merkha + pashta | 0 | 1 | 1 |
| merkha + munaḥ | 1 | 0 | 1 |

---

## 3. Yeivin's inventory is larger than the whitelist as stated, and most of it is closed lists

Grepping the full OCR at `../MAM-private/masorah-books/books/itm/md-export-of-docx/`
(`../yeivin-itm/` when this plan was written, and `../masorah-books/` until the tree moved under
MAM-private on 2026-08-10) turns up a **named section for each
of these**, and the closed ones match the measured MAM counts case for case. This is the plan's
central finding: the whitelist is not something to invent, it is something to transcribe, and
transcribing it yields a differential check against an independent oracle — the one test shape
that has ever paid in this repo.

| ITM § | what it names | Yeivin's own count | MAM measured *(probe)* |
| --- | --- | --- | --- |
| §210 | mayela with silluq | "in five places" | **5** — and his five verses are the measured five (Lev 21:4, Nu 15:21, Is 8:17, Hos 11:6, 1C 2:53) |
| §215 | munaḥ with etnaḥta | "in two cases" | **2** — his two (2S 12:25, 1C 5:20) |
| §216 | mayela with etnaḥta | "in ten or eleven cases" | **11** — his eleven |
| §219/§221 | munaḥ-zaqef | "in many cases"; a fourth variant of the zaqef melody | 1374 |
| §223/224 | metigah-zaqef | — | one token; invisible to this rule |
| §233 | merkha with tipeḥa | "in 8 cases", listed | 12 — **explained**, see §7 |
| §236 | munaḥ with revia | "in five cases" | **5** — his five (Ex 32:31, Gen 45:5, Qoh 4:10, Zech 7:14, Dan 1:7) |
| §241 | **mehuppak with pashṭa** | "in five cases", all on the prefixed ־ש | 8 (his five, plus three compounds) |
| §244 | the two servi of pashta on one word | "in eight places", listed | his eight, inside a 13-strong union of `qadma+mahapakh`, `qadma+merkha`, `munax+mahapakh` |
| §253 | merkha-tevir | "some hundred cases" | 69 |
| §268 | **azla-geresh on one word** | "often" | **126** |
| §276 | munaḥ on the word bearing pazer | "in one case, Gen 50:17" | **1**, at gn50:17 |
| §372/§373 | tsinnorit, poetic metigah | poetic | out of scope |

*(Re-derived; every measured figure above is now read out of `out/accgram/chanted-word-accents.json`.
Two section numbers were wrong in the planning pass: the "fourth variant of the zaqef melody"
sentence is **§219**, not §221 — §221 gives munaḥ-zaqef's conditions — and the pazer case is
**§276**, which the plan had cited only by OCR line number.)*

Three consequences, each of which changes the work:

**(a) `azla-geresh` (§268) is missing from the whitelist as stated, and it is the second-largest
class.** 126 chanted words in both WLC and MAM. Yeivin frames it in exactly Ben's terms:
*"Azla is often marked as a secondary accent on the word bearing geresh. This occurs under
conditions similar to those governing the marking of munaḥ on the word bearing zaqef, or merka on
the word bearing tevir (#221, 253)."*

**(b) `maqaf_nonfinal_accents._NAMED_CONFIGURATIONS` has two citation faults.** It cites
"ITM §§233, 241" for the secondary merkha in a tevir's chanted word; the section is **§253**
(`Merka-tevir and the Servi of Tevir`). And its `(MAHAPAKH, TEVIR)` entry has never fired in any
corpus, because **§241 is mehuppak with *pashṭa*, not with tevir** — which is also why
`mahapakh+pashta` shows up in the measurement and `mahapakh+tevir` does not.

**(c) Yeivin states Ben's own principle outright**, so the atomic-and-compound unification needs
no argument of its own. ITM **§302** (not §301, which is about maqaf variants between
manuscripts): *"From the point of view of the accentuation, words joined by maqqef are considered
as a single unit, and are treated so in the marking of conjunctives, secondary accents, and
gaʿya"*, illustrated with אל־האשה taking munaḥ-zaqef precisely because the maqaf makes it one unit.

### The residue

After the whitelist above, MAM prose leaves **18** chanted words whose token sequence no section
of Yeivin's inventory names — `qadma+darga` 6 (including Job's prose frame ×4), `merkha+silluq` 5,
the five telisha-gedola + geresh-family words already whitelisted elsewhere in
`lexical_validation`, `merkha+pashta` 1, `merkha+munax` 1. That is a publishable finding on its
own: the whole prose Tanakh, in the corpus a grammatical claim takes, has eighteen chanted words
with two accents that Yeivin's inventory does not name, and five of those eighteen are the
telisha-gedola words the almost-errors page already documents. The list is carried as
`mam_residue` in the JSON.

WLC's residue is larger and different in kind, and includes the cases the pages already care
about: `munax+munax` at 1c27:14 לעשתי־עשר, 2c1:11 ויאמר־אלהים and ek8:6 מה־הם (which the probe
missed), plus one atomic `munax+munax` at gn36:13. **MAM has none.**

---

## 4. Recommendations

### 4.1 A new module, not a change to the grammar

`py/accgram/chanted_word_accents.py` (+ `_page`), beside `maqaf_nonfinal_accents`.

Teaching the PLY grammar about boundaries means threading a boundary token through every
production of a 39,000-line grammar file whose completion criterion was byte-identical parity with
the frozen Goerwitz C checker. The rule is not a rule about accent *sequence* — the grammar's
whole subject — it is a rule about how a sequence is distributed over chanted words. This repo
already has a home for word-level rules the C grammar has no notion of (`lexical_validation`'s
three checks), and the precedent is a separate layer, not a grammar change.

The one enabling change to mature code is small and additive: give `prose_scanner.Token` a
`start: int = -1` field, set at emit time. Nothing in the repo compares `Token` instances — only
`.type` and `.leaf` are read — and the six positional `Token("TILDE", "")` constructions keep
working.

### 4.2 A separate diagnostic channel first; the ERROR leaf is a later, gated decision

Recommend recording hits as their own field on the verse record, leaving `status` and `tree`
untouched, and deciding promotion only once the whitelist is closed. Three reasons:

- `lexical_validation` short-circuits, so routing through it discards parse trees and **overwrites**
  the SimTiq Exodus taḥton verdict instead of standing beside it. Ben's instruction is explicit
  that the new rule be evaluated against the existing verdicts.
- `parse_marks_body` — the Koren path — does not call `lexical_validation` at all, so an
  `illegal_mark` implementation would miss the motivating case unless separately wired.
- A channel makes the whitelist reviewable against evidence before it changes any verdict, and the
  promotion is then a one-line change with a readable diff.

A clean rate is not a goal, so this is not a reluctance to flag; it is sequencing.

---

## 5. Phases

### Phase 1 — Measure both halves, and transcribe Yeivin's inventory

New `py/accgram/chanted_word_accents.py`: pure computation plus a JSON writer, the shape
`maqaf_nonfinal_accents` already has.

- Re-derive every *(probe)* number above in the module, over WLC 4.22, UXLC and MAM-simple, prose
  verses only, routed by `prose_filter.should_keep_line`.
- Per hit: `bcv`, the chanted word in **letters and accents, no vowels**
  (`almost_errors_html_shared.accents_and_letters`, lifted from the corpus, never retyped), the
  token sequence, and the kind (atomic / compound with the accents split across atoms / compound
  with both on the final atom).
- A `yeivin_inventory` table transcribed from
  `../MAM-private/masorah-books/books/itm/md-export-of-docx/`: section number,
  what it names, Yeivin's stated count, his listed verses where he lists them, and the measured
  count beside it. Where his list is closed, assert set equality and **raise** on drift.
- Correct `maqaf_nonfinal_accents._NAMED_CONFIGURATIONS`: §253 for merkha-tevir; replace the
  never-firing `(MAHAPAKH, TEVIR)` with §241's mehuppak-with-pashṭa; add §268 azla-geresh, §215,
  §236, §210's silluq mayela and the §pazer case as far as that survey's shape allows.
- Note as data, not as prose: 5 of 324 `METHIGAZAQEF` tokens span a chanted-word boundary
  *(probe)* — the fusion the design leans on is not perfectly word-internal, and the five cases
  should be named. **Done, and then settled: on 2026-08-03 the fuse was stopped at a space, so
  the count is 0 in all three corpora and `_methigazaqef_crossings` is now a lint that must read
  0 rather than a record of exceptions. See §7's bullet.**

**Verification.** `out/accgram/chanted-word-accents.json` is written and read; the closed-list
assertions pass (§210's five, §215's two, §236's five, §244's eight, the one §pazer case); the
§233 mismatch (8 stated vs 12 measured) is either explained or recorded as an open question.
Regenerate `out/accgram/maqaf-nonfinal-accents.json` and its page with
`generate-html-maqaf-nonfinal-accents` and read the diff — the citation corrections should move
`by_configuration` labels and nothing else.

**Handoff.** The whitelist table, closed against MAM and cited to Yeivin, plus the named residue.

### Phase 2 — The whitelist, the token positions, and the diagnostic channel

- `prose_scanner.Token` gains `start`.
- `chanted_word_accents.classify_verse(body, tokens)` → the hits of one verse, each named
  (with its ITM section) or unnamed. The whitelist is keyed on the **token pair**, not on a verse
  reference (decision 1): Yeivin's closed lists are checked in Phase 1's data, not consulted here.
- Wire it into **both** consumer paths as an additive field: `prose_run._verse_record` and
  `printed_decalogue.parse_marks_body` (which covers the eight Wikisource strands and all twelve
  transcriptions in one stroke).

**Verification.** Regenerate `out/accgram/prose/*_ag.json` (`run-prose`) and
`out/accgram/printed-decalogue/_printed_decalogue.json` (`run-printed-decalogue`). Every existing
`status`, `errors` and `tree` must be **byte-identical**; the only diff anywhere is the new field.
That invariant is the phase's test, and it is checkable by eye in the diff.

### ~~Phase 3 — The rendered page~~ — WITHDRAWN 2026-07-29, after being built

`chanted_word_accents_page.py` → `gh-pages/accgram/chanted-word-accents.html`, one page one
question: does a chanted word with two accents that Yeivin's inventory does not name have a
precedent in the prose Tanakh?

**Built, shown to Ben, and dropped the same day.** Two reasons, and the second is the one that
matters for the rest of this plan:

- `0ab2c6a`, "Ask the page's question of all three printed compounds, not Koren's alone", had
  meanwhile widened `maqaf-nonfinal-accents.html` onto the same ground, adding an
  `unprecedented_pairs()` derivation and a simple-chanted-word appendix. Ben: "mostly now
  redundant".
- **A page was never this plan's thrust.** §§1–4 are about teaching the checker a chanted-word
  rule; §4.2 sequences it as a diagnostic channel first and an ERROR leaf later. Ben, 2026-07-29:
  "the production of such an HTML page was at best a waypoint along the way, right? I don't even
  remember asking for it". A phase whose deliverable is a rendering does not advance the checker.

**Nothing was lost by dropping it.** The Yeivin cross-check — his sections, his stated counts, his
closed verse lists, and the assertion that raises where a list and the measurement disagree —
lives in `out/accgram/chanted-word-accents.json`, written by `survey-chanted-word-accents`, and
that is the form Ben wanted it in: "if needed it can be recorded in some way other than HTML."

**The lesson for whoever plans the next one of these.** A phase that renders is a phase that does
not advance the plan's own goal, so it needs a reason of its own to exist. This one had a real
one when it was written — the survey had no reader-facing form at all — and lost it to a commit
on a neighbouring page. Check the neighbours before writing a page, and prefer folding a finding
into an existing page over standing up a new one.

### Phase 4 — Whitelist MAM's residue, and go on recording it — REWRITTEN 2026-08-03

**What this entry said until then, under the title "Promotion (gated on the answers in §6)".** If
the flag became an ERROR, `classify.py` and the goerwitz page
would pick it up with no further wiring, and the phase's job was to show which verdicts were
**newly** ungrammatical rather than a total — SimTiq's Exodus appendix taḥton third chanted verse
being already ungrammatical for an unrelated reason (three servi where the pashta phrase takes
two). That question — should a chanted word whose accent pair no section of Yeivin's inventory
names be ungrammatical? — **Ben answered on 2026-08-03, and the answer for MAM is no, for the time
being.** §6 decision 5 has his words. The 13 MAM chanted words a promotion would have made newly
ungrammatical become **whitelist entries**.

**This decides verdicts; it does not retire the measurement.** "All divergences … should continue
to be recorded, for possible future return to (for further research)" is half of Ben's ruling, and
it binds this phase: every one of them stays in `out/accgram/chanted-word-accents.json` — the
residue lists, the sequences, the ITM cross-check and its assertions — so that the research Ben
means to return to has its data waiting. Nothing in the survey is dropped, narrowed or folded away
because the verdict changed.

The whitelist grows two ways, along the line Ben's ruling draws:

- **As policy, for a sequence that occurs more than once**: configuration-level entries beside
  Yeivin's sections, marked as MAM-attested rather than ITM-named so that a reader can see which
  entries are transcribed from Yeivin and which are Ben's ruling.
- **As a per-verse exception, for a one-timer**, by the mechanism §10 records: keyed on the chanted
  word's mark run plus the token sequence, with the verse reference in a comment. Do not invent a
  second one, and see §6 decision 1, which this qualifies.

**Which chanted words those are is no longer what this entry first said, and §10 is the correction
to read.** It named `qadma darga` ×6 and `merkha silluq` ×5 as the policy entries and ne8:7's
`merkha munax` and ek16:12's `merkha pashta` as the two exceptions. Of those, the six `qadma darga`
went to **ITM §256** rather than to a whitelist, and ek16:12 together with four of the five `merkha
silluq` are **§357 maqaf-after-gaʿya compounds** — chanted words, with two accent tokens, whose
second token is the non-final atom's retained accent rather than a secondary accent, so no whitelist
entry is owed. What is left is **ne8:7 ושר֥בי֣ה**, held on MAM-basics#215 until MAM tokenizes its
legarmeh as one, and **ca8:6 שלה֥בתיה**.

**And `merkha silluq` is a one-timer, not the multiple-timer decision 5's sentence names it as**
(Ben, 2026-08-03). Its count of five is four שלף־חרב compounds that §357 accounts for plus ca8:6,
which is the only atomic `merkha silluq` in any of the three corpora. So it takes a per-verse
exception, not the configuration-level entry the ruling's parenthesis assigns it — a
configuration-level entry would name a pair on the strength of one chanted word, which is the thing
the per-verse mechanism exists to avoid. The same test disposes of the parenthesis's other example:
`qadma darga` ×6 went to ITM §256 and needs no entry at all. **Read "one-timer" as counting the
chanted words a sequence still has after the inventory has taken what it names, not the raw
`by_sequence` figure.**

Also to settle here: whether the five telisha-gedolah words `lexical_validation` already
whitelists should be named the same way, so that the whole whitelist reads out of one place.

**Verification.** Regenerate `out/accgram/prose/*_ag.json` and
`out/accgram/printed-decalogue/_printed_decalogue.json` and read the diff. **No `status` may move,
in any corpus** — the phase adds no error, so a moved verdict is a bug and not a finding. What
changes is the `chanted_word_accents` field's null `itm_section`s, into whatever the whitelist
records. Regenerate `out/accgram/chanted-word-accents.json` too, and check that `mam_residue` and
its WLC counterpart are **unchanged**: a residue that shrank as the whitelist grew would be the
measurement quietly following the verdict, which is the one thing Ben's ruling forbids.

### Phase 5 — WLC's residue as an unlinked page (added 2026-08-03; executed the same day)

**Ben's ruling is about MAM, and WLC's residue is a different set** — §8 item 6 records that
neither contains the other. Nothing in §6 decision 5 reaches it, and this plan should not extend it
there. What Ben asked for on the same day, instead, is a **"sneak peek"**: a page under
`gh-pages/accgram/` holding WLC's unnamed chanted-word accent pairs, **unlinked** from the site,
**deliberately not folded into `goerwitz.html` or `almost-errors.html`**, and possibly never folded
in — though the goerwitz page may eventually link it.

**Why this rendering is not the one §5's struck Phase 3 entry warns against.** That entry rules
that a phase whose deliverable is a rendering needs a reason of its own, and that the neighbouring
pages must be checked first. This one has the reason: Ben asked for the page directly, and asked
for it standing apart rather than folded in, which is the opposite of the fold Phase 3 lost to. The
neighbour check still applied before a line of it was written — `maqaf-nonfinal-accents.html`
widened onto Phase 3's ground once already — and the page ended up sharing that neighbour's opening
at Ben's asking rather than colliding with it (`3760b2f`).

- One page, one question: where does the Westminster transcription of the LC have a chanted word
  with two accents that no section of Yeivin's inventory names?
- The data is already tracked, as `mam_residue`'s WLC counterpart in
  `out/accgram/chanted-word-accents.json`. The page derives every number it states from that file
  and pins it, `maqaf_nonfinal_accents_page.pin_claims`-style.
- WLC's own shapes are the half worth showing — `munax munax` at gn36:13, ek8:6, 1c27:14 and
  2c1:11, which MAM has nowhere. §2 already frames those as facts about the Westminster
  transcription rather than about the accentuation, and that framing belongs on the page.
- **Unlinked means unlinked**: no index entry, no cross-reference from a neighbouring page. Whether
  the goerwitz page comes to link it is Ben's to say later, not this phase's to anticipate.

**Executed 2026-08-03, the day it was added.** The page is
`gh-pages/accgram/wlc-chanted-word-residue.html` (wlc-utils `43890f8`), generated by
`MAM-basics/py/accgram/wlc_chanted_word_residue_page.py` via `main_accgram.py
generate-html-wlc-chanted-word-residue`, both landed in MAM-basics `5fb9a69`. Three same-day
regenerations are part of the record: `2302605` (ITM §256 joined the inventory in MAM-basics
`007e708` / wlc-utils `d3d656e`, taking the six `qadma darga` rows out of the residue), `1812076`
(an opening-paragraph fix) and `3760b2f` (the opening rewritten to
`maqaf-nonfinal-accents.html`'s, at Ben's asking). Against the specification above, point by
point:

- **The one question, answered as a table**: one row per WLC chanted word whose accent pair no
  section of Yeivin's inventory names — **28 rows in 19 distinct pairs**, re-derived 2026-08-03
  from `out/accgram/chanted-word-accents.json` at the write-back; the tracked page states the
  same 28 and 19.
- **Derived and pinned.** One precision against the bullet above: the JSON has no stored WLC
  counterpart of `mam_residue` — the set is derived, an occurrence of `corpora.wlc422` whose
  sequence no inventory entry's `token_sequences` has, which is what the generator's `residue()`
  does. And the page's numbers come from `chanted_word_accents.build_survey()`, the same function
  `survey-chanted-word-accents` writes the JSON from, rather than off the file itself — the
  stronger coupling, since page and data then cannot disagree. Its `pin_claims` raises on drift,
  `maqaf_nonfinal_accents_page`-style, as specified.
- **WLC's shapes shown**: the four `munax munax` rows are at gn36:13, ek8:6, 1c27:14 and 2c1:11,
  exactly the verses the bullet above names, and the
  facts-about-the-Westminster-transcription-not-about-the-accentuation framing is the page's
  second paragraph.
- **Unlinked, verified**: no file under `gh-pages/` names the page (checked 2026-08-03). The page
  links out to `goerwitz.html`; the specification bans incoming links, not outgoing ones.

Nothing of the specification remains. This record was written back on 2026-08-03, after the same
day's review (MAM-basics#219, major 1) found §0, this entry and `§9` all still framing Phase 5 as
unbuilt hours after the page had landed.

---

## 6. Decisions (settled with Ben, 2026-07-28; decision 5 and decision 1's qualification, 2026-08-03)

1. **Pin Yeivin's lists as DATA, allow the configuration as the RULE.** Where he gives a closed
   list, the `yeivin_inventory` section of the JSON carries his verses and the module asserts set
   equality against the measurement, raising on drift — so the differential oracle is kept in full.
   The checker's own whitelist is nonetheless **configuration-level**: `munax+revia` is named
   wherever it occurs, not only at §236's five. This keeps verse references out of the flagging
   path while keeping the sharpness where it earns its keep.

   **Qualified 2026-08-03 by decision 5, and the qualification is real** — but it costs decision 1
   less than it first looked. The whitelist is configuration-level for a sequence that repeats and
   **per-verse for a one-timer**; what §10 settles is that "per-verse" is spelled **as the chanted
   word's mark run plus its token sequence, with the verse reference in a comment**, so no verse
   reference reaches the flagging path after all and `classify_verse(body, tokens)` keeps its
   signature. That honours decision 1's actual reason, which was that a chanted word be named by
   what it has and not by where it stands: a mark run is what it has. What survives unqualified:
   **Yeivin's closed lists still stay out of the flagging path**, as the survey's differential check
   and nothing else. An exception here is Ben's ruling about a MAM chanted word, not a transcription
   of ITM, and the two must not be fed from one table.

   **The two chanted words this was written for have since come apart** — ek16:12 is a §357
   maqaf-after-gaʿya compound and is owed no entry, and ne8:7 is held on MAM-basics#215. §10 has
   both.
2. **Survey WLC, UXLC and MAM; flag WLC (and the Decalogue paths) only.** The whitelist is closed
   against MAM, as a grammatical claim requires, but the per-verse field lands in
   `out/accgram/prose` and `_printed_decalogue.json`, which is where verdicts live today. Record
   plainly that Isaiah 40:7 נבל־ציץ is therefore a MAM-only case the WLC flag never sees: WLC sets
   נבל and ציץ as two chanted words.
3. **CTR stays glyph-level.** Its two cases are recorded in `ctr_decalogue` as evidence about CTR;
   grammar-checking it would produce verdicts that invite reading it as a precedent, which it is
   not.
4. **Channel first, promotion decided later** — §4.2 as written. Phases 1–3 add a diagnostic field
   only; Phase 4 revisits it once the whitelist is closed and the residue is visible.
5. **MAM's divergences from Yeivin's and Breuer's rules are recorded, and grammatical** (settled
   2026-08-03). This is the answer decision 4 deferred. Ben, in his words:

   > For the time being at least, all divergences of MAM from Yeivin and/or Breuer rules should
   > continue to be recorded, for possible future return to (for further research), but they should
   > be considered grammatical, either as policy, for multiple-timers (qadma darga x6, merkha
   > silluq x5), or as per-verse exceptions (merkha munax x1 (ne8:7), merkha pashta x1) for
   > one-timers.

   **It rules on verdicts only.** "Continue to be recorded" is the other half of it and is not a
   courtesy: the survey keeps every divergence, so that the future research Ben names has its data.
   A phase that whitelisted a sequence and dropped it from `mam_residue` in the same stroke would
   have obeyed half the sentence.

   **It covers MAM.** WLC's residue is a different set, and Phase 5 — delivered 2026-08-03 as an
   unlinked page, not a verdict — is what Ben asked for there instead. Do not read this decision
   onto WLC.

   **What it does to #86.** §9 made the 13 the strongest argument for settling #86 before anything
   else, because a promotion would have flagged MAM — the corpus a grammatical claim takes — on a
   whitelist whose Yeivin citations this plan already records as unsettled. With MAM no longer
   flagged, that argument is spent. **#86's contents are unchanged**: the §233/§241 surplus, the
   `(MERKHA, SILLUQ)` citation to a section about tipeḥa, the `(QADMA, ZAQEF_QATAN)` citation to
   §224 rather than to §223 where metigah-zaqef is defined, the METHIGAZAQEF boundary crossings and
   the rest all stand exactly as §7 and §8 leave them. What changed is why they matter: they are
   now research into Yeivin's inventory, worth doing for its own sake, rather than a precondition
   for avoiding a bad verdict. **#86 does not gate Phase 4.**

---

## 7. Phase 1 state (executed 2026-07-28)

### Main moved under this phase, and Phase 1 was rebased onto it

Phase 1 was written against `48137a6`. While it ran, Ben committed **`832df3e`, "Report the pairs
that occur, and count them on simple chanted words too"**, which cut the whole route
classification out of `maqaf-nonfinal-accents.html` — the undecided and no-named-configuration
rows, the §§293/357 paragraph, the Judges 7:13 positional worked example, and two `pin_claims`
assertions — and added, to the survey, a per-pair count of the **simple chanted words** carrying
two different accents. Phase 1 was rebased onto it, and that changed what Phase 1 lands:

- **Dropped**, as superseded: every page-side edit. `_CONFIG_DISPLAY` no longer exists, so the
  labels, the `ROM_AZLA` constant added for them, the reworded route sentence and the two new
  `pin_claims` assertions all went with it. `maqaf_nonfinal_accents_page.py` and
  `printed_decalogue_strands.py` are untouched by this phase, and
  **`gh-pages/accgram/maqaf-nonfinal-accents.html` does not move at all.**
- **Kept**: the new module, `Token.start`, the subcommand, and the citation corrections — the
  survey still computes the routes, so `_NAMED_CONFIGURATIONS` is still live and still wrong
  without them. It is now only the JSON's `by_configuration` that moves.
- **Also kept from Ben's rewrite**: his rule that it is "the mayela", never "the mayela tipexa".
  The new module's §210 and §216 entries follow it.

**A convergence worth acting on in Phase 2 or 3.** `832df3e`'s own message says of its new simple
chanted-word count that "two marks are not always two accents — 135 of them are a tsinnorit beside
a tsinnor, which in a prose verse is the zarqa written twice — and telling those apart wants the
scanner's tokenization rather than this scan." That is exactly what `chanted_word_accents` does:
the scanner fuses tsinnorit + tsinnor into one `ZARQA` token, so its atomic counts have the 135
already removed. The two measures should be reconciled rather than left to disagree.

**Superseded — read §8's first open-question bullet before acting on this paragraph.** The 135 are
not a case the two measures decide differently: in a prose verse U+0598 is the zarqa's stress
helper and U+05AE is the zarqa, so the pair is one accent and its helper. Issue #85.

### What changed

**New: `py/accgram/chanted_word_accents.py`** — pure computation plus a JSON writer, modelled on
`maqaf_nonfinal_accents`. It builds each verse's mark body **atom by atom**, keeping every
fragment's Unicode beside its marks, so a token position is an offset into the same string the
chanted-word boundaries are offsets into. For WLC the rebuilt body is asserted equal to
`uni_to_marks.verse_to_marks`' own output for every verse of WLC 4.22, poetic ones included,
which is what makes the Unicode-to-marks alignment a checked fact rather than a claim. It writes
`out/accgram/chanted-word-accents.json` (29,710 lines).

**New subcommand** `survey-chanted-word-accents` in `main_accgram.py`. Phase 3's page generator
should either call this module or replace the subcommand, as
`generate-html-maqaf-nonfinal-accents` does for the other survey.

**`prose_scanner.Token` gained `start`**, as `field(default=-1, compare=False, repr=False)`.
Excluding it from `__eq__`/`__hash__`/`__repr__` is stronger than the plan proposed and costs
nothing: two tokens of the same type and leaf stay equal and interchangeable everywhere the repo
already treats them so, and the six positional `Token("TILDE", "")` constructions are unaffected.
`scan_accents` sets it at emit time; the recovered verse-final `SILLUQ` of a sof-pasuq-less verse
carries the position of the U+05BD it came from.

**Reuse hooks in `maqaf_nonfinal_accents`**: `_UXLC_FILE_TO_BB` → `UXLC_FILE_TO_BB` and
`_uxlc_text` → `uxlc_text`, since the new module reads the same XML for atoms rather than for
chanted words.

**The two citation faults are fixed**, and four sections added, in
`maqaf_nonfinal_accents._NAMED_CONFIGURATIONS`:

- merkha-tevir is **§253**, not "§§233, 241".
- `(MAHAPAKH, TEVIR)` — which had never fired in any corpus, in either genre, since the survey
  was written — is replaced by `(MAHAPAKH, PASHTA)`, §241's real pairing.
- added: §268 azla-geresh, §215 munaḥ-with-etnaḥta, §236 munaḥ-with-revia, §276 munaḥ-with-pazer;
  and §216 / §210 now carry their section numbers on the two mayela labels.

`maqaf_nonfinal_accents_page` is **not** touched. It was, until the rebase onto `832df3e` above
made every one of those edits unnecessary.

### What was verified

1. **`out/accgram/chanted-word-accents.json` written and read back.** Every figure quoted here
   and in the tables above is read out of the regenerated file.
2. **The closed-list assertions pass and raise on drift.** §210's five, §215's two, §216's
   eleven, §236's five and §276's one at gn50:17 match exactly; §233's eight, §241's five and
   §244's eight are each fully contained in the measurement, with the surplus recorded as data.
   The assertion **earned its keep on the first run**: it rejected `nu2:26` for §216, and the OCR
   line ("בשבעת יכם 8:26 2 Nu") turns out to be Numbers **28**:26 with the 28 broken across the
   reference. That transcription slip would have stood unnoticed without the check.
3. **§233's discrepancy is explained**, in the JSON's `merkha_tipexa_discrepancy`. All eight of
   Yeivin's have both marks on ONE atom (four atomic chanted words, four compounds with the
   merkha on the same atom as the tipeḥa); all four beyond his list instead have the merkha on a
   non-final atom — is66:8 אם־יולד־גוי, ek1:4 ונגה־לו, 2c8:11 אשר־באה־אליהם, 2c14:6 וינח־לנו.
   §241's three-case surplus has exactly the same shape. **This is left as an open question, not
   a verdict**, because the two surveys currently answer it differently: `_NAMED_CONFIGURATIONS`
   labels a merkha on a non-final atom with a tipeḥa on the compound as §233's secondary merkha,
   which is precisely those four, while Yeivin's own list excludes them. Issue #82.
4. **`generate-html-maqaf-nonfinal-accents` regenerated, diff read.** Hit sets, per-hit shapes,
   oracle evidence, the whole gray-maqaf section and **the rendered page itself** are unchanged in
   all three corpora and both genres. What moved, in the JSON only: the label renames, and six
   hits reclassified from route (b)/undecided into route (a) now that §§215, 236 and 241 name them
   (WLC prose 126→132 route (a), UXLC 120→124, MAM 230→233). MAM prose now has neither a route-(b)
   nor an undecided case. §268 and §276 name nothing in *that* survey, since no compound anywhere
   has a qadma on a non-final atom with a geresh on the compound; they are correct entries that
   this shape cannot express, which is why the wider survey exists.
5. **`run-prose` regenerated: `out/accgram/prose/*_ag.json` byte-identical**, 18,724/18,724 verses.
   The `Token.start` field is invisible to the outputs.
6. **`.venv/Scripts/pytest.exe py/tests`: 487 passed, 5 skipped.** The tree-wide transliteration
   lint caught Yeivin's `mehuppak` and `merka` spellings on first run; his verbatim quotes now
   carry `# translit-ok`, and every line of the repo's own prose says `mahapakh` and `merkha`.
7. **black** run on all six touched files.

### Generated outputs: what moved and what deliberately did not

| file | moved? |
| --- | --- |
| `out/accgram/chanted-word-accents.json` | **new** |
| `out/accgram/maqaf-nonfinal-accents.json` | yes — route/configuration labels and six reclassified hits; no hit, shape, oracle or gray-maqaf change |
| `gh-pages/accgram/maqaf-nonfinal-accents.html` | **no** — `832df3e` had already cut the classification out of the page |
| `out/accgram/prose/*_ag.json` | **no**, byte-identical, and that is the check on `Token.start` |
| everything else under `out/` and `gh-pages/` | not regenerated and not touched |

### Unresolved risks and open questions

- **The §233/§241 surplus (above) is unresolved**, and the two surveys disagree about it. It has
  to be settled before either the route-(b) material or a Phase 3 page states what those hits
  are. Issue #82.
- **`(MERKHA, SILLUQ)` is cited to §233 in `_NAMED_CONFIGURATIONS`, and §233 is about tipeḥa.**
  Yeivin has no section naming a secondary merkha in a silluq's chanted word — §209 gives silluq
  one conjunctive, merkha, and says nothing of a secondary. Left alone this phase (it is the same
  #82 question). Less urgent since `832df3e`, which stopped the page printing the label at all,
  but it still covers four MAM prose hits in the JSON.
- **`(QADMA, ZAQEF_QATAN)` is cited to §224.** §223 is where metigah-zaqef is defined; §224 is
  the retraction of methigah. Not wrong — §224 does discuss the combination — but not the
  defining section either. Left alone as out of this phase's scope.
- **MAM's `merkha tevir` is 69, WLC's is 2 and UXLC's is 10.** Yeivin §254 predicts exactly this
  ("Already in L gaʿya occurs in most of the cases where merka is expected"), and a meteg emits no
  token, so a manuscript that has one there shows a single accent token. The WLC-to-UXLC gap is
  Kimball's corrections. Worth a sentence somewhere; it is a finding, not a defect.
- **The METHIGAZAQEF fuse was not perfectly word-internal, and now is. RESOLVED 2026-08-03.**
  As first measured: 5 of WLC's 324 prose tokens spanned a chanted-word boundary (gn18:18,
  je37:10, je49:19, mi2:7, ne9:20) and 3 of UXLC's 324 (gn18:18, je37:10, 1k19:11). MAM's 410 had
  **none** — this bullet said "1 of MAM's 410 (lv13:33)" until 2026-08-03, which had been stale
  since `b5145ea`.
  The crossings were the fuse reaching across a space, which no source licenses: ITM §223 and CoS
  Ch. 5 §§4-6 both restrict the metigah to the chanted word of the zaqef, while §223's leading example
  Ex 35:9 ואבני־שהם is a compound and CoS Ch. 5 §5 allows a word-initial metigah where "there is
  there a hyphenated tiny word", so crossing a **maqaf** is right and crossing a **space** is not.
  `prose_scanner._METHIGA_MID` now excludes the space, and the counts are WLC 324→319 tokens with
  crossings 5→0, UXLC 324→321 with 3→0, MAM unchanged at 410 with 0. So Phase 2's whitelist **may**
  assume the fuse stays inside one chanted word; `_methigazaqef_crossings` is retained as the lint
  that holds it there. What surfaced: gn18:18, je37:10 and ne9:20 go clean→error, je49:19 and
  mi2:7 were already errors and their `ERROR` node moves to `zaqef_phrase` where it belongs, and
  the Simanim Tanakh's p. 298 transcription (`simtan_dt_taxton`) goes clean→ungrammatical, which
  is now a pinned departure. **Follow-ups are open, and `generate-html` is broken until the first
  is done — MAM-basics#218**: the three newly-ungrammatical verses need research notes
  (`rtmsr_overview` requires an `st-source` for each and raises without one), and the existing
  notes for je49:19 and mi2:7 both explain that the ERROR lands one phrase out from the defect,
  which is exactly what this change fixed, so both now describe a parse the checker no longer
  produces. The corpus-wide oddball count is 93→96.
  The control that settled it: WLC's 1k19:11 has a `]1` note marker
  between הרוח and רעש, whose digit already blocked the fuse, so the grammar already called that
  configuration an error — while the identical configuration at gn18:18 parsed clean, on nothing
  but an unrelated note marker.
- **Two `geresh_folds` fired, both in MAM** (lv10:4 קרבו, ek48:10 ולאלה), exactly as the plan
  predicted; WLC and UXLC need no fold. Each is recorded with its scanned and its counted
  sequence.

### The exact next phase

**Phase 2 as written in §5**, unchanged except that its first bullet is already done:

- ~~`prose_scanner.Token` gains `start`~~ — done in Phase 1, with `compare=False, repr=False`.
- Write `chanted_word_accents.classify_verse(body, tokens)` → the hits of one verse, each named
  with its ITM section or unnamed. Key the whitelist on the **token pair**, not on a verse
  reference (decision 1); Yeivin's closed lists are checked in Phase 1's data and are not
  consulted here. The whitelist is the `token_sequences` of the §-entries in `YEIVIN_ENTRIES`,
  which is already the right shape to read it off; the 18 in `mam_residue` are what it will flag.
- Wire it into **both** consumer paths as an additive field: `prose_run._verse_record` and
  `printed_decalogue.parse_marks_body`.
- **Verification**: regenerate `out/accgram/prose/*_ag.json` and
  `out/accgram/printed-decalogue/_printed_decalogue.json`; every existing `status`, `errors` and
  `tree` must be byte-identical, the new field the only diff anywhere.

---

## 8. Phase 2 state (executed 2026-07-29)

### Main had not moved, but Ben's working tree had

Phase 2 ran against `957113f`, which is still main's tip. Ben's uncommitted work — the
mechanical rules for telling two marks from two accents on a simple chanted word — sits in
`maqaf_nonfinal_accents.py`, `maqaf_nonfinal_accents_page.py`, `printed_decalogue_strands.py`,
`wlc_utils_html.py` and their two artifacts. **Phase 2 touches none of those five files**, and
neither `maqaf-nonfinal-accents.json` nor its page is among its outputs, so the two sets of
changes do not overlap at all. The convergence §7 called for is **not** done — see the open
question below.

### What changed

**`chanted_word_accents` gained the flagging path**, and the survey was refactored onto its
shared core rather than left as a second implementation:

- `NAMED_TOKEN_SEQUENCES` — the whitelist, built at import from the `sequences` of
  `YEIVIN_ENTRIES` and raising if two sections ever claim one sequence. Keyed on the token
  sequence alone (decision 1); Yeivin's closed verse lists stay where they were, as the
  survey's differential check, and nothing on a verdict path reads them.
- `classify_verse(body, tokens)` — one verse's chanted words with two or more accent tokens,
  each as `{marks, sequence, kind, itm_section}`, with `itm_section` null where no section of
  the inventory names the sequence. A null is the finding.
- `units_from_body(body)` — the chanted words read off the mark body alone, which is all a
  verdict path has. `uni_to_marks` puts a space between two chanted words and nowhere else, so
  a space-delimited run of a body is a chanted word; the non-words are the lone `P` / `S` /
  `N]8` markers and a `*`-prefixed ketiv, and a `**`-prefixed qere is a chanted word.
- `_by_chanted_word(units, tokens)` — the token-attribution and geresh-fold core, now called by
  both `scan_corpus` and `classify_verse`, so the survey and the flag cannot answer the same
  verse differently.
- `scan_corpus` asserts on **every** verse of all three corpora that `units_from_body`'s
  derivation equals its own fragment-by-fragment one. That is the guarantee Phase 2 needs and
  it is checked, not assumed.

**Wired into both consumer paths, as an additive field named `chanted_word_accents`:**

- `prose_run._verse_record` — recorded for every verse whatever its status, and omitted where
  there is nothing to report, as `errors` already is. It is set before the lexical layer's
  early return, so an `illegal_mark` verse carries it too.
- `printed_decalogue.parse_marks_body` — a new `ChantedVerseResult` field, emitted through a
  `chanted_word_accents_obj()` method that `transcription_parse._chanted_verse_obj` shares, so
  a transcription's chanted verse and a strand's put the field in the same position. This one
  wiring covers the eight Wikisource strands and all twelve hand transcriptions.
- `lexical_validation` was **not** touched, per §4.2.

**One pre-existing failure fixed.** `test_h_dot_below_nfc.py::test_comments_use_ascii_not_h_dot_below`
was already failing at `957113f`: Phase 1's comment above `YEIVIN_ENTRIES` named Yeivin's
romanizations by embedding the character, and comments must be ASCII. Reworded; the spellings
themselves stay in the quote strings, which are values, not comments. §7's "487 passed" was
therefore recorded against a tree that did not have that comment in its final form.

### What was verified

1. **`out/accgram/prose/*_ag.json`: zero deleted lines.** Every `status`, `errors` and `tree` is
   byte-identical; the diff is 12,638 inserted lines across 37 book files and nothing else, and
   every distinct added line belongs to the new field. 18,724/18,724 verses.
2. **`out/accgram/printed-decalogue/_printed_decalogue.json`: zero deleted lines**, 64 inserted.
   Same summary line as before — 8 versions, 88 chanted verses, 2 ungrammatical; 12
   transcriptions, 132 chanted verses, 1 departing from Wikisource.
3. **`out/accgram/chanted-word-accents.json` is byte-identical** after the refactor, which is
   the check that moving the survey onto the shared core changed nothing.
4. **The two derivations agree independently.** Read back out of the regenerated prose corpus:
   1,602 hits over 1,513 verses in 33 distinct token sequences — exactly the WLC prose figures
   the survey reports, reached by a different route (the body alone, verse by verse, through
   `classify_verse`) from the survey's (fragments, corpus-wide, through `_verse_units`).
5. **The motivating case fires.** `koren_dt_elyon` chanted verse 3 carries one hit: `munax
   munax`, a maqaf compound with its accents split across atoms, `itm_section` null. Its
   `status` stays `clean`, and `simtiq_ex_taxton`'s existing verdict is likewise untouched
   while it picks up two hits of its own (`munax merkha`, `munax qadma`, both null).
6. **Thirty-four unnamed hits in WLC prose**, where MAM's residue is 18. The two are not the
   same set and neither contains the other: WLC's includes its own shapes, `munax munax` at
   1c27:14, 2c1:11, ek8:6 and gn36:13 among them, which MAM has nowhere.
7. **`.venv/Scripts/pytest.exe py/tests`: 487 passed, 5 skipped.**
8. **black** run on the four touched files; `--check` clean.

### Generated outputs: what moved and what deliberately did not

| file | moved? |
| --- | --- |
| `out/accgram/prose/*_ag.json` | yes — the new field, inserted only; no line deleted anywhere |
| `out/accgram/printed-decalogue/_printed_decalogue.json` | yes — the new field, inserted only |
| `out/accgram/chanted-word-accents.json` | **no**, byte-identical, and that is the check on the refactor |
| `out/accgram/maqaf-nonfinal-accents.json` and its page | **no** — Phase 2 touches neither that survey nor its page |
| everything else under `out/` and `gh-pages/` | not regenerated and not touched |

### Unresolved risks and open questions

- **The convergence with Ben's simple-chanted-word count: settled 2026-07-29, and mostly by
  dissolving.** §7 framed the 135 U+0598-before-U+05AE places as a case the two measures counted
  differently. **They are not a case at all.** In a prose verse U+0598 is the zarqa's stress
  helper and U+05AE is the zarqa — Unicode's two names are, in effect, swapped — so those 135
  chanted words have one accent and its helper, exactly as a doubled pashta does, and belong in
  no table of accent pairs. Ben: "they are absolutely not two separate accents; this is just a
  result of unicode naming and annotation confusion." The rule now lives in the `hebrew-prose`
  skill and in this repo's auto-memory, and **issue #85** records why it kept being re-derived.
  **Do not reopen this**, and do not have a Phase 3 page adjudicate it.

  What genuinely differs is small, and only on MAM prose: Ben's scan counts **1,353** simple
  chanted words with two accents (`maqaf-nonfinal-accents.json`, as of `829d1f6`) against
  `chanted_word_accents`' **1,160** atomic hits. All sixteen shared pairs agree exactly, case for
  case; the whole gap is 1,353 − **198** + **5** = 1,160, where the 198 are qadma before zaqef
  qatan, one `METHIGAZAQEF` token here and two marks there, and the 5 are the geresh-or-gershayim
  with telisha gedolah that his scan sets aside as two marks on one letter. Whether even that
  belongs on the Phase 3 page is Ben's to say and is not yet answered.
- **`ne8:7` is `merkha legarmeh`**, unnamed, and it is one of the seventeen `has_legarmeh`
  passages. Whether a legarmeh's own conjunctive standing in the same chanted word is a case
  Yeivin's inventory ought to name is not settled here.
- **Four Job hits are `qadma darga` in the prose frame** (jb1:15, 1:16, 1:17, 1:19), unnamed in
  both corpora. Job's prose frame is prose-cantillated, so they are correctly in scope; they
  are simply not in Yeivin's list.
- **The §233/§241 surplus and the `(MERKHA, SILLUQ)` citation carry over from §7 unchanged.**
  Issue #82. Neither affects the flagging path, which is keyed on the sequence and names
  `merkha tipexa` wherever it stands; it does affect what a Phase 3 page may say those hits are.
- **The METHIGAZAQEF boundary crossings no longer carry over. RESOLVED 2026-08-03**, by §7's
  bullet: the fuse stops at a space, so `classify_verse` inherits a fuse that cannot reach across
  a chanted-word boundary, and there is no longer any place where one token stands for two chanted
  words. `methigazaqef.crossings` is empty in all three corpora and is kept as a lint.

### The exact next phase

**Phase 3 as written in §5** — `chanted_word_accents_page.py` →
`gh-pages/accgram/chanted-word-accents.html`, wired into `generate-html` and
`generate-html-chanted-word-accents`, one run writing both the JSON and the page, with a
`pin_claims` that re-derives every stated number from the data and raises on drift. One page,
one question: does a chanted word with two accents that Yeivin's inventory does not name have a
precedent in the prose Tanakh? Before it is written, settle with Ben (a) whether the residual
198-and-5 arithmetic above belongs on that page at all — the 135 half of that question is closed,
see #85 — and (b) how much of §7's and §8's open-question material goes to an issue rather than
onto the page. On (b), note that **#82 is the wrong issue**: its subject is Yeivin's two Deut 33
maqaf readings for the LC, so §7's and §8's citations of it for the §233/§241 surplus look
misfiled. #83, which holds the material cut from the maqaf-nonfinal-accents page, is the closer
fit; a new issue is the other option.

---


## 9. Phase 3 state (executed and then WITHDRAWN, 2026-07-29)

**Phase 3 built the rendered page, Ben looked at it, and it was dropped the same day.** The
reasoning is in §5's struck Phase 3 entry; in short, `0ab2c6a` had widened
`maqaf-nonfinal-accents.html` onto the same ground, and a page was never this plan's thrust.
So the phase's net contribution to the tree is small and deliberate, and the plan resumes at
Phase 4.

### Main moved under this phase, twice

Phase 3 started against `f0dbbc0` in the worktree `.claude/worktrees/great-easley-34eee3`, with
the primary checkout clean. By the time the page was ready, **main was at `0ab2c6a`** — "Ask the
page's question of all three printed compounds, not Koren's alone", 6,744 insertions across the
sibling survey, its page, its two artifacts and `printed_decalogue_strands.py` — and the primary
also had **21 insertions and 7 deletions uncommitted in `py/accgram/maqaf_nonfinal_accents.py`**,
the session "Continue editing maqaf-nonfinal-accents page" (worktree `sleepy-bell-ad6a3e`,
branch `claude/mystifying-hopper-c2f1f9`) finishing #85's stress-helper sweep into the one prose
module `fb3e5cc` had missed.

**That is the concrete hazard for the next phase, and it is not hypothetical: it is what killed
this one.** This plan's work sits next door to a page under active parallel edit. Check
`git log --oneline -3` and `git status` in the primary before starting, not only at the end.

**"The primary" was one repo when that was written, and is two now** (2026-08-03). The code
primary is `C:\Users\BenDe\GitRepos\MAM-basics`, holding `py/accgram/...` and `py/tests/`; the
artifact primary is `C:\Users\BenDe\GitRepos\wlc-utils`, holding `out/` and `gh-pages/`. A phase
here writes into both, so the check is two checks — and the page next door,
`maqaf_nonfinal_accents_page.py`, is in MAM-basics while `maqaf-nonfinal-accents.html` is here.

### What actually landed

- **`chanted_word_accents.merkha_tipexa_discrepancy`'s `open_question` cites #86, not #82.**
  Phase 1 filed the §233/§241 surplus under #82, whose subject is Yeivin's two Deuteronomy 33
  maqaf readings for the LC. This is the **one line** `out/accgram/chanted-word-accents.json`
  moves, and it is a correction worth having whatever happens to the page.
- **Issue [#86](https://github.com/bdenckla/wlc-utils/issues/86)**, "Yeivin-inventory questions
  the chanted-word-accents survey raises (not #82)" — the §233/§241 surplus, the
  `(MERKHA, SILLUQ)` and `(QADMA, ZAQEF_QATAN)` citations, the METHIGAZAQEF boundary crossings,
  `ne8:7`'s merkha with legarmeh, Job's four prose-frame `qadma darga`, and the
  1,353-vs-1,160 reconciliation between the two surveys (198 metigah-zaqef + 5 two-marks-on-one-
  letter), which Ben had already ruled off the page before the page itself went.
  **The boundary crossings were answered on 2026-08-03** and the answer is a comment on that
  issue; §7's bullet has it. The 1,353-vs-1,160 arithmetic is untouched by that answer, MAM having
  had no space crossing to lose. The issue's other items stand.
- **A docstring note in `chanted_word_accents`** recording that a page was built and dropped, so
  the absence of one reads as a decision rather than an omission.

### What was reverted

`py/accgram/chanted_word_accents_page.py` and `gh-pages/accgram/chanted-word-accents.html` are
deleted; `main_accgram.py` and `printed_decalogue_strands.py` are back at their committed state,
which takes with them the `generate-html-chanted-word-accents` subcommand, the `_HTML_GENERATORS`
entry and the `ROM_MAYELA` / `ROM_AZLA` constants the pair table needed.
**`survey-chanted-word-accents` is restored** and is again the only way to write the survey JSON.

### What was verified, before and after the withdrawal

Before: the page rendered, its `pin_claims` passed (including a re-derivation of
`koren_dt_elyon`'s compound through `transcription_parse.check`), `run-prose` and
`run-printed-decalogue` were byte-identical, and the whole `generate-html` batch was
byte-identical against `f0dbbc0`. That verification is now moot except for the one JSON line.

After the revert, and this is what stands:

1. **`survey-chanted-word-accents` re-run: `out/accgram/chanted-word-accents.json` differs from
   the committed file by the single `open_question` line.**
2. **`.venv/Scripts/pytest.exe py/tests`: 487 passed, 5 skipped.** Run with `WLC_SIBLINGS_ROOT`
   set — without it an agent worktree cannot reach `../MAM-simple` and thirteen tests fail with
   twenty-three errors that have nothing to do with this plan.
3. **black** clean on `chanted_word_accents.py`, the only Python file still changed.
4. **No test was added**, and none should be: the survey's Yeivin assertions already are the
   differential check against an independent oracle.

### Generated outputs: what moved and what deliberately did not

| file | moved? |
| --- | --- |
| `out/accgram/chanted-word-accents.json` | yes — one line, the #82 → #86 citation |
| `gh-pages/accgram/chanted-word-accents.html` | built and **deleted**; never committed |
| `out/accgram/prose/*_ag.json` | **no** |
| `out/accgram/printed-decalogue/_printed_decalogue.json` | **no** |
| `out/accgram/maqaf-nonfinal-accents.json` and its page | **no** — and they are `0ab2c6a`'s and Ben's, not this plan's |
| everything else under `out/` and `gh-pages/` | not touched |

### The exact next phase

**Rewritten 2026-08-03.** Until then this section put the promotion question — should a chanted
word whose accent pair no section of Yeivin's prose inventory names be **ungrammatical**? — and
made the 13 newly-ungrammatical MAM chanted words listed below into the argument for settling #86
before anything else. **Ben answered the question on 2026-08-03**, and §6 decision 5 has his words: for
MAM, not ungrammatical, for the time being, with every divergence still recorded. What follows
replaces the ask. The figures it stood on did not move, and are kept below.

**Phase 4, as §5 now states it — whitelist MAM's residue and go on recording it.** The 13 become
whitelist entries: `qadma darga` ×6 and `merkha silluq` ×5 as policy, at configuration level;
ne8:7's `merkha munax` and ek16:12's `merkha pashta` as per-verse exceptions, whose mechanism `§10`
has since settled. **No `status` may move in any corpus** — that is the phase's test, and
`mam_residue` must not shrink either.

**Phase 5 is done — WLC's residue as an unlinked page**, built the morning of 2026-08-03:
`gh-pages/accgram/wlc-chanted-word-residue.html`, wlc-utils `43890f8` with the generator in
MAM-basics `5fb9a69`, deliberately outside `goerwitz.html` and `almost-errors.html`. Ben's ruling
reaches MAM and not WLC's different set, and the page is what he asked for there instead. `§5`'s
Phase 5 entry has the execution record.

What Phase 4 starts from — and Phase 5 started from — all of it in tracked artifacts today:

- **MAM's residue is 18**, and after the five telisha-gedolah words that `lexical_validation`
  already whitelists, **13 chanted words in the consensus text are what a promotion would have
  made newly ungrammatical**: `qadma darga` ×6 (four of them Job's prose frame), `merkha silluq`
  ×5, `merkha munax` ×1 (ne8:7, which is also a legarmeh passage), `merkha pashta` ×1 (ek16:12).
  Those 13 are now Phase 4's whitelist entries.

  **#86 was settled later the same day, and it takes those 13 down to 2 — read this before
  writing a whitelist.** The residue is **12**, and six of the eighteen went not to a whitelist
  but to Yeivin: **ITM §256** names the six `qadma darga`, and Job's four prose-frame ואמלטה are
  his own example, so the entry was simply missing from `YEIVIN_ENTRIES` and is now there as a
  closed list that matches exactly. Five more of the twelve are compounds found by a maqaf that
  does **not** join two atoms into one chanted word — ITM §357's and CoS Ch. 1 §43's maqaf
  written after an atom that has its own accent and a gaʿya after that accent, measured by
  `chanted_word_accents.maqaf_after_gaya` at 13 of MAM's 22 compounds with their accents split
  across atoms. The four `merkha silluq` שלף־חרב and ek16:12's `merkha pashta` are among them.
  So Phase 4's list is **ne8:7 ושרביה and ca8:6 שלהבתיה**, both atomic, and its first question is
  now whether a maqaf-after-gaʿya compound belongs on a whitelist at all rather than in the
  `kind` that says what it is. `mam_residue` shrank from 18 to 12 in `d3d656e`, which is the
  measurement moving under a source correction, not the whitelist eroding it. `§10` then settled
  the exception mechanism, ran ca8:6's owed search (`521e8dc` — both books silent, so Phase 4 may
  write ca8:6's entry), and holds ne8:7 on MAM-basics#215.
- **WLC's residue is 28, in 19 distinct pairs** — re-derived 2026-08-03 from
  `out/accgram/chanted-word-accents.json`; the larger figure this bullet was first written with
  predates ITM §256's entry, whose `d3d656e` regeneration took the six `qadma darga` rows out — a
  different set that neither contains nor is contained by MAM's. Its
  own shapes — `munax munax` at gn36:13, ek8:6, 1c27:14 and 2c1:11 among them — are facts about
  the Westminster transcription rather than about the accentuation. That is what Phase 5's page
  shows, and it is why WLC's residue is worth a page where MAM's is worth a whitelist.
- **Three printed-Decalogue chanted verses carry a null `itm_section` today**:
  `koren_dt_elyon` verse 3 (`munax munax`, `clean`), and `simtiq_ex_taxton` verses 2
  (`munax merkha`, `clean`) and 3 (`munax qadma`, already `ungrammatical`). That is the whole
  blast radius on that path, and `koren_dt_elyon` is the case that motivated the plan. All three
  stay as they are: Phase 4 moves no verdict.

**Before starting: read §6, decision 5 above all, and check main and the working tree in BOTH
primaries** — `C:\Users\BenDe\GitRepos\MAM-basics` for the code (`py/accgram/...`, `py/tests/`)
and `C:\Users\BenDe\GitRepos\wlc-utils` for the artifacts (`out/`, `gh-pages/`). A phase here
touches both, and the parallel-edit collision this section records is what killed Phase 3.
**#86 no longer gates the work**; decision 5 says what changed about it and what did not.

---

## 10. The two one-timers: mechanism settled, ek16:12 dissolved, ne8:7 held (2026-08-03)

This is the "separate task" §5's Phase 4 entry and §6 decision 1's qualification both defer the
per-verse mechanism to. It took up MAM's two one-timers — `merkha munax` at ne8:7 and `merkha
pashta` at ek16:12 — and **neither ends as a per-verse exception written today.** One dissolved
while the task ran; the other is held on a defect the task found.

### ek16:12 is not a one-timer at all — `007e708` had already answered it

Ezekiel 16:12's ו֥אתן־נ֙זם֙ is one of the five compounds `mam_residue.accounted_for_by_maqaf_after_gaya`
sets aside: ITM §357's and CoS Ch. 1 §43's maqaf written after an atom that has its own accent and
a gaʿya after that accent. **ואתן־נזם is a chanted word** on the only test there is — a maqaf is
written in it — and it does have two accent tokens. What §357 settles is where the second token
comes from: וָ֥אֶתֵּֽן keeps the accent it has, the gaʿya after that accent having had to be marked,
so the merkha is not a secondary accent of the kind §§233 and 241 describe.

**What that maqaf signifies is unsettled in both books, and the name does not wait on it.** Yeivin's
"the word must be joined to the following word" reads as denying a pause rather than as making one
accented unit: he writes these very compounds with a **space** at §354 — Ezekiel 1:4 ונגה לו, Ruth
1:21 הרע לי, 1 Kings 2:8 ואשבע לו — where a servant on one chanted word before its mafsik on the
next is the ordinary relation. Breuer CoS Ch. 1 §43 records that "different views have been
expressed" about this maqaf, calls the mark a *mesharet* and leaves the maqaf out of the book, while
Ch. 9 §37 points the other way, that an ordinary-order mark cannot stand in a hyphenated word. The
two are not squared by either book. **An earlier draft of this section argued the opposite way, from
§357's "joined", and that argument is withdrawn**: it settled the name on an interpretation, which
is exactly what the terminology rule forbids. MAM
has וָ֥אֶתֵּֽן־נֶ֙זֶם֙ — a merkha, then a meteg, then the maqaf — and that meteg between the accent
and the maqaf is Breuer's test. So וָ֥אֶתֵּֽן has a merkha as its accent and נֶ֙זֶם֙ has the pashta,
which is also how WLC and UXLC mark the pair, as the two chanted words וָאֶתֵּ֥ן  נֶ֙זֶם֙ with no
maqaf between them. The merkha stands on a different syllable in each — the opening וָ֥ in MAM, the
stressed תֵּ֥ן in WLC and UXLC — but all three have one on that atom. **No exception is owed, and
none should be written.**

**The reading this replaces, recorded so it is not reinstated.** Before `007e708` was read, the
same marks were taken for ITM §241's phenomenon with a merkha where Yeivin's five have a mahapakh:
the merkha in gaʿya position on the opening syllable וָ֥, the meteg marking the stress of תֵּֽן, and
the pashta the compound's one accent. It fits the marks, and §241's "an open syllable suitable for
gaʿya" fits וָ. What defeats it is that §357 explains the same marks **and** explains why WLC and
UXLC have a merkha on that atom too, which the §241 reading leaves as a coincidence.

**A configuration-level `merkha pashta` allowance would have been wrong either way**, and the
reason is worth keeping. The pair occurs once more anywhere in this survey, at **Ex 10:13 in WLC**:
רוּ֥חַ־קָדִים֙, where UXLC and MAM both instead have a meteg — רֽוּחַ־קָדִים֙. WLC's is a
Westminster reading that both the correction of WLC and the consensus text reject, and decision 2
wants the WLC flag to keep exactly that visible. A whitelist keyed on the bare token pair cannot
tell the two apart.

### ne8:7 is held on MAM-basics#215, because MAM does not have the pair the survey names

`mam_residue.left_over_after_both` reports ne8:7 ושר֥בי֣ה as `merkha munax`. **WLC and UXLC report
the same chanted word as `merkha legarmeh`**, and the disagreement is an artifact, not a reading:
MAM-simple sets the Unicode PASEQ (U+05C0) as its own space-delimited element where WLC and UXLC
attach it to the word, and `prose_scanner`'s two legarmeh rules are `munax {TEXT} paseq` with
`{TEXT}` = `[^ \r\n-]*`, which cannot cross a space. Measured over the code path `scan_corpus`
uses, prose verses only:

| corpus | `LEGARMEH` tokens | lone U+05C0 runs counted as chanted words |
| --- | --- | --- |
| WLC 4.22 | 1,167 | 0 |
| UXLC | 1,169 | 0 |
| MAM-simple | **0** | **1,610**, in 1,461 verses |

So no MAM legarmeh can ever tokenize as one, and MAM's tracked `chanted_words` of 234,676 is 1,610
high (`atomic_chanted_words` 197,890 likewise) — a lone bar satisfies `_run_is_a_chanted_word`.
Nothing on a verdict path reads this, since `prose_run` scans WLC, so it is contained to the
survey — but the survey is the thing whose whole design is that a claim about what the accentuation
does takes MAM. **MAM-basics#215** has it. Ben, 2026-08-03: fix it before Phase 4, and write ne8:7's
exception afterwards, against the sequence MAM actually has.

**The merkha itself is a secondary accent, and is not an artifact of the legarmeh.** MAM has
וְשֵׁרֵ֥בְיָ֣ה ׀: the merkha sits on רֵ֥, an open syllable suitable for gaʿya, and the chanted
word's accent is the munaḥ-legarmeh on the stressed יָ֣ה — the position §221, §253 and §268 all
give for a secondary accent. **MAM-basics#185 is a different question about the same mark**, not
this one: it asks whether the mark is a merkha or a meteg. BHS, BHQ and Koren have a meteg there;
WLC, the Jerusalem Crown, the Simanim Tiqqun and BHL have a merkha; skadish1's S1, C13, L-A,
EVR-II-B-92 and S2 support the merkha. The two meet at one point — if #185 settles on a meteg, this
residue entry disappears on its own, a meteg emitting no token.

### The mechanism, for whoever writes the exception

**Key it on the chanted word's mark run plus the token sequence, and leave the verse reference in a
comment** (Ben, 2026-08-03), as `lexical_validation._WHITELISTED_SAME_LETTER` already does with its
`gn5:29, zp2:15`. `classify_verse(body, tokens)` has no verse reference and must not grow one:
threading a bcv in would change both consumer call sites and would be the thing §6 decision 1
refused, which was naming a chanted word by where it stands rather than by what it has. A mark run
says what the chanted word **has**, and it is far tighter than the sequence alone — Ezekiel 16:12's
`א֥אאֽא-א֙אא֙` cannot match Exodus 10:13's `א֥אא-אאא֙`. The survey then asserts that each exception
matches exactly the expected places in MAM and raises on drift, which is the shape Yeivin's closed
lists already have.

### What is left

MAM's unexplained residue is **two atomic chanted words**: ne8:7 ושר֥בי֣ה (`merkha munax`, held on
MAM-basics#215) and ca8:6 שלה֥בתיה (`merkha silluq`). Both take a per-verse exception, by the
mechanism above.

**ca8:6 is the same in all three corpora, byte for byte** — שַׁלְהֶ֥בֶתְיָֽה׃, one atomic chanted
word, a merkha on the open הֶ֥ and a U+05BD on יָֽ immediately before sof pasuq, so that one is
silluq. A secondary merkha in a silluq's chanted word.

**THE SEARCH BELOW WAS RUN, 2026-08-03, and both books are silent. Phase 4 may write ca8:6's
entry.** The silence is checkable on both sides now rather than observed in passing:

- **ITM.** §209 is the whole statement of silluq's conjunctives — *"Silluq can only be preceded by
  one conjunctive, and this is merka"* — and adds no secondary. §210 is the only "in addition"
  section silluq has: *"In five places, the word bearing silluq has, in addition, a secondary
  accent like ṭifḥa in form"*, which is the mayela. Its stated condition excludes ca8:6 on its own
  terms — *"In these cases silluq has neither ṭifḥa nor a conjunctive before it"* — and Song 8:6
  has the tipeḥa one chanted word earlier, on אֵ֖שׁ. Every section of the form "X as a secondary
  accent on the same word as Y" was enumerated over the full OCR — §§210, 215, 216, 219/221, 223,
  233, 236, 241, 244, 253, 256, 268, 276 — and silluq is in exactly one of them, §210, with the
  mayela. Two near misses are not it: §212's exceptional Mic 6:3, where a merkha is the only accent
  between etnaḥta and silluq but stands on a chanted word of its own; and §373's poetic metigah,
  where the metigah is the secondary mark and the merkha an ordinary servus, which cannot reach
  Song of Songs in any case, that being prose cantillated, and which Yeivin says is in neither A
  nor L nor S.
- **CoS.** Already pinned, and by an entry written for something else. `check_cos_claims.py`'s
  "confirmed as a negative" claim carries Ch. 3 §39, the silluq's servant as a merkha across two
  separate words, and §40, the same-word section, which is the mayela's alone.
- **Neither book discusses Song 8:6's accentuation.** ITM cites the verse once, at §286, and it is
  Rashi on the zaqef gadol of רִשְׁפֵּי; CoS does not cite it.

**And ca8:6 is not a MAM case — it is the one atomic merkha-with-silluq chanted word in any of the
three corpora, and all three have it.** WLC measures 5 of that pair, UXLC 3, MAM 5, and in each
corpus ca8:6 is the lone atomic one while every other is a compound. So the entry Phase 4 writes
rests on a reading a diplomatic transcription and a consensus text agree on, which is firmer ground
than a MAM-only case would be.

The pinning pair is in the code as well: `chanted_word_accents.YEIVIN_ENTRIES` gained a `§209`
entry the same day, a rule and not a count, shaped like `§223` and `§302`, carrying the search
above so the silence sits beside the inventory it bounds. It names no token sequence, so
`NAMED_TOKEN_SEQUENCES` and `mam_residue` are untouched by it.

The task as it stood, kept for what it says about why an assumed silence is not one:

**OUTSTANDING TASK, and Phase 4 should not write ca8:6's entry before it is done: search both books
for a secondary merkha with silluq.** §7's open-question list already recorded that Yeivin appears
to have no section for it — §209 gives silluq one conjunctive, merkha, and names no secondary, and
§210's mayela-with-silluq is a mayela and not a merkha — but that was a by-the-way observation and
not a search. `007e708` then re-pointed `(MERKHA, SILLUQ)` from §233 to §357, which is right for the
four שלף־חרב compounds and **cannot reach ca8:6, which has no maqaf at all**; that commit answered
the compounds and left the atomic case where it stood. So the search is still owed, over the full
ITM OCR at `../MAM-private/masorah-books/books/itm/md-export-of-docx/` and the CoS export at
`../MAM-private/masorah-books/books/cos/md-export-of-docx/`, remembering that both romanize the
accent names differently from this repo and that Breuer's English says "hyphen" and "makaf" far
more often than "maqaf". A silence found by searching is worth recording; the silence assumed here is not yet one.
