# Updates to the Koren meteg-after-silluq lookup candidates

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/meteg-after-silluq-koren-lookup-candidates.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written. A correction or later disposition goes in a
sibling file named `<stem>-update.md`, which is what this file is for that report.

## Finding 11.4: the two possession verbs should read “has”

Recorded by Codex on 2026-09-12. Both cited sites are the report's analytic prose rather than
protected quotations. In the section “Syllables after the stress in Phonetic MAM, the basis of
the syllable verdict,” the paragraph beginning “Two readings of a deḥi as the stress” should be
read with these two corrections:

1. The phrase “At Psalms 4:3 MAM writes one deḥi” should read “At Psalms 4:3 MAM has one deḥi”.
2. The clause “MAM-simple carries no deḥi stress helper anywhere” should read “MAM-simple has no
   deḥi stress helper anywhere.”

The finished Koren-candidates report remains unchanged. The corrections replace only the two
possession verbs and do not change either claim.

## Finding 11.5: narrative `hataf` should read `ḥataf`

Recorded by Codex on 2026-09-13. A fresh census of the finished Koren-candidates report found 10
plain-`hataf` sites on five lines. The corrected readings are:

1. In the opening decision **Syllables are counted the Masoretic way**, all three `hataf` sites
   should read `ḥataf`.
2. In section 2's **Syllable verdict** item, both `hataf` sites should read `ḥataf`.
3. In section 2's **Sheva after the first mark** item, `hataf` should read `ḥataf`.
4. In section 2's **Twin evidence** item, both `hataf` sites should read `ḥataf`.
5. In the paragraph beginning “Over all 263,320 chanted words of Phonetic MAM,” both `hataf`
   sites should read `ḥataf`.

The identifier path `py/explicit_xataf/extract.py` remains as written because file paths and
code identifiers retain the ASCII-oriented spelling `xataf`. The finished Koren-candidates
report's substantive bytes match historical blob `51dfa981efc871449cee7830b294389e5ecb7dbf`;
its only additional line is the authorized update pointer.

## Koren lookup status when the inquiry ended on 2026-09-20

