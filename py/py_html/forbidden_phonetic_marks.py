"""Refuse to publish a page containing a Phonetic MAM-only mark.

Published HTML exposes generic Hebrew points and Latin transcription, never the intermediate
annotation points U+05C8 and U+05C9. The guard also retains the earlier protection against
U+05AF and U+05C4: those retired carriers must not reappear, and a genuine source dot requires
an independently validated path rather than passing through these generators unnoticed.

The guard checks a page's complete text before writing it, so a page that fails is never
written and whatever page was already at that path is left as it was. The refusal is a named
exception rather than a bare ``assert``, so it survives ``python -O``.
"""

from py_html import legacy_html
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu

FORBIDDEN_PHONETIC_MARKS = frozenset(
    (hpu.MCIRC, hpu.UPDOT, hpo.SHEVA_NA, hpo.DAGESH_XAZAQ)
)


class ForbiddenPhoneticMarkError(ValueError):
    """A page's text holds a mark that must never reach a published page."""


def write_published_page(body_contents, write_ctx, forbidden=FORBIDDEN_PHONETIC_MARKS):
    """Write one page unless its text holds a forbidden mark.

    The complete page text is built by ``legacy_html.html_text`` and checked first; only a page
    that passes is written, by ``legacy_html.write_html_text_to_file``.
    """
    text = legacy_html.html_text(body_contents, write_ctx)
    refuse_forbidden_phonetic_marks(text, write_ctx.path, forbidden)
    legacy_html.write_html_text_to_file(text, write_ctx)


def refuse_forbidden_phonetic_marks(text, label, forbidden=FORBIDDEN_PHONETIC_MARKS):
    """Raise ForbiddenPhoneticMarkError if ``text`` holds a forbidden mark.

    The error names ``label``, normally the page's path, and each mark's code point.
    """
    present = forbidden & set(text)
    if present:
        marks = ", ".join(sorted(f"U+{ord(mark):04X}" for mark in present))
        raise ForbiddenPhoneticMarkError(
            f"Refusing to publish {label}: its text holds {marks}, which must never reach "
            "a published page."
        )
