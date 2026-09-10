"""Read the Google-derived MAM product through the plain JSON schema."""

from mb_cmn import paths
from py_misc import read_books_from_mam_parsed_plain as plain


def read_parsed_google_bk39s(bk39ids=None, google_dir=None):
    """Read Google-derived books without requiring the plain or plus product."""
    if google_dir is None:
        google_dir = paths.require_mam_parsed_google_dir()
    return plain.read_parsed_plain_bk39s_from_dir(google_dir, bk39ids=bk39ids)
