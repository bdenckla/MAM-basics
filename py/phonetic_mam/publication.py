"""Publish the validated public corpus and its complete licensed asset set."""

from mb_cmn import paths
from phonetic_mam import example_display, release, renderer
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks
from py_html.taamey_d_assets import product_font_assets


def _write(path, data):
    if path.is_file() and path.read_bytes() == data:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def render():
    """Generate one public site; never read or write a sibling repository."""
    release.validate_complete_release()
    examples = release.read_examples()
    example_pages = example_display.page_texts(examples)
    assets = product_font_assets("phonetic-mam")
    for name, data in renderer.source_assets().items():
        assets[f"phonetic-mam/{name}"] = data
    for name in example_display.IMAGE_NAMES:
        source = paths.in_dir() / "phonetic-mam-images" / name
        assets[f"phonetic-mam/img/{name}"] = source.read_bytes()
    root = paths.gh_pages_dir()
    for relative, data in assets.items():
        _write(root / relative, data)
    site = root / "phonetic-mam"
    for name, text in {"index.html": renderer.render_index(), **example_pages}.items():
        refuse_forbidden_phonetic_marks(text, name)
        _write(site / name, text.encode("utf-8"))
    for book in release.iter_books():
        for name, text in renderer.render_book_pages(book).items():
            refuse_forbidden_phonetic_marks(text, name)
            _write(site / name, text.encode("utf-8"))
