# Transcribing a printed edition's Decalogue

The procedure behind `in/accgram/edition_transcriptions/`, tracked by
[#69](https://github.com/bdenckla/wlc-utils/issues/69). Written down so a session can pick the
work up from here rather than from a long handoff.

**The Python behind this procedure lives in the sibling repo since 2026-08-01** (`6180f8d` took
it out of wlc-utils with the rest of the code): every `py/...` path in this doc names a file
under `C:/Users/BenDe/GitRepos/MAM-basics/py/`, which is why every command below runs from
`C:/Users/BenDe/GitRepos/MAM-basics`, with that repo's interpreter. The `in/`, `out/`,
`gh-pages/` and `.novc/` paths still name this repo, which the code writes back into. The same
mapping covers the module names inside the committed transcription headers under
`in/accgram/edition_transcriptions/`: all twelve name `accgram/transcription_editor.py`, four of
the twelve name a further module — `zoom_line.py`, `printed_decalogue_taxton_diff.py`,
`printed_decalogue_simanim_page.py`, `test_edition_transcriptions.py` — and all five of those are
files under `MAM-basics/py/`. The headers themselves are left exactly as written: they are the
provenance record of how each transcription was read, not live pointers, so a module changing
repos is no reason to edit one (Ben's decision of 2026-08-04,
[#90](https://github.com/bdenckla/wlc-utils/issues/90)). `col_profile.py` and `row_profile.py`,
named in `simtiq_ex_elyon.txt`, have nothing to resolve to at either end: they were untracked
`.novc` scratch, tracked in neither repo, and were unfollowable already on the day that header
was written.

**Division of labour: the assistant displays, aligns and reports; Ben reads the accents.** A
transcription's header claims primary observation read off the book, and the tests pin its
divergences as established — so a machine-read token would be recorded as an edition's real
divergence rather than caught as an error. Offer zoomed crops to make the reading easier; never
offer your own token readings as the transcription.

**This whole procedure is for a *paper* edition — a page to read.** A *digital* edition, whose
accents are already Unicode, is not transcribed at all: it is fetched and diffed, and none of
§§1–4 below applies. That is a different track — no editor, no scan, no `corrected_from`, no
uncertain readings — written up under [Digital sources](#digital-sources-fetched-not-transcribed)
at the end.

## 1. Find the page and build the editor

**Every tool this procedure uses is a subcommand of one entry point,
`py/main_edition_transcription.py`** — `scan-page`, `editor`, `zoom-line`, `check`, `build`.
None of the five modules under `py/accgram/` is runnable on its own; `--help` on the entry
point lists them, and `--help` on a subcommand gives its flags.

Scans live outside the repo (see the `book-scan-page-naming` note; `WLC_SCANS_DIR` overrides
the root). Render a whole page first to locate the Decalogue:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py scan-page "Feldheim Simanim Tiqqun" C208 --width 1100
```

Then build the per-line editor. **Default to the whole page — pass no `--crop` at all:**

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py editor "Feldheim Simanim Tanakh" A5-D-0297 --name simtan_dt_taxton_p297 --width 2000 --debug
```

**A crop is worth measuring only when a foreign column has to be excluded.** That is the
Simanim Tiqqun and nothing else so far: it sets two columns, and a two-column page profiled
whole has no clean troughs, since the columns' lines do not align. Marginal verse numbers and
sidenotes are *not* a reason to crop — they fall inside their own line's band and produce no
spurious ones. On a single-column edition a measured crop is worse than useless: it is where an
edge lands a few pixels inside a prepositive or a postpositive, silently. Verified on Simanim
Tanakh pp. 297–298 (2026-07-23), where the whole page gives one band per printed line on both,
against a measured crop that had come out with 26 px of clearance at one edge.

Raise `--width` rather than reaching for a crop to make the text legible on screen. Width
affects only the reading; `zoom_line` works from the export's source-pixel coordinates and is
unaffected by it.

`--debug` writes `<stem>-lines.png` with the detected bands drawn on. **Check it before anyone
types into the editor, and take the band NUMBERS off it** rather than counting printed lines:
whether the running head and the ornament rule merge into one band or split into two shifts
every number below them, and which happens turns on `--width`.

**Hand Ben a `file:///` link to `.novc/scans/<stem>-editor.html` and open nothing** — a
markdown link with an absolute path in forward slashes, which he clicks into his own default
browser. A Decalogue spanning two printed pages gets one editor per page, so one link each.

**Do not launch it** — Ben, 2026-07-28: "in sessions like this, I usually already have the
document open, so particularly after the first turn, this results in multiple copies up in my
browser." No `Start-Process`. **And do not reach for the in-app Browser pane** — Ben,
2026-07-26: it is "too unreliable, and has yet to show any advantage over an external browser,
for my needs." A link returns no screenshot, so verify with the **Read** tool on the file,
which is better evidence than eyeballing anyway.

No dev server and no `.claude/launch.json` are needed or wanted either way.

**If a task genuinely needs the pane's introspection** (console, network, live DOM), a
`file://` URL with an absolute path in forward slashes *can* work — it is unreliable, not
impossible, so try once and move on rather than diagnosing it: `preview_start` with
`file:///C:/.../wlc-utils/.novc/scans/<stem>-editor.html`, then `tabs_context` to see which
tab actually holds it, then a screenshot **with an explicit `tabId`**. Four things mislead,
each looking like "the file did not load": `computer` without a `tabId` fails
input-validation, which reads as a load failure on the first screenshot; `navigate` reports
success while the content lands in a different tab than the id passed, leaving the named one
answering "No site is open in this tab"; the pane fits an image to the viewport and does not
scroll, so a tall debug overlay is unreadable there and the Read tool on the PNG is the better
check anyway; and the "renders as static snapshots" note means only that there is no
live-reload — scripts run, the editor's inputs accept typing, and its `localStorage` survives
across sessions, which is what makes the typed-line persistence below work at all.
Regenerating a PNG in place will **not** refresh an open tab, so write a fresh filename and
open a fresh tab, and screenshot before believing any of it.

### When a crop IS needed

Everything below applies only to the two-column case above. Crop tight enough horizontally to
exclude the neighbouring column: a sliver of foreign glyphs at either edge shows up in the
debug overlay.

**That "tight" is about the HORIZONTAL bound only. Vertically, just crop to the lines you want.**
`--crop`'s top and bottom name the lines to transcribe, not the region to detect over. The editor
grows the detected region about a line past them each way, gives an entry field only to the bands
whose centre falls inside what you asked for, and renders the neighbours it pulled in as dimmed
**context** strips. That context is the point — Hebrew stacks marks above *and* below its letters,
and a line's own above-marks are what let them be told apart from the line above's below-marks —
but including it is now the editor's job, not a bound you have to land by hand.

The old dead zone went with it. There used to be no safe tight vertical bound: a crop trimmed to
the text clipped the outermost line's marks, while a crop clipping only a *sliver* of the next
line left a fragment that `_absorb_slivers` folded into the last real band — on Koren A5-D-281 a
bottom of 0.5945 clipped line 17, and 0.610/0.614, chosen to dodge exactly that, gave the last
band 208 and 232 px against a true 127. The grow makes the requested boundary lines interior, so
neither can happen; the region detected over is no longer yours to choose. See
[#71](https://github.com/bdenckla/wlc-utils/issues/71).

The export records both meanings: `render.crop` is the lines you requested, `render.detect_crop`
the grown region actually rendered. An export with no `detect_crop` predates this change and its
`render.crop` still means the region that was rendered — every transcription committed before it
is of that kind. `zoom_line` reads only `render.crop`'s left and right, so it is unaffected either
way.

The merge warning survives as a backstop — the editor still complains when a transcribable band is
too tall to be one line — but the old edge-touching *note* no longer fires on the lines you type:
on a grown crop the edge bands are context, drawn dimmed and unnumbered, so the debug overlay tells
context from transcribed line by colour, not by a warning to read.

**Measure the column's edges; do not eyeball them.** On C247 a crop guessed by eye landed
~0.006 of the page width inside the true right edge and clipped the first letter of every line
— in RTL, where the line *starts*. The debug overlay does not show this: a third of a letter
missing still looks like a line. Profile the ink instead (dark-pixel fraction per x column over
the text's vertical band) and set the crop from the numbers, then leave a margin. Only
*prepositive* accents sit at a word's right edge, so a right-edge clip endangers those; a
left-edge clip endangers postpositives.

## 2. Ben types; **Save JSON** exports to Downloads

**Hand over the editor, do not merely announce that it exists.** The handoff is a step of this
procedure, not a courtesy at the end of one: paste the `file://` URL of each page's editor in
full so it can be clicked, and say which bands to type and which are context to leave blank. A
turn that ends with the setup described and no link is a turn that has not delivered the thing
the transcriber needs. **Do not open the editor in the in-app Browser pane to hand it over** —
it renders badly there and the transcriber uses an external browser anyway; reach for the pane
only when a task needs introspection an external browser cannot give. Keep the reasoning behind
the setup out of the handoff, or below the instructions, and keep it short: what belongs at the
top is the URL, the band ranges, and any question only Ben can answer (whether the edition
distinguishes paseq from legarmeh, say).

Hebrew is typed, not Latin: translating every mark in your head while holding your place on the
line is the thing to avoid. Any **unique prefix of the accent's Hebrew name** works — `זר`
zarqa, `פז` pazer, `סג` segolta — and the full name always does. An ambiguous prefix is rejected
with its candidates rather than guessed. `תג`/`תק` and `גר` are explicit exceptions.

Three ways to record a pasoleg, and which one is right is a fact about the **edition**, not
about the position: `מונ_לג` (`mun_leg` in the `.txt`) asserts munaḥ legarmeh, `[פסק]`
(`[paseq]`) asserts a narrow-sense paseq, and `[פסלג]` (`[pasoleg]`) says only that a stroke
stands there. The third exists because not every edition draws the distinction — Koren prints
the stroke without saying which it is, so either of the first two would claim more than the
book does. Record which the edition does in the `.txt` header, as
`pasoleg_kinds: distinguished` or `not distinguished`; a test then holds a `not distinguished`
transcription to using no kind-asserting notation, in either file and either spelling.

**Read the edition's own front matter before treating any of this as unobservable.** The
Simanim Tanakh's introduction turns out to document its whole sign system, sixteen numbered
*ma'alot* over pp. י-כז (scans `2-10`…`2-27`), and two questions that had been left open or
assumed were answered flatly there. Its sixteenth says the narrow-sense paseq is printed as a
**hollow** bar throughout the volume, leaving the solid bar to legarmeh — so `pasoleg_kinds` for
that edition is documentary, not an inference from a sibling volume. Its ninth identifies the
small **zigzag stroke above a letter**, which sits higher than any accent and is easy to mistake
for one, as the **rafe**, restored "partially" in four listed situations. Both were noticed as
puzzles on the page first; neither needed to be. Where the front matter draws a sign in a display
font it may not match the body font — the introduction's rafe is a solid bar, the body's is the
zigzag — so match a sign by the **example word**, not by its shape: the introduction's rafe
example is Joshua 1:2 וכל־העם, and the main text at Joshua 1:2 has the zigzag over that same kaf.

All sixteen of that introduction's *ma'alot* are indexed in
[`doc/simanim-tanakh-signs.md`](simanim-tanakh-signs.md), which leads with the four signs that can
be mistaken for accents — the rafe, the hollow-vs-solid stroke, the doubled accent of ma'ala 11
that is nonetheless **one** accent, and the chronology ring that sits at accent height. Read it
before transcribing anything further from that volume.

Three joiners now, and they are not interchangeable. `-` is a **maqaf**, binding two accents
into one chanted word (`mun-mer`). `+` is its **simple-word** counterpart — two accents on a
word that is no compound at all, as in `קד+גר` on ויצאך (p. 247), where the first accent is by
convention called *metigah* rather than *qadma*. Both contribute one token per accent; keeping
them distinct is what lets a difference still be placed on the scale — at the maqaf, or a rung
up in the accents themselves. `_` binds two
**marks** into one accent (`מונ_לג`) and contributes one token.

Where the joiners are implemented matters, because it once went wrong. `+` was added to
`edition_transcription.py` and not to `transcription_check.py`, which split chunks by its own
copy of the same rule; the .txt came out right while the check that guards it rejected `קד+גר`
as an unknown abbreviation. Splitting a chunk into its accents now lives in one function,
`edition_transcription.editor_accents`, which the check and the .txt writer both call, and
`test_editor_export_and_txt_agree` runs an export down both routes so a future divergence fails
a test rather than surfacing as a puzzling runtime message.

## 3. Check before committing

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py check $HOME/Downloads/simtiq_dt_elyon_p208-transcription.json $HOME/Downloads/simtiq_dt_elyon_p209-transcription.json --key dt elyon printed
```

It reports token and chanted-verse counts, every difference region with the reference word and
the printed page and line it came from, and the pasoleg placements **and kinds** — the
transcribed side mapped through the diff into reference coordinates first, since the two sides
index different token streams and an insertion upstream of a pasoleg would otherwise shift it
off its reference position. Run it on a partly typed page too — a problem then shows up before
the rest is typed.

The **kind** is comparable because the vendored source keeps `{{מ:לגרמיה}}` and `{{מ:פסק}}` apart
in `faithful_chanted_verses` ([#74](https://github.com/bdenckla/wlc-utils/issues/74)), beside the
folded `chanted_verses` that collapses both to U+05C0 and that every other consumer reads;
`edition_transcription.reference_pasoleg_kinds` reads them back out. So a transcribed `mun_leg`
or `[paseq]` is checked against the strand's **own** reference rather than against glyph shape
and grammar, and `[pasoleg]` asserts no kind and leaves nothing to compare. Both halves are
pinned in `test_edition_transcriptions.py`: the reference kinds per strand
(`test_vendored_reference_preserves_the_pasoleg_kinds`) and every kind claim each transcription
makes (`test_transcription_pasoleg_kinds_round_trip_against_the_reference`, which pins the number
of strokes compared too, so a regression that quietly stopped comparing cannot pass vacuously).

For any difference, before calling it an accent difference:

- **Look at the word.** If the two texts divide words differently (maqaf vs. space), the marking
  usually follows mechanically. "Usually" — a maqaf compound *can* bear two accents, written
  `mun-mer`; p. 246 has two.
- **Zoom the printed line** and let Ben re-read it. Never crop at the band edge:
  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py zoom-line <export.json> 12
  ```
  `zoom_line` pads a full band height above, because a tight crop once cut the upper dot off a
  zaqef qatan and left something that reads exactly like a revia. It also pads *sideways* past
  the crop it was given, so that a too-tight page crop cannot bound the zoom made to check it.
  A zoom shows the padding band above as a second line of text — the line being adjudicated is
  the **lower** one.
- **Check all eight strands** before concluding whose divergence it is:
  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py check --site השבת לקדשו
  ```
  The site is located by the skeleton of the word *and* of the word after it. Confirm all eight
  strands are **listed**, and that every zero-hit row has an explanation — the word is absent
  from that strand's text, or the pair straddles a chanted-verse boundary there — rather than a
  skeleton typo. Do not expect eight *hits*: a word present in all eight gives eight, and the
  השבת example above is one (Deuteronomy's tenth commandment opens ולא where Exodus's opens לא,
  and a filter that missed that once made a four-strand result look like eight), but a
  legitimate discriminator gives fewer — `אתה ובנך` hits only the two `ex/taxton` strands.

## 4. Commit the pair

`<stem>.txt` (canonical for the parser) and `<stem>.json` (the audit trail: what was typed, per
line, against coordinates in both the rendering and the source scan, with the scan's sha256). A
two-page Decalogue puts both exports under `pages`, in page order. Derive the `.txt` from the
corrected export rather than typing it, so the two cannot drift; a correction made after export
goes into the JSON with the superseded reading kept in `corrected_from`, and into the `.txt`
header.

**Both of those are one tool now — the `build` subcommand. Do not write a script per
transcription.** Thirteen near-duplicate ones had accumulated in `.novc/` before it existed
([#72](https://github.com/bdenckla/wlc-utils/issues/72)), and the last two had already diverged
on whether a page's trailing empty lines are dropped — which is a difference in what gets
committed, not in style.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_edition_transcription.py build <stem> --export <path>... --corrections <path>
```

- `--export` takes one downloaded export per page, **in page order**; more than one gets the
  `pages` wrapper, one is committed as the bare export.
- `--corrections` and `--uncertain` are `{"p298": {"15": <value>}}`, keyed by the page label
  `transcription_check` reports an origin as. Both are **throwaway files** — write them in
  `.novc/`. The committed JSON is the durable record, since an applied correction keeps the
  superseded reading in `corrected_from`; a tracked sidecar would be a third copy of the same
  two strings. A key naming a page or a band that does not exist raises rather than silently
  applying to nothing.
- **The `.txt` header is never rewritten** — only the body beneath it. Write the header by hand
  above the first derived body, and re-run with `--derive-only` after any later edit; that is
  also the re-run after a post-export correction.
- Empty `.txt` lines: **trailing** ones are dropped per page (the whole-page editor's bands run
  past the Decalogue's end — eleven of them on p. 298), **interior** ones kept (a printed line
  that really carries no accent; dropping it would shift every line number after it).
- `--check` re-derives every committed stem's body and reports any that would change. The suite
  runs it too (`test_the_committed_txt_is_byte_for_byte_its_own_derived_body`), so the mandatory
  derive rule above is enforced by the tool that implements it rather than alongside it.

Then pin the result in `py/tests/test_edition_transcriptions.py`: the divergence list (exactly,
even when empty) and the chanted-verse count.

**A new transcription also gets a grammaticality verdict, and three things have to be regenerated
for it to be recorded** ([#52](https://github.com/bdenckla/wlc-utils/issues/52)).
`transcription_parse` runs every committed transcription through the prose checker against the
strand its header names, so:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_accgram.py run-printed-decalogue
```

writes it into the `transcriptions` section of
`out/accgram/printed-decalogue/_printed_decalogue.json` — per chanted verse, its status beside the
strand's, plus any `departures`. Then add the stem to its edition's verdict table on the Simanim or
Koren page (the row's fourth cell is written by hand; the fifth comes from the checker, so a stem
with no committed transcription fails the page build) and regenerate the three pages with
`generate-html`. Pin the verdict in `test_edition_transcriptions.py` too: a departure appearing
where none is pinned means an edition prints an accent sequence the prose grammar rejects and
nobody has looked at it.

## What the harness cannot tell you

**The review loop is asymmetric.** It flags only positions where transcription and reference
already disagree, so only those get re-read. "No divergences" means no divergence survived a
procedure that never inspects the agreeing majority. The Exodus elyon's two real divergences
cancelled in the token count, so equal totals are not agreement either.

**On a page where a divergence is expected, the asymmetry runs the other way** — the loop
re-examines only positions that already disagree, so on such a page it pushes toward
*confirming* the thing you went in expecting. Run the eight-strand `--site` check before
forming a view, not after, and where possible get evidence the loop had no stake in. The one
that worked on p. 247 was **re-running the whole comparison against a different strand**: the
transcription agreed with the p-trad everywhere except the Shabbat commandment and with the
m-trad exactly there, the two partitioning the differences with nothing left over. Agreement
over a contiguous run with a strand nothing had flagged is positive evidence; a flagged
position surviving a re-read is not.

**A stroke is invisible to the token diff — its kind, and its presence.** Legarmeh and
narrow-sense paseq both fold onto a plain munaḥ on either side of the comparison
(`edition_transcription._LEGARMEH_TOKENS`), so exchanging the two, or omitting a stroke
outright, moves neither the difference list nor the token counts. `simtiq_dt_taxton` is the
live case: the page prints one stroke where its p-trad strand has two — nothing on אתה, which is
part of what makes it depart to the m-trad there — and no difference region says so. The strokes
are checked separately, in the report's own pasoleg section (§3), so read that section: "0
difference regions" is not a statement about them. The scanner layer is only partly better — a
stroke in a legarmeh position does change its token, but one the positional rule does not fire on
comes out as a plain munaḥ, indistinguishable from no stroke at all, and the stream-for-stream
comparison against the strand runs only for the seven stems that diverge nowhere.

**What the separate check on the strokes still cannot reach.** An edition that does not draw the
distinction is not checked at all: Koren prints the stroke without saying which kind it is, so all
fourteen of its strokes are written `[pasoleg]` and the round trip compares none of them.
`transcription_parse.scanner_pasoleg_kinds` does determine all fourteen — the scanner's
positional rule, a munaḥ + stroke before a revia — and agrees with the vendored reference at
every one; but that is the grammar's answer rather than the book's, and being positional it is
blind to what is printed, so it can supply a kind an edition withholds and could never
corroborate one an edition states. A stroke landing inside a difference region has no exact
reference counterpart and goes uncompared too — none does in any of the twelve, and the report
prints `in a difference region at ref N` where it would. And the kinds have a second,
independent source only for the m-trad: MAM-parsed-plus carries them per stroke (cell E, the two
strands split by `מ:כפול` א/ב) and `test_decalogue_m_trad` pins that the two sources agree stroke
for stroke, but the plus tree holds no printed tradition, so the four p-trad strands rest on the
single vendored copy — see [#68](https://github.com/bdenckla/wlc-utils/issues/68).

## Digital sources (fetched, not transcribed)

Everything above is for a paper edition. A **digital** edition — one whose accents are already
Unicode — has no page to read, so it is not a transcription: it is a **vendored strand**, fetched
and diffed by machine. The one done so far is CTR, the Complete Tanach with Rashi on chabad.org
([#73](https://github.com/bdenckla/wlc-utils/issues/73)); it is the same edition the Simanim page
links to as "a p-trad Bible on the web". Only its two running-text Decalogues exist online, Exodus
20 and Deuteronomy 5.

**What is gone, and why.** There is no primary observation to audit, so the whole audit apparatus
is absent: no line editor, no page scan or coordinates or sha256, no `corrected_from`, no
`uncertain_readings`. The bytes *are* the reading. A transcription's authority is that a human read
the marks off the page; a digital strand's is that nobody did — so the header claims a retrieval,
not an observation, and the tests pin what the fetch found rather than what a reader saw.

**The two pieces.**

- `py/accgram/ctr_decalogue_fetch.py` is a network author-tool, in the mould of
  `printed_decalogue_fetch.py`: it fetches the two chapter pages, extracts the accent-exact Hebrew
  per verse, strips rendering cruft only (inline tags, the parenthetical ketiv note beside a qere,
  non-breaking spaces, the bare ס/פ setuma/petuha markers) while **keeping CTR's own encoding
  intact**, and writes the vendored `in/accgram/ctr_decalogue.json` with its provenance. Chabad
  `403`s a bare tool User-Agent, so it sends a browser one. `--cache <dir>` re-vendors an
  already-fetched snapshot without hitting the server again — use it rather than re-fetching.
- `py/accgram/ctr_decalogue.py` is the comparison, and it runs **at the glyph level, not the
  accent level**. A paper transcription resolves each mark to an accent because a reader
  distinguishes a qadma from a pashta, or a yetiv from a mahapakh, by grammar and position — a
  distinction the two members of each pair do not draw *graphically*. A digital source gives no
  such reading, and CTR's encoding is nonstandard on top of that (it reuses one code point per
  lookalike pair and leans on vowel-relative order — MAM-basics' `rocc_2_pre_vowel_accents_in_ctr`
  documents this), so its bytes recover the **glyph** reliably but not always the accent. So each
  lookalike pair is folded onto one glyph (qadma≡pashta, yetiv≡mahapakh, germuq≡geresh). This hides
  nothing that matters: the accents that discriminate elyon from taxton and p-trad from m-trad are
  not lookalike pairs, so the fold leaves every discriminator intact and gives up only the
  azla-vs-pashta / mahapakh-vs-yetiv distinction CTR could not have expressed anyway.

**The trap that replaces the review loop's asymmetry.** The glyph fold could in principle
*manufacture* agreement, the way the paper loop's "re-read only the disagreements" can manufacture
a clean result. The guard is the same in spirit: **the cross-strand re-run is mandatory**. Compare
against the *other* tradition too; if agreement does not collapse there, a clean match against the
expected strand is suspect. For CTR it collapses hard — Exodus 139/142 vs the elyon against 80/142
vs the taxton; Deuteronomy 163/164 vs the taxton against 90/164 vs the elyon — which is the
positive evidence, not the clean number on its own.

**What it still takes a human to settle** is which strand the edition follows and what the residual
differences mean — the same judgement §3 asks for, minus the reading. CTR's answer was a surprise
worth stating: its **Exodus 20 carries the ta'am *elyon*** word-accents, not the taxton a running
text was expected to hold (though it keeps its own numbered-verse division, 16 chanted verses, not
the elyon's 9), while its **Deuteronomy 5 is the *taxton***, division and all. Every residual
difference in both books is conjunctive — a munax CTR prints on a non-final atom of a maqaf
compound, or a munax/merkha swap — so the disjunctive skeleton, which is #69's surviving claim,
holds. `py/tests/test_ctr_decalogue.py` pins all of it.
