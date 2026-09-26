# HBCE Psalms: a snapshot of its transcriptions, compared with MAM

This directory holds a snapshot of the Critical Edition of the Hebrew Psalter's diplomatic
transcriptions of the Aleppo and Leningrad Codices, Psalms 1–51, and the outputs of a comparison of
them with MAM. The project's site is hbcepsalms.manuscriptroom.com, and this directory calls the
project HBCE, as that address does. The report of record is
[`../doc/hbce-psalms-vs-mam-2026-09-26.md`](../doc/hbce-psalms-vs-mam-2026-09-26.md): it gives the
results, the research queue's tiers, and a workflow for the manuscript research if it resumes.

**Claude sessions downloaded the snapshot, wrote the comparison, and wrote this directory's files
on 2026-09-26. Ben has not reviewed any of it.**

## The download, and why it must not be repeated

HBCE publishes its transcriptions through the Virtual Manuscript Room of the Institut für
Neutestamentliche Textforschung (INTF). The site's robots.txt, kept here as evidence at
[`in/metadata/robots.txt`](in/metadata/robots.txt), disallows the platform's web-service API to
every agent, and asks bulk data consumers to contact the INTF or to use its documented exports.
On 2026-09-26 a Claude session made about 85 requests to that API before anyone had read
robots.txt, and every file under `in/` comes from those responses. The download was made in good
faith, by a session that had not read robots.txt.

It must not be repeated. Nothing in this repository fetches from the site, and nothing here gives
the API's addresses or parameters. If the work resumes, fresh data comes only by contacting the
INTF or through its documented exports, and whether to contact the INTF or HBCE is Ben's decision.

## License and attribution

Each TEI file under `in/transcriptions/` states in its header "(C) 2026 Institut für
Neutestamentliche Textforschung" and a Creative Commons Attribution 4.0 license. The
transcriptions are the work of the Critical Edition of the Hebrew Psalter project, co-directed by
Brent Strawn and Drew Longacre at Duke University, published through the INTF's Virtual Manuscript
Room. They are reproduced here unchanged, under that license.

The catalogue responses and robots.txt under `in/metadata/` state no terms, and no grant is made or
implied here. The outputs under `out/` quote MAM, which keeps its CC-BY-SA 4.0 terms, and forms
from HBCE's transcriptions, which keep CC BY 4.0 with the attribution above; the outputs change
those forms only by splitting them into chanted words and, in `out/research_queue.md`, by putting
their marks in MAM-normal order. [`../DATA-LICENSES.md`](../DATA-LICENSES.md) records the same
terms.

## Files

- `in/transcriptions/`: 35 TEI files, one per codex page, byte for byte as served. `MA_25000.xml`
  to `MA_25140.xml` are the Aleppo Codex, 15 pages, Psalms 1:1–14:7 and 25:2–51:14; `ML_25000.xml`
  to `ML_25190.xml` are the Leningrad Codex, 20 pages, Psalms 1:1–51:21. The number is the
  platform's page id. Each file is the transcription owned by the project account, since the
  platform's published transcription of each page was empty.
- `in/metadata/`: the API's catalogue responses for those documents (`MA_meta.json`,
  `ML_meta.json`, `MA_pages.json`, `ML_pages.json`, `MS1_pages.json`, `MA_coverage.json` and
  `MA_document_groups.json`) and the site's `robots.txt`. `MA_pages.json` and `ML_pages.json` were
  converted to LF line endings; every other file is byte for byte as served. MS1 is Sassoon 1053,
  whose 18 transcribed pages are listed here but not held.
- `out/`: the comparison's outputs, script-regenerable by the command below. Section 9 of the
  report of record describes each one.

The program is [`../py/main_hbce_psalms.py`](../py/main_hbce_psalms.py) and the package
[`../py/hbce_psalms/`](../py/hbce_psalms/).

## Regenerating the outputs

From the repository root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_hbce_psalms.py compare
```

It reads only this directory and this repository's MAM-simple, `MAM-parsed/plus/`, mirrored
introduction and UXLC data, and it never touches the network. Then read
`git diff -- hbce-psalms/out`: the outputs are the test, and every difference is a finding until
it is explained. `py/main_hbce_psalms.py lint-receipt` checks that every Hebrew form in the report
of record is in MAM-normal mark order and occurs in the outputs or the transcriptions.

The outputs record one run, on 2026-09-26, against MAM as this repository had it then:
`MAM-simple/xml-vtrad-mam/Ps.xml` as of `47a86b4d` and `MAM-parsed/plus/D1-Psalms.json` as of
`b5b15c01`. The mega does not run the comparison, so the outputs do not follow later changes to
MAM's data; rerun it if the work resumes. `py/tests/test_mega_coverage.py` declares that reason,
which Ben has not yet reviewed.
