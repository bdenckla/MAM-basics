import mb_cmn.my_utils as my_utils

_METADATA = {
    "tocsec-id-131": {
        "tsm-filename": "yeivin_itm-131_135.html",
        "tsm-range": (131, 135),
    },
    "tocsec-id-192": {
        "tsm-filename": "yeivin_itm-192_206.html",
        "tsm-range": (192, 206),
    },
    "tocsec-id-207": {
        "tsm-filename": "yeivin_itm-207_285.html",
        "tsm-range": (207, 285),
    },
    "tocsec-id-286": {
        "tsm-filename": "yeivin_itm-286_289.html",
        "tsm-range": (286, 289),
    },
    "tocsec-id-290": {
        "tsm-filename": "yeivin_itm-290_306.html",
        "tsm-range": (290, 306),
    },
    "tocsec-id-307": {
        "tsm-filename": "yeivin_itm-307_310.html",
        "tsm-range": (307, 310),
    },
    "tocsec-id-311": {
        "tsm-filename": "yeivin_itm-311_317.html",
        "tsm-range": (311, 317),
    },
    "tocsec-id-318": {
        "tsm-filename": "yeivin_itm-318_344.html",
        "tsm-range": (318, 344),
    },
    "tocsec-id-345": {
        "tsm-filename": "yeivin_itm-345_357.html",
        "tsm-range": (345, 357),
    },
    "tocsec-id-358": {
        "tsm-filename": "yeivin_itm-358_374.html",
        "tsm-range": (358, 374),
    },
    "tocsec-id-375": {
        "tsm-filename": "yeivin_itm-375_375.html",
        "tsm-range": (375, 375),
    },
    "tocsec-id-376": {
        "tsm-filename": "yeivin_itm-376_393.html",
        "tsm-range": (376, 393),
    },
    "tocsec-id-394": {
        "tsm-filename": "yeivin_itm-394_416.html",
        "tsm-range": (394, 416),
    },
}


def filename_for_secnum(secnum):
    for metval in _METADATA.values():
        if _in_range(metval, secnum):
            return metval["tsm-filename"]
    assert False


def filename_for_tsid(tsid):
    return _METADATA[tsid]["tsm-filename"]


def all_in_range(tsid, secnums):
    metval = _METADATA[tsid]
    return all(my_utils.sl_map((_in_range, metval), secnums))


def _in_range(metval, secnum):
    the_range = metval["tsm-range"]
    return the_range[0] <= secnum <= the_range[1]
