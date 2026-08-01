"""Exports write."""

import py_wlc_json_and_unicode.wlc_read_and_parse_mdc as rp_mdc
import py_wlc_json_and_unicode.wlc_read_and_parse_uni as rp_uni
import py_wlc_json_and_unicode.wlc_kqparse as kqparse
import py_wlc_json_and_unicode.wlc_foi_utils as foi_utils
import py_wlc_json_and_unicode.wlc_smallish_files as smallish_files
import py_wlc_json_and_unicode.wlc_convert_mdc_to_uni as mu
import py_wlc_json_and_unicode.wlc_release_info as ri


def write(path_info, wlc_id):
    in_path_fn, out_path_fn = path_info
    in_file_filename = ri.RELEASE_INFO["ri-filenames"][wlc_id]
    format = ri.RELEASE_INFO["ri-formats"][wlc_id]
    in_path = in_path_fn(wlc_id)
    in_file_path = f"{in_path}/{in_file_filename}"
    read_and_parse_fn = _READ_AND_PARSE_FNS[format]
    parsed = read_and_parse_fn(in_file_path)
    parsed = {"id": wlc_id, **parsed}
    smallish_files.write(out_path_fn(wlc_id, ""), parsed)
    foi_utils.write(out_path_fn(wlc_id, ""), wlc_id, parsed)
    _write_kq(path_info, wlc_id, parsed)
    if ri.encoding_is_mdc(wlc_id):
        parsed_u = mu.convert_p_mdc_to_p_uni(parsed)
        smallish_files.write(out_path_fn(wlc_id, "-u"), parsed_u)
        return parsed, parsed_u
    return parsed


def _write_kq(path_info, wlc_id, parsed):
    _in_path_fn, out_path_fn = path_info
    parsed_kq = kqparse.kqparse(parsed)
    smallish_files.write(out_path_fn(wlc_id, "-kq"), parsed_kq)
    foi_utils.kqwrite(out_path_fn(wlc_id, "-kq"), wlc_id, parsed_kq)
    if ri.encoding_is_mdc(wlc_id):
        parsed_kq_u = mu.convert_p_mdc_to_p_uni(parsed_kq)
        smallish_files.write(out_path_fn(wlc_id, "-kq-u"), parsed_kq_u)


_READ_AND_PARSE_FNS = {
    "fmt-M-C": rp_mdc.read_and_parse,
    "fmt-Uni": rp_uni.read_and_parse,
}
