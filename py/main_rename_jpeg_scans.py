"""Rename JPEG scan files based on their containing directory structure."""

from pathlib import Path
from pycmn import bib_locales as tbn


def main():
    top_path = Path(_TOP_PATH_STR)
    els_in_top = top_path.iterdir()
    dirs_in_top = list(filter(_is_dir, els_in_top))
    for dir_in_top in dirs_in_top:
        _process_dir(dir_in_top)


def _process_dir(dir):
    if dir.name == "Introduction to the Tiberian Masorah":
        return
    els_in_dir = dir.iterdir()
    files = list(filter(_is_file, els_in_dir))
    for file in files:
        if file.name[2] == "-":
            fn01 = file.name[:2]
            if short := _ORD_SHORT_TO_SHORT.get(fn01):
                new_name = file.name[:3] + short + "-" + file.name[3:]
                new_file = file.with_name(new_name)
                # print(file)
                # print(new_file)
                file.rename(new_file)
            else:
                assert fn01 in _KNOWN_NON_MATCHES


def _is_dir(dir_el):
    return dir_el.is_dir()


def _is_file(dir_el):
    return dir_el.is_file()


_TOP_PATH_STR = "C:/Users/BenDe/Downloads/Smooth-JPEG"
_ORD_SHORT_TO_SHORT = {tbn.ordered_short(b): tbn.short(b) for b in tbn.ALL_BK39_IDS}
_KNOWN_NON_MATCHES = {"A0", "A9", "B0", "D0"}

if __name__ == "__main__":
    main()
