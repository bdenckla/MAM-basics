"""Maintain the declared Wikisource special-page mirror on every MAM download.

The mirror is independent from the chapter JSON under ``in/mam-ws/``.  It keeps
byte-verbatim Wikitext for the four Decalogue pages, the twenty-four song-form
pages, and the eight chapter pages that carry the same layouts.  The literal
inventory is checked against chapter 2 of the local introduction mirror before any
network result can replace a file: the table in its Decalogue section gives three of
the titles, the paragraph after that table gives the fourth, and its song-form table
gives the other thirty-two.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re

from mb_cmn import file_io
from mb_cmn import paths
from mb_misc import my_utils_for_mainish as my_utils_fm
from ws import ws_revision_api as api
from ws import ws_revision_metadata as chapter_metadata

SLUG_TO_TITLE = {
    "decalogue": "עשרת הדברות/טעמים",
    "decalogue-en": "Decalogue",
    "decalogue-base": "עשרת הדברות בסיס/טעמים",
    "decalogue-vowels": "עשרת הדברות/ניקוד",
    "song-sea-taamim": "שירת הים/טעמים",
    "song-sea-layout": "שירת הים/צורת השיר",
    "song-sea-alternates": "שירת הים/צורות נוספות",
    "song-haazinu-taamim": "שירת האזינו/טעמים",
    "song-haazinu-layout": "שירת האזינו/צורת השיר",
    "song-haazinu-alternates": "שירת האזינו/צורות נוספות",
    "canaan-kings-taamim": "מלכי כנען/טעמים",
    "canaan-kings-layout": "מלכי כנען/צורת השיר",
    "canaan-kings-alternates": "מלכי כנען/צורות נוספות",
    "song-deborah-taamim": "שירת דבורה/טעמים",
    "song-deborah-layout": "שירת דבורה/צורת השיר",
    "song-deborah-alternates": "שירת דבורה/צורות נוספות",
    "song-david-taamim": "שירת דוד/טעמים",
    "song-david-layout": "שירת דוד/צורת השיר",
    "song-david-alternates": "שירת דוד/צורות נוספות",
    "song-times-taamim": "שירת העתים/טעמים",
    "song-times-layout": "שירת העתים/צורת השיר",
    "song-times-alternates": "שירת העתים/צורות נוספות",
    "ten-sons-haman-taamim": "עשרת בני המן/טעמים",
    "ten-sons-haman-layout": "עשרת בני המן/צורת השיר",
    "ten-sons-haman-alternates": "עשרת בני המן/צורות נוספות",
    "song-asaph-taamim": "שירת אסף/טעמים",
    "song-asaph-layout": "שירת אסף/צורת השיר",
    "song-asaph-alternates": "שירת אסף/צורות נוספות",
    "exodus-15": "שמות טו/טעמים",
    "deuteronomy-32": "דברים לב/טעמים",
    "joshua-12": "יהושע יב/טעמים",
    "judges-5": "שופטים ה/טעמים",
    "2-samuel-22": "שמואל ב כב/טעמים",
    "ecclesiastes-3": "קהלת ג/טעמים",
    "esther-9": "אסתר ט/טעמים",
    "1-chronicles-16": "דברי הימים א טז/טעמים",
}

DECALOGUE_TITLES = (
    "עשרת הדברות/טעמים",
    "Decalogue",
    "עשרת הדברות בסיס/טעמים",
    "עשרת הדברות/ניקוד",
)
SONG_TITLES = (
    "שירת הים/טעמים",
    "שירת הים/צורת השיר",
    "שירת הים/צורות נוספות",
    "שירת האזינו/טעמים",
    "שירת האזינו/צורת השיר",
    "שירת האזינו/צורות נוספות",
    "מלכי כנען/טעמים",
    "מלכי כנען/צורת השיר",
    "מלכי כנען/צורות נוספות",
    "שירת דבורה/טעמים",
    "שירת דבורה/צורת השיר",
    "שירת דבורה/צורות נוספות",
    "שירת דוד/טעמים",
    "שירת דוד/צורת השיר",
    "שירת דוד/צורות נוספות",
    "שירת העתים/טעמים",
    "שירת העתים/צורת השיר",
    "שירת העתים/צורות נוספות",
    "עשרת בני המן/טעמים",
    "עשרת בני המן/צורת השיר",
    "עשרת בני המן/צורות נוספות",
    "שירת אסף/טעמים",
    "שירת אסף/צורת השיר",
    "שירת אסף/צורות נוספות",
)
CHAPTER_TITLE_TO_OWNER = {
    "שמות טו/טעמים": ("Exodus", "טו"),
    "דברים לב/טעמים": ("Deuter", "לב"),
    "יהושע יב/טעמים": ("Joshua", "יב"),
    "שופטים ה/טעמים": ("Judges", "ה"),
    "שמואל ב כב/טעמים": ("2Samuel", "כב"),
    "קהלת ג/טעמים": ("Ecclesiastes", "ג"),
    "אסתר ט/טעמים": ("Esther", "ט"),
    "דברי הימים א טז/טעמים": ("1Chronicles", "טז"),
}
CHAPTER_TITLES = tuple(CHAPTER_TITLE_TO_OWNER)
DECLARED_TITLES = tuple(SLUG_TO_TITLE.values())

MAX_CONTENT_TITLES = 20
MAX_METADATA_TITLES = 50
SCHEMA_VERSION = 1
_LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]*))?\]\]")
_SLUG_RE = re.compile(r"[a-z0-9-]+")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_RECORD_FIELDS = {
    "requested_title",
    "resolved_title",
    "page_id",
    "revision_id",
    "revision_timestamp",
    "byte_size",
    "sha256",
}


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _links(text):
    return [
        (target.strip(), (label or target).strip())
        for target, label in _LINK_RE.findall(text)
    ]


def titles_from_intro(intro_text):
    """Extract the inventory independently from chapter 2's Decalogue section and song-form table."""
    decalogue_start = intro_text.index("==עשרת הדברות: תצוגת מערכת הטעמים הכפולה==")
    decalogue_end = intro_text.index('==עיצוב טעמי אמ"ת במהדורתנו==', decalogue_start)
    decalogue_block = intro_text[decalogue_start:decalogue_end]
    decalogue_titles = {
        target
        for target, _label in _links(decalogue_block)
        if "#" not in target and not target.startswith(":")
    }

    caption = '|+ דפי "צורת השיר" במקרא על פי המסורה'
    caption_offset = intro_text.index(caption)
    song_start = intro_text.rfind("{|", 0, caption_offset)
    song_end = intro_text.index("\n|}", caption_offset) + len("\n|}")
    song_block = intro_text[song_start:song_end]
    table_parts = song_block.split("|- align=center")
    _require(len(table_parts) == 10, "Expected one header and eight song table rows")
    song_titles = set()
    chapter_titles = set()
    for row_number, row in enumerate(table_parts[2:], start=1):
        cells = [
            line[1:].strip()
            for line in row.splitlines()
            if line.startswith(("! ", "| "))
        ]
        _require(
            len(cells) == 6,
            f"Song table row {row_number} does not have six declared cells",
        )
        for cell_number in (1, 2, 3):
            cell_titles = [
                target
                for target, _label in _links(cells[cell_number])
                if "#" not in target
            ]
            _require(
                len(cell_titles) == 1,
                f"Song table row {row_number}, cell {cell_number + 1} is ambiguous",
            )
            song_titles.add(cell_titles[0])
        chapter_candidates = {
            target.split("#", 1)[0]
            for target, label in _links("\n".join(cells[4:6]))
            if "#" in target and "פרק" in label
        }
        _require(
            len(chapter_candidates) == 1,
            f"Song table row {row_number} has no unique chapter identity",
        )
        chapter_titles.update(chapter_candidates)
    return decalogue_titles | song_titles | chapter_titles


