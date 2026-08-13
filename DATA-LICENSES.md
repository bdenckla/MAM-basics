# Data licenses

MAM-basics holds code and data under different terms, so it takes two license declarations.

**The code is GPL-3.0**, declared in [`LICENSE`](LICENSE) at the repository root. That is the
license of MAM-basics' own work in code and prose: everything under `py/`, the Pages workflow
under `.github/`, the plans and notes under `doc/` — the font at `doc/woff2/` excepted, since the
table below covers it — and the generated indexes and reports under `out/` that carry no corpus
text.

**Most of the data is not MAM-basics' to license.** Nearly every corpus here was prepared
elsewhere and is reproduced under the terms its preparers set. This file states those terms; over
that material it grants nothing of its own.

**The exception is Ben Denckla's own data, which this file does dedicate, under CC0 1.0** — the
accent-grammar analyses, the hand transcriptions of printed editions, the generated pages under
`gh-pages/wlc/`, and the other paths the table marks CC0. That is not a new grant. Those files
were published under a repository-wide CC0 `LICENSE` in `bdenckla/wlc-utils` until they were
copied into MAM-basics on 2026-08-12, and restating the dedication path by path is what stops the
move from silently withdrawing it. The full text is at the end of this file, after the MAM
statement.

**Three things about the shape of these two declarations, recorded so they are not tidied away.**
The root [`LICENSE`](LICENSE) holds the GPL-3.0 text itself and must not be replaced by a pointer
to this file: GitHub reads only a root `LICENSE`, `LICENSE.md` or `COPYING` when it reports a
repository's license, so a pointer there would leave MAM-basics reading as unlicensed. This file
is named `DATA-LICENSES.md` rather than `LICENSE-DATA.md` for the mirror-image reason — GitHub's
detector also matches root filenames beginning `LICENSE-`, and would then find two license files
and report the repository's license ambiguously. And **no CC0 `LICENSE` file sits in any
subtree**, though Phase 4 of
[`doc/PLAN-evacuate-the-rest-of-wlc-utils.md`](doc/PLAN-evacuate-the-rest-of-wlc-utils.md)
expected one at `gh-pages/wlc/` and one over the wlc portions of `in/` and `out/`. Measured on
2026-08-12, when those trees arrived, none of the three holds only Ben Denckla's own work: 125 of
the 284 files under `gh-pages/wlc/` are scan crops and a third-party font, `in/` is mostly
tanach.us and J. Alan Groves Center material, and `out/` carries the Westminster Leningrad Codex
text itself. A `LICENSE` file at a directory root reads as covering everything below it, so
placing one in any of those trees would claim for CC0 exactly what the table below withholds. The
dedication is made in the table instead, path by path, with the CC0 text repeated verbatim at the
end of this file.

## Which terms cover which paths

