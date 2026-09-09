# Terminology — every rule with its reasoning and its exemptions

The quick table in `SKILL.md` is the checklist; this is why each row is there, what is exempt,
and which known holdouts are deliberate.

## Atom vs chanted word (wlc-utils#81)

- **Atom** — one written word, between spaces or maqafs; the thing a maqaf joins to the next.
- **Chanted word** — a lone atom *or* a whole maqaf compound. The unit cantillation operates on,
  normally with one accent. A maqaf compound is ONE chanted word, not two words joined.

Since #81 these are the terms the **rendered prose** must use too, not just the terms for
talking about the prose. `MAQAF_IS_THE_LAST_RUNG` introduces "atom" to the reader with an
appositive gloss, and that gloss is what licenses the bare term elsewhere on the pages.

Name a compound whole: **על־פני**, **לא־תעשה**. Never name a bare **פני** and then qualify or
apologize that it is "maqaf-joined as על־פני" or that "the accent is on its פני half" — Ben
rejected exactly that parenthetical. The hedge is the error, not just the wording.

Plain "word" survives where it means an ordinary English word ("in other words," "a great many
Hebrew words take one vowel where the reading pauses") and inside quoted or translated source
material — MAM's notes rendering תיבה, the WLC manual's bracket-note counts, the Breuer quotation
— which keeps whatever it says. Scan-box code comments may still say which half of a compound a
highlight rectangle covers: that is geometry, not a claim about which word is meant.

**And plain "word" survives wherever the context already settles which sense is meant.** What #81
bans is a loose "word" the reader has to resolve from nothing; the qualifier is owed where the
sense is genuinely in doubt and is noise where it is not. Ben, 2026-07-29, on a table heading
shortened from "Chanted word" to "Word": *"even a column having only compound words, or simple and
compound words, might still be labelled word since what definition of 'word' is active is clear
from the contents of the column! Also in many contexts it is unnecessary to qualify a word as
chanted because it is clear from context."*

- **A table heading is read with its column**, never alone, so the forms below it show the sense.
  This holds whether the column is all simple, all compounds, or mixed — do NOT reason that a
  column containing compounds must say "chanted word".
- The same goes for running prose whose subject has already been established a sentence or two
  above. Qualify at the point where a reader could take it the other way.
- Where the qualifier costs nothing, it can still go in the **hover text** while the visible label
  stays short: accgram's one-letter appendix heading is `Word` with `title="The chanted
  word; …"`.

## Naming an atom by position, not by role

Say **"a non-final atom of a compound."**

- Never **"proclitic"** — it asserts a grammatical role the scan never checks, where the atom's
  *position* is exactly what is measured.
- Never call a lone atom **"maqaf-joined"** full stop: it is joined *to* the next atom, or else
  the two of them are joined to each other. That was Ben's actual objection, so "Maqaf-Joined
  Atom" is not the repair.
- **"A joined atom" is ambiguous too**: in a two-atom compound both atoms are joined.
- Phrase the normal case as "a non-final atom of a compound normally **has** no accent," or
  flipped, "normally only the final atom of a compound has an accent."

The rendered title that came out of this is "Accents on a Non-Final Atom of a Compound" —
"maqaf" dropped there only for space, since there is no other kind of compound.

## Maqaf is the last rung of one scale

Every chanted atom's marking sits on ONE scale of separating force: disjunctives → conjunctives
→ **maqaf** at the bottom.

- Say "the weakest **separating** force," never a bare "weakest."
- **No second ledger.** The convention "word division is counted apart from accents" was rejected
  (2026-07-25): it fixed a real double-counting problem by declaring one of the two facts
  non-existent, and it contradicted `supplied_marks.py`'s own published prose (maqaf is coupled
  to the lack of an accent so tightly that detangling accents and punctuation "can be regarded as
  one and the same activity").
- **Counted once**, at the atom whose marking changed.
- **Stated as an exchange, both marks named.** Naming only the absent maqaf is the replaced
  convention surviving in the phrasing.
- **Do not define** a maqaf as "the atom left blank of an accent." **The implication runs one way**
  (Ben, 2026-07-26): *if an atom has no accent, it had better have a maqaf* — that direction is
  always true. The converse — *an atom with a maqaf also lacks an accent* — holds only in the vast
  majority of cases. So it is a good way to think about most maqaf use, and a fair gloss for the
  normal case (Yeivin §292 states it as a near-rule for the best manuscripts), but it is not a
  definition: `koren_dt_elyon`'s `mun-mun` on לא־תעשה keeps a munaḥ on the joined atom, as do the
  Simanim Tiqqun's two munaḥ-on-לא. Phrase it in the direction that is always true, or say
  explicitly that the other direction is the usual case rather than the rule.
- Cost accepted: "all four follow their strand in every accent" is gone; two Koren Decalogues now
  read "differ only at the maqaf."

Verdicts became a ladder — chanted verse boundaries → disjunctive skeleton → conjunctives →
maqafs — each cell naming the first rung that breaks. The reader-facing statement is the verbatim
`printed_decalogue_strands.MAQAF_IS_THE_LAST_RUNG`: **splice that constant, do not paraphrase
it.** Its guardrail comment records the replaced convention so it does not get reinstated.

## Chanted verse, not pasuq

The cantillation unit delimited by a sof pasuq is a **chanted verse**; the BHS unit is a
**numbered verse** (bcv). The distinction is central — the elyon chants Exod 20:8–11 as one
chanted verse where the taḥton makes each its own; Gen 35:22 is one numbered verse and two
chanted verses.

Keep the **mark** name "sof pasuq" and identifiers like `SOF_PASUQ` — only the unit is renamed.

**Refinement:** a sof pasuq does not by itself make a chanted verse. A chanted verse is a
well-formed cantillation unit, which minimally means **silluq** on the last word before the sof
pasuq. A span that, in Ben's test, "doesn't even seem to be trying to obey the rules of
cantillation" is a **sof pasuq span**. CTR's Exodus 20 = the elyon's nine chanted verses cut into
sixteen sof pasuq spans. Same care in identifiers: `sof_pasuq_spans()`, not `chanted_verses()`.

## Meteg vs silluq; meteg not ga'ya

Both are Unicode `\N{HEBREW POINT METEG}` (U+05BD) — **no separate codepoint** for silluq, which
is why code that names the constant broadly spells it `MTGOSLQ`.

- **Meteg** (= ga'ya) is a purely metrical mark, not an accent, not part of the cantillation
  system; it can sit on any word anywhere in a verse.
- **Silluq** is the same glyph *only* on the stressed syllable of the verse's own **last word**,
  paired with sof pasuq. There is no silluq on a non-verse-final word, however accented.
- **Check verse-finality before naming a bare U+05BD "silluq."** A word joined by maqaf to a
  following word is by definition not verse-final, so a U+05BD there is always an ordinary meteg.
  This is the commonest way the mistake happens, and it has reached rendered output before (a
  2026-07-02 CLC note claimed Deut 5:7's mid-verse יִהְיֶה־ "calls for a silluq").
- In **accgram** say **"meteg"**, never "ga'ya" and never "ga'ya meteg." (Other codebases do not
  standardize this way.) Do not reword quotations that cite ga'ya, or established phenomenon
  names like "qadma-as-ga'ya."

Implementations that already do the disambiguation, both in MAM-basics:
`py/accgram/meteg_silluq_context.py` (`u05bd_is_silluq()`), and `py/clc/clc_dual_cant.py`'s
`_accent_name`, which is CLC's and arrived in MAM-basics with the CLC code on 2026-08-03.

## Paseq vs legarmeh

Both are Unicode `\N{HEBREW PUNCTUATION PASEQ}` (U+05C0) — again **no separate codepoint**, which
is why the shared constant in `mb_cmn/hebrew_punctuation.py` is called `PASOLEG`.

- **Narrow-sense paseq** — an ordinary separating stroke, not an accent, not part of the musical
  system; a reader's cue to pause slightly. "Not part of the accent grammar, not tracked."
- **Legarmeh** — the same glyph after a conjunctive (usually *munaḥ* in the prose system; *azla
  legarmeh* / *mahapakh legarmeh* in the poetic) **transforms that accent into a disjunctive**,
  with its own melody and its own servants (typically *merkha*). Graphically identical to a
  genuine conjunctive munaḥ plus an independent paseq; the difference is grammatical, adjudicated
  by Masoretic tradition, not derivable from the bare text.
- **Broad-sense paseq** = the Unicode character itself. Write "broad-sense paseq" or "Unicode
  PASEQ" (capitals significant). Always disambiguate unless context makes it 100% obvious.

Canonical treatment: MAM-basics `py/author_misc/he_ws_intro_to_mam_pasleg.py` (+ its footnotes
module), a bilingual essay adapted from Avi Kadish's introduction to *Miqra al pi ha-Masora*
ch. 2 "פסק ולגרמיה", rendered at `MAM-with-doc/gh-pages/misc/he_ws_intro_to_mam_pasleg.html`. It
has the rules (legarmeh almost always precedes *revia*; the sole Biblical exception is Isa. 42:5)
and the manuscripts' own marginal `לג׳`/`פס׳` annotations. MAM-basics `uxlc/doc/clc-design.md` §7.16 is
the design-doc summary; note its §2 "under-bar" is a *separate* ambiguous-vertical-bar problem —
do not conflate the two. MAM-basics' `py/accgram` already models munaḥ legarmeh as its own
grammatical category.

## Stress helpers, and why U+0598 beside U+05AE is not a pair

**This is the single fact agents most reliably re-derive from scratch and get wrong.** Ben, 2026-07-29:
*"they are absolutely not two separate accents; this is just a result of unicode naming and
annotation confusion … they are an accent and its stress helper, just like the telishas."*

Six accents can need a **stress helper**: *segol*, *pashta*, *zarqa*/*tsinnor*, *telisha qetanna*,
*telisha gedolah*, *deḥi*. Each is prepositive or postpositive — it docks at an edge of its chanted
word, so it does not itself say where the stress falls. The helper is a second copy of the same
accent placed on the first letter of the stressed syllable. About 7,800 words in the Hebrew Bible
need one; roughly 3,800 of those need a *pashta* helper and nearly always have it, while how many
of the rest have theirs depends on the edition. The most authoritative Tiberian manuscripts use
helpers infrequently or not at all outside *pashta*; reader-friendly editions of the last two
centuries (Heidenheim 1818, Baer 1869) use them consistently.

**An accent and its helper share a codepoint — except for the zarqa.** A helped *pashta*, *telisha
gedolah* or *telisha qetanna* is one codepoint written twice, so nothing about it looks like a
pair. Ben's term for that is **self-help**. The zarqa is the sole exception, and only for an
encoding reason:

| codepoint | Unicode's name | what it actually is, in a **prose** verse | in a **poetic** verse |
| --- | --- | --- | --- |
| U+0598 | HEBREW ACCENT **ZARQA** | the zarqa's stress **helper** | *tsinnorit*, a real conjunctive |
| U+05AE | HEBREW ACCENT **ZINOR** | the **zarqa** itself | *tsinnor* |

The names are, in effect, swapped: the codepoint called ZARQA is not the zarqa, and the zarqa is
the codepoint called ZINOR. `mb_cmn/hebrew_accents.py` is named for exactly this — **`ZSH_OR_TSIT`**
(U+0598: "**z**arqa **s**tress **h**elper **or** **tsi**nnori**t**") and **`Z_OR_TSOR`** (U+05AE:
"zarqa or tsinnor"). Read those constants and their comment block before writing anything about
either mark.

So a **prose** chanted word carrying U+0598 then U+05AE has **one accent and its helper**. Never
call it two accents, never "two of the same accent", and never give it a row in a table of accent
pairs — the exclusion is not a judgement call but a consequence of the encoding. In a **poetic**
verse the same two codepoints are two genuinely distinct accents, so the prose/poetic split is
load-bearing here and a merged count is meaningless.

Why the encoding is like this: in most fonts *pashta*, *zarqa*/*tsinnor* and *deḥi* each have a
centered **lookalike** accent — *qadma*, *tsinnorit* and *tarḥa* respectively — whose codepoint
*could* be pressed into service as the helper. In practice this is done only for the zarqa, and
Unicode, as Ben puts it, "pretty much prescribes" it. He considers the practice a bad idea and has
proposed deprecating it.

**Primary sources — read these rather than reconstructing the argument.** `../document-index`
(repo `bdenckla/document-index`) indexes every proposal Ben has authored, in
`Unicode-and-ISO-Proposals.md`:

- **"Adding Hebrew stress helper accents," L2/25-242** — the full account, 27 pages, publicly at
  `https://www.unicode.org/L2/L2025/25242-hebrew-accents.pdf`. §9G, "Tsinnor as the helper for
  zarqa," is the passage that settles this entry; §9M has per-accent counts. Withdrawn after
  feedback that it was unlikely to be accepted, so it is a statement of the facts, not of a
  standard. The PDF needs a text extractor — `WebFetch` returns raw stream data. `pypdf` is in
  no venv that anything rebuilds (wlc-utils', the last that had it, was orphaned by the
  2026-08-01 evacuation and removed from disk soon after). Expect to install it.
- **"Re-documenting ZARQA and ZINOR"** — the proposal specifically about the misleading names.
  Google Doc only, no L2 number, linked from the same index.
- **"Forced helper forms of Hebrew accents"** — the follow-on. Word doc on OneDrive.

In accgram the scanners already fuse a helper into its accent, so a **token** count never sees a
pair where a **mark** count does: `prose_scanner`'s `ZARQA` rule fuses U+0598 with U+05AE, and
`PASHTA` and `TELISHAQETANNA` fuse the self-help cases. A survey that counts marks has to exclude
them by hand, which is what `maqaf_nonfinal_accents.simple_exclusion` does. Also relevant:
`MAM-with-doc/gh-pages/misc/tsinnorit_and_oleh_on_ivs.html` ("Tsinnorit & Oleh on Initial Vocal
Shewa").

## Never "word-division"

Maqaf is word-*forming* — it **joins** atoms into a chanted word. Sof pasuq is not word-level at
all — it **ends** a chanted verse. Only a space truly divides words. Umbrella noun =
**punctuation**, or **grouping** where a process noun is needed. Re-express, do not relabel.

## "Accent," not "cantillation accent" — and "cantillation" over "accentuation"

**These are two rules, not one, and they are compatible.** Confirmed by Ben, 2026-07-26.

- **Ban "cantillation accent"** — the phrase is, in his words, crazy. In accent-grammar contexts
  the subject is already cantillation, so the qualifier is redundant: "two cantillation accents
  crowding one letter" → "two accents…". Keep "cantillation" where it carries real contrast —
  "dual-cant," "single-cant," strand labels, "carrying a meteg, with no accent of its own." Watch
  for the phrase split across two source lines: a line-based grep for "cantillation accent"
  misses `…no cantillation\n" "accent…`.
- **Prefer the noun "cantillation" to "accentuation"** when naming the system or the subject
  matter. This is a separate choice about which noun to reach for, and it does not license
  gluing the two words together.

## Just say "has"

Full list in `SKILL.md`. Two extra notes:

- The rule is **not only about corpora** — the subject that "has" an accent is just as often an
  atom, a chanted word, or a compound. The false-agency argument is not what makes *bears* wrong
  there; plain-word aversion is.
- **"prints" / "is printed"** is banned as agency *and* as a tic Ben dislikes — he calls it
  flatly inappropriate for a digital edition. For a publisher or site, agency is real but use
  "shows." KEEP "printed" only where it means literal print: the `"tradition": "printed"` key,
  the `ws/…/printed` strand names, and hand transcriptions read off a printed page.
- Still open, not swept: the normative "WLC and UXLC **should code** the mark … as a pashta" in
  `prose_ob_notes_1k.py` — a different sense; confirm with Ben before touching it.
- **A rule "restricts X **to** Y", it does not "put X **in** Y."** Ben's rewrite, 2026-08-03, of
  "both Yeivin and Breuer put the metigah in the chanted word of the zaqef". "Put … in" describes
  where the mark goes and leaves the boundary to be inferred; "restrict … to" states the boundary,
  which is usually the whole reason the source is being cited. It also makes a trailing "and
  nowhere earlier" redundant — delete that rather than keep both.

## Name the mark; never "-shaped"

Two rulings from 2026-08-03, on one sentence about the Simanim Tanakh's p. 298.

- **Never "an עליון-shaped accent."** Ben: *"are you referring to the fact that pashta and qadma
  have the same shape? this is confusing. why not just say 'an עליון accent'?"* The hazard is
  sharpest exactly where such a sentence is most tempting: *pashta* and *qadma* really are
  near-identical marks, so "-shaped" reads as a claim about the glyph rather than about which
  strand the accent belongs to. Say "an עליון accent."
- **Name the mark rather than referring to it.** Ben, of "So the mark is very likely the edition's
  error": *"why be coy? name the mark (qadma) or even 'qadma on ויום'."* This is the rendered-prose
  face of the global "name the referent, don't leave me to reconstruct it" rule — a mark that has
  been named three sentences earlier still gets named again here.

**And check the scope word while you are in the sentence.** The same draft said the accent sat
"inside a תחתון phrase rather than an עליון phrase". Ben struck the trailing negation as saying
nothing the positive had not, and then: *"isn't it inside much more than a תחתון phrase? Isn't
inside an otherwise תחתון-conforming Decalogue?"* — which the transcription's own header bears out,
166 accents against 166 with one divergence. Take the scope from the measurement, not from the
nearest grammatical unit.

## Never "witness"

Two objections. In the printed-Decalogue work the subjects are contemporary **printed editions**,
so manuscript-studies vocabulary is misapplied; and even for real manuscripts Ben prefers to just
call them manuscripts. Say "edition," "printed edition," "manuscript," or the name — "the Koren
Tanakh," "the Aleppo Codex." For a page *about* such a source, name the source, not a "witness
page." Applies to identifiers too (`_chabad_witness` → `_chabad_aside`).

Swept: the printed-Decalogue trio. **Not** swept and worth offering if you touch them:
`almost-errors.html` ("three standard witnesses (Aleppo, Leningrad, Cairo)"), `poetic.html`,
`telg-doc-notes.html`.

## Never a bare "Simanim"

Feldheim publishes **two** editions in play, and they do not even agree — the **Simanim Tiqqun**
(tiqqun qorim; Decalogues pp. 83-84, 208-209, 246, 247; p-trad) and the **Simanim Tanakh**
(pp. 119-120, 297-298, 350, 351; m-trad). The repo's vocabulary predates the second, so an
unqualified "Simanim" reads as the Tiqqun by historical accident alone.

- **Code, comments, docstrings, tests, docs, `.txt` transcription headers:** `SimTiq` / `SimTan`
  (`simtiq` / `simtan` lowercase in identifiers and stems).
- **Rendered prose:** the full "Simanim Tiqqun" / "Simanim Tanakh," or a bare "the Tiqqun" once
  the passage has named it — the shorthand is repo jargon a published page's reader has not met.
- **The full name takes a determiner in running prose:** "the Simanim Tiqqun" or "Simanim's
  Tiqqun," never "Simanim Tiqqun has X at Y." "Simanim" is the publisher, doing a possessive's
  work. Contrast **"Koren"**, which by metonymy IS the edition's name and correctly takes no
  determiner. Prefer the **article** whenever a genitive follows ("the Simanim Tiqqun's own
  stance," not the double genitive), and the possessive when it parallels a neighbouring "Koren's
  Classic Tanakh." **Exempt**, as reference tags rather than sentences: citation labels and the
  captions/headings built on them, `img alt` text, filenames, design-doc table cells.
- **THE TEST IS WHETHER THE TWO COULD BE CONFUSED HERE, not the bare word itself** (Ben,
  2026-07-30): *"it is only critical to distinguish tiqqun from tanakh where there would be
  possibility of confusion, e.g. in a document discussing both."* So the qualification is owed in
  the printed-Decalogue pages, which put the Tiqqun and the Tanakh side by side, and is not owed
  in a document where only one of them is ever in play. **And even in a document that does
  discuss both, exceptions are allowed** (Ben, same day): *"where from context it is clear or, as
  in a title, where context *will* make it clear."* A title is read with the page under it, so it
  may leave the disambiguation to the body it introduces. Read the rest of this section as the
  house default rather than as a ban to enforce sight-unseen; the surrounding rules — the
  determiner, the code/prose register split — hold wherever the full name is used.
- **A page title may say bare "Simanim."** `maqaf-nonfinal-accents.html` is titled "Strange
  Spreaders in Koren and Simanim" (Ben, 2026-07-30). Raising it was right and he settled it twice
  over: *"I consider it an acceptable breaking of the rule on the basis of the need for brevity in
  a title,"* and then, more exactly, *"it is a strange spreader in a simanim edition"* — the
  title's "Simanim" is the **publisher**, the surviving sense two bullets down, so it is barely an
  exception at all. A `title` and its matching `h1` are where the full name's cost is paid in a
  browser tab and a search result. **Do not revert it**; the body prose under such a title still
  takes "the Simanim Tiqqun" in full, that page's own material being the Tiqqun's.
- **Three senses of bare "Simanim" deliberately survive** — do not "finish the job": the *page*
  ("the Simanim page," which documents both editions), the publisher or both books at once ("the
  two Simanim editions," "a Simanim edition"), and non-prose identifiers (`simanim-lemma` CSS class,
  `#simanim-conclusion` anchor, scan filenames, the `printed-decalogue-simanim` subcommand, the
  `printed_decalogue_simanim_page` module, `doc/simanim-tanakh-signs.md`). Any stem substitution
  must be anchored on the book/reading suffix or it corrupts that module name.
- One holdout left on purpose: the edition list in `ps17v14_mam_doc_notes_body.py` — Psalms rules
  out a tiqqun so it is almost certainly SimTan, but it may be quoted from MAM's own apparatus.
  Ask Ben.

## Never a bare "the Keter edition"

The same shape as the Simanim rule above, and found the same way — Ben, 2026-09-02, of a sentence
reading "MAM itself says the Keter edition marks one at every place the codex has one": *"When you
say 'the Keter edition', do you mean the 'Keter Yerushalayim' edition (as opposed to the
mgketer.org edition)? If so, please spell it out."* **Two editions carry the word, they are
different books, and MAM's own notes cite both.**

- **`מקראות גדולות הכתר`**, Mikra'ot Gedolot ha-Keter, abbreviated `מג"ה` in MAM's apparatus and
  served at mgketer.org. Write the Hebrew, or "Mikra'ot Gedolot ha-Keter".
- **`כתר ירושלים`**, the Jerusalem Crown — Breuer's edition, the one Yosef Ofer did the detailed
  work on. Write "the Jerusalem Crown" or the Hebrew.
- **And `כתר ארם צובה` is neither**: that is the Aleppo Codex itself, the manuscript both editions
  are named after, which MAM's notes also call `הכתר` and `כתי"א`.

**It is a live hazard rather than a point of taste.** A test for the codex in MAM's prose looks for
`בכתר`, and `נוסח המקרא בכתר ירושלים` inside a note at Judges 7:13 matches it — so a census reading
MAM's prose for the manuscript reports a printed edition unless it excludes that phrase.
`MAM-private/near-aleppo/census/qere_not_encoded.py` carries the exclusion as `NOT_THE_CODEX`, and
`PLAN-near-aleppo.md`'s step 40 row records what it cost before it was there.

## "Reading" is a technical term here, not a catch-all noun

Ben, 2026-07-28: *"You use 'reading', your favorite word for a lot of things, and one that is …
not my favorite."* In one intro it stood for a maqaf compound, for a whole printed Decalogue
page, and for an abstract "what Koren does here" — three referents behind one word, leaving the
reader to work out which. **Name the concrete thing**: Koren's *compound*, one printed *page*,
one printed *edition*, what the strand *has*. Same complaint as the nameless possessive "its
strand" and as the exterminated verb synonyms for *has*.

**The technical sense stays**, and is not a holdout to sweep: the elyon/taḥton `reading` JSON
field and dataclass attribute, `dual_cant_readings`' grouped chanted verse,
`printed_decalogue_strands.resolve_readings`, `render_reading_name`, a transcription's
`uncertain_readings` header and "a reading Ben has flagged as uncertain", and the ordinary verb.
`maqaf_nonfinal_accents_page` was swept 2026-07-28 — its "Koren's reading" heading is now
"Koren's compound."

## Strand vocabulary

- **strand** = one single-cantillation reading of a dual-cant passage (alef/תחתון/pashut,
  bet/עליון/midrashit). Precedent: MAM-basics' "singly-accented strands." Never "thread."
- **unpaired** = a stress-helper written without its fusion partner. Never "stranded."
- **marooned** = an accent or verse number displaced by BHS versification.
- **orphaned** is RESERVED for the ḥiriq of the implicit yod in ירושלם-style spellings.

The point is **search hygiene**: a grep for one sense must not turn up the other. Python
`threading` and the weaving-sense "thread … together" are unrelated and stay.

Vendored Wikisource strands are written **`ws/ex/taxton/printed`** — a display prefix, never a
change to the data keys, and **full triples only** (a bare `ex/taxton` pair stays as it is).
Render via `edition_transcription.strand_name(key)`, not open-coded joins. No `ws/` on the CTR
strand; `p-trad`/`m-trad` are tradition abbreviations, not strand names.

Elyon and taḥton are **arbitrary labels** — no positional meaning; do not gloss them "upper" and
"lower" (see `references/rendered-prose.md`).

**Never a bare "the strand": say which text it is (wlc-utils#77).** What an edition's Decalogue is
measured against is Hebrew Wikisource's version of a strand — an idealization, and our model of
one, not the tradition itself — so write "the Wikisource strand" / "its Wikisource strand",
keeping the strand as the grammatical subject: "the Wikisource strand has a maqaf", never
"Wikisource has a maqaf", which makes the website the author of a cantillation choice long
predating it. **The exemption is the quantifier, not the plural** (Ben's amendment, in
wlc-utils#77's 2026-08-03 comment, which is where it lives): "the four strands" and "all eight
strands" pass because they say which, while a bare "the strands", with nothing but an earlier
sentence to resolve it, is the same defect as a bare "the strand". The worked fix on
`printed-decalogue-simanim.html` put a quantifier where the bare plural had been, and
`printed_decalogue_simanim_page._vayom_forms` renders all four strands and requires the set to have
one member, so its "all four" is asserted rather than claimed.

**Never say never, though** (Ben, 2026-08-04): *"I'm sure there are exceptions where 'the strand'
or 'the strands' is clear from context. This rule is mainly about failing to be explicit that we
use the Wikisource strands as references, but some degree of implicitness (e.g. mention earlier in
a sentence!) is always acceptable."* The rule is about leaving the reference implicit where nothing
settles it, not about the words themselves, and context that already settles which text is meant —
a mention earlier in the same sentence included — is fine. **No sweep has been run against the
amended rule**, and recording it does not start one (Ben, same day): wlc-utils#77's open items 1
(docstrings and comments) and 2 (accgram pages outside the printed-Decalogue trio) still stand, so
existing prose may not conform.

## BIL / AIL, not "preposed"

**BIL** = "before-its-letter," the WLC/M-C digital-stream convention where the accent's code
precedes its base letter's; **AIL** = "after-its-letter," the Unicode order. "Preposed" conflates
three layers Ben keeps apart: (1) BIL stream order, (2) Masoretic *prepositive* — the accent docks
at the start of the atom, (3) the right-biased glyph placement. Keep "prepositive" strictly for
sense (2); say "preposed" only when quoting the M-C manual or naming `_PREPOS_*` identifiers.

## "The LC," not bare "L"

In free-text comments and docstrings spell out **"the LC"** for the manuscript, parallel to
"MAM"; keep **"WLC"** for the digital text and its scanner, and call that scanner "the scanner,"
never "the L scanner" (the LC is a manuscript, not software). Bare "L" is widespread legacy
across the poetic files — a pending sweep, not the standard.

## Transliteration (accgram)

- **ḥet (ח) is never `h`.** ASCII **`x`/`X`** almost everywhere hand-written — identifiers
  (`DEXI`, `MUNAX`, `TARXA`) and free-text comments/docstrings (`dexi`, `munax`, `tarxa`). Real
  Unicode **ḥ** is reserved for string-literal *values* that flow to rendered output or test
  expectations. Issue #13 (closed) established the never-`h` rule and **already deprecates**
  `munah`/`tarha` itself, in a blockquote marked "Refinement (supersedes an earlier draft)" — the
  h-forms appear there only as the thing being retired, not as a live target. Do not read that
  paragraph as a competing standard.
- **ḥ is the precomposed single codepoint U+1E25** (NFC), since #49 (2026-07-01). This is the one
  place #13's text is genuinely out of date: its body requires the **decomposed** `h` + U+0323
  form, and step 3 of its proposed approach was to normalize precomposed ḥ *to* decomposed. #49
  inverted that. `test_no_decomposed_composites_tree_wide` catches regressions.
- The h-forms that survive in the tree are all deliberate and individually tagged
  **`# translit-ok`** — meta-cites that name a spelling in order to reject it, external UXLC
  vocabulary keys, Unicode codepoint names, and finding-aid citations of a source's own spelling.
  `tests/test_transliterations.py` (#26) is the lint that enforces the denylist and honours those
  pragmas. Before "fixing" an `h`-form, check for the pragma and the reason on the line.
- **Keep the kaf**: `merkha` (not `merka`), `mahapakh` (not `mahpak`).
- **`tsinnor`** — never `sinnor` (the grammar's internal nonterminal spelling, which leaks) and
  never `tzinnor` (Breuer's English-translation spelling). `tsinnorit` stays distinct.
- **No transliterated plurals**: "two tsinnor **marks**," never "tsinnorin."
- **`oleh-weyored`**, run together. The ~57 `oleh-we-yored` in the tree are legacy, not the rule.
- **Breuer quotes**: render the accent name in the repo-standard spelling wrapped in **square
  brackets** to flag the divergence — `"[deḥi]"` for his "dekhi"; inside a `#`/docstring context
  use the ASCII form in brackets, `"[dexi]"`.
- Names are single-sourced as `ROM_*` constants in `printed_decalogue_strands.py`; do not retype
  the spellings inline. `tests/test_transliterations.py` (#26) guards them tree-wide.
- Unrelated X: the scanner's base-letter placeholder `accent_marks.LETTER` is **alef (א)**, not
  `"X"`. Do not reintroduce `X` or a display-conversion step.
