# Building near-Aleppo

The near-Aleppo build and example edition are local MAM-basics products. The
entry point is `py/main_near_aleppo.py`. Its inputs are the tracked
`MAM-parsed/plus/` books, `aleppo/index-flat-annotated.json`, and the runtime
data in `in/near-aleppo/`. Its outputs are `out/near-aleppo/plus/` and
`gh-pages/near-aleppo/`. The product README gives the CLI commands and license.

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
without adding written ketiv consonants. The explicit holam-male-vav variant
accepts only its declared carrier and exact mark shape. The no-space template
`ניקוד בלי אות ובלי רווח` accepts only `carrier=final-nun-dalet`, with exactly
DALET + DAGESH + TSERE + MAHAPAKH (GD). At Isaiah 54:16 it immediately follows
the final nun without a space, accommodating that nun's marks without adding a
ketiv consonant. GA and GV still forbid dagesh. This is the first final carrier
case; earlier carriers were initial or medial. The dalet accommodation makes
no claim that the manuscript has ownerless marks.

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

The broader research census, source captures, comparison programs, scan archive,
adoption handoffs and approval records remain private. They are not inputs to any
near-Aleppo public build path.
