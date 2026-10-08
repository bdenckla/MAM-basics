# near-Aleppo dataset

This is a version of MAM-parsed-plus whose Scripture text is nearer to the Aleppo
Codex's body text. It includes reviewed near-Aleppo note clauses and distinguishes
MAM's original targets from changed near-Aleppo targets. It is structured data: use the closed,
role-aware template rules in each book's consumer notice.

The changed-note templates are `נוסח עם הקשר מקרא על פי המסורה` and
`הערה-2 עם הקשר מקרא על פי המסורה`. Parameter 1 is the near-Aleppo target;
parameter 2 is its reviewed clause, or an empty array. `מקרא על פי המסורה`
holds the original structured MAM target, and `הערת מקרא על פי המסורה`
holds the remaining original clauses or the complete source body. The book
JSON contains the note transformations: consumers need no review-ledger lookup.
Display formatting remains the consumer's choice. Original source notes and
review reasoning remain in MAM-parsed-plus and the public review ledger.

Artificial carriers are not ketiv consonants. GA and GV keep their existing
meanings and prohibit dagesh. The no-space template `ניקוד בלי אות ובלי רווח`
licenses only `carrier=final-nun-dalet`, with DALET + DAGESH + TSERE + MAHAPAKH
(GD), immediately after the final nun at Isaiah 54:16. All three marks remain
associated with that nun, and the whole qere is preserved. This first final
carrier case is a font accommodation; earlier carriers were initial or medial.
It makes no claim of ownerless manuscript marks.

The 24 book files are in `plus/`. The example edition and documentation are in
`gh-pages/near-aleppo/`. The build reads local MAM-parsed-plus, the Aleppo coverage
index, and the runtime inputs in `in/near-aleppo/`. The research archive and
approval records are retained separately in MAM-private.

From the repository root:

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py
```

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --check
```

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --check-note-review
```

The first command regenerates the five-instrument MAM census, then the dataset,
its population file `in/near-aleppo/build-populations.json`, and the HTML. The
checks fail on unknown template variants, changed pointing guards, populations
that disagree with the census, or unreviewed note presentations. No private
repository or scan archive is a build dependency.

The shared MAM-with-doc renderer also renders the example edition. Near-Aleppo
selects ketiv as the primary text, using each stored pointed ketiv where available,
and shows pointed qere above it in an HTML ruby annotation at the same size,
with CLC's box around each pair and a small vertical gap between the forms.
The box has its own line height and vertical padding so the border clears marks
above and below the letters. Trivial ketiv/qere templates use their own pointed
ketiv and qere parameters. Missing
readings have the same editorial labels as CLC in the missing reading's position.
Existing notes remain beside the text; the ruby display does not synthesize qere
notes. Trivial-template qere source metadata is available on the annotation's hover.

The example edition's [features of interest](../../gh-pages/near-aleppo/foi/index.html)
start with [interesting ketiv/qere cases](../../gh-pages/near-aleppo/foi/interesting-ketiv-qere.html).
These selected examples show whole verses with the current edition's ruby
display. The BCV in each heading links to the verse in NAEE; relative links work
locally and on the website. The [qere-without-ketiv study](../../gh-pages/near-aleppo/foi/qere-without-ketiv.html)
adds current MAM notes, Ben's dated manuscript observations, and supplied crops.
Its [source note](../../doc/near-aleppo-qere-without-ketiv/README.md) identifies the
maintained records and crop provenance. Regenerate the FOI pages and images with:

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --html
```

The selection and explanations are maintained in
`py/near_aleppo/features_of_interest.py`. To print a verse's local and published
NAEE links from the current checkout, use, for example:

```powershell
./.venv/Scripts/python.exe py/main_verse_links.py 2Samuel 8:3 --near-aleppo
```

The offline final-punctuation review extract is
`review/ketiv-final-punctuation.html`, with a plain-text companion. It shows the
requested 42 maqaf cases and 12 pasoleg cases in separate sections, including
already-present punctuation, complete notes and neighboring verses. Psalm 10:5
uses the trivial ketiv/qere template's pointed ketiv and qere parameters.
Each section is sorted by MAM's book order, then numeric chapter and verse,
interleaving added and already-present cases.
The selection is tracked in `in/near-aleppo/final-punctuation-review-selection.json`;
`py/near_aleppo/punctuation_review.py` renders it from the current edition data
and shared renderer. Reproduce it from the repository root:

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --punctuation-review
```

Append `--check` to regenerate in memory and compare both tracked review files.
The HTML embeds the edition font, its notices and license, styles, exact rendered
text and input selection; it needs no network access. The unchanged font's source
package and notices remain in `in/font-support/taamey-d-0.921/`.

The dataset is derived from [Miqra according to the Masorah](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning)
at Hebrew Wikisource, prepared by Seth (Avi) Kadish with technical assistance from
Erel Segal-Halevi and Benjamin Denckla. See [LICENSE.md](LICENSE.md).
