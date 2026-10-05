"""Differential checks for the local near-Aleppo products and shared renderer."""

from near_aleppo import edition
import main_near_aleppo


def test_dataset_and_population_baselines_are_current():
    assert main_near_aleppo.almost_main(["--census", "--check"]) == 0
    assert main_near_aleppo.almost_main(["--build", "--check"]) == 0


def test_all_changed_note_presentations_match_the_source_inventory():
    assert main_near_aleppo.almost_main(["--check-note-review"]) == 0


def test_shared_renderer_matches_independent_mam_with_doc_files():
    problems, count = edition.check_mam_mode()
    assert not problems
    assert count == 62
