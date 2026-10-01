# Phonetic MAM computation interface

`py/main_phonetic_mam.py compute` provides a read-only, local calculation interface
to the canonical algorithms in `py/phonetic_mam/core/`. It uses UTF-8 NDJSON on
standard input and standard output. One process handles successive requests until
EOF. Each input line receives one output line; requests share no calculation state.
The interface reads no input data files and writes no files, including import caches.

This interface is separate from the public release format. Intermediate calculations
can contain annotations and analysis state that are forbidden in a release. Keep
requests and responses transient. A caller that publishes data must apply the
separate closed release projection and its disclosure checks.

## Envelope

Every request has exactly `schema`, `operation`, and `arguments`. The schema is
`phonetic-mam-compute-v1`. An unknown operation, field, enum value, duplicate JSON key,
or malformed structure is rejected. Non-finite numbers are not JSON input. A request
line is limited to 16 Mi characters; an oversized request terminates the stream.

Success replies have exactly `schema` and `result`. Failure replies have exactly
`schema` and `error`; the error contains a type and a fixed message, never the input
text. A rejected ordinary line does not end the stream. An oversized request or a
broken pipe ends the invocation; callers must treat a missing response as failure.

## Operations

- `phrase`: requires `phrase`, `bcvt`, and `untanglers`. The verse identity is the
  five-element MAM array. Untanglers map a lookup string to two nonempty arrays of
  strings, for the `א` and `ב` strands. Optional `lookup-keys` maps input strings to
  supplied untangler keys. Optional `qamats` is null, `qamats-dal`, or `qamats-sam`;
  optional `include-in-edition-census` is a Boolean, defaulting to true. The result
  contains `sods`, parallel `transcriptions`, `census`, and `untangler-use-counts`.
  A transcription is null, an object with `sephardic` and `ashkenazic` strings, or an
  object with `alef` and `bet` arrays of those transcription objects. Census entries
  contain `cantsys`, `bccvec`, `count`, and `examples`. Accumulate these deltas in the
  caller if a longer-lived census is needed
- `prepare-untanglers`: requires `verses`, an array of public MAM-parsed-plus
  EP sequences. Returns the cooked untangler map accepted by `phrase`. All three
  named dual-template parameters and both qamats alternatives are retained. Only
  direct EP dual templates supply alignment input. The known current template
  names and parameter identities are closed; unknown shapes and nested dual
  templates are rejected. Documentation is validated but supplies no Scripture
  to the calculation. The caller reads its selected MAM input; computation does
  no file I/O
- `word`: requires `word` and `format`, where the format is `generic` or `annotated`.
  Returns the transient extended phonetic calculation, including its audit values
- `ipa`: requires `values`, an array of internal phonetic strings, and returns the
  corresponding array of IPA strings
- `accents`: requires `cantsys` (`cant-sys-prose` or `cant-sys-poetic`) and `values`,
  an array of letters-and-accents strings. Returns `letters`, `bccvec`, and
  `stress-index` for each input. An unknown accent vector has a null stress index
- `accent-names`: requires `values`, an array of accent identities, and returns
  their canonical readable names
- `accent-vectors`: requires `cantsys` (`cant-sys-prose` or `cant-sys-poetic`) and
  returns the known `bccvec`, `stress-index`, and canonical `name` for every vector
- `symbols`: accepts an empty argument object and returns the named string symbols
  of the internal phonetic alphabet
- `transcriptions`: requires `values`, an array of objects with `syllables` and
  `stress`. Syllables are a nonempty array of nonempty atom arrays. Each syllable has
  `sylrec-udl` and optionally `sylrec-next-syl-swp1g` and `sylrec-this-syl-swp2g`.
  Stress is null or a valid nonnegative atom/syllable index pair. Returns both
  transcriptions for every input

No operation accepts a filename, output destination, module name, or function name.
The caller supplies the data and any source-specific adaptations. The algorithms
preserve MAM mark order and never normalize Hebrew.
