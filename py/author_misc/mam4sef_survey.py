"""MAM-for-Sefaria's tracked files, read with closed dispatch and counted.

This is the reading half of the three pages that document MAM-for-Sefaria, whose modules
``mam4sef_common.py`` beside it names: "The encoding of MAM for Sefaria", on ``csv/``, and the
pages on the listings and on the AJF variant.  ``survey()`` returns everything the pages state
about the files, and they state nothing they do not get from here.

WHAT IS READ.  Every tracked file of the product's four folders, listed with
``git ls-files -z``: the 39 Sefaria CSV files of ``MAM-for-Sefaria/csv/``, the 39 AJF CSV files
of ``MAM-for-Sefaria/csv-ajf/``, and the 78 Unicode-name listings of
``MAM-for-Sefaria/misc/unicode-names/`` and ``MAM-for-Sefaria/misc/unicode-names-ajf/``.
Nothing else in MAM-basics reads these files back, and their only writer,
``py/main_mam4sef.py``, is run by hand, so they can lag MAM-simple (``AGENTS.md``, "What this
repository's products are").  That is why the pages read them rather than MAM-simple: what
they document is what the product ships.  The one exception is the meteg-after-silluq table, whose
"other versions of MAM" row is by definition not what the product ships; it is read from the
silluq-before-meteg annotations of ``MAM-simple/json-vtrad-mam/``, the input that
``py/tests/test_sefaria_silluq_documentation.py`` checks the table against.

CLOSED DISPATCH.  Every element, class, attribute, character reference and code point of the
files is dispatched on by name, and anything unrecognized raises, so the pages' lists of markup
and characters are complete by construction.  The string-level features the pages name are
dispatched the same way: each run of NO-BREAK SPACE by its neighbours, each PASEQ by its markup
and spacing, each COMBINING GRAPHEME JOINER by the marks around it, each ketiv/qere pair by its
order, separator and word counts.  A new feature in a regenerated file therefore stops the build
here, as a finding for Ben, rather than reaching the pages undescribed.

THE LISTINGS ARE RE-DERIVED.  Each listing is rebuilt from its CSV file with the line format of
``py/mb_misc/write_utils.py`` and the short names of ``mb_cmn.uni_heb``, and must equal the
tracked listing.  The one difference allowed is the one the CSV writer makes:
``py/mb_sefaria/write_utils_sef_or_ajf.py`` strips trailing spaces from a row's last field, so a
listing, written from the unstripped text, can end a verse with SPACE lines that the CSV lacks.

Every count here is computed, never typed.  The checks that a page sentence relies on raise
rather than warn, as ``accgram.maqaf_nonfinal_accents_page.pin_claims`` does.
"""

import codecs
import collections
import csv
import dataclasses
import functools
import html.parser
import io
import re
import subprocess
import unicodedata

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import mam_simple_json
from mb_cmn import paths
from mb_cmn import str_defs as sd
from mb_cmn import uni_heb
from mb_cmn import unicode_data
from mb_cmn.git_process import git_command
from mb_cmn.uni_denorm import has_std_mark_order
from mb_misc import osis_book_abbrevs
from mb_sefaria import mam4ajf_handlers
from mb_sefaria import mam4sef_handlers
from mb_sefaria import sef_cmn

PRODUCT_DIR = "MAM-for-Sefaria"
FOLDER_CSV = "csv"
FOLDER_AJF = "csv-ajf"
FOLDER_NAMES = "misc/unicode-names"
FOLDER_NAMES_AJF = "misc/unicode-names-ajf"
FOLDERS = (FOLDER_CSV, FOLDER_AJF, FOLDER_NAMES, FOLDER_NAMES_AJF)
PROVENANCE_NAME = "_provenance.md"
HEADER_KEYS = (
    "Index Title",
    "Version Title",
    "Language",
    "Version Source",
    "Version Notes",
)

EM_DASH = "\N{EM DASH}"
BOOKS = tuple(sef_cmn.SEF_BKNA.values())
LETTERS = "".join(chr(cp) for cp in range(0x05D0, 0x05EB))
_LETTER = "[א-ת]"
# Every Hebrew mark the files may attach to a letter: the accents and points, the two
# extraordinary dots, and COMBINING GRAPHEME JOINER.  The four Hebrew punctuation marks the files
# have, MAQAF, PASEQ, SOF PASUQ and NUN HAFUKHA, are not among them: they stand between atoms.
_MARK = (
    "[\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW POINT METEG}\N{HEBREW POINT RAFE}"
    "\N{HEBREW POINT SHIN DOT}\N{HEBREW POINT SIN DOT}\N{HEBREW MARK UPPER DOT}"
    "\N{HEBREW MARK LOWER DOT}\N{HEBREW POINT QAMATS QATAN}"
    "\N{COMBINING GRAPHEME JOINER}]"
)
MARK_CLASS = _MARK
_MARK_RE = re.compile(_MARK)
CLUSTER_RE = re.compile(f"{_LETTER}{_MARK}*")
ATOM_RE = re.compile(f"(?:{_LETTER}{_MARK}*)+")
# A trivial pair's span: one pointed atom, or atoms joined by maqaf marks, with a legarmeh
# at its end where the atom has one.
_TRIVIAL_RE = re.compile(
    f"{ATOM_RE.pattern}(?:{hpu.MAQ}{ATOM_RE.pattern})*(?:{sd.THSP}{hpu.PASOLEG})?"
)
VOWELS = frozenset(
    "\N{HEBREW POINT SHEVA}\N{HEBREW POINT HATAF SEGOL}\N{HEBREW POINT HATAF PATAH}"
    "\N{HEBREW POINT HATAF QAMATS}\N{HEBREW POINT HIRIQ}\N{HEBREW POINT TSERE}"
    "\N{HEBREW POINT SEGOL}\N{HEBREW POINT PATAH}\N{HEBREW POINT QAMATS}"
    "\N{HEBREW POINT HOLAM}\N{HEBREW POINT HOLAM HASER FOR VAV}"
    "\N{HEBREW POINT QUBUTS}\N{HEBREW POINT QAMATS QATAN}"
)
_ACCENTS = frozenset(chr(cp) for cp in range(0x0591, 0x05AF))
# The marks the page lists as having code points of their own, each as opposed to that of a
# mark it looks like: QAMATS, HOLAM and YERAH BEN YOMO.
OWN_CODE_POINT_MARKS = (
    "\N{HEBREW POINT QAMATS QATAN}",
    "\N{HEBREW POINT HOLAM HASER FOR VAV}",
    ha.ATN_H,
)
_PUNCTUATION = frozenset((hpu.MAQ, hpu.PASOLEG, hpu.SOPA, hpu.NUN_HAF))
_ASCII = frozenset(" ()[]{}")
# The code points the verse text of csv/ may have, beyond the letters and marks: the
# punctuation above, the ASCII spaces and brackets, EM DASH, and the two spaces that csv/ writes
# as character references.  csv-ajf/ may have the same set less those two spaces.
_OTHER_CODE_POINTS_AJF = _PUNCTUATION | _ASCII | {EM_DASH}
_OTHER_CODE_POINTS_CSV = _OTHER_CODE_POINTS_AJF | {sd.NBSP, sd.THSP}
_ENTITIES = {"nbsp": sd.NBSP, "thinsp": sd.THSP}

