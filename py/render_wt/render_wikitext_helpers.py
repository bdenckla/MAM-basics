"""
Exports:
    render_wtseq
    render_tmpl_el
    render_named_tmpl_el
    get_renopt
    strip_brackets_of_some_kind
"""

from dataclasses import dataclass

from py_misc import scrdfftar_to_doc
from py_misc import trivial_qere_to_doc
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import shrink
from py_misc import uni_check
from py_misc import orphan_marks


@dataclass
class Hctx:
    """Holds rendering context."""

    handlers: dict
    bcvt: tuple = None
    renopts: dict = None
    io_renlog: dict = None

    def mk_new_with_handler(self, handler):
        """Make a new Hctx with the given handler."""
        return Hctx(handler, self.bcvt, self.renopts, self.io_renlog)


def render_wtseq(hctx: Hctx, wtseq):
    """Dispatch a sequence of Wikitext elements to their handlers."""
    newseq = wtseq
    if get_renopt(hctx, "ro_scrdfftar_to_doc"):
        newseq = scrdfftar_to_doc.convert(newseq)
    if get_renopt(hctx, "ro_trivial_ketiv_qere_to_doc"):
        newseq = trivial_qere_to_doc.convert(hctx.bcvt, newseq, hctx.io_renlog)
    handled_elements = _handle_sequence(hctx, newseq)
    het = map(_tuplify, handled_elements)
    out = shrink.shrink(sum(het, tuple()))
    uni_check.check(out)
    return out


def _handle_sequence(hctx, sequence):
    """Pair explicit body templates with their adjacent qere only in ruby mode."""
    from render_wt import render_wikitext_kq as kq

    result = []
    index = 0
    while index < len(sequence):
        element = sequence[index]
        if (
            kq.ruby_enabled(hctx)
            and isinstance(element, dict)
            and element["tmpl_name"]
            in (
                orphan_marks.MARKS_WITHOUT_LETTER,
                orphan_marks.MARKS_WITHOUT_LETTER_OR_SPACE,
                orphan_marks.SPACE_WITHOUT_MARKS,
            )
            and index + 1 < len(sequence)
            and isinstance(sequence[index + 1], dict)
            and sequence[index + 1]["tmpl_name"] == "קרי ולא כתיב"
        ):
            orphan_marks.validate_body(element, hctx.bcvt)
            body = _tuplify(_handle_wikitext_element(hctx, element))
            result.append(kq.handle_qere_with_body(hctx, sequence[index + 1], body))
            index += 2
        else:
            result.append(_handle_wikitext_element(hctx, element))
            index += 1
    return result


def render_tmpl_el(hctx, tmpl, index):
    """Render the template element at the given index."""
    return render_named_param_val(hctx, tmpl, str(index))


def render_named_param_val(hctx, tmpl, param_name):
    """Render the parameter with the given name"""
    param_val = wtp.template_param_val(tmpl, param_name)
    return render_wtseq(hctx, param_val)


def get_renopt(hctx, opt_name: str):
    """Return None or render option named opt_name."""
    return hctx.renopts.get(opt_name) if hctx.renopts else None


def _tuplify(tup_or_nontup):
    if isinstance(tup_or_nontup, tuple):
        return tup_or_nontup
    return (tup_or_nontup,)


def _handle_wikitext_element(hctx: Hctx, elem):
    dispatch_key = _dispatch_key(elem)
    handler = hctx.handlers[dispatch_key]
    return handler(hctx, elem)


def _dispatch_key(elem):
    if isinstance(elem, str):
        return "__" if elem == "__" else str
    return wtp.template_name(elem)
