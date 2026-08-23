"""Test for clc_collect (the CLC note-collection module).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/clc_collect_test.py

Covers clc_collect's pending-UXLC-change patch (_UXLC_PENDING_CHANGES_APPLIED):
Deut 5:8.2's mid-word pashta is corrected to a qadma upstream, before any note or
strand split ever runs — CLC's first-ever real is_uxlc_departure=True instance
(design doc §7.4), and the first real UXLC-text departure the strand oracle
(clc_dual_cant) sees, rather than an omitted-accent annotation.
"""

import clc.clc_collect as clc_collect
import clc.clc_dual_cant as clc_dual_cant
import clc.clc_long_note as clc_long_note
import clc.clc_note as clc_note
import clc.clc_render as clc_render
import mb_cmn.hebrew_accents as acc
import mb_cmn.hebrew_points as hpo
import uxlc_misc.uxlc_utils_html as H


def _deut_5_8_atom2_note(notes):
    matches = [n for n in notes if n.ch == 5 and n.v == 8 and n.atom_index == 2]
    assert len(matches) == 1, matches
    return matches[0]


def test_text_patch():
    book, _notes = clc_collect.collect_for_book("Deuter", chapters={5})
    atom = book[4][7][1]  # ch5, v8, atom-index 2 (0-based: [4][7][1])
    assert acc.QOM in atom["text"] and acc.PASH not in atom["text"], atom["text"]


def test_note_fields():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    note = _deut_5_8_atom2_note(notes)
    assert note.is_uxlc_departure is True
    assert acc.PASH in note.uxlc_reading and acc.QOM not in note.uxlc_reading
    assert acc.QOM in note.clc_reading and acc.PASH not in note.clc_reading
    assert note.diff_type == clc_note.DIFF_UXLC_PENDING_CHANGE_APPLIED
    assert note.superseding_uxlc_change == ("2026.10.19", "2026.04.10-10")
    assert note.note_code == "t"


def test_no_leakage():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    for note in notes:
        if note.ch == 5 and note.v == 8 and note.atom_index == 2:
            continue
        assert note.is_uxlc_departure is False, note
        assert note.uxlc_reading == note.clc_reading == note.atom_text, note


def test_render():
    _book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    note = _deut_5_8_atom2_note(notes)
    html = H.el_to_str_no_wbr(clc_render._note_block([note]))
    # The departure note's body follows the demoted bare-letter heading on one line, em-dash-joined.
    assert 'class="clc-note"' in html and " — Here CLC replaces UXLC's " in html
    assert "pashta" in html and "qadma" in html
    # No note-code prefix or superseding-change citation: those belong to showing
    # the UXLC note itself, which this departure note deliberately doesn't. But
    # "pending change" itself links to the change record.
    assert 'class="clc-note-code"' not in html
    assert 'class="clc-superseded-cite"' not in html
    assert ">pending change</a>" in html
    assert "2026.04.10-10" in html  # in the link's href, not as visible cite text
    assert note.note_text not in html  # still-suppressed stale prose never shown


def test_dual_cant_integration():
    # Confirms clc_dual_cant._ORACLE's dt 5:8 atom-2 entry (no more "omit", and the qadma
    # kept exclusive to taxton per MAM's cant-alef/cant-bet) against *real* patched input,
    # not just in isolation.
    book, _notes = clc_collect.collect_for_book("Deuter", chapters={5})
    _c8, alef8, bet8 = clc_dual_cant.strand_views("Deuter", 5, 8, book[4][7])
    a2, b2 = alef8.atoms[1]["text"], bet8.atoms[1]["text"]
    assert acc.QOM in a2 and acc.PASH not in a2 and hpo.MTGOSLQ not in a2
    assert acc.QOM not in b2 and acc.PASH not in b2 and hpo.MTGOSLQ in b2
    OMIT = clc_dual_cant.clc_note.SOURCE_DUAL_CANT_OMITTED_ACCENT
    assert [n for n in alef8.notes if n["source"] == OMIT] == []
    assert [n for n in bet8.notes if n["source"] == OMIT] == []


