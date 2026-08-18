"""Exports write_book: render a CLC book as a 3-column always-link page.

Layout (design doc §7.3, build-order step 4): one row per verse, columns
``text | ref | doc``. The verse-number (ref) is a narrow central spine with the
Hebrew text on its left and the doc apparatus on its right; keeping the text
adjacent to the ref means a short verse stays butted against its label (no need
for zebra shading to tie the two together). The text column is running verse
text; every noted word is an always-link (no MAM short-inline / long-link
threshold) to its note in the doc column of the same row. CLC defines its own
``clc-*`` CSS vocabulary parallel
to MAM's ``mam-doc-*`` (design doc §8); the rules live in gh-pages/style.css.
"""

from dataclasses import dataclass

import mb_cmn.hebrew_punctuation as hpu  # for hpu.MAQ (־, U+05BE)
import mb_diff_mpu.describe_diff as describe_diff
import clc.clc_attribution as clc_attribution
import clc.clc_dual_cant as clc_dual_cant
import clc.clc_kq as clc_kq
import clc.clc_long_note as clc_long_note
import clc.clc_note as clc_note
import clc.clc_strip as clc_strip
import uxlc_misc.uxlc_utils_html as H
import uxlc_paths

_HBO_ATTR = {"lang": "hbo", "dir": "rtl"}


def out_label(book_id, chapters=None):
    """Filename stem for a (possibly chapter-limited) book page.

    Whole book -> "Exodus"; limited to chapter(s) -> "Exodus-20" so a focused
    page never clobbers a future full-book "Exodus.html". ``chapters`` is a set of
    1-based chapter numbers (or None / empty for the whole book).
    """
    if not chapters:
        return book_id
    return f"{book_id}-" + "-".join(str(c) for c in sorted(chapters))


def disp_label(book_id, chapters=None):
    """Human label for title/heading: 'Exodus' or 'Exodus 20'."""
    if not chapters:
        return book_id
    return f"{book_id} " + ", ".join(str(c) for c in sorted(chapters))


def write_book(book_id, book, notes, chapters=None):
    """Write gh-pages/clc/<label>.html and return its path.

    ``chapters`` (a set of 1-based chapter numbers, or None) limits rendering to
    those chapters; the page label/title carry the limit (see ``out_label``).
    Numbering still comes from the enumerate index, so skipping keeps ch/v correct.
    """
    notes_by_atom = _group_by_atom(notes)
    label = out_label(book_id, chapters)
    rows = [H.table_row_of_headers(("text", "ref", "doc"))]
    for chidx, chapter in enumerate(book):
        ch = chidx + 1
        if chapters is not None and ch not in chapters:
            continue
        for vridx, verse in enumerate(chapter):
            v = vridx + 1
            if clc_dual_cant.is_dual_cant(book_id, ch, v):
                rows.extend(
                    _dual_cant_rows(book_id, ch, v, verse, notes_by_atom, label)
                )
            else:
                rows.append(_verse_row(ch, v, verse, notes_by_atom, label))
    disp = disp_label(book_id, chapters)
    table = H.table(rows, {"class": "clc-3col border-collapse"})
    body = _body_wrapper(disp, table)
    out_path = uxlc_paths.clc_pages_dir() / f"{label}.html"
    write_ctx = H.WriteCtx(title=f"CLC — {disp}", path=out_path, add_wbr=True)
    H.write_html_to_file(body, write_ctx, "../")
    return out_path


def _group_by_atom(notes):
    grouped = {}
    for note in notes:
        grouped.setdefault((note.ch, note.v, note.atom_index), []).append(note)
    return grouped


def _verse_row(ch, v, verse, notes_by_atom, page_label):
    anchor = f"c{ch}v{v}"
    ref_cell = H.table_datum(
        H.anchor(f"{ch}:{v}", {"href": f"#{anchor}"}),
        {"class": "clc-ref", "id": anchor},
    )
    text_cell = H.table_datum(
        _text_contents(ch, v, verse, notes_by_atom, page_label),
        {**_HBO_ATTR, "class": "clc-text"},
    )
    doc_cell = H.table_datum(
        _doc_contents(ch, v, verse, notes_by_atom), {"class": "clc-doc"}
    )
    return H.table_row((text_cell, ref_cell, doc_cell))


def _dual_cant_rows(book_id, ch, v, verse, notes_by_atom, page_label):
    # A dual-cantillation verse (e.g. Gen 35:22) becomes three grouped rows:
    # combined (C), strand alef (א), strand bet (ב). The combined row keeps the
    # full always-link behaviour (its notes/anchors); the strand rows show the
    # strictly-split text plain, with only a short strand label in the doc
    # column. CSS ties the three into one verse block (gh-pages/style.css).
    views = clc_dual_cant.strand_views(book_id, ch, v, verse)
    strands = [vw for vw in views if vw.suffix != clc_dual_cant.SUFFIX_COMBINED]
    rows = []
    for pos, view in enumerate(views):
        ref_attr = _strand_ref_attr(view.tooltip, pos, len(views))
        ref_text = f"{ch}:{v}-{view.suffix}"
        if view.suffix == clc_dual_cant.SUFFIX_COMBINED:
            # The single per-verse anchor lands on the combined row (issue UXLC-utils#55); the
            # strand rows carry no id, so #c20v2 stays unique per page. That row's ref
            # is also the verse self-link, like a plain verse's (_verse_row).
            anchor = f"c{ch}v{v}"
            ref_attr["id"] = anchor
            ref_content = H.anchor(ref_text, {"href": f"#{anchor}"})
        else:
            ref_content = ref_text
        ref_cell = H.table_datum(ref_content, ref_attr)
        if view.suffix == clc_dual_cant.SUFFIX_COMBINED:
            # The combined row also carries the verse's both-strands one-letter divergence notes
            # (rafe/dagesh, QUPO — clc_dual_cant attaches them here, not to the strands): highlight
            # each such atom's word in the text column and append its note to the doc column.
            div_targets = {n["atom_index"] for n in view.notes}
            text_cell = H.table_datum(
                _text_contents(
                    ch, v, view.atoms, notes_by_atom, page_label, div_targets
                ),
                {**_HBO_ATTR, "class": "clc-text"},
            )
            doc_blocks = _doc_contents(ch, v, view.atoms, notes_by_atom)
            doc_blocks.extend(_combined_divergence_block(n) for n in view.notes)
            doc_cell = H.table_datum(doc_blocks, {"class": "clc-doc"})
        else:
            # De-highlight against the OTHER strand (the two strands agree here),
            # not the combined form — see _plain_text_contents.
            other = next(vw for vw in strands if vw is not view)
            text_cell = H.table_datum(
                _plain_text_contents(
                    view.atoms, other.atoms, _strand_noted_indices(view)
                ),
                {**_HBO_ATTR, "class": "clc-text"},
            )
            doc_cell = H.table_datum(
                _strand_doc_contents(view, page_label), {"class": "clc-doc"}
            )
        rows.append(H.table_row((text_cell, ref_cell, doc_cell)))
    return rows


