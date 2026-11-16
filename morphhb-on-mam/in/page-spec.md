# Specification of the page `morphhb-on-mam.html` (2026-11-15)

Written by Claude (Opus 5.5) on 2026-11-15 for the builder of the feasibility study's page.
The study's folder is `morphhb-on-mam/` (below, "the folder"); its `README.md` maps the
scripts and outputs. Build the page with a script, `py/morphhb_on_mam/build_page.py`, that
reads every figure and every Hebrew form from the outputs named below; never type a figure
or a Hebrew letter into the script by hand. The builder writes only
`out/morphhb-on-mam.html` and its own script, and changes nothing else.

**Paths updated on 2026-11-16**, when the study was put on ice and its record tracked as
`morphhb-on-mam/`. The study ran in `.novc/morphhb-on-mam-2026-11-15/`, where this file,
the page and the fragment stood at the top of the folder, the scripts in `scripts/`, and
the alignment's records in `out/` with the other outputs.

## Rules for the page (all binding)

1. Load the `hebrew-prose` skill and read its `references/rendered-prose.md` and
   `references/mam-basics.md` before writing. Use "atom" (one written form between spaces or
   maqaf marks) and "chanted word" (an atom or a whole maqaf compound) exactly; morphhb's unit
   is the `<w>` element, which corresponds to an atom; call it "morphhb's word" on first use and
   define it.
2. Head of the page: `<!doctype html>`, `lang="en"`, charset, viewport, a `<title>`, and these
   stylesheets by relative path, as the sibling page
   `.novc/hebrew-morphology-2026-11-15/hebrew-morphology.html` does:
   `../../gh-pages/document.css`, `../../gh-pages/MAM-with-doc/misc/style.css` (it loads Taamey
   D for `lang="hbo"` and styles `p.ai-caveat`), `../../gh-pages/near-aleppo/link-presentation.css`.
   Copy that page's small `<style>` block for tables (`table.breakout`, `td.form`, `td.bcv`)
   and add only what you need.
