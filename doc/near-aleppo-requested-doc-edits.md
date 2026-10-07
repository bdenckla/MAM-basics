# A96
Regarding "Where near-Aleppo's text of a note's target differs from MAM's, the preserved note body remains about MAM's text",
is that true any more?
I thought we/you just did a huge sweep to alter MAM's notes so that they remained true,
not so that they remained literally the same, since remaining literally the same
makes them false in many cases.

# A97
Remove:
====
Both U+0598 HEBREW ACCENT ZARQA and U+05AE HEBREW ACCENT ZINOR, which in a poetic verse are the tsinnorit and the tsinnor, two accents that the codex tells apart.
====
(I don't like the way it is written, but I also don't think the message it is trying to express is worth noting,
so please remove it.)

# A98
Remove "for it records where the codex puts the dot, not merely a spelling".
That is a wild assertion about the manuscript that I am unwilling to make,
and I'm not sure what I would have said that made you think I was willing to make that assertion.
====
U+05BA HEBREW POINT HOLAM HASER FOR VAV wherever MAM has it, all 416 of them, for it records where the codex puts the dot, not merely a spelling
====

# A99
Remove:
====
U+05AD HEBREW ACCENT DEHI, which MAM has for the deḥi of a poetic verse, all 2,679 of them; near-Aleppo has 2,681 in all, the others coming with readings of the codex.
====
Why on earth would it be notable that near-Aleppo preserves MAM's dexi marks?
Or, to put it another way, why on earth would we have removed them?

# A100
Remove
====
U+0596 HEBREW ACCENT TIPEHA for both the tipeḥa and the tarḥa, as MAM has it.
====
Not notable and not specific to MAM.
This is just the way to encode tarxa in Unicode, so no need to record that, basically
"we continue to use Unicode correctly in near-Aleppo, as we do in MAM-basics"

# A101
Correspondingly to removals above, remove this example:
====
For example, at Psalms 40:13, both datasets have:

עֲ֭וֺנֹתַי

The deḥi (U+05AD) and the holam haser for vav (U+05BA) are retained.
====

# A102
Remove the entire “The sparseness of the ketiv/qere” row from the limitations
table in `gh-pages/near-aleppo/coverage-and-status.html`, through its generator
in `py/near_aleppo/doc_registers.py`.

The passage refers to trivial qere and should have named it explicitly.
More fundamentally, its claim is false: MAM now explicitly encodes the qere
of trivial qere, and the near-Aleppo dataset retains that information.

The near-Aleppo edition displays trivial qere as a documentation note.
That is a display convention, whereas this discussion concerns fundamental
limitations of the dataset. Delete the row without replacing it with a
display limitation.
