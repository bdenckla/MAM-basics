# Open Siddur's use of MAM, 2026-11-23

State: completed 2026-11-23

Written by Claude (Opus 5.5) on 2026-11-23, from research done on 2026-11-22 and analyses done on
2026-11-23. On 2026-11-22 Ben asked a Claude session to "research how (if at all) repos in the
"opensiddur" organization use
https://github.com/opensiddur/sourcetexts/tree/master/sources/miqra_al_pi_hamasorah". On
2026-11-23 he concurred with that session's two recommendations, to keep its findings in a
tracked file and not to clone opensiddur-projects to search all of its files, and asked for
more, exactly:

> 1. implement those recommendations (meaning, put the findings in a tracked file, since your recommendation for decision 2 is to do nothing)
> 2. describe how much of mam is used in the uses you found (the uses you found being the Humash (MAM facing JPS 1917), the Heidenheim Haggadah and the Expanded Ashkenazi Siddur. the xumash will I imagine use the whole Torah but, for example, does it also contain haftarah selections? and what passages appear in the haggadah and the siddur?
> 3. describe how the wikisource of the sheet is parsed, e.g. a custom parser or mediawikiparserfromhell or something else?
> 4. evaluate whether the templates of mam (its tree-structured data) seems to be navigated well, i.e. used in one of the expected ways
> 5. describe what decisions are used in optional data, e.g. what branch of the qamats template is used, etc.
> 6. describe what custom processing is applied to MAM e.g. changing the Unicode strings in MAM
> 7. create a pull request switching from use of the tsv downloads to use of MAM-simple JSON or MAM-parsed-plus, whichever is more appropriate

This record is item 1. Its sections on items 2 to 6 follow the research's findings. Item 7, the
pull request, is a separate task, and its outcome is not recorded here. All the research was
read-only, through GitHub's API: no opensiddur repository was cloned, nothing was fetched from
opensiddur.org, and nothing has been said to Open Siddur. No human has reviewed this record.

**Commits read.** On 2026-11-22: sourcetexts `master` at
[`13f7844`](https://github.com/opensiddur/sourcetexts/commit/13f78447830420ca961a31ce267f639c9f9c0792),
opensiddur-processor `main` at
[`307d80d`](https://github.com/opensiddur/opensiddur-processor/commit/307d80df3299c7069d02371661b8ff5307017f78),
opensiddur-projects `main` at
[`cb8714e`](https://github.com/opensiddur/opensiddur-projects/commit/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658),
and opensiddur-infra `main` at
[`cbbf4d0`](https://github.com/opensiddur/opensiddur-infra/commit/cbbf4d07668194aef0464d296539a5437bec6133).
On 2026-11-23, for items 2 to 6: opensiddur-processor `main` at
[`474cb10`](https://github.com/opensiddur/opensiddur-processor/commit/474cb10ebb49261d672c693550003c0f45960463),
three commits after `307d80d`, all three in its exporter and none in its MAM importer;
opensiddur-projects at its release commit
[`c91943d`](https://github.com/opensiddur/opensiddur-projects/commit/c91943dc9ec9b039447bbed358e982cc529ae621);
and sourcetexts at
[`2243ced`](https://github.com/opensiddur/sourcetexts/commit/2243ced3187e1364efefc088867784356400e547),
the one commit that wrote MAM's directory there. `main` of opensiddur-projects and `master` of
sourcetexts had not moved by 04:57 on 2026-11-23, New York time.

## Answers to items 2 to 6, in brief

1. **Item 2, how much of MAM the books print.** The Humash prints the whole Torah from MAM, all
   5,853 verses, and also its haftarah portions, the five megillot and its festival and special
   portions: 8,395 distinct verses of MAM in the PDF and 9,183 in the electronic book. The
   Siddur prints from MAM its Torah, maftir and haftarah portions, Hallel, most of its psalms,
   Esther and the Song of Songs: 9,387 distinct verses. The Haggadah prints none of MAM's text
   or notes, although its settings name MAM as a fallback. Four of the Humash's festival Torah
   portions print hundreds of extra verses of Numbers through faulty ranges in its own
   divisions.
2. **Item 3, the parser.** mwparserfromhell 0.7.2, inside the processor's own handler
   framework, with regular expressions before and after; it never raises.
3. **Item 4, the navigation.** Partly as expected: every template in the snapshot is named and
   the common ones are handled as MAM-basics expects, but the walk keeps unknown templates as
   text, reparses its own output, infers meaning from shape and checks no template's
   parameters, and those departures cause the defects of item 6.
4. **Item 5, the choices.** Both ketiv and qere and both strands of a dual-cantillation passage
   are kept, as TEI alternatives, and the books print both, one in parentheses; the qamats and
   stress-helper templates keep the branch MAM-simple keeps; the combined text of a
   dual-cantillation passage and the good endings are dropped, and the notes kept.
5. **Item 6, the processing.** No Unicode normalization, so MAM's mark order survives, and
   263,648 of 263,826 tokens are unchanged; but 88 verses differ, among them 25 verses of Job
   left empty, six qere-only words replaced by URLs and four forms of ירושלמה given the wrong vowel,
   and atoms are fused in 21 places.

## Who reads the directory

**One repository reads the directory: opensiddur-processor.** Its MAM importer wrote the
directory in the first place, by downloading MAM's Google Sheet. Two of its programs read the
directory, through the processor's `sourcetexts` Git submodule: the converter reads the six TSV
files that hold the books, and the README tab, and writes the TEI project
`tanakh-miqra_al_pi_hamasorah-he` into the processor's other submodule, opensiddur-projects; and
the humash importer reads the Torah tab again, for its parashah, aliyah and maftir divisions.

**Everything else uses what the processor made from the directory, not the directory itself.**

1. **opensiddur-projects** holds the converted project, 44 TEI files: the 39 books, an index and
   four division indexes. It also holds the humash project, `chumash-opensiddur-he`, whose
   divisions came from the directory and whose portion files name verses without text of their
   own. Three of its books' settings draw MAM's text from the converted project, and all three
   are in its release `v20261108` of 2026-11-08: the *Humash (annual cycle)*, MAM facing the JPS
   1917 translation; the *Heidenheim Haggadah with English translation*, which fills biblical
   text missing from the Haggadah from MAM; and the *Expanded Ashkenazi Siddur*, which takes
   Bible text from MAM after its own and the humash's and prints MAM's notes.
2. **opensiddur-infra**, the hosted builder, pins that release of opensiddur-projects and the
   processor's `v0.7.0`, and builds books from them on request. None of its 134 files names MAM.
3. **sourcetexts** only stores the directory.
4. **The other fourteen repositories** name no MAM file that code search can find, and every one
   of them was last pushed before the directory was committed, so none can pin a sourcetexts
   commit that contains it.

## Inside opensiddur-processor

1. **Two code paths read the directory, not one.** Besides the converter described below, the
   humash importer reads `sheets/torah.tsv` directly.
   [`aliyot.read_markers`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/aliyot.py#L179-L196)
   takes column D, each verse's `{{מ:פסוק}}` template, and keeps the `{{מ:עלייה}}` template
   nested in it, whose parameters name the parashah, the Shabbat aliyah, the weekday aliyah, the
   maftir and the forms for combined parashot
   ([docstring](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/aliyot.py#L1-L29)).
   It converts MAM's verse numbers to the processor's canonical numbering
   ([L161-L176](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/aliyot.py#L161-L176))
   and ends each division where the next begins
   ([L225-L352](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/aliyot.py#L225-L352)).
   The humash build
   [calls it](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/build.py#L1005-L1008),
   and the humash's index cites MAM as the "Source of the weekly parshah, aliyah and maftir
   divisions"
   ([build.py L975-L980](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/build.py#L975-L980)).
   The converter
   [strips the `{{מ:פסוק}}` template whole](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L24-L27),
   so the TEI project carries none of these markers. A cross-check against hebcal lists four
   known differences
   ([crosscheck.py L37-L45](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/crosscheck.py#L37-L45));
   hebcal's data, not MAM, decides which haftarah and festival portions there are
   ([readings.py L1-L7](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/readings.py#L1-L7)).
2. **Which tabs are read.** The converter reads the six book tabs, `torah` among them; the
   humash reads column D of `torah` again; the converter reads `readme` for the index's front
   matter. No shipped code reads `templates`, `special`, `changes`, `auto_edits` or
   `manifest.json`, though the download
   [writes all eleven tabs](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/download.py#L40-L53).
3. **Nothing re-imports MAM automatically.** The processor's four workflows run exporters,
   validators and release modules, never the MAM download, the converter or the humash build.
   The books are rebuilt by opensiddur-projects' monthly
   [`release.yml`](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/.github/workflows/release.yml#L14-L17),
   which calls the processor's
   [`release-projects.yml`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/.github/workflows/release-projects.yml#L183-L233)
   to build every settings file at the projects' `main` with the
   [newest processor release](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/.github/workflows/release-projects.yml#L107-L115).
   So newer MAM data would reach the books only after someone reran the download, the converter
   and the humash build by hand and committed the results to sourcetexts and opensiddur-projects.
4. **MAM's verse numbering is a fixed table.**
   [`DIVERGENCES`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/common/versification.py#L113-L140)
   records where MAM numbers verses differently from WLC, whose numbering the processor makes
   [canonical](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/common/versification.py#L33-L41):
   the Decalogue in Exodus 20 and Deuteronomy 5; Numbers 25:19, which it says MAM reads as the
   start of its 26:1; Joshua 21:36-37, which it says MAM lacks; and the ends of Jeremiah 30 and
   1 Samuel 23. Its comment says the table came from aligning MAM's TSV with WLC's XML verse by
   verse.
   [`canonical_verses.py`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/canonical_verses.py#L168-L171)
   raises when MAM's source and the table disagree, and `validate_versification` checks the
   Tanakh projects' verse URNs for duplicates and gaps in the projects' validation gate
   ([validate-projects.yml L237-L244](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/.github/workflows/validate-projects.yml#L237-L244)).
   Item 6's differential check, below, found the TEI's verse milestones in agreement with the
   table at every one of the 117 MAM verses that it renumbers or splits.
5. **The license travels with the text.** The colophon builder,
   [`metadata.py`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/exporter/metadata.py#L1-L57),
   gathers the licenses of every file a book drew on, so a book that sets MAM's text should list
   CC BY-SA 4.0; the released books were not opened to see it. The humash project declares CC0
   for itself and cites MAM only as the source of its divisions
   ([build.py L970-L980](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/humash/build.py#L970-L980)).
6. **No record of which MAM was converted.** No processor document names a MAM revision or date;
   the sourcetexts pin listed with each release in the changelog is the only record
   ([CHANGELOG.md L111-L114](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/CHANGELOG.md#L111-L114)).
   The changelog's MAM fixes: in 0.2.0, of 2026-08-17, the Ten Commandments had come out as empty
   verses in Exodus 20 and Deuteronomy 5, and 54 verses had been lost at parashah breaks
   ([L702-L709](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/CHANGELOG.md#L702-L709));
   0.7.0, of 2026-11-08, renamed the project from `miqra_al_pi_hamasorah` to
   `tanakh-miqra_al_pi_hamasorah-he`
   ([L61-L86](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/CHANGELOG.md#L61-L86)).

## The chain, with evidence

1. **MAM's Google Sheet to sourcetexts.** opensiddur-processor's
   [`download.py`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/download.py#L28-L53)
   names the sheet's id, its XLSX export URL and the eleven tab names it keeps;
   [`download_miqra`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/download.py#L129-L185)
   downloads the workbook once, splits each kept tab into a UTF-8 TSV, writes `manifest.json`
   with row counts and SHA-256 sums, and deletes the workbook. Its output directory comes from
   [`pages.py`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/util/pages.py#L165-L177),
   under
   [`SOURCETEXTS_ROOT`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/common/constants.py#L6-L9),
   the `sources` directory of the
   [`sourcetexts` submodule](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/.gitmodules#L1-L4).
   sourcetexts'
   [README](https://github.com/opensiddur/sourcetexts/blob/13f78447830420ca961a31ce267f639c9f9c0792/README.md#L4)
   says its sources were committed directly or downloaded by the processor's import
   preprocessors. The importer's own
   [README](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/README.md#L63-L65)
   still says that only the download is implemented; the converter below shows that sentence is
   out of date.
2. **sourcetexts to the TEI project.**
   [`convert_tsv.py`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L33-L43)
   reads only the six book tabs (torah, neviim_rishonim, neviim_acharonim, sifrei_emet,
   chamisha_megillot, ketuvim_aharonim), with a comment not to ingest the special, AutoEdits and
   other tabs. For each book it
   [selects the rows](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L450-L504)
   whose page key names the book, parses the wikitext of columns C, D and E into an intermediate
   XML, and
   [transforms it](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L521-L532)
   with `miqra_to_tei.xslt` into a validated TEI file. The index's front matter is the
   [README tab's text](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L535-L547).
   The output goes to
   [`opensiddur-projects/project/tanakh-miqra_al_pi_hamasorah-he`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L583-L612)
   by default, the project named by
   [`MIQRA_PROJECT`](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/common/versification.py#L43-L53).
3. **The TEI project to the books.** The humash's portion files name verses without naming an
   edition, as in
   [`haftarat_balak.xml`](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/project/chumash-opensiddur-he/haftarat_balak.xml#L39),
   so each book's settings choose the edition by a priority list:
   - [`settings/chumash-opensiddur-he/annual.yaml`](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/settings/chumash-opensiddur-he/annual.yaml#L20-L46)
     puts MAM first after the humash itself "since the aliyah and maftir divisions were taken
     from MAM", and uses MAM for instructions, annotations and the parallel text facing JPS 1917;
   - [`settings/haggadah_leleil_shimmurim-heidenheim-1822-he/with_translation.yaml`](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/settings/haggadah_leleil_shimmurim-heidenheim-1822-he/with_translation.yaml#L1-L19)
     puts MAM second, to fill biblical text the Haggadah lacks;
   - [`settings/siddur_expanded-opensiddur-he/undated.yaml`](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/settings/siddur_expanded-opensiddur-he/undated.yaml#L33-L49)
     puts MAM third in transclusion and lists it among the annotations.

   The other seven settings files (Birnbaum's siddur, both Metsudah volumes, both Selichoth
   variants and the two previews) and the settings README do not name MAM. The three files that
   do are byte-identical at the release's commit, `c91943d`, so the released books were built
   with these priorities. The
   [download list](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/DOWNLOADS.md#L3-L17)
   gives the three books' files in release
   [`v20261108`](https://github.com/opensiddur/opensiddur-projects/releases/tag/v20261108), whose
   tag is commit `c91943d`, the commit the processor's `main` pins as its opensiddur-projects
   submodule. The Expanded Ashkenazi Siddur is
   [electronic only](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/DOWNLOADS.md#L54-L58).
4. **The release to the hosted builder.** opensiddur-infra's
   [`releases.lock.json`](https://github.com/opensiddur/opensiddur-infra/blob/cbbf4d07668194aef0464d296539a5437bec6133/releases.lock.json#L1-L9)
   pins opensiddur-projects at `c91943d` (`v20261108`) and the processor at `723b083`
   (`v0.7.0`); its
   [README](https://github.com/opensiddur/opensiddur-infra/blob/cbbf4d07668194aef0464d296539a5437bec6133/README.md#L3-L5)
   describes builds whose source and translation priorities a user configures, so a user's book
   may draw on the MAM project too.

## Provenance of the directory

- **What it holds.** [`manifest.json`](https://github.com/opensiddur/sourcetexts/blob/2243ced3187e1364efefc088867784356400e547/sources/miqra_al_pi_hamasorah/manifest.json#L2-L5)
  and eleven TSV files under
  [`sheets/`](https://github.com/opensiddur/sourcetexts/tree/2243ced3187e1364efefc088867784356400e547/sources/miqra_al_pi_hamasorah/sheets),
  9,471,496 bytes in all: one per tab of MAM's Google Sheet, the six book tabs, the README,
  changes, templates, special and AutoEdits tabs. The manifest gives each tab's Hebrew or English
  name, row count and SHA-256 sum. The book tabs hold Wikisource wikitext in five columns, as the
  importer's
  [README](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/README.md#L49-L61)
  describes.
- **When and by whom.** The manifest says the sheet was downloaded at 2026-05-27T06:57:39Z. One
  commit, [`2243ced`](https://github.com/opensiddur/sourcetexts/commit/2243ced3187e1364efefc088867784356400e547)
  by Efraim Feinstein on 2026-06-16, "download of miqra al pi hamasorah", added all twelve
  files; it is the only commit on `master` that touches the directory (query:
  `gh api "repos/opensiddur/sourcetexts/commits?path=sources/miqra_al_pi_hamasorah&sha=master"`),
  so nothing in it has changed since.
- **Which MAM source and version.** The source is the Google Sheet with id
  `1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs`, the sheet MAM's own introduction links. MAM's
  introduction now calls it the frozen data sheet, whose changes page holds the corrections
  recorded up to 12 September 2026, and sends readers to Wikisource's page histories for later
  ones (MAM-basics' mirror, `in/mam-ws-intro/summary.mediawiki`, line 51); MAM-basics'
  `mam-wikisource-refresh` skill says the sheet "has been a frozen historical archive since
  September 12, 2026" (`dot-claude/skills/mam-wikisource-refresh/SKILL.md`, line 175). So Open
  Siddur's copy is the sheet as it stood on 2026-05-27, three and a half months before the
  freeze, and it holds no MAM change made after that day, whether in the sheet or on Wikisource.
  No file states a version number. The copied changes tab lists its entries newest first; its
  newest,
  [record 2](https://github.com/opensiddur/sourcetexts/blob/2243ced3187e1364efefc088867784356400e547/sources/miqra_al_pi_hamasorah/sheets/changes.tsv#L2-L7),
  reads `2026-03-05 00:00:00`, which in the tab's own day-month order is 3 May 2026, and the
  entries after it are dated 21 to 26 April 2026. That interpretation is an inference: 1,033 of
  the tab's 1,053 date cells came through the XLSX export as ISO dates whose day and month may be
  swapped, and two read 3 December 2026, after the download.
- **License and attribution.** The copied README tab states
  [CC BY-SA 4.0 International, with attribution to Hebrew Wikisource and a direct link](https://github.com/opensiddur/sourcetexts/blob/2243ced3187e1364efefc088867784356400e547/sources/miqra_al_pi_hamasorah/sheets/readme.tsv#L2-L6).
  The converter's
  [TEI header](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L178-L219)
  states the same license, names Avi Kadish as editor and Hebrew Wikisource as distributor, and
  notes that the text was "distributed via a public Google Sheet"; the published project's
  [index](https://github.com/opensiddur/opensiddur-projects/blob/cb8714eb89fb0bc1f0ebb81ef35ed1019addf658/project/tanakh-miqra_al_pi_hamasorah-he/index.xml#L12-L25)
  carries that header, with the README tab's text, attribution rules included, as front matter.
  The processor's
  [README](https://github.com/opensiddur/opensiddur-processor/blob/307d80df3299c7069d02371661b8ff5307017f78/README.md#L160-L164)
  says each project text keeps the license its TEI header declares.

## History, from commits, issues and pull requests

Times are UTC, as GitHub records them.

1. **2025-10-03:** opensiddur-processor
   [issue 4](https://github.com/opensiddur/opensiddur-processor/issues/4) asks for a converter
   for MAM.
2. **2026-05-27, 06:57:** the processor's downloader exports the Google Sheet (the manifest's
   time); **2026-05-29:** processor
   [pull request 28](https://github.com/opensiddur/opensiddur-processor/pull/28), "Miqra al pi
   hamasorah importer", is merged.
3. **2026-06-16, 00:53:58:** sourcetexts commit
   [`2243ced`](https://github.com/opensiddur/sourcetexts/commit/2243ced3187e1364efefc088867784356400e547)
   adds the directory, pushed directly, through no pull request. **00:55:24:** opensiddur-projects
   commit
   [`2360659`](https://github.com/opensiddur/opensiddur-projects/commit/23606592dd2ade1995f7bb7041bc3b4b53439602),
   "fix for WLC and JLPTEI miqra", adds the 44 converted files under the project's first name,
   `project/miqra_al_pi_hamasorah`, also pushed directly. Both are by Efraim Feinstein.
4. **2026-08-07 to 2026-08-20:** importer fixes, each followed by a regeneration in
   opensiddur-projects. The Ten Commandments had been dropped from Exodus 20 and Deuteronomy 5
   ([issue 45](https://github.com/opensiddur/opensiddur-processor/issues/45),
   [pull request 47](https://github.com/opensiddur/opensiddur-processor/pull/47)); notes had no
   anchor in the text
   ([issue 46](https://github.com/opensiddur/opensiddur-processor/issues/46),
   [pull request 56](https://github.com/opensiddur/opensiddur-processor/pull/56)); 28 of the 39
   book files had been empty stubs
   ([pull request 70](https://github.com/opensiddur/opensiddur-processor/pull/70),
   [projects pull request 7](https://github.com/opensiddur/opensiddur-projects/pull/7)). The same
   weeks gave the Tanakh projects one canonical verse division
   ([pull request 75](https://github.com/opensiddur/opensiddur-processor/pull/75)), set MAM
   facing JPS 1917 in parallel books
   ([pull request 74](https://github.com/opensiddur/opensiddur-processor/pull/74)), and added the
   humash
   ([pull request 78](https://github.com/opensiddur/opensiddur-processor/pull/78),
   [projects pull request 11](https://github.com/opensiddur/opensiddur-projects/pull/11));
   sourcetexts [pull request 3](https://github.com/opensiddur/sourcetexts/pull/3) added hebcal's
   data for the portions MAM does not mark.
5. **2026-08-18:** processor commit
   [`43f5b73`](https://github.com/opensiddur/opensiddur-processor/commit/43f5b73e23191149fe495f78367ced3fb5c41117),
   "Add submodules and a release procedure", from the processor's
   [pull request 80](https://github.com/opensiddur/opensiddur-processor/pull/80), adds the
   `sourcetexts` submodule. Its first pin,
   `2e59018`, is five commits
   [ahead of `2243ced`](https://github.com/opensiddur/sourcetexts/compare/2243ced3187e1364efefc088867784356400e547...2e59018fba559edc22affa47135d8f5c006e95c0),
   so it includes the directory; the commit before it has no `sourcetexts` path at all. The
   directory's tree is identical at all nine pins from then to `dacca4a` (2026-11-08), as the
   directory's single commit implies.
6. **2026-10-05:** projects
   [pull request 68](https://github.com/opensiddur/opensiddur-projects/pull/68) adds the settings
   files for the printed books, the humash's among them.
7. **2026-10-30:** projects commit
   [`1a4d1b0`](https://github.com/opensiddur/opensiddur-projects/commit/1a4d1b0bf814131b7916c2bfaefd1de98267d7e6)
   ([pull request 89](https://github.com/opensiddur/opensiddur-projects/pull/89), paired with
   processor [pull request 278](https://github.com/opensiddur/opensiddur-processor/pull/278))
   renames the project `tanakh-miqra_al_pi_hamasorah-he`. **2026-11-01:**
   [`510a4c5`](https://github.com/opensiddur/opensiddur-projects/commit/510a4c5753795a9295922c479aeb33196b65370b)
   ([pull request 91](https://github.com/opensiddur/opensiddur-projects/pull/91)) fixes its URNs,
   the last change to the project on `main`.
8. **2026-11-08:** release `v20261108` builds the books with processor `v0.7.0`.

**Open plan: processor
[issue 277](https://github.com/opensiddur/opensiddur-processor/issues/277)**, opened 2026-10-30
and not yet implemented, proposes a monthly job that reruns the MAM download, and, if the source
changed, commits it to sourcetexts, regenerates the project, rebuilds the humash and the expanded
siddur, and opens paired pull requests. It calls the projects "snapshots, refreshed only when
someone happens to rerun the importers", and calls MAM "a Google Sheets edition that is still
being corrected". **That premise is out of date, and nothing has been said to Open Siddur about
it:** MAM's introduction and MAM-basics both record the sheet as frozen since 2026-09-12, so a
job that downloads the sheet would bring in the corrections recorded between 2026-05-27 and the
freeze, and nothing after it; MAM's later corrections are on Wikisource. The issue also says the
downloader refetches only what changed, but `download.py` fetches the whole workbook on every run
and rewrites `downloaded_at`, so even an unchanged sheet would change the manifest. The issue
was still open, with no comments, at 04:57 on 2026-11-23, New York time.

No issue or pull request states MAM's license; the license appears only in the files cited
above.

## Repositories examined and found not to use the directory

| Repository | Fork of | Default branch | Last push | Why no use |
|---|---|---|---|---|
| sourcetexts | | master | 2026-11-22 | Stores the directory; its tree has no script or workflow at all. |
| opensiddur-infra | | main | 2026-11-17 | All 134 files read: none names MAM; it builds from pinned releases. |
| opensiddur-compiler | | develop | 2026-02-13 | Last push predates the directory. |
| opensiddur | | develop | 2025-12-19 | Last push predates the directory; its one "masorah" hit is the 1917 JPS preface. |
| docker-tei-stylesheets | joeytakeda/docker-tei-stylesheets | main | 2025-06-23 | Last push predates the directory. |
| app-reverse-proxy | | master | 2023-05-10 | Last push predates the directory. |
| hebmorph-exist | | master | 2022-09-21 | Last push predates the directory. |
| exist | eXist-db/exist | develop | 2021-12-20 | Last push predates the directory. |
| opensiddur-app | | develop | 2019-04-18 | Last push predates the directory. |
| opensiddur-client | | develop | 2019-02-17 | Last push predates the directory. |
| imports | | master | 2019-02-03 | Last push predates the directory. |
| fonts | | master | 2018-10-05 | Last push predates the directory. |
| input-conversion | | master | 2017-10-24 | Last push predates the directory. |
| Roma | TEIC/Roma-Antiqua | master | 2016-04-15 | Last push predates the directory. |
| Stylesheets | TEIC/Stylesheets | master | 2016-04-15 | Last push predates the directory. |
| HebMorph | EfraimFeinstein/HebMorph | master | 2013-03-24 | Last push predates the directory. |

"Last push" is GitHub's `pushedAt` for the repository, any branch, from
`gh repo list opensiddur --limit 500` on 2026-11-22 (18 repositories, forks and archived ones
included; none is archived). A repository last pushed before 2026-06-16, when the directory was
committed, cannot pin a sourcetexts commit that contains it, and code search found no MAM name
in any of these that it indexes (it skips most forks). Only opensiddur-processor has a
`.gitmodules` naming sourcetexts
(`gh search code sourcetexts --owner opensiddur --filename .gitmodules`), and only processor
files name `opensiddur/sourcetexts`.

## Searches, and what they could not cover

- **Code search** (`gh search code <term> --owner opensiddur`) for `miqra_al_pi_hamasorah`,
  `hamasorah`, `masorah`, `miqra`, the sheet's id, `sifrei_emet`, `ketuvim_aharonim`,
  `chamisha_megillot`, `neviim_rishonim`, `auto_edits`, `torah.tsv`, the Hebrew words for
  "Miqra" and "the Masorah", `wikisource` and `dicta` found MAM-related files only in
  opensiddur-processor and in the directory itself. Code search covers default branches only,
  skips files over 384 KB (so the large TSVs themselves are not searched), skips most forks, and
  cannot see private repositories, if the organization has any.
- **Code search does not index opensiddur-projects or opensiddur-infra at all**: searches for
  words certainly in them (`Heidenheim`, `Terraform`) return nothing. All 134 files of
  opensiddur-infra were read through the API instead. Of opensiddur-projects, all eleven files
  under `settings/`, `DOWNLOADS.md`, the MAM project's index and one humash file were read and
  its tree listed, and for items 2 to 6 the four projects and the settings that those sections
  name were downloaded through the API at `c91943d`. Its other files, 22,859 in all at
  `cb8714e`, were not searched for a file that names the MAM project directly: that needed a
  clone, and Ben chose on 2026-11-23 not to make one.
- **Issue and pull-request search** (`gh search issues|prs <term> --owner opensiddur`) for
  `miqra`, `masorah`, `hamasorah`, `MAM`, `tanakh` and `wikisource` found MAM matters only in
  opensiddur-processor, opensiddur-projects and sourcetexts; the history section summarizes them.

## MAM-basics' own mentions of Open Siddur

1. Line 61 of `in/mam-ws-intro/summary.mediawiki` links the opensiddur.org article as one of the
   two English announcements, in Elul 5773, that MAM's full draft was complete;
   `doc/intro-doc-audit/claims.json` quotes the line. It is an announcement of 2013, not a
   reference to the sourcetexts copy.
2. `py/taamey_d/doc/tad_corpus.py`, lines 128 to 132, builds the URL of an opensiddur.org page
   with Ben Sira's chapters 44 to 50, for Taamey D's corpus, not for MAM.

## How much of MAM the three books print (item 2)

**Two of the three books print MAM's text; the Haggadah prints none of it.** The Humash prints
the whole Torah from MAM, and its haftarah portions, the five megillot and its festival and
special portions too. The Siddur prints from MAM its Torah, maftir and haftarah portions, Hallel,
most of its psalms, Esther and the Song of Songs. The Haggadah's biblical passages are all its
own words.

**How a book's passages are chosen.** The exporter takes each transcluded passage from the first
project in the book's `priority.transclusion` list that carries both of the passage's ends in one
file, matching URNs exactly
([urn.py `resolve_range` and `prioritize_range`, L243-L362](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/urn.py#L243-L362)).
A project whose element only points elsewhere still wins, and its pointers are resolved in turn
with the same list. MAM's notes are anchored in its text, so one prints exactly where MAM
supplies the passage around its anchor and the book lists MAM among its `annotations`
([compiler.py `_annotate`, L596-L646 at v0.7.0](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/exporter/compiler.py#L596-L646)).
The figures below apply that rule, read in the code of `v0.7.0`, which built the release, and
unchanged in what it selects at `474cb10`, to the projects at the release commit `c91943d`.
No book was built.

### The Humash (annual cycle)

**Yes, it has haftarah portions, and more besides the Torah: the five megillot and the festival
and special portions too, every passage from MAM.** The humash project carries no verse of its
own, so all 1,741 of the book's verse ranges resolve to MAM, the next project in its list, and
JPS 1917 carries both ends of every one of them, so it faces MAM verse by verse throughout. The
book is compiled twice, as a PDF and as an electronic book, and the two reach different
conditional passages.

1. **The Torah.** All 5,853 verses of Genesis to Deuteronomy, in WLC's numbering, print once
   each in the parashot, in both compiles.
2. **Haftarah portions.** The PDF prints the annual haftarah portion of each of the 55 haftarah
   divisions: one portion for all rites in 39 of them, and in the other 16 both the Ashkenazi
   portion and the Sephardi one, since the settings declare the Ashkenazi rite but leave the
   Sephardi rite undecided, which prints its portion with its condition marked. The electronic
   book also holds the triennial haftarah portions of years 1 to 3, in 150 divisions.
3. **The megillot and the festival and special portions.** Both compiles print the five megillot
   whole, and the Torah and haftarah portions of 79 festival and special divisions; three more
   such divisions hold only a heading.
4. **A defect in the humash's divisions, not in MAM.** Four festival Torah portions each hold one
   range that bridges two passages of Numbers, so each also prints the 617 to 689 verses between
   them. The sixth day of Hanukkah, whose customary Torah portion is Numbers 28:1-15 and 7:42-47,
   transcludes Numbers 7:42-47, then 7:48-27:23, then 28:1-15 in three ranges
   ([reading_chanukah_day_6.xml L31-L38](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/chumash-opensiddur-he/reading_chanukah_day_6.xml#L31-L38)).
   The seventh day of Hanukkah on Rosh Hodesh (Numbers 7:54-27:23), Shabbat Rosh Hodesh during
   Hanukkah (Numbers 7:48-28:8) and the fourth day of Hol HaMoed Pesah (Numbers 9:15-28:18) are
   alike. Together the four bridges add 2,662 verse occurrences and 548 note occurrences to
   both compiles.
5. **MAM's notes.** All 1,492 of MAM's notes on the Torah and all 259 on the megillot print. Of
   the 821 in the 21 prophetic books that the book draws on, the PDF prints 152 and the
   electronic book 241, so 1,903 and 1,992 notes in all, in 3,044 and 3,219 occurrences. A note
   is left out only where its verse is.

Verses of MAM by book, distinct and in all their occurrences (a verse printed in two portions
counts twice). The figures include the four bridges; without them the occurrences would total
11,893 in the PDF and 13,709 in the electronic book.

| Book | MAM's verses | PDF, distinct | PDF, occurrences | Electronic, distinct | Electronic, occurrences |
|---|---:|---:|---:|---:|---:|
| Genesis | 1,533 | 1,533 | 1,693 | 1,533 | 1,693 |
| Exodus | 1,213 | 1,213 | 1,833 | 1,213 | 1,833 |
| Leviticus | 859 | 859 | 1,235 | 859 | 1,235 |
| Numbers | 1,289 | 1,289 | 4,601 | 1,289 | 4,601 |
| Deuteronomy | 959 | 959 | 1,346 | 959 | 1,346 |
| Joshua | 656 | 61 | 157 | 177 | 293 |
| Judges | 618 | 109 | 140 | 156 | 270 |
| 1 Samuel | 811 | 121 | 192 | 187 | 281 |
| 2 Samuel | 695 | 91 | 212 | 124 | 312 |
| 1 Kings | 817 | 199 | 274 | 260 | 480 |
| 2 Kings | 719 | 112 | 190 | 190 | 325 |
| Isaiah | 1,291 | 385 | 560 | 486 | 946 |
| Jeremiah | 1,364 | 192 | 316 | 272 | 524 |
| Ezekiel | 1,273 | 226 | 404 | 269 | 550 |
| Hosea | 197 | 67 | 103 | 91 | 153 |
| Joel | 73 | 13 | 26 | 22 | 35 |
| Amos | 146 | 28 | 46 | 49 | 91 |
| Obadiah | 21 | 21 | 21 | 21 | 31 |
| Jonah | 48 | 48 | 96 | 48 | 96 |
| Micah | 105 | 20 | 32 | 25 | 48 |
| Nahum | 47 | 0 | 0 | 10 | 10 |
| Habakkuk | 56 | 20 | 78 | 20 | 78 |
| Zephaniah | 53 | 0 | 0 | 12 | 12 |
| Haggai | 38 | 0 | 0 | 21 | 21 |
| Zechariah | 211 | 42 | 210 | 92 | 276 |
| Malachi | 55 | 42 | 43 | 53 | 84 |
| Song of Songs | 117 | 117 | 117 | 117 | 117 |
| Ruth | 85 | 85 | 85 | 85 | 85 |
| Lamentations | 154 | 154 | 155 | 154 | 155 |
| Ecclesiastes | 222 | 222 | 223 | 222 | 223 |
| Esther | 167 | 167 | 167 | 167 | 167 |
| **Total** | 15,892 | 8,395 | 14,555 | 9,183 | 16,371 |

No verse prints from Psalms, Proverbs, Job, Daniel, Ezra, Nehemiah or Chronicles. The 8,395
distinct verses are 36% of the 23,211 verses of MAM's TEI, and the 9,183 are 40%.

### The Heidenheim Haggadah with English translation

**MAM supplies none of its text and none of its notes, although its settings name MAM as the
fallback for biblical text.** Its `priority.transclusion` list is the Haggadah's own project,
then MAM, and the settings' comment says MAM fills "any biblical text missing from the Haggadah
itself"
([with_translation.yaml](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/settings/haggadah_leleil_shimmurim-heidenheim-1822-he/with_translation.yaml#L1-L30)).
But all 102 of the project's transclusions, in every conditional branch, target `haggadah:` or
`prayer:` URNs that the Haggadah's own project carries; none targets a Bible verse, and MAM
carries only Bible URNs, so none reaches MAM. MAM is not among the book's `annotations`, which
list only Feinstein's English, so none of MAM's notes can print either.

The Haggadah's biblical passages are therefore all its own words:

1. **Eight whole psalms, marked with Bible verse milestones, 117 verses:** Psalms 113 and 114 at
   the end of Maggid, Psalm 126 at the start of Barekh, and Psalms 115, 116, 117, 118 and 136 in
   Hallel. Their letters are MAM's, but for one plene spelling in Psalms 116:6, and they carry
   no accents.
2. **Quotations written into its paragraphs, with no Bible markup:** 106 of them, covering 69
   verses in 45 chapters, found by matching the Haggadah's text against MAM's. Among them are
   Genesis 1:31-2:3 in Qaddesh, for Shabbat; in Maggid, Joshua 24:2-4, Genesis 15:13-14,
   Deuteronomy 26:5-8 with the lemmas of its midrash, and verses of Exodus 1, 2, 12 and 13; in
   Barekh, Deuteronomy 8:10 and verses of Psalms; and verses of Psalms in Nishmat. The
   project's header says that the quotations in Maggid were taken from WLC, and that the psalms
   were transcribed from the 1822 print, all but Psalm 126, which came from the Open Siddur
   compilation
   ([index.xml L52](https://github.com/opensiddur/opensiddur-projects/blob/c91943dc9ec9b039447bbed358e982cc529ae621/project/haggadah_leleil_shimmurim-heidenheim-1822-he/index.xml#L52));
   neither claim was checked.

### The Expanded Ashkenazi Siddur

**MAM supplies its Torah, maftir and haftarah portions, Hallel, most of its psalms, and Esther
and the Song of Songs; Birnbaum's Hebrew prayer book supplies the Shema, Ashrei and the rest of
its biblical words.** The siddur project prints no Bible words of its own, and the humash
contributes only its haftarah divisions, which hold MAM's ranges, so every Bible transclusion the
book reaches falls to MAM, the next project in its list. None falls further, to WLC or to
Birnbaum, and none fails to resolve. The book is built only as an electronic book, which leaves
its reader to choose the day, the rite and the cycle, and so holds every variant.

1. **What MAM supplies: 9,387 distinct verses from 29 books**, in 5,186 range occurrences:
   - every verse of the Torah, in the morning Torah portions, which cover the annual and
     combined parashot, the triennial years, the festivals, Hol HaMoed, Rosh Hodesh, Hanukkah,
     Purim, the fasts and the special Sabbaths, besides the Shabbat afternoon portions;
   - the maftir portions and every haftarah portion, 259 distinct haftarah spans in 21 books,
     which reach MAM through 104 of the humash's divisions, each printing its annual, Ashkenazi,
     Sephardi and triennial portions;
   - Hallel, Psalms 113 to 118 but for 118:25; the psalms of Kabbalat Shabbat; those of Pesukei
     de-Zimra other than Psalms 30, 145 and 150; the psalms of the day from Monday to Shabbat;
     the winter Shabbat afternoon's Psalms 104 and 120 to 134; Psalms 20, 27, 49 and 137, among
     others: 663 verses of Psalms in all;
   - Esther and the Song of Songs whole, and single verses such as Deuteronomy 4:4 and 32:3 and
     Numbers 6:24-26.
2. **Birnbaum's own Hebrew, printed in place.** The siddur's prayers come from Birnbaum's Hebrew
   project, which prints its own words for the Shema, Ashrei (Psalm 145), Hodu, the Song at the
   Sea, Psalm 150, Genesis 22:1-19, Exodus 13:1-16 and the sacrificial passages of the morning
   preliminaries, among others: 571 distinct verses that it marks as Bible, and at least 137
   more that it prints with no Bible mark, found by matching letters with MAM. The eleven Bible
   transclusions inside Birnbaum's prayers that the book reaches, nineteen times, all fall to
   MAM, which stands ahead of Birnbaum in the list: the psalms of the day, Exodus 31:16-17,
   Leviticus 23:44 and Genesis 2:1-3.
3. **MAM's notes.** 2,035 distinct notes print, 9,743 times: all 1,492 of MAM's notes on the
   Torah, and 543 of the 2,430 in its other books.
4. **Facing text.** JPS 1917 faces 5,167 of the 5,186 MAM ranges, verse for verse; the 19 inside
   Birnbaum's prayers face Birnbaum's English.

Verses of MAM by book, distinct and in all their occurrences:

| Book | MAM's verses | Distinct | Occurrences |
|---|---:|---:|---:|
| Genesis | 1,533 | 1,533 | 4,728 |
| Exodus | 1,213 | 1,213 | 6,421 |
| Leviticus | 859 | 859 | 6,078 |
| Numbers | 1,289 | 1,289 | 7,654 |
| Deuteronomy | 959 | 959 | 4,164 |
| Joshua | 656 | 177 | 1,009 |
| Judges | 618 | 156 | 1,629 |
| 1 Samuel | 811 | 187 | 620 |
| 2 Samuel | 695 | 125 | 945 |
| 1 Kings | 817 | 260 | 3,217 |
| 2 Kings | 719 | 190 | 1,596 |
| Isaiah | 1,291 | 487 | 3,486 |
| Jeremiah | 1,364 | 272 | 3,290 |
| Ezekiel | 1,273 | 269 | 1,770 |
| Hosea | 197 | 91 | 525 |
| Joel | 73 | 22 | 49 |
| Amos | 146 | 49 | 373 |
| Obadiah | 21 | 21 | 124 |
| Jonah | 48 | 48 | 48 |
| Micah | 105 | 25 | 570 |
| Nahum | 47 | 10 | 40 |
| Habakkuk | 56 | 20 | 78 |
| Zephaniah | 53 | 12 | 48 |
| Haggai | 38 | 21 | 84 |
| Zechariah | 211 | 92 | 538 |
| Malachi | 55 | 53 | 374 |
| Psalms | 2,527 | 663 | 1,162 |
| Song of Songs | 117 | 117 | 117 |
| Esther | 167 | 167 | 668 |
| **Total** | 17,958 | 9,387 | 51,405 |

### Which of item 6's defects reach the books

The Haggadah prints nothing of MAM's, so none of them. The Humash and the Siddur print these
verses from item 6's lists:

| Defect | Humash, PDF | Humash, electronic | Siddur |
|---|---|---|---|
| Qere-only word replaced by a URL | Ruth 3:5, 3:17 | Ruth 3:5, 3:17 | none |
| Ketiv-only word in tripled parentheses | Ruth 3:12; 2 Kings 5:18, in Tazria's haftarah portion | the same | 2 Kings 5:18 |
| Geresh or gershayim with telisha gedola written as a space | Genesis 5:29, Leviticus 10:4 | the same | the same |
| ירושלמה with ḥiriq | none | 1 Kings 10:2 | 1 Kings 10:2 |
| Atoms fused where a note marks a lone space | Deuteronomy 23:8 | the same | the same |
| Good ending dropped after a book's last verse | Isaiah 66:24, Malachi 3:24, Lamentations 5:22, Ecclesiastes 12:14 | the same | Isaiah 66:24, Malachi 3:24 |

None of the emptied verses of Job, the inverted nuns of Psalm 107 or the other fused atoms falls
in a passage that these books take from MAM.

## How the sheet's wikitext is parsed (item 3)

**The parser is mwparserfromhell**, version 0.7.2, the only wikitext library that the
processor's
[`pyproject.toml`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/pyproject.toml#L30-L44)
asks for and its
[`uv.lock`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/uv.lock#L429-L431)
pins; there is no wikitextparser. The converter's `miqra_wikitext.py`
[calls `mwparserfromhell.parse`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L311-L315)
inside the processor's own subclass of a `MediaWikiProcessor` framework that, its
[docstring](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/util/mediawiki_processor.py#L1-L7)
says, was "originally built for the JPS1917 importer"; the subclass
[empties the framework's handler tables](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L191-L197),
so none of the JPS template handling applies. Regular expressions do the rest: before the parse,
MAM's section tags become intermediate elements and, in column C only, the sheet's space code
`__` becomes a space and `//` a line break
([L167-L181](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L167-L181));
after it, `''`, `'''` and `'''''` become highlighting
([L102-L117](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L102-L117)).

1. **What it reads.** The six book tabs' columns C (navigation and layout), D (each verse's
   `{{מ:פסוק}}` scaffold) and E (the verse), and the README tab for the index's front matter. It
   skips every row whose id is `0` or `תתת`
   ([convert_tsv.py L415-L428](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L415-L428)):
   1,858 rows of page furniture, song-format transclusions and the four good endings. All 23,202
   verse rows are read.
2. **What it handles.** Templates are looked up by normalized name in a table, with two
   name-prefix rules: any name beginning כו"ק is read as a ketiv-first pair, and any beginning
   קו"כ as a qere-first pair
   ([L301-L309](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L301-L309)).
   Parameters are read by name or position, each value stripped of surrounding whitespace
   ([L372-L385](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L372-L385)),
   and nesting is followed to a depth of 12. The only tag with a handler is `noinclude`, which
   is deleted. Wikilinks and MAM's link templates become links to Hebrew Wikisource. Comments
   and entities would pass through as text; none occurs in the book tabs. A note's leading `=`
   is parsed as a heading and rebuilt as text.
3. **What it does with what it does not recognize.** It never raises. A template with no
   handler is parsed again from its own text until the depth limit, and so is kept as literal
   wikitext, braces included; an exception in a handler is caught and the handler is run again
   on the unprocessed template
   ([L318-L335](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L318-L335));
   an exception for a whole cell makes the cell's raw wikitext its output, and the errors
   collected are discarded
   ([L199-L224](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L199-L224),
   [L675-L683](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L675-L683)).
   In the snapshot's verse rows every template name has a handler except מ:עלייה, all 532 of
   which sit inside `{{מ:פסוק}}`, which is stripped whole, and the TEI holds no `{{`.
4. **What it hands on.** An intermediate XML, one `miqra:row` per verse row holding the three
   columns, with an inline element for each recognized template
   ([convert_tsv.py L492-L504](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L492-L504)).
   `canonical_verses.py` renumbers and splits rows (item 6);
   [`miqra_to_tei.xslt`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L52-L89),
   run with Saxon, makes TEI paragraphs, milestones and inline markup and gathers the notes
   into a `tei:standOff`; lxml then pretty-prints the result, sub-verse milestones are spliced
   in and the file is validated
   ([convert_tsv.py L243-L262](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/convert_tsv.py#L243-L262)).
5. **The humash's own read of column D.**
   [`aliyot.read_markers`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/humash/aliyot.py#L151-L196)
   uses no wikitext parser. Regular expressions find each `{{מ:עלייה|…}}` with no nested braces
   and read book, chapter and verse from the first three parameters of `{{מ:פסוק|…}}`; the
   parameters are split on `|`, and only the named ones are kept. It finds all 532 markers of
   the Torah tab.

## Whether MAM's templates are navigated well (item 4)

**Partly.** The converter names every template that occurs in the snapshot's verse rows, and it
handles the common ones as MAM-basics expects a consumer to. But its walk departs from closed
dispatch in five ways, and those departures are where the defects of item 6 come from. The
expectations are Ben's rule that template dispatch is closed (his user-level instructions,
"Template dispatch is closed"), MAM-simple's consumer notice
(`gh-pages/MAM-simple/reading-mam-simple.html#consumer-notice`) and MAM-parsed's consumer
cautions (`MAM-parsed/README.md`); the inventory of MAM's templates is
`py/mb_cmn/template_names.py`.

**What it does as expected.**

1. It dispatches on an explicit table of about eighty names, with a separate list of the
   templates it strips
   ([L24-L55, L232-L299](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L232-L299)).
2. It keeps ketiv and qere, and the two strands of a dual-cantillation passage, as TEI
   alternatives, and where MAM-simple keeps one branch, of the qamats template or a
   stress-helper template, it keeps the same one (item 5).
3. It keeps scroll-difference notes and documentation notes out of the running text, each
   anchored in it.
4. The whitespace and break templates at the top level of a verse (מ:ששש, ססס, סס, פפ, פפפ and
   ר0 to ר3) become paragraph or line breaks and never fuse atoms, and narpas keeps MAM's
   spacing, with no space on either side.
5. It leaves MAM's mark order alone.

**Where it departs from closed dispatch.**

1. **Meaning from a name's prefix.** מ:כו"ק מיוחד has no entry; it is read by the כו"ק prefix
   rule as an ordinary ketiv-first pair, and its סוג parameter, which sets the order of its two
   sides, is ignored.
2. **No raising.** An unknown template is kept as literal wikitext, and every exception is
   swallowed and its error discarded. None reached the TEI from this snapshot, but a template
   new to the sheet would pass silently: MAM-basics' inventory names מ:אות-מיוחדת-במילה,
   מ:סילוק לפני געיה and מ:הערה-2, which do not occur in this snapshot and which the converter
   does not name.
3. **Generic recursion.** Every parameter of a recognized template is processed before its
   handler runs, including parameters the handler then discards, and the handler parses its
   already converted parameters again
   ([`_process_template_with_nesting`](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/util/mediawiki_processor.py#L212-L225)).
   That second parse is how six qere-only words nested in notes became URLs: the doubled
   brackets the first pass made were read as a wikilink (Ruth 3:5).
4. **Meaning from shape.** Any numeric parameter from 2 up is taken for a note; a break is
   mid-verse if any parameter contains פסקא באמצע פסוק
   ([L393-L407](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L393-L407));
   fallback chains choose among parameters, as for the qamats template (ד=, else ס=, else
   parameter 1), and מ:כל קמץ קטן מרכא falls back to a fixed form.
5. **No shape validation.** No handler checks the parameters it is given. The centered-title
   handler reads positional parameter 1 where MAM writes `כותרת=`, which empties 25 verses of
   Job (Job 3:2); the ketiv-only and qere-only handlers wrap a parameter that already carries
   MAM's own parentheses or brackets (2 Samuel 13:33, Judges 20:13).

The processor's own tests could not catch the last two: they feed the handlers invented shapes,
`{{כתיב ולא קרי|כתיב}}` and `{{קרי ולא כתיב|קְרִי}}` without MAM's parentheses and brackets and
`{{פרשה-מרכז|כותרת}}` with a positional title, and assert the fixed form for
מ:כל קמץ קטן מרכא
([test_miqra_wikitext.py L194-L198, L239-L241, L300-L301](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/tests/importer/miqra_al_pi_hamasorah/test_miqra_wikitext.py#L194-L198)).

**Against MAM-basics' consumer cautions.**

1. **Alternatives concatenated.** Not in the TEI's markup, where each pair is a `tei:choice`.
   But the two sides of all 1,047 ketiv and qere choices, and of 21 of the 27 strand pairs,
   stand adjacent with no whitespace between them, so a consumer that strips tags fuses them:
   Genesis 8:17's ketiv הוצא and qere הַיְצֵ֣א become הוצאהַיְצֵ֣א. The books print both sides of
   each pair, the second in parentheses (item 5): a display of both, set apart, not a silent
   concatenation, except that the electronic book sets 921 of the ketiv-qere pairs with no space
   between the ketiv's closing parenthesis and the qere.
2. **A scroll-difference target run into its note.** Never: all 31 such notes stay out of the
   running text.
3. **A good-ending repetition run into the text.** Never, because all four are dropped.
4. **Whitespace templates dropped, fusing atoms.** At the top level of a verse, never. But 16
   parashah templates nested in a note are dropped where MAM has no space beside them, five
   notes on a lone space lose the space, and the seven inverted nuns of Psalm 107 are joined to
   the next atom (item 6); and between verses the TEI has no whitespace at all, only a
   milestone, at 18,896 verse boundaries.
5. **Narpas and its spacing.** The spacing is kept, but narpas and legarmeh become the same
   character, HEBREW PUNCTUATION PASEQ, with no markup to tell them apart; only the space after
   legarmeh is left to do it.
6. **The gray maqaf.** Kept as a maqaf, but its gray kind is lost.

So the converter walks MAM's templates in one of the expected ways for the templates that make
up nearly all of MAM's text, but not robustly: it neither raises on what it does not know nor
checks the shapes it assumes, and it parses its own output again. Every word-level defect of
item 6 is in a template that is rare in MAM, and they touch 88 verses.

## Which alternative the converter keeps (item 5)

**Where MAM offers ketiv and qere, or two strands, the converter keeps both, as TEI
alternatives; where MAM offers a vowel or stress-helper alternative, it keeps one, the same one
that MAM-simple keeps.** It differs from MAM-simple in dropping the combined text of a
dual-cantillation passage, ignoring the special ketiv-qere template's type, keeping MAM's
documentation notes and its varika marks, and dropping the good endings. MAM-simple's choices
are `_RENOPTS_MAM_XML` in `py/mb_xml/xml_render.py`: all three texts of a dual-cantillation
passage, the ד= branch of the qamats template, the chanted word without its stress helper, no
varika and no documentation notes. The counts are of the snapshot's verse rows.

| Template | Occurrences | The converter's TEI | MAM-simple | Example |
|---|---|---|---|---|
| כו"ק | 884 | both, as a `tei:choice` of `j:written`, then `j:read` | both, ketiv then qere | Genesis 8:17 |
| קו"כ | 126 | both, qere first | both, qere first | Genesis 36:5 |
| מ:כו"ק מיוחד | 37 | both, always ketiv first; its סוג parameter ignored | both, in the order and with the separator that סוג sets | 2 Kings 18:27 |
| מ:קו"כ-אם-2 | 148 | parameter 1, the pointed ketiv; parameters 2 and 3 dropped | parameter 1 | Genesis 49:10 |
| כתיב ולא קרי | 8 | parameter 1, with two more pairs of parentheses round MAM's own (item 6) | parameter 2, bare | 2 Samuel 13:33 |
| קרי ולא כתיב | 9 | parameter 1, with two more pairs of brackets round MAM's own; in six, a URL instead (item 6) | parameter 2, bare | Judges 20:13 |
| מ:כפול | 34 | strands א and ב as two `j:option` elements, under the conditions `taam-tachton` (א) and `taam-elyon` (ב), in 27; the 7 whose strands differ only by a parashah break become one break; the combined text dropped | all three texts; the consumer chooses | Exodus 20:2 |
| מ:קמץ | 375 | ד= where present (370 of the 372 in running text), else ס=, else parameter 1 | ד= | Genesis 9:21 |
| מ:דחי | 2,316 | parameter 1, the chanted word without its stress helper | parameter 1 | Psalms 1:1 |
| מ:צינור | 56 | parameter 1 | parameter 1 | Psalms 13:6 |
| מ:הערה, scroll difference | 31 | the note alone, in `tei:standOff`, anchored where the template stands | target and note kept together | Deuteronomy 11:21 |
| מ:סיום בטוב, good ending | 4 | dropped, with its note | kept apart from the running text | Isaiah 66 |
| נוסח, documentation note | 3,922 notes | the target in the text, the note in `tei:standOff` | the target alone | Genesis 1:3 |

1. **Strand names.** Genesis 35:22's strands, which MAM's templates tab names פשוטה and
   מדרשית, go under the same `taam-tachton` and `taam-elyon` conditions as the Decalogues'
   תחתון and עליון
   ([miqra_to_tei.xslt L396-L411](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L396-L411)).
2. **The Decalogues.** The converter splits MAM's verses onto WLC's numbering where strand ב
   ends a verse, so each canonical verse of Exodus 20:2-17 and Deuteronomy 5:6-21 has its own
   choice of the two strands; MAM's own verse number survives in an `edition-verse` milestone
   (item 6).
3. **Varika.** The TEI keeps all 669 varika marks, which MAM-simple drops.
4. **In the books.** The exporter compiles both sides of every pair, at `v0.7.0` and at `474cb10`
   alike: since `474cb10` it can select a strand, but none of the three books' settings
   declares the condition that would
   ([compiler.py L1209-L1233](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/compiler.py#L1209-L1233)).
   The PDF prints the qere, in italic, and then the ketiv in parentheses, whatever the TEI's
   order
   ([reledmac.xslt L3727-L3801, v0.7.0](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/exporter/tex/reledmac.xslt#L3727-L3801)).
   The electronic book keeps the TEI's order, with the ketiv in parentheses
   ([html.xslt L404-L467, v0.7.0](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/exporter/html/html.xslt#L404-L467);
   [reader.css L95-L96](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/exporter/html/assets/reader.css#L95-L96)),
   so in the 921 ketiv-first choices it shows the ketiv's closing parenthesis directly before
   the qere, with no space. Both outputs print strand א and then strand ב in parentheses, as at
   Exodus 20:13, לֹ֥א תִרְצָ֖ח (לֹ֖א תִּרְצָֽח׃)
   ([reledmac.xslt L3754-L3772, v0.7.0](https://github.com/opensiddur/opensiddur-processor/blob/723b083c9e1f548e3c78a3b375704650093040e6/opensiddur/exporter/tex/reledmac.xslt#L3754-L3772)).
   The ketiv-only and qere-only words, with their tripled parentheses or brackets or their URLs,
   print as they stand, and MAM's own verse numbers, the `edition-verse` milestones, never
   print. All of this is read from the exporter's code: no book was built or opened.

## What the converter changes in MAM's strings (item 6)

**The converter applies no Unicode normalization, so MAM's mark order survives, and most of
MAM's text reaches the TEI unchanged: 263,648 of 263,826 tokens. But 88 verses differ in their
words, mostly by loss, and in other places atoms are fused or distinctions dropped.** Each
change below was found in the code and confirmed on the data, by comparing the TEI at `c91943d`
with the snapshot it was made from, so that none of it is a correction MAM made after
2026-05-27. Every finding is unfixed: the code and the data are Open Siddur's, and nothing has
been said to them.

1. **No normalization.** No normalization call lies on the conversion path, and the output
   declares no normalization form; the one call in the code, an NFD in `subverse.py`, serves
   matching and writes nothing
   ([subverse.py L157-L164](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/common/subverse.py#L157-L164)).
   Every letter cluster in the TEI's running text is in MAM-normal order, as
   `py/mb_cmn/uni_denorm.py` defines it, and 167,449 of them are clusters that NFC would
   reorder; 9,035 verse rows with no template are identical to their TEI text.
2. **Text lost.**
   1. **Centered titles.** All 26 instances of the template פרשה-מרכז become an empty
      `<tei:hi rend="centered"/>`, because the handler reads a positional parameter and MAM
      names it `כותרת=`
      ([miqra_wikitext.py L519-L521](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L519-L521)).
      So 25 verses of Job whose whole text is the title, Job 3:2 (וַיַּ֥עַן אִיּ֗וֹב וַיֹּאמַֽר׃) among
      them, are empty, and Proverbs 10:1 loses its title.
   2. **Good endings.** The four good endings, after the last verse of Isaiah, Malachi,
      Lamentations and Ecclesiastes, are dropped with their notes.
   3. **Qere-only words in notes.** Six qere-only words nested in a documentation note are
      replaced by the URL of a Hebrew Wikisource page named after the word (2 Samuel 16:23,
      18:20, Jeremiah 31:37 in MAM's numbering, Jeremiah 50:29, Ruth 3:5, 3:17); Ruth 3:5's
      qere אֵלַ֖י is gone from the text.
3. **Characters changed.**
   1. **Ketiv-only and qere-only words.** The converter wraps MAM's parameter, which already
      carries parentheses or brackets, in another pair, and the stylesheet in a third
      ([miqra_wikitext.py L478-L484](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L478-L484),
      [miqra_to_tei.xslt L320-L334](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L320-L334)):
      all eight ketiv-only words and the three qere-only words not nested in a note, as in
      2 Samuel 13:33, `כִּֽי־(((אם)־))אַמְנ֥וֹן`.
   2. **The inverted nuns of Psalm 107.** MAM writes each `{{מ:נו"ן הפוכה|׆__}}`, with the
      sheet's space code, which the converter replaces only in column C; so all seven come out
      as the nun, two LOW LINE characters and the next atom, as in Psalms 107:23, ׆__יוֹרְדֵ֣י.
   3. **Geresh or gershayim with telisha gedola.** The templates מ:גרש ותלישא גדולה and
      מ:גרשיים ותלישא גדולה become one SPACE
      ([miqra_to_tei.xslt L368-L370](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L368-L370)),
      which splits the atom and loses both accents, seven times in running text (Genesis 5:29,
      Leviticus 10:4 twice, Zephaniah 2:15, 2 Kings 17:13, Ezekiel 48:10 twice) and three times
      in notes: MAM's זֶ֞֠ה at Genesis 5:29 becomes זֶ ה.
   4. **מ:ירושלמה.** The stylesheet treats it like מ:ירושלם and gives the implicit yod HEBREW
      POINT HIRIQ, where MAM gives HEBREW POINT SHEVA
      ([miqra_to_tei.xslt L362-L366](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_to_tei.xslt#L362-L366)):
      all four instances (1 Kings 10:2, 2 Kings 9:28, Isaiah 36:2, Ezekiel 8:3). The 636
      instances of מ:ירושלם are right.
   5. **מ:כל קמץ קטן מרכא.** The template has no parameter, so the handler's fixed fallback,
      with plain qamats and no merkha, replaces MAM's qamats qatan and merkha
      ([miqra_wikitext.py L592-L593](https://github.com/opensiddur/opensiddur-processor/blob/474cb10ebb49261d672c693550003c0f45960463/opensiddur/importer/miqra_al_pi_hamasorah/miqra_wikitext.py#L592-L593)):
      Psalms 35:10 and Proverbs 19:7, where MAM's כׇּ֥ל, joined to the next atom by a gray maqaf, becomes כָּל־, with a plain maqaf (see "The gray maqaf" below).
4. **Atoms fused and whitespace lost.**
   1. **A note on a lone space.** Parameter stripping removes the space that a documentation
      note marks, and five times two atoms fuse (Deuteronomy 23:8, Ezra 2:69, Nehemiah 3:2,
      3:10, 7:68).
   2. **Parashah templates nested in a note.** Seventeen are dropped, with no break and, in 16
      places where MAM writes no space beside them, fused atoms, as in Judges 2:1, where the
      atoms הַבֹּכִ֑ים and וַיֹּ֩אמֶר֩ have only a note's anchor between them.
   3. **Between verses.** At 18,896 verse boundaries the TEI has nothing between one verse's
      sof pasuq and the next verse's first letter but the verse milestone, where the sheet's
      column C has the space code or the template ר4; a consumer that strips tags runs the
      verses together, as Genesis 1:1-2 into הָאָֽרֶץ׃וְהָאָ֗רֶץ.
   4. **Poetic line breaks.** ר0 becomes `<tei:lb/>` and ר1, ר2 and ר3 `<tei:lb type="indent"/>`,
      with no space beside them, and the 4,269 ר4 of column C, which start a poetic verse on a
      new line, are dropped.
   5. **Added whitespace.** Pretty-printing puts a newline and indentation between adjacent
      elements, 1,473 times inside paragraphs, among them 16 places inside a maqaf compound
      before a ketiv-qere choice.
5. **Distinctions lost.**
   1. **Parashah breaks.** פפ becomes `tei:p type="open-1"` and פפפ `open-3`, but סס, ססס, סס2
      and מ:ששש all become `closed-1`, so MAM's in-line setumah and the spaces of its song
      layout each start a paragraph; the mid-verse flag is dropped.
   2. **Narpas and legarmeh.** מ:פסק (508) and מ:לגרמיה-2 (1,787) both become a bare HEBREW
      PUNCTUATION PASEQ; MAM's spacing survives, but no markup says which is which.
   3. **The gray maqaf.** מ:מקף אפור (116) becomes a plain HEBREW PUNCTUATION MAQAF.
6. **Verse numbering.** The converter renumbers or splits 117 of MAM's verses onto WLC's
   numbering, through the processor's `DIVERGENCES` table and `canonical_verses.py`, which
   raises if the two disagree, and the TEI's milestones agree with the table at every one:
   Exodus 20 and Deuteronomy 5 (the Decalogues, item 5); MAM's Numbers 26:1, split into
   canonical 25:19 and 26:1 at a mid-verse break, which is itself one of the dropped nested
   breaks; MAM's Joshua 21:36-43, numbered 21:38-45, with no milestone for canonical 21:36-37,
   which MAM lacks; MAM's Jeremiah 30:25 and 31, numbered 31:1-40; and MAM's 1 Samuel 23:29 and
   24, numbered 24:1-23. MAM's own number survives in 115 `edition-verse` milestones, which give
   a verse but no chapter.
7. **Notes and their anchors.** All 3,922 notes of the verse rows are in the TEI, 3,917 with
   identical text. Each is anchored by a point before its target's first character, so where a
   note's target ends is lost; the notes on a dual-cantillation passage's combined text sit
   before the whole choice of strands, up to 45 atoms from their word; and the notes of columns
   C and D sit at the head of the verse. The doc-part separator `{{ש}}` becomes a superscript
   asterisk within one `tei:note`. Note ids come from one counter over the whole run, so a change
   in an early book renumbers every later note.
8. **Kept.** Large, small and hung letters (as `tei:hi` with `rend` set to `large`, `small` or
   `raised`), dotted letters, the inverted nun, varika and COMBINING GRAPHEME JOINER.
9. **Added.** 42,338 half-verse milestones, 4 named verse-part milestones and the 115
   `edition-verse` milestones; three half-verse milestones fall inside notes.

## What this record could not cover

1. **The released books were neither built nor opened.** Item 2 applies the exporter's rule,
   read in its code, to the projects at the release commit, and item 5's account of how the
   books print alternatives is read from the exporter's stylesheets. Neither was checked
   against a built book or a released file; downloading the release's files was not approved.
2. **The converter was not run.** That the code at `474cb10` made the TEI at `c91943d` rests on
   the commit history: no commit after `149ce8e` (2026-11-01) touches the importer or a module it
   imports, and the projects' `510a4c5` of the same minute changed one header line per book. The
   whitespace that pretty-printing adds between elements could not be reproduced with
   MAM-basics' own lxml build, so which of those runs survive is known from the TEI, not from
   the code.
3. **The comparison is with the snapshot, not with MAM today.** Item 6 compares the TEI with
   the sheet as exported on 2026-05-27, which is what the converter read. The processor's
   numbering table was checked against that snapshot, where it agrees at all 117 verses, and
   not against MAM's text on Wikisource or MAM-basics' products. Two long notes in the Song of
   Songs differ from the snapshot after their first 200 characters and were not examined.
4. **opensiddur-projects was not searched in full**, as "Searches, and what they could not
   cover" says.
5. **Quotations without Bible markup are counted by matching.** The Haggadah's and Birnbaum's
   unmarked quotations were found by matching their letters with MAM's and chosen by judgment, so
   their counts are approximate. They are not MAM's text in any case.
