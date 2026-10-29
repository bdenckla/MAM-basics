import json
from os.path import dirname, relpath
from pathlib import Path

from vharfbuzz import Vharfbuzz

from mb_cmn import file_io
from taamey_d.qa import fails_filename
from taamey_d.qa.html_report import HTML_FOOTER, HTML_HEADER

FAIL, PASS, SKIP = "FAIL", "PASS", "SKIP"


def all_out_filename(reports_dir, font_fna, check_type, dotext):
    font_stem = font_fna.stem  # e.g. Taamey_D from font-m-TaD/Taamey_D.ttf
    html_basename = check_type + dotext  # e.g. collides.html
    return reports_dir / font_stem / html_basename
    # E.g. qa-out/Taamey_D/collides.html


def all_out_html_filename(reports_dir, font_fna, check_type):
    return all_out_filename(reports_dir, font_fna, check_type, ".html")


def all_out_json_filename(reports_dir, font_fna, check_type):
    return all_out_filename(reports_dir, font_fna, check_type, ".json")


def all_out_summary_html_filename(reports_dir, font_fna, check_type):
    return all_out_filename(reports_dir, font_fna, check_type + "_summary", ".html")
    # E.g. qa-out/Taamey_D/collides_summary.html


def _write_html_file(html_fp, title, font_rp, report_fn, ctx, all_failed_tcases):
    html_hdr = HTML_HEADER.format(title, Path(font_rp).as_posix())
    html_fp.write(html_hdr)
    report_fn(html_fp, ctx, all_failed_tcases)
    html_fp.write(HTML_FOOTER)


def _write_html_report(html_fna, title, report_fn, ctx, all_failed_tcases):
    font_rp = relpath(ctx["font_fna"], dirname(html_fna))
    file_io.with_tmp_openw(
        html_fna,
        {"newline": ""},
        lambda fp: _write_html_file(
            fp, title, font_rp, report_fn, ctx, all_failed_tcases
        ),
    )


def run_a_check_across_all_tcases(font_fna, progcb, checkobj, qadirs):
    ctx = dict(
        nontest_outputs={},
        font_fna=font_fna,
        progcb=progcb,
        checkobj=checkobj,
        qadirs=qadirs,
        vhb=Vharfbuzz(font_fna),
    )
    ########
    results, all_failed_tcases = run_a_check_across_all_tcases2(ctx)
    ########
    if checkobj.report_all_to_html:
        html_fna = all_out_html_filename(qadirs["outdir"], font_fna, checkobj.name)
        _write_html_report(
            html_fna, checkobj.name, checkobj.report_all_to_html, ctx, all_failed_tcases
        )
    if checkobj.report_summary_to_html:
        html_fna = all_out_summary_html_filename(
            qadirs["outdir"], font_fna, checkobj.name
        )
        _write_html_report(
            html_fna,
            f"{checkobj.name} summary",
            checkobj.report_summary_to_html,
            ctx,
            all_failed_tcases,
        )
    report_all_to_json = checkobj.report_all_to_json
    if report_all_to_json:
        json_fna = all_out_json_filename(qadirs["outdir"], font_fna, checkobj.name)
        file_io.with_tmp_openw(
            json_fna,
            {"newline": ""},
            lambda fp: report_all_to_json(fp, ctx, ctx["nontest_outputs"]),
        )
    return results


def prefix_progcb(progcb, prefix):
    return lambda s: progcb(f"{prefix}: {s}")


def _write_fails_file(fp, ctx, failed_tcases):
    report_fn = ctx["checkobj"].report
    report_records = list(map(report_fn, failed_tcases))
    json.dump(report_records, fp, indent=0, ensure_ascii=False)
    fp.write("\n")


