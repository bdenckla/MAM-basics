"""
Read verses from MAM-simple JSON (json-vtrad-mam) for locating text in manuscripts.

This module serves one application: locating text on the pages and lines of a
manuscript by counting atoms and letters in MAM's word sequence. Its user is the
Evr. II B 55 page index, whose consumer guide in ``evr-ii-b-55/README.md`` defines an
atom number through ``get_verse_atoms``. The Aleppo Codex and Cambridge MS Add. 1753
flat streams under ``aleppo/`` and ``cam1753/`` were made with the same segmentation,
by generators that were retired on 2026-09-26. An atom is one written form between
spaces or maqaf marks, and the standing rule is that the atoms are what is written on the
page. What this application uses is where atoms begin and end and which letters they
have. Pointing and accents play no part in it, so a stream that differs from
MAM-simple in marks alone, such as a meteg, differs in nothing that matters here (Ben,
2026-09-26).

``get_verse_words`` splits each element's text at whitespace, joins the pieces across
each maqaf into one entry of ``words``, and attaches a lone sof pasuq to the entry
before it. ``get_verse_atoms`` then splits each entry after every maqaf, keeping the
maqaf on the atom before it, which gives the atoms. Until 2026-09-26 each flat-stream
generator made that split itself.

Every child of a <verse> is dispatched by name, and an unknown element raises
ValueError. What each contributes:

  - <text>: its text.
  - <lp-legarmeih>, <lp-paseq>: the Unicode PASEQ, U+05C0, appended to the atom
    before it. A legarmeh and a narrow-sense paseq have the same glyph.
  - <kq>: its ketiv, unpointed: <kq-k>'s text=, or its <slh-word>'s slhw-desc-0.
    ketiv_indices lists the entries that hold a ketiv. The qere contributes nothing.
  - <kq-trivial>: its pointed text=, or its <text>/<lp-legarmeih> child form.
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
    Without that join an entry would end in a maqaf, and ``get_verse_atoms`` would
    emit an empty atom.
  - <good-ending>, the repeated ending of four books: nothing. The verse keeps only
    its own atoms: Lam 5:22 has 8, ending מְאֹֽד׃.
  - <spi-pe3>, <spi-samekh3> within a verse: nothing, as for <spi-pe2> and
    <spi-samekh2>. So Neh 3:4's atoms run from 1 to 22.
  - <cant-all-three>, in the two Decalogues and at Gen 35:22: its <cant-combined>
    only, read as verse-level <text>, <lp-legarmeih> and <lp-paseq>. That is one text
    representing the two strands, <cant-alef> and <cant-bet>; it need not include
    every mark of each strand. In the Decalogues they
    are the תחתון and עליון strands, and at Gen 35:22 the פשוטה and מדרשית strands.
    Atom numbers and letters are the same as for either strand, but one entry can join
    atoms that each strand alone divides between two chanted words. So Deut 5:6's
    entries include לֹ֣א־יִהְיֶ֥͏ֽה־לְךָ֛֩.

Each of those seven elements has its shape checked against the one it has in every
occurrence in MAM-simple on 2026-09-26, and any other shape raises ValueError. No
MAM-simple verse is refused: ``py/tests/test_mam_json_verses.py`` runs
``get_verse_atoms`` over every verse of MAM-simple/json-vtrad-mam/ and checks that no
atom is empty.

Parashah breaks. MAM-simple places a break between books, between chapters, between
verses or within a verse (gh-pages/MAM-simple/reading-mam-simple-json.html).
A caller learns of a break only from the starts-with-sampe attribute of the verse after it, which
``get_verses_in_range`` turns into parashah_before: pe2, samekh2, pe3 and samekh3 give
{"parashah": "spi-pe2"}, {"parashah": "spi-samekh2"}, {"parashah": "spi-pe3"} and
{"parashah": "spi-samekh3"}. A verse without the attribute gets None, and any other
value raises ValueError. The spi-pe3 and spi-samekh3 markers, Ben's decision of
2026-09-26, keep MAM's hint that the break has no blank line (pe3, MAM's פפפ) or is
in mid-line (samekh3, MAM's ססס). A break within a verse, of any of the four kinds,
never reaches a caller, as Ben decided on 2026-09-26 for the flat streams.

Usage:
    from mb_cmn.mam_json_verses import get_verses_in_range

    verses = get_verses_in_range(
        r'C:/path/to/MAM-basics/MAM-simple/json-vtrad-mam/Job.json',
        'Job', (37, 9), (38, 20),
    )
    # Returns: [{'cv': '37:9', 'words': [...], 'ketiv_indices': [], 'atoms': [...],
    #            'parashah_before': None}, ...]
    # parashah_before is None or one of the four markers above
"""