| Path | Content | Terms |
|---|---|---|
| `in/mam-ws/` | MAM wikitext, downloaded from Hebrew Wikisource | CC-BY-SA 4.0 — the statement below |
| `in/mam-go/` | MAM, downloaded from the MAM Google spreadsheet | CC-BY-SA 4.0 — the statement below |
| `in/mam-from-sefaria/`, `in/mam-from-Sefaria-2021-11-23/` | MAM, downloaded from Sefaria | CC-BY-SA 4.0 — the statement below |
| `in/mam-ws-bot-edits/` | edits this repository's bot makes to MAM on Hebrew Wikisource | CC-BY-SA 4.0 — the statement below |
| `out/mam-ws-parsed-fmt-2/`, `out/mam-ws-bot/`, `out/tmpl-survey-plain/`, `out/tmpl-survey-plus/` | derived from the MAM inputs above | CC-BY-SA 4.0, inherited: the license is share-alike, so what is derived from MAM carries MAM's terms |
| `in/chabad-ctr/` | sample verses of the Complete Tanach with Rashi, from chabad.org | chabad.org's; **no grant is made or implied here.** Reproduced for textual comparison, with the source URL of every chapter recorded in the files themselves |
| `in/Psalms 120-134 -- wlcubs420.txt` | a Westminster Leningrad Codex sample | tanach.us's terms: the biblical Hebrew text may be copied without restriction, and citation of the site and version number is requested |
| `in/osisCore.2.1.1-cw6.xsd` | the OSIS 2.1.1 schema | the Bible Technologies Group's: "freely available for all purposes", with acknowledgement requested. The full notice is in the file's own opening annotation |
| `in/scan-pages/` | page-level indexes of printed editions | MAM-basics' own work, so GPL-3.0. These record where a book begins and ends on a scanned page; they carry no text from the editions they index |
| `in/Tanach-26.0--UXLC-1.0--2020-04-01/` | the tanach.us UXLC 1.0 snapshot: 46 XML files under `Books/` — 39 books, five Documentary-Hypothesis variants, and the header and index — plus the site's publisher page and images | tanach.us's, stated in [`License.html`](in/Tanach-26.0--UXLC-1.0--2020-04-01/License.html) inside the tree — the biblical Hebrew text "may be viewed or copied without restriction", citation of the site and its version number appreciated, but "All other files and the look-and-feel of the site are copyrighted by the publisher and require written permission for any purpose", which is what covers `Images/` and `Pages/` here. © 2004 Christopher V. Kimball |
| `in/UXLC-39/` | the UXLC 3.9 book XMLs, copied from UXLC-utils; `_provenance.md` records the source commit | tanach.us's, as above. The change descriptions embedded in these files are Chris Kimball's and Moshe Greenberg's own words |
| `in/UXLC-misc/` | `all_changes.json`, Kimball's cumulative list of UXLC changes | tanach.us's, as above. The descriptions are Kimball's and Greenberg's own words, kept verbatim — which is also why the NFC lint excludes this path |
| `in/wlc420/`, `in/wlc422/` | the Westminster Leningrad Codex 4.20 and 4.22 as tanach.us distributes them: the WLC text in Michigan-Claremont transliteration (`wlc420_ps.txt`, `wlc422_ps.txt`), the manuals (`WLCmanual420.pdf`, `WLC_Manual422.pdf`, `michigan.man`, `supplmt.wts`) and seven release-notes pages, five of them distinct | **the strictest terms in this file, and none of them MAM-basics' to grant.** The two `_ps.txt` files carry the J. Alan Groves Center's own header: "This file may be redistributed only with permission." The manuals and release notes fall under tanach.us's "all other files ... copyrighted by the publisher". `michigan.man` is H. Van Dyke Parunak's 1982 code manual for the Michigan Old Testament; `supplmt.wts` is the Groves Center's supplement to it |
| `in/accgram/edition_transcriptions/`, `in/accgram/printed_decalogue_teamim.json` | Ben Denckla's hand transcriptions of the accentuation of printed Decalogue editions, and the table that indexes them | CC0 1.0 — the dedication at the end of this file |
| `in/accgram/ctr_decalogue.json` | the Decalogue of the Complete Tanach with Rashi, from chabad.org | chabad.org's; **no grant is made or implied here** — the same terms as `in/chabad-ctr/` above |
| `in/accgram/uxlc_accent_changes.json` | the accent-affecting subset of `in/UXLC-misc/all_changes.json` | tanach.us's, inherited. It carries Kimball's and Greenberg's descriptions verbatim, which is why the NFC lint excludes this file by name |
| `in/lci_recs.json` | a table of Leningrad Codex folio locations, compiled by Ben Denckla from tanach.us's `LCIndex.xml`, which is itself derived from the West Semitic Research Project's index at the University of Southern California. The file's own header records that chain | CC0 1.0 for the compilation — the dedication at the end of this file |
| `out/wlc420/`, `out/wlc420-kq/`, `out/wlc420-u/`, `out/wlc420-kq-u/` and their four `wlc422` counterparts; `out/diff_mm_wlc420_wlc422.json`, `out/diff_mx_wlc420_uxlc.json` | the WLC text of `in/wlc420/` and `in/wlc422/` restructured as JSON, with and without ketiv/qere resolution and conversion to Unicode, plus two difference reports | **the WLC's, inherited** — these carry the Groves Center's text, so its "redistributed only with permission" header reaches them. Ben Denckla's structuring of that text is CC0 1.0 |
| `out/accgram/` | the accent-grammar analyses: the prose and poetic scanner runs, the dual-cantillation and printed-Decalogue outputs, and the run records under `goerwitz-stderr/` — where all 37 captured stderr files are empty, so the C checker's own words are not among them, and the summary beside them is generated here | CC0 1.0 for the analysis — the dedication at the end of this file. The biblical Hebrew each file quotes comes from the WLC and the UXLC and keeps their terms above |
| `gh-pages/index.html` | the site's landing page: a hand-written list of one item, pointing at `wlc/` | MAM-basics' own work, so GPL-3.0. It is not one of the `gh-pages/wlc/` pages the row below dedicates to CC0 — it was written here on 2026-08-13, holds no corpus text, and was never in `bdenckla/wlc-utils` |
| `gh-pages/wlc/`, except the three `img/` directories and `woff2/` | the 154 generated pages, the stylesheet, three scripts, and Ben Denckla's 37 UXLC change proposals in `wlc-a-notes/all_uxlc_change_proposals.xml` | CC0 1.0 — the dedication at the end of this file. The biblical Hebrew the pages display comes from the WLC and the UXLC and keeps their terms above |
| `gh-pages/wlc/accgram/img/`, `gh-pages/wlc/420422/img/`, `gh-pages/wlc/wlc-a-notes/img/` | 124 crops from photographic facsimiles of manuscripts — the Leningrad and Aleppo codices among them — and from printed editions: Koren, Ginsburg, Heidenheim, Hahn, Da'at Miqra and others, each named in its own filename | **each rights holder's; no grant is made or implied here.** Reproduced at crop size for textual comparison, cited by the page that displays each one. These are the reason no CC0 file sits at `gh-pages/wlc/` |
| `gh-pages/wlc/woff2/Taamey_D.woff2`, `doc/woff2/Taamey_D.woff2` (byte-identical copies) | the Taamey D Hebrew font, which renders the pointed and accented text on the pages | the font's own — and they are **not recorded anywhere in this repository**, nor in the file, which carries no metadata block. MAM-basics makes no grant over it, and redistributing it means establishing its terms first |

