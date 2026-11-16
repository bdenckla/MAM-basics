# Upstream: would morphhb's maintainers want an analysed `MAPM/`? (2026-11-15)

Written by a read-only research sub-agent of Claude (Opus 5.5) on 2026-11-15 for question 6
of the morphhb-on-MAM feasibility study. The harness refused the sub-agent's own write of this
file, so it returned the text and the root session saved it here, condensed; every evidence file
it cites is in this folder. Not reviewed by a human. Nothing was posted, pushed or edited.

**Tracked copy, 2026-11-16.** This file was tracked in `morphhb-on-mam/research/upstream/`
when the study was put on ice, with its numbered evidence files and `fetch_log.jsonl`. The
raw API responses (`fetched/`), the decoded files (`decoded-db6c5c9b/` and
`decoded-morphhb-parsing-65dfd513/`) and the scripts stayed untracked in the study folder,
`.novc/morphhb-on-mam-2026-11-15/research/upstream/` (`morphhb-on-mam/README.md`, "What is not tracked").

**Sources.** Pages saved on 2026-11-13 in `.novc/morphhb-corrections-2026-11-13/fetched/` (117
issues and pull requests, 390 issue comments, 6 review comments, 325 commits); `gh api` reads on
2026-11-15 from 14:43 to 14:59 New York time, logged in `fetch_log.jsonl`. File contents are
pinned to morphhb's `db6c5c9b46b8f39346f10915ddb1a70dcd429901` (decoded in `decoded-db6c5c9b/`,
each checked against its blob SHA) and openscriptures/morphhb-parsing's `65dfd513` (in
`decoded-morphhb-parsing-65dfd513/`). API dates are UTC.

**Spot checks by the root session, 2026-11-15:** `decoded-db6c5c9b/.github/scripts/validate_data.py`
lines 31-40, 98-105, 126-140, 165-170, 178-184 and 311-319 read as section 3 says; the
"companion text" sentence is in `03-local-threads-114-115-116.txt`; `11-id-census.txt` shows
every book's ids distinct with the book's two-digit prefix; `13-id-tail-sequences.txt` shows
21,976 distinct tails, Jeremiah's word count; the id paragraph is `decoded-db6c5c9b/README.md`
line 23.

## In brief

No maintainer has said whether they would want an analysed `MAPM/`, and nobody has asked for
one. For it: the README's id paragraph was written so that another codex could share morphhb's
ids, and the one active maintainer accepted MAM-basics' `MAPM/` update within a week and put the
file under CI. For caution: the maintainers describe `MAPM/` as a separate companion text beside
the WLC morphology that the project versions; review is in practice one person's; and the CI
checks nothing at word level in `MAPM/`.

## 1. What morphhb says about ids for another codex, MAPM and Aleppo

- `README.md` line 23 at `db6c5c9b`: the ids are unique and immutable, two digits of the KJV book
  number plus three random characters; another codex could reuse them where its words align and
  create new ones for new words. Added in commit `999ca504` (author "Huberts", 2019-02-06) through
  openscriptures/morphhb#62 (AndyHubert; merged by jag3773 the same day), at Jesse Griffin's request
  in openscriptures/morphhb#58. The ids came with openscriptures/morphhb#56 (2019-01-13, commit
  `5dc21275`).
- `README.md` lines 30-34: the `MAPM/` folder is the project's work with MAM, done with Rabbi
  Kadish for comparison with the OSHB; since openscriptures/morphhb#114 it adds that MAM-basics
  regenerated the file in November 2026.
- David Troidl, openscriptures/morphhb#75, 2021-02-04: "/MAPM is a completely different project."
- David Troidl, openscriptures/morphhb#27, 2017-02-03: the OSHB should respect the WLC, its source.
- Jesse Griffin, body of openscriptures/morphhb#116, 2026-11-11, on the planned 2.3 release: "That
  file is a companion text"; it is not in the npm package; OSHB versions describe `wlc/`'s data;
  the new `MAPM.xml` is the release's one backwards-incompatible change.
- Release notes v.2.0 to v.2.2 describe the morphology as following the WLC.
- No maintainer has said anything about ids for MAPM.

## 2. The pull requests