from mb_cmn.mam_simple_json import (
    attributes as _attributes,
    children as _children,
    find_child as _find_child,
    read_book_group,
)
from mb_cmn.silluq_before_meteg import validate_silluq_before_meteg

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

_CANT_FORMS = ["cant-combined", "cant-alef", "cant-bet"]
_NU10_INVNUN_NEIGHBOR = {"class": "nu10-invnun-neighbor"}


def _scribal_difference_target_text(sdt, verse_osis):
    """Return the visible target text, rejecting an unrecognised target shape."""
    attribute_text = _attributes(sdt).get("text", "")
    if attribute_text.strip():
        if len(_children(sdt)):
            raise ValueError(
                f"<sdt-target> has text= and child elements in {verse_osis}"
            )
        return attribute_text.strip()

    parts = []
    for child in _children(sdt):
        if child["type"] == "slh-word":
            text = _attributes(child).get("slhw-desc-0", "")
            if not text.strip():
                raise ValueError(
                    f"<slh-word> under <sdt-target> has no slhw-desc-0 "
                    f"in {verse_osis}"
                )
            parts.append(text)
        elif child["type"] == "silluq-before-meteg":
            parts.append(_silluq_before_meteg_text(child, verse_osis))
        elif child["type"] == "text":
            if "text" not in _attributes(child):
                raise ValueError(
                    f"<text> under <sdt-target> has no text= in {verse_osis}"
                )
            parts.append(_attributes(child)["text"])
        elif child["type"] == "spi-pe2":
            pass
        else:
            raise ValueError(
                f"Unhandled <sdt-target> child <{child['type']}> in {verse_osis}"
            )
    return "".join(parts).strip()


def _lone_text(el, verse_osis):
    """Return el's text=, which must be non-empty and el's only attribute."""
    if (
        set(_attributes(el)) != {"text"}
        or len(_children(el))
        or not _attributes(el)["text"].strip()
    ):
        raise ValueError(
            f"<{el['type']}> in {verse_osis} is not a non-empty text= alone: "
            f"attributes {_attributes(el)}, {len(_children(el))} children"
        )
    return _attributes(el)["text"]


def _silluq_before_meteg_text(el, verse_osis):
    if set(_attributes(el)) != {"text", "letters-with-silluq"} or len(_children(el)):
        raise ValueError(
            f"Unexpected <silluq-before-meteg> shape in {verse_osis}: {_attributes(el)}"
        )
    text = _attributes(el)["text"]
    validate_silluq_before_meteg(
        text, _attributes(el)["letters-with-silluq"], verse_osis
    )
    return text


def _check_bare(el, verse_osis, allowed_attrib=None):
    """Raise unless el has no children and its attributes are none or allowed_attrib."""
    if len(_children(el)) or (_attributes(el) and _attributes(el) != allowed_attrib):
        raise ValueError(
            f"<{el['type']}> in {verse_osis} is not bare: "
            f"attributes {_attributes(el)}, {len(_children(el))} children"
        )


def _form_words(strand, verse_osis):
    """Check one form of a <cant-all-three> and return its text split at whitespace.

    A form has a text= alone, or no attributes and children drawn from <text>,
    <lp-legarmeih> and <lp-paseq>, read as they are directly under a <verse>.
    """
    if "text" in _attributes(strand):
        return _lone_text(strand, verse_osis).split()
    if _attributes(strand) or not len(_children(strand)):
        raise ValueError(
            f"<{strand['type']}> in {verse_osis} has neither a text= alone nor children "
            f"alone: attributes {_attributes(strand)}, {len(_children(strand))} children"
        )
    words = []
    for piece in _children(strand):
        if piece["type"] == "silluq-before-meteg":
            words.extend(_silluq_before_meteg_text(piece, verse_osis).split())
        elif piece["type"] == "text":
            words.extend(_lone_text(piece, verse_osis).split())
        elif piece["type"] in ("lp-legarmeih", "lp-paseq"):
            _check_bare(piece, verse_osis)
            if not words:
                raise ValueError(
                    f"<{piece['type']}> opens <{strand['type']}> in {verse_osis}, "
                    f"with no text before it"
                )
            words[-1] = words[-1] + PASEQ
        else:
            raise ValueError(
                f"Unhandled <{strand['type']}> child <{piece['type']}> in {verse_osis}"
            )
    return words


