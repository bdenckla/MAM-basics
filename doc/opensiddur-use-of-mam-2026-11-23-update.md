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