# THE ELEMENTS OF csv/, by tag and class, each with the kind this module calls it by.  The
# handlers of py/mb_sefaria/mam4sef_handlers.py emit exactly these; an element absent from this
# table raises in _CellParser.
_ELEMENT_KINDS = {
    ("span", "mam-spi-samekh"): "samekh",
    ("span", "mam-spi-pe"): "pe",
    ("span", "mam-spi-invnun"): "invnun",
    ("span", "mam-implicit-maqaf"): "implicit-maqaf",
    ("span", "mam-kq"): "kq",
    ("span", "mam-kq-k"): "ketiv",
    ("span", "mam-kq-q"): "qere",
    ("span", "mam-kq-trivial"): "trivial",
    ("span", "k-velo-q-maq"): "k-velo-q-maq",
    ("b", None): "legarmeh",
    ("small", None): "small",
    ("big", None): "large",
    ("sup", None): "hung",
    ("br", None): "br",
}
ELEMENT_ORDER = tuple(_ELEMENT_KINDS)
# Where each kind may stand: None is the verse itself.  Measured over every file on
# 2026-10-26; a kind found anywhere else raises.
_ALLOWED_PARENTS = {
    "samekh": {None},
    "pe": {None},
    "invnun": {None},
    "implicit-maqaf": {None},
    "kq": {None},
    "ketiv": {None, "kq"},
    "qere": {None, "kq"},
    "trivial": {None},
    "k-velo-q-maq": {None},
    "legarmeh": {None, "qere", "trivial"},
    "small": {None, "ketiv", "qere"},
    "large": {None},
    "hung": {None},
    "br": {None},
}
_FIXED_TEXT = {
    "samekh": "{\N{HEBREW LETTER SAMEKH}}",
    "pe": "{\N{HEBREW LETTER PE}}",
    "invnun": hpu.NUN_HAF,
    "implicit-maqaf": hpu.MAQ,
    "k-velo-q-maq": hpu.MAQ,
    "legarmeh": hpu.PASOLEG,
}
# The handler keys of the two exporters these pages account for.  A handler added to either
# table raises in check_handlers until a page says what the files have for it.
_SEF_HANDLER_KEYS = frozenset(mam4sef_handlers.HANDLERS)
# The strands of a verse with two cantillations, as the AJF exporter's handler tables and the
# AJF listings name them.
AJF_STRANDS = ("rv-cant-combined", "rv-cant-alef", "rv-cant-bet")


@dataclasses.dataclass
class Element:
    """One element of a verse of csv/, with its offsets in the verse's text."""

    tag: str
    cls: str | None
    kind: str
    parent_kind: str | None
    kids: list = dataclasses.field(default_factory=list)
    start: int = 0
    end: int = 0

    def text(self) -> str:
        return "".join(k if isinstance(k, str) else k.text() for k in self.kids)


@dataclasses.dataclass
class CsvVerse:
    book: str
    bk39id: str
    chapter: int
    verse: int
    ref: str
    poetic: bool
    html: str
    text: str
    elements: list  # every Element, in document order
    top: list  # the verse's children: str or Element

    def scripture(self) -> str:
        """The verse text with its breaks and inverted nun marks replaced by spaces."""
        chars = list(self.text)
        for el in self.elements:
            if el.kind in ("samekh", "pe", "invnun"):
                chars[el.start : el.end] = " " * (el.end - el.start)
        return "".join(chars)


@dataclasses.dataclass
class AjfRow:
    book: str
    bk39id: str
    chapter: int
    verse: int
    ref: str
    poetic: bool
    combined: str
    alef: str
    bet: str


