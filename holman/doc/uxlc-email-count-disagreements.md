# Where Holman's messages disagree with themselves about their count

Three of Daniel Holman's thirteen suggested-UXLC-correction messages state a number of
corrections that something else in the same message contradicts. Two of the three are
disagreements between the cases written up and the images attached, and are the reason
`../MAM-basics/py/hkq_cmn/uxlc_attachment_notes.py` has an `IMAGES_WITH_NO_CASE` table at all. The
third is a preamble sentence reused from an earlier message.

Measured 2026-08-12, against holman-ketiv-qere `636213d` and the thirteen messages in
`emails/`. The messages themselves do not change once ingested, so the figures below are
stable; re-establish them by the method in the last section rather than trusting them.

## Where a count is asserted, and where it is not

Only six of the thirteen messages state a count at all, and no message states one in both its
subject line and its preamble. The two places are separate and are not to be conflated: **28**
is a subject line and **24** is a preamble sentence.

| Message subject | Date | Subject says | Preamble says | Cases | Images in `.eml` | Images in `.json` |
|---|---|---|---|---|---|---|
| Proposed Corrections and Notes for UXLC (Exodus 7, 11, 20 & 38) | 2026-08-06 | — | four | 4 | 5 | 5 |
| Proposed Corrections and Notes for UXLC (Leviticus 7, 15, 16 & 25) | 2026-08-06 | — | four | 4 | 7 | 7 |
| Proposed Correction and Note for UXLC (Deuteronomy 33) | 2026-08-07 | — | one | 1 | 3 | 3 |
| Suggested UXLC Corrections for Joshua (4 Cases) | 2026-08-07 | 4 | four | 4 | 7 | 7 |
| Suggested UXLC Corrections for Joshua (one Case) | 2026-08-07 | one | **four** | **1** | 1 | 1 |
| Fw: Suggested Corrections for Samuel (1Sa - 2Sa) | 2026-08-08 | — | — | 6 | 7 | 7 |
| Proposed Corrections: Chronicles (1Ch–2Ch) | 2026-08-09 | — | — | 13 | 13 | 13 |
| Suggested Corrections for Ezra, Nehemiah, Esther | 2026-08-09 | — | — | 4 | 4 | 4 |
| Suggested Corrections for Job | 2026-08-09 | — | — | 10 | 11 | 11 |
| Suggested Corrections for Psalms (Part I) | 2026-08-10 | — | — | 20 | 21 | 21 |
| 28 Suggested Corrections (Psalms Part 2 of 2) | 2026-08-11 | **28** | — | 28 | **29** | 28 |
| 5 Suggested Corrections Proverbs | 2026-08-11 | 5 | — | 5 | 5 | 5 |
| Suggested Corrections (Jer, Eze, Minor Prophets, Dan) | 2026-08-12 | — | **24** | 24 | 24 | **23** |

The numbers in the Exodus, Leviticus and Deuteronomy subject lines are chapter numbers rather
than counts. The preamble sentences that do state a count are:

- Exodus and Leviticus, the same sentence in both: "Please find below four suggested
  corrections and manuscript notes for the UXLC based on image comparisons."
- Deuteronomy 33: "I have no suggested corrections for Numbers and could only find one for
  Deuteronomy."
- Both Joshua messages, the same sentence in both: "Please find below four suggested
  corrections for the book of Joshua text."
- Jeremiah/Ezekiel/Minor Prophets/Daniel, `emails/suggested-corrections-jer-eze-minor-prophets-dan.txt`
  line 3: "Below are 24 proposed suggested corrections and updates for the UXLC based on my
  recent analysis of the Leningrad Codex (L) images, along with comparisons to BHS and Dotan."

The Psalms Part 2 preamble states no count — "Below is the rest of Psalms." — so its 28 is the
subject line alone.

Eight messages number their cases internally. All eight run 1 to N contiguously, with N equal
to the number of cases written up, so no internal numbering disagrees with anything.

## The two image disagreements

**Psalms Part 2 of 2** attaches 29 images for 28 cases. The cases are numbered 1 to 28 and end
at Ps 143:10.2; Psalm 140 is not mentioned anywhere in the body. The extra image is
`Ps 140.4.1.png`. One image too many, and the case count agrees with the subject line's 28.

