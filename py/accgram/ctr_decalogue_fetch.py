r"""Author tool: vendor CTR's two Decalogues from chabad.org (issue wlc-utils#73).

CTR is the "Complete Tanach with Rashi", the Chabad.org web edition of the Hebrew Bible
(``https://www.chabad.org/library/bible_cdo/aid/<aid>``).  Unlike the eight paper
Decalogues of wlc-utils#69 -- each a HAND TRANSCRIPTION, primary observation read off a printed
page -- CTR is DIGITAL: its accents are already Unicode, so it is fetched and diffed
rather than read and typed.  It is therefore a VENDORED STRAND, not a transcription; this
tool is the network author-tool that refreshes the vendored snapshot, exactly as
``printed_decalogue_fetch.py`` does for the eight idealized Wikisource strands.

CHAPTERS.  Only the two running-text Decalogues exist on the web -- Exodus 20 and
Deuteronomy 5 -- so this fetches those two chapters and keeps the Decalogue span of each
(Exodus 20:2-14, Deuteronomy 5:6-18, the אנכי…תחמד commandments).  What each strand turns
out to FOLLOW is not assumed here (the fetch is tradition-agnostic); see
``ctr_decalogue.py`` for the comparison, which finds Exodus is the ta'am *elyon* and
Deuteronomy the *taxton*.

WHAT IS KEPT vs CLEANED.  The verse text is stored accent-exact, with CTR's own encoding
left intact -- its colon for sof pasuq, its vertical bar for a pasoleg, its lookalike-pair
codepoints (qadma for pashta, yetiv-order for mahapakh; see MAM-basics' review of CTR and
``ctr_decalogue.py``).  Only rendering cruft that is not part of the pointed text is
removed at extraction: inline HTML tags, the parenthetical *ketiv* note beside a qere (the
accented qere itself is kept), non-breaking spaces, and the bare ס/פ setuma/petuha
markers Chabad shows between verses.  Normalizing CTR's encoding is the comparison's job,
not the vendoring's, so the snapshot stays faithful to what the page serves.

This is a network tool run by hand.  The committed JSON records the source URLs, the aids,
and the retrieval date for provenance.  Run from the repo root:

    PYTHONUTF8=1 .venv/Scripts/python.exe py/main_accgram.py vendor-ctr-decalogue

``--cache <dir>`` reads pre-fetched ``ctr_cache_<name>.html`` from a directory instead of
the network, so the exact snapshot already retrieved can be re-vendored without hitting the
server again; the provenance is unchanged either way.
"""

from __future__ import annotations

import argparse
import datetime
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

from mb_cmn import file_io

import wlc_paths

# A browser User-Agent: chabad.org 403s a bare tool UA.
_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
_HEADERS = {
    "User-Agent": _USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,he;q=0.8",
    "Referer": "https://www.chabad.org/library/bible_cdo/aid/63255/",
}
_URL = "https://www.chabad.org/library/bible_cdo/aid/{aid}/jewish/Chapter.htm"

NBSP = "\N{NO-BREAK SPACE}"
_SECTION_MARKS = {
    "\N{HEBREW LETTER SAMEKH}",  # setuma
    "\N{HEBREW LETTER PE}",  # petuha
    "\N{HEBREW LETTER FINAL PE}",
}

# (book, aid, chapter, first Decalogue verse, last Decalogue verse).  The span is the ten
# commandments only -- אנכי (Exodus 20:2 / Deuteronomy 5:6) through the last תחמד -- the same
# span the eight strands cover.
_CHAPTERS: tuple[tuple[str, int, int, int, int], ...] = (
    ("ex", 9881, 20, 2, 14),
    ("dt", 9969, 5, 6, 18),
)

_HEBREW_VERSE = re.compile(
    r'class="hebrew"><a id="v(\d+)" class="co_VerseNum"[^>]*>[^<]*</a>'
    r'<span class="co_VerseText">(.*?)</span></td>',
    re.S,
)
# The parenthetical ketiv note Chabad shows beside a qere, e.g. ``(כתיב מצותו)``; the
# accented qere it annotates sits in the sibling <co:instructional> and is kept.
_KETIV_NOTE = re.compile(r'<span class="instructional[^"]*">.*?</span>', re.S)
_ANY_TAG = re.compile(r"<[^>]+>")


def default_out_path() -> Path:
    return wlc_paths.in_dir() / "accgram" / "ctr_decalogue.json"