class _CellParser(html.parser.HTMLParser):
    """The HTML of one verse of csv/, parsed with closed dispatch on everything it has."""

    def __init__(self, where):
        super().__init__(convert_charrefs=False)
        self.where = where
        self.top = []
        self.elements = []
        self.text = []
        # Not ``offset``, which html.parser's base class keeps for its own position.
        self.text_pos = 0
        self.entities = collections.Counter()
        self._stack = []

    def _kids(self):
        return self._stack[-1].kids if self._stack else self.top

    def _add_text(self, text):
        kids = self._kids()
        if kids and isinstance(kids[-1], str):
            kids[-1] += text
        else:
            kids.append(text)
        self.text.append(text)
        self.text_pos += len(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if set(attrs) - {"class"}:
            raise ValueError(f"{self.where}: <{tag}> has attributes {attrs}")
        cls = attrs.get("class")
        kind = _ELEMENT_KINDS.get((tag, cls))
        if kind is None:
            raise ValueError(
                f"{self.where}: unrecognized element <{tag} class={cls!r}>"
            )
        parent_kind = self._stack[-1].kind if self._stack else None
        if parent_kind not in _ALLOWED_PARENTS[kind]:
            raise ValueError(f"{self.where}: {kind} inside {parent_kind}")
        el = Element(
            tag, cls, kind, parent_kind, start=self.text_pos, end=self.text_pos
        )
        self._kids().append(el)
        self.elements.append(el)
        if tag != "br":
            self._stack.append(el)

    def handle_startendtag(self, tag, attrs):
        raise ValueError(f"{self.where}: self-closing <{tag}/>")

    def handle_endtag(self, tag):
        if not self._stack or self._stack[-1].tag != tag:
            raise ValueError(f"{self.where}: unexpected </{tag}>")
        el = self._stack.pop()
        el.end = self.text_pos

    def handle_data(self, data):
        for char in data:
            if char in (sd.NBSP, sd.THSP):
                raise ValueError(f"{self.where}: a raw {unicode_data.name(char)}")
        self._add_text(data)

    def handle_entityref(self, name):
        if name not in _ENTITIES:
            raise ValueError(f"{self.where}: unrecognized character reference &{name};")
        self.entities[name] += 1
        self._add_text(_ENTITIES[name])

    def handle_charref(self, name):
        raise ValueError(f"{self.where}: numeric character reference &#{name};")

    def handle_comment(self, data):
        raise ValueError(f"{self.where}: an HTML comment")

    def handle_decl(self, decl):
        raise ValueError(f"{self.where}: a declaration")

    def handle_pi(self, data):
        raise ValueError(f"{self.where}: a processing instruction")

    def unknown_decl(self, data):
        raise ValueError(f"{self.where}: an unknown declaration")


def letters_of(text: str) -> str:
    return "".join(c for c in text if c in LETTERS)


def marks_of(cluster: str) -> str:
    return cluster[1:]


def short_name(char: str) -> str:
    """A code point's Unicode name less its script and class words, as the pages show it."""
    name = unicode_data.name(char)
    for prefix in (
        "HEBREW LETTER ",
        "HEBREW POINT ",
        "HEBREW ACCENT ",
        "HEBREW PUNCTUATION ",
        "HEBREW MARK ",
    ):
        if name.startswith(prefix):
            return name[len(prefix) :]
    return name


@functools.cache
def _tracked(pattern: str) -> tuple:
    root = paths.repo_root()
    out = subprocess.run(
        git_command(root, "ls-files", "-z", "--", pattern),
        check=True,
        capture_output=True,
        encoding="utf-8",
    ).stdout
    return tuple(name for name in out.split("\0") if name)


def _book_files(folder: str, extension: str) -> dict:
    """Each book's tracked file in one folder, keyed by its Sefaria title, in book order."""
    names = _tracked(f"{PRODUCT_DIR}/{folder}/*")
    prefix = f"{PRODUCT_DIR}/{folder}/"
    stems = {}
    for name in names:
        rest = name[len(prefix) :]
        if "/" in rest:
            continue  # a deeper folder, read by its own call
        if rest == PROVENANCE_NAME:
            continue
        if not rest.endswith(extension):
            raise ValueError(f"unexpected tracked file {name}")
        stems[rest[: -len(extension)]] = paths.repo_root() / name
    if f"{prefix}{PROVENANCE_NAME}" not in names:
        raise ValueError(f"{prefix} has no {PROVENANCE_NAME}")
    titles = list(sef_cmn.SEF_BKNA.values())
    if set(stems) != set(titles):
        raise ValueError(f"{prefix}: books {sorted(set(stems) ^ set(titles))}")
    return {title: stems[title] for title in titles}


def _read_crlf_csv(path) -> list:
    raw = path.read_bytes()
    if raw.startswith(codecs.BOM_UTF8):
        raise ValueError(f"{path}: byte-order mark")
    if raw.count(b"\n") != raw.count(b"\r\n"):
        raise ValueError(f"{path}: a line end other than CRLF")
    return list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))


def _parse_ref(ref: str, book: str, where: str) -> tuple:
    match = re.fullmatch(rf"{re.escape(book)} (\d+):(\d+)", ref)
    if match is None:
        raise ValueError(f"{where}: reference {ref!r}")
    return int(match.group(1)), int(match.group(2))


def _disallowed_re(allowed_other: frozenset) -> re.Pattern:
    others = "".join(re.escape(c) for c in sorted(allowed_other))
    return re.compile(f"[^א-ת{_MARK[1:-1]}{others}]")


_DISALLOWED_CSV_RE = _disallowed_re(_OTHER_CODE_POINTS_CSV)
_DISALLOWED_AJF_RE = _disallowed_re(_OTHER_CODE_POINTS_AJF)


def _check_code_points(text: str, disallowed: re.Pattern, where: str) -> None:
    if found := disallowed.search(text):
        raise ValueError(f"{where}: unrecognized code point U+{ord(found[0]):04X}")
    stripped = CLUSTER_RE.sub("", text)
    if _MARK_RE.search(stripped):
        raise ValueError(f"{where}: a mark that follows no letter")
    if not has_std_mark_order(text):
        raise ValueError(f"{where}: not in MAM's mark order")


def _check_element(el: Element, where: str) -> None:
    text = el.text()
    elements = [k for k in el.kids if isinstance(k, Element)]
    if el.kind in _FIXED_TEXT:
        if el.kids != [_FIXED_TEXT[el.kind]]:
            raise ValueError(f"{where}: {el.kind} has {text!r}")
    elif el.kind == "br":
        if el.kids:
            raise ValueError(f"{where}: <br> has contents")
    elif el.kind in ("small", "large", "hung"):
        is_paseq = el.kind == "small" and el.kids == [hpu.PASOLEG]
        if not is_paseq and not (len(el.kids) == 1 and CLUSTER_RE.fullmatch(text)):
            raise ValueError(f"{where}: {el.kind} has {text!r}")
    elif el.kind == "kq":
        if len(el.kids) != 3 or not isinstance(el.kids[1], str):
            raise ValueError(f"{where}: ketiv/qere pair {text!r}")
        kinds = {k.kind for k in elements}
        if kinds != {"ketiv", "qere"} or el.kids[1] not in (" ", hpu.MAQ):
            raise ValueError(f"{where}: ketiv/qere pair {text!r}")
    elif el.kind == "ketiv":
        inner = text[1:-1]
        if text[0] != "(" or text[-1] != ")" or set(inner) - set(LETTERS) - {" "}:
            raise ValueError(f"{where}: ketiv {text!r}")
    elif el.kind == "qere":
        if text[0] != "[" or text[-1] != "]" or not ATOM_RE.search(text):
            raise ValueError(f"{where}: qere {text!r}")
    elif el.kind == "trivial":
        if not _TRIVIAL_RE.fullmatch(text):
            raise ValueError(f"{where}: trivial pair {text!r}")
    else:
        raise ValueError(f"{where}: no check for {el.kind}")


