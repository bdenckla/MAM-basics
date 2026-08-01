"""WLC JSON and Unicode generation entrypoint."""

from wlc_cmn.utf8_io import force_utf8_io
import wlc_paths
import py_wlc_json_and_unicode.wlc_write_to_json as wlc_write_to_json
import py_wlc_json_and_unicode.wlc_compare_mdc_with_uxlc as mx
import py_wlc_json_and_unicode.wlc_compare_mdc_with_mdc as mm
import py_wlc_json_and_unicode.wlc_compare_uni_with_uni as uu


def _mx_out_path(wlc_id):
    name = f"diff_mx_{wlc_id}_uxlc.json"
    return f"{_root_for(name)}/out/{name}"


def _mm_out_path(ww_diff_ids):
    wlc_ida, wlc_idb = ww_diff_ids
    name = f"diff_mm_{wlc_ida}_{wlc_idb}.json"
    return f"{_root_for(name)}/out/{name}"


def _uu_out_path(ww_diff_ids):
    wlc_ida, wlc_idb = ww_diff_ids
    name = f"diff_uu_{wlc_ida}_{wlc_idb}.json"
    return f"{_root_for(name)}/out/{name}"


def _out_path(wlc_id, suffix):
    return f"{_root_for(wlc_id)}/out/{wlc_id}{suffix}"


def _in_path(wlc_id):
    return f"{_root_for(wlc_id)}/in/{wlc_id}"


def almost_main():
    """Generate WLC JSON/Unicode outputs and related Unicode diffs."""
    path_info = _in_path, _out_path
    p321uni = wlc_write_to_json.write(path_info, "2025-03-21-uni")
    p321mdc, p321mdcu = wlc_write_to_json.write(path_info, "2025-03-21-mdc")
    p420mdc, _u = wlc_write_to_json.write(path_info, "wlc420")
    p422mdc, _u = wlc_write_to_json.write(path_info, "wlc422")
    uu.compare(p321mdcu, p321uni, _uu_out_path)
    mx.compare(p420mdc, _UXLC_BOOKS_DIR, _mx_out_path)
    mm.compare(p420mdc, p422mdc, _mm_out_path)
    mm.compare(p420mdc, p321mdc, _mm_out_path)


# The dated 2025-03-21-* sources and their outputs stay in the private repo; the
# wlc420/wlc422 trees, the UXLC source, and their diffs live in the public repo
# (this one). _root_for picks the right one per in/out item by name, mirroring how
# the artifacts were partitioned between the repos.
#
# BOTH roots are absolute, and neither is the cwd.  _PUBLIC was "." until 2026-08-01,
# which made every path below relative to wherever the process happened to be started;
# run from another repo that also has in/ and out/, it wrote there instead of failing.
_PUBLIC = str(wlc_paths.wlc_data_root())
# The private repo is a cross-repo sibling; route it through the repo-anchored,
# env-overridable resolver (fixes worktree breakage and the old cwd-relative
# fragility).
_PRIVATE = str(wlc_paths.wlc_utils_private_dir())


def _root_for(name):
    return _PRIVATE if "2025-03-21" in name else _PUBLIC


_UXLC_BOOKS_DIR = f"{_PUBLIC}/in/Tanach-26.0--UXLC-1.0--2020-04-01/Books"


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
