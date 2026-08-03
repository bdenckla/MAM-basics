"""Test for clc_attribution (CLC's UXLC attribution citations).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/clc_attribution_test.py

This is the one place the literal expected version string lives — clc_attribution
itself reads it from the core-XML header (uxlc_version) rather than hardcoding it.
That read goes through my_uxlc.canonical_xml_path, which is absolute, so this test
is cwd-independent with no setup — it used to os.chdir to the repo root instead.
"""

import clc.clc_attribution as attribution
import uxlc_misc.my_uxlc as my_uxlc
import uxlc_misc.uxlc_utils_html as H

_VERSION = "UXLC 2.5"


def test_uxlc_version():
    # Read from the XML header, not hardcoded in the library.
    assert attribution.uxlc_version() == _VERSION


def test_top_credit():
    html = H.el_to_str_no_wbr(attribution.top_credit())
    assert 'class="clc-attribution"' in html
    assert _VERSION in html  # cites the base text's version (cond. 2)
    assert "TANACH US Inc." in html  # names the entity
    assert "used by permission" in html  # acknowledges the copyrighted notes
    assert f'href="{attribution.TANACH_US_URL}"' in html


def test_note_cite_specific_page():
    url = "https://tanach.us/Notes/Samuel_2/Samuel_2.1.1.1-t.html"
    html = H.el_to_str_no_wbr(attribution.note_cite(source_url=url))
    assert 'class="clc-note-cite"' in html
    assert _VERSION in html  # each note cites UXLC + version (cond. 1)
    assert f'href="{url}"' in html  # links the specific note page
    assert 'target="_blank"' in html


def test_note_cite_requires_source_url():
    # No home-page fallback (issue #19): every m/d/t note has a real note page, so
    # the cite requires its URL rather than silently linking to the tanach.us home.
    try:
        attribution.note_cite()
    except TypeError:
        return
    raise AssertionError("note_cite() must require a source_url (no home fallback)")


def test_superseding_change_cite():
    release_and_id = ("2026.10.19", "2026.04.10-10")
    html = H.el_to_str_no_wbr(attribution.superseding_change_cite(release_and_id))
    assert 'class="clc-superseded-cite"' in html
    assert "2026.04.10-10" in html
    expected_href = "https://tanach.us/Changes/2026.10.19%20-%20Changes/2026.10.19%20-%20Changes.xml?2026.04.10-10"
    assert f'href="{expected_href}"' in html
    assert 'target="_blank"' in html


def test_note_page_url_canonical_name():
    # The moved builder still maps the bk39 id to the canonical tanach.us name.
    assert (
        my_uxlc.note_page_url("2Samuel", 1, 1, 1, "t")
        == "https://tanach.us/Notes/Samuel_2/Samuel_2.1.1.1-t.html"
    )
