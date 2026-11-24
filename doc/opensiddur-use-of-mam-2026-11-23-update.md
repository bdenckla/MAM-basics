# Updates to Open Siddur's use of MAM, 2026-11-23

State: open, first entry 2026-11-23. Every entry here corrects or supplements
`doc/opensiddur-use-of-mam-2026-11-23.md`, which is left as written but for the line that
points here.

## 2026-11-23: three corrections after Ben read the report

Written by Claude (Opus 5.5) on 2026-11-23. Ben read the chat report that summed up the record
and replied to four of its passages. One reply asks for a session that will explain the
Humash's four bridging ranges further, which the commander was asked to start; its findings
belong in a later entry here. The other three replies correct or sharpen the record.

### 1. Leaving out the good endings is an editorial choice, not a defect

Ben, replying to the report's "dropped good endings after Isaiah 66 and Malachi 3":

> Although they may have been dropped by accident rather than on purpose, keep in mind that it
> is a completely legitimate editorial decision to drop these, i.e. drop should not be taken to
> have a pejorative meaning here.

The record's section "Which alternative the converter keeps (item 5)" already counts "dropping
the good endings" among the converter's choices, and that stands. Two passages also count it as
a defect, and should be read without it:

1. Item 6's list, under "Text lost": "**Good endings.** The four good endings, after the last
   verse of Isaiah, Malachi, Lamentations and Ecclesiastes, are dropped with their notes."
2. The row "Good ending dropped after a book's last verse" of the table under "Which of item 6's
   defects reach the books".

The fact itself stands: the TEI holds none of the four good endings, so neither the Humash nor
the Siddur prints one. So does the rest of item 6 and of that table. The message of commit
`3d6c66b8`, which added the record, lists "drops the good endings" among the converter's
faults; this entry corrects that too.