def _strand_doc_contents(view, page_label):
    # The strand label, then this strand's synthesized notes (clc_dual_cant._strand_notes):
    # one "added out of thin air" note per SUPPLIED punctuation mark, and one note per accent
    # the strand wants but UXLC OMITTED (noted, never supplied — §7.7). Each is now a
    # first-class TARGETED note like a normal verse's (_note_block): a header repeating the
    # target word, then the note prose (which no longer names the word inline — §7.7). Notes
    # are grouped by atom so an atom with more than one note shares a single header.
    contents = [H.span(view.doc_label, {"class": "clc-strand-label"})]
    for atom_notes in _group_strand_notes(view.notes):
        contents.append(H.line_break())
        contents.append(_strand_note_block(atom_notes, page_label))
    return contents


def _group_strand_notes(notes):
    # Group a strand's synthesized notes by their target atom, preserving atom order, so all
    # notes on one word render under one header (mirrors _group_by_atom for normal verses).
    grouped = {}
    for note in notes:
        grouped.setdefault(note["atom_index"], []).append(note)
    return [grouped[k] for k in sorted(grouped)]


def _stripped_heading(word):
    # The target word as a note's heading, DEMOTED to bare letters (issue UXLC-utils#48,
    # clc_strip.strip_to_bare_letters): every point and accent dropped, keeping only the
    # word-level punctuation maqaf/sof-pasuq/legarmeh. Default font — NO lang="hbo" wrapper
    # (that exists only to font-and-size *pointed* Hebrew in Taamey; bare letters don't need
    # it and read fine in the default font). dir="rtl" isolates the Hebrew from the em dash
    # and English that follow it on the same line (see _headed_note), so those neutral
    # characters resolve into the surrounding LTR doc column rather than flipping around the
    # word.
    return H.span(clc_strip.strip_to_bare_letters(word), {"dir": "rtl"})


def _headed_note(heading, bodies):
    # Assemble one target-as-heading note (§7.7). The demoted heading opens the note; the
    # FIRST note body follows on the SAME line, set off by a space-surrounded em dash; any
    # SUBSEQUENT bodies become bullets. This is the layout MAM-with-doc uses for a
    # multi-paragraph doc-note (mb_misc/py_misc mwd_utils._bido_or_self_contained: the lemma
    # + first part render inline, parts 1.. as a <ul>) — CLC only swaps MAM's plain-space
    # lemma/part join for an em dash. ``bodies`` is a non-empty list; each body is itself a
    # list of inline pieces (str / htel).
    entries = [heading, " — ", *bodies[0]]
    if len(bodies) > 1:
        entries.append(H.unordered_list(bodies[1:], {"class": "clc-note-parts"}))
    return H.div(entries, {"class": "clc-note"})


def _strand_note_block(atom_notes, page_label):
    # A dual-cant strand note, promoted to the same headed shape a normal verse note has
    # (_note_block): the target word as a heading, then each note body — the first on the
    # heading line (em-dash-joined), any others as bullets (_headed_note). The word is pulled
    # out of the prose here, so the bodies read "The elyon strand calls for a silluq here …"
    # rather than "… on תרצח here …" (design doc §7.7).
    bodies = []
    for note in atom_notes:
        if note["source"] in (
            clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT,
            clc_note.SOURCE_DUAL_CANT_OMITTED_VOWEL,
        ):
            # An omitted *vowel* (Deut 5:8's elyon מתחת) shares the omitted-accent note's dict
            # shape and identical "calls for … but the LC has only …" wording, so it renders
            # through the very same body — only the mark category (a vowel) differs.
            bodies.append(_omitted_note_body(note, page_label))
        else:
            bodies.append(_added_note_body(note))
    return _headed_note(_strand_note_header(atom_notes[0]), bodies)


def _strand_note_header(note):
    # The target word repeated as the note's heading, DEMOTED to bare letters like every
    # other target-as-heading note (_stripped_heading). For a SUPPLIED-mark note the heading
    # still shows the mark CLC supplies — kept in its square brackets right after the word —
    # but as PLAIN text: the "added, not in the codex" green formatting (_added_span) is
    # dropped, so the whole heading is one bare Unicode string (e.g. פני[׃]) in the default
    # font. An omitted-accent note adds nothing, so its heading is just the bare word.
    bare = clc_strip.strip_to_bare_letters(note["snippet"])
    if note["source"] == clc_note.SOURCE_DUAL_CANT_ADDITION:
        bare += "[" + note["char"] + "]"
    return H.span(bare, {"dir": "rtl"})


_LC_CORROBORATED_LINK = (
    "https://bdenckla.github.io/wlc-utils/accgram/supplied-marks.html"
)

# The exact URL-fragment on that page for each corroborated case's own "Supplied accents"
# block (wlc-utils supplied_marks._anchor_id), so the long-note deep-links straight to it
# rather than the page top. The fragment CANNOT be derived from CLC's own (strand, kind):
# the two repos frame the same under-bar oppositely -- wlc-utils names the accent it
# *supplied*, CLC the accent UXLC *omitted* -- so both differ. Deut 5:17 is the stark case:
# CLC's "elyon silluq" (omitted) is wlc-utils's "taxton tipexa" (supplied), hence its
# ...-alef-tipexa fragment, not ...-bet-silluq. Keyed like _LC_CORROBORATED / _HAS_LONG_NOTE.
_SUPPLIED_MARKS_ANCHOR = {
    ("Exodus", 20, 3, "taḥton", "merkha"): "supplied-ex20v3-alef-merkha",
    ("Deuter", 5, 6, "elyon", "tipeḥa"): "supplied-dt5v6-bet-tipexa",
    ("Deuter", 5, 6, "elyon", "etnaḥta"): "supplied-dt5v6-bet-atnax",
    ("Deuter", 5, 17, "elyon", "silluq"): "supplied-dt5v17-alef-tipexa",
}


