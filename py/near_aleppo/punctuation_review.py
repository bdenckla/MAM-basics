"""Reproducible offline extract of the edition's final-punctuation ketiv cases.

The tracked selection names the requested frozen and reviewed records. Their
current dataset targets must agree with the inputs. Verse text and complete notes
come from the edition's shared renderer, including notes normally on a big-doc
page. The wrapper adds sizing, isolation and hover names without changing text.
Run py/main_near_aleppo.py --punctuation-review (or append --check).
"""

import base64
import copy
from html import escape
import json
import re

from mb_cmn import bib_locales as tbn
from mb_cmn import mam_bknas_and_std_bknas as bkn
from mb_cmn import read_books_from_mam_parsed_plus as plus
from mb_cmn import uni_heb
from mb_misc import mb_html
from near_aleppo import build_paths, edition, frozen_ketiv
from py_misc import mam_doc_utils, mwd_utils, near_aleppo_params as nap
from py_misc import ren_html_for_renel as hfr
from render_wt import render_wikitext as rwt

_SELECTION = build_paths.input_dir() / "final-punctuation-review-selection.json"
_OUTPUT = build_paths.dataset_dir().parent / "review"
_BASENAME = "ketiv-final-punctuation"
_GROUPS = {
    "maqaf": ("־", 36, 6, 0),
    "pasoleg": ("׀", 5, 6, 1),
}
_SOURCES = (
    "in/near-aleppo/frozen-pointed-ketiv.json",
    "in/near-aleppo/reviewed-pointed-ketiv.json",
)
_HEBREW = re.compile(r"[\u0590-\u05ff]")
_TOKENS = re.compile(r"\s+|\S+")


def selected_records():
    selection = json.loads(_SELECTION.read_bytes())
    if set(selection) != {"format", "groups"} or selection["format"] != (
        "near-aleppo-punctuation-review-v1"
    ):
        raise ValueError("Unexpected punctuation review selection")
    if [g["kind"] for g in selection["groups"]] != list(_GROUPS):
        raise ValueError("Unexpected punctuation review groups")
    result = []
    for group in selection["groups"]:
        kind = group["kind"]
        punctuation, frozen_count, reviewed_count, edition_count = _GROUPS[kind]
        if set(group) != {"kind", "sources", "edition_sites"} or set(
            group["sources"]
        ) != set(_SOURCES):
            raise ValueError(f"{kind}: unexpected input sources")
        for name, count in zip(_SOURCES, (frozen_count, reviewed_count)):
            records = json.loads((build_paths.mam_basics_dir() / name).read_bytes())[
                "records"
            ]
            selected = group["sources"][name]
            status = "Added" if name == _SOURCES[0] else "Already present"
            if set(selected) != {"status", "ids"} or selected["status"] != status:
                raise ValueError(f"{name}: unexpected change label")
            ids = selected["ids"]
            if len(ids) != count or len(set(ids)) != count:
                raise ValueError(f"{name}: unexpected selection size or duplicate")
            by_id = {row["id"]: row for row in records}
            eligible = {
                r["id"] for r in records if r["tmpl_params"]["2"].endswith(punctuation)
            }
            if set(ids) != eligible:
                raise ValueError(
                    f"{name}: {kind}-final population differs from selection"
                )
            for identity in ids:
                row = by_id[identity]
                value = row["value"]
                final = value if isinstance(value, str) else value[-1]
                if not isinstance(final, str) or not final.endswith(punctuation):
                    raise ValueError(f"{identity}: pointed ketiv lacks final {kind}")
                result.append({"source": name, "group": kind, "status": status, **row})
        if len(group["edition_sites"]) != edition_count:
            raise ValueError(f"{kind}: unexpected edition-site count")
        for row in group["edition_sites"]:
            if row["tmpl_name"] != "מ:קו״כ-אם-2" or row["status"] != "Already present":
                raise ValueError("Unexpected edition-site template or change label")
            if not all(
                row["tmpl_params"][key].endswith(punctuation) for key in ("1", "3")
            ):
                raise ValueError(f"{row['id']}: trivial readings lack final {kind}")
            result.append(
                {
                    "source": "edition",
                    "group": kind,
                    "value": row["tmpl_params"]["1"],
                    **row,
                }
            )
    return result


