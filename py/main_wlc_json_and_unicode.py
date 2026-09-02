"""Generate the current public WLC JSON and Unicode artifacts.

The private 2025-03-21 inputs and derived outputs are deliberately outside this
pipeline as of 2026-09-02.  MAM-basics no longer reads or regenerates them, so
those preserved outputs may become stale.  Ben accepted that cost because
severing the runtime dependency on ``MAM-private/wlc-utils-private`` is worth
the loss of automatic refreshes.
"""

from wlc_cmn.utf8_io import force_utf8_io
from mb_cmn import paths
import py_wlc_json_and_unicode.wlc_write_to_json as wlc_write_to_json
import py_wlc_json_and_unicode.wlc_compare_mdc_with_uxlc as mx
import py_wlc_json_and_unicode.wlc_compare_mdc_with_mdc as mm


def _mx_out_path(wlc_id):
    name = f"diff_mx_{wlc_id}_uxlc.json"
    return f"{_PUBLIC}/out/{name}"


def _mm_out_path(ww_diff_ids):
    wlc_ida, wlc_idb = ww_diff_ids
    name = f"diff_mm_{wlc_ida}_{wlc_idb}.json"
    return f"{_PUBLIC}/out/{name}"


def _out_path(wlc_id, suffix):
    return f"{_PUBLIC}/out/{wlc_id}{suffix}"


def _in_path(wlc_id):
    return f"{_PUBLIC}/in/{wlc_id}"


def almost_main():
    """Generate WLC JSON/Unicode outputs and related Unicode diffs."""
    path_info = _in_path, _out_path
    p420mdc, _u = wlc_write_to_json.write(path_info, "wlc420")
    p422mdc, _u = wlc_write_to_json.write(path_info, "wlc422")
    mx.compare(p420mdc, _UXLC_BOOKS_DIR, _mx_out_path)
    mm.compare(p420mdc, p422mdc, _mm_out_path)


# The root is absolute rather than the cwd.  _PUBLIC was "." until 2026-08-01,
# which made every path below relative to wherever the process happened to be started;
# run from another repo that also has in/ and out/, it wrote there instead of failing.
_PUBLIC = str(paths.repo_root())


_UXLC_BOOKS_DIR = f"{_PUBLIC}/in/Tanach-26.0--UXLC-1.0--2020-04-01/Books"


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
