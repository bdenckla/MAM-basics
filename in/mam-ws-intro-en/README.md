# Local mirror of the English translation of the MAM introduction

Read this before using or refreshing the mirror in this directory.

## What this directory holds, and in what sense it is parallel to `in/mam-ws-intro/`

Hebrew Wikisource's introduction to MAM, mirrored in [`in/mam-ws-intro/`](../mam-ws-intro/README.md),
has a partial English translation on English Wikisource. It is kept in the user space of Dovi,
Avi Kadish's account, under `User:Dovi/Miqra according to the Masorah/Introduction`. This
directory mirrors every page under that prefix, byte for byte, one `.mediawiki` file each, with
a `manifest.json` that records each page's title, revision id, revision timestamp and byte size,
and the title of its Hebrew counterpart.

The mirror is parallel to the Hebrew one in one exact sense: **each English page is written
under the slug of the Hebrew page it translates**, so `ch3.mediawiki` here translates part of
`in/mam-ws-intro/ch3.mediawiki`. A Hebrew page with no English page, such as `ch4`, has no file
here. The pairing is checked on every refresh rather than declared: each Hebrew page paired with
an English page with text must end with exactly one interlanguage link to it, or to a redirect
to it, and every other Hebrew page must have none.

Refresh with this command, run from the repository root:

```powershell
./.venv/Scripts/python.exe py/main_download.py fr-ws-intro-en
```

It is separate from `fr-ws-intro`, as that one is from `fr-wikisource`: the English moves when
its translators edit it, not when the Hebrew does. `py/subcommands/download_wikisource_intro_en.py`
does the work, and its docstring gives the checks in full.

## The files

The table records the pages as the first refresh found them on 2026-11-22. `manifest.json`, not
this table, says what the mirror holds now.

| File | English Wikisource page, under the prefix | Revision | Edited (UTC) | What it held on 2026-11-22 |
|---|---|---|---|---|
| `root.mediawiki` | the prefix itself | 15106504 | 2025-06-01 09:17 | a contents list, and a note to the reader by the translator |
| `summary.mediawiki` | `/Abstract` | 15903740 | 2026-04-24 19:25 | the edition's English abstract |
| `ch1.mediawiki` | `/Chapter 1` | 14796317 | 2025-01-17 13:24 | a title only |
| `ch2.mediawiki` | `/Chapter 2` | 14796320 | 2025-01-17 13:24 | two sections, headed 4.6 and 9.1 |
| `ch3.mediawiki` | `/Chapter 3` | 14833310 | 2025-01-30 18:26 | a partial translation |
| `appendices.mediawiki` | `/Appendices` | 14796325 | 2025-01-17 13:26 | a partial translation |
| `data-sheet-guide.mediawiki` | `/Technical Guide to the Spreadsheet` | 14796335 | 2025-01-17 13:29 | the guide to the data sheet |
| `technical-guide.mediawiki` | `/Technical Guide` | 14796336 | 2025-01-17 13:29 | a redirect to `/Technical Guide to the Spreadsheet` |

**`technical-guide.mediawiki` is a redirect, mirrored as the redirect it is,** as the Hebrew
mirror mirrors its own redirect of the same slug. Dovi's move of the guide to its present title,
on 2025-01-17, left it behind, and the English root's contents list still links the guide
through it. The Hebrew page `in/mam-ws-intro/technical-guide.mediawiki` is likewise a redirect to
the Hebrew guide, `data-sheet-guide`. The refresh fails unless each of the two redirects leads to
its own wiki's page of `data-sheet-guide`.

The Hebrew root's interlanguage link names another redirect,
`User:Dovi/Miqra according to the Masorah/Information about this Edition`, outside the prefix;
the refresh resolves it to the English root and does not mirror it.

## How the mirror reads English Wikisource

The refresh reads English Wikisource through the Action API, `https://en.wikisource.org/w/api.php`,
the way `fr-ws-intro` reads Hebrew Wikisource. It makes four requests: a listing of the prefix,
which fails the refresh if the set of pages has changed; a metadata query for the Hebrew pages'
interlanguage targets; a metadata query for the declared pages as themselves; and a query for
those revisions' exact bytes, by revision id. The requests go one at a time, at least five
seconds apart, with `maxlag=1`, and with the User-Agent of the Hebrew mirror. Nothing is cached.

That choice was Ben's Decision 1 of `doc/PLAN-english-intro.md`. His decision page recommended
1A, the Action API as the Hebrew mirror uses it, within the limits that the Robot policy's
Action API section sets, and Ben, 2026-11-22: "I concur with all three off your recommendations
on the decision page."

These are the facts it was decided against, as the plan's section "Wikimedia's robots.txt and
Robot policy" records them from a reading on 2026-11-22:

1. Wikimedia's `robots.txt`, which `en.wikisource.org` serves, disallows `/w/` to every user
   agent, and with it the Action API, `/w/api.php`.
2. Wikimedia's [Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy) asks every
   client to honor every directive of `robots.txt`. Its Action API section sets the limits for
   an unauthenticated client: one request at a time, and fewer than five a second.

So the refresh does not obey `robots.txt`, by Ben's decision, and keeps far inside the Action
API's limits. The Hebrew downloaders read Hebrew Wikisource through the same API under the same
`robots.txt`; Phase 7 of the plan is where their practice will be recorded.

## The text is byte-verbatim

Each file holds its revision's wikitext exactly as English Wikisource returned it. Nothing is
normalized, and nothing is to be repaired here: the pages quote pointed Hebrew in the source's
own mark order, so this tree is exempt from the MAM-normal mark-order rule, as the Hebrew mirror
is, and `doc/mam-normal-mark-order.md` records its clusters in the other order. Do not run
`uni_check` or `has_std_mark_order` over it. Some lines end in spaces or tabs, which
`.gitattributes` keeps, as it keeps the Hebrew mirror's. A change to the English belongs on
English Wikisource, followed by a refresh.

A refresh over an unchanged wiki produces no diff, so a diff that a refresh does produce is an
edit on English Wikisource, or a retitled Hebrew page, and is worth reading.

## License, translator and staleness

The English is under CC BY-SA 4.0, English Wikisource's terms for its text, as
`DATA-LICENSES.md` records. The root's note to the reader, signed by Mitchell Powell, describes the translation as
a student's partial draft, made slowly with online dictionaries and machine translation, not a
reliable scholarly one, and releases it under the CC BY-SA license. Each page's history on
English Wikisource names its contributors.

The mirror goes stale in two ways. English Wikisource can change, which a refresh shows. And
most of the English predates revisions of the Hebrew, so a current English page can translate
Hebrew that has since changed; [`doc/intro-en-evaluation-2026-11-22.md`](../../doc/intro-en-evaluation-2026-11-22.md)
records that drift with its other findings, and
[`doc/PLAN-english-intro.md`](../../doc/PLAN-english-intro.md) plans how the English is kept in
parallel with the Hebrew.
