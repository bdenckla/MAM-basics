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

The shared MAM-with-doc renderer also renders the example edition.

The dataset is derived from [Miqra according to the Masorah](https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah#beginning)
at Hebrew Wikisource, prepared by Seth (Avi) Kadish with technical assistance from
Erel Segal-Halevi and Benjamin Denckla. See [LICENSE.md](LICENSE.md).