- openscriptures/morphhb#114 (bdenckla, opened 2026-11-04): one comment, jag3773's, saying Claude
  prepared it at his direction, reporting independent checks (byte-identical to MAM-basics'
  `MAM-morphhb/MAPM.xml` at `83caf168`; valid against OSIS 2.1.1; verse inventory equal to
  `wlc/`'s minus Joshua 21:36-37); merged by jag3773 on 2026-11-11 as `d4265dfa`, 6.6 days after
  opening. No morphology for MAPM is mentioned.
- openscriptures/morphhb#98 (didib, 2022), the one earlier pull request to touch `MAPM/`: two
  chapter numbers; merged by jdejoode after 134 days.
- openscriptures/morphhb#115 (jag3773, 2026-11-11): the validator and its workflow; its body says
  that with few reviewers review is slow; reviewed and answered from jag3773's own account with
  Claude's help; merged 2026-11-14 as `db6c5c9b`, 3.4 days after opening.
- openscriptures/morphhb#116: Ben's two comments of 2026-11-11 are unanswered; comments are
  invited until 2026-12-15, after which 2.3 is tagged.

## 3. What the validator checks

`decoded-db6c5c9b/.github/workflows/validate.yml` runs `.github/scripts/validate_data.py` on every
pull request and push to master.

- Word checks apply only to `wlc/`'s 39 book files (lines 102-103): every `<w>` inside a verse; id
  a fullmatch of `[0-9]{2}[A-Za-z0-9]{3}` (line 39) and unique in one table across all books
  (lines 100, 128-131); lemma present, not otherwise checked (132-133); morph a fullmatch of
  `[HA][A-Za-z0-9]+(/[A-Za-z0-9]+)*` (37, 134-135); text not empty (138-139); 39 books and 23,213
  verses.
- `MAPM/MAPM.xml` is checked only for presence (167-170), verse milestones with exactly one of sID
  and eID (180-183) and correct nesting and closing, no text outside verses except in `note`,
  `title` or `header`, and a verse inventory equal to `wlc/`'s minus `Josh.21.36` and `Josh.21.37`
  (33-34, 311-319). It reads `<w>` in MAPM for text only.
- Inference: an analysed `MAPM.xml` in today's one-file milestone form would pass with its
  lemmas, morphs and ids unchecked; per-book files or container verses would fail the MAPM checks;
  reused `wlc/` ids would collide in a naive extension of the id table, so a MAPM word check needs
  its own uniqueness rule; and a lowercase `id` attribute is not valid OSIS
  (openscriptures/morphhb#84), so the file's OSIS 2.1.1 validity, which jag3773's review counted
  in its favour, would be lost.

## 4. How ids are formed and made

- An id is the book's two-digit KJV ordinal (01 Genesis to 39 Malachi) plus three characters from
  a 58-character alphabet (digits 1-9 and Latin letters except I, O and l). All 306,785 ids are
  distinct (`11-id-census.txt`); the 1,268 ketiv words and 1,278 qere words have their own ids.
- The three characters repeat across books: 21,976 distinct tails, Jeremiah's word count, and every
  book's tails are among Jeremiah's in the same order (`13-id-tail-sequences.txt`); only the prefix
  makes an id unique.
- morphhb has no tool for new ids. The generator is in openscriptures/morphhb-parsing
  (`morphhb-scripts/makeIdList.js`, `exportToOsis.js` at `65dfd513`), begins with
  `process.exit()`, has been disabled since 2019-01-13 (`efccf292`) and needs a private MySQL
  table.
- Ids have been stable: Daniel's 6,034 ids at `5dc21275` all survive; six books equal their 2022
  versions (`14-id-stability.txt`).
- `wlc/VerseMap.xml` maps WLC to KJV verse numbers only; it does not bear on ids.
- Inference: a MAM word aligned with `wlc/` would reuse its id; a word only MAM has would take its
  book's prefix plus an unused three-character string (173,136 strings are unused in every book);
  the validator would accept it. Whether morphhb would accept ids made outside its own process is
  unknown.

## 5. Maintainers and activity

Jesse Griffin (jag3773) is in practice the only active maintainer: he made every merge since
2024-08-27 and every release since 2017. David Troidl was last active in 2022, J. de Joode on
2024-08-27. The repository was nearly dormant from 2024-08-27 to 2026-11-11 (`17-per-year.txt`);
most of jag3773's 2026 comments say Claude prepared them. Ben's openscriptures/morphhb#118 was
open with no comment at 14:59 New York time on 2026-11-15.

## 6. Requests for morphology on another text, or for MAPM to be analysed

None, in 118 issues and pull requests, 396 comments and 328 commits (`02-`, `06-` and
`15-local-search-*.txt`).

## Open points

1. The maintainers' wishes: only a direct question would settle them, an outward act for Ben.
2. Channels off GitHub (the openscriptures-hb mailing list, a Slack group, the GitHub wiki) were
   not searched.
3. Whether the ids' authors have a convention for other codices' ids was not checked.
4. Licensing of the combination (MAPM CC BY-SA 4.0, morphhb's analyses CC BY 4.0) has not been
   asked of the maintainers.
5. Whether OpenScriptorium's importer, which reads `MAPM.xml` line by line, would suit an analysed
   file was not checked.
