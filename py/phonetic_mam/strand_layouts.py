"""Which layout templates each strand of MAM's dual-cantillation template has.

Read from public MAM-parsed plus, so that the display projection can give a layout
marker the strand that has it, where the two strands of a verse's ``מ:כפול``
templates differ in their layout templates (the 2026-10-04 review's item 4.6). The
``א`` parameter is the first strand and ``ב`` the second, as in the release's
labels.

Dispatch is closed. Each top-level template of a verse's E cell passes
``template_names.validate_current_plus_template``, and only ``מ:כפול`` is read.
Inside a strand, a template that this module does not classify raises; and a
``מ:כפול`` that is not at the top level of an E cell raises too, since this reader
would not see it.
"""

import json
from pathlib import Path

from mb_cmn import mam_bknas_and_std_bknas as mbkn
from mb_cmn import template_names
from phonetic_mam.display_schema import LAYOUT_MARKERS, PublicReleaseError, require

_DUAL = template_names.DUAL_CANTILLATION
_LEGARMEH = "מ:לגרמיה-2"
_NOTE = "נוסח"
_QAMATS = template_names.QAMATS_VARIANT


def _name(template):
    return template["tmpl_name"].replace('"', "\N{HEBREW PUNCTUATION GERSHAYIM}")


def _strand(node, where):
    """The layout templates of one strand of a dual-cantillation template, in order."""
    if isinstance(node, str):
        return []
    if isinstance(node, list):
        return [label for item in node for label in _strand(item, where)]
    params = template_names.validate_current_plus_template(node)
    name = _name(node)
    if name in LAYOUT_MARKERS:
        # A "פסקא באמצע פסוק" parameter tags the break's place, not its form.
        return [name]
    if name == _LEGARMEH:
        # The release keeps a legarmeh inside the chanted word's Hebrew, not as a row.
        return []
    if name == _NOTE:
        # Parameter 1 is the Scripture that the note annotates; parameter 2 is the note.
        return _strand(params["1"], where)
    if name == _QAMATS:
        first, second = _strand(params["ד"], where), _strand(params["ס"], where)
        require(first == second, f"{where}: qamats alternatives differ in layout")
        return first
    raise PublicReleaseError(f"{where}: unclassified template in a strand: {name}")


def _dual_count(node):
    """How many dual-cantillation templates a plus file holds, wherever they are."""
    if isinstance(node, list):
        return sum(_dual_count(item) for item in node)
    if isinstance(node, dict):
        own = 1 if node.get("tmpl_name") == _DUAL else 0
        return own + sum(_dual_count(value) for value in node.values())
    return 0


def read(plus_dir):
    """Map each book to {(chapter, verse): (first strand's, second strand's) layouts}.

    Only verses whose E cell has a dual-cantillation template are listed.
    """
    result = {}
    files = sorted(Path(plus_dir).glob("*.json"))
    require(bool(files), f"missing MAM-parsed plus input: {plus_dir}")
    for path in files:
        book24 = json.loads(path.read_text(encoding="utf-8"))
        read_here = 0
        for book39 in book24["book39s"]:
            bk39id = mbkn.MAM_HBNP_TO_BK39ID[
                (book39["book24_name"], book39["sub_book_name"])
            ]
            for chapter, verses in book39["chapters"].items():
                for verse, record in verses.items():
                    # The plus reader's two pseudo-verses, which hold no verse.
                    if verse in ("0", "תתת"):
                        continue
                    where = f"{bk39id} {chapter}:{verse}"
                    first, second, duals = [], [], 0
                    for element in record[2]:
                        if isinstance(element, str):
                            continue
                        params = template_names.validate_current_plus_template(element)
                        if _name(element) != _DUAL:
                            continue
                        duals += 1
                        first += _strand(params["א"], where)
                        second += _strand(params["ב"], where)
                    if duals:
                        read_here += duals
                        key = (int(chapter), int(verse))
                        result.setdefault(bk39id, {})[key] = (
                            tuple(first),
                            tuple(second),
                        )
        require(
            read_here == _dual_count(book24),
            f"{path.name}: a dual-cantillation template outside an E cell's top level",
        )
    return result