Whole scans of printed editions are still not in this repository, and the indexes under
`in/scan-pages/` are not a substitute for them. See [`doc/scan-pages.md`](doc/scan-pages.md). The
124 crops under the three `gh-pages/wlc/*/img/` directories are the exception: each shows a few
words or a few lines. This paragraph opened "Scans of printed editions are **not** in this
repository" until 2026-08-12, and the arrival of those 124 crops that day is what made the
sentence false.

## The MAM statement, repeated verbatim

What follows is the license and attribution statement from the MAM Google spreadsheet, copied
without change. The same file stands as `LICENSE.md` in the MAM-parsed, MAM-simple, MAM-with-doc,
MAM-OSIS and MAM-for-Sefaria repositories. Where it says "the data in this GitHub repository",
read it as the MAM paths named in the table above, not as everything in MAM-basics.

----

We here repeat, in English & Hebrew, the licence & attribution information
from the MAM Google spreadsheet.
This information applies equally to the data in this GitHub repository.
So, in the text below, ignore any references to "in this spreadsheet" (English)
or שבגליון הנתונים הזה (Hebrew).

----
License:

"Miqra according to the Masorah" as found in this spreadsheet was prepared by Seth (Avi) Kadish
from materials that he originally developed at Hebrew Wikisource,
with major technical assistance from Erel Segal-Halevi and Benjamin Denckla.
All of the material is available under the CC-BY-SA 4.0 license, which is found at the following link:

[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)

Attribution:

Attribution in English and all languages other than Hebrew shall be to "Hebrew Wikisource" (or an equivalent translation) with a direct link to the following page:

[Miqra according to the Masorah](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning)

<!-- No non-Dovi equivalent currently exists for this page on en.wikisource.org. -->

----
רשיון:

"מקרא על פי המסורה" שבגליון הנתונים הזה הוכן ע"י אבי קדיש, על בסיס חומר קיים מהפרויקט שכבר הכין באתר ויקיטקסט, ובעזרת תמיכה טכנית מכרעת מאת אראל סגל-הלוי ובנימין דנקלה. כל החומר מוגש תחת הרשיון Creative Commons ייחוס-שיתוף זהה 4.0, שנמצא בקישור הבא:

[ייחוס-שיתוף זהה 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.he)

ייחוס:

הייחוס בעברית יהיה ל"ויקיטקסט" ביחד עם קישור ישיר לדף שבקישור הבא:

