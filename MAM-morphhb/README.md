# MAM-morphhb

This product directory has `MAPM.xml`: MAM's current text in the form of the 2014 OSIS file
that openscriptures/morphhb keeps as `MAPM/MAPM.xml`. That file is David Troidl's conversion of
MAM, finished on 2014-02-19; MAM-basics keeps a byte-identical copy in `MAM-OSIS/MAPM-orig/`.
`MAPM.xml` here is named as there so that it can replace morphhb's file byte for byte.

The one program found that reads the 2014 file is OpenScriptorium's
`app/services/importers/oshb_features_importer.rb`, which reads it line by line. So MAM-morphhb
keeps the 2014 file's line layout, and the few places where its form deliberately differs call
for a small change to that importer.

Its sources are MAM-simple's BHS JSON, with MAM-simple's MAM JSON for the book groups that have
no BHS file, for the text, and `MAM-parsed/plus/`, for what MAM-simple lacks: the book and
division titles, the parashot and the poetic line breaks. `header.xml` is hand-written.

## How current this product is

**This product is not kept continuously current.** It is regenerated only when someone runs
`py/main_mam_morphhb.py` deliberately, so it can lag `MAM-simple/` and `MAM-parsed/plus/` by
any amount: a refresh of MAM's text does not oblige a rerun. To bring it up to date, for
example before offering morphhb a new `MAPM.xml`, run, from the MAM-basics repository root:

```
.venv/Scripts/python.exe py/main_mam_morphhb.py
```

The run validates `MAPM.xml` against the OSIS 2.1.1 schema, `in/osisCore.2.1.1-cw6.xsd`.

## What MAM-morphhb keeps from the 2014 form

- **The hierarchy.** One book group holds the Torah, the Prophets and the Writings, each a
  titled book group. Samuel, Kings, the Twelve, Ezra–Nehemiah and Chronicles are nested, titled
  book groups. Every other book has a title, and so do the Twelve's books, which take the
  prophets' names; the books in the other four nested groups have none.
- **59 sections,** each with its title on the line after its `div`: the Torah's 54 parashot,
  scoped by verse and named as MAM has them, and Psalms' five books, scoped by chapter.
- **Milestones.** Chapters and verses are milestones, with their Hebrew numbers in `n`.
- **`<p>` as a container:** one per parashah in the Torah, one per chapter elsewhere.
- **Breaks as `<lb/>` lines:** two for a petuḥah (MAM's `פפ`), one for a setumah (`סס`) or for
  MAM's `פפפ`. The line after a setumah opens with three IDEOGRAPHIC SPACE characters. A
  mid-line setumah (`ססס`) is two EM SPACE characters.
- **Poetic lines.** Psalms, Proverbs and Job 3:2–42:6 are laid out in `<lg>` and `<l level>`
  elements, from MAM's `ר1`, `ר2` and `ר3` templates: a verse starts at level 1, and `ר1`,
  `ר2` and `ר3` start a line at levels 2, 3 and 1.
- **The segs.** A narrow-sense paseq is an `x-paseq` seg after a NO-BREAK SPACE; the paseq glyph
  of a legarmeh is bare, after a NO-BREAK SPACE. Large, small and hung letters are `x-big`,
  `x-small` and `x-suspended` segs. An inverted nun is an `x-reversednun` seg, and the setumah
  beside each of Numbers 10's two is an `x-space` seg of two EM SPACE characters.
- **The line layout:** tab indentation, one prose verse or one poetic line per line, LF line
  endings, `osisIDWork="MAPM"`.

## Where MAM-morphhb differs from the 2014 form, and why

1. **BHS numbering throughout,** the numbering of WLC, of morphhb's `wlc/` and of MAM-OSIS. The
   2014 file mixed MAM's own numbering with BHS's. Eight English `type="variant"` notes, each at
   the first verse of a difference, say where MAM's own numbering differs; the 2014 file had
   four notes of that kind, against WLC. Joshua 21:36–37, which BHS numbers but MAM's text does
   not have, are left out, where MAM-OSIS has each as a verse holding an em dash.
2. **The qere is marked.** A ketiv and its qere are
   `<seg type="x-ketiv">…</seg> <seg type="x-qere">…</seg>`, in MAM's order, so a qere can come
   first; the 2014 file wrote the qere as plain text after the ketiv. A ketiv velo qere is
   `<seg type="x-ketiv-velo-qere">(…)</seg>` and a qere velo ketiv
   `<seg type="x-qere-velo-ketiv">[…]</seg>`, as in MAM-OSIS.
3. **No song tables, for now.** The eight songs that the 2014 file set as tables are ordinary
   verse lines, and each shirah space is an `x-space` seg of two EM SPACE characters.
4. **The good endings** of Isaiah, Malachi, Ecclesiastes and Lamentations are `x-good-ending`
   segs inside each book's last verse. The 2014 file had two, as extra verses never closed.
5. **Notes and segs from MAM-OSIS.** MAM-OSIS's notes on scroll differences, on words with
   special letters and on silluq before meteg are kept; its notes on narrow-sense paseq are
   not, since the `x-paseq` seg already says so. MAM's implicit maqaf is an `x-implicit-maqaf`
   seg, and a verse with dual cantillation has the combined text. All nine inverted nuns are
   here; the 2014 file lacked Psalms 107's seven.
6. **No `x-symbol` segs.** The 2014 file's ♫ before each song and ↓↑ at Genesis 35:22 were
   links on MAM's Wikisource page, not text.
7. **Layout details are uniform** where the 2014 file varied:
   - a line opens with no space after a petuḥah or `פפפ`, with three IDEOGRAPHIC SPACE
     characters after a setumah, and otherwise with no space if it starts a `<p>` or `<l>`;
     a prose verse that continues a line opens with one space;
   - a break's `<lb/>` lines stand just before the verse they precede: after a chapter start
     milestone or a `<p>`, and before an `<lg>`;
   - between two verses laid out as poetic lines, a break closes the `<lg>` and opens another,
     with the break's `<lb/>` lines between them;
   - a break inside a verse ends its line; the verse continues on the next line, and the
     verse's end milestone stands on a line of its own.

## License

MAM's CC BY-SA 4.0, as `LICENSE.md` states.
