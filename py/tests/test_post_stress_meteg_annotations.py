"""Mechanical annotation validation of every generated MAS page against its sources."""

from accgram import post_stress_meteg as survey
from author_site import post_stress_meteg as page
from author_site import site_data
from mb_cmn import paths


def test_displayed_annotations_have_source_forms():
    page.assert_no_phonetic_mam_annotations(
        sorted((paths.gh_pages_dir() / site_data.POST_STRESS_METEG_DIR).glob("*.html")),
        survey.load_survey(),
    )