def _is_softened_meteg(note):
    # True for the Deut 5:7-shaped case: an omitted *meteg* takes softened wording
    # (_omitted_meteg_sentence), which never carries a "beyond the limits of CLC's
    # charity" clause to begin with (see that helper for why) -- so it is exempt from
    # the relegation _charity_limit_paragraph/_omitted_note_inline_pieces do below.
    return note["kind"] == "meteg" and note.get("present_kind")


def _omitted_note_core(note):
    # "A(n) <accent> is expected here, but UXLC's combined text carries only the <other>'s
    # <present accent>" — the front clause is passive ("is expected"), dropping the explicit
    # naming of the strand that wants the accent (it's recoverable: the *other* strand from the
    # one the LC actually has) and the verb "calls for"; the possessive sheds "strand" too
    # (issue UXLC-utils#54). NO bracketed mark (nothing is added to the
    # strand; cf. _added_note_body). The target word is NOT named inline: it is repeated as
    # this note's own header instead (_strand_note_header), making the note a first-class
    # targeted note like a normal verse's (§7.7). The accent UXLC *does* have is named, not
    # abstracted. Accents are noted, never supplied (§7.7).
    #
    # "the LC has only..." (crediting the manuscript, not just UXLC's own transcription of it)
    # replaces "UXLC's combined text carries" whenever this note is grounded beyond CLC's own
    # synthesis: either wlc-utils's grammar-checker corroboration (issue UXLC-utils#36,
    # clc_dual_cant._LC_CORROBORATED) or an editor-attached long note making its own independent
    # case (clc_dual_cant._HAS_LONG_NOTE) — e.g. Deut 5:13's taxton pashta, whose long note cites
    # UXLC's own note citing BHL Appendix A. A long note attached here is expected to itself
    # justify that stronger claim, not just restate CLC's own reasoning at length.
    #
    # This is the shared opening every *non-meteg* omitted-accent note has, split out from the
    # "and it is beyond the limits of CLC's charity to supply the missing X" clause that used to
    # always follow it (_omitted_note_sentence) so that clause can be relegated to the long-notes
    # page on its own (_charity_limit_paragraph) whenever a long note is attached, while this core
    # keeps showing inline (_omitted_note_inline_pieces).
    article = "An" if note["kind"][:1] in "aeiou" else "A"
    grounded = note.get("lc_corroborated", False) or note.get("has_long_note", False)
    carries = "the LC has" if grounded else "UXLC’s combined text carries"
    has = (
        f"only the {note['other_strand']}’s {note['present_kind']}"
        if note.get("present_kind")
        else f"no accent for the {note['strand']} strand"
    )
    return [
        f"{article} {note['kind']} is expected here, but {carries} {has}",
    ]


def _omitted_note_sentence(note):
    # The FULL sentence — core + "and it is beyond the limits of CLC's charity to supply the
    # missing <accent>" — used wherever that full reasoning is wanted in one place: the
    # long-notes page always shows it (_charity_limit_paragraph), and so does the main page's
    # own inline note when no long note exists to relegate it to
    # (_omitted_note_inline_pieces). A missing *meteg* takes different, already-full,
    # softened wording (_omitted_meteg_sentence) instead — see _is_softened_meteg.
    if _is_softened_meteg(note):
        return _omitted_meteg_sentence(note)
    return [
        *_omitted_note_core(note),
        f", and it is beyond the limits of CLC’s charity to supply the missing {note['kind']}.",
    ]


def _omitted_meteg_sentence(note):
    # Softened wording for an omitted *meteg* (the strand wants a meteg U+05BD where UXLC's
    # single mark is the OTHER strand's accent). Unlike the accent path in _omitted_note_
    # sentence, this does NOT say the strand "calls for" the mark, nor that CLC's charity
    # declines to "supply the missing meteg." A meteg (gaʿya) is metrical, not part of the
    # cantillation/trope system, and even the gaʿyot usually deemed obligatory are not
    # consistently written in the manuscripts; the special gaʿya on יהיה-type verbs (Deut
    # 5:7's יִהְיֶה־) is not clearly of the obligatory kind at all (cf. Yeivin, ITM). So the
    # situation is not a wanted-but-withheld accent but a single manuscript mark that CLC must
    # transcribe one way or the other: it reads that mark as the OTHER strand's accent, which
    # — unlike the meteg — the chant truly needs. Where an editor attaches a long note (§7.3,
    # clc_dual_cant._HAS_LONG_NOTE), _omitted_note_body links to its further discussion.
    present = note["present_kind"]
    article = "an" if present[:1] in "aeiou" else "a"
    # The word is not named inline — it is this note's header (_strand_note_header) — so the
    # sentence reads "… here, but the LC has only a single mark …" (§7.7).
    return [
        f"A meteg might be expected in the {note['strand']} strand here, but the LC has only a"
        f" single mark, which is best transcribed as {article} {present} since, unlike the"
        f" meteg, the {present} is truly needed.",
    ]


def _omitted_note_inline_pieces(note):
    # What actually renders inline (main-page doc column, and the long-notes page's own
    # verbatim recap of it — _build_long_note_entry). Once a long note is attached
    # (has_long_note), the "and it is beyond the limits of CLC's charity to supply the
    # missing X" clause relegates there ENTIRELY (_charity_limit_paragraph) — this returns
    # just the truncated core instead. The softened meteg wording never had that clause to
    # begin with, so it renders in full regardless of has_long_note.
    if note.get("has_long_note") and not _is_softened_meteg(note):
        return [*_omitted_note_core(note), "."]
    return list(_omitted_note_sentence(note))


def _charity_limit_paragraph(note):
    # The "and it is beyond the limits of CLC's charity to supply the missing X" clause,
    # relegated here in full once a long note exists to hold it (design doc §7.3) — None
    # for the softened meteg wording, which never phrased it that way (_is_softened_meteg).
    if _is_softened_meteg(note):
        return None
    return H.para(
        [
            f"It is beyond the limits of CLC’s charity to supply the missing {note['kind']}."
        ]
    )


