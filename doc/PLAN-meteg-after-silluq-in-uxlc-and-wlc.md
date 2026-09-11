# Survey the verse-final chanted words where UXLC or WLC has a U+05BD later than MAM's last

State: live. Proposed 2026-09-10 at Ben's request; nothing run. Ben asked the same day for it to be run at once, by a session of its own started from a task chip.

## Why this plan exists

Ben, 2026-09-10, after Psalms 72:15 turned up with a U+05BD in UXLC 3.9 later than the one MAM has: "perhaps record somewhere (as its own plan or an addition to a yet-to-be completed, related plan) the desire to do a more complete run for verse-final words in which UXLC or WLC (using a Unicode version of WLC) has a meteg/silluq later than MAM's last meteg/silluq on that word." This file was written by a Claude session the same day, in the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c` on the branch `claude/interesting-taussig-6aa52b`; everything below Ben's quotation is that session's reconstruction.

It is a plan of its own because no unfinished plan fits it. `doc/PLAN-silluq-before-gaya-template.md`, the one live plan on the subject, adds a template to MAM's text; `doc/PLAN-post-stress-meteg-page-and-holman-m23.md` was executed on 2026-09-04.

Terms, as the `hebrew-prose` skill defines them: an **atom** is one written word between spaces or maqafs, and a **chanted word** is a lone atom or a whole maqaf compound. **Meteg** is U+05BD; **silluq** is the U+05BD on the stressed syllable of a verse-final chanted word. A **position** is a letter ordinal within the chanted word, maqafs not counted, as in the screen named below.

## What is already known, and why it is not the complete run

1. **The screen of MAM against UXLC 3.9 and WLC 4.22 looked mainly the other way.** `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` (2026-09-09) was built to find verse-final chanted words where MAM has a U+05BD later than the last U+05BD both sides share, its class (iii). Its class (v) is the reverse, with 4 members against UXLC 3.9 and 3 against WLC 4.22: 1 Samuel 17:5, 1 Kings 14:14 (against UXLC 3.9 only), Psalms 70:2 and Psalms 72:15 (its section 4). The screen listed them and did nothing more with them.
2. **Class (v) is not the run Ben asked for, for two reasons.**
   1. The screen assigns its classes in the priority (iii), (v), (iv), (i), (ii), (vi), (vii), so a chanted word where both MAM and the source have a U+05BD beyond the last common one lands in class (iii) and never in class (v). Proverbs 31:28 is the one such word (that file's section 11, item 4).
   2. Its class (iv), no common position at all, holds chanted words whose only U+05BD in the source is later than MAM's; Judges 9:2 is one (that file's section 5).

   Ben's criterion compares MAM's last U+05BD with the source's last U+05BD directly, so neither exclusion applies to it.
3. **The post-stress-meteg survey's post-silluq page treats one verse of the Leningrad Codex.** `gh-pages/post-stress-meteg-post-silluq.html` is about 1 Samuel 17:5, with crops of the Leningrad Codex and the Aleppo Codex; the survey's count of post-silluq metegs (`post_silluq` in `py/accgram/post_stress_meteg.py`) is of MAM's side only.
4. **Psalms 72:15 was looked at on its own on 2026-09-10**, in `doc/meteg-after-silluq-psalms-72-15.md`. Ben confirmed from an image of the Leningrad Codex the same day that it has both strokes there, and from mgketer.org's image of the Aleppo Codex that it has only the one under the kaf, so that calibration case is a fact about the manuscript and not only about the transcriptions.

## The run

1. **Inputs, as in the screen** (its section 11, item 1): MAM from `MAM-simple/json-vtrad-bhs` through `accgram.mam_simple_verse`; UXLC 3.9 from `in/UXLC-39/*.xml`; WLC 4.22 from its Unicode conversion `out/wlc422-u/`, with `out/wlc420-u/` as a second run; all keyed by WLC's compact bcv. The screen's throwaway `.novc/mas_b_screen.py`, in the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`, already loads and aligns all three. It was there on 2026-09-10, but it is gitignored and may be gone; the screen's section 11 is the method of record.
2. **The verse-final chanted word and the alignment, as in the screen**: the last atom holding sof pasuq plus every atom maqaf-joined to it; a verse whose verse-final chanted words differ in letters is compared by its final atom when only the grouping differs, and is otherwise skipped and counted.
3. **The criterion, Ben's**: a hit is a verse-final chanted word whose last U+05BD in the source is at a later position than MAM's last U+05BD, or which has a U+05BD in the source and none in MAM.
4. **Every hit is put in one of three classes**, using positions and syllables counted the Masoretic way (the screen's section 1, finding 2):
   1. The source also has a U+05BD at MAM's last position. The source then has a U+05BD after the one MAM takes as its silluq; these are the candidates for a meteg after the silluq in the transcription.
   2. The source has no U+05BD at MAM's last position. The source's last U+05BD is then on a later syllable than MAM's, which is a difference in where the silluq is, not a meteg after it.
   3. MAM's last U+05BD is itself a meteg after the silluq: 1 Kings 7:37, and Job 4:12 if its stress is penultimate (`doc/meteg-after-silluq-job-4-12.md`). These are flagged rather than classed by MAM's last position.
5. **Calibration**: the hits must include 1 Samuel 17:5 and Psalms 72:15 against both UXLC 3.9 and WLC 4.22, and 1 Kings 14:14 against UXLC 3.9, each in the first of the three classes; the script raises otherwise.
6. **Output**: a tracked findings file, `doc/meteg-after-silluq-in-uxlc-and-wlc.md`, with every hit, its class, both sides' forms lifted from the data, and the command that re-establishes each figure. Not a rendered page unless Ben asks for one.

## Rules for the run

1. Load the `hebrew-prose` skill before writing the findings file.
2. A claim about the Leningrad Codex made from UXLC or WLC is written as "UXLC 3.9 records" or "WLC 4.22 records"; this run does not consult the manuscript. Looking at the Leningrad Codex's images for the first class is a follow-up for Ben, who reads them himself: give him links, not downloaded images, namely Sefaria's image of the folio with the atom's estimated column and line and tanach.us's page for the verse, built by the user-level `verse-links` skill.
3. Where a meteg stands relative to its vowel plays no part in the run: Ben judged it scribal whim on 2026-09-10, and his later finding that day, that the two codices agree on an early stroke at Job 4:12, is raised in `doc/meteg-after-silluq-job-4-12.md` section 4 rather than here. Positions are letter ordinals, and the order of the marks on a letter, including UXLC's U+034F coding of a leading meteg, plays no part.
4. Pointed Hebrew in the findings file is lifted from the data by script and checked with `mb_cmn.uni_denorm.has_std_mark_order`, because the Write and Edit tools put Hebrew into Unicode-normal order.

## Preconditions, and what is not expected to change

1. Re-measure the screen's class (v) before relying on it: run `.novc/mas_b_screen.py` from the root of the worktree named in step 1, or read the `mas_b_screen_results.json` it writes there, and expect 4 members against UXLC 3.9 and 3 against WLC 4.22. A mismatch is a finding.
2. Work in a secondary worktree of `C:/Users/BenDe/GitRepos/MAM-basics` whose branch contains this plan. On 2026-09-10 that was the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c` on the branch `claude/interesting-taussig-6aa52b`, which another session shared, so commit there with named paths only. Run `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, and set `$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"` for anything that reads MAM-private, which holds Phonetic MAM.
3. Nothing tracked changes but the new findings file: MAM's text, the screen's file and the post-stress-meteg pages are left alone.
4. Commit the findings file on the worktree's branch. While that branch is shared with other sessions it is integrated once, when its work ends, at Ben's word, and not at this run's archival; once it has been merged into `main`, the user-level four-step procedure applies as usual.
