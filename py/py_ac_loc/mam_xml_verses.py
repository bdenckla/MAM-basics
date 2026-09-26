"""
Read verses from MAM-simple XML (xml-vtrad-mam) for locating text in manuscripts.

This module serves one application: locating text on the pages and lines of a
manuscript by counting atoms and letters in MAM's word sequence. Its users are the
Aleppo Codex and Cambridge MS Add. 1753 line-break flat streams
(``py_ac_loc/gen_flat_stream.py`` and ``py_cam1753_loc/gen_flat_stream.py``) and the
Evr. II B 55 page index (``evr-ii-b-55/README.md``). An atom is one written form
between spaces or maqafs, and the standing rule is that the atoms are what is written
on the page. What this application uses is where atoms begin and end and which letters
they have. Pointing and accents play no part in it, so a stream that differs from
MAM-simple in marks alone, such as a meteg, differs in nothing that matters here (Ben,
2026-09-26); compare streams without marks, as both line-break checkers do.

``get_verse_words`` splits each element's text at whitespace, joins the pieces across
each maqaf into one entry of ``words``, and attaches a lone sof pasuq to the entry
before it. Both generators then split each entry after every maqaf, giving the atoms.

Every child of a <verse> is dispatched by name, and an unknown element raises
ValueError. What each contributes:

  - <text>: its text.
  - <lp-legarmeih>, <lp-paseq>: the Unicode PASEQ, U+05C0, appended to the atom
    before it. A legarmeh and a narrow-sense paseq have the same glyph.
  - <kq>: its ketiv, unpointed: <kq-k>'s text=, or its <slh-word>'s slhw-desc-0.
    ketiv_indices lists the entries that hold a ketiv. The qere contributes nothing.
  - <kq-trivial>: its pointed text=.
  - <slh-word>: slhw-desc-0, the whole pointed atom.
  - <scrdfftar>: the visible text of its <sdt-target>, in document order. The note
    contributes nothing.
  - <implicit-maqaf>, <shirah-space>: nothing. Neither has text.
  - <spi-invnun>: nothing. An inverted nun is a scribal mark with no text. Seven occur
    in Psalm 107 and two in Numbers 10:35-36; ``mb_sefaria/mam4ajf_handlers.py`` names
    both groups and handles them for Sefaria.
  - <spi-pe2>, <spi-samekh2> within a verse: nothing (see "Parashah breaks" below).
    <spi-pe1> and <spi-samekh1> are dispatched the same way, though MAM-simple has
    neither.

Ben decided on 2026-09-26 what the seven elements this module did not handle until
then contribute, keeping the atoms what is written on the page:

  - <kq-k-velo-q>, a ketiv that is written but not read: its unpointed text, listed
    in ketiv_indices like any ketiv. In Ruth 3:12, אם is atom 5 and גֹאֵ֖ל atom 6,
    as on the page.
  - <kq-k-velo-q-maq>, a maqaf after such a ketiv: nothing. So the entries of
    2 Kgs 5:18 include יִסְלַח־נא and then יְהֹוָ֥ה, and those of 2 Sam 13:33
    include כִּֽי־אם and then אַמְנ֥וֹן.
  - <kq-q-velo-k>, a qere that is read but not written: nothing. In 2 Kgs 19:31,
    atom 10 is תַּעֲשֶׂה־ and atom 11 זֹּֽאת׃. Where the atom before the qere
    ends in a maqaf, at 2 Sam 16:23, 18:20 and Jer 50:29, the maqaf join above makes
    one entry of the atoms on either side of the qere, as 2 Sam 16:23's יִשְׁאַל־בִּדְבַ֣ר.
    Without that join an entry would end in a maqaf, and each generator's split would
    emit an empty atom.
  - <good-ending>, the repeated ending of four books: nothing. The verse keeps only
    its own atoms: Lam 5:22 has 8, ending מְאֹֽד׃.
  - <spi-pe3>, <spi-samekh3> within a verse: nothing, as for <spi-pe2> and
    <spi-samekh2>. So Neh 3:4's atoms run from 1 to 22.
  - <cant-all-three>, in the two Decalogues and at Gen 35:22: its <cant-combined>
    only, read as verse-level <text>, <lp-legarmeih> and <lp-paseq>. That is one text
    with the marks of both strands, <cant-alef> and <cant-bet>. In the Decalogues they
    are the תחתון and עליון strands, and at Gen 35:22 the פשוטה and מדרשית strands.
    Atom numbers and letters are the same as for either strand, but one entry can join
    atoms that each strand alone divides between two chanted words. So Deut 5:6's
    entries include לֹ֣א־יִהְיֶ֥͏ֽה־לְךָ֛֩.

Each of those seven elements has its shape checked against the one it has in every
occurrence in MAM-simple on 2026-09-26, and any other shape raises ValueError. No
MAM-simple verse is refused: ``py/tests/test_mam_xml_verses.py`` runs
``get_verse_words`` over every verse of MAM-simple/xml-vtrad-mam/ and checks that no
entry ends in a maqaf.

Parashah breaks. MAM-simple places a break between books, between chapters, between
verses or within a verse (MAM-simple/doc/reading-mam-simple-xml.md). A stream learns
of a break only from the starts-with-sampe attribute of the verse after it, which
``get_verses_in_range`` turns into parashah_before: pe2, samekh2, pe3 and samekh3 give
{"parashah": "spi-pe2"}, {"parashah": "spi-samekh2"}, {"parashah": "spi-pe3"} and
{"parashah": "spi-samekh3"}. A verse without the attribute gets None, and any other
value raises ValueError. The spi-pe3 and spi-samekh3 markers, Ben's decision of
2026-09-26, keep MAM's hint that the break has no blank line (pe3, MAM's פפפ) or is
in mid-line (samekh3, MAM's ססס). Both line-break editors show them raw until they
are given a label. A break within a verse, of any of the four kinds, never reaches a
stream (Ben, 2026-09-26): how a stream shows one is to be decided when line-break work
reaches a book that has one.

Usage:
    from py_ac_loc.mam_xml_verses import get_verses_in_range

    verses = get_verses_in_range(
        r'C:/path/to/MAM-basics/MAM-simple/xml-vtrad-mam/Job.xml',
        'Job', (37, 9), (38, 20),
    )
    # Returns: [{'cv': '37:9', 'words': [...], 'ketiv_indices': [], 'parashah_before': None}, ...]
    # parashah_before is None or one of the four markers above
"""

