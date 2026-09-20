"""Mechanical validation of the tracked meteg-after-silluq data."""

from author_site import post_stress_meteg


def test_tracked_meteg_after_silluq_data_is_valid_and_nonempty():
    """Both authored ledgers satisfy their closed schemas and contain records."""
    assert post_stress_meteg.load_post_silluq_cases()
    assert post_stress_meteg.load_post_silluq_koren_observations()