def _omitted_note_body(note, page_label):
    # The omitted-accent/vowel note body: a list of inline pieces (the sentence), plus — when
    # a long note is attached (clc_dual_cant._HAS_LONG_NOTE) — a link to this note's own
    # long-notes-page entry. That page holds e.g. an lc_corroborated note's wlc-utils
    # grammar-checker citation, and its "beyond the limits of CLC's charity" clause, ONLY
    # there (§7.3), never inline; this pointer is all that remains here.
    contents = _omitted_note_inline_pieces(note)
    if note.get("has_long_note"):
        book_id, ch, v = note["verse_loc"]
        anchor = clc_long_note.anchor_id(book_id, ch, v, note["strand"], note["kind"])
        contents.extend(
            [
                " See more details in ",
                H.anchor(
                    "this longer note",
                    {"href": clc_long_note.page_href(page_label, anchor)},
                ),
                ".",
            ]
        )
    return contents


def _added_note_body(note):
    # The supplied-mark note body: "<name> added to improve legibility". The target word and
    # its bracketed mark are the note's heading (_strand_note_header), so the body no longer
    # names the word inline (§7.7). This makes the supplied-mark note a first-class targeted
    # note like a normal verse's, matching the omitted-accent notes beside it.
    return [f"{note['kind']} added to improve legibility"]


def _combined_divergence_block(note):
    # A both-strands one-letter divergence (§7.7, issue UXLC-utils#47) — rafe/dagesh or the QUPO vowel split
    # — rendered ONCE on the combined (-C) row's doc column, naming both strands and the shared
    # letter. Now a first-class TARGET-AS-HEADING note like the omitted-accent/supplied-mark strand
    # notes beside it (_strand_note_block / _note_block): the target word is the note's HEADING and
    # the body no longer names it inline (§7.7). The heading is STRIPPED to its bare letters (issue
    # UXLC-utils#48, clc_strip.strip_to_bare_letters) — e.g. פָּנָֽ͏ַ֗י → פני, כָּל־ → כל־ — while the -C text
    # column still shows the real fully-pointed word (that highlight is untouched). The body still
    # names the specific letter (the header word has several) and gives just the bare visual fact —
    # which mark each strand has on that letter — with plain "has": no phonetics (hard/soft), no
    # cause (the accent driving a rafe/dagesh), no sourcing of the marks (not "UXLC's"). e.g. body
    # "On the נ, the taxton strand has a qamats but the elyon strand has a patax." / "On the ת, the
    # taxton strand has a rafe but the elyon strand has a dagesh." Nothing is added to any strand's
    # text, so no green/bracketed mark. The bare-letter heading carries NO lang="hbo" wrapper (that
    # exists to font-and-size pointed Hebrew in Taamey, which bare letters don't need — they render
    # in the default font); it keeps only a dir="rtl" span, to isolate the Hebrew from the em dash
    # and English that follow it on the note's line (_stripped_heading).
    a_has, b_has = _divergence_has(note)
    body = [
        f"On the {note['letter']}, the {note['a_strand']} strand has {a_has}"
        f" but the {note['b_strand']} strand has {b_has}.",
    ]
    return _headed_note(_stripped_heading(note["word"]), [body])


def _divergence_has(note):
    # The two "has …" phrases (alef strand, bet strand). QUPO: each strand's own vowel. Rafe/dagesh:
    # the mark on the shared letter — "a dagesh", "a rafe", or "neither dagesh nor rafe" (a bare
    # letter, e.g. ex 20:9 כל). Spelling "rafe" (not describe_diff's canonical "rafeh") is deliberate
    # per Ben's preference (2026-07-05); "dagesh" already matches the canonical name.
    if note["source"] == clc_note.SOURCE_DUAL_CANT_QUPO_VOWEL:
        return f"a {note['a_vowel']}", f"a {note['b_vowel']}"
    return _rd_phrase(note["a_state"]), _rd_phrase(note["b_state"])


def _rd_phrase(state):
    if state == "dagesh":
        return "a dagesh"
    if state == "rafe":
        return "a rafe"
    return "neither dagesh nor rafe"  # bare — the letter carries no dagesh and no rafe


def _strand_ref_attr(tooltip, pos, count):
    # Group the strand rows into one verse block: the first row keeps the top
    # divider, the last keeps the bottom one, the middle rows drop both.
    classes = ["clc-ref", "clc-ref-strand"]
    if pos == 0:
        classes.append("clc-strand-first")
    if pos == count - 1:
        classes.append("clc-strand-last")
    return {"class": " ".join(classes), "title": tooltip}


def _text_contents(ch, v, verse, notes_by_atom, page_label, extra_targets=()):
    # Group ketiv/qere atoms into units (clc_kq) so each renders as one boxed
    # ruby — qere on the baseline, ketiv above — and adjacent independent pairs
    # stay visibly separate from a grouped multi-word unit. Plain words render as
    # a highlight if noted (see _noted_word), otherwise bare text. ``extra_targets`` is a set of
    # 1-based atom positions to ALSO highlight though they carry no ClcNote — used on the combined
    # (-C) row for a both-strands divergence note (rafe/dagesh, QUPO) whose block sits in the same
    # doc cell (so a plain span, no link, like any same-row note — §7.3).
    pieces = []
    for item in clc_kq.iter_render_units(verse):
        if isinstance(item, clc_kq.KqUnit):
            pieces.append(clc_kq.kq_ruby(item, notes_by_atom, ch, v))
            _append_join_space(pieces, clc_kq.join_text(item))
        else:
            atom_notes = notes_by_atom.get((ch, v, item.position))
            if not atom_notes and item.position in extra_targets:
                pieces.append(H.span(item.text, {"class": "clc-doc-target"}))
            else:
                pieces.append(_noted_word(item.text, atom_notes, page_label))
            _append_join_space(pieces, item.text)
    return pieces


def _noted_word(text, atom_notes, page_label):
    # A word carrying at least one note is HIGHLIGHTED in the text column (clc-doc-
    # target, design doc §7.3) so the reader can see which words are annotated. It is
    # NOT a same-page link: the note sits in the same row's doc cell, right beside the
    # word, so there is nothing to jump to (a short note is always in the visual
    # vicinity of its target). The sole exception is a note relegated ENTIRELY to the
    # separate long-notes page — then the highlight is a real anchor pointing ACROSS to
    # that page's body (design doc §7.3).
    if not atom_notes:
        return text
    href = _relegated_page_href(atom_notes, page_label)
    if href:
        return H.anchor(text, {"href": href, "class": "clc-doc-target"})
    return H.span(text, {"class": "clc-doc-target"})


