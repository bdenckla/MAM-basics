# CLAUDE.md

## Hebrew marks go in MAM-normal order, not Unicode-normal order — never run NFC over them

Two orders exist for the combining marks of one base-letter cluster, and they differ on where the
dagesh sits:

- **MAM-normal order**, the one this repo uses. Shin dot, sin dot, dagesh/mapiq, rafe, then every
  other mark in the relative order it already had. Spelled out and implemented in
  `py/mb_cmn/uni_denorm.py` — `give_std_mark_order` is the authority, `has_std_mark_order` the
  predicate. The code calls it "(our) standard mark order" and its combining-class table "SBL2",
  after the appendix to the SBL Hebrew Font manual, so grep for **std mark order** and **SBL2** as
  well as for this section's heading.
- **Unicode-normal order**, what `unicodedata.normalize` produces from the canonical combining
  classes (qamats 18, holam 19, dagesh 21, meteg 22). It puts the dagesh **after** the vowel.

**Never call `unicodedata.normalize` (NFC, NFD, any form) on Hebrew.** When two strings that should
match do not, put both through `give_std_mark_order`; do not paper over it by normalizing. The two
orders render identically, so nothing looks wrong on the page and the defect surfaces only where
something compares bytes.

MAM's shipped data is entirely in MAM-normal order — checked 2026-08-04, `has_std_mark_order` true
for all 87 files of `MAM-parsed/plus/`, `MAM-parsed/plain/` and `MAM-for-Sefaria/csv/`. So a cluster
in the other order is always something hand-authored, and **the way in is a paste through anything
that normalizes, a browser above all**. Hebrew you did not lift from the data is the thing to
suspect. There is no lint over hand-authored source here — `py/py_misc/uni_check.py` and
`py/py_misc/check_mpplus.py` check data, and `py/foi/foiz_wt_unicode.py` reports
`NON_STANDARD_MARK_ORDER` as a feature of interest — so the check is yours to run.

Scope: only those four marks have a declared place. A vowel and an accent pass in either order, so
`has_std_mark_order` says nothing about which of them comes first.

**This section is back, not new.** It stood in `CLAUDE.md` and `.github/copilot-instructions.md`
until both were disabled on 2026-05-19 and deleted in `b1fa115` on 2026-08-03. `codex-index-aleppo`
and `codex-index-cam1753` carry near-verbatim copies of the deleted wording, both pointing back at
`uni_denorm.py` in this repo — so the rule survived everywhere except the repo that hosts its
implementation. On 2026-08-04, one day after the deletion, three NFC-ordered clusters were found in
a hand-authored file here. That is why it is worth the tokens.

## Invoke the `hebrew-prose` skill before writing or editing prose about accentuation

That user-level skill (`~/.claude/skills/hebrew-prose/`, tracked in `github-misc` at
`dot-claude/skills/`) is the canonical, single home for the rules the sections below and
`printed_decalogue_strands.py`'s docstring state — atom vs chanted word, the one-scale maqaf rule,
which corpus a claim takes, the banned verbs and framings, where Yeivin and Breuer live, how to
verify a page's numbers. It loads on demand rather than every session, so it can hold the full
statement; the sections here stay as pointers, and **a rule change goes into the skill first**.

## The MAM introduction is mirrored at `in/mam-ws-intro/` — read it, do not fetch it

