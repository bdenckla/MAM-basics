---
name: verse-links
description: Build the links Ben asks for when he looks a verse or an atom up — mgketer.org and masoretica.org for the Aleppo Codex; tanach.us, masoretica.org and Sefaria's image of the Leningrad Codex folio with the atom's estimated column and line; MAM-with-doc and MAM on Hebrew Wikisource; and the rarer mechon-mamre.org and Chabad CTR links — by running MAM-basics' py/main_verse_links.py, never by writing a URL by hand.
when_to_use: Load when Ben asks for any of those links, or for where an atom is in the Leningrad Codex — "the masoretica and mgketer links for 2 Chronicles 28:23", "a sefaria link and the atom estimate" — and before any message that names a verse for Ben to look up in a manuscript or an edition. Not needed for links a generated page already has, such as the mgketer diff cards'.
---

Ben, 2026-09-10: *"all the time I'm asking for one or more of the following: masoretica link,
mgketer.org link, tanach.us link, sefaria.org leningrad image link, leningrad atom location
estimate, MAM with doc link, wikisource MAM link, and some rarer ones: mechon mamre link, chabad
ctr link"*. One command in MAM-basics builds every one of them. **Run it, and never assemble one
of these URLs by hand**: the book spellings masoretica.org takes, mechon-mamre.org's book codes
and hexadecimal chapter, and the percent-encoded Hebrew of a Wikisource page name are each easy
to get subtly wrong. The command's builders agree with the ones the mgketer diff cards use on 278
of 278 cases, checked 2026-09-10.

## Running the command

From any directory — every path is resolved from the script, never from the cwd:

```
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_verse_links.py <book> <c:v> [<hebrew> | --atom N]
```

1. **`<book>` is a bk39 id, and several are not the obvious spelling**: `Levit`, `Deuter`,
   `Tsefaniah`, `1Samuel`, `2Kings`, `1Chronicles`, and `"Song of Songs"`, quoted for its spaces.
   An unknown id is refused with the full list.
2. **Name the atom by its Hebrew text or by `--atom N`.** The Hebrew is matched against the UXLC
   exactly, then by its letters alone, so MAM's pointed form and a bare consonantal one both
   work. With neither, the Leningrad Codex line gives where the verse starts and ends.
3. **`--atom` counts the UXLC's atoms, not MAM's**: one per `<w>` and per `<q>` of the UXLC core
   XML, a ketiv not counted. When the Hebrew given matches none of the verse's atoms, or more than
   one, the command lists the atoms numbered in exactly that count and exits 1; rerun with
   `--atom`.
4. **It needs nothing beyond MAM-basics' tracked data**: no `REPOS_ROOT`, no network, no sibling
   clone. Codex runs it the same way.

`--help` is the full statement, including the versification caveat below.

## What each printed link is

One markdown link per line, in this order:

| Label | What it is |
| --- | --- |
| `mgketer` | mgketer.org's page for the **chapter** |
| `MwD` | the verse in MAM-with-doc |
| `MAM-ws` | MAM on Hebrew Wikisource, the **chapter's** page |
| `tica` | the verse at masoretica.org, in the Aleppo Codex |
| `MM` | the verse at mechon-mamre.org |
| `UXLC` | the verse at tanach.us |
| `tica LC` | the verse at masoretica.org, in the Leningrad Codex |
| `LC <folio>` | Sefaria's image of that Leningrad Codex folio, with the estimator's column and line for the atom; a verse crossing a page break gets two such lines |
| `CTR` | the chapter in Chabad's Complete Tanach with Rashi, **only where MAM-basics records Chabad's URL for it** — ten chapters on 2026-09-10: seven psalms, Proverbs 8, Exodus 20 and Deuteronomy 5. For any other chapter the line says so and gives Chabad's index of the CTR instead. |

## Presenting the links to Ben