def _check_spacing(verse: CsvVerse, counts: collections.Counter) -> None:
    """Dispatch each PASEQ, THIN SPACE and run of NO-BREAK SPACE by its context."""
    text = verse.text
    starts = collections.defaultdict(list)
    ends = collections.defaultdict(list)
    for el in verse.elements:
        starts[el.start].append(el.kind)
        ends[el.end].append(el.kind)
    for el in verse.elements:
        if el.kind == "legarmeh":
            after = text[el.end : el.end + 1]
            if text[el.start - 1 : el.start] != sd.THSP or after not in (" ", "]"):
                raise ValueError(f"{verse.ref}: legarmeh in {text!r}")
            counts["legarmeh"] += 1
        elif el.kind == "small" and el.kids == [hpu.PASOLEG]:
            before = text[el.start - 2 : el.start]
            after = text[el.end : el.end + 2]
            if (
                len(before) != 2
                or len(after) != 2
                or before[1] != sd.THSP
                or after[0] != sd.THSP
                or before[0].isspace()
                or after[1].isspace()
            ):
                raise ValueError(f"{verse.ref}: paseq in {text!r}")
            counts["paseq"] += 1
    if text.count(hpu.PASOLEG) != sum(
        1 for el in verse.elements if el.kids == [hpu.PASOLEG]
    ):
        raise ValueError(f"{verse.ref}: a PASEQ outside <b> and <small>")
    thin = text.count(sd.THSP)
    expected_thin = sum(
        1 if el.kind == "legarmeh" else 2
        for el in verse.elements
        if el.kids == [hpu.PASOLEG]
    )
    if thin != expected_thin:
        raise ValueError(f"{verse.ref}: a THIN SPACE beside no PASEQ")
    for match in re.finditer(f"{sd.NBSP}+", text):
        a, b = match.span()
        run = b - a
        after = starts.get(b, [])
        before = ends.get(a, [])
        if run == 1 and ("samekh" in after or "pe" in after):
            context = "before-break"
        elif run == 8 and "samekh" in before:
            context = "after-samekh"
        elif run == 1 and "invnun" in before:
            context = "after-invnun"
        elif run == 1 and "invnun" in after:
            context = "before-invnun"
        elif run == 8:
            context = "song-layout"
        else:
            raise ValueError(f"{verse.ref}: {run} NO-BREAK SPACE in {text!r}")
        counts[f"nbsp {context}"] += 1
        if context == "song-layout":
            counts[f"song-layout {verse.book} {verse.chapter}"] += 1
    for el in verse.elements:
        if el.kind == "pe":
            following = [k for k in verse.top if isinstance(k, Element)]
            index = following.index(el)
            if index + 1 >= len(following) or following[index + 1].kind != "br":
                raise ValueError(f"{verse.ref}: a pe break with no <br> after it")
        if el.kind == "br":
            if "pe" not in ends.get(el.start, []):
                raise ValueError(f"{verse.ref}: a <br> after no pe break")


def _read_csv_verses() -> tuple:
    """Every verse of csv/, in book order, and the folder's five header values."""
    verses = []
    headers = {}
    entities = collections.Counter()
    files = _book_files(FOLDER_CSV, ".csv")
    for bk39id, book in sef_cmn.SEF_BKNA.items():
        path = files[book]
        rows = _read_crlf_csv(path)
        header = rows[:5]
        if [row[0] for row in header] != list(HEADER_KEYS) or {
            len(r) for r in header
        } != {2}:
            raise ValueError(f"{path}: header {header}")
        if header[0][1] != book:
            raise ValueError(f"{path}: Index Title {header[0][1]!r}")
        for key, value in header[1:]:
            if headers.setdefault(key, value) != value:
                raise ValueError(f"{path}: {key} differs from another file's")
        for row in rows[5:]:
            if len(row) != 2:
                raise ValueError(f"{path}: row {row[:1]} has {len(row)} fields")
            ref, cell = row
            chapter, number = _parse_ref(ref, book, str(path))
            parser = _CellParser(ref)
            parser.feed(cell)
            parser.close()
            if parser._stack:
                raise ValueError(f"{ref}: unclosed <{parser._stack[-1].tag}>")
            entities.update(parser.entities)
            text = "".join(parser.text)
            bcvt = tbn.mk_bcvtsef(bk39id, chapter, number)
            verse = CsvVerse(
                book,
                bk39id,
                chapter,
                number,
                ref,
                tbn.is_poetcant(bcvt),
                cell,
                text,
                parser.elements,
                parser.top,
            )
            _check_code_points(text, _DISALLOWED_CSV_RE, ref)
            for el in parser.elements:
                _check_element(el, ref)
            verses.append(verse)
    return verses, headers, entities


def _read_ajf_rows() -> list:
    rows_out = []
    files = _book_files(FOLDER_AJF, ".csv")
    for bk39id, book in sef_cmn.SEF_BKNA.items():
        path = files[book]
        for row in _read_crlf_csv(path):
            if len(row) != 4:
                raise ValueError(f"{path}: row {row[:1]} has {len(row)} fields")
            ref, combined, alef, bet = row
            chapter, number = _parse_ref(ref, book, str(path))
            for field in (combined, alef, bet):
                _check_code_points(field, _DISALLOWED_AJF_RE, ref)
            if bool(alef) != bool(bet):
                raise ValueError(f"{ref}: one strand without the other")
            bcvt = tbn.mk_bcvtbhs(bk39id, chapter, number)
            rows_out.append(
                AjfRow(
                    book,
                    bk39id,
                    chapter,
                    number,
                    ref,
                    tbn.is_poetcant(bcvt),
                    combined,
                    alef,
                    bet,
                )
            )
    return rows_out


# THE LISTINGS ---------------------------------------------------------------------------------


def _split_runs(text: str) -> list:
    """``text`` cut at SPACE and NO-BREAK SPACE, each separator a run of its own."""
    runs = [text]
    for sep in (" ", sd.NBSP):
        out = []
        for run in runs:
            pieces = run.split(sep)
            for piece in pieces[:-1]:
                if piece:
                    out.append(piece)
                out.append(sep)
            if pieces[-1]:
                out.append(pieces[-1])
        runs = out
    return runs


# uni_heb.shunna, remembered: the listings have some five million code points and fewer
# than a hundred distinct ones.
_shunna = functools.cache(uni_heb.shunna)


def listing_entries(kids: list, indent: str = "") -> list:
    """The lines ``py/mb_misc/write_utils.py`` writes for a verse's children.

    Each entry is a line and the run of text it lists, or None for a line that lists no run.
    A run's line is ``uni_heb.join_shunnas`` of the run, spelled out with ``_shunna``.
    """
    entries = []
    for kid in kids:
        if isinstance(kid, str):
            entries.extend(
                (indent + ",".join(map(_shunna, run)), run) for run in _split_runs(kid)
            )
            continue
        head = kid.tag if kid.cls is None else f"{kid.tag} class={kid.cls}"
        if kid.kids:
            entries.append((f"{indent}START {head}", None))
            entries.extend(listing_entries(kid.kids, indent))
            entries.append((f"{indent}STOP {head}", None))
        else:
            entries.append((f"{indent}START/STOP {head}", None))
    return entries


def _listing_lines(kids: list, indent: str = "") -> list:
    return [line for line, _run in listing_entries(kids, indent)]


def short_name_in_listings(char: str) -> str:
    """The name a listing gives a code point: ``uni_heb.shunna``."""
    return _shunna(char)


