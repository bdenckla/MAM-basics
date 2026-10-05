"""Local paths for the self-contained near-Aleppo build."""

from mb_cmn import paths


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


def input_dir():
    return paths.repo_root() / "in/near-aleppo"


def asset_dir():
    return input_dir() / "img"
