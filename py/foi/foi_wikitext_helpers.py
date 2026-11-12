import re

from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import ws_tmpl_named_params as wtnp
from mb_cmn import template_names as tmpln
from mb_cmn.my_utils import sum_of_map
from foi import foi_gray_marks as gray_marks

# Character-class contents: Hebrew letters, Hebrew marks and the three joiners.
# The Hebrew marks are the Hebrew block's range from HEBREW ACCENT ETNAHTA to
# HEBREW POINT QAMATS QATAN, a range that also holds four punctuation code points,
# MAQAF, PASEQ, SOF PASUQ and NUN HAFUKHA, together with HEBREW POINT
# JUDEO-SPANISH VARIKA, which Unicode encodes outside that block.
LETTERS_MARKS_JOINERS = (
    "\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}"
    "\N{HEBREW ACCENT ETNAHTA}-\N{HEBREW POINT QAMATS QATAN}"
    "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"
    "\N{COMBINING GRAPHEME JOINER}"
    "\N{ZERO WIDTH NON-JOINER}"
    "\N{ZERO WIDTH JOINER}"
)
# Character-class contents: the two double guillemets.
DOUBLE_GUILLEMETS = (
    "\N{LEFT-POINTING DOUBLE ANGLE QUOTATION MARK}"
    "\N{RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK}"
)
_FORM = re.compile(
    "[" + LETTERS_MARKS_JOINERS + DOUBLE_GUILLEMETS + gray_marks.STAND_INS + r"\[\]+]+"
)


def forms(string):
    """Return the forms of a string, its maximal runs of form characters, in order.

    The form characters are those of LETTERS_MARKS_JOINERS and the characters of the
    notation that MAM's documentation notes use within a form: square brackets, plus
    signs and the two double guillemets.  Every other character separates forms: a
    space, and punctuation such as a parenthesis, an angle bracket, a comma, a full
    stop or an equals sign.  So where a note gives a list of sigla, an equals sign and
    a pointed form, that pointed form is a form of its own, with none of the list's
    punctuation attached.  In a string of Scripture, a form is a chanted word, or as
    much of one as the string holds, together with any PASEQ or SOF PASUQ written
    against it, since LETTERS_MARKS_JOINERS includes those punctuation code points.

    Ben Denckla decided on 2026-11-09 that a form keeps its sof pasuq, as it keeps its
    maqaf: "neither should ever be stripped, at least not in any case I can think of.
    Probably also applies to legarmeh (but NOT paseq in the narrow sense!)".  Where
    MAM-parsed-plus writes such a mark in a template or a string apart from its form,
    a FOI that reads by forms reads its strings as with_attached_marks returns them,
    which puts the mark back on its form.  The stand-ins that it writes for the marks
    that such a FOI shows gray, foi_gray_marks.STAND_INS, are form characters too.
    """
    return _FORM.findall(string)


_LEGARMEH = "מ:לגרמיה-2"
_GRAY_MAQAF = "מ:מקף אפור"
_LARGE_LETTER = "מ:אות-ג"
# The marks that with_attached_marks moves from the start of a string to the
# template before it.
_MARKS_AFTER_A_TEMPLATE = hpu.SOPA, hpu.MAQ
# For each template that a mark can follow, the parameters on whose last forms
# with_attached_marks puts the mark: the template's Scripture.  For a ketiv/qere
# template that means its pointed forms, and for a special-letter word both of its
# forms of the word, parameter 1 with its special-letter templates and parameter 2
# without them.  None leaves the mark where it is: the silluq-before-meteg template's
# parameter 1 may hold no punctuation, which validate_current_plus_template enforces.
# Ben approved the entries for a targeted scroll-difference note, a special-letter
# word and a large letter, and the None, on 2026-11-09.
_PARAMS_TAKING_A_MARK_AFTER = {
    "נוסח": ("1",),
    tmpln.QAMATS_VARIANT: ("ד", "ס"),
    "כו״ק": ("2",),
    "קו״כ": ("2",),
    "מ:כו״ק מיוחד": ("2",),
    tmpln.TRIVIAL_QERE: ("1", "3"),
    tmpln.SCRDFF_TAR: ("1",),
    tmpln.SLH_WORD: ("1", "2"),
    _LARGE_LETTER: ("1",),
    tmpln.SILLUQ_BEFORE_METEG: None,
}