1. **Links, not downloads.** Ben, 2026-09-10, when a session offered to download a leaf of each
   codex: *"Normally i'm more interested in getting an mgketer.org link than an image since for
   one thing I don't think its aleppo images are easy (or allowed?) to download. for leningrad
   images, i'm more interested in a sefaria image link plus an estimate of the atom location, or
   a tanach.us link for the verse (which will take me to the sefaria link and give me its own %
   estimate of the atom location, not as good as my estimator but still pretty helpful)"*.
   Download an image only when he asks for one.
2. **Relay the links he asked for, copied from the output verbatim.** If he named none, relay
   them all; the output is short.
3. **Show MAM's form of the atom whenever an atom is at issue**, lifted from MAM's data and never
   retyped. Ben asked for this of printed-edition lookups on 2026-09-10 — *"You didn't show me to
   the Zech 13:3 final word to confirm what I'm looking for (please do in future)"* — and his
   reason, that he confirms by the form that the atom he has found is the one meant, holds for a
   manuscript folio as well. Where the client can render an inline widget, show pointed Hebrew in
   one at twice the chat's text size and regular weight, never as a markdown heading, which is
   bold: *"many fonts don't show pointed Hebrew well in bold"* (Ben, 2026-09-10).
4. **Say which count an atom number is in.** The `LC` line's "atom 11 of 11" counts the UXLC's
   atoms, as item 3 of the previous section describes; do not present it as MAM's atom number,
   which can differ.
5. **Present the line as an estimate, and leave what the manuscript has for Ben to read.** The
   folio comes from the UXLC's page index, and the column and line are interpolated by word
   count. The column agreed with Holman's own on 117 of 124 atoms, measured 2026-08-12
   (`py/main_estimate_uxlc_locations.py`). The line has been checked against the image twice,
   and both times the estimate put the atom lower on the page than it is: Lamentations 2:3 was
   estimated at line 12.9 and is on line 10, and Psalms 72:15 at line 5.5 and is on line 3
   (Ben's readings, 2026-08-04 and 2026-09-10). When Ben reads a position off an image, record
   it in MAM-basics' `leningrad/page-snips/README.md` with a crop and a calibration note, as
   those two are. Never report what the Leningrad Codex has on the UXLC's authority — a
   transcription is evidence about the transcription.
6. **Mind versification.** Every link takes the reference as given. Where MAM's versification
   and the UXLC's differ — the UXLC's Numbers 25:19 is MAM's 26:1 — run the command once with
   each reference. It exits 1 when the UXLC has no such verse, after printing the other links.
7. **Never guess a Chabad article id.** A CTR chapter URL is an article id, and only ten are
   recorded. If Ben wants CTR links routinely, the fix is a table of every chapter's id fetched
   from chabad.org once, which is a download and so his decision.

## Where each piece lives in MAM-basics

All under `C:/Users/BenDe/GitRepos/MAM-basics`. Change a link there, never in this skill:

1. `py/main_verse_links.py` — the command.
2. `py/mb_cmn/verse_external_links.py` — the mgketer, MwD, MAM-ws, tica and MM builders for all
   39 books. It is the shared module `MAM-private/doc/PLAN-share-verse-link-builders.md` designs,
   written 2026-09-10 with this command as its only consumer; the plan's other stages are
   paused, so the mgketer diff cards still build their own copies of those links.
3. `py/hkq_cmn/uxlc_external_links.py` for tanach.us and `py/hkq_cmn/uxlc_manuscript_page.py` for
   Sefaria's image URL.
4. `py/uxlc_misc/my_uxlc_location.py`, the estimator, and `py/uxlc_misc/my_uxlc_find_atom.py`,
   which matches Hebrew to an atom for this command and for `py/main_uxlc_estimate_atom_loc.py`.
5. `in/chabad-ctr/*.json` and `in/accgram/ctr_decalogue.json`, the recorded CTR URLs.

This skill's canonical copy is `MAM-basics/dot-claude/skills/verse-links/`, and it is shared with
Codex: a change reaches `~/.claude/skills/verse-links/` and `~/.agents/skills/verse-links/` by the
procedure in `MAM-basics/dot-claude/README.md`.