def display_shunnas(text):
    """Use the authoritative names, with literal guillemets only in this wrapper."""
    return ",".join(c if c in "«»" else uni_heb.shunna(c) for c in text)


def _hover(value):
    if isinstance(value, str):
        return tuple(
            (
                mb_html.span(token, {"title": display_shunnas(token)})
                if _HEBREW.search(token) or "«" in token or "»" in token
                else token
            )
            for token in _TOKENS.findall(value)
        )
    if isinstance(value, (tuple, list)):
        return mb_html.flatten(tuple(_hover(child) for child in value))
    node = copy.deepcopy(value)
    if node.get("contents"):
        node["contents"] = mb_html.flatten(_hover(node["contents"]))
    if mb_html.htel_get_tag(node) == "bdi":
        attrs = node.setdefault("attr", {})
        attrs["dir"] = "ltr" if attrs.get("lang") == "en" else "rtl"
    return node


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, (tuple, list)):
        return "".join(_text(child) for child in value)
    return _text(value.get("contents") or ())


def _panel(nodes, identity, label, source_data):
    original = _text(nodes)
    hovered = _hover(nodes)
    if _text(hovered) != original:
        raise AssertionError("Review wrapper changed renderer text")
    source_data.append({"label": label, "element_id": identity, "hebrew": original})
    contents = mb_html.el_to_str_for_sef(mb_html.div(hovered))
    return (
        f'<div class="hebrew" lang="he" dir="rtl" id="{identity}">' f"{contents}</div>"
    )


def _resolved_targets(records):
    books, resolved = {}, []
    for row in records:
        name, chapter, number = row["verse"]
        stem, _, sub = name.partition(" ")
        # Some single-book filenames contain spaces; prefer the complete stem.
        full_path = build_paths.dataset_dir() / f"{name}.json"
        path = (
            full_path
            if full_path.is_file()
            else build_paths.dataset_dir() / f"{stem}.json"
        )
        if path not in books:
            books[path] = json.loads(path.read_bytes())
        parts = [
            part
            for part in books[path]["book39s"]
            if part["sub_book_name"] == (None if full_path.is_file() else sub)
        ]
        if len(parts) != 1:
            raise ValueError(f"{row['id']}: dataset book is ambiguous")
        part = parts[0]
        cells = part["chapters"][chapter][number]
        target = frozen_ketiv.at_path(cells[2], row["path"])
        expected = (
            row["tmpl_params"]
            if row["source"] == "edition"
            else {**row["tmpl_params"], nap.POINTED_KETIV: row["value"]}
        )
        actual = {k: v for k, v in target["tmpl_params"].items() if k not in nap.FLAGS}
        if actual != expected:
            raise ValueError(
                f"{row['id']}: edition target differs from its pointing input"
            )
        bkid = bkn.MAM_HBNP_TO_BK39ID[(part["book24_name"], part["sub_book_name"])]
        resolved.append((row, bkid, tbn.mk_bcvtmam(bkid, int(chapter), int(number))))
    return resolved


