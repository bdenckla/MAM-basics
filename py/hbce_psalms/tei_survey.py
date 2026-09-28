"""Survey the HBCE TEI snapshot: its element and attribute inventory, and a census of the
Hebrew marks transcribed inside ``<w>``, written to ``out/tei_survey.txt``.
"""

import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter

from hbce_psalms import hbce_paths
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import str_defs as sd

TEI_NS = "{http://www.tei-c.org/ns/1.0}"

# Characters counted although their canonical combining class is 0.
_EXTRA_MARKS = hpu.MAQ + hpu.PASOLEG + hpu.SOPA + sd.CGJ + hpo.VARIKA


def survey_lines() -> list[str]:
    """The survey's report, one line per element of the list."""
    tags = Counter()
    attrs = Counter()
    marks = Counter()
    seg_notes = Counter()
    for path in sorted(hbce_paths.transcriptions_dir().glob("*.xml")):
        siglum = path.stem.split("_")[0]
        root = ET.parse(path).getroot()
        body = root.find(f".//{TEI_NS}body")
        for el in body.iter():
            tag = el.tag.replace(TEI_NS, "")
            tags[(siglum, tag)] += 1
            for k, v in el.attrib.items():
                if tag in ("ab", "div", "pb", "cb", "lb") and k == "n":
                    continue
                attrs[(siglum, tag, k, v)] += 1
            if tag == "seg":
                seg_notes[(siglum, el.get("subtype"), el.get("n"))] += 1
            if tag == "w":
                text = "".join(el.itertext())
                for ch in text:
                    if unicodedata.combining(ch) or ch in _EXTRA_MARKS:
                        marks[(siglum, ch)] += 1
    lines = ["== element counts =="]
    for (sig, tag), n in sorted(tags.items()):
        lines.append(f"{sig}\t{tag}\t{n}")
    lines.append("== attribute values (excluding n on structural elements) ==")
    for (sig, tag, k, v), n in sorted(attrs.items()):
        lines.append(f"{sig}\t{tag}\t{k}={v}\t{n}")
    lines.append("== seg subtypes ==")
    for (sig, st, n_attr), n in sorted(seg_notes.items(), key=lambda x: str(x)):
        lines.append(f"{sig}\t{st}\t{n_attr}\t{n}")
    lines.append("== marks used inside <w> ==")
    for (sig, ch), n in sorted(marks.items()):
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "?"
        lines.append(f"{sig}\tU+{ord(ch):04X}\t{name}\t{n}")
    return lines


def write_survey() -> None:
    """Write ``out/tei_survey.txt``."""
    text = "\n".join(survey_lines()) + "\n"
    path = hbce_paths.out_dir() / "tei_survey.txt"
    path.write_text(text, encoding="utf-8", newline="\n")
