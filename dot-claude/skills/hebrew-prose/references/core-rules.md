# Core Hebrew-accentuation prose rules

This is the detailed statement behind the compact checklist in `../SKILL.md`.

## The rules that get broken most

**Never a loose "word."** An **atom** is one written word, between spaces or maqafs — the thing
a maqaf joins to the next. A **chanted word** is a lone atom *or* a whole maqaf compound: the
unit cantillation operates on, normally with one accent. Say which you mean. Name a compound
whole — על־פני, לא־תעשה — never a bare half of one with an apology ("פני, maqaf-joined as
על־פני" was rejected outright; the hedge is the error, not the wording). Plain ‘word’ survives
for an ordinary English word, inside quoted or translated source material, and wherever the
context already settles which sense is meant (references/terminology.md).

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
with a munaḥ of its own."

Three exemptions:

1. A source's rule quoted in the source's terms, such as Breuer's “cancelling”.
2. Stress retraction (nesiga).
3. Anything explicitly declared a thought experiment.

Ben's undated rule, already present when MAM-basics became the canonical configuration home on
2026-09-09.

**Just say "has."** A corpus, manuscript, edition, atom, chanted word or compound *has* a mark.
Exterminated so far, each its own cleanup: writes, wrote, codes, carries, reads, prints/is
printed, **bears**. Treat any new synonym the same (shows, displays, features, presents). Ben:
"avoiding your persistent and unappreciated creativity with verbs, simply *has* not *bears*."
Repeating "has" across neighbouring sentences is fine and preferred. Legitimate alternatives are
the ones carrying real information — "lacks" for absence, a positional verb where possession is
the wrong relation. "Bear out" (of evidence) is not possession and is fine. Passive is fine; so
is naming the real agent, the *naqdan*.

Ben's undated rule, already present when MAM-basics became the canonical configuration home on
2026-09-09.

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

Ben's undated rule, already present when MAM-basics became the canonical configuration home on
2026-09-09.

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
| Mikra'ot Gedolot ha-Keter (`מג"ה`); the Jerusalem Crown (`כתר ירושלים`); the Aleppo Codex (`כתר ארם צובה`) | a bare "the Keter edition", which can name Mikra'ot Gedolot ha-Keter or the Jerusalem Crown |
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