def _relegated_anchor(note):
    # Non-None iff this UXLC x-note is relegated to the long-notes page instead of an
    # inline same-row block (design doc §7.3, case-by-case — see _LONG_NOTE_SPECS).
    return _UXLC_NOTES_RELEGATED.get(
        (note.book, note.ch, note.v, note.atom_index, note.note_code)
    )


def _relegated_page_href(atom_notes, page_label):
    # Non-None only when EVERY note on this atom is relegated to the long-notes page
    # (design doc §7.3) — then the highlighted word links ACROSS to that page's anchored
    # body. If any note still renders inline in the same-row doc cell, there is no jump
    # target (same-page notes no longer carry anchors — they sit right beside the word),
    # so return None and _noted_word highlights the word as a plain span.
    if any(_relegated_anchor(n) is None for n in atom_notes):
        return None
    anchors = {_relegated_anchor(n) for n in atom_notes}
    n0 = atom_notes[0]
    assert len(anchors) == 1, (
        n0.ch,
        n0.v,
        n0.atom_index,
        anchors,
    )  # one atom, one long note
    (anchor,) = anchors
    return clc_long_note.page_href(page_label, anchor)


def _plain_text_contents(strand_atoms, other_atoms, noted_indices=()):
    # Like _text_contents but with no note always-links — used by the alef/bet
    # strand rows of a dual-cant verse, whose notes/anchors live on the combined
    # row only (re-emitting them here would duplicate anchor ids). Each word
    # identical across the two strands (taxton == elyon — i.e. not a divergence
    # atom) is de-highlighted (clc-strand-same) so the few divergence words stand
    # out by contrast. A word that differs from the OTHER strand stays highlighted
    # — including one equal to the combined form yet diverging from its sibling
    # (e.g. ex 20:9 כל, whose taxton keeps a dagesh elyon drops), and one carrying a
    # SUPPLIED mark (clc_dual_cant additions) the other strand lacks; any supplied
    # mark is rendered bracketed/green right after the word.
    #
    # A word whose 1-based atom position is in ``noted_indices`` is additionally given the
    # clc-doc-target highlight, exactly like a noted word in a normal verse (_noted_word) — so
    # the reader can see which strand words are annotated, not just which diverge. It is a plain
    # span, not a link: a strand note always keeps an inline block in the same row's doc cell, so
    # there is nothing to jump to (design doc §7.3/§7.7). Dropping same-page note anchors
    # — design doc §9 #6, not an issue — is what removed the id-collision constraint that
    # previously kept these strand words unhighlighted. Which atoms qualify is decided by the
    # caller (_strand_noted_indices): only omitted-accent notes, NOT supplied-mark notes, whose
    # green bracketed mark is its own flag.
    pieces = []
    for index, (strand_atom, other_atom) in enumerate(
        zip(strand_atoms, other_atoms), start=1
    ):
        atom_text = strand_atom["text"]
        additions = strand_atom.get("additions", ())
        same_across_strands = atom_text == other_atom["text"] and tuple(
            additions
        ) == tuple(other_atom.get("additions", ()))
        if index in noted_indices and not same_across_strands:
            # One clc-doc-target span over the WHOLE atom — the word AND its bracketed supplied
            # marks — so the highlight reads as a single unit (conceptually all of "לֹא[־]").
            # The supplied mark GLYPH keeps its green (clc-added-during-detangling sets an
            # explicit color, which wins over the inherited highlight color); its brackets
            # (clc-added-bracket: color inherit) and the word take the highlight color.
            pieces.append(
                H.span(
                    [atom_text, *(_added_span(added) for added in additions)],
                    {"class": "clc-doc-target"},
                )
            )
            _append_join_space(pieces, additions[-1] if additions else atom_text)
            continue
        if same_across_strands:
            pieces.append(H.span(atom_text, {"class": "clc-strand-same"}))
        else:
            pieces.append(atom_text)
        for added in additions:
            pieces.append(_added_span(added))
        _append_join_space(pieces, additions[-1] if additions else atom_text)
    return pieces


def _strand_noted_indices(view):
    # 1-based atom positions of ALL of ``view``'s strand notes — the words to highlight
    # (clc-doc-target) as note targets in this strand's text column (clc_dual_cant tags each
    # note with atom_index), both omitted-accent and supplied-mark. A supplied-mark note is
    # included too: its whole atom (word + brackets) takes the highlight as one unit, while the
    # supplied mark GLYPH itself stays green — the cascade lets clc-added-during-detangling's
    # explicit green win over the inherited highlight color (see _plain_text_contents). So it
    # is the literal maqaf/sof-pasuq that stays green, not the surrounding brackets or word.
    return {note["atom_index"] for note in view.notes}


def _added_span(added_char):
    # A maqaf/sof-pasuq SUPPLIED to this strand for legibility (clc_dual_cant):
    # bracketed, the mark itself green (clc-added-during-detangling) to flag
    # "added, not in the codex". Brackets stay in running-text color.
    return H.span(
        ["[", H.span(added_char, {"class": "clc-added-during-detangling"}), "]"],
        {"class": "clc-added-bracket"},
    )


def _append_join_space(pieces, join_key):
    # Smart-join: a unit ending in maqaf butts directly against the next (one
    # hyphenated compound, e.g. אֶת־הָאָרֶץ); add_wbr still allows a line break at
    # the maqaf. `join_key` is the unit's text — or, for a strand atom that
    # SUPPLIES a trailing mark, that mark — so a supplied maqaf butts while a
    # supplied sof-pasuq still gets a following space. Only non-maqaf units get one.
    if not join_key.endswith(hpu.MAQ):
        pieces.append(" ")


def _doc_contents(ch, v, verse, notes_by_atom):
    blocks = []
    for atidx, _atom in enumerate(verse):
        position = atidx + 1
        atom_notes = notes_by_atom.get((ch, v, position))
        if not atom_notes:
            continue
        visible = [n for n in atom_notes if _relegated_anchor(n) is None]
        if visible:
            blocks.append(_note_block(visible))
    return blocks


