# Sources and corpora

## The corpora, and which one a claim takes

| | What it is |
| --- | --- |
| **WLC** | The Westminster transcription of **L** — diplomatic. A near-perfect copy of BHS that fixes BHS *transcription* errors. Ben, 2026-09-09: WLC "started life as a transcription of BHS and then became an edition of its own (albeit still *very* close to BHS)"; no version of WLC in play here is a transcription of BHS. |
| **UXLC** | Started as WLC 4.20 via WLC2XML and "diverged considerably from there" — from WLC and from BHS (Ben, 2026-09-09) — but still **not a second hand**, not a second manuscript. |
| **MAM** | A **consensus** text: no single manuscript's reading, but the accentuation the Masoretic tradition converges on. |
| **LC / L** | The manuscript itself — the only one of these with a physical, ambiguous vertical **bar**. |

- **Transcription and diplomatic edition are not distinguished here.** Ben, 2026-09-09: BHS, WLC
  and UXLC "all seek to be transcriptions of the Leningrad Codex, i.e. they are diplomatic
  editions of the Leningrad codex", and "the distinction between a diplomatic edition and a
  transcription is a very fine one, if it distinguishes anything at all." So "edition" for
  UXLC or WLC is not a vocabulary fault; the evidence rule two bullets down is the live one.
- **"Consensus," not "eclectic," and never "an edited text."** The standard contrast is
  *diplomatic* vs *eclectic*; Ben prefers **consensus** for the latter. "An edited text, not a
  manuscript reading" says nothing, since all texts are edited, including single-manuscript ones.
- **MAM is not a Breuer edition.** Breuer's own are the **Horev** edition and the **Jerusalem
  Crown**, which he advised on without detailed involvement (health, per Ben's recollection);
  **Yosef Ofer** did the detailed work on the Crown, framing it as using Breuer's methods, as its
  front matter says. MAM follows Breuer heavily, and attributing a *rule* to Breuer to explain
  something MAM does is fine as long as the inference is visible to the reader. Never "MAM is
  Breuer's edition" — `maqaf_nonfinal_accents{,_page}.py` said exactly that in five places.
- **A claim about what the accentuation DOES counts MAM.** WLC is a flawed transcription of a
  flawed manuscript and its blemishes land in such counts. The worked case: the maqaf-non-final
  survey's headline frequency moved from WLC 4.22 (36,806 compounds, 139 hits) to MAM (36,786;
  233; 0.63%), which also made the accompanying claim true without exception — WLC's Joshua 20:4
  זקני־העיר has its compound's only accent on the non-final atom because the mark on העיר is a
  mid-verse meteg. **Re-read those numbers out of the regenerated JSON before quoting them.**
- **WLC keeps the claims that are about a manuscript**, attributed by name (the two-munaḥ
  compound Koren resembles is in L and not in MAM).
- **WLC, BHS 1997 and BHQ are usually ONE transcription, not three that agree.** Ben,
  2026-08-07, correcting exactly that framing: they "should usually be considered a SINGLE
  transcription, not independent transcripts." So their agreeing corroborates nothing about the
  manuscript — it is one reading counted three times, and treating it as three is how a
  transcription-tradition error gets promoted to a manuscript fact. The bullets above already
  say WLC is "a near-perfect copy of BHS"; this is the same point where BHQ is also in play, and
  it is the one that gets forgotten, because three names look like three checks. The worked
  case is MAM-basics #218's **gn 18:18**, where MAM has ונברכו־בו as one chanted word and WLC
  has ונברכו בו with a space: WLC's **bracket-U** note there says outright that it agrees with
  both BHS 1997 and BHQ on an unexpected reading. That settles that the space is at least as old
  as BHS and is not WLC's alone — and settles nothing about the LC, which is why the verse is
  `st-source: tbd` pending a look at folio 009B rather than `lc`. What DOES corroborate is
  someone reading the manuscript: je 37:10, the same shape, is `lc` because UXLC's note reports
  no maqaf in the image.
- **Sibling corpora are not WLC 4.22.** A UXLC feature is UXLC-real, not WLC-4.22-real; verify
  against `out/wlc422-kq-u` and accgram's `…_ag.json`. MAM differs in **both** directions — it
  lacks WLC's own oddities and adds composites and dual-cant overlays — so it is the wrong corpus
  to harvest for WLC anomalies.
