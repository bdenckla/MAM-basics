"""Tests of the special-page download, ``py/ws/ws_special_page_download.py``.

The first test is lint-shaped: it checks the declared inventory against the mirrored
chapter-2 introduction, ``in/mam-ws-intro/ch2.mediawiki``.

BLESSED EXAMPLE-BASED BAND.  The other five test ids run the download over a stub API
that this module builds, and are kept under the exception Ben decided on 2026-09-30,
which ``AGENTS.md``, "Writing tests: differential and lint-shaped only", records.  The
four fault-injection ids hold five cases.  Every case checks that a bad API response or
bad local metadata makes the download raise, and every case but the last, a manifest
overwritten with "not json", also checks that no mirrored file changed: a property with
no regeneratable artifact.  The round trip is the only offline check of the download's
reuse and forced refresh, neither of which a regenerated mirror's diff would show.
"""

import json
from pathlib import Path
import tempfile
from unittest import mock

import pytest

from ws import ws_special_page_download as special


class _CompleteInventoryDownloader:
    def __init__(
        self,
        *,
        omit_metadata_title=None,
        converge_redirects=False,
        malformed_content_title=None,
    ):
        self.calls = []
        self.omit_metadata_title = omit_metadata_title
        self.converge_redirects = converge_redirects
        self.malformed_content_title = malformed_content_title
        self.identities = {}
        for index, title in enumerate(special.DECLARED_TITLES, start=1):
            resolved_title = (
                "מקרא על פי המסורה/Decalogue" if title == "Decalogue" else title
            )
            content = f"requested={title}\nresolved={resolved_title}\n".encode("utf-8")
            self.identities[title] = {
                "requested_title": title,
                "resolved_title": resolved_title,
                "page_id": 1000 + index,
                "revision_id": 2000 + index,
                "revision_timestamp": f"2026-09-{(index % 27) + 1:02d}T12:34:56Z",
                "byte_size": len(content),
                "content": content,
            }

    def get_json(self, _url, *, params=None, **_kwargs):
        params = dict(params or {})
        self.calls.append(params)
        if params["prop"] == "info":
            titles = params["titles"].split("|")
            pages = []
            for title in reversed(titles):
                if title == self.omit_metadata_title:
                    continue
                identity = self.identities[title]
                pages.append(
                    {
                        "pageid": identity["page_id"],
                        "lastrevid": identity["revision_id"],
                        "title": identity["resolved_title"],
                    }
                )
            query = {"pages": pages}
            if "Decalogue" in titles:
                query["redirects"] = [
                    {
                        "from": "Decalogue",
                        "to": "מקרא על פי המסורה/Decalogue",
                    }
                ]
            if self.converge_redirects:
                query.setdefault("redirects", []).append(
                    {
                        "from": "עשרת הדברות/ניקוד",
                        "to": "עשרת הדברות בסיס/טעמים",
                    }
                )
            return {"query": query}

        revision_ids = {int(value) for value in params["revids"].split("|")}
        pages = []
        for identity in reversed(list(self.identities.values())):
            if identity["revision_id"] not in revision_ids:
                continue
            size = identity["byte_size"]
            if identity["requested_title"] == self.malformed_content_title:
                size += 1
            pages.append(
                {
                    "pageid": identity["page_id"],
                    "title": identity["resolved_title"],
                    "revisions": [
                        {
                            "revid": identity["revision_id"],
                            "timestamp": identity["revision_timestamp"],
                            "size": size,
                            "slots": {
                                "main": {"content": identity["content"].decode("utf-8")}
                            },
                        }
                    ],
                }
            )
        return {"query": {"pages": pages}}