def _fetch(url: str, tries: int = 4) -> str:
    last: Exception | None = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers=_HEADERS)
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 -- report and back off
            last = exc
            wait = 5 * (attempt + 1)
            print(f"  attempt {attempt + 1} failed ({exc}); waiting {wait}s")
            time.sleep(wait)
    assert last is not None
    raise last


def _chapter_html(book: str, aid: int, cache: Path | None) -> str:
    if cache is not None:
        name = {"ex": "Exodus20", "dt": "Deut5"}[book]
        return (cache / f"ctr_cache_{name}.html").read_text(encoding="utf-8")
    return _fetch(_URL.format(aid=aid))


def clean_verse(raw: str) -> str:
    """One raw ``co_VerseText`` cell -> accent-exact pointed text, rendering cruft removed.

    Kept verbatim: every point and accent, CTR's colon (sof pasuq) and vertical bar
    (pasoleg), and any ZWJ.  Removed: the parenthetical ketiv note (the qere it annotates
    stays), all inline HTML tags, non-breaking spaces, and the bare ס/פ section markers.
    """
    text = _KETIV_NOTE.sub("", raw)
    text = _ANY_TAG.sub("", text)
    text = unescape(text).replace(NBSP, " ")
    kept = [tok for tok in text.split() if tok not in _SECTION_MARKS]
    return " ".join(kept)


def extract_decalogue(html: str, chapter: int, lo: int, hi: int) -> dict[str, str]:
    """The ``"<chapter>:<verse>" -> cleaned Hebrew`` map for one chapter's Decalogue span."""
    cells = {int(v): raw for v, raw in _HEBREW_VERSE.findall(html)}
    out: dict[str, str] = {}
    for verse in range(lo, hi + 1):
        if verse not in cells:
            raise ValueError(
                f"chapter {chapter}: verse {verse} not found in fetched HTML"
            )
        out[f"{chapter}:{verse}"] = clean_verse(cells[verse])
    return out


def build_payload(cache: Path | None, retrieved: str) -> dict[str, object]:
    chapters: dict[str, object] = {}
    for book, aid, chapter, lo, hi in _CHAPTERS:
        html = _chapter_html(book, aid, cache)
        chapters[book] = {
            "aid": aid,
            "chapter": chapter,
            "url": _URL.format(aid=aid),
            "decalogue_verses": extract_decalogue(html, chapter, lo, hi),
        }
    provenance = {
        "source": "CTR",
        "edition": "Complete Tanach with Rashi, chabad.org (The Bible with Rashi)",
        "provenance": "(speculative) a Judaica Press/Davka CD-ROM; see MAM-basics rocc_1",
        "retrieved": retrieved,
        "span": "the ten commandments: Exodus 20:2-14, Deuteronomy 5:6-18",
        "extraction_notes": (
            "Per-verse co_VerseText cells from the chapter pages. Kept accent-exact, "
            "including CTR's colon (sof pasuq), vertical bar (pasoleg) and lookalike-pair "
            "encoding (e.g. qadma for pashta, yetiv-order for mahapakh). Removed: inline "
            "HTML tags, the parenthetical ketiv note beside a qere (qere kept), non-breaking "
            "spaces, and bare setuma/petuha markers (ס/פ). Normalization is the comparison's "
            "job (ctr_decalogue.py), not the vendoring's."
        ),
    }
    return {"provenance": provenance, "chapters": chapters}


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the vendored snapshot's location comes from
    # ``default_out_path``, which asks ``wlc_paths`` itself.  The parameter is here so the
    # entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument("--out", type=Path, default=default_out_path())
    parser.add_argument(
        "--cache",
        type=Path,
        default=None,
        help="read ctr_cache_<name>.html from this dir instead of the network",
    )
    parser.add_argument(
        "--retrieved",
        default=datetime.date.today().isoformat(),
        help="retrieval date to record (default: today)",
    )


def run(args: argparse.Namespace) -> None:
    payload = build_payload(args.cache, args.retrieved)
    out_path: Path = args.out
    # file_io: temp-file write, PermissionError retry, and it makes the directory.
    # build_payload records the retrieval date itself, so no generator_file=.
    file_io.json_dump_to_file_path(payload, str(out_path))
    n = sum(len(c["decalogue_verses"]) for c in payload["chapters"].values())
    print(
        f"ctr-decalogue: {len(payload['chapters'])} chapters, {n} verses -> {out_path}"
    )
