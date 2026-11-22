# Updates to the evaluation of the English translation of the Introduction to MAM

State: open, first entry 2026-11-22.

## 2026-11-22: the assembler's note on appendices-8 was wrong

Recorded by Claude (Opus 5.5), after Ben corrected it.

**Effective base State:** completed 2026-11-22; not yet acted on.

The base's finding `appendices-8` ends with a note headed "Assembler's correction, 2026-11-22",
which says of `hcanat.us`: "It is a real host that serves the same UXLC tree, the download host
that this repository's `py/uxlc_misc/my_uxlc.py` names as `UXLC_DOWNLOAD_HOST`, so the links
work, and the finding is minor." That conclusion was wrong. Ben, 2026-11-22: "we are trying to
stamp out all uses of hcanat.us from all MAM-related stuff. It is a dev server." On 2026-11-06 he
had asked "to fix all hcanat.us to tanach.us", and `7f43a3c8` did so on seven pages of the Hebrew
introduction, recording `hcanat.us` as the UXLC's development host and `tanach.us` as its public
site. So:

1. The finding stands as the evaluator wrote it. It is substantive again, and its suggested
   tweak is right: point all four links to `https://tanach.us/Tanach.xml`, as the Hebrew does.
   Those links name the whole XML file, which `738dae4e` of 2026-11-20 keeps as XML; only verse
   links take the HTML view, as the next entry says.
2. The base's opening says that one finding "failed its check and is corrected in place, marked
   as the assembler's correction". No finding failed its check. The assembler's check was the
   one that failed.
3. The base's table, "Findings by slice", gives the Appendices 13 substantive findings and 28
   minor, and all slices 70 and 172. With `appendices-8` restored, the Appendices have 14 and
   27, and all slices 71 and 171.

## 2026-11-22: one verse link in the old form, which the evaluation missed

Recorded by Claude (Opus 5.5), from Ben's question the same day about the move to tanach.us URLs
that need no XSLT.

Since `738dae4e` of 2026-11-20, this repository's reader-facing links to a UXLC verse use
tanach.us's HTML view, which `uxlc_verse_url` in `py/mb_cmn/uxlc_verse_url.py` builds, as in
`https://tanach.us/Tanach.html?Job4:12-4:12`. The older form links the XML file with a query, and
a browser renders it through XSLT. One link on the seven English pages has the older form, and
the base has no finding for it:

1. **ch3b-37. The inverted-nun link uses the XSLT view** (markup, minor). English: Scribal
   Tradition in the Torah: Anomalous Letters, under the inverted nun, text line 560, the link
   "In the Leningrad Codex (the Westminster transcription)", whose target is
   `http://tanach.us/Tanach.xml?Num10:1-10:36`. Hebrew: ch3.mediawiki:369, which has the same
   link. The link works, but it is the form that this repository has replaced, and it is plain
   http. **Suggested tweak:** `https://tanach.us/Tanach.html?Num10:1-10:36`, which follows
   `738dae4e`'s form for a range of verses; nobody has opened it in a browser yet.

With it, slice `ch3b` has 37 findings, 10 of them substantive, and all slices 243, 71 of them
substantive.

The Hebrew introduction, as the mirror holds it at revisions no later than 2026-11-07, has eight
verse links of the older form: ch1.mediawiki:260, ch2.mediawiki:128, ch3.mediawiki:33, 369 and
1358, and ch5.mediawiki:262, 851 and 867. `py/ws/ws_bot_edit_history.md` records no bot run that
changed them. They are outside this evaluation of the English, which records them here only
because the English copies one of them.