- **CTR is never a precedent.** Ben: "I wouldn't trust CTR on *anything*." Noting what CTR has is
  worth recording; citing it as authority is not. Its own module distrusts it enough to compare at
  glyph level. Printed editions transcribed by hand off a page (SimTiq, Koren) are primary
  observation and DO carry weight.

## Yeivin, *Introduction to the Tiberian Masorah* (ITM)

Two homes, and they are not the same:

- `../MAM-private/masorah-books/books/itm/md-export-of-docx/*.md` — the **full OCR**, one file per
  section-run, plus the source `Introduction to the Tiberian Masorah -- ABBYY FineReader
  export.docx` under `books/itm/src/`. **Search this one.** The repo was `yeivin-itm` until
  2026-07-31, when it was renamed and CoS was merged in, so ITM and CoS share one tree; that tree
  moved out of its own clone into `MAM-private` on 2026-08-10, which is why the path carries that
  extra directory.
- `../MAM-private/al-hatorah/py/itm/` — Ben's **partial adaptation**;
  `my_yeivin_amisc_sec_not_yet_transcribed.py` names what is missing. That tree moved out of its
  own clone into `MAM-private` on 2026-08-10 and the clone came off the disk on 2026-08-11, which
  is why the path carries that extra directory; `bdenckla/al-hatorah` keeps a breadcrumb
  `README.md` and its 124 issues, so an `al-hatorah#NN` citation still resolves. The body text
  there is
  Yeivin's and Revell's, **not Ben's voice** (his footnotes in it are his) — exclude it when
  treating "Ben's own writing" as a style corpus.

A 2026-07-26 session searched only the adaptation and wrongly reported that Yeivin says nothing
about an accent on a maqaf-joined word. ITM romanizes several accent names differently from
accgram, so **grep ITS spellings**. The ga'ya sections are the worked case, and they run the
opposite way from CoS on every term: ITM writes **`gaʿya`** with U+02BF, throughout, while
`ga'ya` with a plain apostrophe returns **ZERO**; its meteg is `metheg` and its siluk `silluq`,
which are exactly the two spellings CoS never uses. Established 2026-09-09; the occurrence
counts came out the same day, on the reasoning recorded at the `makaf` entry below.

Also on disk: `~/OneDrive/Documents/Tanakh/Introduction to the Tiberian Masorah -- ABBYY
FineReader export.docx`, with excerpts under `~/OneDrive/Documents/Tanakh/misc/Yeivin-ITM-misc/`,
and the Hebrew Ofer edition `Yeivin_המסורה למקרא_Ofer-edition_2003.pdf`.

## Breuer, *The Cantillation of Scripture* (CoS, English)

- **CoS shares the `../MAM-private/masorah-books` tree with ITM** (private, for copyright in the
  source material and not for secrecy, with the same sanctioned exception letting public repos
  name it).
  It had a repo of its own, `bdenckla/breuer-cos`, from 2026-07-27 until 2026-07-31, when it was
  merged with its history into what was then `yeivin-itm`, and that repo was renamed
  `masorah-books` for holding both. On 2026-08-10 the whole tree moved into `MAM-private`, and
  `bdenckla/masorah-books`
  kept a breadcrumb `README.md`, its history and its 19 issues, so a `masorah-books#NN` citation
  still resolves there. The six chapter docx are at `books/cos/src/`. **Read the tree's `CLAUDE.md`
  and
  `README.md` before doing anything with CoS**, and its `doc/migration-checklist.md` for what the
  merge did and did not finish.
