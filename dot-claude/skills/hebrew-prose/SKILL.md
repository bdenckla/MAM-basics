---
name: hebrew-prose
description: Ben's house rules for writing or editing ANY prose about Hebrew accentuation or cantillation — rendered gh-pages text, module docstrings, code comments, commit messages, issue bodies — in MAM-basics (where all the accgram code, data and rendered pages live), MAM-simple, UXLC-utils, al-hatorah, book-of-job, mgketer and codex-index-aleppo. Covers the required vocabulary (atom vs chanted word, maqaf as the last rung of one scale, paseq vs legarmeh, silluq vs meteg, prose/poetic verses never books, never "witness", never a bare "Simanim"), the bans on transformative framing and on agentive verbs, which corpus a grammatical claim takes (MAM, not WLC), where the Yeivin and Breuer primary sources are, and how to verify a page's stated numbers.
when_to_use: Load BEFORE editing any file whose output or text discusses accents, cantillation, maqaf, meteg, paseq, strands, Decalogue readings, or the prose/poetic systems — accgram page modules and their docstrings above all. Also load when reviewing such prose, or when answering Ben about accentuation terminology. Not needed for purely mechanical work (renames, formatting, dependency edits) that touches no such text.
---

Everything below was settled with Ben and then scattered across four homes that no agent
reliably loads. This file is now canonical; the old homes are pointers. If a rule here and a
repo's own file disagree, the repo file wins **only** for its own subject matter — see
`printed_decalogue_strands.py`'s SCOPE paragraph, which marks its bullets TRIO-ONLY vs
REPO-WIDE — and tell Ben about the conflict.

## The rules that get broken most

