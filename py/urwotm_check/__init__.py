"""The differential check on the four-part series
"Undoing and redoing the work of the Masoretes" (urwotm).

py/author_misc/urwotm_[1-4]_*.py are the source of truth for those four
pages. This package holds what verifies them: the frozen source text of the
Google Docs they were ported from (``src/``), the normalizer that puts both
sides in comparable form, and the list of the differences that are
deliberate. ``py/tests/test_urwotm_difftext.py`` is what runs it.

The importer that did the port -- the fetcher, the Google-HTML parser, the
emitter, the image and inventory tooling, and py/main_urwotm_import.py --
was deleted once it had done its one job (#209 item 6). It is in git
history at 4d8d181 if a later question needs it.
"""