- **`bdenckla/breuer-cos` is emptied, and there is no local clone — there is nothing to grep
  there.** Ben deleted the clone at `C:/Users/BenDe/GitRepos/breuer-cos` on 2026-08-07, so
  `../breuer-cos` names nothing on disk; on 2026-08-10 the GitHub repo was emptied to a breadcrumb
  `README.md`, its 69 other files deleted, because the copies had gone stale against the live tree
  — 21 of the 57 export files, all three scripts and the Chapter 10 docx differed. The pre-empty
  tree stays in history at commit `54440aa` if a file is ever wanted as an issue was written
  against it. **The repo has been archived since 2026-08-27, so it is read-only.** It stayed
  deliberately unarchived until then, so its issues would keep their numbers and stay writable,
  and Ben's decision of 2026-08-07 was that archiving was the expected end once #2 and #3
  resolved. That end arrived by a different route: on **2026-08-26** #2 and #3 were **transferred
  to MAM-private**, where they are **#13 and #14** and both still open, and the archiving followed
  the next day. So the two issues are writable still, in MAM-private rather than in
  `bdenckla/breuer-cos`. What `bdenckla/breuer-cos` holds now is #1, #4 and #5, all closed — #5
  having been folded into `masorah-books` #7 and #1 into `masorah-books` #15 and #16. Re-establish
  with `gh api repos/bdenckla/breuer-cos --jq .archived` and
  `gh issue list --repo bdenckla/breuer-cos --state all` (both measured 2026-08-31).
- The same six docx remain at `~/OneDrive/Documents/Tanakh/` (the repo copies were copied, not
  moved): `Cantillation of Scripture - Chapters 1 thru 5.docx`, `... 6 thru 8`, `... Chapter 9`,
  `... Chapter 10`, `... Chapter 11`, `... Chapters 12 thru 15`.
- **Fully scanned**: 719 page images at
  `~/OneDrive/Documents/ScansOfBooks/The Cantillation of Scripture - English/`, deliberately not
  copied into the repo.
- **The markdown export is done for all fifteen chapters** (2026-07-27) — 522 sections in 57
  files, `MAM-private/masorah-books/books/cos/md-export-of-docx/C<NN>-S<NNN>.md`, chapter and first
  section
  number both
  zero-padded, ten sections to a file, so Ch. 9 §25 is in `C09-S021.md`. `C00-S000.md` is the
  front matter. **Grep there, never the docx.** Section counts, since a chapter being short is
  otherwise easy to mistake for a conversion failure: Ch. 1 44, 2 75, 3 40, 4 20, 5 10, 6 34,
  7 24, 8 47, 9 40, 10 35, 11 80, 12 8, 13 7, 14 8, 15 50. Chapters 12–14 really are that short —
  they are the Eme"t counterparts of 4, 5 and 6–8, and Breuer says in each that the rules of the
  21 books mostly carry over. Page anchors and the diacritics repair pass are later phases, and
  each has its own issue in `masorah-books`: **#15** for the page anchors, which wants a
  `page_section_map.json` derived from the 719 scans, and **#16** for the diacritics pass, modelled
  on ITM's `books/itm/historical-docs-fix-diacritics/`. `breuer-cos` #1, which staged both, was
  closed on 2026-08-02, the conversion its title names being done. Say which repo, and now which
  CoS diacritics issue: `masorah-books` has an issue #1 of its own, closed, about **ITM's**
  diacritics, and `masorah-books` #16 is the CoS one. **Do not start a later phase unasked.**
- **Two checks run over the export, and a CoS claim should go through them.** Both are
  subcommands of `MAM-private/masorah-books/py/main_ocr.py`, run with the cwd at that tree's own
  root and on that tree's own `.venv`. It has since 2026-08-01 been the only runnable file
  there — running `py/cos/check_cos_claims.py` directly puts `py/cos/` on `sys.path[0]` and fails
  to find `ocr_cmn`.
  `cos-check-claims` is the differential check: every claim about Breuer is pinned to the
  evidence the export has for it — some written by eye from the docx before it was greppable, the
  rest read off the export instead. Its oracles are modules under `MAM-basics/py/`, most of them
  in `py/accgram/` and not all; `py/author_site/post_stress_meteg.py`, added 2026-09-07, is one
  that is not.
  `cos-check-cross-references` is the lint: the internal section references it fails to resolve
  are one class of OCR damage, a range hyphen pushed past its digits, and each of them is
  declared.
  **How many claims there are, how many references resolve and where every oracle lives are in
  `MAM-private/masorah-books/README.md`** — §"What `check_cos_claims.py` found" and §"What
  `check_cross_references.py` found", with the gate figures themselves in §"The tooling and its
  gates" — and are deliberately not restated here. Ben's decision, 2026-09-09, the same day the
  six-row gate table came out of `references/verifying.md`: this entry's claim count had already
  gone stale once and been corrected by github-misc `1925699` on 2026-09-07, and one home is what
  stops that recurring.
  **Add a new claim to `check_cos_claims.py` rather than asserting one in prose**, a
  NEGATIVE claim included: "Breuer says nothing about X" is evidence only if the neighbouring
  sections are pinned for what they DO say.
