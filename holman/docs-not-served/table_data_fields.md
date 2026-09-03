# table_data.json field guide

This document describes the fields in `docs-not-served/table_data.json` as produced by `../MAM-basics/py/main_extract_docx_and_render_table.py`.

It distinguishes between:

- extractor meaning: what the code is designed to produce
- current data observation: what is true in the present `table_data.json`

## Top-level object

### `source_document`

- Type: string
- Meaning: the path of the DOCX file that was extracted
- Source: the `docx_path` argument passed into the extractor
- Current data observation: a repo-relative path at repo top level

### `introduction_paragraph_count`

- Type: integer
- Meaning: the number of non-empty paragraphs collected before the first table in the DOCX body
- Source: paragraphs encountered before the extractor reaches the first `tbl` element
- Current data observation: `10`

### `table`

- Type: object
- Meaning: the extracted table payload

### `mam_plus_verify`

- Type: object
- Meaning: post-extraction verification summary against MAM-parsed-plus verse text
- Source: `../MAM-basics/py/hkq_cmn/verify_table_words_in_mam_plus.py`
- Current data observation: all `77` rows are found in their mapped MAM-parsed-plus verse text

### `mam_plus_rows_matching_mpu_verse_template_arg`

- Type: array of objects
- Meaning: rows whose `word` appears as an exact token inside at least one template argument in the mapped MAM-parsed-plus verse
- Source: post-extraction verification scan of template arguments, with explicit exclusion of נוסח argument `2`
- Current data observation: `17` rows
- Row payload note: each row includes `template_args_in_mpu_verse`, an extracted list of template argument records for that MAM-plus verse (`template_name`, `argument_key`, `argument_text`) retained for traceable verification context.
- Row payload note: matching rows also include `matching_mpu_surface_words_in_mpu_verse`, the exact projected MAM-parsed-plus surface-word forms from verse text that match the row word after normalization. These forms can preserve trailing sof pasuq even when the matching template argument text does not.

## `table` object

### `header_labels`

- Type: array of strings
- Meaning: the literal text extracted from the header row cells
- Source: the first table row
- Current data observation: `['', 'Verse', 'Word', 'Finding', 'Aleppo', 'Leningrad', 'Notes']`
- Note: the first header cell is blank in the source document

### `column_keys`

- Type: array of strings
- Meaning: normalized keys derived from `header_labels`
- Source: each header label after lowercasing and slugifying non-alphanumeric characters to underscores
- Current data observation: `['entry', 'verse', 'word', 'finding', 'aleppo', 'leningrad', 'notes']`
- Note: because the first header label is blank, its normalized key falls back to `entry`
- Note: `entry`, `aleppo`, and `leningrad` remain source-column keys, but these text fields are intentionally omitted from each row object after extractor assertions

### `row_count`

- Type: integer
- Meaning: number of extracted data rows, excluding the header row
- Source: `len(rows)` after extraction
- Current data observation: `77`

### `finding_value_counts`

- Type: array of objects
- Meaning: each distinct `rows[].finding` value and the number of rows where it appears
- Source: grouped count over extracted row `finding` values
- Current data observation: four entries

### `finding_value_counts[].finding`

- Type: string
- Meaning: one unique finding label
- Source: distinct values from `rows[].finding`

### `finding_value_counts[].count`

- Type: integer
- Meaning: number of rows whose `finding` equals `finding_value_counts[].finding`
- Source: grouped count over `rows[].finding`

### `notes_structured_counts`

- Type: array of objects
- Meaning: each distinct structured notes signature and the number of rows where it appears
- Source: grouped count over parsed notes components
- Current data observation: four entries

### `notes_structured_counts[].notes-UXLC`

- Type: string
- Meaning: abstracted UXLC notes payload with Hebrew runs replaced by `<HEB>`
- Source: parsed `rows[].notes` after the constant prefix `MAM - No Comments | UXLC - `, with any leading pointed prefix atoms banished out of the ketiv token before grouping

### `notes_structured_counts[].notes-UXLC-pointed-prefix-atoms`

- Type: string or null
- Meaning: abstracted leading pointed prefix atoms stripped from the UXLC ketiv token, with Hebrew runs replaced by `<HEB>`
- Source: parsed from the leading ketiv token only when one or more maqaf-terminated prefix atoms can be removed while leaving a ketiv letter skeleton that matches `rows[].word`
- Current data observation: `null` on most rows; `<HEB>` on 10 rows

### `notes_structured_counts[].notes-UXLC-yatir`

- Type: string or null
- Meaning: yatir marker extracted from UXLC notes, when present
- Source: optional trailing `/n(yatir ...)` parsed from UXLC notes payload
- Current data observation: `null` or `yatir aleph`

### `notes_structured_counts[].notes-HaKeter`

- Type: string or null
- Meaning: abstracted HaKeter notes payload with Hebrew runs replaced by `<HEB>`
- Source: optional `| HaKeter - ...` component in `rows[].notes`

### `notes_structured_counts[].count`

- Type: integer
- Meaning: number of rows whose parsed notes components equal this structured signature
- Source: grouped count over parsed notes components

### `verse_book_names`

