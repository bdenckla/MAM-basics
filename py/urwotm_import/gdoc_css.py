"""Parse the document-specific <style> block of a published Google Doc.

Google emits no <h1>/<h2>/<h3> in the published HTML: every block is a
``<p class="cN">`` whose visual role is recoverable only from the CSS. This
module resolves each ``.cN`` class to a property dict so that
:mod:`urwotm_import.inventory` can rank paragraph roles by font size, and so
that :mod:`urwotm_import.class_map` can record the confirmed answer.

Two kinds of class appear, and Google keeps them disjoint:

* *paragraph* classes -- ``text-align``, ``padding-*``, ``margin-left``,
  ``line-height``, ``page-break-after``, ``height``. These sit on the ``<p>``.
* *character* classes -- ``font-size``, ``font-weight``, ``font-style``,
  ``font-family``, ``text-decoration``, ``color``. These sit on the inner
  ``<span>``, and are what a heading's larger type actually comes from.
"""

import re

# One "selector{decls}" rule. Google's published stylesheet has no nesting,
# no @media inside the doc-specific block, and no comments.
_RULE_RE = re.compile(r"([^{}]+)\{([^{}]*)\}")

_PARA_PROPS = (
    "text-align",
    "margin-left",
    "line-height",
    "padding-top",
    "padding-bottom",
    "page-break-after",
    "height",
)
_CHAR_PROPS = (
    "font-size",
    "font-weight",
    "font-style",
    "font-family",
    "text-decoration",
    "color",
    "vertical-align",
)


class Stylesheet:
    """The resolved ``.cN`` (and ``.title``/``.subtitle``) rules of one doc."""

    def __init__(self, rules_in_order):
        # rules_in_order: list of (selector, {prop: value}), source order.
        self._rules = rules_in_order
        self._by_class = {}
        self._class_order = []
        for selector, decls in rules_in_order:
            name = _class_name_of(selector)
            if name is None:
                continue
            if name not in self._by_class:
                self._by_class[name] = {}
                self._class_order.append(name)
            self._by_class[name].update(decls)
        # Bare element rules: p{...}, li{...} supply the inherited defaults.
        self._element = {}
        for selector, decls in rules_in_order:
            sel = selector.strip()
            if sel in ("p", "li", "h1", "h2", "h3", "h4", "h5", "h6"):
                self._element.setdefault(sel, {}).update(decls)

    def class_names(self):
        return list(self._class_order)

    def props_of_class(self, name):
        return dict(self._by_class.get(name, {}))

    def props_of_element(self, tag):
        return dict(self._element.get(tag, {}))

    def resolve(self, class_attr, tag=None):
        """Merge the classes of one element, in stylesheet-definition order.

        All ``.cN`` selectors have equal specificity, so the CSS cascade
        breaks ties by source order -- not by the order the classes happen to
        appear in the ``class`` attribute.
        """
        names = set((class_attr or "").split())
        out = dict(self._element.get(tag, {})) if tag else {}
        for name in self._class_order:
            if name in names:
                out.update(self._by_class[name])
        return out

    def para_props(self, class_attr):
        return _subset(self.resolve(class_attr, "p"), _PARA_PROPS)

    def char_props(self, class_attr):
        return _subset(self.resolve(class_attr), _CHAR_PROPS)


def parse_doc_style(html_doc) -> Stylesheet:
    """Parse the doc-specific stylesheet out of a parsed /pub document.

    A published doc has two ``<style>`` elements: the first is Google's own
    publish-banner chrome, the second (inside ``div#contents``) is the
    document's. Pick the one that actually defines ``.cN`` classes rather than
    trusting the position.
    """
    texts = [st.text_content() for st in html_doc.xpath("//style")]
    candidates = [t for t in texts if re.search(r"\.c\d+\s*\{", t)]
    assert len(candidates) == 1, [len(t) for t in texts]
    return parse_css(candidates[0])


def parse_css(css_text: str) -> Stylesheet:
    rules = []
    for match in _RULE_RE.finditer(css_text):
        selector = match.group(1).strip()
        decls = _parse_decls(match.group(2))
        if decls:
            rules.append((selector, decls))
    return Stylesheet(rules)


def font_size_pt(props):
    """Return the font-size in points, or None."""
    raw = props.get("font-size")
    if not raw:
        return None
    match = re.fullmatch(r"([0-9.]+)pt", raw.strip())
    if match is None:
        return None
    return float(match.group(1))


def is_bold(props) -> bool:
    weight = (props.get("font-weight") or "").strip()
    if weight in ("bold", "bolder"):
        return True
    return weight.isdigit() and int(weight) >= 600


def is_italic(props) -> bool:
    return (props.get("font-style") or "").strip() == "italic"


def is_underlined(props) -> bool:
    return "underline" in (props.get("text-decoration") or "")


###########################################################


def _class_name_of(selector):
    """Return "c7" for a plain ``.c7`` selector, else None.

    Compound and descendant selectors (``ul.lst-kix_x-0``, ``.c9>li:before``)
    are list-bullet machinery, not paragraph or character roles.
    """
    match = re.fullmatch(r"\.([A-Za-z][\w-]*)", selector.strip())
    return match.group(1) if match else None


def _parse_decls(decl_text):
    out = {}
    for chunk in decl_text.split(";"):
        if ":" not in chunk:
            continue
        prop, _, value = chunk.partition(":")
        prop = prop.strip().lower()
        value = value.strip()
        if prop:
            out[prop] = value
    return out


def _subset(props, keys):
    return {k: props[k] for k in keys if k in props}