def _cant_combined_words(cant_all_three, verse_osis):
    """Check the two strands and combined representation; return the combined words.

    Ben's decision of 2026-09-26 selects their combined representation. It need
    not include every mark of each strand.
    """
    strands = _children(cant_all_three)
    if _attributes(cant_all_three) or [s["type"] for s in strands] != _CANT_FORMS:
        raise ValueError(
            f"<cant-all-three> in {verse_osis} does not have exactly the children "
            f"{_CANT_FORMS} and no attributes: {[s['type'] for s in strands]}, "
            f"{_attributes(cant_all_three)}"
        )
    combined, _alef, _bet = [_form_words(s, verse_osis) for s in strands]
    return combined


def _trivial_kq_words(el, verse_osis):
    """Read either known trivial ketiv/qere form, preserving the pointed ketiv."""
    if "text" in _attributes(el):
        return _lone_text(el, verse_osis).split()
    if _attributes(el) or [child["type"] for child in _children(el)] != [
        "text",
        "lp-legarmeih",
    ]:
        raise ValueError(f"Unsupported <kq-trivial> shape in {verse_osis}")
    words = _lone_text(_children(el)[0], verse_osis).split()
    _check_bare(_children(el)[1], verse_osis)
    words[-1] += PASEQ
    return words


def get_verse_words(verse_el):
    """
    Extract the entries of a MAM-simple JSON <verse> element, as the module
    docstring describes.

    Args:
        verse_el: a JSON object whose type is verse.

    Returns a dict:
        words: list of str — the verse's entries, atoms joined across each maqaf
        ketiv_indices: list of int — indices in `words` of the entries holding a ketiv

    Raises ValueError on an unknown child element, or on a shape of a
    <kq-k-velo-q>, <kq-k-velo-q-maq>, <kq-q-velo-k>, <good-ending>, <spi-pe3>,
    <spi-samekh3> or <cant-all-three> that MAM-simple does not have.
    """
    verse_osis = _attributes(verse_el).get("osisID", "?")
    raw_words = []
    ketiv_flags = []

    if "text" in _attributes(verse_el):
        # Simple verse: text is directly on the element
        raw_words = _attributes(verse_el)["text"].split()
        ketiv_flags = [False] * len(raw_words)
    else:
        # Complex verse: iterate children
        for i, child in enumerate(_children(verse_el)):
            tag = child["type"]
            if tag == "silluq-before-meteg":
                ws = _silluq_before_meteg_text(child, verse_osis).split()
                raw_words.extend(ws)
                ketiv_flags.extend([False] * len(ws))
            elif tag == "text":
                text = _attributes(child).get("text", "").strip()
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
                kq_k = _find_child(child, "kq-k")
                if kq_k is not None:
                    kt = _attributes(kq_k).get("text", "").strip()
                    if not kt:
                        slh = _find_child(kq_k, "slh-word")
                        if slh is not None:
                            kt = _attributes(slh).get("slhw-desc-0", "").strip()
                    assert kt, (
                        f"<kq-k> has no text= and no slh-word child "
                        f"in {_attributes(verse_el).get('osisID', '?')}"
                    )
                    ws = kt.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([True] * len(ws))
            elif tag == "kq-trivial":
                ws = _trivial_kq_words(child, verse_osis)
                raw_words.extend(ws)
                ketiv_flags.extend([False] * len(ws))
            elif tag == "slh-word":
                # Suspended-letter word — use desc-0 (full pointed word)
                text = _attributes(child).get("slhw-desc-0", "").strip()
                if text:
                    ws = text.split()
                    raw_words.extend(ws)
                    ketiv_flags.extend([False] * len(ws))
            elif tag == "scrdfftar":
                # Scribal difference target — extract visible text in document order.
                sdt = _find_child(child, "sdt-target")
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
                if i == 0 or _children(verse_el)[i - 1]["type"] != "kq-k-velo-q":
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
    # in the MAM-simple JSON — the sof pasuq ends up as its own token.
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


def _atoms_of(words):
    """Split each entry after every maqaf, keeping the maqaf on the atom before it."""
    atoms = []
    for entry in words:
        parts = entry.split(MAQAF)
        atoms.extend(part + MAQAF for part in parts[:-1])
        atoms.append(parts[-1])
    return atoms