def test_long_note_relegation():
    # Deut 5:13.2-t's UXLC note (design doc §7.3) is relegated to the long-notes page:
    # no inline same-row doc-cell block, and the word's highlight links across to the long
    # note (there is no same-page anchor to point at anymore). This exercises the real
    # clc_collect.collect_for_book pipeline, not the synthetic clc_dual_cant_test path.
    book, notes = clc_collect.collect_for_book("Deuter", chapters={5})
    notes_by_atom = clc_render._group_by_atom(notes)
    verse13 = book[4][12]  # ch5 (0-based 4), v13 (0-based 12)

    doc_blocks = clc_render._doc_contents(5, 13, verse13, notes_by_atom)
    assert not any(
        'id="clc-5-13-2"' in H.el_to_str_no_wbr(b) for b in doc_blocks
    ), doc_blocks

    href = clc_render._relegated_page_href(notes_by_atom.get((5, 13, 2)), "Deuter-5")
    assert href == "Deuter-5-long-notes.html#long-Deuter-5-13-tahton-pashta", href

    # Chapter 5 has six long notes: 5:13's taxton pashta (this one, which relegates an inline
    # UXLC note and carries an image), 5:7's elyon meteg (pure further discussion, below),
    # three more wlc-utils-corroborated cases (5:6's elyon tipexa/etnaxta, 5:17's elyon silluq)
    # whose "See the grammar checker's supplied accents page" citation now lives only here,
    # not inline, and 5:8's elyon patax (an omitted *vowel* — its further discussion weighs the
    # alternative detangling; see clc_dual_cant_test.py for their own content coverage).
    long_notes = clc_render.build_long_notes("Deuter", book, notes, chapters={5})
    by_anchor = {e["anchor"]: e for e in long_notes}
    assert set(by_anchor) == {
        "long-Deuter-5-13-tahton-pashta",
        "long-Deuter-5-7-elyon-meteg",
        "long-Deuter-5-6-elyon-tipeha",  # translit-ok: anchor-id slug
        "long-Deuter-5-6-elyon-etnahta",  # translit-ok: anchor-id slug
        "long-Deuter-5-17-elyon-silluq",
        "long-Deuter-5-8-elyon-patah",
    }, by_anchor
    section_html = H.el_to_str_no_wbr(
        clc_long_note._section(by_anchor["long-Deuter-5-13-tahton-pashta"])
    )
    assert 'id="long-Deuter-5-13-tahton-pashta"' in section_html
    # The short note's own recap and the added content are each labeled, so a reader
    # can tell which part just repeats the main page vs. what's new here. "main page"
    # is itself a back-link to the page this note was relegated from.
    assert (
        'Inline note (repeated from <a href="Deuter-5.html">main page</a>): A pashta'
        " is expected here" in section_html
    )
    assert "beyond the limits" in section_html
    assert "the LC has only the elyon" in section_html
    assert "Further discussion: See the " in section_html
    assert ">UXLC note</a>" in section_html
    assert (
        "https://tanach.us/Notes/Deuteronomy/Deuteronomy.5.13.2-t.html" in section_html
    )
    assert (
        '<abbr title="Dotan’s Biblia Hebraica Leningradensia">BHL</abbr>'
        in section_html
    )
    assert "Appendix A" in section_html
    # The manuscript detail image sits between the short-note recap and the further
    # discussion it illustrates, with its source's own credit line carried forward.
    i_short = section_html.index("Inline note (repeated from")
    i_img = section_html.index('src="../img/Deuter.5.13.2-t.jpg"')
    i_credit = section_html.index("Credit: Sefaria.org.")
    i_further = section_html.index("Further discussion:")
    assert i_short < i_img < i_credit < i_further, section_html

    # Deut 5:7's elyon meteg is a further-discussion long note (§7.3): softened recap, a Yeivin
    # ITM §355 citation, an LC folio-102A detail image, a closing aside on the charitably-read
    # initial yod, and — unlike 5:13 — it relegates no inline UXLC x-note (relegated_position is
    # None, so it never joins _UXLC_NOTES_RELEGATED).
    meteg_html = H.el_to_str_no_wbr(
        clc_long_note._section(by_anchor["long-Deuter-5-7-elyon-meteg"])
    )
    assert (
        'Inline note (repeated from <a href="Deuter-5.html">main page</a>): A meteg might'
        " be expected in the elyon" in meteg_html
    )
    assert "best transcribed as a" in meteg_html
    assert (
        "Further discussion: Regarding the meteg that might be expected on"
        in meteg_html
    )
    assert (
        'href="https://bdenckla.github.io/phonetic-hbo/yeivin_itm-345_357.html#ns355"'
        in meteg_html
    )
    assert 'src="../img/Deuter.5.7.2.LC-102A-col3-line22.jpg"' in meteg_html
    assert "Credit: Sefaria.org." in meteg_html
    # The radically-shortened note keeps only a Yeivin pointer + the yod aside; the old
    # in-prose précis (roots, "slurred over", the initially-stressed litigation) is gone.
    assert "slurred over" not in meteg_html
    assert "initially-stressed" not in meteg_html
    # The aside is promoted to its own paragraph, after the "Further discussion:" one.
    assert "initial yod is a charitable transcription" in meteg_html
    assert (
        "</p>"
        in meteg_html[
            meteg_html.index("Further discussion:") : meteg_html.index("Aside:")
        ]
    )
    # Image sits between the short-note recap and the further discussion it illustrates.
    assert (
        meteg_html.index("Inline note (repeated from")
        < meteg_html.index('src="../img/Deuter.5.7.2.LC-102A-col3-line22.jpg"')
        < meteg_html.index("Further discussion:")
        < meteg_html.index("Aside:")
    ), meteg_html
    assert list(clc_render._UXLC_NOTES_RELEGATED) == [("Deuter", 5, 13, 2, "t")]

    # The three wlc-utils-corroborated entries (5:6 x2, 5:17) share one boilerplate
    # "Further discussion" paragraph -- the grammar-checker citation itself, no longer
    # inline on the main page (clc_dual_cant_test.py covers each note's own content).
    # Each links to its OWN block on the supplied-marks page via a #fragment
    # (clc_render._SUPPLIED_MARKS_ANCHOR), not just the page top -- and the fragment is
    # wlc-utils's supplied-side naming, which inverts CLC's omitted-side naming (5:17's
    # "elyon silluq" is there the "taxton tipexa" it supplied: ...-alef-tipexa).
    _SUPPLIED = "https://bdenckla.github.io/MAM-basics/wlc/accgram/supplied-marks.html"
    for anchor, fragment in (
        (
            "long-Deuter-5-6-elyon-tipeha",  # translit-ok: anchor-id slug
            "supplied-dt5v6-bet-tipexa",
        ),
        (
            "long-Deuter-5-6-elyon-etnahta",  # translit-ok: anchor-id slug
            "supplied-dt5v6-bet-atnax",
        ),
        ("long-Deuter-5-17-elyon-silluq", "supplied-dt5v17-alef-tipexa"),
    ):
        html = H.el_to_str_no_wbr(clc_long_note._section(by_anchor[anchor]))
        assert "Inline note (repeated from" in html
        assert "independently corroborated by wlc-utils’s grammar checker" in html
        assert f'href="{_SUPPLIED}#{fragment}"' in html