import xml.etree.ElementTree as ET

PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"

# The starts-with-sampe values, and the parashah-break element each one names.
_SAMPE_PARASHAH = {
    "pe2": "spi-pe2",
    "samekh2": "spi-samekh2",
    "pe3": "spi-pe3",
    "samekh3": "spi-samekh3",
}
_PARASHAH_TAGS = frozenset(_SAMPE_PARASHAH.values())

_CANT_STRANDS = ["cant-combined", "cant-alef", "cant-bet"]
_NU10_INVNUN_NEIGHBOR = {"class": "nu10-invnun-neighbor"}


def _scribal_difference_target_text(sdt, verse_osis):
    """Return the visible target text, rejecting an unrecognised target shape."""
    attribute_text = sdt.attrib.get("text", "")
    if attribute_text.strip():
        if len(sdt):
            raise ValueError(
                f"<sdt-target> has text= and child elements in {verse_osis}"
            )
        return attribute_text.strip()

    parts = []
    for child in sdt:
        if child.tag == "slh-word":
            text = child.attrib.get("slhw-desc-0", "")
            if not text.strip():
                raise ValueError(
                    f"<slh-word> under <sdt-target> has no slhw-desc-0 "
                    f"in {verse_osis}"
                )
            parts.append(text)
        elif child.tag == "text":
            if "text" not in child.attrib:
                raise ValueError(
                    f"<text> under <sdt-target> has no text= in {verse_osis}"
                )
            parts.append(child.attrib["text"])
        elif child.tag == "spi-pe2":
            pass
        else:
            raise ValueError(
                f"Unhandled <sdt-target> child <{child.tag}> in {verse_osis}"
            )
    return "".join(parts).strip()


def _lone_text(el, verse_osis):
    """Return el's text=, which must be non-empty and el's only attribute."""
    if set(el.attrib) != {"text"} or len(el) or not el.attrib["text"].strip():
        raise ValueError(
            f"<{el.tag}> in {verse_osis} is not a non-empty text= alone: "
            f"attributes {el.attrib}, {len(el)} children"
        )
    return el.attrib["text"]


def _check_bare(el, verse_osis, allowed_attrib=None):
    """Raise unless el has no children and its attributes are none or allowed_attrib."""
    if len(el) or (el.attrib and el.attrib != allowed_attrib):
        raise ValueError(
            f"<{el.tag}> in {verse_osis} is not bare: "
            f"attributes {el.attrib}, {len(el)} children"
        )


