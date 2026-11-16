"""Show that page_check.py's checks can fail, and build_page.py's placeholders work.

Written by Claude (Opus 5.5) on 2026-11-15, and moved into this package on 2026-11-16, when
the study was put on ice (morphhb-on-mam/README.md).  run() plants, in memory only, a wrong
headline figure in the page's visible text and three markup faults in a small page, and
prints whether page_check.py's checks catch each; then asks build_page.py for its parts as
if page-fragment.html were missing, or lacked a section, and prints whether the pending
paragraph and the nav's own headings appear.  Writes nothing.
"""

import json

from morphhb_on_mam import build_page as BP
from morphhb_on_mam import page_check as PC

SHALOM = (
    "\N{HEBREW LETTER SHIN}\N{HEBREW POINT SHIN DOT}\N{HEBREW POINT QAMATS}"
    "\N{HEBREW LETTER LAMED}\N{HEBREW LETTER VAV}\N{HEBREW POINT HOLAM}"
    "\N{HEBREW LETTER FINAL MEM}"
)


def run():
    """Print whether each planted fault is caught and each placeholder appears."""
    F = json.loads((PC.OUT / "30-figures.json").read_text(encoding="utf-8"))
    total = "{:,}".format(F["mam_atoms"])
    wrong = "{:,}".format(F["mam_atoms"] + 1)
    text = PC.TEXT.read_text(encoding="utf-8")
    if total not in text:
        raise ValueError("the total is not in the text")
    PC.PROBLEMS.clear()
    PC.check_headlines(text.replace(total, wrong), F)
    print("a wrong total is caught by the headline check:", bool(PC.PROBLEMS))
    found = PC.scan(text.replace(total, wrong))
    print("the scan sees the wrong total:", wrong in found)

    cases = {
        "pointed Hebrew outside lang=hbo": "<p>A word, %s, in prose.</p>" % SHALOM,
        "a Hebrew cell without dir=rtl": '<table><tr><td><span lang="hbo">%s</span>'
        "</td></tr></table>" % SHALOM,
        "a sentence that begins with Hebrew": '<p>Here. <span lang="hbo">%s</span> '
        "begins this one.</p>" % SHALOM,
    }
    for label, snippet in cases.items():
        PC.PROBLEMS.clear()
        parser = PC.Markup()
        parser.feed("<html><body>%s</body></html>" % snippet)
        parser.close()
        PC.check_starts(parser.block_texts)
        print("%s is caught: %s" % (label, bool(PC.PROBLEMS)))

    saved = BP.FRAGMENT
    BP.FRAGMENT = saved.parent / "no-such-fragment.html"
    frag = BP.fragment_sections()
    BP.FRAGMENT = saved
    parts = [BP.fragment_part(frag, a, h)[0] for a, h in BP.FRAGMENT_HEADINGS.items()]
    print(
        "with no fragment, sections 6 and 7 are pending:",
        frag == {} and all(BP.PENDING in p for p in parts),
    )
    nav = "".join(BP.sec_nav(frag))
    print(
        "with no fragment, the nav keeps its own headings:",
        all(">%s<" % h in nav for h in BP.FRAGMENT_HEADINGS.values()),
    )
    partial = {"upkeep": '<section id="upkeep"><p>x</p></section>'}
    upkeep = BP.fragment_part(partial, "upkeep", BP.FRAGMENT_HEADINGS["upkeep"])
    shape = BP.fragment_part(
        partial, "shape-upstream", BP.FRAGMENT_HEADINGS["shape-upstream"]
    )
    print(
        "a section without its own h2 gets one; a missing id is pending:",
        upkeep[0].startswith("<h2>") and upkeep[1] == partial["upkeep"],
        BP.PENDING in shape[0],
    )
