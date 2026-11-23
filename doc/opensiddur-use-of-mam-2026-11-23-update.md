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

Whether the released books print the gaps, and how, is read from the release's TEI and the
exporter's rules: no book was built, and opening a release file is a download that waits on
Ben's approval. Nothing has been said to Open Siddur.
