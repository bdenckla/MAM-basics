# Building near-Aleppo

The near-Aleppo build and example edition are local MAM-basics products. The
entry point is `py/main_near_aleppo.py`. Its inputs are the tracked
`MAM-parsed/plus/` books, `aleppo/index-flat-annotated.json`, and the sealed
runtime data in `in/near-aleppo/`. Its outputs are `out/near-aleppo/plus/` and
`gh-pages/near-aleppo/`. The product README gives the CLI commands and license.

The build resolves templates through a closed dispatch table. Each structure
has explicitly selected Scripture fields; notes retain their original bodies,
and unselected apparatus fields retain their documented roles. Unknown names
and unexpected parameter sets fail before writing.

Representation policies then apply the declared near-Aleppo conventions. Source
relations are read from MAM's clause heads, including testimony and doubt
qualifiers. Direct readings quoted in MAM notes are applied only where their
classified form and target meet the code's explicit requirements. Ambiguous
readings remain pending or flagged. Policy-sensitive populations and site lists
are checked against the tracked build snapshot.

Pointings are applied in priority order: note-derived readings, the frozen
MAM-derived set, individual editorial decisions, then reviewed portable
pointings. The latter stages cannot overwrite an earlier pointing. Sealed file
hashes and per-site source guards reject drift; importing a payload makes no new
editorial choice. Artificial carriers preserve orphan marks and their positions
without adding written ketiv consonants. The explicit holam-male-vav variant
accepts only its declared carrier and exact mark shape.

The build preserves C and D columns, qeres, source note bodies, atom boundaries
and edition punctuation except where a stated policy explicitly applies. It
copies the original MAM target into every changed note, then adds evidence flags
and gives those notes distinct near-Aleppo names. Consumers can distinguish the
dataset's Scripture from the preserved MAM apparatus subject.

Five independent MAM instruments supply the mechanically refreshable population
counts. The census checks clean tracked input identities before and after its
run, gathers every result before writing, and records the input object IDs.
Automatic expectation refresh cannot change sensitive site lists or editorial
decisions. A changed source guard, population or presentation stops the build for
review rather than choosing a replacement.

The presentation ledger contains the source evidence and substantive reviewed
clause dispositions needed by the renderer. A fresh full-source enumeration must
match all 1,548 changed-note entries. The shared renderer serves both MAM-with-doc
and near-Aleppo. Every near-Aleppo HTML run compares its MAM mode against 62
independent tracked MAM-with-doc files at the public commit named in `edition.PIN`.
Sealed Hebrew source strings retain their own codepoints; display projection
uses MAM-normal mark order and one explicit exceptional ordering, without Unicode
normalization.

The broader research census, source captures, comparison programs, scan archive,
adoption handoffs and approval records remain private. They are not inputs to any
near-Aleppo public build path.