def assert_declared_inventory():
    """Fail before downloading if the local introduction's inventory has drifted."""
    _validate_declaration()
    intro_path = paths.in_dir() / "mam-ws-intro" / "ch2.mediawiki"
    actual = titles_from_intro(intro_path.read_text(encoding="utf-8"))
    declared = set(DECLARED_TITLES)
    _require(
        actual == declared,
        "Wikisource special-page inventory changed in in/mam-ws-intro/ch2.mediawiki; "
        f"missing={sorted(declared - actual)!r}; extra={sorted(actual - declared)!r}",
    )


def _validate_declaration():
    _require(len(SLUG_TO_TITLE) == 36, "Expected exactly 36 special-page slugs")
    _require(
        all(_SLUG_RE.fullmatch(slug) for slug in SLUG_TO_TITLE),
        "Special-page slugs must be ASCII lowercase names",
    )
    _require(
        len(set(DECLARED_TITLES)) == len(DECLARED_TITLES),
        "Duplicate requested special-page titles",
    )
    _require(
        set(DECLARED_TITLES)
        == set(DECALOGUE_TITLES) | set(SONG_TITLES) | set(CHAPTER_TITLES),
        "Special-page categories do not cover the declared slug inventory",
    )
    _require(
        "שירת דוברה/טעמים" not in DECLARED_TITLES
        and "שירת דבורה/טעמים" in DECLARED_TITLES,
        "The declared Deborah title is misspelled",
    )


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _valid_record(record, requested_title):
    return (
        isinstance(record, dict)
        and set(record) == _RECORD_FIELDS
        and record.get("requested_title") == requested_title
        and isinstance(record.get("resolved_title"), str)
        and bool(record["resolved_title"])
        and chapter_metadata.positive_id(record.get("page_id"))
        and chapter_metadata.positive_id(record.get("revision_id"))
        and isinstance(record.get("revision_timestamp"), str)
        and _TIMESTAMP_RE.fullmatch(record["revision_timestamp"]) is not None
        and type(record.get("byte_size")) is int
        and record["byte_size"] >= 0
        and isinstance(record.get("sha256"), str)
        and _SHA256_RE.fullmatch(record["sha256"]) is not None
    )