def get_verse_atoms(verse_el):
    """
    Return the atoms of a MAM-simple JSON <verse> element: each entry of
    ``get_verse_words``'s ``words``, split after every maqaf, which stays with the
    atom before it. An atom's number in its verse is its index here plus one.

    Raises ValueError where ``get_verse_words`` does.
    """
    return _atoms_of(get_verse_words(verse_el)["words"])


def _find_book39(root, book_osis_prefix, json_path):
    """Return the one <book39> under root whose osisID is book_osis_prefix."""
    if root["type"] != "book24":
        raise ValueError(f"The root of {json_path} is <{root['type']}>, not <book24>")
    matches = []
    for child in _children(root):
        if child["type"] == "book39":
            if _attributes(child)["osisID"] == book_osis_prefix:
                matches.append(child)
        elif child["type"] in _PARASHAH_TAGS:
            pass  # A break between books reaches a stream through starts-with-sampe
        else:
            raise ValueError(
                f"Unhandled <book24> child <{child['type']}> in {json_path}"
            )
    if len(matches) != 1:
        raise ValueError(
            f"{json_path} has {len(matches)} <book39> elements whose osisID is "
            f"{book_osis_prefix!r}, not 1"
        )
    return matches[0]


def _parashah_before(verse_el):
    """Return the marker for a parashah break before verse_el, or None."""
    sampe = _attributes(verse_el).get("starts-with-sampe")
    if sampe is None:
        return None
    if sampe not in _SAMPE_PARASHAH:
        raise ValueError(
            f"Unhandled starts-with-sampe {sampe!r} in {_attributes(verse_el)['osisID']}"
        )
    return {"parashah": _SAMPE_PARASHAH[sampe]}


def get_verses_in_range(json_path, book_osis_prefix, start_cv, end_cv):
    """
    Extract verses from a MAM-simple JSON file in a chapter:verse range.

    Args:
        json_path: path to a MAM-simple JSON file (e.g., .../json-vtrad-mam/Job.json)
        book_osis_prefix: the osisID of one <book39> in that file, e.g., 'Job', or
            '2Chr' in 1Chr-2Chr.json
        start_cv: (chapter, verse) tuple, inclusive
        end_cv: (chapter, verse) tuple, inclusive

    Returns:
        list of dicts, each with:
            cv: str — e.g., '37:9'
            words: list of str — the verse's entries, as from get_verse_words
            ketiv_indices: list of int — indices in `words` of the entries holding
                a ketiv
            atoms: list of str — the verse's atoms, as from get_verse_atoms
            parashah_before: None, or {"parashah": ...} with "spi-pe2",
                "spi-samekh2", "spi-pe3" or "spi-samekh3" — parashah break before
                this verse (from its starts-with-sampe attribute)

    Raises ValueError unless the file has exactly one <book39> whose osisID is
    book_osis_prefix, on a starts-with-sampe value other than those four, and on an
    element this module does not handle.
    """
    book39 = _find_book39(read_book_group(json_path), book_osis_prefix, json_path)

    verses = []
    for child in _children(book39):
        if child["type"] in _PARASHAH_TAGS:
            continue  # A break between chapters: see starts-with-sampe below
        if child["type"] != "chapter":
            raise ValueError(
                f"Unhandled <book39> child <{child['type']}> in {json_path}"
            )
        osis = _attributes(child)["osisID"]  # e.g., 'Job.37'
        if not osis.startswith(book_osis_prefix + "."):
            raise ValueError(f"Chapter {osis} is not in book {book_osis_prefix}")
        ch = int(osis.split(".")[-1])

        for v in _children(child):
            if v["type"] in _PARASHAH_TAGS:
                continue  # A break between verses: see starts-with-sampe below
            if v["type"] != "verse":
                raise ValueError(f"Unhandled <chapter> child <{v['type']}> in {osis}")
            v_osis = _attributes(v)["osisID"]
            vs = int(v_osis.split(".")[-1])
            if (ch, vs) < start_cv or (ch, vs) > end_cv:
                continue
            result = get_verse_words(v)
            result["atoms"] = _atoms_of(result["words"])
            result["cv"] = f"{ch}:{vs}"

            # Check for parashah break before this verse
            result["parashah_before"] = _parashah_before(v)

            verses.append(result)

    return verses
