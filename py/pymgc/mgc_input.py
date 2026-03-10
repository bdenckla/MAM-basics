""" Exports get_diffs_and_cles """

import csv
import json
import collections
from pymgc import mgc_add_heb_bcv as add_heb_bcv
from pymgc import mgc_add_eng_bcv as add_eng_bcv


def get_diffs_and_cles(diffs_path):
    """Get Go-Go diffs and change log entries"""
    cles_path = "in/mam-go-2023-04-06/Miqra_al_pi_ha-Masorah - שינויים changes.csv"
    #
    with open(diffs_path, encoding="utf-8") as ggds_json_in_fp:
        diffs = json.load(ggds_json_in_fp)
    with open(cles_path, encoding="utf-8") as csv_in_fp:
        cle_fields = "when,who,where,what,what_x_heb,what_y_heb"
        CleType = collections.namedtuple("ChangeLogEntry", cle_fields)
        cles = list(map(CleType._make, csv.reader(csv_in_fp)))
    del cles[0]  # remove header row
    #
    diffs = list(map(add_heb_bcv.add_heb_bcv, diffs))
    cles = list(map(add_eng_bcv.add_eng_bcv, cles))
    cles = list(map(_massage_date_format, cles))
    cles = list(filter(_date_in_desired_range, cles))
    cles = list(filter(_not_in_misc_excludes, cles))
    #
    return diffs, cles


def _massage_date_format(cle):
    day_month_year = cle["when"].split("/")
    year_month_day = reversed(day_month_year)
    when_ymd = "-".join(year_month_day)
    return dict(cle, when=when_ymd)


def _date_in_desired_range(cle):
    return "2021-12-07" <= cle["when"] <= "2023-04-06"


def _not_in_misc_excludes(cle):
    misc_excludes = (
        "rm parens around x to match Wikisource",
        "add missing doc. note starter x",
        "separate args of נוסח using vertical bar ( | )",
        "Corrected documentation note.",
        ("Stopped using שני ... אחת template to implement x. " "(It is not needed.)"),
        "Restored the accidentally-removed letter ו (vav) from the qeri x.",
        (
            "Accidentally removed the letter ו (vav) from the qeri x. "
            "This was the result of applying auto-edits from Wikisource "
            "and Wikisource lacking the change that added the vav."
        ),
    )
    return cle["what"] not in misc_excludes