def run_a_check_across_all_tcases2(ctx):
    checkobj = ctx["checkobj"]
    results = []
    tcases_fnas = sorted(
        ctx["qadirs"]["indir"].glob("*.testcases.json"), key=lambda path: path.name
    )
    if len(tcases_fnas) == 0:
        results.append((SKIP, "No JSON test case files found."))
        return results
    all_failed_tcases = []
    for tcases_fna in tcases_fnas:
        progcb = prefix_progcb(ctx["progcb"], tcases_fna)
        ctx2 = dict(ctx, tcases_fna=tcases_fna, progcb=progcb)
        ########
        rasot3 = run_a_check_across_all_tcases_in_a_file(ctx2)
        ########
        failed_tcases = []
        if rasot3 is not None:
            passfailskip, msg, failed_tcases = rasot3
            results.append((passfailskip, msg))
            all_failed_tcases.extend(failed_tcases)
        if checkobj.report:
            fails_fna = fails_filename.fails_filename(
                ctx["qadirs"]["outdir"], ctx["font_fna"], checkobj.name, tcases_fna
            )
            file_io.with_tmp_openw(
                fails_fna,
                {"newline": ""},
                lambda fp: _write_fails_file(fp, ctx, failed_tcases),
            )
    if len(results) == 0:
        results.append(
            (
                SKIP,
                f"{tcases_fna}: JSON test case files were found, but no test cases were run.",
            )
        )
    return results, all_failed_tcases


def report_progress(progstate, len_tcases, progcb):
    if progstate is None:
        newprogstate = 1
    else:
        newprogstate = progstate + 1
    if newprogstate % 2000 == 0:
        progcb(f"processing test case {newprogstate} of {len_tcases}")
    return newprogstate


def run_a_check_across_all_tcases_in_a_file(ctx2):
    font_fna, checkobj, tcases_fna = (
        ctx2["font_fna"],
        ctx2["checkobj"],
        ctx2["tcases_fna"],
    )
    failed_tcases = []
    gcnt_failmsg, cfg, tcases = get_cfg_n_tcases(tcases_fna)
    if gcnt_failmsg:
        return FAIL, gcnt_failmsg, failed_tcases
    setupfn = checkobj.setup
    extra_data = setupfn(font_fna, cfg) if setupfn else None
    some_tcases_ran = False
    progstate = None
    ctx3 = dict(
        font_fna=ctx2["font_fna"],
        vhb=ctx2["vhb"],
        nontest_outputs=ctx2["nontest_outputs"],
        cfg=cfg,
        failed_tcases=failed_tcases,
        extra_data=extra_data,
    )
    for tcase in tcases:
        progstate = report_progress(progstate, len(tcases), ctx2["progcb"])
        ########
        checkobj.run(ctx3, tcase)
        ########
        some_tcases_ran = True
    if failed_tcases:
        return FAIL, "", failed_tcases
    if some_tcases_ran:
        return PASS, f"{tcases_fna}: No failures detected", failed_tcases
    return None


def get_cfg_n_tcases(tcases_fna):
    try:
        # fc: file contents
        tcases_fc = json.loads(tcases_fna.read_text(encoding="utf-8"))
    except Exception as e:
        msg = f"{tcases_fna}: Invalid JSON: {e}."
        return msg, None, None
    try:
        tcases = tcases_fc["testcases"]
    except KeyError:
        msg = f"{tcases_fna}: «testcases» key missing from top-level dict."
        return msg, None, None
    for tcase in tcases:
        if "input" not in tcase:
            msg = f"{tcases_fna}: «input» key is missing from test case dict."
            return msg, None, None
    return None, get_cfg(tcases_fna, tcases_fc), tcases


def get_cfg(tcases_fna, tcases_fc):
    raw_cfg = tcases_fc.get("configuration")
    if raw_cfg is None:
        return {}
    if isinstance(raw_cfg, str):
        cfg_path = tcases_fna.parent / raw_cfg
        with open(cfg_path, encoding="utf-8") as cfg_fp:
            return json.load(cfg_fp)
    assert isinstance(raw_cfg, dict)
    return raw_cfg
