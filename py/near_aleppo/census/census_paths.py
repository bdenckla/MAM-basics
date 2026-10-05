"""Repository-local MAM inputs for near-Aleppo population instruments."""

from mb_cmn import paths


def mam_parsed_path():
    return str(paths.mam_parsed_dir())


def aleppo_dir():
    return paths.repo_root() / "aleppo"
