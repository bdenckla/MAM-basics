"""Write every base chapter's page from the tracked JSON into a new directory, to preview.

Each page goes to <stem>/<two-digit chapter>.wiki, exactly as MediaWiki would store it,
and titles.tsv maps each file to its Wikisource title. Nothing tracked is written.
"""

from pathlib import Path

from miqra_mevoar import tracked
from miqra_mevoar import wikitext


def run(out_dir):
    """Write the pages into out_dir, which must not exist yet."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=False)
    titles = []
    for book in tracked.tracked_books():
        for chapter in tracked.read_record(book)["chapters"]:
            rel = f"{book.stem}/{chapter['chapter']:02d}.wiki"
            _write(out / rel, wikitext.chapter_wikitext(chapter))
            title = wikitext.page_title(book.mam_book, chapter["chapter"])
            titles.append(f"{rel}\t{title}")
    _write(out / "titles.tsv", "\n".join(titles) + "\n")
    print(f"{len(titles)} pages: {out}")


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="")
