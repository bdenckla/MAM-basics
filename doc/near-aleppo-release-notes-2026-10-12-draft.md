# Near-Aleppo (NA) release notes — 2026-10-12 (draft)

State: live; awaiting Ben's edits before release

This update puts NA-adjusted note content directly in the dataset, adds body-text
encodings at qere-without-ketiv sites, and improves pointed-ketiv representations.
The Near-Aleppo example edition (NAEE) now displays ketiv/qere pairs in a curved
box or "cartouche", with the pointed qere above the ketiv.

This is a draft dated 2026-10-12, not a release announcement. It describes the
dataset and pages at commit `a29f1c08924cb9ab01fe7952257fc8df615ebdbf`, compared
with the dataset first announced on 2026-10-06. The release date, tag, and final
commit remain to be selected after editing.

## Dataset changes

### NA-adjusted note content is included in the JSON

Notes whose targets differ from MAM's now store the NA-adjusted note content
and original MAM context separately. Previously the dataset kept the original
note body in parameter 2, and the renderer supplied the NA-adjusted presentation.
Consumers can now render the stored roles directly.

The changed-note template names have changed:

| Earlier name | Current name |
| --- | --- |
| Note `נוסח למקרא על פי המסורה` | Note `נוסח עם הקשר מקרא על פי המסורה` |
| Note `הערה-2 למקרא על פי המסורה` | Note `הערה-2 עם הקשר מקרא על פי המסורה` |

Parameter 1 holds NA's target. Parameter 2 holds the reviewed NA-adjusted
clause, or an empty array. The added parameter `הערת מקרא על פי המסורה`
holds the remaining original MAM clauses, or the complete original note.
The parameter `מקרא על פי המסורה` preserves MAM's original structured target.

The current dataset has 1,552 changed notes: 1,047 include an NA-adjusted clause,
and 505 keep the complete original note in MAM context. These counts include
the new body encodings and the correction at 1 Kings 8:11 described below.