**Jeremiah/Ezekiel/Minor Prophets/Daniel** states 24, writes up 24 and attaches 24, and the two
sets of 24 still do not line up. `Ezek 10.3.2.png` names a case the message does not write up,
and the Amos 8:12.8 case has no image naming it. Across all thirteen messages these are the only
image naming an unwritten case besides `Ps 140.4.1.png`, and the only case with no image of its
own.

Both images are declared in `IMAGES_WITH_NO_CASE` and are not written out, so neither reaches
`gh-pages/uxlc_img/` nor the page. That also means neither appears in the tracked
`emails/<key>.json`, which is why the table above states the `.eml` and `.json` image counts
apart: for these two messages the untracked `.novc/eml/` is the only place the full attachment
list survives.

## What the two images show

Neither is a stray file. Each is a crop of exactly the atom its filename names, and each atom is
the shape of the cases its message is made of.

- `Ps 140.4.1.png` shows שָֽׁנֲנ֣וּ, which is what the UXLC has at Psalms 140:4 atom 1: a meteg
  under the shin. That is the meteg-against-merkha question the whole of Psalms Part 2 is about.
- `Ezek 10.3.2.png` shows עֹֽמְדִ֛ים, the UXLC's Ezekiel 10:3 atom 2: a meteg under the ayin and
  a tevir on the dalet. That is precisely the template of the ten cases in its own message whose
  Correction line is "Add note regarding appearance of accent" — יָֽרְד֛וּ, נָֽתְנ֛וּ, יֵֽלְכ֛וּ
  and the rest.

Both forms above are quoted from the UXLC core XML in the sibling `../UXLC-utils`, at
`in/UXLC-39/Psalms.xml` and `in/UXLC-39/Ezekiel.xml`, rather than typed.

## Why the Jeremiah totals matching at 24 is not proof of a swap

Two crops made, two cases not written for them, and a total that comes out right anyway invites
reading the Jeremiah message as a swap: Ezekiel 10:3.2 dropped and Amos 8:12.8 put in its place.
Three things weaken that reading, though none of them settles it.

**The attachment order is filename sort, not body order.** The Jeremiah message's images arrive
Amos, Daniel, Ezekiel, Hosea, Jeremiah, Micah, Obadiah, Zechariah, where the body runs Jeremiah,
Ezekiel, Minor Prophets, Daniel. So the images were picked from a directory listing, and where
`Ezek 10.3.2.png` sits among them says nothing about the body.

**The Amos 8:12.8 case looks copied from the case eight lines above it.** Amos 3:10.7 and
Amos 8:12.8 have the same Correction sentence, the same Note sentence word for word, and the
same scan file `618_Amos_2.7b-4.1a`, differing only in the column. That leaf covers Amos
2:7b–4:1a and cannot hold Amos 8:12: leaf 621 covers Amos 6:11–8:3 and leaf 623 covers Amos
9:12b–Obadiah 20a, so Amos 8:12 sits on the leaf between those two. A case typed by copying a
neighbour, with the scan citation left unfixed, reads as a late addition rather than as a
substitution.

**The two totals are produced separately** — files selected in one action, case blocks typed in
another — so their agreeing at 24 can be coincidence.

Taken together these favour two independent slips over one swap: an image of Ezekiel 10:3.2
prepared and never written up, and an Amos 8:12.8 case written up with neither an image nor a
corrected scan citation. Only Holman can settle it, which is what the question below asks.

For Psalms Part 2 there is one further small piece of evidence: that message has no `<ol>` or
`<li>` markup at all, so its 1-to-28 numbering is text he typed. A case deleted after typing
would have needed a manual renumber.

## What is not a disagreement

Three things look like surplus images and are not, and each is already settled in code.

- **A captioned companion on a case that is written up.** `Ex 38.12.6 close up.png`, three more
  images on Lev 25:20.4, four on Josh 20:4.12, `2Sa 5.21.1 Enlarged.png` and
  `Ps 9.1.2 Enlarged image of Maqqef.png` all name their case in the filename and are ordinary.
  They are why six messages have more images than cases.
