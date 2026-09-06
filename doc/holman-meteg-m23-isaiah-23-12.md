# Notes: suggestion M23 (Isaiah 23:12 atom 11, קוּמִי) adds a meteg after the stress

Evidence for the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md),
and specifically for that programme's item 1, which has a plan of its own,
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md).

Captured 2026-09-03 in a plan-mode session of MAM-basics (`C:/Users/BenDe/GitRepos/MAM-basics`,
HEAD `3829585`, clean tree), one of a set of six notes: the M13 note is
[`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md), the
lineup of all 30 meteg suggestions against the mgketer reports is
[`holman-meteg-vs-mgketer.md`](holman-meteg-vs-mgketer.md), and the census report is
[`post-stress-meteg-census-2026-09-03.md`](post-stress-meteg-census-2026-09-03.md). The census
script stays untracked at
`C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-census.py`, its line 49 being a
`sys.path.insert`, which `~/.claude/CLAUDE.md` bans in tracked source at a count of zero per
repository. The six notes were written under `C:/Users/BenDe/.claude/plans/` because concurrent
work in git-tracked areas had not concluded, and were moved into `doc/` on 2026-09-03.

## What M23 says — IMPLEMENTED 2026-09-03

**Status, 2026-09-04: M23 HAS BEEN IMPLEMENTED, and this heading said "not yet
implemented; no edit made" until now.** The Wikisource bot added the meteg on
2026-09-03 as item 3 of
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md),
and item 5 carried it into MAM-parsed and the generated repositories on
2026-09-04. **Nothing in this note decided it, and that part of the old heading
stands**: Ben Denckla had taken all thirty meteg suggestions as a batch before
any of this research was done. M23 is archived as item 6 of that programme, its
disposition keyed `Isa 23:12.11`. Item 7's mgketer refresh removed its diff card
from `mgketer-adds-meteg.html`, which fell from 5 cards to 4.

Record `#mam023` of `gh-pages/holman/table_data_findings.html` (moved there from
the now-retired `holman-ketiv-qere` repo during this session — see the path note in
[`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md)), kind "meteg",
message dated 2026-08-31: Isaiah 23:12 atom 11 of 17. Holman's note reads "Aleppo HAS a Meteg
under Mem". The page's comparison table:

| text (per the findings page) | form |
|---|---|
| MAM | ק֣וּמִי |
| Aleppo Codex | ק֣וּמִֽי |

So the suggestion is to add a meteg on the mem, the syllable after the stress. The verse in
MAM (`MAM-parsed/plain/C1-Isaiah.json` line 8052; `plus/` line 4780 has no note on the atom):

```
ק֣וּמִי עֲבֹ֔רִי גַּם־שָׁ֖ם לֹא־יָנ֥וּחַֽ לָֽךְ׃
```

The munaḥ on the qof is a retracted accent (nesiga): the next chanted word, עֲבֹ֔רִי, is
stressed on its first full syllable, the ḥaṭaf not counting. The meteg M23 adds would sit on
the final open syllable of a chanted word whose stress has retracted to its first syllable.
The same difference is mgketer's record `I23:12#e5e7ccd9`, in
`../MAM-private/mgketer/out-reports/by-type/mgketer-adds-meteg.html`, one of five Tanakh-wide
in that category.

**UXLC records the atom without the meteg**: `../UXLC-utils/in/UXLC-39/Isaiah.xml` line 6790 has
`<w>ק֣וּמִי</w>`. That is a statement about UXLC, not about the Leningrad Codex, which was
not consulted, and a transcription's silence on a gaʿya of this class is near-zero evidence.

## A meteg after the stress is a named class in Yeivin and Breuer, in three types

A meteg on a syllable after the chanted word's primary stress is a described category in both
books, with an index entry in Yeivin and a place in Breuer's taxonomy. Both divide it into the
same three types; Breuer marks two obligatory and one optional. M23's קוּמִי is of the optional
type.

### Yeivin, ITM

Paths are under `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/`;
OCR line numbers drift.

1. **Index** (`Z001-list-of-works-cited.md` near lines 754 and 782), under GAʿYA: "Marked —
   after the accent 325, 332, 338".
2. **§332, "Gaʿya on an Open Syllable after the Accent"** (`N0329.md`, heading line 48, body
   lines 50–73). A chanted word stressed on the penult and ending in an open syllable,
   followed by a chanted word accented on its first syllable, may have gaʿya on that final
   open syllable. Examples: Isaiah 14:31 הֵילִ֤ילִֽי שַׁ֙עַר֙, 2 Kings 1:13 עֲבָדֶ֥יךָֽ, Jeremiah 9:20
   עָ֤לָֽה מָ֙וֶת֙, Isaiah 52:11 ס֤וּרֽוּ. "Only rarely marked. It is most common in early MSS", even
   there "only in scattered places", and not marked in printed texts (lines 64, 71–73). It
   "occurs more often where the vowel of the stress syllable of the second word is preceded
   by *shewa*" (lines 66–69: Genesis 28:2 פַּדֶּ֣נָֽה אֲרָ֔ם, Deuteronomy 32:13, Jeremiah 9:18).
   **קוּמִי עֲבֹרִי is this section's case, in its commoner subtype**, since עֲבֹ֔רִי begins with
   a ḥaṭaf. Ben's adaptation: `../MAM-private/al-hatorah/py/itm/my_yeivin_sec_332.py`.
3. **§338, "Gaʿya on a Closed Syllable with Ṣere after the Accent"** (`N0329.md` line 184;
   `N0338.md` lines 1–9): where the accent retracts and a final ṣere stays, that ṣere has
   gaʿya, "marked both in MSS and in printed texts". Examples: Isaiah 66:3 עֹ֣רֵֽף כֶּ֔לֶב and
   מְבָ֣רֵֽךְ אָ֑וֶן, Isaiah 40:7–8 נָ֣בֵֽל. §308 (`N0304.md` lines 119–164) is the nesiga rule that
   feeds it, adding Isaiah 49:7 לִמְתָ֤עֵֽב and, with furtive pataḥ, Isaiah 63:12 בּ֣וֹקֵֽעַ.
4. **§354** (`N0345.md` line 208): phonetic gaʿya "on the last syllable of a word with
   penultimate stress if it ends with a guttural and the following word begins with *lamed*
   or *nun*", extended to furtive pataḥ at lines 214–216. **This is the rule behind
   יָנ֥וּחַֽ לָֽךְ in the same verse** and behind Isaiah 59:16 וַתּ֤וֹשַֽׁע־לוֹ֙.
5. **§357, "Maqqef after Gaʿya"** (`N0345.md` lines 281–286) enumerates the three contexts as
   one class; `chanted_word_accents.py` already cites it for the maqaf-compound case.
6. **§325** (`N0309.md` line 376): gaʿya before paseq, 1 Kings 2:30 וַיֹּ֥אמֶֽר ׀, "only marked in
   this position in early MSS, and is rare even there".

§342 (`N0342.md` lines 1–30): closed-syllable gaʿya, which covers §338, is marked carefully
and consistently across the early manuscripts; open-syllable gaʿya, which covers §332, "is
not consistent in any single MS". Yeivin gives no per-manuscript figure for the post-stress
subset.

### Breuer, CoS

Paths are under `C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/`.
Breuer's translation spells it "ga'aya"; a grep for "ga'ya" or "gaya" misses him.

1. **Ch. 1 §41** (`C01-S041.md` line 83): the ga'aya "usually appears on one of the syllables
   that precede the cantillation mark; but sometimes it appears on the syllable that follows
   the cantillation", example פדנה.
2. **Ch. 8 §3** (`C08-S001.md` lines 37–93), the ten-type taxonomy, closing with all ten
   appearing "usually before the accent and sometimes after it". The three post-stress
   types: (a) big vowel in a closed syllable, obligatory; (b) the guttural's ga'aya at the
   end of the word, obligatory; (j) big vowel in an open syllable, **optional**.
3. **Ch. 8 §§5–8** (`C08-S001.md` from line 109) is type (a), Yeivin's §338, "always" marked;
   Isaiah 66:3 and 63:12 among the examples.
4. **Ch. 8 §§9–10** (`C08-S001.md` from line 307) is type (b), Yeivin's §354; Isaiah 59:16
   among the examples.
5. **Ch. 8 §§46–47** (`C08-S041.md` from line 117) is type (j), Yeivin's §332, **the קוּמִי
   rule**, graded in three tiers (line 177): "mostly common, when the second word begins with
   a *sheva*" (Examples I, including Isaiah 48:6 שמעת חזה), "less common" before a mile'el
   pashta word (Examples II, including Isaiah 14:31 הילילי שער), otherwise "very rare"
   (Examples III, including Leviticus 20:4). Isaiah 23:12 קוּמִי עֲבֹרִי is in the first tier.
6. **Ch. 8 §2** (`C08-S001.md` lines 19–33): optional ga'ayot "do not appear according to a
   set tradition", vary between manuscripts and within one, and the Ben Asher versus Ben
   Naftali disputes do not touch them.

Neither book says a gaʿya is never marked after the stress; both say the opposite. Neither
discusses a gaʿya after silluq, and the rules for the open-syllable and guttural types each
require a FOLLOWING chanted word, which excludes a verse-final chanted word by construction.

## The census: MAM has a meteg after the stress on 231 chanted words

The algorithm is defined by the untracked census script named at the head of this note,
and its output is
[`post-stress-meteg-census-2026-09-03.md`](post-stress-meteg-census-2026-09-03.md). In brief: for every
chanted word in Phonetic MAM's std-set output
(`../MAM-private/al-hatorah/io/a01-phonetic-std-set/`, the same files
`py/tests/test_final_stress_vs_phonetic_mam.py` reads), the script takes Phonetic MAM's one
stressed syllable per chanted word as the oracle, locates the nuclei of the pointed Hebrew so
the two sides' syllable counts can be checked against each other, and classifies every U+05BD
by whether its syllable is before, in, or after the stressed one. A U+05BD in the stressed
syllable of a chanted word with sof pasuq is the silluq. A furtive pataḥ is a syllable of its
own, as Phonetic MAM has it, so a meteg on the guttural of יָנ֥וּחַֽ is after the stress. Marks
that do not indicate stress (ole, geresh muqdam, the prepositives' and postpositives'
non-helper copies) are ignored for the purpose of the same-letter rule; a meteg sharing a
letter with any other accent, or with any accent inside the stressed syllable, fails the run,
per Ben's ruling that the order of two marks on one letter is undefined. The run of 2026-09-03
had zero such failures and zero syllable-count mismatches over 263,320 chanted words.

**Correction, 2026-09-03: every figure in this census section HAS BEEN DEMOTED to a legacy
comparison baseline, and one sentence below it is withdrawn.** The script's verse-final test
treats a final parsed entry as verse-final even when that entry lacks sof pasuq, so its
silluq-versus-post-stress boundary is wrong wherever a final entry has no sof pasuq. The plan
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md)
records the defect, says not to run or edit the script, and makes its Phase 1 tracked generator
the remeasurement authority. The sentence withdrawn is "The census confirms it: zero metegs
after the stress on any chanted word with sof pasuq", in the post-silluq section below: that is
precisely the claim the defective test cannot support. The 231 total and the per-book lists
stand as the baseline the tracked generator is to be measured against.

| system | chanted words | pre-stress meteg | POST-STRESS meteg | silluq |
|---|---|---|---|---|
| prose (21 books plus Job's frame) | 233,715 | 13,131 | **177** | 18,779 |
| poetic (Psalms, Proverbs, Job's poetry) | 29,605 | 1,814 | **54** | 4,486 |

Post-stress metegs by the accent on the stressed letter: prose munaḥ 72, mahpakh 55, merkha
36, qadma 8, darga 5, telisha qetannah 1 (Leviticus 20:4, the meteg between the stress helper
and the postpositive); poetic munaḥ 34, merkha 13, atnaḥ hafukh 2, mahpakh 2, ṭarḥa 1, yeraḥ
ben yomo 1, illuy 1. Every case is listed by book in the report, with its Phonetic MAM form,
so the Yeivin type of each is readable off the list; the Isaiah 15 are all §332, §338 or
§354 cases, and the poetic 54 are overwhelmingly §338 and §354 shapes (שֹׁמֵ֣עַֽ, אֹ֣הֵֽב, ח֣וֹלֵֽל).

Three things about the count worth knowing:

1. **Stress is one per chanted word.** A meteg on a non-final atom of a maqaf compound is
   classified against the compound's one stress, so the §338 gaʿya on MAM's gray-maqaf
   compound נָ֣בֵֽל־צִ֔יץ at Isaiah 40:7 counts as pre-stress, while the same form at 40:8, where
   MAM has a space, counts as post-stress. Yeivin's §357 is about exactly those compounds.
2. **Dual cantillation counts both strands**, so the two Decalogues can contribute a chanted
   word twice.
3. **The exact shape of M23 occurs in MAM once**: Daniel 7:5 ק֥וּמִֽי אֲכֻ֖לִי, merkha on the qof,
   meteg on the final מִי, next chanted word ḥaṭaf-initial and stressed on its first full
   syllable, Breuer's first tier. Of the other 14 atoms in MAM matching ק + accent + וּמִי,
   none has the meteg; Lamentations 2:19's ק֣וּמִי ׀ רֹ֣נִּי, with munaḥ legarmeh, is the nearest.

MAM is selective within the optional §332 type: of Yeivin's examples it has 2 Kings 1:13
עֲבָדֶ֥יךָֽ, Jeremiah 9:20 עָ֤לָֽה, Isaiah 14:31 and Isaiah 48:6, and lacks the meteg on Isaiah
52:11 ס֤וּרוּ, as Ben's `my_yeivin_sec_332.py` comments already record.

### Existing code on this repo's side

- `py/accgram/chanted_word_accents.py` docstring lines 76–88 and `_gaya_after_accent()` at
  line 424, and `py/accgram/maqaf_nonfinal_accents.py`'s `gaya_after_the_nonfinal_accent()`:
  the meteg-after-the-accent signature for a non-final atom of a maqaf compound, Yeivin §357,
  issue wlc-utils#86. Isaiah 8:17 is the case flagged there where UXLC and WLC have such a
  meteg and MAM has none.
- No tracked FOI or survey classifies metegs by position relative to the stress; the census
  script above is the only such count and is untracked.

## The post-silluq meteg: one case, in the Leningrad Codex, not in MAM

A meteg on a syllable after the silluq would complicate telling meteg from silluq, which
share U+05BD. The record on this:

1. **The one case is 1 Samuel 17:5's verse-final נְחֹֽשֶֽׁת׃**, stressed on the penult, so the
   first U+05BD is the silluq and the second, on the final syllable, is a meteg after it. The
   source is Jacobson, *Chanting the Hebrew Bible*, page 31, which reports it as the only case.
2. **Where it is written down.** `bdenckla/MAM-for-JPS#19` "distinguish meteg from silluq?"
   (December 2021), where David E. S. Stein coins "post-silluq metegs" and Ben notes that UXLC
   has the two marks and MAM "(and perhaps wisely)" has only the silluq;
   `bdenckla/phonetic-hbo#78` "handle when gaʿya comes after silluq", opened 2024-12-15 and
   closed 2025-12-02 with "restricted to that one case in LC that is irrelevant to us", citing
   folio F159A column 3 line 8 (`https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F159A.jpg`)
   and calling the mark a "misleading gaʿya"; `bdenckla/trope#18` and `bdenckla/trope#203`,
   the second being the origin of the `mtgmtg` FOI.
3. **The texts.** WLC 4.22 (`out/wlc422/1verses_03_jsju1s.json`, `N:XO75$E75T00`) and UXLC 3.9
   (`../UXLC-utils/in/UXLC-39/Samuel_1.xml`) have two U+05BD; MAM
   (`out/mam-ws-bot/proto-fmt-2/BA-1Samuel.json`) has one, with no note on the atom. The
   census confirms it: zero metegs after the stress on any chanted word with sof pasuq.
4. **What the code encodes.** Nothing names 1 Samuel 17:5. `py/foi/mtgmtg_explanations.py`
   lines 41–49 records the concern as unfounded for MAM. `py/accgram/meteg_silluq_context.py`'s
   `u05bd_is_silluq()` decides by token position only, never by syllable, so run over UXLC or
   WLC it would call both marks of נְחֹֽשֶֽׁת׃ silluq. Safe today because grammatical claims take
   MAM as their corpus; worth knowing if that function is ever pointed at a diplomatic text.
5. **This is a different question from M23's.** Yeivin's and Breuer's post-stress gaʿya rules
   require a following chanted word, so a post-silluq meteg has no grammatical home in either
   book. A post-stress meteg on a non-final chanted word is a described category in both.

## Where this material goes: a gh-pages page about post-stress meteg, which the M23 card points to

Ben's decision, 2026-09-03. **None of the material in this note goes into the M23 card
itself.** Instead:

1. **A new gh-pages HTML page about the phenomenon of post-stress meteg in general**, not
   about M23: the three types in Yeivin (§§332, 338, 354, with §357 and §325) and Breuer
   (Ch. 8 types a, b and j, the first two obligatory and the third optional), the census
   figures and the per-chanted-word lists behind them, the one-stress-per-chanted-word rule
   and its effect on maqaf compounds, and the post-silluq record (1 Samuel 17:5). The census
   script beside this note is the raw material for the page's numbers and lists; a tracked
   generator will have to replace it, with the same Phonetic MAM oracle, so the page's figures
   regenerate rather than being typed in.
2. **The M23 card points to that page.** The card keeps its comparison table and Holman's
   note, and gains a link to the page; the page is where a reader learns what kind of gaʿya
   the card's meteg is and how common that kind is in MAM.

Which repo hosts the page, and its name, are not decided. The page is about MAM's
accentuation, so MAM-basics' `gh-pages/` tree, where the accgram pages live, is the natural
home, with the Holman card (now in `gh-pages/holman/`) linking across; nothing
here settles that.

**Correction, 2026-09-03: the paragraph above HAS BEEN SUPERSEDED — the host and the name are
decided.** Ben's decision that day, recorded in the plan
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md):
MAM-basics hosts the page, published at its deploy root as `gh-pages/post-stress-meteg.html`,
beside `gh-pages/unicode-proposals.html`, and the M23 card's link is the relative
`../post-stress-meteg.html#m23-isaiah-23-12`. That plan put the page under
`gh-pages/wlc/accgram/` until later the same day, when it moved to the deploy root: the `wlc/`
prefix exists so wlc-utils' 154 frozen redirect stubs can rewrite a prefix onto
`MAM-basics/wlc/<path>`, a page published here after the 2026-08-17 move earns no stub, and the
page does not take WLC as its corpus.

## What this leaves for Ben to decide about M23

**Correction, 2026-09-03: nothing was left to decide, and this section HAS BEEN
DEMOTED to background.** Ben stated that day that he is taking all thirty
Holman meteg suggestions, M23's addition among them, and that the acceptance
was settled before this research began: meteg-after-primary-stress is, in his
words, “an interesting and not-that-common phenomenon”, and the research “was
not to determine whether we want to take the suggestion (we'd already decided
that) but to provide background on that phenomenon.” So this section's heading
and its opening sentence name a question that was not in fact open. The three
facts below stand, as background on the phenomenon rather than as inputs to a
disposition.

Nothing here says whether to accept M23. The facts that bear on it:

1. The Aleppo Codex reading, per Holman's page and its image `mam_img/mam023_01.png`, is a
   §332 / Ch. 8 §46 gaʿya in its commonest subtype, and MAM has that subtype elsewhere
   (Isaiah 14:31, Isaiah 48:6, 2 Kings 1:13, Jeremiah 9:20, Daniel 7:5).
2. Both books call this type optional and manuscript-dependent, and Yeivin says printed texts
   omit it. MAM's practice within the type is selective, and the rule MAM follows for including
   or omitting such a gaʿya is not written down anywhere found in this session. Deciding M23 on
   principle would mean stating that rule; deciding it on the manuscript would mean following
   the Aleppo Codex here as MAM evidently does at Isaiah 14:31.
3. UXLC's silence on the meteg is near-zero evidence, this being exactly the class of fine
   gaʿya a transcription most readily drops.

## How to re-establish the findings

- The verse: search `MAM-parsed/plain/C1-Isaiah.json` for `ק֣וּמִי עֲבֹ֔רִי`; one hit expected.
- The census: run the script as its docstring says; it exits nonzero on any failure or
  mismatch and rewrites the report. Figures above are from MAM-private's state on 2026-09-03.
- The קוּמִי shape: ripgrep `ק[\x{0591}-\x{05AE}]וּמִ[\x{0591}-\x{05AE}\x{05BD}]?י` over
  `MAM-parsed/plain/`; 15 hits, exactly one with the meteg, Daniel 7:5.
- The 1 Samuel 17:5 record: `gh issue view 78 --repo bdenckla/phonetic-hbo` and
  `gh issue view 19 --repo bdenckla/MAM-for-JPS`.
- Yeivin and Breuer: grep the two `md-export-of-docx` trees for `after the accent`, and
  Breuer's for `ga'aya`; the section files named above.
