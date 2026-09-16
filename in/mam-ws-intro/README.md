# Local mirror of the MAM Wikisource introduction

Read this reference before using or refreshing the mirror in this directory.

## The MAM introduction is mirrored at `in/mam-ws-intro/` — read it, do not fetch it

Hebrew Wikisource's introduction to MAM is consulted constantly here, and since 2026-08-31 all
thirteen of its pages are mirrored locally as verbatim wikitext, one `.mediawiki` file each.
Refresh with `.venv/Scripts/python.exe py/main_download.py fr-ws-intro`, which is deliberately
**separate** from `fr-wikisource` (Ben's decision, 2026-08-31): the books and the introduction
have unrelated refresh rhythms, and nothing downstream reparses when the introduction moves.

| File under `in/mam-ws-intro/` | Wikisource subpage |
|---|---|
| `root.mediawiki` | the introduction's root page |
| `summary.mediawiki` | `/תקציר` |
| `ch1` … `ch5.mediawiki` | `/פרק א` … `/פרק ה` |
| `appendices.mediawiki` | `/נספחים` — the sigil roster `doc/sigil-decoding.md` leans on |
| `index-aleppo.mediawiki` | `/מפתח לכתר ארם צובה` |
| `index-leningrad.mediawiki` | `/מפתח לכתי"ל` |
| `westminster-typing.mediawiki` | `/מידע טכני על הקלדת וסטמינסטר` |
| `data-sheet-guide.mediawiki` | `/מדריך טכני לגיליון הנתונים` |
| `technical-guide.mediawiki` | `/מדריך טכני` |

Three things about it are worth knowing before you touch it:

1. **Never summarize-fetch these pages, mirror or no mirror.** That is what the mirror is for.
   `doc/sigil-decoding.md`'s source #1 records what a summarizing fetch did to the sigil roster
   on 2026-08-06, and the mirrored wikitext is where you can see what it flattened.
2. **This tree is exempt from the mark-order rule at the top of this file.** It is hand-authored
   wiki prose, so clusters in Unicode-normal rather than MAM-normal order are what the source
   says, not defects. Do not run `uni_check` or `has_std_mark_order` over it, and never
   normalize on refresh — the files are byte-verbatim by design.
3. **A mirror goes stale in a way `in/mam-ws/` does not.** The books move when Ben edits them;
   the introduction moves when Avi Kadish does, unannounced — five of the thirteen pages were
   edited in August 2026 alone (the committed manifest's count; this said four until 2026-09-01,
   from a drafting-time fetch predating the month's last two edits). `manifest.json` beside the
   pages records each one's revision id
   and timestamp, so staleness is checkable without a network call.

**`index-aleppo.mediawiki` and `index-leningrad.mediawiki` are hand work, and nothing in this
repository generates them.** Each page began as wikitext from a one-off generator. Ben,
2026-08-31: those generated files "were only ever intended to be starting points for manual work
on Wikisource." The published pages are that manual work. On Ben's decision of 2026-09-10 both
generators and their outputs were removed from the repository — they "will never be run again"
— so there is no generated form left to compare a mirrored page against. Phase 3 of
`doc/PLAN-mega-coverage.md` names every file removed, and git history keeps them.

Measured before the removal, **26 (4%)** of the Aleppo generator's 700 lines survived into the
live page, and **94 (8%)** of the Leningrad generator's 1,135. The `aleppo/aleppo-wiki/` tree
also keeps two snapshots of the hand work itself, `Wikisource-manual-initial.txt` (63 lines,
carrying `{{בעבודה}}`) and `Wikisource-manual-final.txt` (713 lines, **97%** of whose lines are
in the live page) — which is the pipeline written down: generate raw material, then build the
page by hand from it. The generated Aleppo file's overlap with the hand-made line was the same 26
lines whether measured against the initial snapshot, the final snapshot or the live page, so the
hand work left the generated form immediately and never went back to it. No snapshot of the
Leningrad hand work was kept.