**Never a loose "word."** An **atom** is one written word, between spaces or maqafs — the thing
a maqaf joins to the next. A **chanted word** is a lone atom *or* a whole maqaf compound: the
unit cantillation operates on, normally with one accent. Say which you mean. Name a compound
whole — על־פני, לא־תעשה — never a bare half of one with an apology ("פני, maqaf-joined as
על־פני" was rejected outright; the hedge is the error, not the wording). Plain ‘word’ survives for an ordinary English word, inside quoted or translated source material, and wherever the context already settles which sense is meant (references/terminology.md).

**"Chanted word" is MECHANICAL, and an analysis never takes the name away.** What makes a chanted
word is the writing: atoms joined by maqafs, bounded by spaces. So **never write that a maqaf
compound "is not really a chanted word"** because some section explains its maqaf as unusual — say
it is a chanted word **in presentation only**, or **superficially a chanted word**, and then say
what the analysis adds. Ben, 2026-08-03, on a draft calling ITM §357's maqaf-after-gaʿya compounds
"not chanted words with two accents": *"reserve our terminology of 'chanted word' to be a very
concrete, easily-defined notion related to maqaf joining and not be blurred with 'yes, there's a
maqaf there, but not really, based on our analysis'."* **What that maqaf signifies is genuinely
disputed** — Yeivin writes the same compounds with a *space* at §354, Breuer CoS Ch. 1 §43 says
"different views have been expressed" and leaves it out, Ch. 9 §37 points the other way, and neither
book squares them — which is the whole reason the name must not rest on it. Do not fix such a draft
by arguing the other side either: a first correction here replaced "not a chanted word" with "the
maqaf JOINS, as §357 says outright", and that settled the name on an interpretation just as much.
Rest it on the writing and let the dispute be reported as a dispute. **The rule runs the other way
too**: two atoms separated by a
**space** are two chanted words, however plainly they "should" have been joined — this is the
poetic case, where a pair wanting a maqaf has a space instead. In MAM, where such a pair has a
**gray maqaf**, calling it one chanted word is fine; in an edition or manuscript that simply has a
space, it is not.

**Maqaf is the last rung of ONE scale.** Disjunctives → conjunctives → maqaf. A maqaf separates
the atom it sits on from the next even less than a conjunctive does. Never a bare "weakest" — a
maqaf *binds* tightest, so unqualified it reads as backwards to anyone who knows Wickes or
Yeivin; write "the weakest **separating** force." There is **no second ledger** for "word
division." A maqaf difference is counted **once**, at the atom whose marking changed, never as a
regrouping plus an accent, and is stated as an **exchange with both marks named** ("a maqaf where
its Wikisource strand has a merkha"), never as the absent maqaf alone. Do not *define* a maqaf as
"the atom left blank of an accent": **that implication runs one way only.** An atom with no accent
had better have a maqaf — always true. An atom with a maqaf also lacking an accent — true of the
vast majority, not all, so it is a good way to think about most maqaf use and not a definition.

**Prose verses and poetic verses, never prose or poetic BOOKS.** Job's prose frame (1:1–3:1,
42:7–17) is poetically booked and prose cantillated, so "book" makes the phrase false, not merely
loose. The systems themselves are "the prose system" / "the poetic system." Quoted sources keep
"the Three Books"; "the 21 books" as a corpus *name* is fine.

**An accent and its stress helper are not two accents — least of all the zarqa's.** Six accents
can need a **stress helper**, a second copy that marks the stress the accent itself does not:
segol, pashta, zarqa/tsinnor, telisha qetanah, telisha gedolah, deḥi. For five of the six the
helper shares its accent's codepoint, so it never looks like a pair. **The zarqa is the sole
exception**, and only because Unicode's two names are misleading: U+0598 "HEBREW ACCENT ZARQA" is
the helper, and U+05AE "HEBREW ACCENT ZINOR" is the zarqa. So a **prose** chanted word with U+0598
before U+05AE has **one accent and its helper**, exactly like a doubled pashta — not two accents,
not two of the same accent, and never a row in a table of accent pairs. In a **poetic** verse the
same two codepoints are the genuine and distinct *tsinnorit* and *tsinnor*. This gets re-derived
from scratch about once a session; the full account, with Ben's own Unicode proposals behind it,
is in `references/terminology.md` §"Stress helpers."

**No transformative framing.** Never "the joined atom gives up its accent," "MAM cancels the
maqaf," "Breuer restores the secondary mark." Such framing never declares whether it is a
teaching aid, a historical claim, or a picture of someone scratching ink off a manuscript. State
what each text **has**: "MAM has no maqaf there: ויאמר and אלהים stand as two chanted words, each
with a munaḥ of its own." Three exemptions — a source's own rule quoted in its own terms
(Breuer's "cancelling"), **stress retraction** (nesiga), and anything explicitly declared a
thought experiment.

**Just say "has."** A corpus, manuscript, edition, atom, chanted word or compound *has* a mark.
Exterminated so far, each its own cleanup: writes, wrote, codes, carries, reads, prints/is
printed, **bears**. Treat any new synonym the same (shows, displays, features, presents). Ben:
"avoiding your persistent and unappreciated creativity with verbs, simply *has* not *bears*."
Repeating "has" across neighbouring sentences is fine and preferred. Legitimate alternatives are
the ones carrying real information — "lacks" for absence, a positional verb where possession is
the wrong relation. "Bear out" (of evidence) is not possession and is fine. Passive is fine; so
is naming the real agent, the *naqdan*.

**Never "witness."** Say edition, printed edition, manuscript, or the thing's name. Ben dislikes
the term even for actual manuscripts.

**Cut "own."** Ben, of a rendered label in 2026-07-29: *"it features your favorite, usually
meaningless word: own"*; again on 2026-07-31, of "— his own term" on a page: *"there's that 'own'
that you like so much and I dislike."* It is a tic, not an intensifier, and it survives because
each instance looks harmless. Delete it and read the sentence back: "Breuer's word" says what
"Breuer's own term" said, "the translator's transliteration" what "the translator's own
transliteration" said, "Ch. 7 §1's definition" what "Ch. 7 §1's own definition" said. Keep it only
where it carries a **contrast the sentence actually makes** — "MAM is not one of Breuer's own
editions" (against the ones he merely influenced), "a compound whose joined atom keeps its own
munaḥ" (against the accent of the compound as a whole). Grep a draft for it the way you would for
a banned verb; this rule covers rendered prose, comments, docstrings, commits and issue bodies
alike.

**MAM is a consensus text, and is not a Breuer edition.** See "Which corpus a claim takes" below
— this one has been got wrong five times in one module.

## Which corpus a claim takes

- **Diplomatic** (one manuscript as it stands) = WLC, UXLC. **Consensus** = MAM. Ben prefers
  "consensus" to the standard "eclectic." Never write "an edited text, not a manuscript reading":
  *all* texts are edited, so that says nothing.
- **MAM is NOT a Breuer edition.** Breuer's editions proper are the **Horev** one and the
  **Jerusalem Crown** (which he advised on without detailed involvement; **Yosef Ofer** did the
  detailed work, framing it as using Breuer's methods, as its front matter says). MAM follows
  Breuer heavily — attributing a *rule* to Breuer to explain something MAM does is fine as long
  as the inference is visible to the reader.
- **A claim about what the accentuation DOES takes MAM as its corpus**, not WLC: WLC is a flawed
  transcription of a flawed manuscript and its blemishes land straight in such counts. WLC keeps
  only claims that are *about a manuscript*, attributed by name.
- **WLC, BHS 1997 and BHQ are usually ONE transcription, not three that agree** (Ben,
  2026-08-07). Their agreeing corroborates nothing about the manuscript — it is one reading
  counted three times. Never "all three have it, so the LC has it"; only someone reading the
  manuscript settles that. Worked case, and why gn 18:18 is `tbd` rather than `lc`:
  `references/sources-and-corpora.md`.
- Only the **LC** has the ambiguous vertical **bar**; WLC/UXLC/MAM have definite codepoints. Say
  "the LC's bar, which WLC transcribes as merkha," never "WLC's bar."

## Vocabulary quick table

| Say | Not |
| --- | --- |
| atom / chanted word | a loose "word" |
| a non-final atom of a compound | "proclitic"; a lone atom "maqaf-joined" |
| chanted verse (sof pasuq span when unchantable) | pasuq |
| meteg (silluq only verse-finally) | ga'ya, "ga'ya meteg" |
| legarmeh; broad-sense paseq / Unicode PASEQ | an unqualified "paseq" for the glyph |
| punctuation / grouping | "word-division" |
| accent | "cantillation accent" |
| strand; unpaired; marooned; orphaned | thread; stranded |
| the Wikisource strand; "all four strands" | a bare "the strand" / "the strands" where nothing settles which |
| the LC (manuscript), WLC (digital text) | bare "L" |
| SimTiq / SimTan in code; "the Simanim Tiqqun" in prose | a bare "Simanim" where both editions are in play |
| Mikra'ot Gedolot ha-Keter (`מג"ה`); the Jerusalem Crown (`כתר ירושלים`); the Aleppo Codex (`כתר ארם צובה`) | a bare "the Keter edition", which names either of the first two |
| BIL / AIL | "preposed" (outside M-C quotes) |
| the compound / the page / the edition | "reading" as a vague catch-all noun |

Each row's reasoning, exemptions and known holdouts: `references/terminology.md`.

**Show it in Unicode, not only in words — letters and accents, NO vowels.** If the claim is
about what marks a text has, print the Hebrew and let the sentences run into and out of it. Ben,
2026-07-28: *"why would you only describe in words what can be shown in Unicode? … why ever words
alone? I'm stumped by this favored style of yours."* "sets לא־תעשה as a maqaf compound and accents
both atoms with a munaḥ" makes a reader assemble in their head a form they could have looked at,
and the contrast a page turns on is often one mark wide — **ל֣א־תעש֣ה** against **ל֣א תעש֣ה**.

Show it through `almost_errors_html_shared.accents_and_letters`, which exists for exactly this
and drops vowels, dagesh and the sin/shin dots. Ben, same day, on a first pass that kept them:
*"I said please point with appropriate accents, why did you add vowels. we almost never use
vowels in such discussions."* The exception is a table where the vowel **is** the point (the
`printed-decalogue-vowel-diff` and pausal tables), which says so in its own comment.

**Never retype an accent**: lift the form from the vendored data at generation time, with an
assertion that the lookup still finds exactly one match. A hand-typed accent is a claim with no
oracle behind it. The pattern is `maqaf_nonfinal_accents_page`'s `_find_span()` / `_render_span()`
pair (2026-07-29, replacing the `lo_taase_atoms()` / `simtiq_lo_compounds()` this line used to
cite): search by a tuple of atom letters **per chanted word**, so the pattern fixes the grouping
as well as the letters and cannot match a strand that groups those atoms differently; raise unless
exactly one place matches; render each atom through `accents_and_letters` and put the maqafs back.
Two lessons are built into it. **Collect matches in a list, never a set** — a strand's two
byte-identical לא־תעשה compounds deduped to one and the `len == 1` assertion passed having
distinguished nothing (item 14 of `MAM-basics/doc/review-findings-2026-07-29.md`); what tells such
sites apart is the word that follows, so carry it in the pattern and display only what you mean to
show. And **a span runs to whatever length keeps every chanted word in it whole in every column
being compared** — where one strand joins the next word to your second atom, the comparison shows
that word too, half of a compound being a thing these pages never print.

**Comparing two or three texts at one place? A table, not paragraphs.** Ben, 2026-07-29, of an
intro that had built the comparison out of running prose and single-form specimens: *"I can't
process all the verbosity, I need to just see this using actual unicode. You've fallen into the
trap of not giving me Unicode. Or only very spotty use of it."* One row per case, one column per
text, every cell a form — and then prose for the interpretation only, which is what prose is for.
The same ask fixed a framing fault at the same time: two editions had become one in running prose
with the other appended as a shorter paragraph ("X's is not the only such compound in print"), and
same-columns-same-derivations is what put them on a par. Watch for the afterthought shape whenever
one instance was found before the others.

## Rendered prose has extra rules

Rendered gh-pages text is written for Hebrew-Bible readers, not for people who know what the
checker does. Strand names in Hebrew letters (תחתון / עליון), single-sourced `ROM_*`
romanizations in italic, real em dashes, no English sentence opening on a Hebrew word, no
implementation jargon, no previews of a later section or satellite page, no hedging over bounded
doubts. Full list with the exemptions: `references/rendered-prose.md`.

**A table cell holding Hebrew is declared `dir="rtl"`** — every such cell, unless the whole table
already is, and without waiting to be asked. Right-justification then follows from having said what
the cell holds, which is why the declaration beats a literal `text-align`. Ben, 2026-07-29: this is
*"something I find myself telling you about frequently … this should just be sort of obvious."*
Blank cells in the column included, the English heading left alone, no class and no stylesheet
rule. That plus the companion rule about abbreviating a long accent name in a cell:
`references/rendered-prose.md` §"A table cell holding Hebrew is declared `dir="rtl"`".

**Never open a line with Hebrew — this one covers chat replies to Ben, not only a rendered page.**
The first strong character sets a paragraph's base direction, so a bullet, list item, paragraph or
mixed table cell **beginning** on a Hebrew word is laid out entirely RTL, English and punctuation
and list marker with it. Two fixes, Ben's, 2026-08-25: give the Hebrew a **cell of its own** in a
table, where its direction affects nothing else, or give the line an English **runway** —
`As for "בכתר": …`. The runway **carries** the Hebrew and does not replace it; substituting the
English gloss ("As for the Keter") breaks the show-it-in-Unicode rule above, and was the second
correction of the same message. **BiDi control characters are not the fix, so do not offer Ben a
test of them**: `<bdi>` does not render in the Claude or Codex desktop apps' markdown, and wrapping each
Hebrew run in U+2068 FIRST STRONG ISOLATE … U+2069 POP DIRECTIONAL ISOLATE — the exact `<bdi>`
equivalent — leaves the paragraph direction untouched, because what flips the line is its first
word. Hebrew in the **middle** of an English line needs nothing at all. Fuller statement:
`references/rendered-prose.md` §"Typography and sentence shape".

**A RUNWAY HAS TO BE A STRONG LATIN CHARACTER, AND A SECTION SIGN, A DIGIT AND A BACKTICK ARE NONE
OF THEM.** Ben, 2026-09-02, of a numbered proposal whose items opened on a section sign and then a
Hebrew section name: *"I basically can't read that numbered list (1-3) above because of BiDi
issues. Perhaps if you use a Latin-char-containing lead-in like 'Item 1', 'Item 2', etc. it will be
readable."* Section signs, list markers, bold asterisks, backticks, quotation marks and digits are
all **neutral**, so a line opening on any of them and reaching Hebrew before it reaches a Latin
letter is laid out entirely RTL — exactly as if the Hebrew had come first. That is why one item of
that list survived and two did not: the survivor read "rule 4" after its section sign, and the
other two went straight into Hebrew. **The fix is a real word before the Hebrew** — "Item 3 — the
zaqef-metigah section…", "Chapter 2's section on the zaqef metigah says…" — and in a numbered list
open **every** item the same way, one flipped item being enough to make the whole list hard to
read. **So check the first STRONG character of every line, not the first character.**

## Primary sources — grep these before saying a source is silent

**Both books share one tree, `../MAM-private/masorah-books`** (private, for copyright in the source
material and not for secrecy). They have shared it since 2026-07-31: it was `yeivin-itm` until the
rename, and `breuer-cos` was merged into it with its history. On 2026-08-10 that tree moved out of
its own clone into `MAM-private`, so the path above replaces `../masorah-books`; the repo
`bdenckla/masorah-books` keeps a breadcrumb `README.md` and its 19 issues, and a `masorah-books#NN`
citation still resolves there. **Read the tree's `CLAUDE.md` and `README.md` first**, and
`doc/migration-checklist.md` for what the merge left unfinished.
`bdenckla/breuer-cos` still exists but has been **archived since 2026-08-27, so it is read-only**
(`gh api repos/bdenckla/breuer-cos --jq .archived` returns true; measured 2026-08-31). It was
deliberately unarchived until then, so its issues would keep their numbers and its two open ones
stay editable — and archiving cost neither, because on 2026-08-26 those two open issues, #2 and
#3, were **transferred to MAM-private**, where they are **#13 and #14** and both still open. What
`bdenckla/breuer-cos` holds now is #1, #4 and #5, all closed — #5 having been folded into
`masorah-books` #7 and #1 into `masorah-books` #15 and #16. **There is nothing to grep there**: its
clone was deleted on 2026-08-07, so `../breuer-cos` names nothing on disk, and on 2026-08-10 the
GitHub repo was
emptied to a breadcrumb `README.md` because its copies had gone stale against the live tree. The
pre-empty tree stays in history at commit `54440aa`.

- **Yeivin, *Introduction to the Tiberian Masorah*.** The **full OCR** is
  `../MAM-private/masorah-books/books/itm/md-export-of-docx/*.md`, one file per section-run.
  `../MAM-private/al-hatorah/py/itm/` is
  Ben's **partial adaptation** — searching only that once produced a flatly wrong "Yeivin says
  nothing about this" when §§291–293 and §357 cover it squarely. That tree moved out of its own
  clone into `MAM-private` on 2026-08-10 and the clone came off the disk on 2026-08-11, so
  `../al-hatorah` names nothing now; `bdenckla/al-hatorah` keeps a breadcrumb `README.md` and its
  124 issues. ITM romanizes several accent
  names differently from accgram: grep ITS spellings.
- **Breuer, *The Cantillation of Scripture* (English).** The six chapter docx (Chs. 1–5, 6–8, 9,
  10, 11, 12–15) are at `../MAM-private/masorah-books/books/cos/src/`, and remain under
  `~/OneDrive/Documents/Tanakh/` as well. The
  markdown export is **done for all fifteen chapters** (2026-07-27) — 522 sections in 57 files at
  `../MAM-private/masorah-books/books/cos/md-export-of-docx/C<NN>-S<NNN>.md`, so **grep there,
  never the docx**. Its two checks are subcommands of
  `../MAM-private/masorah-books/py/main_ocr.py`, which since
  2026-08-01 is the only runnable file there — `cos-check-claims` and
  `cos-check-cross-references`, never the module paths. Run it with the cwd at that tree's own
  root, `C:/Users/BenDe/GitRepos/MAM-private/masorah-books`, and on that tree's own `.venv`;
  MAM-private's root holds a venv carrying black and nothing else. Page anchors
  and a diacritics repair pass are still outstanding, one issue each in `masorah-books` — #15 for
  the page anchors, #16 for the diacritics. `breuer-cos` #1, which staged both, was closed on
  2026-08-02, the conversion its title names being done. The book is also
  **fully scanned**, 719
  page images at `~/OneDrive/Documents/ScansOfBooks/The Cantillation of Scripture - English/`.
  Breuer's English translation mostly says **"hyphen"** and never "maqqef"/"maqaf" — but the
  translator's transliteration **"makaf"** occurs across the export, and מקף in the front
  matter: grep all three, or the topic looks absent when it is not.
  **The same trap catches the meteg, and it catches Yeivin as well.** The two books spell it
  disjointly, so one grep finds neither: CoS says **`ga'aya`**, concentrated in Ch. 8, which is
  the ga'aya chapter, and ITM says **`gaʿya`**, with U+02BF rather than an apostrophe. Grepping
  either export for `meteg` returns ZERO, as does `ga'ya` in ITM and `gaʿya` in CoS. Breuer's
  siluk is `siluk` and Yeivin's is `silluq`, and neither book uses the other's spelling.
  **`methiga` is not a spelling of meteg** in either book: it is the servant in the word of a
  small zaqef, CoS Ch. 5 §§4-6. Established 2026-09-09; the worked case is
  `MAM-basics/doc/foi-mtgmtg-empty-cell.md`, whose first grep of CoS missed Chapter 8 entirely.
- Details, section numbers and the prose-vs-poetic asymmetry they establish:
  `references/sources-and-corpora.md`.

## How to verify what you wrote

Numbers in prose with no regeneration path are exactly what
`MAM-basics/doc/agent-planning-principles.md` §"Generated Outputs Are the Tests" forbids.

- **Regenerate the tracked artifact with the real CLI command and read the diff.** That is the
  test. One run writes both the JSON and the HTML, so page and data cannot drift.
- **Never quote a number you have not read out of the regenerated file.** On 2026-07-26 a figure
  restated from memory reached Ben wrong. Read it back out; do not retype it from a plan, a
  docstring, or an earlier turn.
- **Do not restate a survey's numbers in another module's docstring** — keep a pointer.
- A page's stated-in-words claims are kept honest by a **`pin_claims`-style assertion** that
  re-derives them from the data and **raises** on drift (`maqaf_nonfinal_accents_page.pin_claims`,
  `printed_decalogue_strands.resolve_readings`). Never soften one to a warning: a warning in a
  generator's output is a warning nobody reads.
- Do not add tests beyond the two shapes that have ever paid here — differential against an
  independent oracle, or mechanical lint over the tree. Everything else: regenerate and diff.
- Commands and the black/Unicode mechanics: `references/verifying.md`.

## Reference files

- `references/terminology.md` — every vocabulary rule with its reasoning, exemptions, and the
  spots deliberately left alone.
- `references/rendered-prose.md` — the gh-pages-only conventions.
- `references/sources-and-corpora.md` — Yeivin, Breuer, CTR, the corpora, and the prose-vs-poetic
  asymmetry about two accents on one chanted word.
- `references/verifying.md` — regeneration commands, `pin_claims`, tests, black, Unicode hazards.

## If this skill stops firing

If description-triggering proves unreliable in practice, the belt-and-braces option is a
`PreToolUse` hook on `Edit|Write` matching the accgram page modules, emitting these rules as
feedback. Ben's `update-config` skill covers the settings.json and hook mechanics. Proposed, not
implemented — ask before adding it.

## Where these rules used to live

`~/.claude/CLAUDE.md` (the paseq/legarmeh, silluq/meteg and maqaf-scale entries),
`MAM-basics/CLAUDE.md` (the rendered-prose pointer section),
`MAM-basics/py/accgram/printed_decalogue_strands.py`'s module docstring (the fullest statement of
the rendered-prose conventions, and still the home of the trio-specific ones), and the wlc-utils
auto-memory directory. Those stay as pointers; when a rule changes, change it **here** first.

**All of the Python moved on 2026-08-01**, out of wlc-utils and into MAM-basics, which is why
every `py/accgram/...` path in this skill reads `MAM-basics/`. **The rest of wlc-utils
followed** (copied 2026-08-12, wlc-utils emptied 2026-08-17;
`MAM-basics/doc/PLAN-evacuate-the-rest-of-wlc-utils.md`): its `in/`, `out/` and `doc/` trees are
MAM-basics' own now, its `gh-pages/` is `MAM-basics/gh-pages/wlc/` (old
`bdenckla.github.io/wlc-utils/...` URLs still resolve — each serves a stub forwarding to the new
site), and wlc-utils itself is a redirect host holding nothing but generated stubs, where no
prose is written any more. `wlc-utils#NN` issue citations still name that tracker, whose issues
were not transferred — 93 of them, measured 2026-08-17.