- **Breuer's English translation mostly says "hyphen."** Grepping the whole
  export for "maqaf" returns ZERO, while "hyphen" runs through the whole book — including all of
  Ch. 7, which is the hyphen chapter. But the translator's transliteration is **`makaf`**, spread
  over several files, and it holds Ch. 7 §1's definition, Ch. 1 §43's "words that have been
  joined by *makaf* are considered as a single word", and Ch. 5 §5's rule for a *methiga* opening
  a word joined by one. The Hebrew מקף occurs in the front matter's note to the English reader
  and nowhere else. This entry said "grep both spellings" until 2026-07-31 and there were three
  all along: grep `hyphen`, `makaf` AND `מקף`, or the topic looks absent when it is not. **The
  occurrence counts came out of this entry and of both ga'ya-spelling entries — ITM's above and
  CoS's below — on 2026-09-09**, Ben's
  decision, with his reason: what these entries are for is knowing which spellings to grep, and
  even one reference using a spelling is worth searching for, so a figure sizing the problem
  bought nothing while giving a re-export something to falsify. Each ZERO stays, being the
  categorical fact its trap rests on.
- **And CoS spells the meteg `ga'aya`, which is the same trap one term over.** Established
  2026-09-09: `ga'aya` runs through the export and is concentrated in Ch. 8, the ga'aya chapter
  (`C08-S001.md` through `C08-S041.md`). Grepping the export for `meteg`, `metheg`, `gaya`,
  `gaʿya` or `silluq` returns **ZERO**, and `ga'ya` returns next to nothing, so the whole
  subject looks absent. Breuer's siluk is `siluk`. And **`methiga` is not a spelling of
  meteg**: it names the servant in the word of a small zaqef (Ch. 5 §§4-6), and does not occur
  in Ch. 8 at all. Ch. 8 §1 is where Breuer separates the two marks, the ga'aya being "always
  written beside a *sheva* or beside an unaccentuated vowel", unlike the siluk. Worked case:
  `MAM-basics/doc/foi-mtgmtg-empty-cell.md`, whose first grep of the export missed Chapter 8
  entirely.
- The docx are ABBYY OCR exports, so `word/document.xml` leaks run-property XML into some `w:t`
  values — strip tags after extracting.
- Ch. 10 §9 covers the Ps 17:14 double tsinnor.
- Ben **dislikes Breuer's transformative framing** and will not have it adopted (see the ban in
  `SKILL.md`), though Breuer's own rules quoted in his own terms keep his wording.

## Two accents on one chanted word: prose vs poetic

This asymmetry is a **major difference between the two systems, not a detail** — state it that
way, and do not treat a prose case as ordinary.

