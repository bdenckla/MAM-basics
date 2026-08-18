"""Resolve Holman's manuscript-image citations to Leningrad Codex folios.

Holman cites the page he worked from as, for example,
``069_Exo_7.9b-8.3a / Col. 2 middle``. The leading number is a 1-based ordinal
over page sides, counting folio 001A as 1, so

    ordinal = 2 * folio + (0 for side A, 1 for side B) - 1

and the folio and side invert out of it. The three-letter code names the book
the page starts in, which is not always the book of the case on it, so it is
neither shown nor checked.

Checked 2026-08-08: inverting all twenty ordinals in ``emails/`` and looking the
folios up in the sibling ``codex-index-leningrad``'s
``UXLC-utils-sparse/data/lci_recs.json`` reproduced Holman's verse range in
every one. That file is derived from tanach.us's ``LCIndex.xml``, the UXLC page
index, which is presumably where Holman's ordinals come from too. To
re-establish the check, decode an ordinal here and compare against the
``page`` row of that JSON.

The Sefaria image URL follows
``codex-index-leningrad/lenin-wiki/py/image_urls.py``.

The rest of a citation, ``Col. 2 middle``, is Holman's own placing of the atom
on that page. ``manuscript_position`` parses it so that the page can compare his
column against the estimate in ``uxlc_atom_locations``, which is what it reports
instead. The comparison is on the column alone: a column is a
discrete fact both sources state, whereas top/middle/bottom is a loose gloss
that an estimated line number supersedes, and checking it against equal
nine-line thirds manufactures disagreements a line wide.

Since 2026-08-12 the decoded folio is compared the same way rather than shown as
the card's answer, because five of the 124 citations name a scan that cannot
hold their own verse. Each scan-file name carries its verse range, so no
estimator is needed to see it -- ``623_Amos_9.12b-Oba_20a`` cannot hold Micah
1:14. The five are Jer 3:24.2, Amos 8:12.8, Obad 1:1.17, Mic 1:14.10 and Zech
12:5.1, all in the message of 2026-08-12, and four of them run consecutively
through its MINOR PROPHETS section; Amos 8:12.8 repeats the file name of the
case above it verbatim. Their cited ordinals run low by 2 to 4 pages, never
high, and the other 119 agree with the estimate exactly. Ben's decision the same
day, on being shown the five: do not keep echoing Holman's mistakes. So the card
links ``uxlc_atom_locations``' folio and gives Holman's beside it where the two
disagree, as it already does for his column.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

_LOCATION_RE = re.compile(r"^(?P<ordinal>\d{2,4})_(?P<book_code>[A-Za-z0-9]+)_")
# Holman writes the position two ways, "/ Col. 2 middle" and "(Col. 1 bottom)",
# so the surrounding punctuation is not matched -- only the column and the
# word after it, which he has always supplied.
_POSITION_RE = re.compile(
    r"Col\.?\s*(?P<column>\d)\s+(?P<band>top|middle|bottom)\b", re.IGNORECASE
)
_SEFARIA_PREFIX = "https://manuscripts.sefaria.org/leningrad-color/"


@dataclass(frozen=True)
class ManuscriptPage:
    ordinal: int
    folio: int
    side: str
    book_code: str

    @property
    def folio_label(self) -> str:
        """The folio in the DDDA form the image URLs use, e.g. 035A."""
        return f"{self.folio:03d}{self.side}"

    @property
    def sefaria_image_url(self) -> str:
        return sefaria_image_url(self.folio_label)


def sefaria_image_url(folio_label: str) -> str:
    """The Sefaria scan of one leaf, named in the DDDA form both sources use.

    Takes the label rather than a ``ManuscriptPage`` because the card links the
    estimated folio, which arrives as a bare string from
    ``uxlc_atom_locations``, and Holman's decoded ordinal is only compared
    against it.
    """
    return f"{_SEFARIA_PREFIX}BIB_LENCDX_F{folio_label}.jpg"


@dataclass(frozen=True)
class ManuscriptPosition:
    """Where on the page Holman puts the atom: a column and a band down it."""

    column: int
    band: str

    @property
    def display(self) -> str:
        """Holman's wording, normalized to one spelling of ``Col.``."""
        return f"Col. {self.column} {self.band}"


def manuscript_page(image_location: str) -> ManuscriptPage | None:
    """Decode a manuscript-image citation, or None when it has no ordinal."""
    match = _LOCATION_RE.match(image_location.strip())
    if match is None:
        return None
    ordinal = int(match.group("ordinal"))
    if ordinal < 1:
        raise ValueError(f"manuscript page ordinal out of range: {image_location!r}")
    # ordinal + 1 == 2 * folio + side, with side 0 for A and 1 for B.
    folio, side = divmod(ordinal + 1, 2)
    return ManuscriptPage(
        ordinal=ordinal,
        folio=folio,
        side="A" if side == 0 else "B",
        book_code=match.group("book_code"),
    )


def manuscript_position(image_location: str) -> ManuscriptPosition | None:
    """Holman's column and band, or None when his citation names neither."""
    match = _POSITION_RE.search(image_location)
    if match is None:
        return None
    return ManuscriptPosition(
        column=int(match.group("column")), band=match.group("band").lower()
    )
