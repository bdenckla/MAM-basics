"""Local paths for the self-contained near-Aleppo build."""

from mb_cmn import paths
from mb_cmn import site_links


def mam_basics_dir():
    return paths.repo_root()


def mam_parsed_plus_dir():
    return paths.mam_parsed_dir() / "plus"


def dataset_dir():
    return paths.repo_root() / "out/near-aleppo/plus"


def aleppo_index():
    return paths.repo_root() / "aleppo/index-flat-annotated.json"


def html_pages_dir():
    return paths.repo_root() / "gh-pages/near-aleppo"


def site_folder(*parts):
    """The folder of the pages below the deploy root, or of the named folder within it, from
    which a page's link to another page of the site is computed (mb_cmn/site_links.py).
    """
    return site_links.folder_below_root(html_pages_dir().joinpath(*parts))


def site_href(target, *parts):
    """The relative href to ``target``, a path below the deploy root, from a page in the
    folder that ``site_folder(*parts)`` names."""
    return site_links.site_href_from_folder(site_folder(*parts), target)


def input_dir():
    return paths.repo_root() / "in/near-aleppo"


def asset_dir():
    return input_dir() / "img"
