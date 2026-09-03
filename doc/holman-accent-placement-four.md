# Notes: the four accent-placement Holman suggestions (M17, M24, M32, M34)

Evidence for the seven-item programme
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md). **"The larger
rollout plan" and "the rollout plan" below name that programme**, whose item 4 is the phase this
note calls "download the chapters" and whose item 7 is the phase it calls "refresh mgketer". The
four records covered here are the four the programme excludes: its thirty are M1–M16, M18–M23,
M25–M31 and M33, all of M1–M34 except M17, M24, M32 and M34.

Captured 2026-09-03 in a plan-mode session of MAM-basics, one of a set of six notes written
under `C:/Users/BenDe/.claude/plans/` because concurrent work in git-tracked areas had not
concluded. All six were moved into `doc/` on 2026-09-03.

**Correction, 2026-09-03: the date "2026-09-05" HAS BEEN LEFT AS WRITTEN in two places below**,
the original heading's "Captured 2026-09-03/05" and the section headed "Ben's expectation,
2026-09-05". Both postdate the note's capture, and nothing found on 2026-09-03 explains them.
They are recorded here rather than silently changed, since a date in an evidence note is
evidence; read the expectation as Ben's, stated in the session that wrote the note.

## The four records and their dispositions

All four compare MAM against the Jerusalem Crown (not the Aleppo Codex), and all four already
carry a ruling in `py/hkq_cmn/mam_suggestion_dispositions.py`, decided by Seth (Avi) Kadish on
2026-08-28.

| M | verse.atom | MAM | Jerusalem Crown | Holman's suggestion | Ruling |
|---|---|---|---|---|---|
| M17 | 2 Kings 17:15.15 | וַיֵּ֨לְכ֜וּ (geresh over kaf) | וַיֵּ֨לְכוּ֜ (geresh over final vav) | Move geresh to end of word | Not taken. Aleppo is not extant here; against Leningrad, the geresh (erased, per UXLC) still stood over the kaf, not the vav. Same misplacement in BHS and Mechon-Mamre — three editions sharing one source. Avi added a note in MAM rather than moving the accent. |
| M24 | Joshua 10:12.3 | יְהוֹשֻׁעַ֙ (one pashta) | יְהוֹשֻׁ֙עַ֙ / as sent יְהוֹשֻׁ֨עַ֙ (qadma as helper) | Add helper accent | Taken. Changed on Wikisource 2026-08-28: "MAM now has the pashta repeated over the ש (shin)." |
| M32 | Judges 10:11.1 | וַיֹּ֥אמֶר (merkha on yod) | וַ֥יֹּאמֶר (merkha on vav) | Place merkha on first syllable | Not taken. The stressed syllable begins with the yod; Aleppo agrees with MAM. JC's placement is an error also in Mechon-Mamre. Avi added documentation in MAM. |
| M34 | Zechariah 2:4.11 | זֵר֣וּ (munaḥ on vav-side) | זֵ֣רוּ pattern reversed | Place munaḥ on second syllable | Taken. Changed on Wikisource 2026-08-28: "MAM now has the munaḥ on the ר (resh)." |

So of the four, two are declined (MAM's existing reading stands, Aleppo/Leningrad agrees with
MAM against the Jerusalem Crown) and two are accepted and already edited directly on
Wikisource by Avi. Nothing further is planned for M17 or M32.

## M24 and M34 differ in how far the accepted edit has propagated

Checked 2026-09-03 by reading the actual text at each stage, not by inferring from mgketer's
diff reports alone:

| stage | M34, Zechariah 2:4 | M24, Joshua 10:12 |
|---|---|---|
| Live Hebrew Wikisource | Has the fix (Avi's diff link, 2026-08-28) | Has the fix (Avi's diff link, 2026-08-28) |
| `MAM-basics/in/mam-ws/` (local copy) | Has the fix — זֵ֣רוּ | **Does not** — יְהוֹשֻׁעַ֙, one pashta |
| `MAM-parsed/plain/` | Has the fix | **Does not** — same, one pashta |
| mgketer's own parsed JSON | Has the fix — confirms it | Does not — but see below, this is expected regardless |