def _read_listing(path, book: str) -> list:
    raw = path.read_bytes()
    if b"\r" in raw or raw.startswith(codecs.BOM_UTF8):
        raise ValueError(f"{path}: a CR or a byte-order mark")
    lines = raw.decode("utf-8").split("\n")
    if lines[0] != f"unicode_names {book}" or lines[-1] != "":
        raise ValueError(f"{path}: first or last line")
    verses = []
    current = None
    for line in lines[1:-1]:
        if line == "":
            current = None
        elif current is None:
            current = [line, []]
            verses.append(current)
        else:
            current[1].append(line)
    return verses


def listing_verse(folder: str, book: str, head: str) -> list:
    """The lines a listing has for the verse whose line is ``head``, that line first."""
    path = _book_files(folder, ".txt")[book]
    hits = [[line, *lines] for line, lines in _read_listing(path, book) if line == head]
    if len(hits) != 1:
        raise ValueError(f"{path}: {len(hits)} verses {head!r}")
    return hits[0]


def _match_listing(want: list, got: list, where: str) -> bool:
    """Whether ``got`` is ``want``, or ``want`` plus the trailing SPACE lines it lost."""
    if got == want:
        return False
    tail = got[len(want) :]
    if got[: len(want)] == want and tail and all(t.strip() == "SPACE" for t in tail):
        return True
    raise ValueError(f"{where}: the listing differs from its CSV row")


def _check_listings(verses: list, ajf_rows: list) -> dict:
    out = collections.Counter()
    by_book = collections.defaultdict(list)
    for verse in verses:
        by_book[verse.book].append(verse)
    for book, path in _book_files(FOLDER_NAMES, ".txt").items():
        listed = _read_listing(path, book)
        if len(listed) != len(by_book[book]):
            raise ValueError(f"{path}: {len(listed)} verses")
        for (head, lines), verse in zip(listed, by_book[book]):
            want_head = (
                f"{verse.bk39id} {verse.chapter}:{verse.verse} in vtrad {tbn.VT_SEF}"
            )
            if head != want_head:
                raise ValueError(f"{path}: {head!r} for {verse.ref}")
            stripped = _match_listing(_listing_lines(verse.top), lines, verse.ref)
            out["csv stripped"] += stripped
            out["csv verses"] += 1
            out["csv lines"] += len(lines)
    ajf_by_book = collections.defaultdict(list)
    for row in ajf_rows:
        ajf_by_book[row.book].append(row)
    for book, path in _book_files(FOLDER_NAMES_AJF, ".txt").items():
        listed = _read_listing(path, book)
        if len(listed) != len(ajf_by_book[book]):
            raise ValueError(f"{path}: {len(listed)} verses")
        for (head, lines), row in zip(listed, ajf_by_book[book]):
            want_head = f"{row.bk39id} {row.chapter}:{row.verse} in vtrad {tbn.VT_BHS}"
            if head != want_head:
                raise ValueError(f"{path}: {head!r} for {row.ref}")
            if row.alef:
                want = []
                for strand, field in zip(
                    AJF_STRANDS, (row.combined, row.alef, row.bet)
                ):
                    want.append(strand)
                    want.extend(_listing_lines([field], "    "))
            else:
                want = _listing_lines([row.combined] if row.combined else [])
            stripped = _match_listing(want, lines, row.ref)
            # The AJF page says why: each such row's last field, its cant-bet strand, ends
            # with a samekh break, whose space the CSV writer stripped.
            if stripped and not (row.alef and row.bet.endswith("{ס}")):
                raise ValueError(
                    f"{row.ref}: a listing longer than its row, unexplained"
                )
            out["ajf stripped"] += stripped
            out["ajf verses"] += 1
            out["ajf lines"] += len(lines)
    return out


# THE SURVEY -----------------------------------------------------------------------------------


@dataclasses.dataclass
class Survey:
    verses: list
    ajf_rows: list
    headers: dict
    entities: collections.Counter
    element_counts: collections.Counter
    spacing: collections.Counter
    listings: collections.Counter
    code_points_csv: collections.Counter
    code_points_ajf: collections.Counter
    by_system: collections.Counter
    kq_shapes: collections.Counter
    kq_qere_first_after_maqaf: int
    velo: dict
    cgj: dict
    zarqa: collections.Counter
    geresh_telisha: list
    atoms: collections.Counter
    em_dash_csv: list
    em_dash_ajf: list
    dual_cant_refs: list
    refs_only_csv: list
    refs_only_ajf: list
    silluq_cases: list
    ajf_text: collections.Counter

    @functools.cached_property
    def _verse_by_ref(self) -> dict:
        return {v.ref: v for v in self.verses}

    @functools.cached_property
    def _ajf_row_by_ref(self) -> dict:
        return {r.ref: r for r in self.ajf_rows}

    def verse(self, ref: str) -> CsvVerse:
        """The verse of csv/ at a reference the files have."""
        return self._verse_by_ref[ref]

    def ajf_row(self, ref: str) -> AjfRow:
        """The row of csv-ajf/ at a reference the files have."""
        return self._ajf_row_by_ref[ref]


def _kq_shape(el: Element, verse: CsvVerse) -> tuple:
    first, sep, _second = el.kids
    order = "ketiv first" if first.kind == "ketiv" else "qere first"
    ketiv, qere = sorted((el.kids[0], el.kids[2]), key=lambda k: k.kind)
    words_k = len(ketiv.text()[1:-1].split(" "))
    words_q = len(qere.text()[1:-1].split(" "))
    separator = "space" if sep == " " else "maqaf"
    return order, separator, words_k, words_q