- **`Job 14.19 where UXLC reads as Merekha.png`**, which names the atom the Job 30:1.2 case
  compares against rather than the case itself. It is declared in `COMPANION_IMAGE_CASES`.
- **`Bomberg edition by ben Chayyim.png` and `Sassoon 1053.png`** in the Deuteronomy 33 message,
  which name no case. That message has one case, so `_assign_images` attaches them to it without
  guessing.

## The third disagreement, in the second Joshua message

`Suggested UXLC Corrections for Joshua (one Case)` reuses the opening lines of the Joshua message
sent four hours earlier, so its preamble reads "Please find below four suggested corrections for
the book of Joshua text." while its subject line says one Case and its body has one case. This is
also the message whose one case is Judges 11:24: `uxlc_bracketed_corrections.py` replaces the
subject's "Joshua" with "[Judges]", but the preamble is rendered verbatim, so the page shows
"four suggested corrections for the book of Joshua text" above a single Judges case.

On images against cases, all six messages through Samuel are clean.

## Open, as of 2026-08-12

Nothing below has been decided, and nothing in the parser, the page or the data was changed for
any of it.

1. **The question to Holman has not been sent.** Draft:

   > Two images attached to your recent messages do not line up with the cases in them, and I
   > would like to check which way each mismatch runs before filing them.
   >
   > 1. "28 Suggested Corrections (Psalms Part 2 of 2)" of 11 August has 29 images attached. The
   > extra one is "Ps 140.4.1.png", a crop of שָֽׁנֲנ֣וּ. The message writes up 28 cases, numbered
   > 1 to 28 and ending at Ps 143:10.2, and Psalm 140 is not mentioned anywhere in it. Was a
   > Ps 140:4.1 case meant to be there, or was the image attached in error?
   >
   > 2. "Suggested Corrections (Jer, Eze, Minor Prophets, Dan)" of 12 August attaches 24 images
   > for the 24 corrections it states, but the two sets do not line up. "Ezek 10.3.2.png", a crop
   > of עֹֽמְדִ֛ים, names no case in the message, and the Amos 8:12.8 case has no image. Is the
   > Ezekiel image a case that was dropped, and is the missing Amos image an oversight? Since the
   > totals match at 24, are the two related?

   The draft leaves out the Amos 8:12.8 scan-file point deliberately: Amos 8:12.8 is one of the
   cases whose manuscript citation names a leaf that cannot hold it, and those are better raised
   together than one at a time.

2. **`IMAGES_WITH_NO_CASE`'s comment overstates one thing.** It says Ezekiel 10 "is not mentioned
   anywhere in the body", and Ezekiel 10 is in fact mentioned, in the Ezek 11:1.29 case's scan
   citation `560_Eze_10.7b-11.10a`. What is true, and what the comment needs to say, is that no
   Ezek 10 case is written up.

3. **The second Joshua message's preamble has no bracketed correction**, though its subject line
   has one. Whether "four" and "Joshua" in that sentence should be bracketed the way the subject's
   "Joshua" is has not been decided.

## Re-establishing the figures

No tracked script produces the table above; it was measured with a throwaway in `.novc/`. The
method, run from `C:/Users/BenDe/GitRepos/holman-ketiv-qere` on that repo's own venv:

- **Cases per message** — `uxlc_email_extract.read_emails(emails_dir, image_dir)`, grouping the
  returned cases by `email_key`.
- **Subject and preamble** — the `subject` and `preamble` of each returned `SourceEmail`. Both
  come from `emails/<key>.json` and `emails/<key>.txt`, so this half needs nothing untracked.
- **Images per message, as filed** — the `attachments` list in `emails/<key>.json`.
- **Images per message, as sent** — every `image/png` part of the matching `.eml` in
  `.novc/eml/`, which is untracked and is the only place the two suppressed filenames survive. A
  fresh clone has no `.novc/eml/` and can therefore reproduce every column here except this one.
- **An image naming a case not written up** — match `uxlc_email_extract._ATTACHMENT_REF_RE`
  against each attachment stem and look the resulting `CaseRef.key` up among the message's cases.
- **A case with no image of its own** — the same match, the other way about.

Read anything Hebrew out of a file rather than printing it, and take nothing but attachment
filenames out of a `.eml`: those files hold the correspondents' addresses, and this repo is
public.
