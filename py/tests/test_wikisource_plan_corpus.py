"""Compare the complete download plan with independently captured chapter keys."""

import json
from pathlib import Path

from mb_cmn import bib_locales as tbn
from mb_cmn import mam_bknas_and_std_bknas as names
from mb_cmn import paths
from py_misc import get_wikisource_plan as wsplan
from ws.ws_chapter_counts import BOOK39_CHAPTER_COUNTS


def test_download_plan_matches_raw_wikisource_corpus():
    raw_dir = paths.repo_root() / "in/mam-ws"
    book_plans = wsplan.get_book_plans()
    book_ids = [names.MAM_HBNP_TO_BK39ID[name] for name, _ in book_plans]
    assert book_ids == list(tbn.ALL_BK39_IDS)
    assert set(BOOK39_CHAPTER_COUNTS) == set(book_ids)
    planned_paths = set()
    for book_id, (_name, chapters) in zip(book_ids, book_plans):
        raw_path = Path(names.wikisource_book_path_fr_bk39id(raw_dir, book_id))
        planned_paths.add(raw_path)
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        assert chapters == list(raw), book_id
    assert planned_paths == set(raw_dir.glob("*.json"))