def _strand_words(strand, verse_osis):
    """Check one strand of a <cant-all-three> and return its text split at whitespace.

    A strand has a text= alone, or no attributes and children drawn from <text>,
    <lp-legarmeih> and <lp-paseq>, read as they are directly under a <verse>.
    """
    if "text" in strand.attrib:
        return _lone_text(strand, verse_osis).split()
    if strand.attrib or not len(strand):
        raise ValueError(
            f"<{strand.tag}> in {verse_osis} has neither a text= alone nor children "
            f"alone: attributes {strand.attrib}, {len(strand)} children"
        )
    words = []
    for piece in strand:
        if piece.tag == "text":
            words.extend(_lone_text(piece, verse_osis).split())
        elif piece.tag in ("lp-legarmeih", "lp-paseq"):
            _check_bare(piece, verse_osis)
            if not words:
                raise ValueError(
                    f"<{piece.tag}> opens <{strand.tag}> in {verse_osis}, "
                    f"with no text before it"
                )
            words[-1] = words[-1] + PASEQ
        else:
            raise ValueError(
                f"Unhandled <{strand.tag}> child <{piece.tag}> in {verse_osis}"
            )
    return words


def _cant_combined_words(cant_all_three, verse_osis):
    """Check a <cant-all-three> and all three strands; return <cant-combined>'s words.

    Ben's decision of 2026-09-26: the combined text, which has the marks of both
    strands, and neither strand alone.
    """
    strands = list(cant_all_three)
    if cant_all_three.attrib or [s.tag for s in strands] != _CANT_STRANDS:
        raise ValueError(
            f"<cant-all-three> in {verse_osis} does not have exactly the children "
            f"{_CANT_STRANDS} and no attributes: {[s.tag for s in strands]}, "
            f"{cant_all_three.attrib}"
        )
    combined, _alef, _bet = [_strand_words(s, verse_osis) for s in strands]
    return combined


def get_verse_words(verse_el):
    """
    Extract the entries of a MAM-simple XML <verse> element, as the module
    docstring describes.

    Args:
        verse_el: an xml.etree.ElementTree Element for a <verse>.

    Returns a dict:
        words: list of str — the verse's entries, atoms joined across each maqaf
        ketiv_indices: list of int — indices in `words` of the entries holding a ketiv

    Raises ValueError on an unknown child element, or on a shape of a
    <kq-k-velo-q>, <kq-k-velo-q-maq>, <kq-q-velo-k>, <good-ending>, <spi-pe3>,
    <spi-samekh3> or <cant-all-three> that MAM-simple does not have.
    """
    verse_osis = verse_el.attrib.get("osisID", "?")
    raw_words = []
    ketiv_flags = []

    if "text" in verse_el.attrib:
        # Simple verse: text is directly on the element
        raw_words = verse_el.attrib["text"].split()
        ketiv_flags = [False] * len(raw_words)
    else:
        # Complex verse: iterate children
        for i, child in enumerate(verse_el):
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
                # Scribal difference target — extract visible text in document order.
                sdt = child.find("sdt-target")
                if sdt is not None:
                    text = _scribal_difference_target_text(sdt, verse_osis)
                    if text:
                        ws = text.split()
                        raw_words.extend(ws)
                        ketiv_flags.extend([False] * len(ws))
            elif tag == "implicit-maqaf":
                pass  # No visible text
            elif tag == "shirah-space":
                pass  # Visual spacing in song layout, no text
            elif tag == "spi-invnun":
                pass  # Inverted nun (nun hafukha) — a scribal mark, no text
            elif tag in ("spi-pe2", "spi-samekh2", "spi-pe1", "spi-samekh1"):
                pass  # A break within a verse contributes nothing
            elif tag == "spi-pe3":
                # Ben, 2026-09-26: a break within a verse contributes nothing.
                _check_bare(child, verse_osis)
            elif tag == "spi-samekh3":
                # Ben, 2026-09-26: a break within a verse contributes nothing.
                _check_bare(child, verse_osis, _NU10_INVNUN_NEIGHBOR)
            elif tag == "kq-k-velo-q":
                # Ben, 2026-09-26: a ketiv that is not read is written, so it is
                # an atom, unpointed, like any ketiv.
                ws = _lone_text(child, verse_osis).split()
                raw_words.extend(ws)
                ketiv_flags.extend([True] * len(ws))
            elif tag == "kq-k-velo-q-maq":
                # Ben, 2026-09-26: no maqaf after a ketiv that is not read.
                _check_bare(child, verse_osis)
                if i == 0 or verse_el[i - 1].tag != "kq-k-velo-q":
                    raise ValueError(
                        f"<kq-k-velo-q-maq> in {verse_osis} does not follow "
                        f"a <kq-k-velo-q>"
                    )
            elif tag == "kq-q-velo-k":
                # Ben, 2026-09-26: a qere that is not written is no atom.
                _lone_text(child, verse_osis)
            elif tag == "good-ending":
                # Ben, 2026-09-26: the repeated ending contributes no atoms.
                _lone_text(child, verse_osis)
            elif tag == "cant-all-three":
                # Ben, 2026-09-26: the combined text of both strands.
                ws = _cant_combined_words(child, verse_osis)
                raw_words.extend(ws)
                ketiv_flags.extend([False] * len(ws))
            else:
                raise ValueError(f"Unhandled tag <{tag}> in verse {verse_osis}")

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
    # in the MAM-simple XML — the sof pasuq ends up as its own token.
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