def _note_block(atom_notes):
    # Opens with the atom text repeated as a heading, DEMOTED to bare letters like every
    # target-as-heading note (_stripped_heading), then each note body — the first on the
    # heading line (em-dash-joined), any others as bullets (_headed_note). No id anchor: the
    # always-link that used to jump here was dropped (see _noted_word) — the block sits in the
    # same row as its highlighted target word, so the reader has nothing to jump from.
    heading = _stripped_heading(atom_notes[0].atom_text)
    return _headed_note(heading, [_note_body(note) for note in atom_notes])


def _note_body(note):
    # One normal-verse note's body: a list of inline pieces. A UXLC-departure note reads as a
    # plain sentence (_departure_note_body); every other note is the UXLC note itself —
    # "[code] text — cite", or a superseding-change cite in place of the text.
    if note.is_uxlc_departure:
        return _departure_note_body(note)
    pieces = [H.span(f"[{note.note_code}] ", {"class": "clc-note-code"})]
    if note.superseding_uxlc_change:
        pieces.append(
            clc_attribution.superseding_change_cite(note.superseding_uxlc_change)
        )
    else:
        pieces.append(note.note_text)
        pieces.append(clc_attribution.note_cite(note.source_url))
    return pieces


def _departure_note_body(note):
    # States plainly that CLC replaced UXLC's own reading (never "shared" -- that
    # framing was rejected), naming the two marks via _accent_diff_names rather than
    # hardcoding "pashta"/"qadma" so this reads correctly if reused for a different
    # mark pair later. No note-code prefix or Hebrew snippets -- those belong to
    # showing the UXLC note itself, which this note deliberately doesn't (its whole
    # point is that CLC now departs from UXLC here) -- but "pending change" itself
    # links to the UXLC change record, reusing clc_attribution's link builder.
    old_name, new_name = _accent_diff_names(note.uxlc_reading, note.clc_reading)
    return [
        f"Here CLC replaces UXLC's {old_name} with a {new_name}. UXLC has a ",
        clc_attribution.change_record_link(
            note.superseding_uxlc_change, "pending change"
        ),
        " making this correction.",
    ]


def _accent_diff_names(uxlc_reading, clc_reading):
    # Diff the two same-length readings at their single differing character, naming
    # each via the canonical mb_diff_mpu authority (mirrors clc_dual_cant's own
    # _accent_name/_present_accent pattern) -- so this note never hardcodes
    # "pashta"/"qadma" and stays correct if reused for a different departure later.
    assert len(uxlc_reading) == len(clc_reading), (uxlc_reading, clc_reading)
    diffs = [(a, b) for a, b in zip(uxlc_reading, clc_reading) if a != b]
    assert len(diffs) == 1, (uxlc_reading, clc_reading, diffs)
    old_char, new_char = diffs[0]
    return describe_diff.accent_name(old_char), describe_diff.accent_name(new_char)


_BHL_TITLE = "Dotan’s Biblia Hebraica Leningradensia"
_WLC_TITLE = "Westminster Leningrad Codex"
_BHS_TITLE = "Biblia Hebraica Stuttgartensia"


def _dt_5_13_taxton_extra(_spec, _book, notes):
    # "See the UXLC note on this word. The lack of this pashta is noted in BHL
    # Appendix A." -- UXLC's own Deut 5:13.2-t note (suppressed inline, see
    # _UXLC_NOTES_RELEGATED below) already says as much ("BHL Appendix A has no
    # pashta on the final mem."); this just surfaces that citation instead of
    # reproducing the note's full text a second time.
    #
    # Second paragraph: the flip side of that same absence. wlc-utils's grammar checker
    # (the accgram detangler) supplies a strand's missing accent so it parses -- but it
    # never had to for this pashta, because WLC already carries it (wrongly). Named
    # generically as "the grammar checker" per Ben; the BHS-origin guess stays hedged.
    uxlc_note = next(
        n
        for n in notes
        if (n.book, n.ch, n.v, n.atom_index, n.note_code) == ("Deuter", 5, 13, 2, "t")
    )
    # A list of paragraphs (each a list of inline pieces).
    return [
        [
            "See the ",
            H.anchor("UXLC note", {"href": uxlc_note.source_url, "target": "_blank"}),
            " on this word. The lack of this pashta is noted in ",
            H.abbr("BHL", {"title": _BHL_TITLE}),
            " Appendix A.",
        ],
        [
            "This pashta is not among the accents the grammar checker has to supply"
            " to ",
            H.abbr("WLC", {"title": _WLC_TITLE}),
            " when detangling the two strands: it is already"
            " present in WLC — erroneously, presumably carried over from ",
            H.abbr("BHS", {"title": _BHS_TITLE}),
            ", though this has not yet been verified.",
        ],
    ]


# Yeivin, Introduction to the Tiberian Masorah §355 (the special "phonetic" gaʿya of
# היה/חיה-root forms), in Ben's adaptation on phonetic-hbo. House style for such deep
# links is a "section NNN" anchor (cf. MAM-basics rocc_4_mid_word_ga3ya_with_shewa).
_YEIVIN_ITM_355_URL = (
    "https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns355"
)


def _dt_5_7_elyon_meteg_extra(_spec, _book, _notes):
    # Why the elyon's missing mark here is treated as an optional meteg, not a wanted
    # accent (see _omitted_meteg_sentence for the short-note wording this expands on):
    # the mark is the special gaʿya of היה/חיה-root forms, whose marking Yeivin (ITM §355)
    # calls inconsistent across manuscripts and absent from the xillufim lists.
    #
    # The one caveat Yeivin adds — this gaʿya IS "as a rule" marked when the word is joined by
    # maqqef to an *initially-stressed* following word — may or may not cover Deut 5:7 (יהיה־לך).
    # Do NOT adjudicate it: an earlier draft claimed לך is "final-stressed, not initial," so the
    # exception fails — but whether Yeivin counts לך as initially stressed is genuinely unclear
    # (it turns on whether he reckons syllable/stress in modern or Masoretic terms — e.g. a vocal
    # shewa forming no syllable of its own would make לְךָ pattern with his monosyllables). Per
    # Ben, we do NOT litigate that in the note. Either way CLC's move stands: a gaʿya is metrical
    # (not an accent), "as a rule" is not "always," and — decisively — the one mark the LC
    # actually carries is the taxton's merkha, which the chant needs; CLC reads the mark as that
    # merkha and invents no second one for the gaʿya. No inline UXLC x-note is relegated for this
    # one. The rendered note keeps none of this argument in prose: it is just a one-sentence
    # pointer to Yeivin ITM §355 (where his own "as a rule" caveat lives) plus the aside below.
    #
    # Closing aside (paired with the LC folio-102A detail image this spec carries): the mark
    # is this note's main subject, but the word's own initial yod is a separate act of
    # charity — most of its top has flaked off, and it is read from the faint
    # surviving remnants together with the context. Charity is CLC's central principle, so
    # it is worth surfacing even where the mark, not the letter, is the occasion for the note.
    #
    # Returns a list of paragraphs (each a list of inline pieces); see _build_long_note_entry.
    return [
        [
            "Regarding the meteg that might be expected on ",
            H.span("יִהְיֶה־", _HBO_ATTR),
            ", see ",
            H.anchor("section 355", {"href": _YEIVIN_ITM_355_URL, "target": "_blank"}),
            " of Yeivin’s Introduction to the Tiberian Masorah.",
        ],
        [
            "Aside: the mark transcribed as merkha is this note’s main subject,"
            " but it should be noted that the word’s initial yod is a charitable transcription,"
            " since most of the top of the yod seems to have flaked off."
            " This yod is transcribed as present based on"
            " expectation combined with"
            " the tail that did not flake off,"
            " plus the faint remnants that seem to have remained even after flaking.",
        ],
    ]


