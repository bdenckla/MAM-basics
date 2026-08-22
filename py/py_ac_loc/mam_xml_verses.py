"""
Extract verse words from MAM-XML (xml-vtrad-mam) for Aleppo Codex alignment.

Handles all special MAM-XML elements:
  - <text>: plain text spans
  - <lp-legarmeih>, <lp-paseq>: append paseq (U+05C0) to preceding word
  - <kq>: ketiv/qere — use ketiv (kq-k child, unpointed) for manuscript alignment
  - <kq-trivial>: trivial ketiv/qere — use text attribute (pointed)
  - <slh-word>: suspended-letter word — use slhw-desc-0 (full pointed word)
  - <scrdfftar>: scribal difference target — extract word from <sdt-target> child
  - <implicit-maqaf>: no visible text, skip
  - <shirah-space>: visual spacing in song layout, skip
  - <spi-pe2>: petuxah (open paragraph) break — emitted as {"parashah": "spi-pe2"}
  - <spi-samekh2>: setumah (closed paragraph) break — emitted as {"parashah": "spi-samekh2"}

Usage:
    from py_ac_loc.mam_xml_verses import get_verses_in_range

    verses = get_verses_in_range(
        r'C:\\path\\to\\codex-index-aleppo\\MAM-XML\\Job.xml',
        'Job', (37, 9), (38, 20),
    )
    # Returns: [{'cv': '37:9', 'words': [...], 'ketiv_indices': [], 'parashah_before': None}, ...]
    # parashah_before is None, {"parashah": "spi-pe2"}, or {"parashah": "spi-samekh2"}
"""

import xml.etree.ElementTree as ET

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"


def get_verse_words(verse_el):
    """
    Extract the word list from a MAM-XML <verse> element.

    Args:
        verse_el: an xml.etree.ElementTree Element for a <verse>.

    Returns a dict:
        words: list of str — space-separated words (maqaf-connected words joined)
        ketiv_indices: list of int — indices in `words` that are ketiv (unpointed)
    """
    raw_words = []
    ketiv_flags = []

    if "text" in verse_el.attrib:
        # Simple verse: text is directly on the element
        raw_words = verse_el.attrib["text"].split()
        ketiv_flags = [False] * len(raw_words)
    else:
        # Complex verse: iterate children
        for child in verse_el:
            tag = child.tag
            if tag == "text":
                text = child.attrib.get("text", "").strip()
                if text:
                    ws = text.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([False] * len(ws))
            elif tag in ("lp-legarmeih", "lp-paseq"):
                # Append paseq to the last word
                if raw_words:
                    raw_words[-1] = raw_words[-1] + PASEQ
            elif tag == "kq":
                # Non-trivial ketiv/qere — use ketiv text (unpointed)
                kq_k = child.find("kq-k")
                if kq_k is not None:
                    kt = kq_k.attrib.get("text", "").strip()
                    if not kt:
                        slh = kq_k.find("slh-word")
                        if slh is not None:
                            kt = slh.attrib.get("slhw-desc-0", "").strip()
                    assert kt, (
                        f"<kq-k> has no text= and no slh-word child "
                        f"in {verse_el.attrib.get('osisID', '?')}"
                    )
                    ws = kt.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([True] * len(ws))
            elif tag == "kq-trivial":
                # Trivial k/q — use pointed text attribute
                text = child.attrib.get("text", "").strip()
                if text:
                    ws = text.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([False] * len(ws))
            elif tag == "slh-word":
                # Suspended-letter word — use desc-0 (full pointed word)
                text = child.attrib.get("slhw-desc-0", "").strip()
                if text:
                    ws = text.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([False] * len(ws))
            elif tag == "scrdfftar":
                # Scribal difference target — extract word from sdt-target child
                sdt = child.find("sdt-target")
                if sdt is not None:
                    text = sdt.attrib.get("text", "").strip()
                    if not text:
                        # sdt-target may contain slh-word with the word
                        slh = sdt.find("slh-word")
                        if slh is not None:
                            text = slh.attrib.get("slhw-desc-0", "").strip()
                    if text:
                        ws = text.split()
                        raw_words.extend(ws)
                        ketiv_flags.extend([False] * len(ws))
            elif tag == "implicit-maqaf":
                pass  # No visible text
            elif tag == "shirah-space":
                pass  # Visual spacing in song layout, no text
            elif tag in ("spi-pe2", "spi-samekh2", "spi-pe1", "spi-samekh1"):
                pass  # Parashah markers handled at verse level
            else:
                raise ValueError(
                    f"Unhandled tag <{tag}> in verse "
                    f"{verse_el.attrib.get('osisID', '?')}"
                )

    # Join maqaf-connected words
    joined = []
    joined_ketiv = []
    for w, is_k in zip(raw_words, ketiv_flags):
        if joined and joined[-1].endswith(MAQAF):
            joined[-1] = joined[-1] + w
            # If either part is ketiv, mark the joined word as ketiv
            joined_ketiv[-1] = joined_ketiv[-1] or is_k
        else:
            joined.append(w)
            joined_ketiv.append(is_k)

    # Attach standalone sof pasuq (׃) to the preceding word.
    # This happens when a <kq> element is followed by <text text="׃" />
    # in the MAM-XML — the sof pasuq ends up as its own token.
    SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
    merged = []
    merged_ketiv = []
    for w, is_k in zip(joined, joined_ketiv):
        if w == SOF_PASUQ and merged:
            merged[-1] = merged[-1] + SOF_PASUQ
        else:
            merged.append(w)
            merged_ketiv.append(is_k)

    ketiv_indices = [i for i, k in enumerate(merged_ketiv) if k]
    return {"words": merged, "ketiv_indices": ketiv_indices}


def get_verses_in_range(xml_path, book_osis_prefix, start_cv, end_cv):
    """
    Extract verses from a MAM-XML file in a chapter:verse range.

    Args:
        xml_path: path to the MAM-XML file (e.g., .../xml-vtrad-mam/Job.xml)
        book_osis_prefix: e.g., 'Job'
        start_cv: (chapter, verse) tuple, inclusive
        end_cv: (chapter, verse) tuple, inclusive

    Returns:
        list of dicts, each with:
            cv: str — e.g., '37:9'
            words: list of str — maqaf-joined words
            ketiv_indices: list of int — indices of ketiv (unpointed) words
            parashah_before: None or {"parashah": "spi-pe2"} or {"parashah": "spi-samekh2"}
                — parashah break before this verse (from starts-with-sampe attribute)
    """
    tree = ET.parse(xml_path)
    book39 = tree.getroot()[0]

    sampe_tag = {"pe2": "spi-pe2", "samekh2": "spi-samekh2"}

    verses = []
    for child in book39:
        if child.tag != "chapter":
            continue
        osis = child.attrib.get("osisID", "")  # e.g., 'Job.37'
        if not osis.startswith(book_osis_prefix + "."):
            continue
        ch = int(osis.split(".")[-1])

        for v in child:
            if v.tag != "verse":
                continue
            v_osis = v.attrib["osisID"]
            vs = int(v_osis.split(".")[-1])
            if (ch, vs) < start_cv or (ch, vs) > end_cv:
                continue
            result = get_verse_words(v)
            result["cv"] = f"{ch}:{vs}"

            # Check for parashah break before this verse
            sws = v.attrib.get("starts-with-sampe")
            if sws and sws in sampe_tag:
                result["parashah_before"] = {"parashah": sampe_tag[sws]}
            else:
                result["parashah_before"] = None

            verses.append(result)

    return verses