The code does not settle whether the omission was meant; it points both ways. The wikitext step
registers a handler for the good-ending template
([miqra_wikitext.py L293](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L293))
that would carry its text forward as a `miqra:good-ending` element
([L624-L626](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L624-L626)),
and a test checks it
([test_miqra_wikitext.py L311](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/tests/importer/miqra_al_pi_hamasorah/test_miqra_wikitext.py#L311)).
But the stylesheet that makes the TEI names that element in a rule that outputs nothing
([miqra_to_tei.xslt L431](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L431)).
And neither runs on the snapshot's four good endings: the row selection skips the rows that
hold them, as the record's item 3 says under "What it reads".

### 2. "It never raises" describes how the converter uses mwparserfromhell

Ben, replying to the report's "It never raises: an unknown template stays as literal text, and
errors are swallowed":

> Is this a property of the parser, or a property of the way the parser is used (configured)?
> E.g. are there options to provide callbacks for unknown templates and errors, and the open
> siddur code just didn't avail itself of those options?

**It is a property of the way the parser is used.** The record's brief answer for item 3,
"mwparserfromhell 0.7.2, inside the processor's own handler framework, with regular expressions
before and after; it never raises", lets "it" be read as mwparserfromhell. It means the
converter, as item 3's own section makes clear under "What it does with what it does not
recognize".

1. **mwparserfromhell offers no such options, because it never interprets a template.** It
   parses every `{{…}}` into a template node holding a name and parameters, whatever the name;
   what a name means, and whether it is known, is for the caller to decide. Its `parse` takes
   only the text, a starting context and a switch that treats `''` and `'''` as plain text
   ([`parse` is `parse_anything`](https://github.com/earwig/mwparserfromhell/blob/d9a889d41791eeb4a56fa09fee3a4a7b6894f0d8/src/mwparserfromhell/__init__.py#L53),
   [`parse_anything` L37-L39](https://github.com/earwig/mwparserfromhell/blob/d9a889d41791eeb4a56fa09fee3a4a7b6894f0d8/src/mwparserfromhell/utils.py#L37-L39),
   [`Parser.parse` L68-L86](https://github.com/earwig/mwparserfromhell/blob/d9a889d41791eeb4a56fa09fee3a4a7b6894f0d8/src/mwparserfromhell/parser/__init__.py#L68-L86),
   at v0.7.2). Its one exception, `ParserError`, reports a bug in the parser itself; invalid
   markup is still parsed
   ([errors.py L26-L37](https://github.com/earwig/mwparserfromhell/blob/d9a889d41791eeb4a56fa09fee3a4a7b6894f0d8/src/mwparserfromhell/parser/errors.py#L26-L37)).
   That leniency toward malformed markup is the parser's own, and it has no strict setting, but
   it concerns markup, not templates.
2. **The processor's framework has the hooks, and its top-level loop reports what it cannot
   handle.** `MediaWikiProcessor`, written for the JPS 1917 importer, dispatches through its own
   tables of template and tag handlers. Its top-level `process_wikitext` records each unknown
   template or tag as a warning and each failing handler as an error, in the result it returns
   ([mediawiki_processor.py L665-L759](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/util/mediawiki_processor.py#L665-L759)).
   Its recursive `_process_nested_content` records nothing: it reprocesses an unknown
   template's own text, which leaves the template as it was, and retries a failing handler
   without nesting
   ([L152-L210](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/util/mediawiki_processor.py#L152-L210)).
3. **The MAM converter takes the silent path and discards what it collects.** Its
   `process_wikitext` replaces the framework's loop with the recursive path alone, and catches
   any exception for a whole cell
   ([miqra_wikitext.py L199-L224](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L199-L224)).
   Its own copy of the recursive path, with MAM's handler table and name rules, reparses an
   unknown template's text until the depth limit, which leaves it as literal wikitext
   ([L311-L335](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L311-L335)).
   And its one caller returns the converted text alone, so the result's errors and warnings go
   nowhere
   ([L675-L683](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L675-L683)).

So closed dispatch needed nothing from the parser: a raise in the unknown-template branch, or
the framework's warnings kept and checked, would have stopped the conversion at any template new
to the sheet.

### 3. "The notes kept" means kept and printed

Ben, replying to the report's "The documentation notes are kept":

> "Kept," as in "kept by the parser" but then never used, i.e. effectively discarded?

**No: kept, and printed in two of the three books.** In the record's brief answer for item 5,
"and the notes kept" means that the converter carries MAM's notes into the TEI, each in its
book file's `tei:standOff`, anchored in the running text, as the rows for מ:הערה and נוסח in
the table of "Which alternative the converter keeps (item 5)" say. The exporter prints a note
wherever a book prints MAM's text around the note's anchor and lists MAM among its
`annotations`, as the record's item 2 explains:

1. **The Humash** prints 1,903 of MAM's notes in the PDF and 1,992 in the electronic book,
   among them all 1,492 on the Torah.
2. **The Siddur** prints 2,035, among them all 1,492 on the Torah.
3. **The Haggadah** prints none, since its `annotations` list only Feinstein's English.

In a PDF the exporter sets such a note as a footnote unless a book's settings say otherwise,
and neither book's settings do; in an electronic book it shows the note as a popover
([reledmac.xslt L3969-L3974](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/tex/reledmac.xslt#L3969-L3974),
[typography.py L1036](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/typography.py#L1036),
[html.xslt L579](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/html/html.xslt#L579),
at `474cb10`). Like all of item 2, these figures come from the exporter's code; no book was
built.

## 2026-11-23: the bridging festival portions, explained

Written by Claude (Opus 5.5) on 2026-11-23, in a session that the commander started for this
question. Ben, replying to the report's line on the Humash's four bridging ranges:

> Ask the commander for a session that will explain this further. It sounds like perhaps some non-contiguous passages forming a single reading (passage one from W to X and passage 2 from Y to Z, where W < X < Y < Z) are instead rendered as one range from W to Z? And just as a sanity check, it sounds like the range that was supposed to be excluded, i.e. the range from X to Y, is at least in some cases rather huge since 2,662 extra verses is a huge number of extra verses!

**Ben's reading is right, and the excluded stretch is huge in four cases; but six portions
bridge, not four.** For a festival or special reading, the processor's humash importer takes
the day's Torah aliyot from hebcal's data, sorts each book's aliyot by their first verse, names
one range from the earliest verse to the latest, and transcludes that whole range, cut at each
aliyah's boundaries. Where a day reads two separate passages of one book, the stretch between
them becomes a piece of its own, with no aliyah marker, and is transcluded like the rest. Six
of the Humash's 82 festival and special divisions read two separate passages of one book, with
a stretch between them, and all six bridge: the four in Numbers that the record found, and the two fast-day readings, which bridge
Exodus 32:15-33:23. Together they print 2,750 extra verse occurrences and 568 extra note
occurrences, not 2,662 and 548. The same sort also prints nine divisions' aliyot out of the
order they are read. No part of the fault lies in MAM's data.

Everything here was read through GitHub's API, without a clone: the processor at `v0.7.0`,
[`723b083`](https://github.com/opensiddur/opensiddur-processor/commit/723b083c9e1f548e3c78a3b375704650093040e6),
which built the release, and whose humash importer files have the same blobs at `474cb10`, the
processor's `main` at 11:31 on 2026-11-23, New York time; the release's data, opensiddur-projects
`c91943d`, whose humash project had not changed on `main` by then; and hebcal's data in
sourcetexts at `dacca4a`, the processor's submodule pin at both commits. No book was built, and
no release file was opened.

### What joins the passages

1. **hebcal supplies the festival readings, in reading order.** The importer's `readings.py`
   says so: "MAM records no haftarot and no festival readings at all, so these come from hebcal"
   ([L3](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/readings.py#L3)).
   Its `festival_readings` reads each day's aliyot from
   [`holiday-readings.json`](https://github.com/opensiddur/sourcetexts/blob/dacca4a8e4317c4555e5c849d1a75db8df28e3dd/sources/hebcal_leyning/holiday-readings.json),
   where they stand in the order they are read, and sorts them by unit and label, so that the
   aliyot precede the maftir
   ([L223-L279](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/readings.py#L223-L279),
   the sort at L276).
2. **`festival_file` sorts each book's aliyot by verse and names one range.** It groups a day's
   aliyot by book and, for each book
   ([build.py L834-L841](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/build.py#L834-L841)):

   ```python
   ordered = sorted(book_spans, key=lambda span: (span.start, span.end))
   book = ordered[0].book
   start = min(span.start for span in ordered)
   end = max(span.end for span in ordered)
   parts.append(_citation_milestone(_citation_range(book, start, end)))
   segments = model.segment_reading(
       ordered, sourcetexts_root=sourcetexts_root
   )
   ```

   The sort puts the aliyot in book order, whatever order the day reads them in; the citation
   milestone names one range, from the first verse to the last; and `segment_reading` gets no
   start or end.
3. **`segment_reading` then cuts the whole range at the aliyot's boundaries.** Given no start or
   end, it takes them from the spans and, unless two spans of one unit overlap, hands the range
   to `segment_by_union`
   ([model.py L165-L169](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/model.py#L165-L169)):

   ```python
   if allow_duplication and has_internal_overlap(spans):
       return segment_by_span(spans)
   start = start if start is not None else min(span.start for span in spans)
   end = end if end is not None else max(span.end for span in spans)
   return segment_by_union(spans, start, end, sourcetexts_root)
   ```

   `segment_by_union` is written for a continuous reading: "Cut `start`-`end` at every span
   boundary, emitting the text once"
   ([L78](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/model.py#L78)).
   Every boundary opens a segment that runs to the next boundary, and only an empty segment is
   skipped
   ([L93-L107](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/model.py#L93-L107)).
   Its docstring shows that the gap was foreseen: "each span's end closes one, so that a span
   which ends before the next one begins does not swallow the gap" (L80-L81). That keeps the
   gap out of the aliyah before it, but the gap remains a segment, opened by no marker, and
   `_segment_xml` transcludes it like any other
   ([build.py L506](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/build.py#L506)).
4. **Only the festival Torah readings take this path without bounds.** A parashah passes its
   own start and end, which is right for "one continuous reading"
   ([build.py L568-L578](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/build.py#L568-L578)).
   A haftarah goes through `_passage_xml`, which transcludes each span by itself, in hebcal's
   order
   ([build.py L670-L695](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/build.py#L670-L695)),
   as the docstring of `readings.py` models a haftarah: "an ordered list of spans, because a
   haftarah is frequently discontinuous" (L4-L5).

### The six bridging portions

In each paragraph, hebcal's data gives the day's aliyot in reading order; the Humash's division
at `c91943d` holds the citation and transclusions quoted; and the gap is the stretch between the
two passages in book order. Where the release puts the gap is read from the division's TEI, not
from a released book: the gap's transclusion carries no marker of its own, so the book would run
it on as part of the aliyah before it, faced by JPS 1917 like every MAM range in the book.

1. **The sixth day of Hanukkah** (`reading/chanukah_day_6`). hebcal's data gives the Rosh
   Hodesh passage, Numbers 28:1-5, 28:6-10 and 28:11-15, as aliyot 1 to 3, and then Hanukkah's,
   Numbers 7:42-47, as aliyah 4. The division's citation milestone names "במדבר 7:42–28:15",
   and it transcludes aliyah 4's 7:42-47 first, then 7:48-27:23 with no marker, then aliyot 1 to 3
   ([reading_chanukah_day_6.xml L29-L38](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_chanukah_day_6.xml#L29-L38)).
   The gap, Numbers 7:48-27:23, holds 681 verses. It would follow the fourth aliyah's text,
   which itself comes first, and precede the first aliyah's marker.
2. **The seventh day of Hanukkah on Rosh Hodesh** (`reading/chanukah_day_7_on_rosh_chodesh`).
   hebcal's data gives Numbers 28:1-15 as aliyot 1 to 3 and Numbers 7:48-53 as aliyah 4. The division
   names "במדבר 7:48–28:15" and transcludes 7:48-53 (aliyah 4), 7:54-27:23 with no marker, then
   aliyot 1 to 3
   ([L29-L38](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_chanukah_day_7_on_rosh_chodesh.xml#L29-L38)).
   The gap, Numbers 7:54-27:23, holds 675 verses, and would stand where the sixth day's does.
3. **Shabbat Rosh Hodesh during Hanukkah** (`reading/shabbat_rosh_chodesh_chanukah`). The first
   six aliyot are the week's parashah, outside this division. hebcal's data gives Numbers 28:9-15 as
   aliyah 7 and the sixth day's Hanukkah passage, Numbers 7:42-47, as the maftir. The division
   names "במדבר 7:42–28:15" and transcludes the maftir's 7:42-47 first, then 7:48-28:8 with no
   marker, then aliyah 7's 28:9-15
   ([L29-L34](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_shabbat_rosh_chodesh_chanukah.xml#L29-L34)).
   The gap, Numbers 7:48-28:8, holds 689 verses. It would follow the maftir's text, itself
   printed before the seventh aliyah, and precede the seventh aliyah's marker.
4. **The fourth day of Hol HaMoed Pesah** (`reading/pesach_chol_hamoed_day_4`). hebcal's data
   gives Numbers 9:1-5, 9:6-8 and 9:9-14 as aliyot 1 to 3 and Numbers 28:19-25 as aliyah 4. The
   division names "במדבר 9:1–28:25" and transcludes the four aliyot in that order, with
   9:15-28:18 between aliyah 3 and aliyah 4's marker
   ([L29-L38](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_pesach_chol_hamoed_day_4.xml#L29-L38)).
   The gap, Numbers 9:15-28:18, holds 617 verses, and would run on as part of the third aliyah.
5. **The morning of a fast day** (`reading/fast_day_morning`). hebcal's data gives Exodus 32:11-14,
   34:1-3 and 34:4-10 as aliyot 1 to 3. The division names "שמות 32:11–34:10" and transcludes
   32:11-14, then 32:15-33:23 with no marker, then 34:1-3 and 34:4-10
   ([L29-L36](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_fast_day_morning.xml#L29-L36)).
   The gap, Exodus 32:15-33:23, holds 44 verses, and would run on as part of the first aliyah.
6. **The afternoon of a fast day** (`reading/fast_day_afternoon`). hebcal's data gives Exodus 32:11-14
   and 34:1-3 as aliyot 1 and 2 and 34:4-10 as the maftir. The division's Torah portion is the
   morning's, with the same 44-verse gap after the first aliyah
   ([L29-L36](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_fast_day_afternoon.xml#L29-L36));
   its haftarah, Isaiah 55:6-56:8, is unaffected.

Ben's reading needs two refinements. The single range is cut at the aliyot's boundaries, so the
gap is one transclusion of its own rather than part of a longer one; and on the three Hanukkah
days the passage read first is the later one in the book, Numbers 28, yet the importer still
prints Numbers 7 first.

**Ben's sanity check holds: in the four Numbers portions the excluded stretch is about half of
the book.** Each of those days pairs a passage of Numbers 7 or 9 with one of Numbers 28, some
twenty chapters later, so each gap holds 617 to 689 of Numbers' 1,289 verses. The fast-day gap
is smaller, 44 verses, because Exodus 34 is only two chapters after 32. The counts are of the
verse milestones of the release's MAM project, which follow the processor's canonical numbering,
WLC's; the processor's versification table records that MAM itself makes canonical Numbers 25:19
the head of its own 26:1
([versification.py L130-L133](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/common/versification.py#L130-L133)),
so by MAM's numbering each Numbers gap is one verse shorter.

**No part of the fault lies in MAM's data.** The readings, and their order, come from hebcal's
data, which lists each day's aliyot as they are read, for example Rosh Hodesh's three before
Hanukkah's one; the joining and the reordering are the importer's. MAM's own divisions, the
aliyah markers of the sheet's column D, reach only the weekly parashot, through `aliyot.py`'s
`read_markers`. MAM supplies the words of the festival portions, the gaps' words among them, and
the 568 note occurrences in the gaps print because MAM's text there prints.

### The other portions that read two or more passages

I checked the Torah part of all 82 festival and special divisions against hebcal's data,
verse by verse, with hebcal's numbering of Exodus 20 and Deuteronomy 5 converted as the
processor converts it, and every haftarah portion of two or more passages, in the festival
divisions and the 55 haftarah divisions alike.

1. **A bridge:** the six portions above, and no other.
2. **Aliyot out of reading order, nine divisions:** the three Hanukkah divisions above, and the
   six Sukkot divisions in which aliyah 4 reads again the offerings of the days before. In
   `reading/sukkot_chol_hamoed_day_1` to `_day_5`, aliyah 4 is printed second, after aliyah 1;
   in `reading/sukkot_final_day_hoshana_raba`, third, after aliyah 2. The cause is the same sort
   (build.py L834) followed by `segment_by_span`, whose docstring says that it emits "each span
   as its own segment, in reading order"
   ([model.py L112](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/model.py#L112)),
   but which receives the spans in book order.
3. **A misplaced instruction, in the same six Sukkot divisions.** The instruction
   "חוזרים על הפסוק", that the verses are read again, stands before aliyah 4, which does read
   them again, but also before aliyah 2 (aliyah 3 on Hoshana Raba), whose verses are read there
   for the first time. `segment_by_span` marks a span as a repeat when it overlaps any span
   emitted before it
   ([model.py L120-L123](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/model.py#L120-L123)),
   and the misplaced aliyah 4 was emitted before it. On the first day, for example, the division
   prints Numbers 29:17-19 (aliyah 1), then the instruction and 29:17-22 (aliyah 4), then the
   instruction and 29:20-22 (aliyah 2), then 29:23-25 (aliyah 3)
   ([reading_sukkot_chol_hamoed_day_1.xml](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_sukkot_chol_hamoed_day_1.xml)).
4. **Alternatives printed as one sequence:** `reading/sukkot_shabbat_chol_hamoed` holds the five
   maftirs that hebcal's data keys by the intermediate day on which that Shabbat falls, Numbers 29:17-22,
   29:20-25, 29:23-28, 29:26-31 and 29:29-34, each marked with its day. A congregation reads one
   of them, but no condition chooses, so all five print in a row under one citation,
   "במדבר 29:17–29:34", with the repeat instruction before the second to the fifth
   ([L44-L58](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_sukkot_shabbat_chol_hamoed.xml#L44-L58)).
   There is no bridge and no reversal.
5. **Sound:** the other portions of two or more passages. Weekday Rosh Hodesh
   (`reading/rosh_chodesh`), whose aliyot 1 and 2 share Numbers 28:3, prints that verse twice,
   with the instruction before aliyah 2, as it is read. The 30 other divisions whose Torah
   reading spans two or more books print each book's passage once, in reading order:
   `pesach_i`, `pesach_i_on_shabbat`, `pesach_ii`, `pesach_ii_chm`, `pesach_chol_hamoed_day_1`
   to `_day_3`, `pesach_shabbat_chol_hamoed`, `pesach_vii`, `pesach_vii_on_shabbat`,
   `pesach_viii`, `pesach_viii_on_shabbat`, `shavuot`, `shavuot_i`, `shavuot_ii`,
   `shavuot_ii_on_shabbat`, `rosh_hashanah_i`, `rosh_hashanah_i_on_shabbat`,
   `rosh_hashanah_ii`, `yom_kippur`, `yom_kippur_on_shabbat`, `sukkot_i`,
   `sukkot_i_on_shabbat`, `sukkot_ii`, `shmini_atzeret`, `shmini_atzeret_on_shabbat`,
   `simchat_torah`, `simchat_torah_on_shabbat`, `shabbat_shekalim_on_rosh_chodesh` and
   `shabbat_hachodesh_on_rosh_chodesh`. Of the other divisions, 27 read one contiguous passage
   and 11 have no Torah portion. The weekly parashot are continuous readings with explicit
   bounds and cannot bridge.
6. **Haftarot: sound, but for one disagreement within the importer.** All 48 haftarah portions
   that print two or more passages transclude them one by one, in hebcal's order, Mishpatim's
   backward step from Jeremiah 34 to 33 included. Forty-seven equal hebcal's data as written.
   The 48th, Emor's year-3 triennial portion, equals it once hebcal's spelling Nachum is allowed
   for and its closing piece, Nahum 2:2b-3a, is dropped: the importer drops a closing piece that
   lies inside an earlier one, as the verse on which the pairing with the parashah turns
   ([readings.py L151-L177](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/readings.py#L151-L177)).
   In Ki Teitzei's year-3 portion the same rule drops Isaiah 48:20, which the importer has just
   corrected from hebcal's "4:20" with the comment that the verse is read again after 48:21
   ([L95-L103](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/importer/humash/readings.py#L95-L103)).
   Which of the two is right is unresolved here; the portion prints Isaiah 48:12-21 alone.

### Corrections to the record

1. The brief answer for item 2, "Four of the Humash's festival Torah portions print hundreds
   of extra verses of Numbers through faulty ranges in its own divisions", should say six: four
   print hundreds of extra verses of Numbers, and the two fast-day portions 44 of Exodus each.
2. Item 4 of "The Humash (annual cycle)", "Four festival Torah portions each hold one range that
   bridges two passages of Numbers, so each also prints the 617 to 689 verses between them",
   should add the two fast-day portions, which bridge Exodus 32:15-33:23, 44 verses each; and
   "Together the four bridges add 2,662 verse occurrences and 548 note occurrences to both
   compiles" should read: the six bridges add 2,750 verse occurrences and 568 note occurrences.
   Its "A defect in the humash's divisions, not in MAM" stands; those divisions are what the
   processor's humash importer generates from hebcal's data.
3. Under the same heading, "The figures include the four bridges; without them the occurrences
   would total 11,893 in the PDF and 13,709 in the electronic book": the table's figures include
   all six bridges, since they count every transclusion, and without them the occurrences would
   total 11,805 and 13,621. Exodus's 1,833 occurrences include the fast-day bridges' 88.

### What this entry could not cover

No book was built. Whether the released books print the gaps was read here from the
release's TEI and the exporter's rules; the books were checked later the same day, with Ben's
approval, and the next entry gives the result. Nothing had been said to Open Siddur when this
entry was written.

## 2026-11-23: the released books print the bridges

Written by Claude (Opus 5.5) on 2026-11-23, in the session that wrote the entry above. Ben,
answering the two questions that entry left open, exactly:

> I concur with your recommendation for decision 1: please download the two released Humash files and use them to check whether they print the gaps.

and, on whether Open Siddur should be told:

> in spirit I choose "You [Ben] tell them" but I would like you (Claude) to do the telling and the form I choose, unless you object, is a pull request. Isn't this fixable in code? In fact I'm hoping the download of the two Humash files is just to verify that indeed these are code-generated and not hand-fixed to eliminate these problems.

**Both released books print all six bridges, where the TEI puts them, and nothing in them looks
hand-edited: the faults are the code's, all the way to the books.** A separate session is
preparing the pull request that fixes the importer; it puts the pull request's text to Ben before
opening it, and its outcome belongs in a later entry here.

1. **The files,** from opensiddur-projects' release `v20261108`, downloaded on 2026-11-23 with
   Ben's approval and kept untracked:
   `chumash-opensiddur-he-annual-v20261108.pdf`, 9,439,943 bytes, SHA-256
   `AB1CBC29101BAA28488F79D64FB9FC43F4BAD583A924A7CA8D4C9778FBB26D10`; and
   `chumash-opensiddur-he-annual-v20261108.html`, 17,925,002 bytes, SHA-256
   `4092B707402F94CE9F8B2013725186814B68737B50E155E678204938843F6E3C`.
2. **The electronic book.** A sub-agent's script compared each checked division of the HTML file
   with the release's TEI, item by item. All six gaps print where the TEI puts them, each Hebrew
   verse faced by JPS's English. The Sukkot weekday divisions print their aliyot in the order 1,
   4, 2, 3 (1, 2, 4, 3 on Hoshana Raba), with the repeat instruction where the TEI has it, and the
   Shabbat of the intermediate days prints its five maftirs in a row. The two controls, the fifth
   day of Hanukkah and the first day of Hol HaMoed Pesah, print only their own verses. Each
   Hebrew verse checked in Exodus and Numbers, 3,047 in all, matches MAM's TEI letter for letter,
   marks included. Checked again by a script of this session's own: the section of the sixth day
   of Hanukkah holds 1,404 verse markers, its 702 verses in two columns (6, then the gap's 681,
   then 15), with chapter markers 8 to 28; that of the fourth day of Hol HaMoed Pesah, 638
   verses (14, 617 and 7); that of the fast-day morning, 58 (4, 44 and 10); and that of the fifth
   day of Hanukkah, 12.
3. **The PDF.** The sub-agent's reader of the PDF's text found the same six gaps in the same
   places, and the same Sukkot faults; in these divisions the PDF differs from the HTML file only
   in setting the repeat instruction on its label's line. The sixth day of Hanukkah's gap runs
   from printed page 1069 to page 1151 (pages 1071 to 1153 of the file). This session read page
   1151 by eye: under the running heads of the festival readings and of the sixth day of
   Hanukkah, it ends Numbers 27 with verses 22 and 23, and only then sets the first aliyah's label
   and Numbers 28:1.
4. **No sign of a hand edit.** Nothing in the checked divisions differs from the TEI. The PDF's
   metadata gives one time for its creation and its last change, 2026-11-08 23:12:07 UTC, from
   LuaHBTeX, and the file has one cross-reference section, which suggests that nothing was added
   to it after it was written; the release was published at 23:36:49 UTC that day. The TEI is
   itself code-generated: the session that prepared the processor's pull request to read
   MAM-parsed/plus reported that its regeneration of the humash reproduced all 195 files of the
   release's commit, `c91943d`, byte for byte. This session did not repeat that regeneration.

## 2026-11-23: narpas, legarmeh and the space between verses

Written by Claude (Opus 5.5) on 2026-11-23, in the session that took over the review of Open
Siddur's pull request
[opensiddur/opensiddur-processor#316](https://github.com/opensiddur/opensiddur-processor/pull/316).
That pull request's body listed two behaviors of the TEI as known issues, and this record counts
both among its defects. Ben doubts both. His words, of 2026-11-23:

> Failing to distinguish narpas from legarmeh is a common editorial choice. As usual, it *could*
> be an accident, but it is far from safe to assume that it was an accident.

And of the TEI's lack of any character between verses:

> But it seems to me an legitimate encoding (albeit a bit burdensome to the edition-generating
> application) that says "if there's no special whitespace between verses, supply your own space"

### 1. Writing narpas and legarmeh alike is an editorial choice, not a defect

Two passages count it as a defect, and should be read without that:

1. Under "Whether MAM's templates are navigated well (item 4)", the caution "**Narpas and its
   spacing.**"
2. Under item 6, in the list "**Distinctions lost.**", the item "**Narpas and legarmeh.**"

The facts stand: מ:פסק and מ:לגרמיה-2 both become HEBREW PUNCTUATION PASEQ, no markup says which
is which, and MAM's spacing survives. But the printed tradition writes them alike too. MAM's
introduction, chapter 2, section ד, says that Unicode has one character for both and that the
printed editions all set the stroke alike, and MAM tells the two apart on its page only by its
two templates' look: a bold stroke after a thin space for legarmeh, a small gray stroke between
thin spaces for narpas
([ch2.mediawiki L242-L244](https://github.com/bdenckla/MAM-basics/blob/aa92904ca59c718259794bb8cf273dfdc7150ba8/in/mam-ws-intro/ch2.mediawiki?plain=1#L242-L244)).
The consumer notice of MAM-parsed plus asks nothing about the distinction: its rule on narpas
says only that narpas forms no compound and that the spacing around it is the edition's choice.

The TEI still tells most strokes apart by their spacing, since MAM's text, as MAM-parsed plus
has it, never puts a space after narpas and puts one after most legarmeh: of the 2,295 strokes in
the running text of the TEI at `c91943d`, 1,686 are followed by a space and 482 by a letter. The
other 127 stand beside markup, where spacing does not say which they are.

The code does not settle whether the processor's author meant it. The wikitext step labels the
two, as `miqra:punct` with `type="legarmeh"` or `type="paseq"`
([miqra_wikitext.py L595-L599](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L595-L599)),
and the stylesheet's one rule for them prints only the character
([miqra_to_tei.xslt L374-L376](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L374-L376)),
as it prints the gray maqaf as a plain maqaf, which the consumer notice expressly allows. That
rule dates from the importer's first commit, `b1f2246`, and no comment, test, README, changelog
entry or issue says why.

### 2. Nothing between verses is an encoding, not fused atoms

Two passages count it as a defect, and should be read without that:

1. Under item 4's cautions, the last clause of "**Whitespace templates dropped, fusing
   atoms.**": "and between verses the TEI has no whitespace at all, only a milestone, at 18,896
   verse boundaries."
2. Under item 6, in the list "**Atoms fused and whitespace lost.**", the item "**Between
   verses.**"

The facts stand. What the record did not say is where the rest of column C goes: a parashah
break, the song layout's included, becomes a paragraph boundary, closing the paragraph after the
sof pasuq and opening the next with the verse's milestone. Only the plain space and the template
ר4 are left out.

Nor did it say how the books separate verses. Both of the processor's exporters print each verse
milestone as a superscript verse number, with a thin space after it and nothing before it
([reledmac.xslt L2261-L2293](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/tex/reledmac.xslt#L2261-L2293),
[typography_tex.py L585-L599](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/tex/typography_tex.py#L585-L599),
[html.xslt L502-L511](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/html/html.xslt#L502-L511),
[reader.css L77-L81](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/html/assets/reader.css#L77-L81)).
The processor's WLC text puts a space before nearly every verse milestone, and its JPS 1917 text
a space, a line break or a paragraph's start; MAM's puts nothing there unless a paragraph
starts. So in the books MAM's verse number stands against the sof pasuq before it, and a book
that hid verse
numbers, as the setting `markers.verse_numbers: hidden` allows and no book in
opensiddur-projects does, would run MAM's verses together. This is read from the code; no book
was built.

The code does not settle intent here either. The stylesheet's comment "Column C: only parashah
markers structure paragraphs; // line breaks are cosmetic." dates from the importer's first
commit
([miqra_to_tei.xslt L93-L98](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L93-L98)),
and the importer's README calls column C "Navigation / header wikitext"
([README.md L57](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/README.md#L57));
neither names the space.

Item 6's "**Poetic line breaks.**", which counts the 4,269 ר4 of column C as dropped, stands as
written. The message of commit `3d6c66b8`, which added the record, names neither behavior.

## 2026-11-23: the pull request that fixes the festival portions

Written by Claude (Opus 5.5) on 2026-11-23, in the session that took over the festival pull
request from the session that prepared it. That session put the pull request's title, body and
commit messages to Ben for approval, and asked whether to open a second pull request, to
opensiddur-projects, with the regenerated humash. It recommended approving the texts as written
and not opening the second pull request now. Ben, exactly:

> I concur with both of your recommendations.

**[opensiddur/opensiddur-processor#320](https://github.com/opensiddur/opensiddur-processor/pull/320),
"Print each festival Torah reading's aliyot in the order read, and only their verses", opened on
2026-11-23 at 13:09 New York time, fixes the humash importer so that each festival division
prints only the verses read, in the order in which they are read.** It is how Open Siddur was
told of the faults that the entries "2026-11-23: the bridging festival portions, explained" and
"2026-11-23: the released books print the bridges" describe, in the form Ben asked for in the
second of them; nothing else has been said to Open Siddur.

1. **The branch,** `festival-readings` on Ben's fork, `bdenckla/opensiddur-processor`, holds two
   commits on the processor's `main` at `474cb10`: the fix, `7917a2c`, and the changes that an
   independent code review led to, `1bcbe38`. Together they change
   `opensiddur/importer/humash/build.py` and `opensiddur/importer/humash/model.py`, add
   `opensiddur/tests/importer/humash/test_festival_readings.py`, and add a bullet to the
   `[Unreleased]` section of `CHANGELOG.md`.
2. **The fix.** `festival_file` no longer sorts a day's aliyot by verse and transcludes one range
   from the first verse to the last. It keeps hebcal's order, cuts the aliyot into runs that are
   read without a break, segments each run by itself, and opens each later run with a citation
   of its own, as the importer already did for a haftarah read from two passages. The repeat
   instruction is decided over the whole reading, in reading order, and the five maftirs of
   Shabbat Hol HaMoed Sukkot, which hebcal keys by the day on which that Shabbat falls, no
   longer count as repeating one another.
3. **The regeneration,** without validation, since jing does not run where the work was done.
   At `474cb10`, with sourcetexts at its pin, `dacca4a`, the importer reproduced all 195 humash
   files of opensiddur-projects' `c91943d`, the release's commit, byte for byte, which repeats,
   independently, the regeneration that "2026-11-23: the released books print the bridges" took
   from another session's report. With the fix, 13 files change: the six bridging divisions, the
   six weekday Sukkot divisions and `reading_sukkot_shabbat_chol_hamoed`; the other 182 do not.
   A separate script written for this survey, which compares each festival division's
   transclusions with hebcal's aliyot verse by verse, finds none of the release's faults in the
   branch's files. It still reports the day-keyed maftirs, because it counts any overlap as a
   repeat.
4. **The tests.** The humash's 154 tests pass, rerun at `1bcbe38` when this entry was written.
   Against `main`'s code, the new test fails for exactly the 13 divisions and for 366 of its 493
   synthetic arrangements. The whole suite, run on Windows without jing or the compiled schema,
   fails the same 248 tests on `main` and on the branch. No check had run on GitHub when this
   entry was written.
5. **What the pull request leaves to Open Siddur:** whether a volume for one date should print
   only the maftir for its own day, and the regenerated humash for opensiddur-projects, which
   the pull request's body offers to submit. By Ben's answer at the head of this entry, Claude
   opens that second pull request only if Open Siddur asks for it and Ben agrees.
6. **Ben's two other open pull requests in that repository,**
   [opensiddur/opensiddur-processor#316](https://github.com/opensiddur/opensiddur-processor/pull/316),
   branch `mam-parsed-plus`, and
   [opensiddur/opensiddur-processor#319](https://github.com/opensiddur/opensiddur-processor/pull/319),
   branch `windows-tests`, each share only `CHANGELOG.md` with the festival pull request, and git
   merge-tree reports no conflict with either one's head, `90e28d2` or `e01c63a`. The festival
   pull request's body mentions neither.

## 2026-11-23: answering the review of pull request 316

Written by Claude (Opus 5.5) on 2026-11-23, in the session that answered the review of
[opensiddur/opensiddur-processor#316](https://github.com/opensiddur/opensiddur-processor/pull/316),
by a sub-agent of that session, from the facts that the session checked. Efraim Feinstein
submitted the review on 2026-11-23 at 22:05:48 UTC, 17:05 New York time. The session found each
of its eight comments accurate and put ten decisions to Ben: a commit and a reply for each
comment; whether the new commits should follow Open Siddur's conventions where two of Ben's
standing rules differ; and whether to edit the pull request's description and post a summary
comment. Ben, at 18:05 New York time, exactly:

> I accept all 10 of your recommendations.

**Six commits on the pull request's branch fix what all eight comments found; a reply under each
comment, a summary comment and an edit of the description say so on the pull request. The pull
request now waits on Open Siddur.**

1. **The review,** in the state "Commented", holds a thank-you, for the contribution and for
   being told that MAM's Google Sheet is no longer maintained, and eight inline comments. CI's
   "Run Tests" had passed on the head reviewed, `90e28d2`.
2. **The new commits follow Open Siddur's conventions where two of Ben's standing rules
   differ,** as the session recommended. The processor's tests include example-based unit tests
   of synthetic cases, which Ben's rules add only when he asks for one, and its Python files are
   not formatted with Black, which Ben's rules run on every changed Python file.
3. **The commits,** `90e28d2..7f224c1` on `mam-parsed-plus`, the pull request's branch on Ben's
   fork, `bdenckla/opensiddur-processor`, were written by a sub-agent of the session, checked by
   the session and pushed at 18:44 New York time, a fast-forward. Under each commit are the
   comments whose findings it fixes, numbered in GitHub's order:
   1. `32ba582`, "Convert every MAM book before writing any, so that --only-book numbers notes
      as a full run does":
      [comment 1](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654647),
      that with `--only-book` the pull request's converter, `convert.py`, restarted the note
      ids at `miqra-note-1`, and
      [comment 5](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654673),
      that `convert.py` found a missing book only after it had written the files of the books
      before it. The pull request did not introduce the fault that comment 1 found: the TSV
      converter on the processor's `main` had numbered notes the same way, through a
      module-level processor.
   2. `50e5627`, "Retry a rate-limited 403, and fail at once when GitHub asks for a wait over a
      minute":
      [comment 2](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654657),
      that `download.py` failed on a 403 carrying `Retry-After` as on a bare 403, and
      [comment 3](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654664),
      that its waits for `Retry-After` and `X-RateLimit-Reset` had no bound.
   3. `feda7b5`, "Replace the unit test that read the real download with convert --check":
      [comment 4](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654668),
      that a unit test in `test_miqra_plus.py` read the real download in sourcetexts.
   4. `06afc42`, "Read the humash's aliyah markers through the converter's load_source":
      [comment 6](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654680),
      that the humash's `aliyot.py` read the files of MAM-parsed plus without the converter's
      checks, and the first part of
      [comment 7](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654687),
      that `aliyot.py` duplicated the converter's loading.
   5. `572a6c9`, "Keep one copy of the patterns and the XML escaping that the importer defined
      twice": the rest of comment 7, three smaller duplicates, of the full-SHA pattern, the
      number pattern and `_xml_escape`.
   6. `7f224c1`, "Check the download's files byte for byte, leaving line ends to sourcetexts'
      .gitattributes":
      [comment 8](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4672654695),
      that `download.py` handled CRLF in three places, where one line of `.gitattributes` in
      sourcetexts fixes the cause.
4. **The checks,** made by the session:
   1. The MAM importer's and the humash's tests pass after each of the six commits: 271, 273,
      274, 275, 275 and 272 tests, in the commits' order, against 269 at `90e28d2`.
   2. The MAM project and the humash, regenerated without validation, since jing does not run
      where the work was done, are byte for byte what `90e28d2`'s tree produced, all 44 files
      and all 195, at both pins, MAM-basics `632ff4b` and MAM-parsed `8a254bf`.
   3. `--only-book` writes, for Exodus, for Hosea and for II Chronicles, exactly the file that
      the full run writes.
   4. The processor's whole suite, run on Windows without jing or the compiled schema, ran 2,951
      tests, and the same 243 failed as on the processor's `main` and at `90e28d2`.
   5. No pointed Hebrew in the changed files changed.
   6. git merge-tree finds no conflict between the new head and the heads of
      [opensiddur/opensiddur-processor#319](https://github.com/opensiddur/opensiddur-processor/pull/319),
      `e01c63a`, and
      [opensiddur/opensiddur-processor#320](https://github.com/opensiddur/opensiddur-processor/pull/320),
      `1bcbe38`; and git diff --name-only from the processor's `main`, `474cb10`, to each head
      shows that the new head still shares only `CHANGELOG.md` with pull request 320. This
      repeats, for the new head, item 6 of the entry "2026-11-23: the pull request that fixes
      the festival portions".
5. **By an eleventh decision, the replies and the summary comment each say that a Claude session
   wrote them, and the description says who edited it.** Before posting, the session loaded
   Ben's `github-issues` skill, whose rules say that every comment or body edit a session writes
   says that it is agent-written and gives the date. The plan that Ben had accepted under the
   tenth decision said that the replies would carry no such line, so the session asked him
   whether each reply and the summary comment should open with a line saying that a Claude
   session wrote it, and the description end with a dated line saying who edited it. It
   recommended yes. Ben, at 19:59 New York time, exactly:

   > For decision 11, follow your recommendation.

6. **The description,** edited at 19:59 New York time (00:59:49 UTC on 2026-11-24), changes the
   three passages that Ben approved: the download's bullet, on rate limits and waits; the
   converter's bullet, on converting every book first, `--only-book` and `--check`; and step 1
   of "Order of merging", which now requires the sourcetexts commit that adds the download to
   carry the `.gitattributes` line `sources/miqra_al_pi_hamasorah/** -text`. After its line
   saying that it was generated with Claude Code, it now ends with the line "Edited on
   2026-11-23 by a Claude session, with Ben's approval, to describe the commits that answer the
   review." Read back from GitHub, the stored description equals what was sent.
7. **The replies,** posted at 20:00 New York time, one under each comment, each open with
   "Written by a Claude session on 2026-11-23, at Ben's request." Read back from GitHub, each
   equals what was sent. In the comments' order, they are the replies to comments
   [1](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674123621),
   [2](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674123891),
   [3](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674124071),
   [4](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674124271),
   [5](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674124487),
   [6](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674124685),
   [7](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674124877) and
   [8](https://github.com/opensiddur/opensiddur-processor/pull/316#discussion_r4674125120).
8. **[The summary comment](https://github.com/opensiddur/opensiddur-processor/pull/316#issuecomment-7118657993),**
   posted at 20:00 New York time with the same opening line, thanks Efraim Feinstein, gives the
   six commits as the range `32ba582` to `7f224c1`, and says that at the pinned commit the MAM
   project's 44 files and the humash's 195 are byte for byte what they were before the six
   commits.
9. **What is left to Open Siddur:** approving the run of CI's "Run Tests" on `7f224c1`, which
   waits for a maintainer's approval, as it did after the first push; merging; the sourcetexts
   commit that adds the download, with that `.gitattributes` line; and regenerating
   opensiddur-projects. The paired pull requests that the description offers, to sourcetexts and
   opensiddur-projects, remain only offered.