def _find_book39(root, book_osis_prefix, xml_path):
    """Return the one <book39> under root whose osisID is book_osis_prefix."""
    if root.tag != "book24":
        raise ValueError(f"The root of {xml_path} is <{root.tag}>, not <book24>")
    matches = []
    for child in root:
        if child.tag == "book39":
            if child.attrib["osisID"] == book_osis_prefix:
                matches.append(child)
        elif child.tag in _PARASHAH_TAGS:
            pass  # A break between books reaches a stream through starts-with-sampe
        else:
            raise ValueError(f"Unhandled <book24> child <{child.tag}> in {xml_path}")
    if len(matches) != 1:
        raise ValueError(
            f"{xml_path} has {len(matches)} <book39> elements whose osisID is "
            f"{book_osis_prefix!r}, not 1"
        )
    return matches[0]


def _parashah_before(verse_el):
    """Return the marker for a parashah break before verse_el, or None."""
    sampe = verse_el.attrib.get("starts-with-sampe")
    if sampe is None:
        return None
    if sampe not in _SAMPE_PARASHAH:
        raise ValueError(
            f"Unhandled starts-with-sampe {sampe!r} in {verse_el.attrib['osisID']}"
        )
    return {"parashah": _SAMPE_PARASHAH[sampe]}


def get_verses_in_range(xml_path, book_osis_prefix, start_cv, end_cv):
    """
    Extract verses from a MAM-simple XML file in a chapter:verse range.

    Args:
        xml_path: path to a MAM-simple XML file (e.g., .../xml-vtrad-mam/Job.xml)
        book_osis_prefix: the osisID of one <book39> in that file, e.g., 'Job', or
            '2Chr' in 1Chr-2Chr.xml
        start_cv: (chapter, verse) tuple, inclusive
        end_cv: (chapter, verse) tuple, inclusive

    Returns:
        list of dicts, each with:
            cv: str — e.g., '37:9'
            words: list of str — the verse's entries, as from get_verse_words
            ketiv_indices: list of int — indices in `words` of the entries holding
                a ketiv
            parashah_before: None, or {"parashah": ...} with "spi-pe2",
                "spi-samekh2", "spi-pe3" or "spi-samekh3" — parashah break before
                this verse (from its starts-with-sampe attribute)

    Raises ValueError unless the file has exactly one <book39> whose osisID is
    book_osis_prefix, on a starts-with-sampe value other than those four, and on an
    element this module does not handle.
    """
    tree = ET.parse(xml_path)
    book39 = _find_book39(tree.getroot(), book_osis_prefix, xml_path)

    verses = []
    for child in book39:
        if child.tag in _PARASHAH_TAGS:
            continue  # A break between chapters: see starts-with-sampe below
        if child.tag != "chapter":
            raise ValueError(f"Unhandled <book39> child <{child.tag}> in {xml_path}")
        osis = child.attrib["osisID"]  # e.g., 'Job.37'
        if not osis.startswith(book_osis_prefix + "."):
            raise ValueError(f"Chapter {osis} is not in book {book_osis_prefix}")
        ch = int(osis.split(".")[-1])

        for v in child:
            if v.tag in _PARASHAH_TAGS:
                continue  # A break between verses: see starts-with-sampe below
            if v.tag != "verse":
                raise ValueError(f"Unhandled <chapter> child <{v.tag}> in {osis}")
            v_osis = v.attrib["osisID"]
            vs = int(v_osis.split(".")[-1])
            if (ch, vs) < start_cv or (ch, vs) > end_cv:
                continue
            result = get_verse_words(v)
            result["cv"] = f"{ch}:{vs}"

            # Check for parashah break before this verse
            result["parashah_before"] = _parashah_before(v)

            verses.append(result)

    return verses