def render():
    records = selected_records()
    resolved = _resolved_targets(records)
    bkids = tuple(dict.fromkeys(bkid for _, bkid, _ in resolved))
    books = plus.read_parsed_plus_bk39s(bkids, str(build_paths.dataset_dir().parent))
    mode = edition.NEAR_ALEPPO_MODE
    ctx = hfr.HfrCtx(mode.ht_tac_for_ren_tag)
    rendered = {bkid: rwt.render(bkid, books, mode.renopts, {}) for bkid in bkids}
    source_data = []
    sections = {kind: [] for kind in _GROUPS}
    plain = []
    for ordinal, (record, bkid, target_bcvt) in enumerate(resolved, 1):
        verse_map = rendered[bkid]
        keys = list(verse_map)
        position = keys.index(target_bcvt)
        context = keys[max(0, position - 1) : position + 2]
        reference = f"{bkid} {record['verse'][1]}:{record['verse'][2]}"
        rows = []
        plain.append(f"{ordinal}. {reference} ({record['group']}; {record['status']})")
        for offset, bcvt in enumerate(context):
            veraf = verse_map[bcvt]
            nondoc = veraf.map_over(mam_doc_utils.mark_doc_targets)
            docs = veraf.map_over(mam_doc_utils.extract_docs)
            ver_ndd = mwd_utils.VerseNdd(bcvt, nondoc, docs)
            verse_html = mwd_utils._html_for_nondoc(ctx, ver_ndd)
            # Keep complete notes in the extract, including the long-note content.
            doc_ctx = mwd_utils._DocCtx(bkid, ctx, ver_ndd)
            notes_html = mwd_utils._html_for_docs(
                doc_ctx, mwd_utils._DocType.SELF_CONTAINED
            )
            chapter, number = tbn.bcvt_get_chnu_vrnu(bcvt)
            label = f"{bkid} {chapter}:{number}"
            focus = " target" if bcvt == target_bcvt else " context"
            verse = _panel(
                verse_html.verse, f"case-{ordinal}-verse-{offset}", label, source_data
            )
            notes = _panel(
                notes_html.verse,
                f"case-{ordinal}-notes-{offset}",
                label + " notes",
                source_data,
            )
            rows.append(
                f'<div class="verse-row{focus}"><p class="verse-label" dir="ltr">'
                f"{escape(label)}</p><div>{verse}</div><div>{notes}</div></div>"
            )
            plain.extend((label, _text(verse_html.verse), _text(notes_html.verse), ""))
        sections[record["group"]].append(
            f'<section id="case-{ordinal}"><h3>{ordinal}. {escape(reference)} '
            f'<small>{escape(record["status"])}</small></h3>{"".join(rows)}</section>'
        )
    root = build_paths.mam_basics_dir()
    css = (root / "py/mb_misc/styles_mam_with_doc.css").read_text(encoding="utf-8")
    font = (root / "gh-pages/near-aleppo/edition/woff2/Taamey_D.woff2").read_bytes()
    css = css.replace(
        'url("woff2/Taamey_D.woff2")',
        'url("data:font/woff2;base64,' + base64.b64encode(font).decode("ascii") + '")',
    )
    support = root / "in/font-support/taamey-d-0.921"
    notice = (support / "FONT-NOTICE.txt").read_text(encoding="utf-8")
    license_text = (support / "GPL-2.0.txt").read_text(encoding="utf-8")
    embedded = json.dumps(source_data, ensure_ascii=False).replace("<", "\\u003c")
    title = "Near-Aleppo: final-punctuation ketiv extract"
    groups_html = "".join(
        f'<div id="{kind}" class="case-group"><h2>{kind.capitalize()} ({len(cases)})</h2>{"".join(cases)}</div>'
        for kind, cases in sections.items()
    )
    page = (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; '
        "style-src 'unsafe-inline'; script-src 'unsafe-inline'; font-src data:; "
        "connect-src 'none'\">"
        f"<title>{title}</title><style>{css}\n{_CSS}</style></head><body>"
        f"<header><h1>{title}</h1><p>42 maqaf cases and 12 pasoleg cases, "
        "with verse context and notes.</p>"
        '<label for="hebrew-size">Hebrew size </label>'
        '<input id="hebrew-size" type="range" min="20" max="48" step="1" value="30">'
        '<output id="size-value" for="hebrew-size">30 px</output></header><main>'
        + groups_html
        + "</main><footer>Derived from Miqra according to the Masorah, "
        "by Seth (Avi) Kadish, with technical assistance from Erel Segal-Halevi "
        "and Benjamin Denckla. CC BY-SA 4.0. Taamey D font notices and GPL v2 "
        "license are embedded in this file.</footer>"
        f'<script id="source-data" type="application/json">{embedded}</script>'
        f'<script id="selection-data" type="application/json">{json.dumps(records, ensure_ascii=False).replace("<", "\\u003c")}</script>'
        f'<script id="font-license" type="text/plain">{notice}{license_text}</script>'
        f"<script>{_SCRIPT}</script></body></html>\n"
    )
    return {
        _BASENAME + ".html": page.encode("utf-8"),
        _BASENAME + ".txt": ("\n".join(plain).rstrip("\n") + "\n").encode("utf-8"),
    }