def _write_chapter_manifest(path, endpoint, identities):
    books = {}
    for title, (bkid, chapter) in special.CHAPTER_TITLE_TO_OWNER.items():
        identity = identities[title]
        books.setdefault(bkid, {})[chapter] = {
            "requested_title": title,
            "resolved_title": identity["resolved_title"],
            "page_id": identity["page_id"],
            "revision_id": identity["revision_id"],
            "sha256": "0" * 64,
        }
    path.write_text(
        json.dumps(
            {"schema_version": 1, "endpoint": endpoint, "books": books},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _download(downloader, endpoint, out_dir, chapter_manifest_path, *, force=False):
    return special.download(
        downloader,
        endpoint=endpoint,
        out_path=out_dir,
        manifest_path=out_dir / "manifest.json",
        chapter_metadata_path=chapter_manifest_path,
        force_download=force,
    )


def test_declared_special_page_inventory_matches_the_independent_intro_tables():
    special.assert_declared_inventory()


def test_special_mirror_matches_complete_api_oracle_reuse_and_force():
    endpoint = "https://example.invalid/w/api.php"
    downloader = _CompleteInventoryDownloader()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        out_dir = root / "mam-ws-special"
        manifest_path = out_dir / "manifest.json"
        chapter_manifest_path = root / "mam-ws-revisions.json"
        _write_chapter_manifest(chapter_manifest_path, endpoint, downloader.identities)
        write_order = []
        real_write = special._write_bytes_if_changed

        def record_write(path, content):
            write_order.append(Path(path).name)
            return real_write(path, content)

        with mock.patch.object(
            special, "_write_bytes_if_changed", side_effect=record_write
        ):
            first_stats = _download(
                downloader, endpoint, out_dir, chapter_manifest_path
            )
        manifest_bytes = manifest_path.read_bytes()
        first_contents = {
            path.name: path.read_bytes() for path in out_dir.glob("*.mediawiki")
        }

        second_downloader = _CompleteInventoryDownloader()
        second_stats = _download(
            second_downloader, endpoint, out_dir, chapter_manifest_path
        )
        forced_downloader = _CompleteInventoryDownloader()
        forced_stats = _download(
            forced_downloader, endpoint, out_dir, chapter_manifest_path, force=True
        )

        assert first_stats["selected"] == len(special.SLUG_TO_TITLE)
        assert first_stats["fetched"] == len(special.SLUG_TO_TITLE)
        assert second_stats["reused"] == len(special.SLUG_TO_TITLE)
        assert second_stats["fetched"] == 0
        assert forced_stats["fetched"] == len(special.SLUG_TO_TITLE)
        assert forced_downloader.calls[0]["prop"] == "info"
        assert all(call["prop"] == "revisions" for call in forced_downloader.calls[1:])
        assert manifest_path.read_bytes() == manifest_bytes
        assert {
            path.name: path.read_bytes() for path in out_dir.glob("*.mediawiki")
        } == first_contents
        assert len(first_contents) == 36
        assert write_order[-1] == "manifest.json"
        assert set(write_order[:-1]) == set(first_contents)
        assert all(call["prop"] == "info" for call in second_downloader.calls)
        for slug, title in special.SLUG_TO_TITLE.items():
            assert (
                first_contents[f"{slug}.mediawiki"]
                == downloader.identities[title]["content"]
            )


@pytest.mark.parametrize(
    "downloader",
    [
        _CompleteInventoryDownloader(omit_metadata_title="שירת אסף/צורות נוספות"),
        _CompleteInventoryDownloader(converge_redirects=True),
        _CompleteInventoryDownloader(malformed_content_title="דברי הימים א טז/טעמים"),
    ],
)
def test_invalid_complete_response_replaces_no_existing_special_file(downloader):
    endpoint = "https://example.invalid/w/api.php"
    good_downloader = _CompleteInventoryDownloader()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        out_dir = root / "mam-ws-special"
        chapter_manifest_path = root / "mam-ws-revisions.json"
        _write_chapter_manifest(
            chapter_manifest_path, endpoint, good_downloader.identities
        )
        _download(good_downloader, endpoint, out_dir, chapter_manifest_path)
        before = {path.name: path.read_bytes() for path in out_dir.iterdir()}

        with pytest.raises((ValueError, RuntimeError)):
            _download(downloader, endpoint, out_dir, chapter_manifest_path, force=True)

        assert {path.name: path.read_bytes() for path in out_dir.iterdir()} == before


def test_wrong_or_malformed_local_metadata_replaces_no_special_file():
    endpoint = "https://example.invalid/w/api.php"
    downloader = _CompleteInventoryDownloader()
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        out_dir = root / "mam-ws-special"
        manifest_path = out_dir / "manifest.json"
        chapter_manifest_path = root / "mam-ws-revisions.json"
        _write_chapter_manifest(chapter_manifest_path, endpoint, downloader.identities)
        _download(downloader, endpoint, out_dir, chapter_manifest_path)
        before = {path.name: path.read_bytes() for path in out_dir.iterdir()}

        chapter_manifest = json.loads(chapter_manifest_path.read_text(encoding="utf-8"))
        first_title, second_title = tuple(special.CHAPTER_TITLE_TO_OWNER)[:2]
        first_owner = special.CHAPTER_TITLE_TO_OWNER[first_title]
        second_owner = special.CHAPTER_TITLE_TO_OWNER[second_title]
        first_record = chapter_manifest["books"][first_owner[0]][first_owner[1]]
        second_record = chapter_manifest["books"][second_owner[0]][second_owner[1]]
        chapter_manifest["books"][first_owner[0]][first_owner[1]] = second_record
        chapter_manifest["books"][second_owner[0]][second_owner[1]] = first_record
        chapter_manifest_path.write_text(
            json.dumps(chapter_manifest, ensure_ascii=False), encoding="utf-8"
        )
        with pytest.raises(ValueError):
            _download(
                _CompleteInventoryDownloader(),
                endpoint,
                out_dir,
                chapter_manifest_path,
            )
        assert {path.name: path.read_bytes() for path in out_dir.iterdir()} == before

        _write_chapter_manifest(chapter_manifest_path, endpoint, downloader.identities)
        manifest_path.write_text("not json", encoding="utf-8")
        with pytest.raises(ValueError, match="special-page manifest"):
            _download(
                _CompleteInventoryDownloader(),
                endpoint,
                out_dir,
                chapter_manifest_path,
            )