def _cgj_kind(cluster: str, letters: str, index: int, where: str) -> tuple:
    """The kind of a letter that has a COMBINING GRAPHEME JOINER, and the parts around it."""
    marks = marks_of(cluster)
    if marks.count(sd.CGJ) != 1:
        raise ValueError(f"{where}: {marks.count(sd.CGJ)} CGJ on one letter")
    before, after = marks.split(sd.CGJ)
    vowels_before = [m for m in before if m in VOWELS]
    accents_before = [m for m in before if m in _ACCENTS or m == hpo.MTGOSLQ]
    lamed = cluster[0] == "\N{HEBREW LETTER LAMED}"
    if (
        lamed
        and after == "\N{HEBREW POINT HIRIQ}"
        and letters.endswith("ירושלם")
        and index == len(letters) - 2
        and before[:1] in ("\N{HEBREW POINT PATAH}", "\N{HEBREW POINT QAMATS}")
        and len(before) <= 2
        and all(m in _ACCENTS or m == hpo.MTGOSLQ for m in before[1:])
    ):
        return "jerusalem-hiriq", before, after
    if (
        lamed
        and after == "\N{HEBREW POINT SHEVA}"
        and letters.endswith("ירושלמה")
        and index == len(letters) - 3
        and before[:1] in ("\N{HEBREW POINT PATAH}", "\N{HEBREW POINT QAMATS}")
        and len(before) == 2
        and before[1] in _ACCENTS
    ):
        return "jerusalem-sheva", before, after
    if (
        vowels_before == ["\N{HEBREW POINT QAMATS}"]
        and len(accents_before) == 1
        and (
            accents_before[0] in ha.UNI_UNDER_ACCENTS
            or accents_before[0] == hpo.MTGOSLQ
        )
        and len(after) == 2
        and after[0] == "\N{HEBREW POINT PATAH}"
        and after[1] in ha.UNI_OVER_ACCENTS
    ):
        return "qupo", before, after
    if (
        len(vowels_before) == 1
        and len(accents_before) == 1
        and accents_before[0] in ha.UNI_UNDER_ACCENTS
        and after == hpo.MTGOSLQ
    ):
        return "accent-meteg", before, after
    raise ValueError(f"{where}: unrecognized CGJ context {cluster!r}")


def _survey_cgj(verses: list, ajf_rows: list) -> dict:
    found = collections.defaultdict(list)
    for verse in verses:
        for atom in ATOM_RE.findall(verse.scripture()):
            if sd.CGJ not in atom:
                continue
            letters = letters_of(atom)
            for index, cluster in enumerate(CLUSTER_RE.findall(atom)):
                if sd.CGJ in cluster:
                    kind, before, after = _cgj_kind(cluster, letters, index, verse.ref)
                    found[kind].append(
                        {
                            "ref": verse.ref,
                            "book": verse.book,
                            "atom": atom,
                            "cluster": cluster,
                            "before": before,
                            "after": after,
                        }
                    )
    csv_atoms = collections.Counter(
        hit["atom"] for hits in found.values() for hit in hits
    )
    ajf_atoms = collections.Counter(
        atom
        for row in ajf_rows
        for atom in ATOM_RE.findall(row.combined)
        if sd.CGJ in atom
    )
    if csv_atoms != ajf_atoms:
        raise ValueError(
            "csv/ and the combined field of csv-ajf/ differ in their CGJ atoms"
        )
    if any(sd.CGJ in row.alef + row.bet for row in ajf_rows):
        raise ValueError("a cant-alef or cant-bet field of csv-ajf/ has a CGJ")
    for kind in ("qupo", "accent-meteg"):
        for hit in found[kind]:
            hit["strands"] = _strand_atoms(hit, ajf_rows)
    for hits in found.values():
        for hit in hits:
            joined = hit["cluster"].replace(sd.CGJ, "")
            hit["normalized"] = unicodedata.normalize("NFC", joined)
            if hit["normalized"] == joined:
                raise ValueError(
                    f"{hit['ref']}: a CGJ where normalization reorders nothing"
                )
    return dict(found)


def _strand_atoms(hit: dict, ajf_rows: list) -> dict:
    """The cant-alef and cant-bet atoms of csv-ajf/ at a combined CGJ atom of csv/."""
    rows = [
        row
        for row in ajf_rows
        if row.book == hit["book"] and row.alef and hit["atom"] in row.combined
    ]
    if len(rows) != 1:
        raise ValueError(
            f"{hit['ref']}: {len(rows)} csv-ajf/ rows have {hit['atom']!r}"
        )
    row = rows[0]
    atoms = {
        "combined": ATOM_RE.findall(row.combined),
        "alef": ATOM_RE.findall(row.alef),
        "bet": ATOM_RE.findall(row.bet),
    }
    lengths = {len(v) for v in atoms.values()}
    if len(lengths) != 1:
        raise ValueError(f"{row.ref}: the strands have different numbers of atoms")
    positions = [i for i, a in enumerate(atoms["combined"]) if a == hit["atom"]]
    if len(positions) != 1:
        raise ValueError(f"{row.ref}: {len(positions)} places have {hit['atom']!r}")
    position = positions[0]
    out = {"ref": row.ref}
    letters = letters_of(hit["atom"])
    cgj_index = next(
        i for i, c in enumerate(CLUSTER_RE.findall(hit["atom"])) if sd.CGJ in c
    )
    for strand in ("alef", "bet"):
        atom = atoms[strand][position]
        if letters_of(atom) != letters:
            raise ValueError(f"{row.ref}: the {strand} atom has other letters")
        out[strand] = atom
        out[f"{strand} marks"] = marks_of(CLUSTER_RE.findall(atom)[cgj_index])
    pairs = (("alef", "bet"), ("bet", "alef"))
    sides = [
        (x, y)
        for x, y in pairs
        if out[f"{x} marks"] == hit["before"]
        and _is_subsequence(hit["after"], out[f"{y} marks"])
    ]
    if len(sides) != 1:
        raise ValueError(
            f"{row.ref}: the CGJ letter of {hit['atom']!r} is not two strands'"
        )
    out["before strand"], out["after strand"] = sides[0]
    return out


def _is_subsequence(part: str, whole: str) -> bool:
    chars = iter(whole)
    return all(c in chars for c in part)


def _silluq_cases(verses: list, ajf_rows: list) -> list:
    """MAM-simple's silluq-before-meteg annotations, with csv/'s and csv-ajf/'s atoms."""
    root = paths.repo_root()
    names = _tracked("MAM-simple/json-vtrad-mam/*.json")
    if not names:
        raise ValueError("no tracked MAM-simple/json-vtrad-mam/ JSON")
    cases = []
    for name in names:
        group = mam_simple_json.read_book_group(root / name)
        for verse_node in mam_simple_json.verses(group):
            for node in _nodes(verse_node):
                if node["type"] == "silluq-before-meteg":
                    cases.append((verse_node["osisID"], node))
    out = []
    for osis_id, node in cases:
        if set(node) != {"type", "text", "letters-with-silluq"}:
            raise ValueError(f"{osis_id}: silluq-before-meteg node {sorted(node)}")
        bk39id, chapter, number = osis_book_abbrevs.get_bcv_from_osis_id(osis_id)
        ref = f"{sef_cmn.SEF_BKNA[bk39id]} {chapter}:{number}"
        full = node["text"]
        marked = node["letters-with-silluq"]
        silluq_index = marked.index(hpo.MTGOSLQ) - 1
        letters = letters_of(full)
        sefaria = _one_atom(
            [v.scripture() for v in verses if v.ref == ref], letters, ref
        )
        ajf = _one_atom([r.combined for r in ajf_rows if r.ref == ref], letters, ref)
        if ajf != sefaria:
            raise ValueError(f"{ref}: csv/ and csv-ajf/ differ at {letters}")
        if sefaria != _drop_metegs_after(full, silluq_index):
            raise ValueError(
                f"{ref}: csv/ has {sefaria!r}, not {full!r} less its meteg"
            )
        out.append(
            {
                "osis_id": osis_id,
                "ref": ref,
                "full": full,
                "sefaria": sefaria,
                "silluq_index": silluq_index,
            }
        )
    if not out:
        raise ValueError("MAM-simple has no silluq-before-meteg annotation")
    return out