_CSS = """
:root { --hebrew-size: 30px; color-scheme: light; }
body { margin: 0 auto; padding: 1.4rem; max-width: 110rem;
       font: 16px/1.55 system-ui, sans-serif; color: #222; background: #fff; }
h1 { font-size: 1.5rem; } h2 { font-size: 1.3rem; } h3 { font-size: 1.1rem; } small { font-size: .85rem; }
h3 small { margin-left: 1rem; font-weight: normal; }
header { margin-bottom: 2rem; } input { vertical-align: middle; } output { margin-left: .7rem; }
section { padding: .7rem 0 1.7rem; border-top: 1px solid #aaa; }
.verse-row { display: grid; grid-template-columns: 7rem minmax(0, 1fr) minmax(0, 1fr);
             gap: 1rem; padding: 1rem .7rem; }
.target { background: #f5f7fa; border-block: 1px solid #d4d8e0; }
.verse-label { font-size: .85rem; text-align: left; align-self: start; }
.hebrew { font-family: "Taamey D WOFF2", "SBL Hebrew", "Ezra SIL", "Noto Serif Hebrew",
          "Noto Sans Hebrew", "David", "DejaVu Sans", serif;
          font-size: var(--hebrew-size); line-height: 1.95; text-align: center;
          unicode-bidi: isolate; letter-spacing: normal; overflow-wrap: normal; }
.hebrew [lang="hbo"] { font-size: inherit; }
.hebrew [lang="en"], .near-aleppo-english { font: 16px/1.55 system-ui, sans-serif;
                                          direction: ltr; unicode-bidi: isolate; }
bdi { unicode-bidi: isolate; } .mam-doc-parts { text-align: right; }
.context { color: #555; } footer { font-size: .85rem; margin-top: 2rem; }
:focus-visible { outline: 3px solid #245baa; outline-offset: 3px; }
@media (max-width: 850px) {
  body { padding: .8rem; } .verse-row { grid-template-columns: minmax(0,1fr); }
  .verse-label { margin: 0; } .hebrew { width: 100%; }
}
@media print {
  header input, header label, header output { display: none; }
  body { max-width: none; padding: 0; } section { break-inside: avoid; }
}
"""

_SCRIPT = """
const slider = document.getElementById('hebrew-size');
const value = document.getElementById('size-value');
slider.addEventListener('input', () => {
  document.documentElement.style.setProperty('--hebrew-size', slider.value + 'px');
  value.textContent = slider.value + ' px';
});
"""


def main(check=False):
    outputs = render()
    if check:
        for name, content in outputs.items():
            if (_OUTPUT / name).read_bytes() != content:
                raise AssertionError(f"Punctuation extract differs: {name}")
        print("Punctuation review extract is current: 42 maqaf + 12 pasoleg cases")
    else:
        _OUTPUT.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (_OUTPUT / name).write_bytes(content)
        print(f"Wrote 42 maqaf + 12 pasoleg cases with context and notes to {_OUTPUT}")
