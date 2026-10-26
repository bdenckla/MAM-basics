"""Independent endpoint and focused renderer comparisons; no sibling inputs."""

from hashlib import sha256
from pathlib import Path
import re
import subprocess

from mb_cmn import paths
from near_aleppo import doc_investigation
from py_html import taamey_d_assets
from py_render import uc_html

OLD = "4490e668dc168b598010dd2250878defc88830c1"
ROOT = paths.repo_root()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def test_asset_bytes_and_source_links():
    old_fonts = [
        p.decode()
        for p in git("ls-tree", "-r", "--name-only", "-z", OLD).split(b"\0")
        if p.endswith(b".woff2")
    ]
    assert len(old_fonts) == 17
    canonical = taamey_d_assets.font_bytes()
    assert (
        sha256(canonical).hexdigest()
        == "5cc8df8ae3311b91e506edbb294561f6f0e39ebe4260bdb972c90902186c2474"
    )
    assert all(git("show", f"{OLD}:{name}") == canonical for name in old_fonts)
    assets = taamey_d_assets.site_font_assets()
    assert len(assets) == 9
    for name, data in assets.items():
        assert (ROOT / "gh-pages" / name).read_bytes() == data, name
    source = ROOT / "gh-pages/woff2/SOURCE.txt"
    links = re.findall(r"^  (\.\./\S+)$", source.read_text(), re.M)
    assert len(links) == 2
    assert all((source.parent / link).is_file() for link in links)
    assert "No exact rebuild is claimed" in source.read_text()


def test_changed_published_html_only_moves_font_references():
    names = git("diff", "--name-only", "-z", OLD, "HEAD", "--", "gh-pages").split(b"\0")
    changed_html = [n.decode() for n in names if n.endswith(b".html")]
    assert len(changed_html) == 3
    for name in changed_html:
        before = git("show", f"{OLD}:{name}").decode()
        after = (ROOT / name).read_text()
        collapse = lambda text: re.sub(
            r"(?:\.\./)*woff2/(?:Taamey_D\.woff2|SOURCE\.txt)", "FONT-REFERENCE", text
        )
        assert collapse(before) == collapse(after), name


def test_investigation_reproduces():
    pages = doc_investigation.render()
    assert pages
    for name, data in pages.items():
        assert (ROOT / "gh-pages/near-aleppo" / name).read_bytes() == data, name


def test_report_assets_shared_and_standalone(tmp_path):
    assets = ROOT / "holman/assets"
    for href, expected_url in (
        ("../report.css", "../woff2/Taamey_D.woff2"),
        (None, "woff2/Taamey_D.woff2"),
    ):
        directory = tmp_path / ("shared" if href else "standalone")
        directory.mkdir()
        output = directory / "review.html"
        uc_html._write_assets(
            assets_dir=assets,
            output_html_path=output,
            filter_ids=[],
            report_css_href=href,
        )
        css = output.with_suffix(".css").read_text()
        assert css.count(f'url("{expected_url}")') == 1
        font = directory / taamey_d_assets.FONT
        assert font.exists() == (href is None)
        if href is None:
            assert font.read_bytes() == taamey_d_assets.font_bytes()