Recorded by Codex on 2026-09-20. Ben ended the lookup sequence with this instruction: “I'm
discontinuing this particular line of inquiry; record what we have (if it hasn't been recorded,
or hasn't been recorded in git-tracked form)”.

The tracked `in/meteg_after_silluq_koren_readings.json` now has 28 fully classified Koren
observations: the 11 already present when the finished report was generated and the 17 added on
2026-09-20. The three formal values remain relative only to MAM's two U+05BD positions. A Koren
metsil somewhere else is recorded separately and does not make a `last` observation `both`.
None of the 17 additions is `first`, so none is a new signal for silluq followed by meteg in MAM.

The added formal observations are:

- **2 Kings 22:1 — `last`; `sheva` is `silent`.** Koren also has qamats qatan under ב, where MAM
  has qamats gadol. Ben subsequently found that the Simanim Tanakh agrees with MAM on both
  qualities: qamats gadol under ב and vocal shewa under צ.
- **Jeremiah 33:21 — `both`; `sheva` is `vocal`.**
- **Ezekiel 37:9 — `both`; `sheva` is `silent`.** With the later metsil as silluq, the earlier
  metsil is meteg on the closed syllable ending at ח.
- **Psalms 60:9 — `both`; `sheva` is `vocal`.** MAM's varika suffices to identify the shewa as
  vocal, while Phonetic MAM supplies the explicit vocal-versus-silent classification.
- **Daniel 3:14 — `both`; `sheva` is `vocal`.**
- **Daniel 3:28 — `both`.** No relevant simple sheva follows MAM's earlier U+05BD.
- **Daniel 5:6 — `both`; `sheva` is `vocal`.**
- **Daniel 5:12 — `both`.** The following ח has ḥataf pataḥ rather than a simple sheva.
- **Nehemiah 7:52 — `both`; `sheva` is `vocal`.**
- **Nehemiah 12:22 — `last`; `sheva` is `silent`.** Koren also has pataḥ under פ where MAM has
  qamats.
- **1 Chronicles 4:30 — `both`; `sheva` is `vocal`.**
- **Genesis 6:19 — `both`; `sheva` is `silent`.** With the later metsil as silluq, the earlier
  metsil is meteg on the closed syllable ending at ה.
- **Isaiah 1:18 — `both`; `sheva` is `silent`.** With the later metsil as silluq, the earlier
  metsil is meteg on the closed syllable ending at ה.
- **Jeremiah 25:33 — `both`; `sheva` is `silent`.** With the later metsil as silluq, the earlier
  metsil is meteg on the closed syllable ending at ה.
- **Numbers 23:26 — `both`.** The following ע has ḥataf segol rather than a simple sheva.
- **Numbers 5:18 — `both`.** Koren also has a metsil on the initial ה, a vocal simple shewa under
  מ, and ḥataf pataḥ under the first ר where MAM has varika-sheva. The JSON deliberately has no
  `sheva` field here: immediately after MAM's earlier U+05BD, Koren has ḥataf pataḥ rather than a
  simple sheva.
- **Daniel 3:6 — `last`; `sheva` is `vocal`.** Koren has another metsil on י, which is outside
  MAM's two U+05BD positions. Koren therefore has two metsils in total but only MAM's later one.

Ben's fuller observation at Numbers 5:18 was:

> Koren's last metsil is, like MAM's under the last resh (ר) of the word, but Koren's pointing
> differs in a few ways that I think are not relevant to our investigation, but still worth
> recording.
>
> On each letter, parenthesized, assuming silluq last, Koren's pointing is (patax, meteg), (vocal
> simple shewa), (qamats, meteg), xataf patax, (xiriq, silluq).
>
> I think the differences boil down to: Koren has an extra meteg (on he) (not surprising due to
> Koren's meteg-heavy policies), and Koren has an explicit xataf patax on resh instead of MAM's
> more implicit varika-shewa.

Ben tentatively grouped Ezekiel 37:9, Genesis 6:19, Isaiah 1:18 and Jeremiah 25:33 as forms with
meteg on a closed syllable involving roots with yod-he or yod-ḥet. Ben did not recall the full
root definition and presented the association tentatively. This update records that grouping
without establishing or refining it. After Jeremiah 25:33, Ben decided to stop checking further
candidates of that type. Ezekiel 34:26, rank 27, was therefore left uninspected and has no formal
Koren classification.

Three other boundaries remain important:

1. **1 Samuel 21:7 remains formally unresolved between `last` and `both`.** Ben found Koren's
   later metsil on ח, agreeing with MAM and ruling out the post-silluq signal, but did not report
   whether Koren also has MAM's earlier U+05BD. The partial observation is not forced into the
   three-value JSON field.
2. **Genesis 11:6 remains uninspected and formally unclassified.** Ben questioned whether its
   earlier U+05BD was a plausible silluq position. The broad ranking admitted the candidate
   because only one Masoretically counted syllable follows that position, but the narrower corpus
   evidence strongly favors final stress: 174 of 175 exact mid-verse twins, all 8 atnaḥ twins,
   all 14 verse-final one-mark twins and all 48 suffix twins stress the final syllable. The sole
   exact earlier-position twin is Psalms 40:9, לַ֥עֲשׂוֹת־רְצוֹנְךָ֣, where the merkha on לַ is a
   secondary accent and the compound's primary stress is on final רְצוֹנְךָ. A corpus query found
   no verse-final MAM case combining primary penultimate stress on pataḥ with a final ḥolam
   syllable in the current Phonetic MAM snapshot. Genesis 11:6 was removed from the active lookup
   sequence without assigning a Koren classification.
3. **Daniel 3:11 and every later candidate remain uninspected and unclassified.** Daniel 3:11
   had been displayed as the next candidate, but Ben ended the inquiry before reporting a Koren
   observation there.

The finished base report remains unchanged. A validation run of its untracked writer, redirected
to an untracked output, confirmed the expanded JSON against the original analysis without
overwriting the finished report.