**Correction, 2026-09-03: the M34 column of the two middle rows above IS WRONG, and both stages
lacked the fix.** Measured that day while item 4 of the rollout programme ran, immediately before
the download: `MAM-basics/in/mam-ws/CK-Zechariah.json` held אֲשֶׁר־זֵ֣רוּ, the munaḥ on the
zayin, and `MAM-parsed/plain/CA-The-12-Minor-Prophets.json` still does. The fix is
the form אֲשֶׁר־זֵר֣וּ, the munaḥ on the resh, which is what this note's M34 row says the
ruling was — so the table names זֵ֣רוּ as "the fix" when זֵ֣רוּ is the form the fix replaced. The rows are
left as written, per the convention above, but read the M34 column of both as **Does not**.
The consequence is that Zechariah 2:4 propagates exactly as Joshua 10:12 does, and the sentence
below saying the download "is not just hygiene for Joshua" understates it: it was repair for
both. `PLAN-holman-meteg-rollout-programme.md`'s item 4 inherited the same error from this
table and now carries the measurement.

So Phase "download the chapters" in the larger rollout plan is not just hygiene for Joshua:
this repo's local Wikisource snapshot is genuinely stale there, and the standard pipeline
(wsgo diff, Google Sheet, mega) needs to run for Joshua chapter 10 before MAM-parsed reflects
Avi's correction.

## Ben's expectation, 2026-09-05: mgketer is not expected to ever agree at M24, even after the fix propagates

Ben's point, stated directly: the added pashta at Joshua 10:12 is a **stress helper** — MAM's
convention of repeating a postpositive accent's own codepoint to mark where the stress
actually falls (the same convention `hebrew-prose`'s terminology reference documents for
pashta, segol, telisha qetanah, telisha gedolah and deḥi; zarqa is the one exception, using a
different codepoint pair). Ben does not expect the Aleppo Codex, or mgketer's own reading, to
carry this helper at all — the helper is a MAM notational addition, not a manuscript reading
mgketer inherits.

**Consequence for the rollout plan's later phases:** once the Wikisource fix propagates
through the standard pipeline into `MAM-parsed/plain/` (the rollout's Phase "download the
chapters" through the mega run), MAM's text at Joshua 10:12 will have TWO pashta marks where
mgketer's own scrape has one. At that point mgketer's comparison is **expected to show a new
diff at this word**, not silence — and that new diff is correct, not a regression or a sign
anything went wrong. It is the ordinary case of MAM adding a stress helper the source
manuscript does not mark, the same shape as any other MAM-adds-an-accent divergence.

**What this means for verifying Phase "refresh mgketer" of the rollout plan:** do not expect
Joshua 10:12 to go quiet the way the 30 meteg suggestions and Zechariah 2:4 do. If a new diff
card appears there after the refresh, read it, confirm it says what is expected (MAM has a
second pashta that mgketer/the comparison edition lacks), and leave it — it is not one of the
30 meteg suggestions and needs no suppression-list entry or further action. If mgketer already
shows a category or a suppression mechanism for stress-helper doubling generally (untested in
this session — worth checking mgketer's `py/python_modules/categorise_diff.py` category list and its
`py/python_modules/manual_suppressions.py`, both under
`../MAM-private/mgketer/`, for any existing pashta/stress-helper entries before assuming this
one is new), that would explain the shape rather than change the conclusion.

**Not verified in this session:** whether MAM's other stress-helper doublings (pashta, segol,
telisha qetanah, telisha gedolah, deḥi) already show up as routine, expected diffs throughout
mgketer's existing reports, which would corroborate Ben's expectation directly from the
data. Worth a quick check — grep
`../MAM-private/mgketer/out-reports/by-type/*.html` for a category naming stress helpers or
repeated accents — before relying solely on Ben's stated expectation.
