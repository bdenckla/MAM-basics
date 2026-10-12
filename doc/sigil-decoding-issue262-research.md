# Issue 262: internal qualifier-scope clarification

State: live; public-guide synchronization requires separate approval

Recorded by Codex on 2026-10-12 against MAM-basics
`c1f569a6e1137e37d80f7146d0cd366e49f5eb6b`, after reading the issue body and all six
comments on [#262](https://github.com/bdenckla/MAM-basics/issues/262).

This is an internal research supplement to [sigil-decoding.md](sigil-decoding.md),
especially the passage beginning **"The restriction to these two qualifiers still
stands, but as pending rather than settled."** That passage awaits answers which
have now arrived. The supplement records those answers without changing decoder
behavior, source notes, datasets, editions, the guide's table or public HTML.

## What the discussion settles

The [first answer](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5440221283)
confirms the meanings and distribution of מסורת and מסורות, the missing comma in
Isaiah 56:10's לד, and ד as the Venice Miqra'ot Gedolot. Those answers are already
in the guide. The eight-sigla pass and the ב2 to ת451 update also stand;
this task does not reopen them.

The [worked-example question](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5442563836)
distinguished sharing a qualifier over an entire comma list from attaching it only
to the adjacent sigil. Avi's [worked-example answer](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5443100250)
explicitly reports inconsistency. Its numbered answers establish these local scopes:

| Site and clause in the question | Confirmed scope | Justified local count | Current committed note |
|---|---|---|---|
| Daniel 3:5, `ל,ב1,ש2-כתיב` | The cited ketiv is in all three manuscripts. | 3 ketiv attestations: ל, ב1 and ש2. The historical direct-only treatment credited ש2 alone. | Now `ל,ב1,ש2=` followed by the reading and a parenthesis identifying the ketiv spelling; the trailing qualifier has been removed. |
| Deuteronomy 28:30, `ל,ל1,ש,ש1,ק3,ו,ל3,ל9-כתיב` | The pointed ketiv is written thus in all eight manuscripts. | 8 ketiv attestations, one for each listed manuscript. The historical direct-only treatment credited ל9 alone. | Now the same eight-item list followed by `=`, with the ketiv identified inside the explanatory parenthesis. |
| Genesis 43:26, `במ"ק-ב,ק13` | The masora parva in both manuscripts has the cited note. | 2 masora qetannah attestations: ב and ק13. The direct-only treatment misses ק13. | The leading qualifier and two-item list remain in this form. |
| Deuteronomy 32:18, `ק3,ל-קטנות` | ק3 supplies the reading in its text; ל supplies the small-letter list at the back of the Leningrad Codex. | 1 small-letter-list attestation, on ל. Do not credit ק3 with a small-letter list. | The clause remains `=ק3,ל-קטנות ומ"ש`. |
| Psalms 84:4, `א,ל,ש1,ק-מ,ל-גדולות` | The four manuscript texts lack the large ק; the large-letter list of ל has it. Avi identifies a mistake in the old note and says he corrected it. | 1 large-letter-list attestation, on ל, supporting the large letter. The four manuscript-text readings support its absence. The repeated ל has two different roles. | The positive clause now cites `=ל-גדולות,קורן` for the large letter. Do not treat the old combined clause as five list attestations or as a list supporting absence. |

The source locations for that last column are `MAM-parsed/plus/F1-Daniel.json`
(3:5), `A5-Deuter.json` (28:30 and 32:18), `A1-Genesis.json` (43:26), and
`D1-Psalms.json` (84:4), under each file's `book39s[0].chapters` mapping. These
files were read without edits. The column records current local evidence; it is
not a Wikisource refresh or a claim that every live revision has been mirrored.

## Counts and generalizations that remain unresolved

The three distributive examples justify local counts of 3, 8 and 2. Relative to
direct-only counting of the clauses quoted in the question, their increments are
2, 7 and 1 respectively. These are site-level differences, not new totals for the
guide's qualifier rows. In particular, the first two current clauses no longer
contain the hyphenated כתיב qualifier which the guide's counting method searches.
Adding their historical increments to a current syntactic census would mix two
populations.

The small-letter and large-letter examples justify one list attestation each;
their scopes do not justify distributing those qualifiers over the preceding
manuscript sigla. Psalms 84:4 also requires keeping the positive list evidence
distinct from the negative manuscript-text evidence.

The worked-example reply does not establish a general parsing rule for all nine
remaining qualifiers or all occurrences of כתיב, קרי or מ"ק. It does not separately
answer the longhand-equivalence control or the sentence-comma control. Keep those
generalizations unresolved, rather than replacing the guide's restriction with
universal distribution. The earlier broad "same idea" answer must be read with
the later explicit statement of inconsistency and the individual worked answers.

For Genesis 43:28, the discussion continues after the worked-example answer:
Avi [first reports a clarification](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5443149866),
then [reports a complete rewrite correcting it](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5444189440),
then links a [final touch](https://github.com/bdenckla/MAM-basics/issues/262#issuecomment-5444223726).
These later comments supersede relying on the first clarification as final.
The current local note no longer has the old `-כתיב` / `-קרי` clauses, but still
has `ל,לו,ק3=` in the ketiv explanation and `ל,ל1,ק3=` in the qere explanation.
The comments themselves do not explicitly decode לו as ל1 or ל,ו. Do not add an
alias, repair the corpus, or count a fourth manuscript from that unresolved spelling.

## Public synchronization worklist

[MAM-with-doc/README.md](../MAM-with-doc/README.md) identifies
`gh-pages/MAM-with-doc/sigil-decoding.html` as a manually maintained public subset
of `doc/sigil-decoding.md`, with no automatic Markdown renderer. The Pages workflow
uploads `gh-pages/` directly. Because this task excludes published changes and
their generation, the existing guide and HTML remain unchanged; this internal
supplement is not an input to their generators.

With separate approval for public-guide synchronization:

1. Replace the stale pending-confirmation passage with the five local answers,
   preserving the unresolved general rule and the two unanswered controls.
2. Re-derive affected qualifier cells against one declared current corpus and
   counting population. Verify the existing cells before changing them; distinguish
   hyphenated-compound occurrences from semantic attestations in revised notes.
3. Preserve the one-list scopes of קטנות and גדולות and the corrected direction of
   the Psalms 84:4 evidence. Treat Genesis 43:28's spelling as unresolved unless the
   final source revision supplies explicit evidence.
4. Reconcile the public subset manually and inspect the resulting HTML diff.

No new siglum identity, universal qualifier-scope rule, revised table total,
source-data correction or public-page update is adopted here.