- Type: array of strings
- Meaning: distinct standard 39-book names observed in `rows[].verse`
- Source: extracted `verse` values normalized to the vendored `mb_cmn/bib_locales.py` standard names
- Current data observation: includes names like `Joshua`, `1Samuel`, and `Tsefaniah`

### `rows`

- Type: array of objects
- Meaning: the extracted row records
- Source: each non-header table row in document order
- Current data observation: `77` row objects

## Row object

### `row_number`

- Type: integer
- Meaning: the 1-based output row index
- Source: generated by the extractor while enumerating non-header rows
- Guarantee level: generated metadata
- Current data observation: runs from `1` to `77`

### `verse`

- Type: string
- Meaning: verse reference from the second table column
- Source: source-table content normalized to `mb_cmn/bib_locales.py` standard 39-book names
- Current data observation: values like `Joshua 3:4.5`

### `word`

- Type: string
- Meaning: the Hebrew word or form under discussion
- Source: source-table content, with any trailing sof pasuq stripped during extraction
- Current data observation: populated with Hebrew strings

### `word_orig`

- Type: string, optional
- Meaning: the original extracted DOCX `word` value before a trailing sof pasuq was stripped
- Source: copied from source-table `word` only when extraction normalizes a trailing sof pasuq away from `rows[].word`
- Current data observation: present only on rows whose source `word` ended in sof pasuq

### `finding`

- Type: string
- Meaning: the finding label from the table
- Source: source-table content
- Current data observation: values like `A - Masorah Circle | L - Qere` and `A and L - Qere`

### `notes-UXLC`

- Type: string
- Meaning: parsed UXLC notes payload (without the constant `MAM - No Comments | UXLC - ` prefix), with any leading pointed prefix atoms banished out of the ketiv token
- Source: parsed from the source-table notes column after extractor cleanup and row-word-guided ketiv-prefix splitting
- Current data observation: populated for all rows

### `notes-UXLC-pointed-prefix-atoms`

- Type: string, optional
- Meaning: leading pointed prefix atoms stripped from the UXLC ketiv token and preserved separately
- Source: parsed from maqaf-terminated atoms at the start of the ketiv token when the remaining ketiv letters match `word`
- Current data observation: present on 10 rows
- Example: row `1Samuel 30:6.15` stores `notes-UXLC` as `בנו בָּנָ֣יו` and `notes-UXLC-pointed-prefix-atoms` as `עַל־`

### `notes-UXLC-yatir`

- Type: string or null
- Meaning: optional yatir marker parsed from the UXLC payload
- Source: parsed from a trailing newline marker in UXLC notes payload (for example `/n(yatir aleph)`)
- Current data observation: `null` for most rows; `yatir aleph` on two rows

### `notes-HaKeter`

- Type: string or null
- Meaning: optional HaKeter notes payload
- Source: parsed from an optional `| HaKeter - ...` component in the source-table notes column
- Current data observation: `null` for most rows; populated on four rows

### `notes_orig`

- Type: string, optional
- Meaning: original notes column text before a targeted note correction is applied
- Source: copied from source-table `notes` only when a row-specific fix in `NOTES_TARGETED_FIXES_BY_ROW_NUMBER` is applied
- Current data observation: present on `2` rows (`Joshua 10:24.19` and `Isaiah 52:5.2`)
- Note: this is not used for routine junk-character cleanup; it is retained only when content-level correction changes the note itself

### `image_files`

- Type: object, optional by schema
- Meaning: exported image paths grouped by column key
- Source: embedded images found in row cells
- Current data observation: present on all `77` rows
- Note: this field appears only when at least one image is found in the row

## `image_files` object

### `image_files.aleppo`

- Type: array of strings
- Meaning: exported image paths for embedded images from the Aleppo cell
- Current data observation: one image path per row
- Path format: `gh-pages/img/rowNNN_aleppo_XX.ext`

### `image_files.leningrad`

- Type: array of strings
- Meaning: exported image paths for embedded images from the Leningrad cell
- Current data observation: one image path per row
- Path format: `gh-pages/img/rowNNN_leningrad_XX.ext`

## Short conclusions

- `row_number` is generated metadata.
- `entry` text is asserted to equal the string form of `row_number`, then omitted from row output.
- `finding_value_counts` summarizes each distinct `finding` label and its row count.
- `notes_structured_counts` summarizes `notes-UXLC`, `notes-UXLC-pointed-prefix-atoms`, `notes-UXLC-yatir`, and `notes-HaKeter` signatures with row counts.
- `verse_book_names` lists the distinct standard MAM 39-book names observed in `rows[].verse`.
- `aleppo` and `leningrad` text fields are dropped from `rows` after extractor assertions (`aleppo` must be empty; `leningrad` must be empty or a single `’` marker).
- Aleppo/Leningrad screenshots or embedded figures remain under `image_files`.
- `mam_plus_verify` summarizes post-extraction presence checks in plus verse text, excluding נוסח argument 2 documentation.
- `mam_plus_rows_matching_mpu_verse_template_arg` captures rows where the table `word` appears as a whole token in any template argument text, excluding נוסח argument `2`.
