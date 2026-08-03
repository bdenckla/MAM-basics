"""Exports the UXLC attribution citations CLC must carry to use UXLC's notes.

The UXLC author licenses the detailed notes on condition that (1) each note cites
the UXLC and its version number ("UXLC 2.5") and (2) UXLC is cited as the base of
the Hebrew biblical text. This is the single source of truth for that wording and
version, so nothing is duplicated:

  * top_credit()  -> the page-level credit: cites UXLC as the base of the Hebrew
                     text (condition 2) and acknowledges the notes as copyrighted,
                     used by permission
  * note_cite()   -> the short per-note cite appended to each note (condition 1)

The version is read once from the core-XML header (uxlc_version), never hardcoded,
so the citations auto-update if UXLC bumps to 2.6.
"""

import xml.etree.ElementTree as ET

import mb_cmn.bib_locales as tbn
import mb_cmn.uxlc_change_url as uxlc_change_url
import uxlc_misc.my_uxlc as my_uxlc
import uxlc_misc.uxlc_utils_html as H

TANACH_US_URL = "https://tanach.us"

_VERSION_MEMO = None


def uxlc_version():
    """The UXLC edition string (e.g. "UXLC 2.5"), read once from the XML header.

    Data-driven so the citation auto-updates if UXLC bumps its version: parse the
    ``<version>`` out of the canonical core-XML header rather than hardcoding it.
    The header is namespace-free (root ``<Tanach>`` declares only ``xmlns:xsi``),
    so a plain ElementTree path works.
    """
    global _VERSION_MEMO
    if _VERSION_MEMO is None:
        path = my_uxlc.canonical_xml_path(tbn.BK_GENESIS)
        elem = (
            ET.parse(path)
            .getroot()
            .find("teiHeader/fileDesc/editionStmt/edition/version")
        )
        version = elem.text.strip() if elem is not None and elem.text else ""
        assert version, f"no <version> in UXLC header: {path}"
        _VERSION_MEMO = version
    return _VERSION_MEMO


def top_credit():
    """The page-level credit line (htel): a ``<p class="clc-attribution">``.

    Distinguishes the two by their rights: the Hebrew body text is *based on* the
    (public-domain) UXLC transcription — citing it as the base satisfies the
    license's text-attribution condition — while the detailed notes are the
    author's copyrighted work, acknowledged here as used by permission.
    """
    return H.para(
        [
            "Hebrew text based on the Unicode/XML Leningrad Codex (",
            H.bold(uxlc_version()),
            "). The detailed notes are copyright © Christopher V. Kimball / "
            "TANACH US Inc. and are used by permission. See ",
            H.anchor("tanach.us", {"href": TANACH_US_URL}),
            ".",
        ],
        {"class": "clc-attribution"},
    )


def note_cite(source_url):
    """The per-note cite (htel): a small ``— UXLC 2.5`` linked to its note page.

    Links to the specific tanach.us note page the prose came from. Every m/d/t
    note has such a page, so clc_collect always supplies its URL — even for a
    not-yet-downloaded note whose prose is still a ``[note not yet downloaded]``
    placeholder (issue #19): the link points at where that prose lives. There is
    no home-page fallback.
    """
    return H.span(
        [
            " — ",
            H.anchor(
                uxlc_version(),
                {"href": source_url, "target": "_blank"},
            ),
        ],
        {"class": "clc-note-cite"},
    )


def change_record_link(release_and_id, link_text):
    """Anchor to a UXLC change record, for embedding mid-sentence.

    ``release_and_id`` is a (release_date, change_id) pair (e.g.
    ("2026.10.19", "2026.04.10-10")), as stored in
    clc_note.ClcNote.superseding_uxlc_change. ``link_text`` is caller-chosen so
    the same link can read as a change id (superseding_change_cite) or as a
    phrase like "pending change" (clc_render._departure_note_body).
    """
    release_date, change_id = release_and_id
    href = uxlc_change_url.uxlc_change_url(release_date, change_id)
    return H.anchor(link_text, {"href": href, "target": "_blank"})


def superseding_change_cite(release_and_id):
    """Link to the UXLC change record that supersedes this note's prose.

    Used instead of note_cite() when a note's tanach.us prose is superseded by
    a later, more specific UXLC change record (clc_note.ClcNote.superseding_uxlc_change).
    ``release_and_id`` is a (release_date, change_id) pair, e.g.
    ("2026.10.19", "2026.04.10-10").
    """
    _release_date, change_id = release_and_id
    return H.span(
        [
            "Superseded by pending UXLC change ",
            change_record_link(release_and_id, change_id),
            ".",
        ],
        {"class": "clc-superseded-cite"},
    )
