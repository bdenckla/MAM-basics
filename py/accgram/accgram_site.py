"""The folder of the published site that holds the accgram pages, and their links to the
site's other pages.

Every page that the accgram generators write sits in ``gh-pages/wlc/accgram/``, and each
builds its links before it names its page, so a link to another page of the site is
computed from that folder (mb_cmn/site_links.py says why such a link is relative).  This
module imports nothing from accgram, so that any accgram module may import it.
"""

from mb_cmn import paths
from mb_cmn import site_links

FOLDER = site_links.folder_below_root(paths.wlc_pages_dir() / "accgram")


def href(target: str) -> str:
    """The relative href from an accgram page to ``target``, a path below the deploy root."""
    return site_links.site_href_from_folder(FOLDER, target)
