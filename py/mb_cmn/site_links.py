"""Links from one page of the published site to another, and the site's own address.

MAM-basics publishes ``gh-pages/``, the deploy root, at ``SITE_URL``.  A link from one page
of the site to another page of the same site is relative: ``site_href`` computes it from
the two pages' paths below the deploy root.  A relative link works in a local checkout and
in a preview as well as on the published site, and py/check_html_syntax_and_sanity.py
checks that its file and fragment exist, which it cannot do for an absolute address.  Ben,
2026-11-11, of the site index's absolute link to a page of the same site: "Fix it to be a
relative link and fix any other inappropriately-absolute links please".

An address that a reader meets off the site stays absolute: a data product's notice or
metadata, a README, a record under ``in/`` or ``out/``, or a link Ben opens from chat.
``site_url`` gives that form.  A page rendered from such a record converts the record's
address with ``site_href_from_url`` as it renders, and the record keeps its address.

Python under ``py/`` writes no ``"../<sub-site>/..."`` literal: py/tests/test_sibling_reach.py
reads a literal beginning ``../X`` as reaching the sibling repository X whenever X names a
repository, and several sub-sites, MAM-with-doc and book-of-job among them, share their
names with retired repositories.  Compute such an href here instead.
"""

import posixpath
from pathlib import Path

from mb_cmn import paths

SITE_URL = "https://bdenckla.github.io/MAM-basics/"


def site_href(page: str, target: str) -> str:
    """The relative href from ``page`` to ``target``, both paths below the deploy root.

    ``page`` names the linking page's file, such as ``"wlc/accgram/supplied-marks.html"``.
    ``target`` names a file and may add a query, a fragment or both, such as
    ``"MAM-with-doc/A1-Genesis.html#c1v11"``.  A directory's page is named as its
    index.html: the HTML checker resolves an href to a file, and does not supply the
    index.html that the server sends for an address ending in a slash.
    """
    _require_file_below_root(page, "page")
    return site_href_from_folder(posixpath.dirname(page), target)


def site_href_from_folder(folder: str, target: str) -> str:
    """The relative href to ``target`` from any page in ``folder``, as ``site_href`` gives it.

    For a generator that writes all its pages into one folder, and builds their links
    before it names the page: ``folder`` is a path below the deploy root, such as
    ``"wlc/accgram"``, or ``""`` for the deploy root itself.
    """
    if (
        folder.startswith("/")
        or folder.endswith("/")
        or "://" in folder
        or ".." in folder.split("/")
    ):
        raise ValueError(f"folder is not a path below the deploy root: {folder!r}")
    path, suffix = _split_off_query_and_fragment(target)
    _require_file_below_root(path, "target")
    return posixpath.relpath(path, folder or ".") + suffix


def folder_below_root(directory: Path | str) -> str:
    """``directory``, a folder of the site's tree on disk, as a path below the deploy root."""
    folder = Path(directory).resolve().relative_to(paths.gh_pages_dir().resolve())
    return "" if folder == Path(".") else folder.as_posix()


def site_url(target: str) -> str:
    """The absolute address of ``target``, a path below the deploy root, for a reader
    off the site.  Unlike ``site_href``'s, this target may name a directory, ending in a
    slash, since the server sends that directory's index.html for it."""
    path, _suffix = _split_off_query_and_fragment(target)
    if path.startswith("/") or "://" in path or ".." in path.split("/"):
        raise ValueError(f"target is not a path below the deploy root: {target!r}")
    return SITE_URL + target


def site_href_from_url(page: str, url: str) -> str:
    """The relative href from ``page`` to ``url``, an address below ``SITE_URL``.

    For a page rendered from a record that keeps the absolute address because it is read
    off the site.  An address whose path is empty or ends in a slash names that
    directory's index.html, which is what the server sends for it.
    """
    return site_href(page, _target_of(url))


def href_in_folder(folder: str, address: str) -> str:
    """The href that a page in ``folder`` gives ``address``, an absolute address that a
    shared builder made for readers off the site as well: the relative href if the address
    is below ``SITE_URL``, as ``site_href_from_url`` converts it, and the address itself if
    it is elsewhere."""
    if not address.startswith(SITE_URL):
        return address
    return site_href_from_folder(folder, _target_of(address))


def _target_of(url: str) -> str:
    """``url``, an address below ``SITE_URL``, as a target below the deploy root."""
    if not url.startswith(SITE_URL):
        raise ValueError(f"not an address below {SITE_URL}: {url!r}")
    path, suffix = _split_off_query_and_fragment(url[len(SITE_URL) :])
    if path == "" or path.endswith("/"):
        path += "index.html"
    return path + suffix


def _split_off_query_and_fragment(target: str) -> tuple[str, str]:
    """``target``'s path, and the query and fragment that follow it, if any."""
    cuts = [at for at in (target.find("?"), target.find("#")) if at >= 0]
    cut = min(cuts, default=len(target))
    return target[:cut], target[cut:]


def _require_file_below_root(path: str, what: str) -> None:
    """Raise unless ``path`` names a file by a path below the deploy root."""
    if (
        path == ""
        or path.startswith("/")
        or path.endswith("/")
        or "://" in path
        or ".." in path.split("/")
    ):
        raise ValueError(f"{what} is not a file's path below the deploy root: {path!r}")
