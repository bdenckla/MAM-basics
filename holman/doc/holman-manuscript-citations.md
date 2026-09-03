# Holman's manuscript-image citations, and the five that name the wrong scan

Measured 2026-08-12, on `holman-ketiv-qere` at `bc2ce42`. Everything here is
re-establishable from what the repo tracks, plus the sibling `UXLC-utils` clone
for the change-record section.

Each of Daniel Holman's suggested-correction cases carries an `Image` field
naming the Leningrad Codex scan he worked from and where on it he found the
atom, for example `492_Jer_2.11b-2.37a | Col. 1 middle`. Two facts are read out
of that citation: the leading number is a page-side ordinal that
`../MAM-basics/py/hkq_cmn/uxlc_manuscript_page.py` inverts to a folio, and the rest is
his column and band.

## The finding

**Five of the 124 citations name a scan file whose own name says it cannot hold
the case's verse.** The name carries its verse range, so this needs no
estimator: `623_Amos_9.12b-Oba_20a` holds Amos 9:12 through Obadiah 20, and
Micah 1:14 is past its end.

| case | Holman's `Image` field | verse range the file name states | folio from his ordinal | estimated folio |
| --- | --- | --- | --- | --- |
| Jeremiah 3:24.2 | `492_Jer_2.11b-2.37a \| Col. 1 middle` | Jer 2:11b – 2:37a | 246B | 247B |
| Amos 8:12.8 | `618_Amos_2.7b-4.1a \| Col. 2 top` | Amos 2:7b – 4:1a | 309B | 311B |
| Obadiah 1:1.17 | `621_Amos_6.11-8.3 \| Col. 1 bottom` | Amos 6:11 – 8:3 | 311A | 312A |
| Micah 1:14.10 | `623_Amos_9.12b-Oba_20a \| Col. 2 bottom` | Amos 9:12b – Obadiah 20a | 312A | 313B |
| Zechariah 12:5.1 | `644_Zech_8.21b-10.3a \| Col. 2 middle` | Zech 8:21b – 10:3a | 322B | 323B |

The estimated folio is `data/uxlc_atom_locations.json`'s, keyed as
`CaseRef.key` spells a reference.

Two nearby cases show the slip is not systematic across the message. **Amos
3:10.7** cites the very same `618_Amos_2.7b-4.1a` and is right, folio and
estimate both 309B; **Jeremiah 8:9.9** cites `499_Jer_7.24b-8.9a` and is right,
both 250A.

## The five are the complete set

Two independent tests agree on every one of the 124 cases: parsing the verse
range out of the scan-file name and asking whether it holds the case's verse,
and comparing the folio Holman's ordinal decodes to against the estimate. Five
fail containment, and those same five are the only ones whose decoded folio
differs from the estimate. **No case's cited range misses its verse while the
decoded folio still happens to match the estimate**, which is the combination a
folio comparison alone would not see.

The other 119 split into 115 whose verse is strictly inside the cited range, and
four whose verse is the range's closing part-`a` verse — 2 Samuel 5:21.1,
Jeremiah 8:9.9, Psalms 18:7.3 and Job 34:20.4. All four of those agree with the
estimate.

## What the pattern looks like

All five are in one message, `emails/suggested-corrections-jer-eze-minor-prophets-dan.txt`,
dated 2026-08-12 04:45 UTC. Four run consecutively: that message's MINOR
PROPHETS section has six cases, the first two of which (Hosea 5:6, Amos 3:10)
cite correctly and the last four of which all fail. Amos 8:12.8 repeats the file
name of the case directly above it, `618_Amos_2.7b-4.1a`, verbatim.

The cited ordinals run **low** by 2, 4, 2, 3 and 2 page-sides respectively, and
never high.

## Two things checked and ruled out

**The scan-file names are a coherent series.** Sorting the 99 distinct names by
ordinal gives verse ranges that ascend with it, apart from two steps —
`726_2Ch_33.20b-34.14a` to `732_Ps_5.5b-8.5a`, and `816_Job_39.4b-40.19a` to
`823_Pro_7.3-8.18a`. Both steps are the Leningrad Codex's own book order,
Chronicles heading the Ketuvim and Job preceding Proverbs, showing up against
the ordinary book numbering the check used. Neither is a break in the names.

No containment verdict depends on that ordering. The only ranges spanning two
books are `552_Jer_52.26b-Eze_1.16a` and `623_Amos_9.12b-Oba_20a`, and Jeremiah
precedes Ezekiel and Amos precedes Obadiah in the Leningrad Codex's order and in
the ordinary one alike.

**One name needed an allowance.** Holman typed `790_Ps_141.6b-144.11a.` with a
trailing period, on Psalms 143:10.2. Stripped of the period the range holds the
verse and the folio agrees.

## What changed on the page

Ben Denckla's decision, 2026-08-12, on being shown the five: do not keep echoing
Holman's mistakes. So `../MAM-basics/py/py_render/uc_case_card.py` now links the folio from
`data/uxlc_atom_locations.json` and names Holman's beside it where the two
disagree — the treatment his column already had. Micah 1:14 now reads
"Column 2, line 26 or thereabouts. Holman cites folio 312A." above a link to
folio 313B. Only those five cards changed. Commit `bc2ce42`.

His wrong folio is kept visible as a labelled divergence rather than dropped.
The citation itself is still in the tracked message body either way.