def _dt_5_8_elyon_patax_extra(_spec, _book, _notes):
    # The "further discussion" this note's short-note recap points to: the elyon מתחת's tav is
    # left bare because the LC has only the taxton's qamats there, never the patax the elyon's
    # chant wants (its ex 20:4 twin, a genuine QUPO split, does carry that patax). The one
    # alternative — lending the taxton's qamats to the elyon too — does not resolve the problem,
    # only reframes it (a qamats where a patax is wanted, rather than no vowel at all); either
    # way the LC's marks cannot yield the elyon's patax, so CLC notes it rather than inventing
    # it. This paragraph deliberately does NOT repeat the "beyond the limits of CLC's charity"
    # clause — _charity_limit_paragraph already prints it just above, on this same page.
    # Returns a list of paragraphs (each a list of inline pieces); see _build_long_note_entry.
    return [
        [
            "An alternative detangling would have lent the taḥton strand’s qamats to the"
            " elyon strand as well, rather than leaving the elyon strand’s tav bare. That"
            " would not resolve the difficulty, only reframe it: the elyon would then show a"
            " qamats where its chant calls for a pataḥ — as the parallel word in Exodus 20:4,"
            " where the two strands split the vowel outright, confirms. Whether the problem is"
            " put as “no vowel where a pataḥ is expected” or “a qamats where a pataḥ is"
            " expected,” the substance is the same: the Leningrad Codex never wrote the elyon’s"
            " pataḥ, so no detangling of the marks it does carry can give the elyon strand the"
            " vowel its chant wants.",
        ],
    ]


@dataclass(frozen=True)
class _LongNoteSpec:
    """One editor-opted-in long note (design doc §7.3) -- case-by-case, never an
    automatic length threshold. ``strand``/``kind`` locate the clc_dual_cant omitted-
    accent note this long note expands on (see clc_dual_cant._HAS_LONG_NOTE, which
    must independently list the same case); ``relegated_position``/``relegated_code``
    is the UXLC x-note this long note's own citation subsumes, so it is suppressed
    from its usual same-row doc-cell block instead of showing twice -- ``None``/``""``
    when this long note relegates no inline UXLC note (e.g. Deut 5:7's elyon meteg, pure
    further discussion). ``image_filename`` is a file under gh-pages/img/ (empty string
    for no image) -- fetched by hand, once, from the UXLC note's own detail image (see
    .novc/fetch_dt_5_13_2_t_image.py) and committed as a static asset, never re-downloaded
    at build time; ``image_credit`` is that source page's own credit line, carried forward
    alongside it. ``extra_blocks`` is ``(spec, book, notes) -> [H pieces]``, this note's own
    added content beyond the verse/short-note recap every long note gets automatically (it
    gets ``spec`` so e.g. _lc_corroborated_extra can pick its own supplied-marks #fragment).
    """

    book_id: str
    ch: int
    v: int
    strand: str
    kind: str
    relegated_position: object  # int, or None when no inline UXLC note is relegated
    relegated_code: str
    image_filename: str
    image_credit: str
    extra_blocks: object


def _lc_corroborated_extra(spec, _book, _notes):
    # Shared by all four _LC_CORROBORATED cases below (Exod 20:3, Deut 5:6 ×2, Deut 5:17):
    # the same wlc-utils grammar-checker citation (issue UXLC-utils#36) grounds every one of them
    # identically, so one boilerplate paragraph serves all four rather than bespoke
    # per-verse prose like 5:13's/5:7's. This citation used to be an inline "— see the
    # grammar checker's supplied accents page" link on the main page; it now lives here
    # only, with just a "See more details in this longer note" pointer left inline
    # (clc_render._omitted_note_body). The link carries a #fragment (per spec, via
    # _SUPPLIED_MARKS_ANCHOR) so it lands on this very case's block, not the page top.
    fragment = _SUPPLIED_MARKS_ANCHOR[
        (spec.book_id, spec.ch, spec.v, spec.strand, spec.kind)
    ]
    return [
        [
            "This omitted accent is independently corroborated by wlc-utils’s grammar"
            " checker — see its ",
            H.anchor(
                "supplied accents", {"href": f"{_LC_CORROBORATED_LINK}#{fragment}"}
            ),
            " page.",
        ]
    ]


_LONG_NOTE_SPECS = (
    _LongNoteSpec(
        "Deuter",
        5,
        13,
        "taḥton",
        "pashta",
        2,
        "t",
        "Deuter.5.13.2-t.jpg",
        "Sefaria.org",
        _dt_5_13_taxton_extra,
    ),
    _LongNoteSpec(
        "Deuter",
        5,
        7,
        "elyon",
        "meteg",
        None,
        "",
        "Deuter.5.7.2.LC-102A-col3-line22.jpg",
        "Sefaria.org",
        _dt_5_7_elyon_meteg_extra,
    ),
    _LongNoteSpec(
        "Exodus",
        20,
        3,
        "taḥton",
        "merkha",
        None,
        "",
        "",
        "",
        _lc_corroborated_extra,
    ),
    _LongNoteSpec(
        "Deuter",
        5,
        6,
        "elyon",
        "tipeḥa",
        None,
        "",
        "",
        "",
        _lc_corroborated_extra,
    ),
    _LongNoteSpec(
        "Deuter",
        5,
        6,
        "elyon",
        "etnaḥta",
        None,
        "",
        "",
        "",
        _lc_corroborated_extra,
    ),
    _LongNoteSpec(
        "Deuter",
        5,
        17,
        "elyon",
        "silluq",
        None,
        "",
        "",
        "",
        _lc_corroborated_extra,
    ),
    _LongNoteSpec(
        "Deuter",
        5,
        8,
        "elyon",
        "pataḥ",
        None,
        "",
        "",
        "",
        _dt_5_8_elyon_patax_extra,
    ),
)