def _empty_manifest(endpoint):
    return {"schema_version": SCHEMA_VERSION, "endpoint": endpoint, "pages": {}}


def _load_manifest(path, endpoint):
    try:
        data = json.loads(
            Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object
        )
        _require(
            isinstance(data, dict)
            and set(data) == {"schema_version", "endpoint", "pages"}
            and data["schema_version"] == SCHEMA_VERSION
            and data["endpoint"] == endpoint
            and isinstance(data["pages"], dict),
            "Unsupported special-page manifest",
        )
        _require(
            set(data["pages"]) == set(SLUG_TO_TITLE),
            "Incomplete or undeclared special-page manifest entries",
        )
        _require(
            all(
                _valid_record(data["pages"][slug], title)
                for slug, title in SLUG_TO_TITLE.items()
            ),
            "Invalid special-page manifest record",
        )
    except FileNotFoundError as error:
        print(
            f"Wikisource special-page manifest unavailable ({path}): {error}; "
            "fetching content"
        )
        return _empty_manifest(endpoint)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ValueError(f"Invalid existing special-page manifest: {path}") from error
    return data


def _validate_existing_files(out_dir):
    if not out_dir.exists():
        return
    actual = {path.stem for path in out_dir.glob("*.mediawiki")}
    extra = actual - set(SLUG_TO_TITLE)
    _require(not extra, f"Undeclared special-page mirror files: {sorted(extra)!r}")


def _local_record_is_reusable(out_dir, slug, record):
    try:
        content = (out_dir / f"{slug}.mediawiki").read_bytes()
    except OSError:
        return False
    return (
        len(content) == record["byte_size"]
        and hashlib.sha256(content).hexdigest() == record["sha256"]
    )


def _valid_chapter_record(record):
    return (
        isinstance(record, dict)
        and set(record) == {*chapter_metadata.IDENTITY_FIELDS, "sha256"}
        and all(
            isinstance(record.get(key), str) and record[key]
            for key in ("requested_title", "resolved_title")
        )
        and all(
            chapter_metadata.positive_id(record.get(key))
            for key in ("page_id", "revision_id")
        )
        and isinstance(record.get("sha256"), str)
        and _SHA256_RE.fullmatch(record["sha256"]) is not None
    )


def _chapter_identity_maps(path, endpoint):
    data = json.loads(
        Path(path).read_text(encoding="utf-8"), object_pairs_hook=_unique_object
    )
    _require(
        isinstance(data, dict)
        and set(data) == {"schema_version", "endpoint", "books"}
        and data["schema_version"] == chapter_metadata.SCHEMA_VERSION
        and data["endpoint"] == endpoint
        and isinstance(data.get("books"), dict),
        "Invalid chapter revision manifest",
    )
    by_page_id = {}
    by_resolved_title = {}
    for chapters in data["books"].values():
        _require(isinstance(chapters, dict), "Invalid chapter records")
        for record in chapters.values():
            _require(
                _valid_chapter_record(record),
                "Invalid chapter identity",
            )
            page_id = record["page_id"]
            resolved_title = record["resolved_title"]
            _require(page_id not in by_page_id, "Duplicate chapter page ID")
            _require(
                resolved_title not in by_resolved_title,
                "Duplicate chapter resolved title",
            )
            by_page_id[page_id] = record
            by_resolved_title[resolved_title] = record
    return data["books"], by_page_id, by_resolved_title