def with_attached_marks(wtseq):
    """Return wtseq as a FOI that reads by forms reads it, with marks on their forms.

    MAM-parsed-plus writes some marks apart from the forms they belong to.  It writes
    legarmeh as the template מ:לגרמיה-2, directly after the string that ends with its
    chanted word, and MAM's gray maqaf as the template מ:מקף אפור, between the atoms
    that it joins.  And where a template ends a verse's text, as a documentation note,
    a qamats variant or a ketiv/qere template can, the verse's sof pasuq begins the
    string after that template.  Read string by string, those forms would lack their
    marks.  This reading puts the marks back, at every depth, and leaves the data
    unchanged:

    1. A PASEQ code point ends the string before each legarmeh template.  After a large
       letter, as in a note at Leviticus 8:23, it ends the large letter's parameter 1
       instead.  The legarmeh template stays where it is, and holds nothing that a FOI
       reading by forms reads.
    2. A gray maqaf becomes the stand-in foi_gray_marks.GRAY_MAQAF, which ends the
       string before it and which the string after it continues, so that the atoms it
       joins are one form.  After a template, the stand-in ends the last form of each
       parameter that _PARAMS_TAKING_A_MARK_AFTER names for that template instead.
    3. A sof pasuq or maqaf that begins a string after a template moves to the end of
       the last form of each parameter that _PARAMS_TAKING_A_MARK_AFTER names for that
       template, through any template that ends such a parameter.  A template without
       an entry raises.

    Ben Denckla decided rule 2 on 2026-11-09: a form includes MAM's gray maqaf, shown
    gray and perhaps noted in a GM column of its own, which foi_gray_marks does.  The
    same day he asked for a supplied sof pasuq to be gray, in a GSP column, "for cases
    where, narrowly speaking, the phenomenon in question does not include sof pasuq
    (e.g. the argument of a template being "studied" (listed))".  He then ruled out
    the Unicode and dual-ml-alef FOIs: "These FOIs are not studying/listing something
    like all uses of the X template."  Nor does rule 3 move a mark into a note's body,
    the documentation that the doc-note-notation FOI lists.  So the mark that rule 3
    moves is shown as it is.

    A mark that begins its sequence follows no template, so it stays where it is: the
    sof pasuq that is itself the target of a documentation note, at Genesis 35:22 and
    in both Decalogues, where the verse division depends on the strand, and the maqaf
    that begins parameter 3 of a כתיב ולא קרי template.  A narrow-sense paseq, which is
    the template מ:פסק, still separates the forms around it, as Ben decided.
    """
    out = []
    after_gray_maqaf = False
    for wtel in wtseq:
        prev = out[-1] if out else None
        if isinstance(wtel, str):
            if any(stand_in in wtel for stand_in in gray_marks.STAND_INS):
                raise ValueError(f"MAM's text holds a gray-mark stand-in: {wtel!r}")
            if after_gray_maqaf:
                out[-1] = prev + wtel
            elif prev is not None and wtel[:1] in _MARKS_AFTER_A_TEMPLATE:
                out[-1:] = _with_mark_moved_back(prev, wtel)
            else:
                out.append(wtel)
            after_gray_maqaf = False
            continue
        after_gray_maqaf = False
        tmpl = _with_attached_marks_in_params(wtel)
        tmpl_name = wtp.template_name(tmpl)
        if tmpl_name == _LEGARMEH:
            out[-1] = _with_legarmeh(prev, out)
            out.append(tmpl)
        elif tmpl_name == _GRAY_MAQAF:
            after_gray_maqaf = _add_gray_maqaf(out, tmpl)
        else:
            out.append(tmpl)
    return out


def _with_attached_marks_in_params(tmpl):
    tmpln.validate_current_plus_template(tmpl)
    return wtp.mktmpl_mp(with_attached_marks, tmpl)