# Derived from _LONG_NOTE_SPECS: (book, ch, v, atom_index, note_code) -> long-note
# anchor id, consulted by _relegated_anchor/_relegated_page_href/_doc_contents to suppress
# a relegated UXLC x-note's inline block and redirect its highlight link. Only specs that
# actually relegate an inline UXLC note participate (relegated_position is not None) --
# a pure-further-discussion long note like Deut 5:7's elyon meteg subsumes nothing.
_UXLC_NOTES_RELEGATED = {
    (
        spec.book_id,
        spec.ch,
        spec.v,
        spec.relegated_position,
        spec.relegated_code,
    ): clc_long_note.anchor_id(spec.book_id, spec.ch, spec.v, spec.strand, spec.kind)
    for spec in _LONG_NOTE_SPECS
    if spec.relegated_position is not None
}


def build_long_notes(book_id, book, notes, chapters=None):
    """Build this build job's long-note page entries (design doc §7.3), for the
    caller (main_clc.py) to hand straight to clc_long_note.write_page as this job's
    own long-notes page. ``book``/``notes`` are collect_for_book's own return values --
    reused here, never re-read from disk. ``chapters`` mirrors write_book's own
    chapter limit."""
    entries = []
    for spec in _LONG_NOTE_SPECS:
        if spec.book_id != book_id:
            continue
        if chapters is not None and spec.ch not in chapters:
            continue
        entries.append(_build_long_note_entry(spec, book, notes, chapters))
    return entries


def _build_long_note_entry(spec, book, notes, chapters):
    verse_atoms = book[spec.ch - 1][spec.v - 1]
    views = clc_dual_cant.strand_views(spec.book_id, spec.ch, spec.v, verse_atoms)
    strands = [vw for vw in views if vw.suffix != clc_dual_cant.SUFFIX_COMBINED]
    view, note = _find_strand_note(strands, spec.strand, spec.kind)
    other = next(vw for vw in strands if vw is not view)
    anchor = clc_long_note.anchor_id(
        spec.book_id, spec.ch, spec.v, spec.strand, spec.kind
    )
    # The kind suffix disambiguates a verse+strand with more than one long note (Deut
    # 5:6's elyon wants both a tipexa and an etnaxta) -- without it, both would show the
    # identical heading "Deuter 5:6 — elyon strand" with nothing to tell them apart.
    heading = f"{spec.book_id} {spec.ch}:{spec.v} — {view.doc_label} ({spec.kind})"
    verse_recap = H.para(
        [
            H.span(
                _plain_text_contents(
                    view.atoms, other.atoms, _strand_noted_indices(view)
                ),
                _HBO_ATTR,
            )
        ]
    )
    # Labeled so a reader landing here from the always-link (not from the short note's
    # own "see more details" link) can tell which part is a verbatim recap of what the
    # main page already says, versus the content that's new to this page. "main page"
    # itself is the back-link to that page -- same label/href scheme write_book uses to
    # name its own output file (out_label), so this always matches the file actually built
    # for spec's book/chapters, whether or not it happens to be chapter-limited.
    main_page_href = f"{out_label(spec.book_id, chapters)}.html"
    short_recap = H.para(
        [
            "Inline note (repeated from ",
            H.anchor("main page", {"href": main_page_href}),
            "): ",
            *_omitted_note_inline_pieces(note),
        ]
    )
    # extra_blocks returns a list of paragraphs (each a list of inline pieces); the
    # "Further discussion:" label leads the first, the rest (e.g. Deut 5:7's aside) follow.
    para_contents = spec.extra_blocks(spec, book, notes)
    extra_paras = [H.para(["Further discussion: ", *para_contents[0]])]
    extra_paras += [H.para(pc) for pc in para_contents[1:]]
    blocks = [verse_recap, short_recap]
    charity_para = _charity_limit_paragraph(note)
    if charity_para is not None:
        blocks.append(charity_para)
    if spec.image_filename:
        blocks.append(_long_note_image(spec))
    blocks.extend(extra_paras)
    return clc_long_note.entry(anchor, heading, blocks)


def _long_note_image(spec):
    # The image sits between the short-note recap and the further discussion it
    # illustrates. gh-pages/clc/<label>-long-notes.html -> gh-pages/img/ is one level up.
    return H.div(
        [
            H.img(
                {
                    "src": f"../img/{spec.image_filename}",
                    "alt": f"Manuscript detail for {spec.book_id} {spec.ch}:{spec.v}",
                    "class": "clc-long-note-img",
                }
            ),
            H.para(
                [f"Credit: {spec.image_credit}."], {"class": "clc-long-note-img-credit"}
            ),
        ],
        {"class": "clc-long-note-img-wrap"},
    )


def _find_strand_note(strands, strand, kind):
    for view in strands:
        for note in view.notes:
            if note.get("strand") == strand and note.get("kind") == kind:
                return view, note
    raise LookupError((strand, kind))


def _body_wrapper(book_id, table):
    # The "clc-main-page" class is a hook for gh-pages/style.css to widen <body> itself
    # (past its site-wide 40em cap) on these pages only -- the long-notes page carries no
    # such class, so it stays at the site-wide width. Widening the page is what actually
    # lets td.clc-doc's own wider max-width (gh-pages/style.css) render wider, instead of
    # squeezing the text/ref columns to make room.
    style = "max-width: 60rem; margin-left: auto; margin-right: auto"
    contents = [
        H.heading_level_1(f"Charitable Leningrad Codex — {book_id}"),
        clc_attribution.top_credit(),
        table,
    ]
    return [H.div(contents, {"style": style, "class": "clc-main-page"})]
