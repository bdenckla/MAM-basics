"""Commentary on Holman's suggested UXLC corrections, keyed by case.

This is the aggregator. Each contributor gets a module of their own beside it
(``comments_bd.py`` for Ben Denckla's comments; add one per person whose emailed
remarks are worth keeping), exporting ``BY_REF`` in the shape below.

``BY_REF`` maps a case key to a tuple of comment entries. The key is the case
reference as ``uxlc_email_extract.CaseRef.key`` spells it -- the bk39 book id, a
space, chapter, a colon, verse, a dot, and the word index within the verse:

    "Exodus 7:20.19", "Levit 7:25.6", "Deuter 33:28.13", "1Samuel 7:10.10"

Two of those book ids are not the English name: Leviticus is ``Levit`` and
Deuteronomy is ``Deuter``, following ``mb_cmn.bib_locales``. A key matching no
case raises at render time, so a typo is loud rather than silently invisible.

Each comment entry is a dict:

  * ``author``  -- required, who wrote it, e.g. "Ben Denckla".
  * ``date``    -- required, ISO ``YYYY-MM-DD``, when it was written.
  * ``body``    -- required, the prose. A plain string is one paragraph. A
    tuple or list is one paragraph per element. An element that is itself a
    list is an inline sequence: plain strings within it are escaped as text,
    and a ``raw(...)`` part is emitted as HTML, which is how a link gets in.

Hebrew inside a plain string is detected and wrapped in the pointed-Hebrew span
automatically, so Hebrew is typed inline with no markup.

``link`` and ``raw`` come from ``uxlc_comments.comment_parts``. A contributor
module imports them from there, never from this module: this module imports
every contributor module, so a contributor module importing this one back is a
circular import and raises ``ImportError``.

    BY_REF: dict[str, tuple[dict[str, object], ...]] = {
        "Exodus 7:20.19": (
            {
                "author": "Ben Denckla",
                "date": "2026-08-08",
                "body": (
                    "A first paragraph, with Hebrew such as וַיֵּהָ֥פְכ֛וּ inline.",
                    ["A second paragraph citing ", link("MAM", MAM_URL), "."],
                ),
            },
        ),
    }
"""

from __future__ import annotations

from uxlc_comments import comments_bd

__all__ = ["BY_REF", "comments_for_ref"]

# Every contributor module, in the order their comments should be shown. Two
# contributors commenting on one case must both survive the merge, so the
# tuples are concatenated rather than dict-splatted.
_CONTRIBUTOR_TABLES = (comments_bd.BY_REF,)


def _merged() -> dict[str, tuple[dict[str, object], ...]]:
    merged: dict[str, tuple[dict[str, object], ...]] = {}
    for table in _CONTRIBUTOR_TABLES:
        for ref_key, entries in table.items():
            merged[ref_key] = merged.get(ref_key, ()) + tuple(entries)
    return merged


BY_REF: dict[str, tuple[dict[str, object], ...]] = _merged()


def comments_for_ref(ref_key: str) -> tuple[dict[str, object], ...]:
    return BY_REF.get(ref_key, ())
