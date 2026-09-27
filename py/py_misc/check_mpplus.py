"""Checks on MAM-parsed-plus output."""

import json

from mb_cmn import ws_tmpl2
from mb_cmn import my_utils
from mb_cmn import uni_denorm as ud


def check_mpplus(plus_paths):
    """Validate all plus JSON files, accumulating errors.

    Returns a list of (path, error) tuples. Empty means all checks passed.
    """
    all_errors = []
    for plus_path in plus_paths:
        with open(plus_path, encoding="utf-8") as fp:
            data = json.load(fp)
        errors = []
        _validate(data, errors)
        for error in errors:
            all_errors.append((plus_path, error))
    return all_errors


def _validate_dict(dic, errors):
    _check_doc_tmpl(dic, errors)
    _check_note_link_tmpl(dic, errors)
    for key, val in dic.items():
        _validate(key, errors)
        _validate(val, errors)


def _check_doc_tmpl(dic, errors):
    """
    Check נוסח template: must have exactly 2 args, one of which has key "2".
    The intention is to catch failure to use the "2=" prefix when needed, e.g.
    The intention is to catch something like {{nusx|targ|a=b}}.
    (Should be {{nusx|targ|2=a=b}}.)
    Note that this does not catch failure to use the "2=" prefix when it is not needed,
    i.e. this does not catch mere style violations.
    (Our standard style is to use the "2=" prefix regardless of whether it is needed.)
    """
    if not ws_tmpl2.is_doc_template(dic):
        return
    if ws_tmpl2.template_len(dic) != 3:  # tmpl_len counts the tmpl_name as 1
        errors.append(("doc-tmpl-arg-count", dic))
        return
    if "2" not in ws_tmpl2.template_param_keys(dic):
        errors.append(("doc-tmpl-2nd-arg", dic))


# Whether each note-link template's target, its first parameter, is a URL.
_NOTE_LINK_TARGET_IS_URL = {"מ:קישור בהערה": True, "מ:קישור פנימי בהערה": False}


def _check_note_link_tmpl(dic, errors):
    """
    Check a note-link template's target: מ:קישור בהערה links to a URL, and
    מ:קישור פנימי בהערה to a Wikisource page. Until its bot edit of 2026-09-27,
    Leviticus 10:6 gave the internal-link template an archive.org URL, so
    MAM-with-doc linked to https://he.wikisource.org/wiki/https://archive.org/...
    """
    name = ws_tmpl2.template_name_if_is_template(dic)
    if name not in _NOTE_LINK_TARGET_IS_URL:
        return
    target = my_utils.first_and_only_and_str(ws_tmpl2.template_param_val(dic, "1"))
    if target.startswith(("http://", "https://")) != _NOTE_LINK_TARGET_IS_URL[name]:
        errors.append(("note-link-target", dic))


def _validate_listlike(listlike, errors):
    for element in listlike:
        _validate(element, errors)


def _validate_str(string, errors):
    if not ud.has_std_mark_order(string):
        errors.append(("mark-order", string))


def _validate(obj, errors):
    if obj is None:
        return
    if isinstance(obj, int):
        return
    validate_fns = {
        dict: _validate_dict,
        tuple: _validate_listlike,
        list: _validate_listlike,
        str: _validate_str,
    }
    # mtypes: types that obj is an instance of, from the set of types that are
    # keys in validate_fns
    mtypes = tuple(filter(lambda typ: isinstance(obj, typ), validate_fns))
    validate_fns[my_utils.first_and_only(mtypes)](obj, errors)