Hebrew Wikisource's introduction to MAM is consulted constantly here, and since 2026-08-31 all
thirteen of its pages are mirrored locally as verbatim wikitext, one `.mediawiki` file each.
Refresh with `.venv/Scripts/python.exe py/main_download.py fr-ws-intro`, which is deliberately
**separate** from `fr-wikisource` (Ben's decision, 2026-08-31): the books and the introduction
have unrelated refresh rhythms, and nothing downstream reparses when the introduction moves.

| File under `in/mam-ws-intro/` | Wikisource subpage |
|---|---|
| `root.mediawiki` | the introduction's own root page |
| `summary.mediawiki` | `/תקציר` |
| `ch1` … `ch5.mediawiki` | `/פרק א` … `/פרק ה` |
| `appendices.mediawiki` | `/נספחים` — the sigil roster `doc/sigil-decoding.md` leans on |
| `index-aleppo.mediawiki` | `/מפתח לכתר ארם צובה` |
| `index-leningrad.mediawiki` | `/מפתח לכתי"ל` |
| `westminster-typing.mediawiki` | `/מידע טכני על הקלדת וסטמינסטר` |
| `data-sheet-guide.mediawiki` | `/מדריך טכני לגיליון הנתונים` |
| `technical-guide.mediawiki` | `/מדריך טכני` |

Three things about it are worth knowing before you touch it:

1. **Never summarize-fetch these pages, mirror or no mirror.** That is what the mirror is for.
   `doc/sigil-decoding.md`'s source #1 records what a summarizing fetch did to the sigil roster
   on 2026-08-06, and the mirrored wikitext is where you can see what it flattened.
2. **This tree is exempt from the mark-order rule at the top of this file.** It is hand-authored
   wiki prose, so clusters in Unicode-normal rather than MAM-normal order are what the source
   says, not defects. Do not run `uni_check` or `has_std_mark_order` over it, and never
   normalize on refresh — the files are byte-verbatim by design.
3. **A mirror goes stale in a way `in/mam-ws/` does not.** The books move when Ben edits them;
   the introduction moves when Avi Kadish does, unannounced — four of the thirteen pages were
   edited in August 2026 alone. `manifest.json` beside the pages records each one's revision id
   and timestamp, so staleness is checkable without a network call.

**`index-aleppo.mediawiki` and `index-leningrad.mediawiki` were never meant to match what
`py/main_ac_wikisource_page.py` and `py/main_lenin_wikisource_page.py` generate — do not treat
the difference as drift.** Ben, 2026-08-31: those generators' `index.wiki` outputs, in the
sibling codex-index-aleppo and codex-index-leningrad, "were only ever intended to be starting
points for manual work on Wikisource." The published pages are that manual work. So the gap is
the intended transformation, there is no sync to maintain in either direction, and **no test or
lint should compare the two.**

The measurements say the same thing, and are worth quoting because the gap is much wider than
"a wrapper around a generated body" — re-establish them with
`py/main_ac_wikisource_page.py` and `py/main_lenin_wikisource_page.py`, then compare their
output against this mirror. Of the Aleppo generator's 700 lines, **26 (4%)** survive into the
live page; of the Leningrad generator's 1,135 lines, **94 (8%)** do. codex-index-aleppo also
keeps two snapshots of the hand work itself, `aleppo-wiki/Wikisource-manual-initial.txt` (63
lines, carrying `{{בעבודה}}`) and `Wikisource-manual-final.txt` (713 lines, **97%** of whose
lines are in the live page) — which is the pipeline written down: generate raw material, then
build the page by hand from it. The generated file's overlap with the hand-made line is the
same 26 lines whether measured against the initial snapshot, the final snapshot or today's live
page, so the hand work left the generated form immediately and has never gone back to it.
codex-index-leningrad keeps no such snapshots.

## Rendered-prose conventions: `py/accgram/printed_decalogue_strands.py`'s module docstring

That docstring is where the editorial conventions for accgram's **rendered prose** are recorded
— strand names in Hebrew letters and never transliterated, the two signal-word sets, atom vs
chanted word, the single-sourced `ROM_*` romanizations and their italic wrapper, "the Simanim
Tiqqun" and never a bare "Simanim", real em dashes, no English sentence opening on a Hebrew word.
It lives in the printed-Decalogue trio because that is where each rule was settled, but the rules
are not all trio-specific — its SCOPE paragraph says which are which: read it before writing or
editing prose on **any** accgram page. Nothing referenced it for a long time, so it was
discoverable only by already editing the file it governs.

**A table cell holding Hebrew is declared `dir="rtl"`.** Every such cell of every table on a page,
unless the whole table already is, and without waiting to be asked — right-justification then
follows from having said what the cell holds, which is why the declaration beats a literal
`text-align`. Blank cells in the column included; the English heading left alone; no class and no
stylesheet rule. `maqaf_nonfinal_accents_page`'s `_HEBREW_CELL`, spliced through each table's one
`*_CELL_ATTRS` tuple, is the pattern. This is here as well as in the skill because Ben has had to
say it repeatedly (2026-07-29: "something I find myself telling you about frequently … this should
just be sort of obvious"), and `CLAUDE.md` loads whether or not the skill fires. The fuller
statement, with the companion rule about abbreviating a long accent name in a cell, is the
`hebrew-prose` skill's `references/rendered-prose.md`.

Two of those conventions are claims about Hebrew accentuation rather than about this repo:

**Never a loose "word"** (wlc-utils#81). An **atom** is one written word, between spaces or maqafs
— the thing a maqaf joins to the next. A **chanted word** is a lone atom *or* a whole maqaf
compound: the unit cantillation operates on, normally bearing one accent. Say which you mean, and
name a compound whole (על־פני, לא־תעשה), never a bare half of one. Plain "word" survives for an
ordinary English word, inside quoted or translated source material (which keeps whatever it says),
**and wherever the context already settles which sense is meant** — what wlc-utils#81 bans is a
loose "word" the reader must resolve from nothing, so the qualifier is owed where the sense is in
doubt and is noise where it is not. A table heading is read with its column, so `Word` over a
column of Hebrew forms is right whether they are simple, compound or mixed (Ben, 2026-07-29); the
sense can still go in the heading's hover text, as the one-letter appendix's does.
`MAQAF_IS_THE_LAST_RUNG` is where "atom" is glossed for the reader; that gloss is what licenses
the bare term on the pages. Note that the two senses come apart exactly where the rung below
matters, so the two rules are best read together.

**Maqaf is the last rung of one scale.** Disjunctives, then conjunctives, then maqaf — a maqaf
separates the atom it sits on from the next even less than a conjunctive does, so it carries the
weakest *separating* force on the scale. (Never write a bare "weakest": a maqaf *binds* tightest,
so unqualified it reads as backwards.) There is no second ledger for "word division". A maqaf
difference is counted **once**, at the atom whose marking changed, never as a regrouping plus an
accent; and it is stated as an **exchange with both marks named** — "a maqaf where its Wikisource
strand has a merkha" — never as the absent maqaf alone. Do not define a maqaf as "the atom left
blank of an accent": that is only the normal case, and `koren_dt_elyon`'s `mun-mun` on לא־תעשה is
a maqaf compound whose joined atom keeps its munaḥ — as are the Simanim Tiqqun's two munaḥ-on-לא.
But do not swing the other way either: in the **prose** system a second accent on a compound is
rare, and is largely just a consequence of the compound being one chanted word — the accents found
there are the ones that can be the first of two on an atomic word, which is also Yeivin's short
list of prose "secondary accents" (munaḥ-zaqef, metigah-zaqef, rare merkha/mehuppakh on a tevir
word). The separate case is a maqaf written after a word that keeps its own conjunctive: a
manuscript habit, and one **L is specifically named for** (Yeivin ITM §293). The **poetic** system
is far more willing to put two accents on one chanted word; that asymmetry is a major difference
between the systems, not a detail. `edition_transcription`'s "HOW RARE THAT IS IN PROSE" paragraph
has it with its Yeivin and Breuer citations.

**Yeivin lives in two places and they are not the same.**
`../MAM-private/al-hatorah/py/itm/` is Ben's
*adaptation* — partial, with sections still untranscribed.
`../MAM-private/masorah-books/books/itm/md-export-of-docx/` is
the *full* OCR of the book. That repo was `yeivin-itm` until 2026-07-31, when it was renamed and
Breuer's *Cantillation of Scripture* was merged into it from `breuer-cos`; CoS is the sibling
`../MAM-private/masorah-books/books/cos/md-export-of-docx/`, so both books are still one clone
away, that clone being MAM-private since 2026-08-10. **The `../masorah-books/…` spellings that
remain in `py/accgram/` docstrings and comments are stale by exactly that one directory** — eight
sites in `breuer_word_length.py`, `chanted_word_accents.py`, `edition_transcription.py`,
`maqaf_nonfinal_accents.py` and `maqaf_nonfinal_accents_page.py`, each naming a path that now
reads `../MAM-private/masorah-books/…`. Ben chose this sentence over editing the eight, 2026-08-10,
as he chose the same answer for UXLC.

**The `al-hatorah` citations in `py/accgram/` are stale the same way, and Ben chose the same
answer, 2026-08-11.** That tree moved to `../MAM-private/al-hatorah/` on 2026-08-10 and its clone
came off the disk on 2026-08-11, so `../al-hatorah/…` names nothing on either count. **Seven
sites**, named here so nobody re-derives them: `chanted_word_accents.py:638`, `final_stress.py:5`
and `maqaf_nonfinal_accents.py:112` write `../al-hatorah/py/itm/` and
`../al-hatorah/py/aht_phon…`, which want `../MAM-private/al-hatorah/…`; `breuer_word_length.py:37`,
`:43`, `:106` and `py/tests/test_final_stress_vs_phonetic_mam.py:4` write "al-hatorah's
`io/a01-phonetic-std-set`" and "al-hatorah's `py/aht_phon`", which want `MAM-private/al-hatorah/`
in front of the in-repo path. Two further mentions name the repo with no path in them —
`edition_transcription.py:67` and `final_stress.py:16` — and read correctly as written.
Search the full OCR before concluding Yeivin is silent on something;
a first pass at wlc-utils#76 searched only the adaptation and wrongly reported the maqaf material
absent. The verbatim reader-facing statement is
`MAQAF_IS_THE_LAST_RUNG`; its guardrail comment records the convention it replaced (a 2026-07-25
audit fix that made maqaf differences non-differences) and why that one was wrong, so it does not
get reinstated. Issue wlc-utils#76.

## Five issue trackers: a bare `#NN` here means MAM-basics

wlc-utils' issues were **not** transferred when its Python moved here on 2026-08-01. They keep
their numbers and stay in `bdenckla/wlc-utils`, which is still where they are read, commented on
and closed — 93 of them as of 2026-08-17 (this paragraph long said 88, a count that was already
five short when it was written: #89–#93 were filed 2026-07-31). The trackers unify *going forward* only: **every new issue, including new work on the
moved code, is filed in MAM-basics.**

So in this repo a bare `#NN` names a MAM-basics issue, and a citation of a wlc-utils issue is
written **`wlc-utils#NN`**. The prefix is not decoration: both trackers have issues in the 1-88
range, and several numbers name quite unrelated things in each — wlc-utils#52 is the printed
Decalogue where MAM-basics #52 asks about a meteg in Ezekiel, wlc-utils#69 the hand transcriptions
where MAM-basics #69 is a CSS URL, wlc-utils#75 making maqaf a token of its own where MAM-basics
#75 is the `mb_cmn/paths.py` convention. The moved code's 326 bare citations were prefixed on
2026-08-02.

**UXLC-utils is the third tracker and works the same way.** Its issues were not transferred when
its Python moved here on 2026-08-03 either — 56 of them as of 2026-08-18, numbered 1–56, still
read, commented on and closed in `bdenckla/UXLC-utils`. So a citation of a UXLC-utils issue is
written **`UXLC-utils#NN`**, and here the whole numbered range collides: UXLC-utils#19 removes the
CLC note fallbacks where MAM-basics #19 asks for a no-args mode in `main_diff_mpp`, UXLC-utils#29
encodes the pasoleg-tokenization verses where MAM-basics #29 wants mgketer links, UXLC-utils#48
lets the editor simplify a reiterated note-target word where MAM-basics #48 is a space before sof
pasuq in Isaiah 44:24. The moved code's 50 bare citations were prefixed on 2026-08-18, across
eight `py/clc/` modules and `py/main_clc_download_notes.py`.

**holman-ketiv-qere is the fourth tracker.** Its Python moved here on 2026-08-18 and its issues
were not transferred either — **81 of them, numbered 1–81, 60 open**, measured 2026-08-18, still
read, commented on and closed in `bdenckla/holman-ketiv-qere`. So a citation of one is written
**`holman-ketiv-qere#NN`**, and the whole numbered range collides, all 81:
holman-ketiv-qere#4 is row 13's 2 Samuel 11:24 ויראו where MAM-basics #4 produces MIDI of a trope
realization, holman-ketiv-qere#48 is row 41's Jeremiah 17:11 ימו where MAM-basics #48 is a space
before sof pasuq in Isaiah 44:24, holman-ketiv-qere#75 is row 65's Ezekiel 40:34 ואלמו where
MAM-basics #75 is the `mb_cmn/paths.py` convention. Most of holman-ketiv-qere's issues are one per
review row, titled "row NN Book C:V FORM MAM qere", and `io/table_row_github_issues.json` holds
that mapping. **Six numbers became four-way collisions when holman-ketiv-qere's tracker was
added** — #19, #29, #48, #52, #69 and #75, each already cited above as a wlc-utils or a
UXLC-utils collision.

**Unlike the two moves that had citations to prefix — wlc-utils' 326 and UXLC-utils' 50 —
holman-ketiv-qere's move had nothing to prefix**, which is worth stating because the arithmetic
that predicts otherwise is so easy to do. Phase 6 read every `#`-plus-digit site in
the 60 files that moved and found no citation of any tracker among them: 19 CSS hex colours in
`py/py_render/rt_assets.py`, and the `#2026.08.05-6` UXLC **change** anchor in
`py/hkq_cmn/uxlc_change_records.py`. The rest of holman-ketiv-qere's pre-move `py/` carried eight
more sites, and every one is disposed of rather than moved. Six sat in `py/mb_cmn/`, which was a
pure deletion: four lines of `hebrew_accents.py` citing Yeivin *ITM* as `#194`, `#358` and `#361`,
and two of `paths.py`, a `#75` naming MAM-basics' paths convention and an already-prefixed
`wlc-utils#48`. The other two are both `#187`, naming MAM-basics' NFC convention — one in
`main_test.py`, which disappeared, one in `test_h_dot_below_nfc.py`, which collided with this
repo's copy. **A repo can move its whole
Python and still owe this section nothing but a clause** — count the citations, never the files.

**book-of-job is the fifth tracker.** Its Python moved here on 2026-08-19 and its issues were not
transferred either — **61 of them, numbered 1–61 with no gaps, 19 open**, measured 2026-08-22,
still read, commented on and closed in `bdenckla/book-of-job`. So a citation of one is written
**`book-of-job#NN`**, and the numbered range collides from #1 upward: book-of-job#1 studies UXLC
changes in Job where MAM-basics #1 syllabifies pointed Hebrew, book-of-job#7 shows only the first
five of each group where MAM-basics #7 adds `main_diff_mpp.py`. **Its issues take the shape
holman-ketiv-qere's do rather than wlc-utils'**: 37 of the 61 name a Job verse or a quirk-record
SID in the title, 11 of those leading with the verse, as "30:18: add prefix; expand Lenin crop"
does — one issue per quirk record, per manuscript image, or per crop-editor failure. **The bullet
below about modules that render issue references as data does not apply here**: book-of-job's
issue numbers live in its tracker and in prose, and no module of its code turns them into links or
tags, so it has no counterpart to `io/table_row_github_issues.json`. `py/boj_paths.py`'s
`DATA_REPO_NAME` names a sibling repo to build paths from, exactly as `py/hkq_paths.py`'s does,
and is nothing to do with `gh`.

**Four of the six numbers named above are now FIVE-way collisions** — #19, #29, #48 and #52, whose
book-of-job titles are "Add Aleppo Codex image for 34:5", "supplement μA images with manuscript
locations", "details is getting too big" and "30:18: add prefix; expand Lenin crop". **#69 and #75
stay four-way**, book-of-job's numbering stopping at 61.

**book-of-job had nothing to prefix either, which makes it twice running.** Its move was the
programme's largest, 241 modules against holman-ketiv-qere's 60, and it owed this section exactly
as little. All **29** `#`-plus-digit sites in the 268 `.py` that repo tracked before the move are
disposed of without a prefix: **24 are lines of CSS hex colours**, 32 colour tokens on those 24
lines (the two files hold 46 tokens over 36 such lines, the other 12 lines opening with a letter
and so not matching `#`-plus-digit; this sentence said "46 colour tokens between them" until the
2026-08-22 review), in `py/main_gen_aleppo_crop_editor.py` and
`py/main_gen_cam1753_crop_editor.py`; **four are Yeivin
*ITM* section numbers** — `#194`, `#358` and `#361` — in the `mb_cmn/hebrew_accents.py` copy Phase
4 deleted, the same four lines holman-ketiv-qere's copy carried; and the twenty-ninth,
`py/author_boj_util/qr_relations.py:75`, was already written out in full as
`bdenckla/wlc-utils#43`. book-of-job's copy of `mb_cmn/` held no `paths.py` and its
`test_h_dot_below_nfc.py` cited nothing, so even the two `#187` sites and the `#75` that
holman-ketiv-qere's move disposed of have no counterpart here. **Two moves of very different
sizes have now confirmed the same thing: how many citations a move owes is a function of what its
code talks about, never of how many files it is.**

**Five more public trackers were emptied into this one on 2026-08-26, by transfer, and this
section keeps its "Five" name anyway.** Between 18:50 and 19:01 local that evening, Ben
transferred all 27 open issues of five public trackers into MAM-basics, where they are
**#234–#260**: codex-index-cam1753 2 (#234–#235), MAM-simple 2 (#236–#237), codex-index-aleppo 6
(#238–#243), MAM-parsed 8 (#244–#251), MAM-with-doc 9 (#252–#260) — re-derived 2026-08-27 from
the GitHub GraphQL timeline (`TransferredEvent.fromRepository`), all 27 open here that day. A
transferred issue is a MAM-basics issue: its home citation is a bare `#NN`, and the old qualified
form still resolves through GitHub's transfer redirect (Ben observed this during the 2026-08-26
review), so an old-form citation is stale-but-working rather than broken. The first repointing is
done: `doc/sigil-decoding.md` carried `MAM-with-doc#6` at six sites — five citations of its
umbrella issue plus the paragraph justifying their qualifier, all six qualified by `e624139` at
18:27 that same evening, 34 minutes before the transfer — and since 2026-08-27 it cites the issue
as **#257**, its number here (Ben's decision), the justifying paragraph now carrying the
citation's three forms instead. `e624139`'s message, "MAM-with-doc becomes the sixth tracker
cited from this repo", is immutable and stays as the record of those 34 minutes.

**The five source trackers hold closed issues only now** — MAM-with-doc 1, MAM-parsed 12,
MAM-simple 2, codex-index-aleppo 21, codex-index-cam1753 10, 0 open each, measured 2026-08-27 —
and no new issue is filed in any of them: a new public-side issue goes to MAM-basics, and the
private half of that doctrine is recorded at MAM-private `9dfe424` (2026-08-26), new issues to
MAM-private or MAM-basics and nowhere else. A citation of one of those closed issues takes the
repo prefix like every cross-tracker citation in this section — `MAM-parsed#NN`,
`codex-index-aleppo#NN` — and every number in all five closed sets collides with a MAM-basics
number, so the prefix is as non-decorative there as anywhere. **The count in the section's name
stays at five** because the five it counts are unchanged — MAM-basics itself, then wlc-utils,
UXLC-utils, holman-ketiv-qere and book-of-job, whose issues stay put and are still read,
commented on and closed where they are. The newly emptied five are a consolidation record inside
the section, not a sixth through tenth count; settled 2026-08-27, Ben having deferred the
framing, and recorded here so a rename is not re-proposed. Finding 2 of
`doc/review-findings-2026-08-26.md` is the fuller record of the transfer evening.

**This section has had four names.** It was "Two issue trackers" until 2026-08-18, "Three issue
trackers" for part of that same day, "Four issue trackers" from later that day until 2026-08-22,
and "Five issue trackers" since. **Ten sentences across four plans still cite it under one of the
three retired names**, counted 2026-08-22: four in `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`
under "Two issue trackers"; three under "Three issue trackers", being
`doc/PLAN-evacuate-python-from-UXLC-utils.md`'s Status row and its Phase 6 record plus
`doc/PLAN-evacuate-python-programme.md`'s UXLC-utils row; and three under "Four issue trackers",
being `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md`'s Status row and its Phase 6 record
plus `doc/PLAN-evacuate-python-programme.md`'s holman-ketiv-qere row. They are those plans'
execution records, describing the section as it stood when each phase ran, so they are left as
written rather than re-pointed.

Three things a blind sweep gets wrong, so read the surrounding sentence before adding a prefix:

- **Not every `#NN` is an issue.** Yeivin's *ITM* is cited by section number in exactly the same
  shape (`#194`, `#221`, `#246`, and the `#325`–`#391` poetic run), CSS carries hex colours —
  `py/main_gen_aleppo_crop_editor.py` and `py/main_gen_cam1753_crop_editor.py` hold 46 between
  them — and `poetic_ply_grammar.py` numbers the accents of Ps 17:14 as `#7`–`#10`. None of those
  take a prefix. **The CLC code has seven such sites, and each has a real UXLC-utils issue of that
  number waiting to be mistaken for it**: `doc/clc-design.md` numbers its §9 open questions in
  the identical shape, so `clc_collect.py`'s "design doc §9 #2" and `clc_render.py`'s "design doc
  §9 #6" name that list rather than issues #2 and #6; three sites name a UXLC **change** number,
  the 2026.10.19 release's tenth change, written "change #10" and "pending change #10"; and
  `main_uxlc_grammar_test.py`'s #218 and #219 are MAM-basics' own, so they are already right
  bare. `clc_render.py`'s site read "issue #6" until 2026-08-18 and now says "design doc §9 #6,
  not an issue", which is what the `clc_collect.py` site had said all along.
- **Two modules render issue references as DATA about the Holman review, not as citations of a
  tracker, and prefixing them corrupts the rendered table.** `py/py_render/rt_issue_tags.py` and
  `py/hkq_cmn/table_row_github_issues.py` turn `io/table_row_github_issues.json` into the per-row
  issue links, state and tags on holman-ketiv-qere's report pages. Those numbers are
  holman-ketiv-qere issue numbers already, resolved through the `REPO_OWNER` and `REPO_NAME`
  constants that name `bdenckla/holman-ketiv-qere` and are passed to `gh issue list --repo`;
  leave the constants and the rendering alone. Phase 6 of
  `doc/PLAN-evacuate-python-from-holman-ketiv-qere.md` names this as the trap to check for first.
- **`wlc_issue_edit.py` is what keeps the split safe, and its own `#69` is deliberate.** `gh`
  resolves which tracker `issue <number>` names from the checkout it runs in, so `repo` is a
  required argument there rather than an inherited cwd; the bare `#69` in its docstring is the
  worked example of the ambiguity and must stay bare.

wlc-utils' own `doc/`, `in/` and `CLAUDE.md` were left alone — a bare `#NN` read there still meant
a wlc-utils issue, and qualifying those would imply they were ambiguous. Phase 10 of
`doc/PLAN-evacuate-the-rest-of-wlc-utils.md` then deleted that repo's `doc/` and `in/` outright
(2026-08-17), and their byte-identical copies live in **this** repo's `doc/` and `in/` — the six
`doc/` files that arrived 2026-08-12 (`agent-planning-principles.md`,
`edition-transcription-workflow.md`, `review-findings-2026-07-29.md`, `simanim-tanakh-signs.md`,
`PLAN-overall-port-to-python.md`, `PLAN-two-accents-on-one-chanted-word.md`) and the wlc trees
under `in/` (`in/accgram/edition_transcriptions/` above all) — still carrying bare `#NN` issue
citations that mean wlc-utils issues. Those files are one of the two standing exceptions to "a
bare `#NN` here means MAM-basics". wlc-utils' own rewritten `CLAUDE.md` keeps its
bare-`#NN`-means-wlc-utils note for the redirect host itself.

**UXLC-utils' `doc/` is the same exception, still live.** Only that repo's Python left; it keeps
its `doc/` (2 files), `in/` (556), `out/` (27), `gh-pages/` (184) and `data/` (2), measured
2026-08-18. So a bare `#NN` read in its `doc/clc-design.md` still means a UXLC-utils issue, and
nothing there was qualified — for the same reason wlc-utils' `doc/` was left alone, that
qualifying them would imply they were ambiguous.

**holman-ketiv-qere needs no such exception, the first of the four evacuated repos to need none.**
Its `doc/` has two files and neither carries a bare `#NN`. Measured 2026-08-18, the only
`#NN` in any of its tracked prose is the `#19` its `CLAUDE.md` quotes once, in the one backtick
span `gh-pages/JC3 The Biblical Text in the JC Edition #19-ז` that names the two pages sharing
that stem (this said "quotes twice from the filenames" until the 2026-08-22 review's follow-up;
`git grep -c '#19' -- CLAUDE.md` there is 1), and that is a JC Edition article number
rather than an issue — one more instance of the bullet above, met in the repo whose tracker had
just been added.

**book-of-job needs no such exception either, and it goes further than holman-ketiv-qere does.**
Measured 2026-08-22, `git grep -nIE '#[0-9]+'` over its **whole tracked tree** returns nothing at
all — not in its `CLAUDE.md`, its `README.md`, its two `doc/` files or the three `.md` under
`py_ac_loc/`, and not in any of the 701 artifacts under `gh-pages/` and `out/` either. All **784**
files that repo tracks are free of `#NN` in every shape, issue numbers and hex colours alike, so
there is nothing there for a reader to have to disambiguate. **So the four evacuated repos split
two and two**: wlc-utils' `doc/` and `in/` copies now living in this repo and UXLC-utils' own live
`doc/` are the two standing exceptions, and holman-ketiv-qere and book-of-job need none.

## `doc/boj-*.md` are book-of-job's procedures, and they were written for Copilot

Seven files, arrived 2026-08-21 with Phase 4 of `doc/PLAN-evacuate-python-from-book-of-job.md`
(deleted as spent by the 2026-08-29 `doc/` sweep, and in git history),
following the code they describe: `boj-aleppo-word-crops.md`, `boj-cam1753-word-crops.md`,
`boj-leningrad-word-crops.md`, `boj-leningrad-image-scaling.md`,
`boj-image-crop-reproducibility.md`, `boj-viewing-image-metadata.md` and
`boj-quirkrec-comments.md`. They cover cropping a word from the three manuscripts μA, μL and μY,
scaling a μL image to match a μA one, keeping a crop reproducible, reading a PNG's embedded
metadata, and quirk-record comment style. **Read the relevant one before touching
`py/author_boj*`, `py/py_ac_word_image_helper/` or `py/py_cam1753_word_image/`** — nothing in
the code points at them.

Every path in them was repointed on arrival: this repo's code as `py/…`, book-of-job's corpus and
published site as `../book-of-job/…`. **But the prose is Copilot-era and has not been
re-verified.** All seven were `.github/copilot-instructions-*.md` in book-of-job until
2026-08-03. Where one gives a command that conflicts with the global conventions in
`~/.claude/CLAUDE.md` — a `python -c` one-liner, a bare `python`, `PYTHONIOENCODING`, a
`Start-Process` that opens a page rather than handing Ben a `file:///` link — the global
conventions win.

book-of-job keeps two procedures of its own, `doc/opening-html-files.md` and
`doc/reading-mam-simple.md`, both about reading what that repo holds rather than how it is made.

## There is no local `wlc-utils` clone either, and its stub set is frozen

`~/GitRepos/wlc-utils` came off the disk on 2026-08-22 (Ben's decision), the way al-hatorah's
clone did on 2026-08-11. **The repo itself is alive** — `bdenckla/wlc-utils` is the redirect host
for `bdenckla.github.io/wlc-utils/<path>`, and only the local clone went. Nothing routine wanted
it: its 93 issues are read and written with `gh --repo bdenckla/wlc-utils`, which needs no
checkout (`py/wlc_issue_edit.py`); its site deploys from the remote by its own `pages.yml`; and no
test here resolves that sibling.

**The clone came back once, on 2026-08-31, and nothing prevents that happening again — so a clone
found on this disk is not evidence that this section is out of date.** An ad-hoc sweep that day
pulled, cleaned and cloned across `~/GitRepos`, leaving a full 95.6 MB clone rather than the
`--depth 1` one the command below produces. There is **no sync script on this machine** — the only
clone loops are `misc/linux-sh/`, Linux-only, last touched 2026-03-09, driven by a stale 13-name
`repos.txt` that does not even list wlc-utils — so the sweep was run by hand or from a session, and
there is nothing to add an exclusion to. Ben's decision, 2026-08-31: remove the clone again, this
section standing unchanged. Expect recurrence, because the cause is structural: `~/GitRepos` now
holds every non-archived, non-fork repo Ben owns bar `trope`, which makes **archiving the only
thing that actually keeps a repo off this disk** — and wlc-utils cannot use it, staying alive as
the redirect host being the whole reason it is not archived. Re-establish that shape by comparing
`gh repo list bdenckla --json name,isArchived,isFork` against the directories of `~/GitRepos`.
Before rewriting this section on the strength of a clone being present, check whether any session
or `doc/` file records a decision to reverse it, and re-read `py/wlc_redirect/stubs.py`'s
docstring, which states the same decision from the code's side.

**One thing still wants a clone, and its occasion is now rare.**
`py/main_wlc_redirect_stubs.py build --publish`, and `check` with no `--dir`, reach
`py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir`, which is the only site in this tree that
resolves the clone. It raises with the command that fixes it:

```powershell
git clone --depth 1 https://github.com/bdenckla/wlc-utils.git C:\Users\BenDe\GitRepos\wlc-utils
```

**The stub set is frozen at `in/wlc_redirect_pages.json`, the 154 URLs wlc-utils published at the
2026-08-17 move, and it can only shrink.** Until 2026-08-22 both subcommands derived it from the
live `git ls-files gh-pages/wlc`, which anchored the lint to the wrong set: a page published
*here* after the move never had a wlc-utils URL and is cited as a MAM-basics one, so it earns no
stub — but the derivation would have reported the first such page as an old URL about to 404. The
two sets coincided only because nothing had been added under `gh-pages/wlc/` since `f99996f`
(2026-08-12). So a publish is needed only if one of those 154 pages is **renamed or dropped**,
which breaks its stub; `py/tests/test_wlc_redirect_manifest.py` is the half of that lint needing
no clone, and it fires here.

**`../wlc-utils` was dropped from `all-repos.code-workspace` in the same commit, 20 folders to
19** — not tidying: `py/repo_util/repo_selection.py`'s `load_workspace_repo_dirs` raises
`FileNotFoundError` on any listed folder that is not on disk, and it runs before *every* action,
so a stale entry would kill `--run-black`, `--clean-worktrees` and the standards checks alike, not
just the part that names wlc-utils. That is the same three-step the frozen repos took on
2026-08-07 (move out, drop from the workspace file, record it).

The `../wlc-utils` paths in `doc/`'s plans are execution records of what was true when each phase
ran, and are left as written — the answer Ben chose for al-hatorah's and masorah-books' stale
citations too.

## There is no `wlc-koren-12th` repo

`~/GitRepos/wlc-koren-12th` was never a repo of its own. It was a **worktree of wlc-utils** on
branch `claude/koren-12th-site`, which is why it sat flat among the siblings and answered
`git remote -v` with `bdenckla/wlc-utils`; its copies of files such as
`py/accgram/poetic_ply_grammar.py` were the same files on an older branch, never duplicates to
reconcile or keep in sync. Repeated sessions read it as a twin repo and burned a turn
"reconciling" it — that is the whole reason for this note. Deleted 2026-07-27, along with the
fully-merged leftover branches `claude/koren-12th-site` and `claude/festive-napier-38d58d`, both
accepted by `git branch -d` (never `-D`), which is the record that nothing was lost. The only
place the name survives is old session transcripts under `~/.claude/projects/`, which is exactly
where the wrong conclusion kept being copied from.

**General lesson:** a directory sitting flat under `~/GitRepos` is not necessarily a repo. Run
`git -C <dir> rev-parse --git-common-dir` (or `git worktree list` from the repo you suspect)
before treating one as a peer whose files need syncing.

(Moved here from wlc-utils' `CLAUDE.md` on 2026-08-17, when Phase 10 of
`doc/PLAN-evacuate-the-rest-of-wlc-utils.md` shrank that file to redirect-host facts — the
disposition that plan's Phase 0 recorded for it. The note lives on because the transcripts do,
and because all wlc work now happens in this repo.)

## Running tests — always from the repo root

Run tests via the canonical entrypoint, from the repo root (`~/GitRepos/MAM-basics`), never from `py/`:

```bash
.venv/Scripts/python.exe py/main_test.py
```

Sibling-repo paths (MAM-parsed, MAM-simple, MAM-with-doc, MAM-OSIS, MAM-for-Sefaria)
are built from `mb_cmn.paths.repo_root()` / `repos_root()` / `sibling_repo(name)` — a
single `__file__`-relative utility (issue #75), not cwd-relative `"../MAM-parsed"`
literals or ad hoc `Path(__file__).resolve().parents[N]` chains. New path-construction
code should use it too. Exception: a handful of files that get vendored/copied verbatim
into sibling repos (`mb_cmn/read_books_from_mam_parsed_plus.py`, `mb_cmn/provenance.py`,
`mb_misc/write_utils.py`, `mb_sefaria/mam4sef_or_ajf.py`) intentionally keep their
existing cwd-relative or self-contained `__file__`-relative logic instead, so they stay
portable when copied elsewhere without also requiring `mb_cmn/paths.py` to travel with them.

Even so, still run from the repo root, never from `py/`: some in-repo paths (e.g.
`in/mam-ws-bot-edits/...`) remain cwd-relative by design, and the venv itself
(`.venv/Scripts/python.exe`) is a repo-root-relative path. Running pytest from `py/`
(e.g. `cd py && pytest tests/`) breaks these with a plain `FileNotFoundError`, which reads
as a real test failure rather than a wrong-invocation-directory error. On 2026-07-01 this
exact mistake produced 17 misleading test failures that got misdiagnosed as
pre-existing/unrelated bugs.

If a shell has already `cd`'d into `py/` from an earlier command, explicitly `cd` back to
the repo root before running tests — a persistent-cwd shell keeps resolving
repo-root-relative paths wrong otherwise.

**`py/main_test.py` is the only runner — a bare `pytest` is not supported from anywhere,
including the repo root.** `fd2241a` migrated this repo onto that single entrypoint on
purpose. It needs no path configuration because CPython prepends a script's own directory
to `sys.path`, which is exactly why the entrypoint lives in `py/` and not at the root. So
`pytest py/tests` failing with ~34 `ModuleNotFoundError` collection errors (`No module
named 'mb_author'`, ...) is the designed state, not a defect: **do not "fix" it** with a
`pytest.ini` `pythonpath`, a root `conftest.py`, a `.pth`, or `PYTHONPATH`. Each re-creates
the second entrypoint the migration removed. This was reported as a bug on 2026-07-30 and
the report was wrong. The cross-repo rule is user-level CLAUDE.md's "No `sys.path` surgery"
section, which this repo is the worked example for — it is what settled the standard at zero
inserts per repo rather than one. `py/versification_and_cantillation/doc.py`'s module
docstring says the same thing.

**There is no test registry any more, and no file to add a new test to.** `main_test.py`
was a hand-maintained `TEST_MODULE_SPECS` tuple plus a `unittest` loader until 2026-08-01;
it is now a `pytest.main()` wrapper, so pytest discovers `py/tests/` itself. The registry
is gone because of the failure mode it had: an unregistered file does not skip, it reports
nothing at all — worse than the silent-green skip the global rules warn about — and two
files went unrun that way here from the 2026-05-03 migration until 2026-07-30, one of them
edited four times meanwhile.

**Drop a new test file in and it runs, so long as it is named `test_*.py` or `*_test.py`.**
Those two patterns are pytest's default `python_files` and both are in use under
`py/tests/`: this repo's own tests are prefix-named, and the CLC tests that arrived from
UXLC-utils on 2026-08-01 are suffix-named. A file matching neither is the registry's failure
mode back again — nothing collects it and nothing says so. `py/tests/mc_marks.py` is the one
file there matching neither, and rightly so: it is a helper four test modules import
`mc_to_marks` from, not a test.

Arguments pass straight through to pytest, so `-k`, `-x`, `-q`, `--lf` and `--collect-only`
all work; naming a file replaces the default target of the whole `py/tests` tree:

```bash
.venv/Scripts/python.exe py/main_test.py --collect-only -q
```

Both test styles collect natively — this repo's `unittest.TestCase` classes and the
module-level `def test_` functions that arrived with the wlc-utils code — so no test file
was rewritten in either direction.

## Writing tests — differential and lint-shaped only

An audit of git history, comments, and issues across all of Ben's repos (2026-07-25) found
four occasions where a test demonstrably found something, and **zero** recorded cases of a
pre-existing example-based unit test failing later and thereby catching a regression. All
four have one of two shapes. Do not add a test unless it is one of them, or Ben asks.

- **A differential check against an independent oracle** — regenerate the corpus and compare
  against a frozen reference or a second derivation of the same fact. The accgram code that
  arrived from wlc-utils on 2026-08-01 brought two of the four: the PLY parity comparator against
  the frozen C `accents` checker, and the printed-Decalogue transcriptions against their vendored
  strands.
- **A mechanical lint over the tree** — a decidable property of the *source text* rather than
  of behavior (`py/tests/test_h_dot_below_nfc.py`, `py/tests/test_transliterations.py`
  (wlc-utils#26), and the `check_repo_standards.py` scans are this shape).

Otherwise the generated, git-tracked artifact is the test: regenerate it with the real command
and read the diff. Unexplained diffs are failures until explained. This is how the real bugs
here were actually found — `1ef8f51` (#199, a top-level ketiv/qere silently dropped from a
strand) surfaced as wrong text in generated output, not as a red test.

Do not write an example-based unit test that pins one hand-picked case, a string, or a name.
Nothing in the record shows one catching anything, and they have to be dragged through every
terminology rename.

**A missing input must FAIL, never skip.** wlc-utils' `25a7800` removed twenty-one skip guards
that reported green having verified nothing. Skips are a *semantic* channel in the accgram tests
(a skip reports that a page diverges from its strand), so an environment skip mixed in corrupts
the signal. An empty `@parametrize` list also reports as a skip — hence the
`or ["(none committed)"]` fallbacks, which are the failure mechanism and must stay. Reach for
`require_sibling` rather than a "sibling repo not present" skip.

**The `ws_bot` tests are a deliberate exception.** A Wikisource edit is an irreversible,
outward-facing action against a live wiki, and there is no regeneratable artifact to diff
after the fact — so pinning an edit payload before it is sent is worth its cost on those
grounds, not because the general rule has an escape hatch.

The fullest statement of this rule, with the evidence behind it, is in this repo:
`doc/agent-planning-principles.md` §"Generated Outputs Are the Tests". (This sentence said "in the
sibling repo: `wlc-utils/doc/…`" until 2026-08-17 — the file came home with the rest of wlc-utils'
`doc/` in the 2026-08 evacuation, which then deleted wlc-utils' copy.)

**This file is the only instruction file this repo has.** `CLAUDE-disabled.md` and
`.github/copilot-instructions-disabled.md` were deleted on 2026-08-03, when GitHub Copilot
stopped being used; nothing in either was moved here, because it was stale or already said
better in `~/.claude/CLAUDE.md`, in `doc/`, or in the docstring of the module it described.
Both are in git history if a claim in them ever needs checking.
