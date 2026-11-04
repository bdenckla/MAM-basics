"""A live bot's local creation receipt survives a read-back transport failure.

This fault injection falls under AGENTS.md's live-ws_bot test exception. The real
runner generates one page, records a mocked successful creation and then encounters
a transport failure during verification. No request is submitted and no page is saved.
"""

import json
from unittest.mock import Mock

import pytest
import requests

from miqra_mevoar import display_page
from subcommands import ws_bot_miqra_mevoar_display as bot


def test_creation_ids_survive_a_readback_transport_failure(tmp_path, monkeypatch):
    network = Mock(side_effect=AssertionError("No network is permitted"))
    monkeypatch.setattr("socket.socket.connect", network)
    monkeypatch.setattr("requests.sessions.Session.request", network)
    monkeypatch.setattr(bot, "_RUNS_ROOT", str(tmp_path))
    monkeypatch.setattr(
        bot.ws_bot_real, "assert_pywikibot_dir_configured", lambda _: None
    )
    monkeypatch.setattr(bot.pywikibot, "Site", lambda *_args: object())
    monkeypatch.setattr(bot.pywikibot, "Page", lambda *_args: object())
    monkeypatch.setattr(bot, "_outcome", lambda *_args: ("create", []))
    title = display_page.PAGES["yona"].title()
    identity = {
        "title": title,
        "outcome": "create",
        "pageid": 123,
        "oldrevid": None,
        "newrevid": 456,
        "diff": "offline creation",
        "verified": False,
    }
    monkeypatch.setattr(bot, "_save", lambda *_args: identity.copy())
    monkeypatch.setattr(
        bot,
        "_verify",
        Mock(side_effect=requests.ConnectionError("read-back unavailable")),
    )

    with pytest.raises(requests.ConnectionError, match="read-back unavailable"):
        bot.run(["yona"], [], summary="offline receipt check")

    receipts = list(tmp_path.glob("*/misc/saved-pages.json"))
    assert len(receipts) == 1
    assert json.loads(receipts[0].read_text(encoding="utf-8")) == [identity]
    network.assert_not_called()