**Consumer action:** Update closed template dispatch for the new names and
parameter roles. The [JSON reference](https://bdenckla.github.io/MAM-basics/near-aleppo/reading-json.html#own-templates)
and consumer notices in all 24 book files describe the current contract.

### Body encodings at qere-without-ketiv sites

All nine qere-without-ketiv sites now have an additional template describing the
body's marks or horizontal space. Each body template immediately precedes the
unchanged `קרי ולא כתיב` call, without an intervening separator. The body
template and qere call describe the same site.

| Body encoding | Sites |
| --- | --- |
| Marks with horizontal space, `ניקוד בלי אות` | Judges 20:13; 2 Kings 19:31 and 19:37 |
| Marks without horizontal space, `ניקוד בלי אות ובלי רווח` | 2 Samuel 18:20 |
| Horizontal space without marks, `רווח בלי ניקוד` | 2 Samuel 16:23; Jeremiah 31:37 and 50:29; Ruth 3:5 and 3:17 |

At 2 Samuel 18:20, the formerly planned encoding is now implemented: parameter 1
contains the artificial alef carrier `אֵ֥`, recording tsere and merkha without
dagesh. At 2 Kings 19:31, the mixed payload `אְאָא֖וֹ` has three marked
artificial alefs followed by an artificial vav with holam. The vav preserves
the ḥolam male carrier meaning; it is not a written body-text consonant.

The [qere-without-ketiv study](https://bdenckla.github.io/MAM-basics/near-aleppo/foi/qere-without-ketiv.html)
documents the recorded manuscript readings, supplied image crops, MAM notes
with English translations, and NAEE excerpts. The carrier and display-box
widths do not measure manuscript spacing.

**Consumer action:** Add dispatch for the parameterless `רווח בלי ניקוד`
template and the supported no-space carrier template. A body projection selects
the body template; a reading projection selects the qere. Do not concatenate
the body payload and qere as consecutive Scripture.

### Carrier contracts and pointed-ketiv representations

The two carrier templates, `ניקוד בלי אות` and
`ניקוד בלי אות ובלי רווח`, now have only parameter 1. The redundant
`carrier=holam-male-vav` parameter has been removed; the artificial vav and
holam in the payload retain that meaning.

Medial artificial carriers without adjacent literal separators now use the
no-space template. Leading carriers and existing explicit separators retain
their representations. Several pointed ketivs also now express marks through
explicit artificial-carrier structures rather than ambiguous mark combinations
on a written letter.

At Isaiah 54:16, the pointed ketiv is stored as `הִן` followed immediately by
a no-space template containing `דֵּ֤`. The artificial dalet accommodates the
final nun's dagesh, tsere, and mahapakh for fonts that have difficulty displaying
those marks on a final nun. The dalet adds no ketiv consonant and makes no
claim that these manuscript marks lack a letter owner.

**Consumer action:** Accept the documented payloads and exact parameter sets;
do not require the removed `carrier` parameter. Artificial alef, vav, and dalet
carriers are not written ketiv consonants. Do not insert a separator at a
carrier-template boundary. The [carrier definitions](https://bdenckla.github.io/MAM-basics/near-aleppo/reading-json.html#own-templates)
give the supported forms.

### Punctuation and other corrections

Stored pointed ketivs now retain final maqaf and U+05C0 punctuation at additional
sites. U+05C0 is the glyph NA uses for both narrow-sense paseq and legarmeh.
A final maqaf joins the ketiv to the following atom; it is not a separator
between ketiv and qere alternatives.

Other corrections include:

- At 2 Samuel 15:8, the pointed ketiv `יָשֹׁ֨יב` has holam before qadma on
  the shin. The letters and marks are unchanged; their stored order is corrected.
- At 2 Kings 14:7, the stored pointed ketiv `המֶלַח֙` has the final pashta
  without the additional stress helper previously retained on the mem.
- At 1 Kings 8:11, NA now retains the divine-name holam in `כְבוֹד־יְהֹוָ֖ה`,
  following MAM's explicit manuscript note. NA's target now agrees with MAM's,
  so this note uses the ordinary `נוסח` template.
- At 2 Samuel 20:23, Jeremiah 48:21, Ezekiel 39:25, and 2 Chronicles 13:19,
  paired templates have the name `קו״כ` instead of `כו״ק`, following MAM's
  source correction. Their readings are unchanged; parameter 1 remains the
  ketiv and parameter 2 the pointed qere.

## Documentation and example edition

NAEE uses ketiv as its primary text, using the stored pointed ketiv where
available, with pointed qere above it at the same size. Each pair has the curved
box or cartouche used by the Charitable Leningrad Codex (CLC) example edition.
Spacing and padding keep borders clear of the Hebrew marks. An absent reading
has an editorial label in its position; a qere-without-ketiv body encoding
instead supplies marks or empty guillemets below its qere.

Existing notes remain beside the text, and the display adds no synthesized
qere notes. Trivial ketiv/qere templates also show both readings; their qere
source metadata is available on hover.

The new [features of interest](https://bdenckla.github.io/MAM-basics/near-aleppo/foi/)
include selected ketiv/qere examples and the qere-without-ketiv study. The JSON
guide explains the implemented body templates and carrier contracts. The
edition index brings the book links ahead of the detailed introduction, and
the pages use shared English styling and arrow link markers.

## Remaining limitations

The body encodings complete the previously planned 2 Samuel 18:20 representation,
but broader one-sided ketiv/qere work remains. Some note-derived readings and
apparatus clauses are still pending. In particular, the new blank body encoding
at Jeremiah 31:37 does not complete its separate note-derived replacement.
The [coverage and status page](https://bdenckla.github.io/MAM-basics/near-aleppo/coverage-and-status.html#pending)
lists the outstanding cases and coverage limitations.

## Release contents

The proposed dataset ZIP contains `README.md`, `LICENSE.md`, and the 24 book
JSON files in `plus/`, all from `out/near-aleppo/` at the final release commit.
These release notes are a separate attachment. The dataset license remains
CC BY-SA 4.0, with attribution in `LICENSE.md`.

The [NA documentation](https://bdenckla.github.io/MAM-basics/near-aleppo/)
and [NAEE](https://bdenckla.github.io/MAM-basics/near-aleppo/edition/) remain live
pages that can change independently of a dataset release. The ZIP excludes
the example edition, manuscript image crops, fonts, and internal review records.

Draft comparison and verification details are maintained in
[near-aleppo-release-status.md](near-aleppo-release-status.md).
