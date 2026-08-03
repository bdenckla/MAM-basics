"""Test for clc_note_pages (issue #30: the page's own <h2> leads).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/clc_note_pages_test.py

Both tanach.us note-page formats are exercised as synthetic HTML strings (not
files under in/UXLC-notes/, so this test does not depend on the corpus):

  * NoteMaker (newer) -- modeled on in/UXLC-notes/Deuter/Deuter.5.13.2-t.html --
    asserts the <h2> change-summary line is now the first paragraph (issue #30),
    the <h1> citation text is absent, and the author/change-link text is absent.

  * Hand-authored (older) -- modeled on
    in/UXLC-notes/2Kings/2Kings.21.26.1-c.html -- asserts unchanged behavior:
    the <h4> lead line is still the first paragraph.
"""

import clc.clc_note_pages as note_pages

_NOTEMAKER_HTML = """<html><head><title>Deuteronomy 5:13.2</title></head>
<body background="../../Images/Background">
  <h1>Deuteronomy 5:13.2</h1>
  <h2>Remove pashta from final mem. Add note 't'.</h2>
  <table align="center"><tr><td><center>
    <img src="../../Changes/x.jpg"/>
  </center></td></tr><tr><td><center>Credit: Sefaria.org.</center></td></tr></table>
  <p>
    This change does not refer to the tipeha above the right edge of the final mem.<!--# translit-ok: quotes the tanach.us note page-->
  </p>
  <p>
    <b><i>Daniel Holman</i></b>
  </p>
  <p align="right">
    <b><a target="_blank" href="../../Changes/x.xml">2023.04.01 - Changes.xml : 1</a></b>
  </p>
</body></html>"""

_OLD_FORMAT_HTML = """<html><body background="../../Images/Background">
  <h1>2 Kings 21:26.1</h1>
  <h4>The LC contains the unusual markings on the bet.</h4>
  <table align="center"><tr><td>
    <center><img src="../../Changes/x.jpg"/></center>
  </td></tr>
  <p/>
  <tr><td><center><i>Credit: Sefaria.org.</i></center></td></tr>
  </table>
  <p/>
  A sheva and a holam on a consonant is unusual.
  <p/>
  <b><i>Ben Denckla</i></b>
  <p/>
  <p align="right"><b>2021.10.19 - Changes.xml : 1</b></p>
</body></html>"""


def test_notemaker_h2_leads():
    paragraphs = note_pages._extract_prose_paragraphs(_NOTEMAKER_HTML)
    assert paragraphs[0] == "Remove pashta from final mem. Add note 't'."
    joined = " ".join(paragraphs)
    assert "Deuteronomy 5:13.2" not in joined  # <h1> citation excluded
    assert "Daniel Holman" not in joined  # author excluded
    assert "Changes.xml" not in joined  # change link excluded


def test_old_format_h4_leads_unchanged():
    paragraphs = note_pages._extract_prose_paragraphs(_OLD_FORMAT_HTML)
    assert paragraphs[0] == "The LC contains the unusual markings on the bet."
    joined = " ".join(paragraphs)
    assert "2 Kings 21:26.1" not in joined  # <h1> citation excluded
    assert "Ben Denckla" not in joined  # author excluded
    assert "Changes.xml" not in joined  # change link excluded
