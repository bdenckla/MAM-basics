"""The book-of-job pages' links to the published site's other pages.

The book-of-job pages that link another page of the site sit in ``book-of-job/jobn/`` and
``book-of-job/jobn-details/``, and each builds its links before it names its page, so a link
to another page of the site is computed from the page's folder (mb_cmn/site_links.py says
why such a link is relative).
"""

import boj_paths
from mb_cmn import site_links

JOBN_FOLDER = site_links.folder_below_root(boj_paths.jobn_dir())
JOBN_DETAILS_FOLDER = site_links.folder_below_root(boj_paths.jobn_details_dir())


def jobn_href(target: str) -> str:
    """The relative href from a page in jobn/ to ``target``, a path below the deploy root."""
    return site_links.site_href_from_folder(JOBN_FOLDER, target)


def jobn_details_href(target: str) -> str:
    """The relative href from a page in jobn-details/ to ``target``, as ``jobn_href`` gives
    it."""
    return site_links.site_href_from_folder(JOBN_DETAILS_FOLDER, target)