## Are these entered as UXLC change records, with the right folios?

**Not from this message, and it is too early for them to be.** The message is
dated 2026-08-12, and the newest batch the UXLC's editor has entered is
2026.08.05, a week earlier. That batch is 30 records, `2026.08.05-1` through
`-30`, running Genesis, Exodus, Leviticus, Deuteronomy, Joshua, Judges, Samuel,
Job. **It has no Jeremiah, Ezekiel, Minor Prophets or Daniel record at all**, so
none of the five is in it.

**Two of the five do have older records on the same word, from earlier rounds,
and both give the correct folio** — correct precisely where the 2026 citation is
wrong:

| case | record | changes file | author | record's folio | estimate | Holman's 2026 citation |
| --- | --- | --- | --- | --- | --- | --- |
| Obadiah 1:1.17 | 2021.08.07-15 | `2021.10.19 - Changes.xml` | Ben Denckla | 312A col 1 line 20 | 312A col 1 line 20.8 | 311A |
| Micah 1:14.10 | 2022.12.12-9 | `2023.04.01 - Changes.xml` | Daniel Holman | 313B col 2 line 27 | 313B col 2 line 25.9 | 312A |

The Micah one is the sharpest: **Holman himself gave folio 313B for that word in
2022 and cited 312A for the same word in 2026.** His own earlier record
contradicts his current citation. That 2022 record asked to add a merkha to the
kaf; the 2026 case says the accent should be a tifcha rather than a merkha, so
he is revisiting his own change.

Jeremiah 3:24.2, Amos 8:12.8 and Zechariah 12:5.1 have no record in any changes
file.

**Change-record folios are reliable in general.** Across the 17 changes files in
`UXLC-utils/in/UXLC-misc/` — 1398 records — 54 of the 124 cases have at least
one record, and every one of those records agrees with the estimator's folio.
Five look like disagreements and are only older spellings of the same leaf:
`43r` and `71v` in recto/verso notation for 043A and 071B, and an `F` prefix in
`F367B` and `F376A` for 367B and 376A. So what slipped is the per-message
`Image` citation in this one email, not the change records.

## Two loose ends in `uxlc_change_records.py`, observed but not acted on

Both turned up while checking the above, both concern
`CHANGE_RECORD_IDS_BY_REF`, and neither was changed here, because a separate
session was working in that file on 2026-08-12. Re-check each before acting.

- **The six Samuel cases do have records.** The module docstring says they have
  none; the 2026.08.05 batch holds `-17` through `-22` on 1Sa 7:10.10, 1Sa
  13:4.11, 2Sa 5:21.1, 2Sa 7:22.7, 2Sa 15:26.11 and 2Sa 24:10.20, which are the
  six Samuel cases. The table maps `-1` through `-16` and `-23` through `-30`,
  skipping exactly that run.
- **The four Exodus ids look rotated.** The table maps Exodus 7:20.19 to `-6`,
  11:6.1 to `-3`, 20:3.2 to `-4` and 38:12.6 to `-5`. The changes file has those
  four in verse order instead: `-3` is Exodus 7:20.19, `-4` is 11:6.1, `-5` is
  20:3.2 and `-6` is 38:12.6. Everything from `-7` onward matches the table.

Both readings come from `UXLC-utils/in/UXLC-misc/2026.10.19 - Changes.xml` as
that file stood mid-refresh on 2026-08-12, **uncommitted in another session's
working tree**. The tracked version at `UXLC-utils` commit `c31aeea` (2026-07-01)
holds only the ten 2026.04.10 records and knows nothing of the 2026.07.24 or
2026.08.05 entries, so a checkout of that commit cannot reproduce this section.
Confirm against the committed refresh, or against the live page
`uxlc_change_records.CHANGES_PAGE_URL` names, before changing the table.

## How to re-establish all of it

No network access is needed for the first two; the third needs the sibling
`UXLC-utils` clone.

1. **The cases and their citations.** `read_emails(Path("emails"),
   Path("gh-pages/uxlc_img"))` from `../MAM-basics/py/hkq_cmn/uxlc_email_extract.py`.
   Each case's `image_location` property is the citation, and `ref.key` spells
   its reference.
2. **The two tests.** Take the first whitespace-separated token of the citation,
   strip a trailing period, and read the range off it: the names run
   `NNN_Book_C.Vb-C.Va`, the second endpoint carrying its own `Book_` prefix
   only when the page spans two books, a single-chapter book giving a bare verse
   number, and the `a`/`b` suffixes marking part-verses. Compare the range
   against the case's own reference. Separately, compare
   `manuscript_page(...).folio_label` against `data/uxlc_atom_locations.json`'s
   `folio`. Expect the two tests to pick out the same five cases.
3. **The change records.** Parse every `in/UXLC-misc/*Changes*.xml` in the
   sibling `UXLC-utils` with `ElementTree`; each `<change>` has a `<citation>`
   of book, `<c>`, `<v>` and `<position>`, and an `<lc>` of `<folio>`,
   `<column>` and `<line>`. Match on book, chapter and verse rather than
   position, since the change list and Holman number atoms differently. Read
   `in/UXLC-misc` only: `in/UXLC-misc-fixed` holds a `Changes fake.xml` fixture
   and, on 2026-08-12, an untracked shadow copy of the 2026.10.19 file that
   double-counts 82 records.

Run anything written for this from the repo root with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.