def _nodes(node):
    """Every node under a MAM-simple verse, with closed dispatch on the Sefaria handlers."""
    key = (node["type"], node.get("class"))
    if key not in _SEF_HANDLER_KEYS:
        raise ValueError(f"MAM-simple node {key} has no Sefaria handler")
    yield node
    for child in mam_simple_json.children(node):
        yield from _nodes(child)


def _one_atom(texts: list, letters: str, ref: str) -> str:
    hits = [a for t in texts for a in ATOM_RE.findall(t) if letters_of(a) == letters]
    if len(hits) != 1:
        raise ValueError(f"{ref}: {len(hits)} atoms have the letters {letters}")
    return hits[0]


def _drop_metegs_after(atom: str, silluq_index: int) -> str:
    """``atom`` less each METEG on a letter after the one at ``silluq_index``."""
    out = []
    letter_index = -1
    for char in atom:
        if char in LETTERS:
            letter_index += 1
        if char != hpo.MTGOSLQ or letter_index <= silluq_index:
            out.append(char)
    return "".join(out)


def _survey_ajf_text(
    ajf_rows: list, element_counts: collections.Counter
) -> collections.Counter:
    """csv-ajf/'s spellings of what csv/ marks up, each checked against csv/'s count."""
    out = collections.Counter()
    for row in ajf_rows:
        for field_name, field in (
            ("combined", row.combined),
            ("alef", row.alef),
            ("bet", row.bet),
        ):
            for match in re.finditer(f"{hpu.PASOLEG}+", field):
                a, b = match.span()
                after = field[b : b + 1]
                if b - a == 1 and after in (" ", "]"):
                    out[f"{field_name} legarmeh"] += 1
                elif b - a == 2 and after and not after.isspace():
                    if field[a - 1 : a].isspace():
                        raise ValueError(f"{row.ref}: a paseq after a space")
                    out[f"{field_name} paseq"] += 1
                else:
                    raise ValueError(f"{row.ref}: {b - a} PASEQ in {field!r}")
            for letter, name in (("ס", "samekh"), ("פ", "pe")):
                brace = re.escape("{" + letter + "}")
                for match in re.finditer(f"(.?){brace}(.?)", field):
                    before, after = match.group(1), match.group(2)
                    end = match.end() == len(field)
                    if before != " " or (after != " " and not end):
                        raise ValueError(f"{row.ref}: {name} break in {field!r}")
                    out[f"{field_name} {name}"] += 1
            out[f"{field_name} pairs"] += len(
                re.findall(r"\([^()\[\]]*\)[ ־]\[[^()\[\]]*\]", field)
            )
            out[f"{field_name} nun hafukha"] += field.count(hpu.NUN_HAF)
    for kind, csv_kind in (
        ("legarmeh", "legarmeh"),
        ("paseq", "small paseq"),
        ("samekh", "samekh"),
        ("pe", "pe"),
        ("pairs", "kq"),
        ("nun hafukha", "invnun"),
    ):
        if out[f"combined {kind}"] != element_counts[csv_kind]:
            raise ValueError(
                f"csv-ajf/ has {out[f'combined {kind}']} {kind}, csv/ {element_counts[csv_kind]}"
            )
    return out


def check_handlers() -> dict:
    """What the Sefaria exporter writes for each MAM-simple node it leaves out, pinned.

    The Sefaria page's "What the files leave out" section rests on these, and the AJF page's
    strands and table of spellings on the AJF exporter's handlers below.  Each is checked by
    calling the handler, so a handler changed to write something fails here.
    """
    handlers = mam4sef_handlers.HANDLERS
    probe = ["x"]
    left_out = {}
    for key in (
        ("sdt-note", None),
        ("good-ending", None),
        ("cant-alef", None),
        ("cant-bet", None),
    ):
        left_out[key[0]] = handlers[key]({"type": key[0]}, probe, [])
        if left_out[key[0]] != []:
            raise ValueError(f"the Sefaria handler for {key} writes {left_out[key[0]]}")
    if handlers[("cant-combined", None)]({"type": "cant-combined"}, probe, []) != probe:
        raise ValueError("the Sefaria handler for cant-combined does not pass its text")
    target, note = ["target"], ["note"]
    kept = handlers[("scrdfftar", None)](
        {"type": "scrdfftar"}, target + note, [({}, target), ({}, note)]
    )
    if kept != target:
        raise ValueError("the Sefaria handler for scrdfftar keeps more than its target")
    strand_keys = (("cant-combined", None), ("cant-alef", None), ("cant-bet", None))
    for strand, key in zip(AJF_STRANDS, strand_keys):
        table = mam4ajf_handlers.HANDLERS[strand]
        if table[key]({"type": key[0]}, probe, []) != probe:
            raise ValueError(
                f"the AJF {strand} handler for {key} does not pass its text"
            )
    # What csv-ajf/ has where csv/ has markup that the files' text cannot show, each as the
    # AJF page's table of spellings states it.
    ajf = mam4ajf_handlers.HANDLERS["rv-cant-combined"]
    plain = {
        ("shirah-space", None): [" "],
        ("implicit-maqaf", None): [hpu.MAQ],
        ("kq-k-velo-q-maq", None): [hpu.MAQ],
        ("kq-trivial", None): probe,
        ("letter-small", None): probe,
        ("letter-large", None): probe,
        ("letter-hung", None): probe,
    }
    for key, want in plain.items():
        if ajf[key]({"type": key[0]}, probe, []) != want:
            raise ValueError(f"the AJF handler for {key} does not write {want}")
    return left_out