[מקרא על פי המסורה](https://he.wikisource.org/wiki/%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94#%D7%A8%D7%90%D7%A9)

## The CC0 1.0 dedication, repeated verbatim

What follows is the CC0 1.0 Universal legal code, copied without change from the root `LICENSE`
of `bdenckla/wlc-utils`, where it stood over that repository's whole corpus until 620 of its files
were copied into MAM-basics on 2026-08-12. It is fenced because its indentation carries meaning.
**It dedicates the paths the table above marks CC0, and no others** — in particular it reaches
none of the vendored material, and its own clause 4(c) says as much: the affirmer "disclaims
responsibility for clearing rights of other persons that may apply to the Work".

```
Creative Commons Legal Code

CC0 1.0 Universal

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS DOCUMENT DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS
    PROVIDED HEREUNDER, AND DISCLAIMS LIABILITY FOR DAMAGES RESULTING FROM
    THE USE OF THIS DOCUMENT OR THE INFORMATION OR WORKS PROVIDED
    HEREUNDER.

Statement of Purpose

The laws of most jurisdictions throughout the world automatically confer
exclusive Copyright and Related Rights (defined below) upon the creator
and subsequent owner(s) (each and all, an "owner") of an original work of
authorship and/or a database (each, a "Work").

Certain owners wish to permanently relinquish those rights to a Work for
the purpose of contributing to a commons of creative, cultural and
scientific works ("Commons") that the public can reliably and without fear
of later claims of infringement build upon, modify, incorporate in other
works, reuse and redistribute as freely as possible in any form whatsoever
and for any purposes, including without limitation commercial purposes.
These owners may contribute to the Commons to promote the ideal of a free
culture and the further production of creative, cultural and scientific
works, or to gain reputation or greater distribution for their Work in
part through the use and efforts of others.

For these and/or other purposes and motivations, and without any
expectation of additional consideration or compensation, the person
associating CC0 with a Work (the "Affirmer"), to the extent that he or she
is an owner of Copyright and Related Rights in the Work, voluntarily
elects to apply CC0 to the Work and publicly distribute the Work under its
terms, with knowledge of his or her Copyright and Related Rights in the
Work and the meaning and intended legal effect of CC0 on those rights.

1. Copyright and Related Rights. A Work made available under CC0 may be
protected by copyright and related or neighboring rights ("Copyright and
Related Rights"). Copyright and Related Rights include, but are not
limited to, the following:

  i. the right to reproduce, adapt, distribute, perform, display,
     communicate, and translate a Work;
 ii. moral rights retained by the original author(s) and/or performer(s);
iii. publicity and privacy rights pertaining to a person's image or
     likeness depicted in a Work;
 iv. rights protecting against unfair competition in regards to a Work,
     subject to the limitations in paragraph 4(a), below;
  v. rights protecting the extraction, dissemination, use and reuse of data
     in a Work;
 vi. database rights (such as those arising under Directive 96/9/EC of the
     European Parliament and of the Council of 11 March 1996 on the legal
     protection of databases, and under any national implementation
     thereof, including any amended or successor version of such
     directive); and
vii. other similar, equivalent or corresponding rights throughout the
     world based on applicable law or treaty, and any national
     implementations thereof.

2. Waiver. To the greatest extent permitted by, but not in contravention
of, applicable law, Affirmer hereby overtly, fully, permanently,
irrevocably and unconditionally waives, abandons, and surrenders all of
Affirmer's Copyright and Related Rights and associated claims and causes
of action, whether now known or unknown (including existing as well as
future claims and causes of action), in the Work (i) in all territories
worldwide, (ii) for the maximum duration provided by applicable law or
treaty (including future time extensions), (iii) in any current or future
medium and for any number of copies, and (iv) for any purpose whatsoever,
including without limitation commercial, advertising or promotional
purposes (the "Waiver"). Affirmer makes the Waiver for the benefit of each
member of the public at large and to the detriment of Affirmer's heirs and
successors, fully intending that such Waiver shall not be subject to
revocation, rescission, cancellation, termination, or any other legal or
equitable action to disrupt the quiet enjoyment of the Work by the public
as contemplated by Affirmer's express Statement of Purpose.

3. Public License Fallback. Should any part of the Waiver for any reason
be judged legally invalid or ineffective under applicable law, then the
Waiver shall be preserved to the maximum extent permitted taking into
account Affirmer's express Statement of Purpose. In addition, to the
extent the Waiver is so judged Affirmer hereby grants to each affected
person a royalty-free, non transferable, non sublicensable, non exclusive,
irrevocable and unconditional license to exercise Affirmer's Copyright and
Related Rights in the Work (i) in all territories worldwide, (ii) for the
maximum duration provided by applicable law or treaty (including future
time extensions), (iii) in any current or future medium and for any number
of copies, and (iv) for any purpose whatsoever, including without
limitation commercial, advertising or promotional purposes (the
"License"). The License shall be deemed effective as of the date CC0 was
applied by Affirmer to the Work. Should any part of the License for any
reason be judged legally invalid or ineffective under applicable law, such
partial invalidity or ineffectiveness shall not invalidate the remainder
of the License, and in such case Affirmer hereby affirms that he or she
will not (i) exercise any of his or her remaining Copyright and Related
Rights in the Work or (ii) assert any associated claims and causes of
action with respect to the Work, in either case contrary to Affirmer's
express Statement of Purpose.

4. Limitations and Disclaimers.

 a. No trademark or patent rights held by Affirmer are waived, abandoned,
    surrendered, licensed or otherwise affected by this document.
 b. Affirmer offers the Work as-is and makes no representations or
    warranties of any kind concerning the Work, express, implied,
    statutory or otherwise, including without limitation warranties of
    title, merchantability, fitness for a particular purpose, non
    infringement, or the absence of latent or other defects, accuracy, or
    the present or absence of errors, whether or not discoverable, all to
    the greatest extent permissible under applicable law.
 c. Affirmer disclaims responsibility for clearing rights of other persons
    that may apply to the Work or any use thereof, including without
    limitation any person's Copyright and Related Rights in the Work.
    Further, Affirmer disclaims responsibility for obtaining any necessary
    consents, permissions or other rights required for any use of the
    Work.
 d. Affirmer understands and acknowledges that Creative Commons is not a
    party to this document and has no duty or obligation with respect to
    this CC0 or use of the Work.
```
