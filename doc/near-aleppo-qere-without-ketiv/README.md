# Near-Aleppo qere-without-ketiv manuscript readings

State: live

The maintained study is generated at
[`gh-pages/near-aleppo/foi/qere-without-ketiv.html`](../../gh-pages/near-aleppo/foi/qere-without-ketiv.html).
It is linked from the near-Aleppo FOI index and the existing ketiv/qere guide.
Ben approved this first draft on 2026-10-08: “what you propose seems fine, at least as a first draft.”
Implementation and further discussion of the readings proceed together.

## Maintained inputs and rendering

[`in/near-aleppo/qere-without-ketiv-readings.json`](../../in/near-aleppo/qere-without-ketiv-readings.json)
owns the selected references, Ben's dated image observations, their qualifications,
and crop provenance. Update that file as Ben supplies further readings or revises
an assessment. A case without an image reading has `reading`, `observation`, and
`crop` set to `null`; the page states that an image reading has not yet been recorded.

[`py/near_aleppo/foi_qere_without_ketiv.py`](../../py/near_aleppo/foi_qere_without_ketiv.py)
renders the study through the existing HTML build. The shared renderer supplies
current NAEE Scripture from `out/near-aleppo/plus/`, and current qere and attached
MAM doc-notes from `MAM-parsed/plus/`. It owns closed template dispatch. The FOI
selects semantic qere-only render elements and notes whose rendered lemma contains
that element; it does not interpret raw template parameters independently.

An image reading's subject is its whole recorded qere, including every letter
and mark. A changed current qere requires reconciling that reading's subject.
There are no input hashes or fixed-population gates. The dated Samuel comparisons
identify the MAM notes reviewed on 2026-10-08; their verbatim quotations remain in
the reading records even if the current notes later change.

The study's observations do not change the near-Aleppo source text or decide a
template design. Actual near-Aleppo source decisions remain in their existing
maintained inputs and procedures.

Run from the MAM-basics repository root in PowerShell 7:

```powershell
& "$HOME/GitRepos/MAM-basics/.venv/Scripts/python.exe" "$HOME/GitRepos/MAM-basics/py/main_near_aleppo.py" --html
```

The corresponding read-only comparison is:

```powershell
& "$HOME/GitRepos/MAM-basics/.venv/Scripts/python.exe" "$HOME/GitRepos/MAM-basics/py/main_near_aleppo.py" --html --check
```

## Crop provenance

Ben supplied and interpreted the following Aleppo manuscript crops on 2026-10-08.
Codex inspected the supplied crops. The canonical PNG files are under
[`in/near-aleppo/img/qere-without-ketiv/`](../../in/near-aleppo/img/qere-without-ketiv/),
and the HTML build copies their unchanged bytes under
`gh-pages/near-aleppo/img/qere-without-ketiv/` for inline display. These small crops
follow the established manuscript-crop fair-use convention recorded in
[`doc/meteg-after-silluq-snips/README.md`](../meteg-after-silluq-snips/README.md).
The supplied screenshot names identify the captures; no manuscript page, column,
or line coordinate is inferred from a screenshot filename.

| Entry | Canonical crop | Supplied screenshot |
| --- | --- | --- |
| Judges 20:13 | [aleppo-Ju20-13.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-Ju20-13.png) | `Screenshot 2026-10-08 105138.png` |
| 2 Samuel 16:23 | [aleppo-2S16-23.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2S16-23.png) | `Screenshot 2026-10-08 105548.png` |
| 2 Samuel 18:20 | [aleppo-2S18-20.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2S18-20.png) | `Screenshot 2026-10-08 110056.png` |
| 2 Kings 19:31 | [aleppo-2K19-31.png](../../in/near-aleppo/img/qere-without-ketiv/aleppo-2K19-31.png) | `Screenshot 2026-10-08 110419.png` |

## Judges 20:13

Ben read the below-marks of בְּנֵ֣י: sheva, tsere, and munaḥ, without letters or
dagesh, with space above the marks. The orphan marks are at the end of a manuscript
line. Ben's hypothesis is that the line ending may have provided that space,
possibly accidentally.

Ben also reported a masorah circle above the marks. The circle is documented but
not encoded in the written-form record. The standalone review used blank SPACE
anchors for the marks. Their count and width are display conventions, not
measurements of physical manuscript spacing or a proposed template design. The
record preserves that display text and its mark order as historical documentation.

## 2 Samuel 16:23

Ben read a fairly generous space even after the maqaf, with no pointing for
אִ֖ישׁ. The space is insufficient for the letters of איש, but ample for its
below-marks, ḥiriq and tipeḥa. Available room does not establish the marks as present.
Ben questions whether “narrow” fits the space described in the MAM note reviewed
on 2026-10-08. That dated quotation is stored in `reading.reviewed_mam_note`.

## 2 Samuel 18:20

Ben agrees with the MAM note reviewed on 2026-10-08. The tsere and merkha of
כֵּ֥ן are present below, between the surrounding written atoms, without the qere
letters or dagesh. In particular, no space lies above the marks. The dated MAM
quotation is stored in `reading.reviewed_mam_note`.

## 2 Kings 19:31

Ben read very generous spacing for צְבָא֖וֹת, with all its below-marks present:
sheva, qamats, and tipeḥa. Perhaps the qere letters could have fit. A ḥolam male dot
also seems to be represented. The letter-fit assessment and the dot reading remain
tentative; the record does not promote the dot to a confirmed manuscript reading.

## Entries awaiting image readings

The study also includes 2 Kings 19:37, Jeremiah 31:37, Jeremiah 50:29, Ruth 3:5,
and Ruth 3:17. Their current NAEE verses, qere, and any attached MAM notes are
displayed. No new image reading or crop has yet been supplied for these entries.

## Historical standalone review

The Downloads editing bundle remains a historical snapshot. Its frozen source
packets, delivered HTML, reconstructed generator, and later local edits were not
deleted. Ongoing manuscript observations are now maintained in the tracked FOI
records and this source note. The standalone generator's README points here.
