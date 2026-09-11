"""Reuse verified raw chapters and commit complete books before revision metadata."""

import json
from pathlib import Path

from mb_cmn import file_io
from mb_cmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from mb_misc import my_utils_for_mainish as my_utils_fm
from py_misc import get_wikisource_plan as wsplan
from ws import ws_revision_api as api
from ws import ws_revision_metadata as metadata

MAX_CONTENT_TITLES = 20
MAX_METADATA_TITLES = 50


def _full_book_plan(he_bn_sbn):
    bkid = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
    return list(wsplan.get_book_plans(bkid, None))[0]


def _validate_book(contents, chapters, book_path):
    if not (
        isinstance(contents, dict)
        and set(contents) == set(chapters)
        and all(metadata.valid_lines(lines) for lines in contents.values())
    ):
        raise ValueError(
            f"Expected a complete book of chapter line arrays: {book_path}"
        )


def _prepare_books(book_plans, out_path):
    books, seen_titles, seen_books = [], set(), set()
    for book_plan in book_plans:
        he_bn_sbn, selected = book_plan
        bkid = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
        if bkid in seen_books:
            raise ValueError(f"Duplicate selected book: {bkid}")
        seen_books.add(bkid)
        full_chapters = _full_book_plan(he_bn_sbn)[1]
        if (
            not selected
            or len(set(selected)) != len(selected)
            or not set(selected) <= set(full_chapters)
        ):
            raise ValueError(f"Invalid selected chapters: {bkid}")
        chapter_plans = list(wsplan.get_chapter_plans(book_plan))
        for _chapter, title in chapter_plans:
            if title in seen_titles:
                raise ValueError(f"Duplicate requested chapter title: {title}")
            seen_titles.add(title)
        path = Path(mbkn_a_sbkn.wikisource_book_path_fr_bk39id(out_path, bkid))
        partial = set(selected) != set(full_chapters)
        existing = None
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            _validate_book(existing, full_chapters, path)
        except (OSError, UnicodeError, ValueError) as error:
            if partial:
                raise ValueError(
                    f"Partial download requires an existing complete book: {path}"
                ) from error
            print(
                f"Wikisource local book unavailable ({bkid}): {error}; fetching full book"
            )
            existing = None
        books.append(
            {
                "bkid": bkid,
                "chapters": chapter_plans,
                "full_chapters": full_chapters,
                "path": path,
                "existing": existing,
            }
        )
    return books


def _reusable_titles(books, manifest, force_download):
    reusable = []
    for book in books:
        records = manifest["books"].get(book["bkid"], {})
        for chapter, title in book["chapters"]:
            if force_download:
                continue
            record = records.get(chapter)
            if record is None or book["existing"] is None:
                continue
            if record["sha256"] != metadata.chapter_hash(book["existing"][chapter]):
                print(
                    f"Wikisource local hash mismatch: {book['bkid']}/{chapter}; fetching content"
                )
                continue
            reusable.append(title)
    return reusable


def _download_book(book, manifest, checked, client, metadata_path):
    existing = book["existing"] or {}
    records = dict(manifest["books"].get(book["bkid"], {}))
    downloaded, direct, changed = {}, [], []
    reused = 0
    for chapter, title in book["chapters"]:
        if title not in checked:
            direct.append(title)
        elif metadata.matches(records[chapter], checked[title]):
            downloaded[chapter] = existing[chapter]
            reused += 1
        else:
            changed.append(checked[title])
    fetched = {}
    for titles in api.batches(direct, MAX_CONTENT_TITLES):
        fetched.update(client.by_titles(titles, content=True))
    for identities in api.batches(changed, MAX_CONTENT_TITLES):
        fetched.update(client.by_revisions(identities))
    for chapter, title in book["chapters"]:
        if title in fetched:
            identity, lines = fetched[title]
            downloaded[chapter] = lines
            records[chapter] = metadata.with_hash(identity, lines)
    merged = {**existing, **downloaded}
    contents = {chapter: merged[chapter] for chapter in book["full_chapters"]}
    _validate_book(contents, book["full_chapters"], book["path"])
    if contents != book["existing"]:
        my_utils_fm.show_progress_g(__file__, str(book["path"]))
        file_io.json_dump_to_file_path(contents, book["path"])
    # A crash here leaves old hashes, so changed local content cannot be reused.
    manifest["books"][book["bkid"]] = {
        chapter: records[chapter]
        for chapter in book["full_chapters"]
        if chapter in records
    }
    metadata.write_if_changed(manifest, metadata_path)
    return reused, len(fetched)


def download_books(
    book_plans, downloader, *, endpoint, out_path, metadata_path, force_download
):
    """Check reusable titles across books, then retrieve and commit each book."""
    books = _prepare_books(book_plans, out_path)
    full_titles = {
        mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[plan[0]]: dict(wsplan.get_chapter_plans(plan))
        for plan in wsplan.get_book_plans()
    }
    manifest = metadata.load(metadata_path, endpoint, full_titles)
    client = api.ChapterClient(downloader, endpoint)
    checked = {}
    titles = _reusable_titles(books, manifest, force_download)
    for batch in api.batches(titles, MAX_METADATA_TITLES):
        checked.update(
            {
                title: result[0]
                for title, result in client.by_titles(batch, content=False).items()
            }
        )
    reused, fetched = 0, 0
    for book in books:
        book_reused, book_fetched = _download_book(
            book, manifest, checked, client, metadata_path
        )
        reused += book_reused
        fetched += book_fetched
    return {
        "selected": sum(len(book["chapters"]) for book in books),
        "reused": reused,
        "fetched": fetched,
        "metadata_batches": client.metadata_batches,
        "content_batches": client.content_batches,
    }