3. Directly under the `<h1>`, a `<p class="ai-caveat">` saying that the page has not been
   reviewed by a human; that Claude (Opus 5.5) wrote it on 2026-11-15 at Ben Denckla's request;
   that every reading is attributed to the transcription that has it, morphhb (whose text is
   WLC 4.20's) or MAM (as MAM-simple gives it, in the BHS versification); and that nothing on the
   page says what the Leningrad Codex itself has.
4. Every pointed form is in `<span lang="hbo" dir="rtl">` (Taamey D at 140% comes from the
   stylesheet), large enough to read its points: use a `big` class at 200% or more in tables.
   Unpointed Hebrew keeps the surrounding font in a `<bdi>` with no `lang`, except an unpointed
   ketiv shown beside pointed forms it is compared with, which keeps their font
   (rendered-prose.md, "Unpointed Hebrew keeps the surrounding font"). Never underline pointed
   Hebrew; a link on it takes `text-decoration: none`.
5. Tables of forms follow rendered-prose.md: every Hebrew cell `dir="rtl"`; columns, from left
   to right, `[more pointed Hebrew] | pointed Hebrew | BCV | [Latin columns]`; when two forms
   are compared, put them in one cell, one above the other, with a Latin label for each line in
   a cell beside it (for example "MAM" above "morphhb"); natural widths, the `breakout` class.
6. Never open an English sentence or a list item with a Hebrew word. Real em dashes. No
   jargon a Hebrew-Bible reader would not know without a gloss: explain "lemma", "morph code",
   "id", "alignment" once, briefly. Say "Claude's first reading" for any judgment of a case.
7. Attribute every form: "morphhb has", "MAM has". Cite morphhb's issues and pull requests as
   openscriptures/morphhb#NN with a link to its GitHub URL, never a bare #NN. Book names in
   English, chapter:verse, for example "Judges 19:4"; the outputs' OSIS ids (`Judg.19.4`) need
   a lookup table from OSIS book ids to English names, which `py/morphhb_on_mam/morphhb_reader.py`'s `BOOKS`
   list (OSIS id, tanach.us file name, ...) can seed; write the English names as a literal map
   in the script.
8. Each example shows: the reference; MAM's form; morphhb's form (as morphhb writes it, with
   its slashes); morphhb's lemma, morph code and id in `<code>`; and one Latin sentence saying
   what differs. Show Hebrew forms in MAM-normal mark order (`morphhb_reader.mnorm`); say so once
   in the method section.
9. Center tables horizontally by default (the user-level rule), keeping natural widths.

## Inputs

- `out/30-figures.json`: every headline figure (tiers, classes, slashes, maqaf, Rd).
- `out/20-coverage.txt`, `out/22-refine.txt`, `out/25-strands.txt`, `out/26-kq-ids-slashes.txt`:
  the breakdowns; read a figure from them only by parsing the file in the script.
- `10-atoms.jsonl` in the work directory, `.novc/morphhb-on-mam/work/` by default: one
  JSON record per MAM atom (fields `vid`, `on`, `text`, `class`,
  `w` with `id text lemma morph type in_qere maqaf_after`, `ws`, `sig`, `cons`, `slash`).
  Look up an example here by `vid` and morphhb id.
- `out/21-examples.json`, `out/23-lists.json`, `out/27-kq-ids-slashes.json`: example lists.
- `10-atoms-cant-alef.jsonl`, `10-atoms-cant-bet.jsonl` in the work directory: the other
  two strands.
- `research/upstream/FINDINGS.md`, `research/upkeep-shape/FINDINGS.md`: sections 5 to 7 draw
  on them; the root session has checked their material claims (its notes are in
  `research/CHECKED.md`).

## Sections

1. **The answer.** A short paragraph from the figures: feasible; 99.64% of MAM's 306,525 atoms
   (the figure `same + supported`) take morphhb's lemma, morph and id with evidence; 1,091 atoms
   (0.36%: `untested + flagged + structural`) need a rule or a person; the cost (an alignment
   that takes about 20 seconds; a review queue of the flagged and structural atoms; rules for
   the rest). Then a table of the five tiers with counts and percentages and one-line meanings:
   - **the same form**: letters equal and the vowel key equal (A1), or an unpointed ketiv with
     morphhb's ketiv's letters (K with an x-ketiv partner);
   - **supported**: the form differs, but morphhb gives MAM's form this same lemma and morph
     elsewhere;
   - **untested**: MAM's form occurs nowhere else in morphhb;
   - **flagged**: MAM's form occurs elsewhere in morphhb, never with this lemma and morph;
   - **structural**: no one-to-one partner (word division, ketiv/qere structure, words one text
     lacks).
2. **How the comparison was made.** Brief: per verse, on the ketiv side and the qere side,
   morphhb's words and MAM's atoms are aligned by their letters (the 2026-11-13 study's
   "Method 2", difflib over whole atoms); each MAM atom counted once; the vowel key ignores
   accents, meteg, rafeh, the dots and invisible marks, and reads qamats qatan as qamats and
   holam haser as holam. The test of "supported" counts how morphhb analyses MAM's exact form
   (by that key) elsewhere. Forms shown in MAM-normal mark order. Inputs: morphhb `wlc/` at
   `db6c5c9b` (identical to `d4265dfa`), MAM-simple at `374d9436`.
3. **Coverage, tier by tier.** With examples (table rows built from the records):
   - same: Genesis 1:1's first atom (show the record).
   - supported, the Tetragrammaton's holam: figures `a2_holam_only` (bare and prefixed); one
     example of each (the first records of each kind in `10-atoms.jsonl`).
   - supported, other pointing: `a2_other_than_holam_by_tier`; one example from
     `21-examples.json` key "A2 one letter: hataf-patah -> shewa / supported: ...".
   - supported, spelling: `b_by_letters`, `b_by_tier`; one example of a vowel letter missing in
     MAM and one of a vowel letter added (keys beginning "B mater ...supported").
   - flagged: 23 pointing and 36 spelling atoms (`tier_by_class`); a table of these examples,
     Claude's first reading in the last column:
     Judges 19:4 (`07GJ8`, MAM's form is a Hiphil where morphhb's morph says Qal),
     2 Chronicles 1:5 (`14A4a`, MAM has a shin dot, "there", where morphhb has a sin dot,
     "he put"), 2 Chronicles 15:16 (`144SZ`, MAM's vowel under the lamed implies the article,
     which morphhb's morph lacks), Jeremiah 11:2 (`24Rdh`, MAM's form is second person plural
     where morphhb's is singular with a suffix), 2 Samuel 15:3 (`10Jp4`, MAM has the plural),
     Psalms 68:27 (`19MkY`, a different word), Deuteronomy 2:9 (`057a3`, lemma already reads
     MAM's form, the morph WLC's), and two that are only homographs, 1 Kings 1:15 (`11VTb`)
     and Numbers 23:25 (`04QZ8`). Say that Claude's first reading counts about half of the 59
     as real changes and half as homographs or interpretive choices, and that no person has
     reviewed them; the full lists are `out/23-lists.json`'s "A2 contradicted" and
     "B contradicted".
   - untested: 707; one example; say they need a reader or acceptance by rule.
   - structural: 325, broken down from `out/20-coverage.txt` section 7 and
     `out/26-kq-ids-slashes.txt`; examples Numbers 2:12 (a name MAM writes as one atom and
     morphhb as two words), 2 Samuel 7:22 (a word each text lacks: `out/29-show-pairs.txt`
     shows that MAM reads the Tetragrammaton followed by another word where morphhb reads
     another word followed by the Tetragrammaton). Daniel 5:19 is an artifact of the
     alignment, not a missing word: two atoms in which MAM and morphhb exchange a final alef and
     he (`out/29-show-pairs.txt`) are left unpaired, two on each side; say so. Of the 25 morphhb
     words that no MAM atom matches (`out/20-coverage.txt` section 8), 20 are in Joshua 21:36-37,
     which MAM lacks, one is 2 Samuel 7:22's, two are Daniel 5:19's artifact, and two are matched
     on one side only.
   - Two checks the vowel key could hide: qamats qatan (`out/22-refine.txt` section 2: 7,389
     atoms, almost all on nouns, wayyiqtol, infinitive and imperative pieces, where it is
     expected; 52 sit on a piece whose morph is a perfect or a participle, listed in
     `out/23-lists.json` "qatan with a perfect or participle morph"; most are Hophal, Pual or
     other forms that have a qamats qatan, but in Claude's first reading two look like real
     differences: 2 Kings 8:6 (`12LrY`) and Micah 2:10 (`33PUg`), where MAM's qamats qatan
     reads an infinitive or a noun and morphhb's morph says a third feminine singular perfect;
     show both as examples and say that these two belong in the review queue although the
     vowel key counts them as "the same form") and a stress screen (section 5: 48 atoms where
     morphhb's and MAM's stress accents sit on different letters; in Claude's first reading of
     the 26 with a verb, listed in `out/28-show-stress.txt`, none needs a different analysis;
     say no more about their accents than that).
   - The nine corrections that the 2026-11-13 study found (`out/22-refine.txt` section 3):
     four land in "supported" or "untested" because morphhb's analysis already fits MAM's form;
     five are flagged because only one of lemma and morph fits it.
4. **Morpheme division.** Figures `slashes`: every morphhb slash stands directly before a
   letter, so in a letters-equal pair it moves by letter count (163,726 slashes in 145,825
   words); every matched word's morph has exactly one part per slash-separated piece; in the
   spelling pairs (B), 529 of 627 slashes are placed by aligning letters, a fallback rule
   places 72 more words, and 26 words stay ambiguous (`out/26-kq-ids-slashes.txt` section 4).
   One worked example of a letters-equal word with two or more slashes, shown as morphhb has
   it and as MAM's text with the slashes placed (`slash.mam` in the record), and one spelling
   example. The `Rd` segment (preposition with the article, whose he is not written): figure
   `rd_words_by_class`; the code needs no letter, so it carries with its piece; the one flagged
   case is 2 Chronicles 15:16.
5. **MAM's markup.** (a) Ketiv and qere: from `out/20-coverage.txt` section 4 and
   `out/26-kq-ids-slashes.txt` sections 1 and 2: MAM's ketiv is unpointed, as morphhb's is;
   1,018 ketiv atoms have morphhb's ketiv's letters; MAM's one-form cases (MAM's trivial
   ketiv/qere, and MAM writing one form where morphhb has a ketiv and a qere), with the counts of
   agreeing and differing analyses; examples 1 Samuel 2:9 and Genesis 49:10 (show MAM's form,
   morphhb's ketiv and qere with their morphs); MAM's ketiv/qere where morphhb has one word (28
   verses). (b) Maqaf: the `maqaf` figure as a small table; the analyses do not depend on it,
   because both texts' unit is the atom. (c) Dual cantillation: `out/25-strands.txt`: 24 verses,
   243 atoms, identical letters and the same morphhb word in all three strands (`cant-combined`,
   `cant-alef`, `cant-bet`, MAM-simple's names); 12 atoms differ in vowels and 11 in maqaf
   between strands; one example (Exodus 20:3's last atom in the three strands, from the three
   JSONL files, beside morphhb's). (d) Closed dispatch: what the reader found
   (`py/morphhb_on_mam/mam_reader.py`): 55 ketiv atoms that MAM-simple writes straight before the next
   atom, with no separator, where the qere ends in a maqaf (for example Numbers 23:13); an empty
   scroll-difference target at Exodus 26:6; a legarmeh inside a large-letter atom at Ruth 3:13;
   and what a product's generator would dispatch on (from `research/upkeep-shape/FINDINGS.md`).
6. **Upkeep.** From `research/upkeep-shape/FINDINGS.md` section C, as checked in
   `research/CHECKED.md`, and this design: the alignment is regenerated from scratch at each
   run; every decision a person makes is a stored statement keyed by verse, morphhb id and MAM's
   whole form (letters and every mark), and a check fails loudly when MAM's form changes under a
   statement; no hashes or pinned populations.
7. **Product shape and upstream.** From the two FINDINGS.md files, as checked: where the result
   could live and in what format, and what morphhb's README, pull requests and validator say.
   End with a pointer to the decision page, `decisions.html`, without restating its questions.
8. **What this study could not establish.** A list: whether the 707 untested atoms' analyses fit
   MAM's forms; whether each flagged atom is a real change (Claude's first reading only);
   analyses that turn on an accent beyond the stress screen; anything about the Leningrad Codex
   itself; whether morphhb's maintainers want an analysed MAPM (only documentary evidence);
   MACULA Hebrew's syntax and senses, which ride on the same ids but were not studied; the
   hours a person's review would take.
9. **Files.** One short paragraph pointing to `README.md`.

After building, extract the page's visible text to `out/40-page-text.txt` with a script and
check every figure in it against `out/30-figures.json` and the breakdown files.

## The fragment for sections 6 and 7

The root session writes sections 6 and 7, and the sentence of section 5(d) about what a
product's generator would dispatch on, as an HTML fragment, `in/page-fragment.html`, in the
folder, after checking the research reports. `build_page.py` splices that file's content in
verbatim where those parts go: the fragment holds `<section>` elements whose ids are
`upkeep`, `shape-upstream` and `generator-dispatch`; the script places each by its id. If the
file is missing, or lacks an id, the script puts in that place a paragraph saying
"Pending: this part waits for the root session's check of the research reports." and prints a
warning. The root session reruns the script after writing the fragment.
