"""Exports main"""

import sys
import xml.etree.ElementTree

import mb_cmn.file_io as my_open
import uxlc_misc.my_uxlc_changes as my_uxlc_changes
import uxlc_changes.uxlc_bhl_appendix_a as uxlc_bhl_appendix_a
import uxlc_changes.uxlc_change_prep as prep
import uxlc_changes.uxlc_change_sanity as sanity
import uxlc_changes.uxlc_changes_loc as changes_loc
import uxlc_changes.uxlc_misc_path as uxlc_misc_path
import uxlc_changes.xml_node as xml_node
import uxlc_paths


def _listify(list_or_nonlist):
    if isinstance(list_or_nonlist, list):
        return list_or_nonlist
    return [list_or_nonlist]


def _get_changes(changeset):
    date = changeset["date"]
    if "change" not in changeset:
        # Sometimes a changeset just has a date, because it is an empty
        # placeholder, to be filled in with changes later.
        return []
    changes = _listify(changeset["change"])
    sanity_path = uxlc_paths.out_uxlc_misc_dir() / "sanity_problems.json"
    sanity.check(date, changes, sanity_path)
    return [prep.date_qualify_and_reformat(date, c) for c in changes]


def _get_lines(change):
    return [change["description"]] + change["notes"]


def _dump_txt_write_callback(lines, out_fp):
    out_fp.write("\n".join(lines))


def _dump_txt(changes, path):
    list_of_lists = list(map(_get_lines, changes))
    lines = sum(list_of_lists, [])
    my_open.with_tmp_openw(path, {"newline": ""}, _dump_txt_write_callback, lines)


def _do_one_changes_file(bhla, filename):
    release_date, changes = _do_one_changes_file_core(filename)
    changes = [{"release": release_date, **c} for c in changes]
    changes = [{**c, "bhla": _join_bhla(bhla, c)} for c in changes]
    return changes


def _do_one_changes_file_core(filename):
    """
    Convert a Changes file to JSON format. (E.g., for import into Excel).
    """
    xml_input_path = uxlc_misc_path.get(filename)
    tree = xml.etree.ElementTree.parse(xml_input_path)
    root = tree.getroot()
    root_dic = xml_node.to_dic(root)
    # release_major_dot_minor = root_dic['target']  # E.g. 'UXLC 1.2'
    release_date = root_dic["filedate"]
    changesets_list = _listify(root_dic["dates"]["date"])
    list_of_lists = list(map(_get_changes, changesets_list))
    changes = sum(list_of_lists, [])
    basename = filename.removesuffix(".xml")
    assert basename != filename
    txt_output_path = uxlc_paths.out_uxlc_misc_dir() / f"{basename}.txt"
    _dump_txt(changes, txt_output_path)
    return release_date, changes


def _join_bhla(bhla, change_record):
    citation = change_record["citation"]
    if citation in bhla:
        return True
    cite_sod = citation.split(".")  # sod: split on dot
    return cite_sod[0] in bhla


def _get_all_changes():
    bhla = uxlc_bhl_appendix_a.read()
    all_changes = []
    for filename in my_uxlc_changes.FILENAMES:
        changes = _do_one_changes_file(bhla, filename)
        all_changes.extend(changes)
    return all_changes


def main():
    """
    Convert various Changes files to JSON format.
    """
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    changes = _get_all_changes()
    check_results_f = changes_loc.check(changes)
    #
    json_output_path1 = uxlc_paths.canonical_all_changes_path()
    my_open.json_dump_to_file_path(changes, json_output_path1)
    json_output_path2 = uxlc_paths.out_uxlc_misc_dir() / "all_changes_loc_checks.json"
    my_open.json_dump_to_file_path(check_results_f, json_output_path2)


if __name__ == "__main__":
    main()
