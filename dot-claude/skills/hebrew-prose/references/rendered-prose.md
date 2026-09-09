# Rendered prose — the extra rules for published pages

These govern text a reader of a gh-pages page actually sees. They are additional to everything
in `terminology.md`, which applies to comments and docstrings as well.

The home of record is `MAM-basics/py/accgram/printed_decalogue_strands.py`'s module docstring,
whose **SCOPE** paragraph divides its bullets:

- **TRIO-ONLY** (about the printed-Decalogue pages' own subject matter): strand names in Hebrew
  letters, "signal word," the maqaf scale as a verdict ladder, the scoped "no difference
  anywhere," the `ROM_*` single-sourcing and italic wrapping, the two Simanim editions and their
  determiner, the attribute exemption.
- **REPO-WIDE**, applied to every accgram page: atom vs chanted word, "cantillation" over
  "accentuation," the real em dash, never opening an English sentence with a Hebrew word.

## Strand names in Hebrew letters

**תחתון / עליון — never transliterated and never translated.** No "taḥton"/"elyon" and no
"upper"/"lower" in the output: the upper/lower glosses invite confusion with above-letter vs
below-letter accents, which is *not* what the names mean, and for a reader who does not know the
terms no gloss beats a misleading one. The full `טעם תחתון` / `טעם עליון` appears ONLY at first
mention; after that drop the טעם — bare עליון reads as "the [טעם] עליון". Render via the `TAHTON`
/ `ELYON` constants or `render_reading_name`. Verbatim quoted source Hebrew keeps whatever it
says. Cross-repo rule; cf. MAM-basics `py/versification_and_cantillation/doc.py`.

Romanized "taḥton"/"elyon" survive only as **internal keys** and inside **attributes**.

**Exactly TWO exempt registers: attributes and internal keys.** `img alt` and `abbr title` text
is announced by screen readers and copied into plain-text contexts, where ASCII romanization
survives and a bidirectional Hebrew run does not — so the hover/screen-reader text being
romanized while the prose is Hebrew-lettered is a **deliberate asymmetry, not an inconsistency
to clean up**. Compact *notation* in visible prose is NOT a third register: an axis gloss like
"(two books × תחתון/עליון × m-trad/p-trad)" is visible prose and takes the Hebrew letters,
however schematic it looks. Only the strand words are governed; `m-trad`/`p-trad` stay.

## Romanized accent names are italic and single-sourced

Every romanized accent/mark name renders inside `<span class="romanized">` — the pages do the
wrapping, aliasing the `ROM_*` strings through `py_html.my_html_span_romanized.rmn` ONCE at
module level. Because the aliases are HTML nodes, not strings, they cannot go into an f-string:
splice them into a contents tuple. Book and apparatus terms (Tiqqun, ḥumash, Keter, qere/ketiv,
pisqa) are NOT accent names and stay unwrapped; nor is the `pashta_phrase` code identifier, which
is a checker error name.

## Typography and sentence shape

- **Real Unicode em dash** `—` (U+2014) in rendered prose. ASCII `--` is fine in code, comments
  and docstrings.
- **Never open an English sentence with a Hebrew word.** "תרצח is that same alternation…" became
  "With תרצח, we have that same alternation…" — give the sentence an English runway and let the
  Hebrew arrive inside it. A sentence-initial RTL run makes the reader resolve the direction
  switch before there is any English context to switch back to; at a paragraph start there is not
  even a preceding word to anchor it. Scoped to *English* prose: a quoted Biblical verse, a
  Hebrew-language note, and the Hebrew cells of a table are untouched. As of 2026-07-25 the trio
  and its siblings had no other violation, so any new one is newly introduced.
  **The cost is mechanical as well as a matter of reading comfort, and the rule reaches past
  rendered pages to prose written for Ben** — a bullet or paragraph *beginning* on a Hebrew word
  takes RTL as its base direction and is laid out entirely RTL, English and punctuation and list
  marker with it. Ben, 2026-08-25, of chat bullets that opened that way: *"Your output is hard to
  read because of BiDi issues."* The fixes and the failed BiDi-control-character detour are in
  `SKILL.md` §"Rendered prose has extra rules"; this bullet stays the home of the rendered-page
  half.
- **Never open a sentence with an abbreviation that cannot be capitalized.** Ben, 2026-08-03, of
  "p. 298's *qadma* fits no configuration either book allows": *"weird to start a sentence with an
  abbreviation like 'p.' since it can't really be capitalized."* Recast so the abbreviation moves
  inside — "The *qadma* on p. 298 fits no configuration either book allows" — which usually reads
  better anyway. Same session fixed "p. 246's extra *munaḥ* is…" to "The extra *munaḥ* on p. 246
  is…".
- **Cut the sentence that only insists.** Ben, 2026-08-03, of "The transcription is not in doubt:
  the mark was flagged by the diff and re-read off a zoom of the page": *"yank it: it reduces to
  'I really mean it'."* Evidence for a reading belongs in the transcription's `.txt` header, where
  a primary observation is recorded; on the page it reads as the author bracing against a doubt
  the reader had not formed. This is the sibling of "bounded doubts get no mention at all" below —
  that bans naming the doubt, this bans pre-emptively answering it.

## Cite the two books as ITM and CoS, with the full title on hover

Ben, 2026-07-28: *"'Breuer, Chapter 9' doesn't say what breuer book … use CoS and ITM
respectively, and make these hover-reveal the full title."* So `<abbr title="Introduction to the
Tiberian Masorah">ITM</abbr>` and `<abbr title="The Cantillation of Scripture">CoS</abbr>`, never
the full title spelled out in the visible prose. Both are single-sourced in
`MAM-basics/py/accgram/almost_errors_html_shared.py` as `itm()` / `cos()` — call those rather than
building an `abbr` locally, and note `COS_TITLE` keeps Breuer's leading "The".

Recorded here on 2026-08-03 because it had been living **only** in a code comment on
`maqaf_nonfinal_accents_page`, which is not somewhere a session writing a new page will look: a
new paragraph on `printed-decalogue-simanim.html` duly spelled both titles out in full and had to
be corrected.

## Quoting a source that romanizes differently: bracket OUR names in

A quotation keeps its own words, but a translator's romanizations inside one are noise to a reader
who has just read the page's. Substitute in square brackets, and say once that that is what the
brackets are. Ben, 2026-08-03, of Breuer's "a *methiga* will appear in the word of the small
*zakef*": *"use our standard romanizations in square brackets rather than introducing these
jarring, though literal, parts of the quote."*

The rendered result: “a [metigah] will appear in the word of the [zaqef qatan]”, followed by "the
bracketed names being this page's, in place of the translator's."

Two details settled at the same time. **Let the bracket swallow the whole phrase** rather than
leaving a fragment of the original stranded outside it — "the small [zaqef]" was rejected for
"the [zaqef qatan]". And **expand to `zaqef qatan` here** even though `ROM_ZAQEF_QATAN` romanizes
as a bare "zaqef" by default: the section being quoted is about which of the two zaqefs a word
takes, so the *qatan* is the point rather than a redundancy. The literal wording still belongs in
the docstrings, comments and issue bodies that cite the same passage — a citation should reproduce
what the book says.

## A table cell holding Hebrew is declared `dir="rtl"`

**Unless the whole table is already `dir="rtl"`, every cell whose content is Hebrew gets
`dir="rtl"` on the cell itself.** Right-justification is then a consequence of having said what
the cell holds, rather than a separate thing to remember — which is why the declaration and not
`text-align` is the fix. Ben, 2026-07-29, on being handed one column right-justified and the rest
of the page's tables not: *"this problem afflicts the other tables in the document as well, and
indeed is something I find myself telling you about frequently … this should just be sort of
obvious."* So it is not a per-table decision and not something to wait to be asked for: when you
add or touch a table with a Hebrew column, declare all of them.

- **Put it on the `td`, not on an inner `span`.** The `lang="hbo"` span is about the language of a
  run; the direction is a property of the cell's block.
- **Do the whole column, blank cells included.** A `Total` row's empty example cell is declared
  like the rest — the declaration describes the column, and an exception for the blank one is a
  second rule to keep in step.
- **Leave the English heading alone.** `Chanted word` / `Example` over the column is English, and
  an `rtl` declaration would misdescribe it. If Ben wants the heading moved over its column, that
  is a separate ask.
- **No stylesheet rule, and no class.** A class plus a CSS rule puts the behavior in a second file
  to look in, for something one attribute states outright. In accgram the attribute dict is
  `maqaf_nonfinal_accents_page._HEBREW_CELL`, spliced through each table's single
  `*_CELL_ATTRS` tuple so a table's body rows and its `Total` row cannot come to disagree.
- Also **abbreviate a long accent name in a cell** (`TG` with `abbr title="telisha gedolah"`,
  the title taken from the `ROM_*` constant and never retyped): a fifteen-character name sets the
  column's width and pushes the rest of the row apart. Same trade the `Acc1`/`Acc2`/`C`/`S`
  headings already make. Rendered *prose* still gets the name in full.

## No jargon, no previews

The audience is Hebrew-Bible readers, not people who know what the checker does.

- **Expand the jargon.** "Parses clean" → "is grammatical"; "genuinely different parses" →
  "genuinely different accent-grammar trees." Ben's test is *"I'm not sure whether the reader
  will understand what a 'parse' is,"* prefixed with **"as is often the case"** — a standing
  rule, not a one-off. Keep the parsing verb only where the sentence is about the act ("does it
  parse?"), not about the status of a strand.
- **No previews.** A hub sentence that trails off into what a satellite page does gets **cut**,
  not softened with an "as we shall see" cue. Same for forward-referencing a later section of the
  same page. The fact can live in a `#` comment or a docstring explaining *why* the satellite
  says what it says — it just must not be rendered. Cutting a preview usually shortens an
  already-long sentence, which is itself the point.

Grep the rendered strings (not the comments) for `parse`/`clean` as a status and for named
satellite pages.

## Bounded doubts get no mention at all

When a finding rests on a reading Ben has flagged as uncertain, and the uncertainty is
**bounded** (it discriminates nothing the page claims) and no surprising result hinges on it, the
rendered document says **nothing about it** — not a hedge, not a footnote, not a small line. Its
only reader-facing home is the GitHub issue. The page assumes the reading true and states its
verdict flat. Ben rejected even an optional footnote-style line offered "for the honesty on the
page": he is confident enough to treat the readings as true for the documents' purposes, and a
page that names doubts at that grain invites a reader to weigh them against findings they cannot
affect.

Do not offer "mention it in a small line?" as a middle option — the choice is issue-only vs page.
This governs **rendered documents only**: transcription `.txt` headers, JSON `uncertain_readings`
fields and test pins still record the doubt. An uncertainty that COULD move a verdict is a
different case and is not covered here.

## Scope a verdict's "anywhere" (trio)

Never write a bare "no difference anywhere"; write **"no difference anywhere the comparison
reaches."** What backs these cells is a hand transcription of the printed **accents**, so
"anywhere" can only mean that, and the unscoped phrasing invites a reader to take it for the
whole page — it was already false once. Two things fall outside: the **maqaf**, which the `.txt`
line records but the token stream drops (issue #75), and the **pointing** — the two תחתון strands
part at תרצח in a vowel and nothing else, which the diff cannot see. Where a vowel or a maqaf HAS
been checked off the page, say so in the cell and put the evidence in the transcription's `.txt`
comment block: that is a primary observation, and no test will defend it.

## Methodology stays out of rendered prose

How the harness works belongs in the docstring, not on the page (wlc-utils#79 tracks the sweep;
wlc-utils#77 bare "the strand" and wlc-utils#78 the two senses of "strand" are its siblings).

## Handing a page to Ben

Lead with the thing he acts on — the full clickable `file://` URL and exactly what to do with it.
Analysis, crop measurements and caveats go below, or get cut. **The bar for including anything
beyond link + instruction is a trap he could actually fall into.** Ben: "this is huge overload, I
just can't read all this. Lots of caveats I'm just going to take as 'transcribe carefully.'"
Collapsing the wall into a `<details>` block is not enough.

**Hand him the link; open nothing.** A markdown link whose href is an absolute `file:///` URL,
forward slashes:

```
[maqaf-nonfinal-accents.html](file:///C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/maqaf-nonfinal-accents.html)
```

A repo-relative link is the wrong thing — it opens the *source* in the editor. And do **not**
launch it. Ben, 2026-07-28: *"in sessions like this, I usually already have the document open, so
particularly after the first turn, this results in multiple copies up in my browser."* No
`Start-Process`, and never the Claude Browser pane — Ben, 2026-07-26, the pane is **"too
unreliable, and has yet to show any advantage over an external browser, for my needs."** Do not
burn a turn diagnosing the pane, do not reach for it as a fallback, and do not treat the global
`~/.claude/CLAUDE.md`'s older `file://`-URLs-work-in-the-pane material as a reason to try. No dev
server and no `.claude/launch.json` is ever needed for a local file.

A link gives no screenshot back, so verify content with the **Read** tool on the file — better
evidence than eyeballing anyway, and now the only evidence you have. Canonical statement: the
global `~/.claude/CLAUDE.md` §"Showing me a local file", updated 2026-07-28. The transcription
workflow's own statement is `MAM-basics/doc/edition-transcription-workflow.md` §2.