def _assert_cross_mirror_overlaps(identities, chapter_metadata_path, endpoint):
    books, by_page_id, by_resolved_title = _chapter_identity_maps(
        chapter_metadata_path, endpoint
    )
    expected_records = {}
    for title, (bkid, chapter) in CHAPTER_TITLE_TO_OWNER.items():
        _require(
            bkid in books and chapter in books[bkid],
            f"Missing declared chapter mirror owner for {title!r}",
        )
        record = books[bkid][chapter]
        identity = identities[title]
        _require(
            record["page_id"] == identity["page_id"]
            and record["resolved_title"] == identity["resolved_title"],
            f"Wrong chapter mirror owner for {title!r}",
        )
        expected_records[title] = record

    overlaps = set()
    for identity in identities.values():
        id_owner = by_page_id.get(identity["page_id"])
        title_owner = by_resolved_title.get(identity["resolved_title"])
        if id_owner is None and title_owner is None:
            continue
        _require(
            id_owner is not None
            and title_owner is not None
            and id_owner is title_owner,
            f"Inconsistent cross-mirror identity for {identity['requested_title']!r}",
        )
        _require(
            identity["requested_title"] in expected_records
            and id_owner is expected_records[identity["requested_title"]],
            f"Undeclared cross-mirror overlap for {identity['requested_title']!r}",
        )
        overlaps.add(identity["requested_title"])
    _require(
        overlaps == set(CHAPTER_TITLES),
        "Special/chapter mirror overlap changed; "
        f"missing={sorted(set(CHAPTER_TITLES) - overlaps)!r}; "
        f"extra={sorted(overlaps - set(CHAPTER_TITLES))!r}",
    )


def _identity_matches_record(identity, record):
    return all(
        record[key] == identity[key]
        for key in ("requested_title", "resolved_title", "page_id", "revision_id")
    )


def _write_bytes_if_changed(path, content):
    if path.exists() and path.read_bytes() == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    my_utils_fm.show_progress_g(__file__, str(path))
    file_io.with_tmp_path(str(path), _write_bytes, content)
    return True


def _write_bytes(content, path):
    Path(path).write_bytes(content)


def _write_manifest_if_changed(manifest, path):
    content = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    return _write_bytes_if_changed(Path(path), content)


def download(
    downloader,
    *,
    endpoint,
    out_path,
    manifest_path,
    chapter_metadata_path,
    force_download,
):
    """Validate, retrieve, and replace the special-page mirror, one file at a time.

    Every response is validated before anything is written.  Then each fetched page whose
    bytes changed is replaced atomically through ``file_io.with_tmp_path``, and
    ``manifest.json`` is replaced last; the mirror as a whole is not replaced atomically.
    If writing a page's temporary file fails, ``with_tmp_path`` removes it and leaves the
    page as it was, and a later run refetches any page whose bytes disagree with the
    manifest.  If the final replacement fails, ``<slug>.tmp.mediawiki`` is left behind,
    which Git ignores and ``_validate_existing_files`` rejects, so every later run, a
    saving bot run's post-run download included, stops before any request until a person
    deletes it.
    """
    assert_declared_inventory()
    out_dir = Path(out_path)
    _validate_existing_files(out_dir)
    manifest = _load_manifest(manifest_path, endpoint)
    client = api.ChapterClient(downloader, endpoint)

    identities = {}
    for batch in api.batches(list(DECLARED_TITLES), MAX_METADATA_TITLES):
        identities.update(
            {
                title: result[0]
                for title, result in client.by_titles(batch, content=False).items()
            }
        )
    _assert_cross_mirror_overlaps(identities, chapter_metadata_path, endpoint)

    reusable = {}
    fetch_identities = []
    for slug, title in SLUG_TO_TITLE.items():
        record = manifest["pages"].get(slug)
        if (
            not force_download
            and record is not None
            and _identity_matches_record(identities[title], record)
            and _local_record_is_reusable(out_dir, slug, record)
        ):
            reusable[title] = record
        else:
            fetch_identities.append(identities[title])

    fetched = {}
    for batch in api.batches(fetch_identities, MAX_CONTENT_TITLES):
        fetched.update(client.by_raw_revisions(batch))

    final_records = {}
    fetched_content = {}
    for slug, title in SLUG_TO_TITLE.items():
        if title in reusable:
            final_records[slug] = reusable[title]
            continue
        identity, revision = fetched[title]
        content = revision.pop("content")
        fetched_content[slug] = content
        final_records[slug] = {
            **identity,
            **revision,
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        _require(
            _valid_record(final_records[slug], title),
            f"Invalid fetched special-page record: {title!r}",
        )
    _require(
        set(final_records) == set(SLUG_TO_TITLE),
        "Incomplete special-page manifest before replacement",
    )

    for slug, content in fetched_content.items():
        _write_bytes_if_changed(out_dir / f"{slug}.mediawiki", content)
    _write_manifest_if_changed(
        {
            "schema_version": SCHEMA_VERSION,
            "endpoint": endpoint,
            "pages": final_records,
        },
        manifest_path,
    )
    return {
        "selected": len(SLUG_TO_TITLE),
        "reused": len(reusable),
        "fetched": len(fetched),
        "metadata_batches": client.metadata_batches,
        "content_batches": client.content_batches,
    }
