"""Saved-revision receipts survive verification failures in the three bot modes.

These fault injections use AGENTS.md's live-ws_bot test exception. The real
runners receive mocked successful saves, then verification either succeeds or
raises. Their list-shaped receipts retain the known revision identities and the
verification flags. All network requests and saving operations are mocked.
"""

import json
from unittest.mock import Mock

import pytest
import requests

from miqra_mevoar import books
from miqra_mevoar import display_page
from miqra_mevoar import wikitext
from subcommands import ws_bot_miqra_mevoar as chapters
from subcommands import ws_bot_miqra_mevoar_display as display
from subcommands import ws_bot_miqra_mevoar_index as index


@pytest.mark.parametrize(
    "mode,outcome",
    [
        ("display", "create"),
        ("chapters", "create"),
        ("chapters", "update"),
        ("index", "update"),
    ],
)
@pytest.mark.parametrize("verification_raises", [True, False])
def test_saved_ids_survive_verification(
    mode, outcome, verification_raises, tmp_path, monkeypatch
):
    network = Mock(side_effect=AssertionError("No network is permitted"))
    monkeypatch.setattr("socket.socket.connect", network)
    monkeypatch.setattr("requests.sessions.Session.request", network)
    bot = {"display": display, "chapters": chapters, "index": index}[mode]
    monkeypatch.setattr(bot, "_RUNS_ROOT", str(tmp_path))
    monkeypatch.setattr(
        bot.ws_bot_real, "assert_pywikibot_dir_configured", lambda _: None
    )
    monkeypatch.setattr(bot.pywikibot, "Site", lambda *_args: object())
    monkeypatch.setattr(bot.pywikibot, "Page", lambda *_args: object())
    if mode == "display":
        title = display_page.PAGES["yona"].title()
        monkeypatch.setattr(bot, "_outcome", lambda *_args: (outcome, []))
        run = lambda: bot.run(["yona"], [], summary="offline receipt check")
    elif mode == "chapters":
        title = wikitext.page_title(books.BOOKS["yona"].mam_book, 1)
        monkeypatch.setattr(bot, "_outcome", lambda *_args: (outcome, [], None))
        run = lambda: bot.run(["yona"], "1-1", [], summary="offline receipt check")
    else:
        title = wikitext.INDEX_TITLE
        base = {
            "content": b"old",
            "revision_id": 123,
            "revision_timestamp": "2026-11-04T00:00:00Z",
            "byte_size": 3,
        }
        monkeypatch.setattr(bot, "_latest_revision", lambda: ({"page_id": 1}, base))
        monkeypatch.setattr(bot.index_page, "page_text", lambda _: "new")
        monkeypatch.setattr(
            bot,
            "_facts",
            lambda *_args: {
                "base-revid": 123,
                "base-timestamp": base["revision_timestamp"],
                "new-links": 1,
                "new-sections": 1,
                "old-links": 0,
                "old-sections": 1,
                "diff-added": 1,
                "diff-removed": 1,
                "old-bytes": 3,
                "new-bytes": 3,
            },
        )
        run = lambda: bot.run([], base_revid=123, summary="offline receipt check")
    identity = {
        "title": title,
        "outcome": outcome,
        "pageid": 1,
        "oldrevid": None if outcome == "create" else 123,
        "newrevid": 456,
        "diff": "offline save",
        "verified": False,
    }
    save = Mock(side_effect=lambda *_args: identity.copy())
    monkeypatch.setattr(bot, "_save", save)

    def verify(saved, _texts):
        if verification_raises:
            raise requests.ConnectionError("read-back unavailable")
        records = [saved] if mode == "index" else saved
        for record in records:
            record["verified"] = True
        return None if mode == "index" else []

    monkeypatch.setattr(bot, "_verify", verify)
    if verification_raises:
        with pytest.raises(requests.ConnectionError, match="read-back unavailable"):
            run()
    else:
        run()

    receipts = list(tmp_path.glob("*/misc/saved-pages.json"))
    assert len(receipts) == 1
    expected = {**identity, "verified": not verification_raises}
    assert json.loads(receipts[0].read_text(encoding="utf-8")) == [expected]
    save.assert_called_once()
    network.assert_not_called()
