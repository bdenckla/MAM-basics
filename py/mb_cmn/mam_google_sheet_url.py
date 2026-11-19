"""URLs into MAM's old Google Sheet, which Hebrew Wikisource's page histories replaced.

The Sheet's changes tab recorded MAM's corrections until the whole Sheet was frozen, as the
MAM introduction's appendices say (``in/mam-ws-intro/appendices.mediawiki``). The change logs
cite a row of that tab as the evidence for a credit ported from it.
"""

_SHEET_EDIT_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs/edit"
)
CHANGES_TAB_GID = 953964633


def changes_tab_row_url(row: int) -> str:
    """The URL of one row of the Sheet's changes tab, by its row number in the Sheet."""
    return f"{_SHEET_EDIT_URL}?gid={CHANGES_TAB_GID}#gid={CHANGES_TAB_GID}&range=A{row}"