def _add_gray_maqaf(io_out, tmpl):
    """Add a gray maqaf to io_out; return whether the string after it continues it."""
    prev = io_out[-1] if io_out else None
    if isinstance(prev, str):
        io_out[-1] = _with_mark_on_last_form(prev, gray_marks.GRAY_MAQAF)
        return True
    if prev is None:
        raise ValueError(f"a gray maqaf begins its sequence: {tmpl!r}")
    if (attached := _with_mark_after(prev, gray_marks.GRAY_MAQAF)) is not None:
        io_out[-1] = attached
    else:
        io_out.append(tmpl)
    return False


def _with_mark_moved_back(prev, string):
    """Return prev and string, with the mark that begins string moved back into prev."""
    if isinstance(prev, str):
        raise ValueError(f"a string directly after a string: {prev!r}, {string!r}")
    attached = _with_mark_after(prev, string[0])
    if attached is None:
        return [prev, string]
    rest = string[1:]
    return [attached, rest] if rest else [attached]


def _with_legarmeh(prev, out):
    if isinstance(prev, str):
        return _with_mark_on_last_form(prev, hpu.PASOLEG)
    if prev is not None and wtp.is_template_with_name(prev, _LARGE_LETTER):
        return _with_mark_after(prev, hpu.PASOLEG)
    raise ValueError(f"a legarmeh after neither string nor large letter: {out!r}")


def _with_mark_after(tmpl, mark):
    """Return tmpl with mark on the last form of each parameter that takes it.

    Return None if the mark stays apart.
    """
    tmpl_name = wtp.template_name(tmpl)
    if tmpl_name not in _PARAMS_TAKING_A_MARK_AFTER:
        raise ValueError(f"no parameter is named to take {mark!r} after {tmpl!r}")
    if (param_names := _PARAMS_TAKING_A_MARK_AFTER[tmpl_name]) is None:
        return None
    params = dict(tmpl["tmpl_params"])
    for param_name in param_names:
        param_val = wtp.template_param_val(tmpl, param_name)
        if not param_val:
            raise ValueError(
                f"parameter {param_name} is empty, to take {mark!r}: {tmpl!r}"
            )
        *init, last = param_val
        if isinstance(last, str):
            new_last = _with_mark_on_last_form(last, mark)
        elif (new_last := _with_mark_after(last, mark)) is None:
            return None
        params[param_name] = wtnp.simplify_singleton([*init, new_last])
    return {**tmpl, "tmpl_params": params}


def _with_mark_on_last_form(string, mark):
    if not string or not _FORM.fullmatch(string[-1]):
        raise ValueError(f"no form ends {string!r}, to take {mark!r}")
    return string + mark


def templates_before_sof_pasuq(wtseq):
    """Return the ids of the templates in wtseq, at any depth, that a sof pasuq follows.

    A template counts if a string beginning with a sof pasuq directly follows it, or if
    it ends a parameter that _PARAMS_TAKING_A_MARK_AFTER names for a template that
    counts.  These are the templates on whose parameters' last forms rule 3 of
    with_attached_marks puts that sof pasuq, and the same closed table raises on any
    other template before a sof pasuq.  A FOI that lists the argument of such a
    template adds the sof pasuq after it, gray, as foi_gray_marks.gray_sof_pasuq.  An
    id names its template while the FOI's traversal holds the same template objects,
    as it does within one call.

    The search enters every parameter of every template, at any depth, as
    with_attached_marks does, and like it validates each template first with
    validate_current_plus_template, so an unknown template or parameter raises.
    """
    found = set()
    _add_templates_before_sof_pasuq(wtseq, found)
    return found


def _add_templates_before_sof_pasuq(wtseq, io_found):
    seq = list(wtseq)
    for index, wtel in enumerate(seq):
        if isinstance(wtel, str):
            continue
        tmpln.validate_current_plus_template(wtel)
        for param_val in wtp.template_param_vals(wtel):
            _add_templates_before_sof_pasuq(param_val, io_found)
        after = seq[index + 1] if index + 1 < len(seq) else None
        if isinstance(after, str) and after.startswith(hpu.SOPA):
            if (reached := _templates_taking_a_mark_after(wtel)) is not None:
                io_found.update(id(tmpl) for tmpl in reached)