**Prose is stingy.** An accent on a non-final atom of a compound is rare, and largely nothing but
a consequence of the compound being a single chanted word: what turns up there is what can be the
**first of two accents on an atomic word**. That is also Yeivin's own short list of prose
**secondary accents** — *munaḥ*-zaqef (ITM §221, frequent enough to count as a fourth variant of
the zaqef melody), *metigah*-zaqef (§224; *metigah* is in effect a special name for *qadma* used
this way, hence accgram's `METHIGAZAQEF` token, whose middle span deliberately crosses a maqaf),
and rare *merkha*/*mahapakh* on the word of a *tevir* (§§233, 241, about five cases apiece). Ben's
rule and Yeivin's inventory agree.

**A separate prose case, not a grammatical category:** a maqaf written after a word that keeps
its own conjunctive. Yeivin §293 — occasional, "in a number of MSS," commonest with penultimate
stress, "possibly intended to show that the last syllable of the word has no accent." §21 uses it
to **tell manuscripts apart**, and **L is named for it** (ועזר־מצריו, Dt 33:7, "a tradition
somewhat different from the standard"). §357 is the neighbouring case, a maqaf after a word
bearing a ga'ya that follows the accent. So such an accent is neither unheard-of nor evenly
distributed, and *whose habit it is* is part of any question about one. Caveat the survey already
records: two of §293's three L-specific citations (Dt 33:7, Dt 33:3) come out the opposite way in
WLC.

**Poetic is far more willing.** Breuer CoS Ch. 9 gives it §§20–21 (a mafsik plus a servant, and
two servants, in one word), §22 for the governing rule that two marks "appear in one word — in
the same manner in which they are used to appear in two separate words", and §§23–26 for the
secondary *mahapakh*/*merkha*. He notes the maqaf after a secondary *merkha* is usually
**omitted** — the compound written as two words though chanted as one — with "but a few cases"
keeping it: §37 gathers **three**, Job 6:10 ותהי־עוד, Prov. 25:20 מעדה־בגד, and מעללי־אל (Ps.
78:7) from §36.

**Both of those corrections came out of the differential check** (`masorah-books`
`py/cos/check_cos_claims.py`, then `breuer-cos` `scripts/check_cos_claims.py`, 2026-07-27), and
this section had them wrong before it: the span
was written as one §§22–26 doing the work of two, and the cases as two rather than three. Breuer
cites the §§23–26 span himself, twice, in §27; §22 is the *tzinnorit* section. **All fifteen
chapters are now greppable**, so check a CoS claim in the export rather than restating one from
here. `MAM-basics/py/accgram/edition_transcription.py` still has the uncorrected pair, since the
check deliberately leaves the repos it checks alone.

**Assume a CoS section number written before 2026-07-27 may be off, and check it.** The same pass
found four more citations in `MAM-basics/py/accgram/` naming the right rule at the wrong section:
the small *revia'* servant is Ch. 11 §17 not §16 (§16 is the *dekhi*-in-its-own-word section), the
*revia' mugrash* servant §38 not §35, the big *shalshelet* servant §37 not §30, and the doctrine
that a *revia'* stands in for an *ethnakhta* with too little to its left to divide is Ch. 10 §14
not §17–18, along with its three verses. Two substantive findings there as well, both still
unapplied in accgram: Ch. 11's "always *galgal*" is the rule for the **last of several**
servants (§8), while a **lone** servant of a *pazer* is *merkha* (§7, whose own two examples are
Ps. 4:3 and Ps. 71:3); and Ch. 9 §11 is a two-column table of single servants, not a rule limiting
the servant of *siluk* or *ethnakhta* — its *Siluk* row has an entry under "another cantillation
mark", its *Ethnakhta* row does not.

**Two things Yeivin settles for the framing itself**, worth not re-deriving. §291: a maqaf "has no
musical motif of its own, and is therefore not considered an 'accent', either conjunctive or
disjunctive" — the narrow sense the one-scale reading already concedes. §292: the "atom left
blank" gloss, stated as a near-rule for the best manuscripts — a good gloss, still not a
definition.

Where this lives in code: `MAM-basics/py/accgram/edition_transcription.py`'s "HOW RARE THAT IS IN
PROSE, AND HOW ORDINARY IN POETRY" paragraph (fullest, with citations) and its "WHAT A DIFFERENCE
MEANS" paragraph; the `ctr_decalogue` docstring's own caveat.

Koren's `mun-mun` on לא־תעשה (`koren_dt_elyon`) strikes Ben as **highly anomalous**; whether
anything in Tanakh precedes it is an open question.

## Where the survey of this lives

`MAM-basics/py/accgram/maqaf_nonfinal_accents.py` (the scan; its docstring is the method of
record) and `maqaf_nonfinal_accents_page.py` beside it (the rendered argument, with
`pin_claims`); then, in MAM-basics too, `out/accgram/maqaf-nonfinal-accents.json` (every hit,
tracked and diffable) and `gh-pages/wlc/accgram/maqaf-nonfinal-accents.html`. **Extend it there and diff the JSON — never
restate its numbers in another docstring.** The research first landed as ~60 lines of docstring
with the scan in gitignored `.novc/`, and accreted corrections instead of being re-derived.

## Routing by system

accgram has two checkers, `prose_scanner` and `poetic_scanner`, and both `prose_filter.py` and
`poetic_filter.py` route **verse by verse** through `bib_locales.is_poetcant`. Never poetic-scan a
prose verse: telisha and zaqef come out as a meaningless NO_PARSE while shared marks look
spuriously clean.
