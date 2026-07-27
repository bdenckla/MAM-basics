"""Import the four-part series "Undoing and redoing the work of the
Masoretes" (urwotm) from published Google Docs into authored Python modules.

This is one-shot tooling. Once py/author_misc/urwotm_*.py are the source of
truth, the emitter half of this is deleted (see the plan's Phase 8); only the
differential verifier and the vendored source text survive.

Subcommands:
    fetch      Download the four /pub documents into .novc/urwotm_cache/.
    inventory  Write the class / link / $-candidate reports.
    images     Download the images, write the manifest and contact sheets.
    install-images
               Copy the cached images into MAM-with-doc under the descriptive
               names in urwotm_import/img_names.py.
    emit       Write py/author_misc/urwotm_N_*.py and the per-part report.

Examples:
    .venv/Scripts/python.exe py/main_urwotm_import.py fetch
    .venv/Scripts/python.exe py/main_urwotm_import.py inventory
    .venv/Scripts/python.exe py/main_urwotm_import.py images
    .venv/Scripts/python.exe py/main_urwotm_import.py emit --part 1
"""

import argparse
import sys

from mb_cmn import paths
from mb_cmn import polite_download
from urwotm_import import difftext as difftext_mod
from urwotm_import import emit as emit_mod
from urwotm_import import fetch as fetch_mod
from urwotm_import import gdoc_parse
from urwotm_import import images as images_mod
from urwotm_import import inventory as inventory_mod
from urwotm_import import parts


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True
    _add_subcommands(subparsers)
    args = parser.parse_args()
    args.func(args)


def _add_subcommands(subparsers) -> None:
    fetch_parser = subparsers.add_parser(
        "fetch", help="Download the four /pub documents into the .novc cache."
    )
    _add_part_opt(fetch_parser)
    fetch_parser.set_defaults(func=_run_fetch)

    inv_parser = subparsers.add_parser(
        "inventory", help="Write the class / link / $-candidate reports."
    )
    _add_part_opt(inv_parser)
    inv_parser.set_defaults(func=_run_inventory)

    img_parser = subparsers.add_parser(
        "images",
        help="Download images, write the manifest and the contact sheets.",
    )
    _add_part_opt(img_parser)
    img_parser.add_argument(
        "--redownload",
        action="store_true",
        help="re-fetch the image bytes instead of reusing the cached manifest",
    )
    img_parser.set_defaults(func=_run_images)

    install_parser = subparsers.add_parser(
        "install-images",
        help="Copy cached images into MAM-with-doc under their real names.",
    )
    _add_part_opt(install_parser)
    install_parser.set_defaults(func=_run_install_images)

    emit_parser = subparsers.add_parser(
        "emit",
        help="Write the authored Python module(s) and the per-part report.",
    )
    _add_part_opt(emit_parser)
    emit_parser.set_defaults(func=_run_emit)

    diff_parser = subparsers.add_parser(
        "difftext",
        help="Diff the generated page against the source doc, word by word.",
    )
    _add_part_opt(diff_parser)
    diff_parser.set_defaults(func=_run_difftext)


def _add_part_opt(parser) -> None:
    parser.add_argument(
        "--part",
        type=int,
        choices=parts.PART_NUMS,
        action="append",
        help="restrict to this part (repeatable); default is all four",
    )


def _part_nums(args):
    return tuple(args.part) if args.part else parts.PART_NUMS


def _run_fetch(args: argparse.Namespace) -> None:
    htmls = fetch_mod.download_all(_part_nums(args))
    for part, html in sorted(htmls.items()):
        print(f"part {part}: {len(html)} chars -> {fetch_mod.snapshot_path(part)}")


def _run_inventory(args: argparse.Namespace) -> None:
    inventory_mod.run(_part_nums(args))


def _run_images(args: argparse.Namespace) -> None:
    refs = images_mod.cached_refs() if not args.redownload else None
    if refs is None:
        part_nums = _part_nums(args)
        docs = {
            part: gdoc_parse.parse_html(part, html)
            for part, html in fetch_mod.read_all(part_nums).items()
        }
        refs = images_mod.collect_refs(docs)
        print(f"{len(refs)} images referenced; downloading...")
        config = fetch_mod.download_config()
        with polite_download.PoliteDownloader(config) as downloader:
            images_mod.download(refs, downloader)
    else:
        print(f"{len(refs)} images reused from the cache")
    manifest_path = images_mod.write_manifest(refs)
    report_path = parts.report_dir() / "img_manifest.md"
    parts.report_dir().mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(images_mod.manifest_report(refs)), encoding="utf-8", newline="\n"
    )
    print(f"wrote {manifest_path}")
    print(f"wrote {report_path}")
    for path in images_mod.write_contact_sheets(refs):
        print(f"wrote {path}")


def _run_install_images(args: argparse.Namespace) -> None:
    written = images_mod.install(images_mod.read_manifest(), _part_nums(args))
    print(f"installed {len(written)} images into {written[0].parent}")


def _run_emit(args: argparse.Namespace) -> None:
    part_nums = _part_nums(args)
    refs = images_mod.read_manifest()
    htmls = fetch_mod.read_all(part_nums)
    out_dir = paths.repo_root() / "py" / "author_misc"
    parts.report_dir().mkdir(parents=True, exist_ok=True)
    for part in part_nums:
        doc = gdoc_parse.parse_html(part, htmls[part])
        source, notes = emit_mod.emit_module(doc, refs)
        module_path = out_dir / f"{emit_mod.module_stem(part)}.py"
        module_path.write_text(source, encoding="utf-8", newline="\n")
        report_path = parts.report_dir() / f"emit_p{part}.md"
        report_path.write_text(
            "\n".join(emit_mod.report_lines(notes)), encoding="utf-8", newline="\n"
        )
        print(f"wrote {module_path}")
        print(f"wrote {report_path}")


def _run_difftext(args: argparse.Namespace) -> None:
    part_nums = _part_nums(args)
    htmls = fetch_mod.read_all(part_nums)
    parts.report_dir().mkdir(parents=True, exist_ok=True)
    all_ok = True
    for part in part_nums:
        lines, ok = difftext_mod.diff_report(part, htmls[part])
        path = parts.report_dir() / f"difftext_p{part}.md"
        path.write_text("\n".join(lines), encoding="utf-8", newline="\n")
        print(f"part {part}: {'OK' if ok else 'UNEXPECTED DIFFERENCES'} -> {path}")
        all_ok = all_ok and ok
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