def _templates_taking_a_mark_after(tmpl):
    """Return tmpl and each template that ends a parameter of it that takes a mark.

    Return None if the mark stays apart, as _with_mark_after does.
    """
    tmpl_name = wtp.template_name(tmpl)
    if tmpl_name not in _PARAMS_TAKING_A_MARK_AFTER:
        raise ValueError(f"no parameter is named to take a mark after {tmpl!r}")
    if (param_names := _PARAMS_TAKING_A_MARK_AFTER[tmpl_name]) is None:
        return None
    reached = [tmpl]
    for param_name in param_names:
        param_val = wtp.template_param_val(tmpl, param_name)
        if not param_val:
            raise ValueError(
                f"parameter {param_name} is empty, to take a mark: {tmpl!r}"
            )
        if isinstance(last := param_val[-1], str):
            continue
        if (more := _templates_taking_a_mark_after(last)) is None:
            return None
        reached.extend(more)
    return reached


def find_fois_in_minirow_ep(foilers, mroge):
    # mroge: minirow or good ending
    if minirow := mroge.get("mroge-minirow"):
        return find_fois_in_wtseq(foilers, minirow.EP)
    assert mroge.get("mroge-good-ending")
    return []


def find_fois_by_forms_in_minirow_ep(foilers, mroge):
    """Find features of interest in column E, reading it by forms.

    Like find_fois_in_minirow_ep, but column E is read as with_attached_marks
    returns it.
    """
    # mroge: minirow or good ending
    if minirow := mroge.get("mroge-minirow"):
        return find_fois_in_wtseq(foilers, with_attached_marks(minirow.EP))
    assert mroge.get("mroge-good-ending")
    return []


def find_fois_in_wtseq(foilers, wtseq):
    """Find features of interest in Wikitext."""
    return _sum_map_find_in_wtel(foilers, _stack_make_empty(), wtseq)


def stack_summary(summary_dic, stack):
    """
    Summarize a stack by using a dict to pick one of the stack's elements.
    """
    index = summary_dic[stack]
    return stack[index] if index is not None else None


def find_fois_in_slh_word_arg_1(foilers, stack, tmpl):
    """arg 1 meaning the second arg, a list whose one and only element is a string"""
    new_stack = _stack_push(stack, wtp.template_name(tmpl))
    wtseq = wtp.template_element(tmpl, 2)
    return _sum_map_find_in_wtel(foilers, new_stack, wtseq)


