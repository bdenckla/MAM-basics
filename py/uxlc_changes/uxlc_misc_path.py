"""Exports get"""

import uxlc_paths


def get(filename):
    """
    Returns basename.xml in UXLC-misc-fixed if it exists there,
    otherwise returns basename.xml in UXLC-misc.
    """
    path_fixed = uxlc_paths.uxlc_misc_fixed_dir() / filename
    if path_fixed.exists():
        return path_fixed
    return uxlc_paths.uxlc_misc_dir() / filename
