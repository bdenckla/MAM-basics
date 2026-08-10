# Data licenses

MAM-basics holds code and data under different terms, so it takes two license declarations.

**The code is GPL-3.0**, declared in [`LICENSE`](LICENSE) at the repository root. That is the
license of MAM-basics' own work: everything under `py/`, and the generated indexes and reports
under `out/` that carry no corpus text.

**The data is not MAM-basics' to license.** Every corpus here was prepared elsewhere and is
reproduced under the terms its preparers set. This file states those terms; it grants nothing of
its own.

**Two things about the shape of these two declarations, recorded so they are not tidied away.**
The root [`LICENSE`](LICENSE) holds the GPL-3.0 text itself and must not be replaced by a pointer
to this file: GitHub reads only a root `LICENSE`, `LICENSE.md` or `COPYING` when it reports a
repository's license, so a pointer there would leave MAM-basics reading as unlicensed. This file
is named `DATA-LICENSES.md` rather than `LICENSE-DATA.md` for the mirror-image reason — GitHub's
detector also matches root filenames beginning `LICENSE-`, and would then find two license files
and report the repository's license ambiguously. Phase 4 of
[`doc/PLAN-evacuate-the-rest-of-wlc-utils.md`](doc/PLAN-evacuate-the-rest-of-wlc-utils.md) adds
the wlc-utils paths as rows in the table below when that plan runs.

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

Scans of printed editions are **not** in this repository, and the indexes under `in/scan-pages/`
are not a substitute for them. See [`doc/scan-pages.md`](doc/scan-pages.md).

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