def label_args_of_doc(foilers, stack, tmpl):
    """Label the arguments of the doc template."""
    # Also checked by check_mpplus, which py/subcommands/parse_ws_products.py runs on
    # every plus book it writes, raising on any error.  So in the mega a doc-note
    # template with the wrong number of arguments stops the run in the parse-ws step,
    # before the foi-features-of-interest step reaches this assert.  The assert's
    # message names the template, for plus JSON that reaches this function without
    # passing that check.  template_len counts the template's name as 1, hence the
    # subtraction.
    n_args = wtp.template_len(tmpl) - 1
    assert n_args == 2, (
        f"doc-note template {wtp.template_name(tmpl)!r} has {n_args} argument(s),"
        f" not 2: {tmpl!r}"
    )
    pnpv_dic = {
        "doc-target": wtp.template_param_val(tmpl, "1"),
        "doc-part-n": wtp.template_param_val(tmpl, "2"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_kq_triv(foilers, stack, tmpl):
    """Label the arguments of the מ:קו״כ-אם-2 template."""
    # New format: |pketiv|uketiv|pqere|מקורות=(optional)|סוג=(optional)
    # pketiv: pointed ketiv (param 1)
    # uketiv: unpointed ketiv (param 2)
    # pqere: pointed qere (param 3)
    # מקורות and סוג: optional named params
    assert wtp.template_len(tmpl) in (4, 5, 6)
    pnpv_dic = {
        "kq-triv-pketiv": wtp.template_param_val(tmpl, "1"),
        "kq-triv-pqere": wtp.template_param_val(tmpl, "3"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_scrdfftar(foilers, stack, tmpl):
    """Label the arguments of the scrdfftar (targeted scrdff) template."""
    pnpv_dic = {
        "scrdfftar-tar": wtp.template_param_val(tmpl, "1"),
        "scrdfftar-note": wtp.template_param_val(tmpl, "2"),
        "scrdfftar-starpos": wtp.template_param_val(tmpl, "3"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_ketiv_qere(foilers, stack, tmpl):
    """Label the arguments of the ketiv/qere template."""
    pnpv_dic = {
        "kq-ketiv": wtp.template_param_val(tmpl, "1"),
        "kq-qere": wtp.template_param_val(tmpl, "2"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


DUALCANT_ARG_COMBINED = "כפול-כפול"
DUALCANT_ARG_ALEF = "כפול-א/תחתון/פשוטה"
DUALCANT_ARG_BET = "כפול-ב/עליון/מדרשית"


def label_args_of_dualcant(foilers, stack, tmpl):
    """Label the arguments of the dual cantillation template."""
    pnpv_dic = {
        DUALCANT_ARG_COMBINED: wtp.template_param_val(tmpl, "כפול"),
        DUALCANT_ARG_ALEF: wtp.template_param_val(tmpl, "א"),
        DUALCANT_ARG_BET: wtp.template_param_val(tmpl, "ב"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def ignore(_foilers, _stack, _tmpl):
    """Handle a template by ignoring it."""
    return []


def fail_on_unexpected_template_in_plus(_foilers, stack, tmpl):
    """Fail fast for templates that are invalid in plus corpus data."""
    tmpl_name = wtp.template_name(tmpl)
    stack_str = "/".join(stack) if stack else "<root>"
    raise RuntimeError(
        f"Unexpected template {tmpl_name} in plus FOI traversal at stack {stack_str}"
    )


def all_branch_foilers(overrides):
    """Return a closed handler map for a whole-plus-dataset FOI inventory.

    Every current template is recognized by name.  Unless ``overrides`` gives a
    template a question-specific handler, every parameter is deliberately part
    of the inventory population.  A new template name therefore raises in
    ``_find_fois_in_wtel`` until the inventory classifies it.
    """
    handlers = {
        name: _foiler_for_all_named_params for name in tmpln.CURRENT_PLUS_TMPL_NAMES
    }
    # The silluq scaffold is position metadata, not another Scripture form.
    handlers[tmpln.SILLUQ_BEFORE_METEG] = _foiler_for_silluq_before_meteg
    handlers.update(overrides)
    return handlers


def _foiler_for_silluq_before_meteg(foilers, stack, tmpl):
    return _sum_map_find_in_wtel(foilers, stack, wtp.template_param_val(tmpl, "1"))


######################################################################
######################################################################


def _ignore_str(_stack, _tmpl):
    """Handle a string by ignoring it."""
    return []


def _find_fois_in_wtel(foilers, stack, wtel):
    if isinstance(wtel, str):
        str_handler = foilers.get(str) or _ignore_str
        return str_handler(stack, wtel)
    tmpln.validate_current_plus_template(wtel)
    tmpl_name = wtp.template_name(wtel)
    try:
        handler = foilers[tmpl_name]
    except KeyError as exc:
        raise RuntimeError(
            f"Unclassified template {tmpl_name!r} in plus FOI traversal"
        ) from exc
    return handler(foilers, stack, wtel)


def _find_fois_with_labelled_args(foilers, stack, pnpv_dic):
    # pnpv: param name and param value
    the_sum = []
    for param_name, param_val in pnpv_dic.items():
        new_stack = _stack_push(stack, param_name)
        the_sum += _sum_map_find_in_wtel(foilers, new_stack, param_val)
    return the_sum


def _stack_push(stack, obj):
    """Push an object (probably a string) on the stack."""
    return *stack, obj


def _stack_make_empty():
    return tuple()


def _foiler_for_all_named_params(foilers, stack, tmpl):
    """Inspect every parameter of one explicitly recognized dataset template."""
    tmpl_name = wtp.template_name(tmpl)
    params = tmpln.validate_current_plus_template(tmpl)
    new_stack = _stack_push(stack, tmpl_name)
    out = []
    for param_name in params:
        labelled_stack = _stack_push(new_stack, param_name)
        param_wtseq = wtp.template_param_val(tmpl, param_name)
        out += _sum_map_find_in_wtel(foilers, labelled_stack, param_wtseq)
    return out


def _sum_map_find_in_wtel(foilers, stack, wtseq):
    return sum_of_map((_find_fois_in_wtel, foilers, stack), wtseq)
