"""Differential: bot update guards remain tied to the ownership-checked revision.

WHY THIS EXISTS

Pywikibot can refresh revision content while constructing an edit request. Its normal
timestamp guard must not silently advance beyond the revision whose ownership the
Miqra Mevoar bot checked. No network request is submitted by this test.

WHAT IT CHECKS

The real bot run, BasePage save/cache methods and pinned APISite edit-request builder
are exercised against a controlled revision provider. The outgoing baseline must be
the checked revision even if a later human edit is discovered during request building.
"""

from unittest.mock import Mock

import pywikibot
from pywikibot.data.api._generators import _update_revisions
from pywikibot.page import BasePage
from pywikibot.site import APISite
import pytest

from miqra_mevoar import books
from subcommands import ws_bot_miqra_mevoar as bot


class _CapturedRequest(Exception):
    pass


def _revision(number, user, content):
    data = {
        "revid": number,
        "timestamp": f"2026-11-03T00:00:0{number}Z",
        "user": user,
    }
    if content:
        data["slots"] = {"main": {"*": f"offline revision {number}"}}
    return data


class _OfflineSite:
    obsolete = False
    tokens = {"csrf": "synthetic-not-a-login-token"}

    def __init__(self, checked_revision, human_after_history):
        self.checked_revision = checked_revision
        self.human_after_history = human_after_history
        self.request = None

    def has_right(self, _right):
        return True

    def loadrevisions(self, page, content=False, **_kwargs):
        number = 3 if content and self.human_after_history else self.checked_revision
        user = "HumanEditor" if number == 3 else "BDencklaBot"
        _update_revisions(page, [_revision(number, user, content)])
        page.latest_revision_id = number

    def editpage(self, page, **kwargs):
        return APISite.editpage(self, page, **kwargs)

    def simple_request(self, **kwargs):
        self.request = kwargs
        raise _CapturedRequest("Captured before a request can be submitted")


class _OfflinePage(BasePage):
    def __init__(self, site, title):
        self._site = site
        self._title = title
        self._revisions = {}
        self._bot_may_edit = True
        _update_revisions(self, [_revision(1, "BDencklaBot", True)])
        self.latest_revision_id = 1
        self._text = "offline revision 1"

    @property
    def site(self):
        return self._site

    def title(self, *args, **kwargs):
        return self._title

    def __str__(self):
        return self._title

    def exists(self):
        return True


@pytest.mark.parametrize(
    "checked_revision,human_after", [(1, True), (2, True), (2, False)]
)
def test_an_update_uses_the_checked_revision(
    tmp_path, monkeypatch, checked_revision, human_after
):
    network = Mock(side_effect=AssertionError("No network is permitted"))
    monkeypatch.setattr("socket.socket.connect", network)
    monkeypatch.setattr("requests.sessions.Session.request", network)
    site = _OfflineSite(checked_revision, human_after)
    monkeypatch.setattr(pywikibot, "Site", lambda *_args: site)
    monkeypatch.setattr(pywikibot, "Page", _OfflinePage)
    monkeypatch.setattr(
        bot.ws_bot_real, "assert_pywikibot_dir_configured", lambda _: None
    )
    monkeypatch.setattr(bot, "_RUNS_ROOT", str(tmp_path))
    monkeypatch.setattr(
        bot,
        "_selected_chapters",
        lambda *_args: [
            (
                books.BOOKS["yona"],
                {
                    "chapter": 1,
                    "verses": [{"verse": 1, "heading": None, "paraphrase": "fixture"}],
                },
            )
        ],
    )
    with pytest.raises(_CapturedRequest):
        bot.run(["yona"], "1-1", [], summary="offline request capture")

    assert site.request is not None
    assert str(site.request["basetimestamp"]) == (
        f"2026-11-03T00:00:0{checked_revision}Z"
    )
    assert site.request["nocreate"] is True
    assert site.request["createonly"] is False
    assert site.request["minor"] is False
    network.assert_not_called()
