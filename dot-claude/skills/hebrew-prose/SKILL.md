---
name: hebrew-prose
description: Ben's house rules for writing, editing, or reviewing any prose about Hebrew accentuation or cantillation, including rendered pages, docstrings, comments, commit messages, issue text, and chat. Use whenever text discusses accents, cantillation, maqaf, meteg, paseq or legarmeh, strands, Decalogue readings, or the prose and poetic systems.
---

# Hebrew accentuation prose

This skill is canonical. A repository may add a narrowly scoped exception; when it does, read
the repository-specific reference before writing. Load only the references needed for the task.

## Checklist that applies to every accentuation task

1. **Name the unit.** An **atom** is one written form between spaces or maqafs. A **chanted
   word** is one atom or a whole maqaf compound, the unit on which cantillation operates. Do
   not leave a loose "word" for the reader to resolve, and name a compound whole rather than
   naming a bare half.
2. **Use one scale of separating force.** Disjunctives, conjunctives, then maqaf. Maqaf has the
   weakest *separating* force and binds most tightly. Count a maqaf difference once and state it
   as an exchange with both markings named. Do not create a separate "word division" ledger.
3. **Distinguish grammar from glyphs.** The paseq glyph can be narrow-sense **paseq** or
   **legarmeh**. U+05BD is **silluq** only on the stressed syllable of the verse's final word
   before sof pasuq; elsewhere it is **meteg**. A maqaf-joined atom is not verse-final.
4. **Write prose and poetic verses, never prose and poetic books.** Psalms, Job, and Proverbs
   contain both systems. Identify the system of the verse being discussed.
5. **Describe structure, not transformation.** An accent does not turn into another accent,
   acquire a mark, replace a neighboring accent, or govern deliberately. State what the text,
   atom, chanted word, syllable, or tradition **has**. Preserve real historical change only when
   the source and evidence establish it.
6. **Name the source relation precisely.** An edition, manuscript, codex, and strand are not
   interchangeable. Do not call any of them a "witness" unless the task is expressly about
   textual criticism. A grammatical claim takes MAM as its corpus unless another corpus is
   explicitly named; WLC is a comparison text, not a substitute corpus.
7. **Use the established names.** Write "the Simanim Tiqqun", not bare "Simanim". Keep strand
   names in Hebrew letters in reader-facing prose. Distinguish narrow-sense meteg from secondary
   stress, and do not infer vowels from secondary-stress placement. Treat stress-helper templates
   as choices among strands, not as a license to traverse all branches. Reserve `MUDGASH` and
   `mudgash` for literal Unicode code-point names.
8. **Show the Hebrew form in Unicode.** Do not replace the form with a transliteration or an
   English gloss. In mixed-direction prose, the first strong character of a line must be Latin;
   give Hebrew an English runway or its own RTL table cell. A section sign, a digit and a backtick
   are neutral rather than strong; none satisfies this rule.

## Load only the references the task needs

- **General writing rules, corpus choice, and the checklist's reasoning:** read
  `references/core-rules.md`.
- **A precise term, transliteration, name, or exemption:** read `references/terminology.md`.
- **Rendered HTML, tables, captions, headings, tooltips, or alt text:** read
  `references/rendered-prose.md`. Every table cell holding Hebrew is `dir="rtl"` unless the
  whole table already is.
- **MAM-basics prose:** also read `references/mam-basics.md`. In particular, the nine
  `gh-pages/post-stress-meteg*.html` pages deliberately use plain "word" because their
  introduction fixes the meaning; never change those pages to "chanted word".
- **Claims about corpora, Yeivin, Breuer, CTR, manuscript practice, or the prose-poetic
  asymmetry:** read `references/sources-and-corpora.md`. Search the full local OCR, not only
  Ben's partial Yeivin adaptation, before saying that a source is silent.
- **Counts, regeneration, generators, Black, or Unicode mechanics:** read
  `references/verifying.md`. Regenerate the tracked artifact, read its diff, and read every
  reported number back from the generated file.

## Canonical copy

This skill is canonical at `MAM-basics/dot-claude/skills/hebrew-prose/` and is shared with
Codex through `dot-claude/shared-skills.txt`. Change the canonical copy first, then use the
deployment procedure in `dot-claude/README.md`.
