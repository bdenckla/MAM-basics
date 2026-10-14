# Building near-Aleppo

The near-Aleppo build and example edition are local MAM-basics products. The
entry point is `py/main_near_aleppo.py`. Its inputs are the tracked
`MAM-parsed/plus/` books, `aleppo/index-flat-annotated.json`, and the runtime
data in `in/near-aleppo/`. Its outputs are `out/near-aleppo/plus/` and
`gh-pages/near-aleppo/`. The product README gives the CLI commands and license.

Follow [Releasing near-Aleppo](near-aleppo-release.md) to prepare a release,
update the dated release links, package the committed dataset, and publish
verified attachments.

The documentation pages load `../document.css` for their shared English
typography, followed by `../MAM-parsed/style.css` for parsed-document examples.
Their own `style.css` adds the Hebrew examples, template notation
and specialized tables; its source is `py/near_aleppo/doc_style.py`.

The build resolves templates through a closed dispatch table. Each structure
has explicitly selected Scripture fields; notes retain their original bodies until the final note-content phase,
and unselected apparatus fields retain their documented roles. Unknown names
and unexpected parameter sets fail before writing.

Representation policies then apply the declared near-Aleppo conventions. Source
relations are read from MAM's clause heads, including testimony and doubt
qualifiers. Direct readings quoted in MAM notes are applied only where their
classified form and target meet the code's explicit requirements. Ambiguous
readings remain pending or flagged. The build records every population and site
list in `in/near-aleppo/build-populations.json`, pinning none, so that the file's
diff shows what a change to MAM's text or to the build moved.

Pointings are applied in priority order: note-derived readings, the frozen
MAM-derived set, individual editorial decisions, then reviewed portable
pointings. The latter stages cannot overwrite an earlier pointing. Each stored
pointing records the ketiv/qere template's parameters, its ketiv and whole qere,
as the build has them where the pointing is written. Where the template no longer
has them, the build stops with an error that names the record and shows both; a
renamed template does not stop it. Importing a payload makes no new editorial
choice. Artificial carriers preserve orphan marks and their positions
without adding written ketiv consonants. Both carrier templates have only
parameter 1, containing their payload. GV is exactly VAV + HOLAM, preserving
the holam-male meaning. The no-space template
`ניקוד בלי אות ובלי רווח` accepts exactly
DALET + DAGESH + TSERE with MAHAPAKH, MUNAH or ETNAHTA (GD).
The MAHAPAKH payload at Isaiah 54:16 immediately follows
the final nun without a space, accommodating that nun's marks without adding a
ketiv consonant. GA and GV still forbid dagesh. This is the first final carrier
case; earlier carriers were initial or medial. The dalet accommodation makes
no claim that the manuscript has ownerless marks. By Ben's revised decision of
2026-10-13, the MUNAH payload follows nun at Ezekiel 14:14 and 14:20, and the
ETNAHTA payload follows nun at 28:3. Nun has exactly its qere cluster, hiriq
alone; the carrier has the absent qere yod's complete dagesh, tsere and accent
cluster. This supersedes the October 8 tsere-only GA representation at these
three sites. The complete qere and original source clauses are preserved.

Recorded qere-without-ketiv body encodings are applied after the pointings and
before MAM-target copying. The build reads the explicit `intended_encoding.template`
in `in/near-aleppo/qere-without-ketiv-readings.json`, checks its whole qere
against the unchanged `קרי ולא כתיב` call, and inserts the body template
immediately before that call without a separator. `ניקוד בלי אות` holds marks
with horizontal space. The no-space body template has exactly
ALEF + TSERE + MERKHA, without dagesh, at 2 Samuel 18:20.
The parameterless `רווח בלי ניקוד` records horizontal space without marks.
Build populations record these body classifications separately from the MAM-only
census. The independent note replay applies the same phase. The example edition
pairs each body template with its following qere, displaying body marks, or
empty double guillemets for space without marks, below the qere; editorial box
and carrier widths do not measure manuscript spacing. The mixed alef/vav payload
is exactly
`אְאָא֖וֹ` at 2 Kings 19:31: three marked alef letters followed by VAV + HOLAM.
The final artificial vav retains the ḥolam male carrier meaning without adding
a written consonant or claiming that a vav is present in the body. This exact
mixed payload does not relax the GA or single-carrier GV payload rules.

The near-Aleppo dataset's zero-width sibling, `ניקוד בלי אות ובלי רווח`,
accepts the same GA and GV shapes. Both render carriers
in guillemets; neither inserts a separator. By Ben's decision of 2026-10-08,
medial orphans between written letters with no adjacent literal separator use
the zero-width name. Leading orphans and existing explicit separators retain
their representations. All Hebrew codepoints are unchanged.

After the last pointing import, before any output is written, a Scripture-target
check requires each supplied ordinary or trivial pointed ketiv to retain its
written ketiv consonants, excluding artificial carriers. Raw combining marks
require a written-letter owner, while explicit orphan templates use the existing
GA/GV/GD contract. GD accommodates final-nun marks or the absent qere yod's
cluster at the declared sites. The check inspects values without changing them. It does not
judge vowel combinations, manuscript ownership or whole-atom grammar.

