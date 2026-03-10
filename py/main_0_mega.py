""" Exports main """

import argparse
import sys

import main_diff_gogo
import main_diff_wsgo
import main_explicit_xataf

# main_download_mam_fr_google.py
# main_download_mam_fr_sefaria.py
# main_download_mam_fr_wikisource.py
import main_gen_misc_authored_english_documents
import main_decnreub
import main_foi_features_of_interest
import main_multimark
import main_parse_go
import main_tmpl_survey
import main_parse_ws
import main_ws_bot_proto
import main_wordlist
import main_mam_with_doc
import main_mam_xml
import main_mam4sef
import main_mam4ajf
import main_osis
import main_mam_xml_copy_py_files
import main_mgc_match_go_changes_to_gogo_diffs

#
#
#
#
#
#


_STEPS = [
    (
        main_parse_go,
        "mam_parsed must come before mam_xml, mam_tmpl_survey, & many others",
    ),
    (main_foi_features_of_interest, None),
    # We run "features of interest" early since it
    # provides information about any malformed Unicode.
    # On later "main" functions, such malformed Unicode will cause
    # asserts that provide little information.
    (main_mam_with_doc, None),
    (main_tmpl_survey, "must come after mam_parsed"),
    (main_mam_xml, "must come after mam_parsed"),
    # mam_xml must come before mam4sef, mam4ajf, & mam_osis
    (main_mam4sef, "must come after mam_xml"),
    (main_mam4ajf, "must come after mam_xml"),
    (main_osis, "must come after mam_xml"),
    (main_decnreub, None),
    (main_multimark, None),
    (main_wordlist, None),
    (main_explicit_xataf, None),
    (main_diff_wsgo, "relies on download of ws"),
    (main_parse_ws, "relies on download of ws"),
    (main_ws_bot_proto, "relies on download of ws"),
    (main_diff_gogo, None),
    (main_gen_misc_authored_english_documents, None),
    (main_mam_xml_copy_py_files, None),
    (main_mgc_match_go_changes_to_gogo_diffs, None),
]

_STEP_NAMES = [mod.__name__ for mod, _comment in _STEPS]


def main():
    """Run various mains"""
    parser = argparse.ArgumentParser(description="Run the mega pipeline")
    parser.add_argument(
        "--resume-from",
        choices=_STEP_NAMES,
        metavar="STEP",
        help="Skip steps before STEP and resume from there. Choices: "
        + ", ".join(_STEP_NAMES),
    )
    args, remaining = parser.parse_known_args()
    sys.argv = [sys.argv[0]] + remaining
    resuming = args.resume_from is not None
    for mod, _comment in _STEPS:
        if resuming:
            if mod.__name__ == args.resume_from:
                resuming = False
            else:
                print(f"Skipping {mod.__name__}")
                continue
        mod.main()
    #
    # Download of ws (Wikisource) can be accomplished by running:
    #    main_download_mam_fr_wikisource.py
    # It must be run in a venv like this:
    #    ./py/venv/Scripts/python.exe ./py/main_download_mam_fr_wikisource.py


if __name__ == "__main__":
    main()