@functools.cache
def survey() -> Survey:
    verses, headers, entities = _read_csv_verses()
    ajf_rows = _read_ajf_rows()
    element_counts = collections.Counter()
    spacing = collections.Counter()
    kq_shapes = collections.Counter()
    qere_first_after_maqaf = 0
    velo = {"ketiv": [], "qere": [], "k-velo-q-maq": []}
    code_points_csv = collections.Counter()
    by_system = collections.Counter()
    zarqa = collections.Counter()
    geresh_telisha = []
    atoms = collections.Counter()
    for verse in verses:
        system = "poetic" if verse.poetic else "prose"
        last_text = len(verse.text.rstrip(sd.NBSP))
        for el in verse.elements:
            if el.kind in ("samekh", "pe") and el.end < last_text:
                element_counts[f"{el.kind} inside a verse"] += 1
            element_counts[el.kind] += 1
            if el.kind == "small":
                small_kind = "paseq" if el.kids == [hpu.PASOLEG] else "letter"
                element_counts[f"small {small_kind}"] += 1
            if el.kind == "kq":
                shape = _kq_shape(el, verse)
                kq_shapes[shape] += 1
                if (
                    shape[0] == "qere first"
                    and verse.text[el.start - 1 : el.start] == hpu.MAQ
                ):
                    qere_first_after_maqaf += 1
            if el.kind in ("ketiv", "qere") and el.parent_kind is None:
                velo[el.kind].append((verse.ref, el.text()))
            if el.kind == "k-velo-q-maq":
                velo["k-velo-q-maq"].append(verse.ref)
        _check_spacing(verse, spacing)
        verse_code_points = collections.Counter(verse.text)
        code_points_csv.update(verse_code_points)
        for char, count in verse_code_points.items():
            by_system[(char, system)] += count
        for atom in ATOM_RE.findall(verse.scripture()):
            atoms["atoms"] += 1
            if unicodedata.normalize("NFC", atom) != atom:
                atoms["changed by NFC"] += 1
            for mark in OWN_CODE_POINT_MARKS:
                if mark in atom:
                    atoms[f"with {unicode_data.name(mark)}"] += 1
            clusters = CLUSTER_RE.findall(atom)
            for index, cluster in enumerate(clusters):
                last = index == len(clusters) - 1
                vowels = [m for m in cluster if m in VOWELS]
                if len(vowels) > 1:
                    between = cluster[
                        cluster.index(vowels[0]) : cluster.rindex(vowels[-1])
                    ]
                    if len(vowels) != 2 or sd.CGJ not in between:
                        raise ValueError(
                            f"{verse.ref}: two vowels with no CGJ in {atom!r}"
                        )
                    atoms["letters with two vowels"] += 1
                if ha.Z_OR_TSOR in cluster:
                    if not last:
                        raise ValueError(
                            f"{verse.ref}: a ZINOR before an atom's last letter"
                        )
                    zarqa[f"z-or-tsor {system}"] += 1
                    if cluster[0] == "\N{HEBREW LETTER LAMED}":
                        zarqa[f"z-or-tsor {system} lamed"] += 1
                if ha.ZSH_OR_TSIT in cluster:
                    zarqa[f"zsh-or-tsit {system}"] += 1
                    if system == "prose":
                        later = "".join(clusters[index + 1 :])
                        if ha.Z_OR_TSOR not in later or ha.Z_OR_TSOR in cluster:
                            raise ValueError(
                                f"{verse.ref}: a prose ZARQA with no later ZINOR"
                            )
                if ha.TEL_G in cluster and (ha.GER in cluster or ha.GER_2 in cluster):
                    marks = marks_of(cluster)
                    if marks.index(ha.TEL_G) < max(
                        marks.find(ha.GER), marks.find(ha.GER_2)
                    ):
                        raise ValueError(
                            f"{verse.ref}: TELISHA GEDOLA before its geresh"
                        )
                    geresh_telisha.append(
                        {"ref": verse.ref, "atom": atom, "cluster": cluster}
                    )
    by_atom = {}
    for hit in geresh_telisha:
        by_atom.setdefault((hit["ref"], hit["atom"]), []).append(hit["cluster"])
    geresh_telisha = [
        {"ref": ref, "atom": atom, "clusters": clusters}
        for (ref, atom), clusters in by_atom.items()
    ]
    code_points_ajf = collections.Counter()
    for row in ajf_rows:
        code_points_ajf.update(row.combined + row.alef + row.bet)
        for cluster in CLUSTER_RE.findall(
            row.combined + " " + row.alef + " " + row.bet
        ):
            vowels = [m for m in cluster if m in VOWELS]
            if len(vowels) > 1 and sd.CGJ not in cluster:
                raise ValueError(f"{row.ref}: two vowels with no CGJ in {cluster!r}")
    em_dash_csv = [v.ref for v in verses if EM_DASH in v.text]
    em_dash_ajf = [r.ref for r in ajf_rows if EM_DASH in r.combined + r.alef + r.bet]
    for verse in verses:
        if EM_DASH in verse.text and verse.text != EM_DASH:
            raise ValueError(f"{verse.ref}: an EM DASH beside other text")
    for row in ajf_rows:
        if EM_DASH in row.combined and (row.combined != EM_DASH or row.alef):
            raise ValueError(f"{row.ref}: an EM DASH beside other text")
    csv_refs = [v.ref for v in verses]
    ajf_refs = [r.ref for r in ajf_rows]
    csv_ref_set, ajf_ref_set = set(csv_refs), set(ajf_refs)
    if len(csv_ref_set) != len(csv_refs) or len(ajf_ref_set) != len(ajf_refs):
        raise ValueError("a reference repeated within one folder")
    out = Survey(
        verses=verses,
        ajf_rows=ajf_rows,
        headers=headers,
        entities=entities,
        element_counts=element_counts,
        spacing=spacing,
        listings=_check_listings(verses, ajf_rows),
        code_points_csv=code_points_csv,
        code_points_ajf=code_points_ajf,
        by_system=by_system,
        kq_shapes=kq_shapes,
        kq_qere_first_after_maqaf=qere_first_after_maqaf,
        velo=velo,
        cgj=_survey_cgj(verses, ajf_rows),
        zarqa=zarqa,
        geresh_telisha=geresh_telisha,
        atoms=atoms,
        em_dash_csv=em_dash_csv,
        em_dash_ajf=em_dash_ajf,
        dual_cant_refs=[r.ref for r in ajf_rows if r.alef],
        refs_only_csv=[ref for ref in csv_refs if ref not in ajf_ref_set],
        refs_only_ajf=[ref for ref in ajf_refs if ref not in csv_ref_set],
        silluq_cases=_silluq_cases(verses, ajf_rows),
        ajf_text=_survey_ajf_text(ajf_rows, element_counts),
    )
    shunnas = collections.defaultdict(set)
    for char in out.code_points_csv | out.code_points_ajf:
        shunnas[_shunna(char)].add(char)
    if any(len(chars) > 1 for chars in shunnas.values()):
        raise ValueError("two code points share a short name in the listings")
    return out