The build preserves C and D columns, qeres, atom boundaries
and edition punctuation except where a stated policy explicitly applies. It
copies the original MAM target into every changed note, then adds evidence flags
and gives those notes distinct near-Aleppo names. Its final phase stores the
reviewed near-Aleppo clause in parameter 2 and the remaining original MAM
clauses in `הערת מקרא על פי המסורה`. When the complete note remains about MAM,
parameter 2 is an empty array and that added parameter preserves the original
body. `מקרא על פי המסורה` is the original structured MAM target. Scroll-note
parameter 3 and flags retain their existing roles. The template names are
`נוסח עם הקשר מקרא על פי המסורה` and `הערה-2 עם הקשר מקרא על פי המסורה`.
Consumers render these stored roles without editorial clause transformations.

Five independent MAM instruments, the census, count populations from MAM's text
alone and write `in/near-aleppo/census/`. The census gathers every result before
writing any. Each population it counts must agree with the build's own count of
the same population. A changed ketiv or qere at a stored pointing, or an
unreviewed presentation, stops the build for review rather than choosing a
replacement.

The presentation ledger contains the source evidence and substantive reviewed
clause dispositions used during the build. A fresh pre-bake source replay must
match every changed-note entry before any dataset file is written. Review
provenance reads source inputs and never hashes published book files, avoiding
an output dependency cycle. The maintained refresh command preserves reviews
only when every row's evidence agrees. The edition renderer reads stored note
roles from the book JSON without loading the ledger. The shared renderer serves both MAM-with-doc
and near-Aleppo; MAM-with-doc's own regenerated pages show any change it makes
there. Stored Hebrew source strings retain their own codepoints; display projection
uses MAM-normal mark order without Unicode normalization.

NAEE opts into the shared HTML-stage typography helper
`py/py_html/hebrew_letter_spacing.py`. Its original family selects contiguous
Hebrew atoms with a yod, vav or final nun carrying both a broad below-letter vowel
(tsere, segol, a hataf vowel or qubuts) and a below-letter accent. By Ben's approval
of 2026-10-13, the active selection also includes the six observed advance-adding
contexts in the frozen Taamey D 0.921 source and its precise preceding-yod
vowel-raising context beside qof. The selected
text gets `0.06em` extra letter spacing in the edition stylesheet. This is a
conservative visual heuristic, not a collision detector or an exhaustive list
of cramped atoms. The same rule reaches ketiv, qere and Hebrew examples in notes;
spaces, maqafs, punctuation and source characters are preserved. Atoms divided
by formatting spans can be missed or only partly expanded; single-letter text
leaves are left alone. MAM-with-doc and Phonetic MAM have not opted in. The
classifier and HTML helper can be reused without changing their datasets.

The font-derived selection keeps the ordered below-mark conditions of
`kern1AddThin`'s five contexts, `kern2AddThin`'s second context, and the preceding-yod
rule in `mark2BalanceVyingBlwMarks`. The font's narrow letters are gimel, vav,
zayin, yod, nun and final nun. `_font_added_space` and `_yod_before_qof` name the
active screens. Their private mark-order projection models shaping for screening
only; it never reorders the source or displayed text. Unsupported glyphs remain
barriers. The first `kern2AddThin` context, with two below marks followed by three
on a narrow letter, had no occurrence in the selected-Scripture investigation and
remains inactive without a visual verdict. Orphan vowels are removed from the
font's below-mark screen; unjudged final he, het or ayin shapes with patah are
excluded from its fifth advance-adding context because the font can use a
filtered-out furtive glyph there. The source archive is
`in/font-support/taamey-d-0.921/Taamey_D-0.921-source-40115a364a4e.zip`, whose
`sources/font-m-TaD/Taamey_D.sym.fea` declares the relevant rules. The runtime
classifier requires no font-analysis libraries.

The spacing FOI, generated by `py/near_aleppo/foi_spacing.py`, compares a small
selection of current Scripture atoms at usual spacing and with the adjustment.
Its first three families receive automatic spacing: the original narrow-letter
family, the observed font-spacing contexts, and the precise yod-before-qof context.
Two broad screens remain display trials: adjacent narrow letters with below-letter
marks, and qof with below-letter marks on its predecessor and itself. A trial match
can also belong to an active family. Examples resolve
from the shared renderer's body, ketiv or qere stream and must retain their
stated family. Notes, ruby fallback text and placeholders are excluded; atoms
crossing special-letter or vowel-variant formatting are not selected.
Each family reports the number of examples shown, distinct complete pointed
forms, and occurrences across all books in this same projection. Counts are
recomputed during HTML generation. Families overlap, so their totals are not
additive.

The broader research census, source captures, comparison programs, scan archive,
adoption handoffs and approval records remain private. They are not inputs to any
near-Aleppo public build path.
