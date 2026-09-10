"""Mechanical annotation validation of every generated MAS page against its sources."""

from accgram import post_stress_meteg as survey
from author_site import post_stress_meteg as page
from mb_cmn import paths


def test_displayed_annotations_have_source_forms():
    page.assert_no_phonetic_mam_annotations(
        sorted(paths.gh_pages_dir().glob("post-stress-meteg*.html")),
        survey.load_survey(),
    )
