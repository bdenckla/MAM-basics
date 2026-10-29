from os.path import basename

from taamey_d.qa import shaping_diff
from taamey_d.qa import check_helpers as hlp
from taamey_d.qa.html_report import report_to_html, span_tf


def _font_group_names(font_bna, cfg):
    if groups_for_all_fonts := cfg.get("font_groups"):
        if groups_for_this_font := groups_for_all_fonts.get(font_bna):
            return tuple(groups_for_this_font)
    return tuple()


def _get_expected(font_fna, cfg, tcase):
    if expected_dic := tcase.get("expected"):
        font_bna = basename(font_fna)
        keys = (font_bna,) + _font_group_names(font_bna, cfg)
        for key in keys:
            if resolved_val := expected_dic.get(key):
                return resolved_val
    return "dummy_expectation"


def run_regression(ctx3, tcase):
    cfg, vhb, font_fna, failed_tcases = (
        ctx3["cfg"],
        ctx3["vhb"],
        ctx3["font_fna"],
        ctx3["failed_tcases"],
    )
    shparams = hlp.get_shaping_parameters(tcase, cfg)
    tinput_str = hlp.tcase_input_str(tcase)
    output_buf = vhb.shape(tinput_str, shparams)
    actual = vhb.serialize_buf(output_buf)
    expected = _get_expected(font_fna, cfg, tcase)
    if actual != expected:
        failed_tcases.append((tcase, expected, output_buf, actual))


def report_regr_fail(failed_tcase):
    tcase, expected, _, actual = failed_tcase  # _ is output_buf
    tinput = tcase["input"]
    return dict(input=tinput, expected=expected, actual=actual)


def _report_all_regr_fails_hdr(html_file, vhb, fails, major_fails, max_to_show):
    nfails = len(fails)
    nmajors = len(major_fails)
    clip_warning = "the majors"
    if nmajors > max_to_show:
        clip_warning = f"the first {max_to_show} majors"
    msg1 = f"{nfails} regression(s) ({nmajors} major) found while shaping; showing only {clip_warning}."
    report_to_html(html_file, vhb, msg1, type="header")


def _glyph_names_not_in_font(vhb, serialization):
    """The glyph names in a serialization that this font does not have.

    An expectation recorded before a glyph rename names glyphs the font no longer
    has. vharfbuzz's buf_from_string gives such a glyph a codepoint of None, and
    both serialize_buf and buf_to_svg then die on that None, so the report has to
    spot the absent name itself rather than hand the buffer on and crash.
    """
    hbfont = vhb.hbfont
    names = (item.partition("=")[0] for item in serialization.split("|"))
    return tuple(name for name in names if hbfont.glyph_from_string(name) is None)


def _buf2_and_note(vhb, expected):
    """A buffer for the expected serialization, or None plus a note saying why.

    So a note also tells the caller that a real expectation went unrendered, which
    is when the caller wants to show that expectation as text instead. A test case
    with no expectation recorded, whose expectation is the "dummy_expectation"
    placeholder, gets no buffer and no note, and so is reported as it always was.
    """
    if "=" not in expected:
        return None, ""
    if names_not_in_font := _glyph_names_not_in_font(vhb, expected):
        note = (
            " The font does not have these glyphs the expectation names, so the"
            f" expectation is shown as text and not rendered: {', '.join(names_not_in_font)}"
        )
        return None, note
    return vhb.buf_from_string(expected), ""


def report_all_regr_fails(html_fp, ctx, failed_tcases):
    major_fails = []
    for failed_tcase in failed_tcases:
        tcase, expected, output_buf, actual = failed_tcase
        major = shaping_diff.major(actual, expected)
        if major:
            major_fails.append(failed_tcase)
    max_to_show = 500
    html_file, vhb = html_fp, ctx["vhb"]
    _report_all_regr_fails_hdr(html_file, vhb, failed_tcases, major_fails, max_to_show)
    for failed_tcase in major_fails[:max_to_show]:
        tcase, expected, output_buf, actual = failed_tcase
        buf2, note = _buf2_and_note(vhb, expected)
        extra_data = {k: tcase[k] for k in hlp.SHPARAM_KEYS if k in tcase}
        extra_data_str = (f" {extra_data}" if extra_data else "") + note
        tinput_str = hlp.tcase_input_str(tcase)
        report_to_html(
            html_file,
            vhb,
            "Shaping did not match",
            text=tinput_str,
            buf1=output_buf,
            buf2=buf2,
            extra_data=extra_data_str,
            expected_str=expected if note else None,
        )


def checkobj_for_regr(font_fna):
    return hlp.CheckObj(
        "regression", "regr", run_regression, report_regr_fail, report_all_regr_fails
    )
