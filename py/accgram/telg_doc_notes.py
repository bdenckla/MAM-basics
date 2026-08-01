"""Generate gh-pages/accgram/telg-doc-notes.html -- a deep-dive translation of
MAM's documentation (נוסח) notes on the five telisha-gedola + geresh/gershayim
words: Genesis 5:29, Zephaniah 2:15, 2 Kings 17:13, Leviticus 10:4, and
Ezekiel 48:10.

This is the companion "deep dive" for the telg + gerstar exhibit in
almost-errors.html: that page argues the checker's representation choice; this
page renders, into English, what MAM's own variant-notes say about each word.
It is the telg analogue of ps17v14-mam-doc-notes.html (the Psalms 17:14 notes).

Following MAM-with-doc's published sigil policy, manuscript sigils and technical
accent names are kept in Hebrew and explained (see the key) rather than replaced
with a Latin-letter system, and the implicit subject "MAM" is supplied where a
note opens with "=".  The verbatim Hebrew of each note is shown too, drawn
byte-exactly from MAM-with-doc via the ``telg_mam_doc_notes`` data module, so the
English rendering can be checked against the original.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import rtms_report
from accgram import telg_mam_doc_notes
from accgram.almost_errors_html_shared import hbo, link, ref_display, verse_links
from wlc_cmn.utf8_io import force_utf8_io
import wlc_provenance as provenance
from py_html import wlc_utils_html as H

import wlc_paths

REPORT_TITLE = "MAM documentation notes on the telg + geresh/gershayim words"

# The five words, in the order almost-errors.html presents them: three
# same-letter (gn, zp, 2k), then two cross-letter (lv, ek).
_REFS = ("gn5:29", "zp2:15", "2k17:13", "lv10:4", "ek48:10")


# --------------------------------------------------------------------------- #
# English renderings.  Sigils and accent names stay in Hebrew (see the key);
# pointed variant-forms are described in words and shown verbatim in the
# Hebrew blockquote under each note, so nothing here retypes combining marks.
# --------------------------------------------------------------------------- #
_EN: dict[str, dict[str, object]] = {
    "gn5:29": {
        "intro": (
            "MAM follows ",
            hbo("ל"),
            ", ",
            hbo("ל1"),
            ", ",
            hbo("ק3"),
            ", and the practice of Aleppo (",
            hbo("שיטת-א"),
            "): gershayim and telisha gedola together on the first letter,"
            " because the gershayim's accent is the one read first. So too in"
            " Dotan (",
            hbo("דותן"),
            "), in BHS, and in the WLC transcript (",
            hbo("המקליד"),
            ") since version 4.20 — all following the Leningrad" " manuscript (",
            hbo("כתי״ל"),
            "), whose reading Breuer also records;" " and so too in ",
            hbo("מג״ה"),
            " (Miqra’ot Gedolot Ha-keter), per the practice of the Keter. Jacob"
            " Sapir's note on the Aleppo Codex (",
            hbo("א(ס)"),
            ") records only that the word has “two accents” (",
            hbo("תרי טעמי"),
            "), which may register their presence without fixing their order.",
        ),
        "parts": [
            (
                "Manuscript ",
                hbo("ו"),
                " (",
                hbo("כתי״ו"),
                ", a sigil left undecoded here), the Yemenite manuscripts (",
                hbo("תיגאן"),
                "), the Sephardic manuscripts, the printed editions" " (",
                hbo("דפוסים"),
                "), and Koren (",
                hbo("קורן"),
                ") instead write the telisha gedola first and the gershayim"
                " second, because the proper place for the prepositive telisha"
                " gedola is at the very start of the first letter; so too the"
                " Breuer edition.",
            ),
            (
                "The WLC typed text (",
                hbo("הקלדה"),
                ") anomalously carries the telisha alone — as was even remarked"
                " in earlier versions — although the gershayim can in fact be"
                " seen in the Leningrad manuscript.",
            ),
        ],
    },
    "zp2:15": {
        "intro": (
            "MAM follows ",
            hbo("א"),
            " (Aleppo) and ",
            hbo("ל"),
            " (Leningrad): gershayim and telisha gedola on the first letter, as"
            " is MAM's custom (",
            hbo("כדרכו"),
            ").",
        ),
        "parts": [
            (
                "The printed editions and Koren put the telisha first and the"
                " gershayim second on the first letter, as does the Breuer"
                " edition — and here even ",
                hbo("מג״ה"),
                " does so, against the Keter, and against ",
                hbo("מג״ה"),
                "’s own practice at Genesis 5:29 and 2 Kings 17:13(!).",
            ),
        ],
    },
    "2k17:13": {
        "intro": (
            "MAM follows ",
            hbo("ל"),
            " and the practice of Aleppo (",
            hbo("שיטת-א"),
            "): a geresh and a telisha gedola at the head of the word in the"
            " Keter, per the Keter's practice — and compare Ezekiel 48:10 and"
            " Zephaniah 2:15 — and ",
            hbo("מג״ה"),
            " follows them.",
        ),
        "parts": [
            (
                "The Cairo Codex of the Prophets (",
                hbo("ק"),
                ") puts the telisha first and the geresh second; so too Koren,"
                " the printed editions, and the Breuer edition.",
            ),
            (
                "The WLC typed text (",
                hbo("הקלדה"),
                ") read telisha-then-geresh per the transcriber up to version"
                " 4.16, and geresh-then-telisha from version 4.18 — and per"
                " Breuer and Dotan, according to the context. There is also a"
                " masorah circle (",
                hbo("עיגול מסורה"),
                ") on this word; apparently Breuer and Dotan reported the second"
                " circle while the transcriber, in the earlier versions,"
                " reported the first.",
            ),
        ],
    },
    "lv10:4": {
        "intro": (
            "Sassoon 1053 (",
            hbo("ש1"),
            ") and the practice of Aleppo (",
            hbo("שיטת-א"),
            ") put both accents on the first letter — gershayim before telisha"
            " gedola; compare Ezekiel 48:10. Jacob Sapir's note on the Aleppo"
            " Codex (",
            hbo("א(ס)"),
            ") again records only “two accents” (",
            hbo("תרין טעמים"),
            ").",
        ),
        "parts": [
            (
                hbo("ל"),
                ", ",
                hbo("ל1"),
                ", ",
                hbo("ב"),
                " (Or. 4445), ",
                hbo("ש"),
                " (Sassoon 507), and manuscript ",
                hbo("ו"),
                "(?) put each accent on the letter proper to it — the telisha"
                " gedola at the head of the word and the gershayim on the"
                " stressed letter — and so do the printed editions, Koren, and"
                " the Breuer editions; even ",
                hbo("מג״ה"),
                " does so, against the practice of the Keter(!).",
            ),
            (
                "The Cairo 18 manuscript (",
                hbo("ק3"),
                ") anomalously swaps them, with the gershayim at the head and"
                " the telisha gedola on the stressed letter.",
            ),
        ],
    },
    "ek48:10": {
        "intro": (
            "Aleppo (",
            hbo("א"),
            ") reads both accents at the head of the word, as is its custom (",
            hbo("כדרכו"),
            ").",
        ),
        "parts": [
            (
                "The Cairo Codex of the Prophets (",
                hbo("ק"),
                ") puts the telisha gedola at the head and the geresh on a later"
                " letter; so too the printed editions, Koren, and the Breuer"
                " edition — and even ",
                hbo("מג״ה"),
                ", against the Keter(!). The WLC typed text does the same"
                " (probably following BHS), against the Leningrad manuscript (",
                hbo("כתי״ל"),
                ").",
            ),
            (
                hbo("ל"),
                " (Leningrad) carries a doubled geresh — one on the vav and one"
                " on the alef — where the first (at the head of the chanted word)"
                " marks that its reading takes precedence in sequence, and the second"
                " (on the stressed letter) marks the accent's actual place. This"
                " is the clearest statement in these notes of why a prepositive"
                " accent and its impositive partner can land on different letters"
                " of the same chanted word.",
            ),
        ],
    },
}

# Compact decoder for the sigils used above, in MAM-with-doc's "standalone
# passage" style: leave the sigil in Hebrew, gloss it in English.
_SOURCE_KEY = (
    ("א", "Aleppo Codex (the Keter)"),
    ("א(ס)", "Aleppo Codex per Jacob Sapir's notes (Me’orot Nathan)"),
    ("ל", "Leningrad Codex (cited in prose as כתי״ל)"),
    ("ל1", "Ms Leningrad Firkovich B17"),
    ("ק", "Cairo Codex of the Prophets"),
    ("ק3", "Cairo 18 manuscript (Torah)"),
    ("ש", "Ms Sassoon 507"),
    ("ש1", "Ms Sassoon 1053"),
    ("ב", "British Library Or 4445 (Torah)"),
    ("כתי״ו", "manuscript “vav” — a sigil left undecoded here"),
    ("שיטת-א", "the general practice of Aleppo (the Keter)"),
    ("תיגאן", "the Yemenite manuscripts (the Taj tradition)"),
    ("דותן", "Dotan's editions and writings"),
    ("ברויאר", "Breuer's editions and writings"),
    ("קורן", "the Koren edition"),
    ("דפוסים", "the (selected) printed editions"),
    ("מג״ה", "Miqra’ot Gedolot Ha-keter"),
    ("BHS", "Biblia Hebraica Stuttgartensia"),
    ("המקליד", "the transcriber of the Westminster/UXLC text of Leningrad"),
    ("הקלדה", "the typed WLC text itself"),
)

_TERM_KEY = (
    (
        "תלישא גדולה",
        "telisha gedola — a prepositive disjunctive, written at the head of its chanted word wherever it is chanted",
    ),
    (
        "גרש / גרשיים",
        "geresh / gershayim — impositive disjunctives, written on the stressed letter",
    ),
    (
        "עיגול מסורה",
        "a masorah circle: the circellus that flags a word as bearing a masoretic note",
    ),
    (
        "תרי טעמי / תרין טעמים",
        "“two accents” (Aramaic) — a masoretic note recording that the word bears two accents",
    ),
    ("כדרכו", "“as is its custom” — i.e. the codex's regular practice"),
)


def _intro_section() -> tuple[object, ...]:
    return (
        H.heading_level_1(REPORT_TITLE),
        H.para(
            (
                "An English rendering of MAM's documentation (",
                hbo("נוסח"),
                ", text-variant) notes on the five chanted words that carry both a"
                " telisha gedola (“telg”) and a geresh or gershayim (a"
                " “gerstar”). It is the deep-dive companion to the ",
                link("telg + gerstar exhibit", "almost-errors.html"),
                " on the “almost errors” page, which argues why the checker keeps"
                " both accents; here we simply translate what MAM's own notes say"
                " about each word. Source: ",
                link(
                    "MAM-with-doc",
                    "https://bdenckla.github.io/MAM-with-doc/",
                ),
                ".",
            )
        ),
        H.para(
            "The telisha gedola is prepositive — written at the very head of its"
            " chanted word no matter where that word is stressed — while the geresh or"
            " gershayim is impositive, written on the stressed letter. So when"
            " the stress is initial the two marks crowd onto the first letter"
            " (the same-letter words: Genesis 5:29, Zephaniah 2:15, 2 Kings"
            " 17:13), and when it is not they land on different letters of the"
            " one chanted word (the cross-letter words: Leviticus 10:4, Ezekiel 48:10)."
            " Most of what these notes argue is the relative order of the two"
            " marks on a shared letter — which one “comes first in the reading” —"
            " and which sources have which first. In 2 Kings 17:13 the leading"
            " mark is technically a geresh muqdam, which the checker reads as a"
            " geresh."
        ),
        H.para(
            (
                "Some reading conventions: a note opening with “=” means “MAM"
                " follows …”; elsewhere “X=Y” means source X has the reading Y. A bang"
                " attaches to that equals — “X!=Y” reads “X surprisingly equals"
                " Y”, flagging X’s reading as striking or unexpected (for"
                " instance a transcript or edition that departs from the codex it"
                " otherwise follows); a bang ending a clause is the same emphasis"
                " standing on its own. The lemma shown in each heading is the"
                " chanted word as it appears in MAM-with-doc — the precise reading MAM"
                " adopts is the one stated in the note. See the ",
                link("key", "#key"),
                " for the sigils and accent terms.",
            )
        ),
    )


def _key_section() -> tuple[object, ...]:
    def _term_node(term: str) -> object:
        return hbo(term) if any("֐" <= ch <= "׿" for ch in term) else term

    def _key_table(pairs: tuple[tuple[str, str], ...]) -> object:
        rows = [H.table_row_of_headers(("sigil", "meaning"))]
        for term, meaning in pairs:
            rows.append(
                H.table_row_of_data((_term_node(term), meaning), ({"dir": "rtl"}, None))
            )
        return H.table(tuple(rows), {"class": "limited-width"})

    return (
        H.heading_level_2("Key to the sigils", {"id": "key"}),
        H.heading_level_3("Manuscripts and editions"),
        _key_table(_SOURCE_KEY),
        H.heading_level_3("Accent terms and masoretic notation"),
        _key_table(_TERM_KEY),
    )


def _hebrew_blockquote(note: dict) -> object:
    """The verbatim Hebrew note, RTL, for checking the English against."""
    contents: list[object] = [H.para(note["intro"])]
    if note["parts"]:
        contents.append(H.unordered_list(tuple(note["parts"])))
    return H.blockquote(tuple(contents), {"dir": "rtl", "lang": "hbo"})


def _note_section(bcv: str, note_he: dict) -> tuple[object, ...]:
    english = _EN[bcv]
    items: list[object] = [
        H.heading_level_2((ref_display(bcv), " — ", hbo(note_he["lemma"]))),
        verse_links(bcv),
        H.para(english["intro"]),
    ]
    if english["parts"]:
        items.append(H.unordered_list(tuple(english["parts"])))
    items.append(H.para(H.small("MAM’s note, verbatim:")))
    items.append(_hebrew_blockquote(note_he))
    return tuple(items)


def _load_notes() -> dict:
    return telg_mam_doc_notes.NOTES


def render_body_contents() -> tuple[object, ...]:
    notes = _load_notes()
    sections: list[object] = [*_intro_section(), *_key_section()]
    for bcv in _REFS:
        sections.extend(_note_section(bcv, notes[bcv]))
    wrapper = H.div(tuple(sections), {"class": "goerwitz-tms-width-limited"})
    return (wrapper,)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def default_html_out_path(repo_root: Path) -> Path:
    return wlc_paths.gh_pages_dir() / "accgram" / "telg-doc-notes.html"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--html-out",
        type=Path,
        default=default_html_out_path(repo_root),
        help="Output HTML path for the telg documentation-notes page.",
    )


def run(args: argparse.Namespace) -> None:
    html_out: Path = args.html_out
    html_out.parent.mkdir(parents=True, exist_ok=True)
    H.write_html_to_file(
        body_contents=render_body_contents(),
        write_ctx=H.WriteCtx(
            title=REPORT_TITLE,
            path=str(html_out),
            html_comment=provenance.generated_html_comment(__file__),
        ),
        path_to_style=rtms_report.path_to_gh_pages_style(html_out),
    )
    print(f"HTML: {html_out}")


def main() -> None:
    force_utf8_io()
    repo_root = wlc_paths.wlc_data_root()
    parser = argparse.ArgumentParser(description=__doc__)
    add_args(parser, repo_root=repo_root)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
