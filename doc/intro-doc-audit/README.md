# Cached Introduction and documentation-note audit

State: live research; isolated branch, no integration scheduled

This audit uses the repository snapshot at `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`.
It changes no Scripture input, edition, published page, or manuscript interpretation.
`source-pin.json` preserves exact Git objects and the current full bodies/comments of
MAM-basics #305–307. `topics.json` covers all thirteen Introduction cache pages;
`claims.json` preserves every nonblank source unit with its topic and source pointer.
Source units include table cells and navigation: their count is not a semantic claim count.

The first inventory contains 340 titled spans, 8,984 source units, and 1,643 units
with explicit canonical verse links. Those units produce 3,125 verse-evidence joins;
2,608 joins have documentation notes, and four link targets name nonexistent verses.
The complete chapter walk discovers 3,905 notes. Four further note copies are in
good-ending metadata outside that walk; their locations are recorded in `summary.json`.
These are research census figures, not a consistency verdict.

Run from the isolated worktree root with the home clone's interpreter:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_intro_doc_audit.py
```

The script lowers its own process priority, reads the 24 parsed book files
sequentially, and writes only this research directory. It uses the current
`explicit_xataf.extract.find_docnote_tmpls` closed inventory, the current sigil
inventory's visible-note renderer, canonical book and Hebrew numeral maps, and
the existing verse-link builders. Sigil meanings and operators come from
`doc/sigil-decoding.md`; `!=` means surprising equality, and a leading `=` has
MAM as its implicit subject. A bare “in the manuscript” does not supply Aleppo
attribution. Structured note targets without the existing survey's text projection
remain complete nodes with an explicit projection limitation.

Hebrew quotation fields are copied directly from source files. Nothing normalizes
the captures. Literal form search and MAM-order comparison are separate triage
categories; neither proves that the named source supports the matched form.
`form-triage.json` is internal routing data, not an alarm list. Source chronology,
the exact source relation, annotation scope, and any disagreement must be reviewed
before assigning a semantic result. Introduction transclusions remain unexpanded
and are explicitly counted. No live Wikisource request was made.

The HTML review, semantic dispositions, coverage routes, and uncertainty queue are
being added in subsequent manageable batches. Existing issues #305–307 will remain
separate from newly validated discrepancies. No issues or comments will be posted.
