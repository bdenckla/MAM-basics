"""The misc pages' links to the published site's other pages.

The pages that py/author_misc/ writes into ``MAM-with-doc/misc/`` build their links before
they name their page, so a link to another page of the site is computed from that folder
(mb_cmn/site_links.py says why such a link is relative).
"""

from mb_cmn import paths
from mb_cmn import site_links

FOLDER = site_links.folder_below_root(paths.gh_pages_dir() / "MAM-with-doc" / "misc")


def href(target: str) -> str:
    """The relative href from a misc page to ``target``, a path below the deploy root."""
    return site_links.site_href_from_folder(FOLDER, target)
