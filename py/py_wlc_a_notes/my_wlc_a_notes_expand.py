"""Exports expand."""


def expand(io_records):
    """
    Add fields including uxlc-change-proposal-sequential and 'at issue English'.
    """
    ucp_count = 0
    ucp_dic = {}
    for record in io_records:
        _add_at_issue_english(record)
        ucp = record["uxlc-change-proposal"]
        if isinstance(ucp, int):
            assert ucp not in ucp_dic
            ucp_dic[ucp] = True
            ucp_count += 1
            record["uxlc-change-proposal-sequential"] = ucp_count


def _add_at_issue_english(io_record):
    summ_in = io_record["summary"]
    atiss_in = io_record["at issue"]
    summ_out = _SUMMARY_MAP[summ_in]
    atiss_key = summ_in, atiss_in
    atiss_out = _AT_ISSUE_MAP[atiss_key]
    io_record["at issue English"] = f"{summ_out}{atiss_out}"


_AT_ISSUE_MAP = {
    ("אֻ/אוּ", "וּ"): "",
    ("+mqf", "־"): "",
    ("הּ", "הּ"): "",
    ("?", "?"): "unclear",
    #
    ("+dg", "בּ"): " to bet",
    ("+dg", "וָּ"): " to vav-qamats",
    ("+dg", "פּ"): " to pe",
    ("+dg", "יּ"): " to yod",
    ("+dg", "דּ"): " to dalet",
    ("+dg", "כּ"): " to kaf",
    ("+dg", "טּ"): " to tet",
    ("+dg", "לּ"): " to lamed",
    ("+dg", "צּ"): " to tsadi",
    ("+shrq dt", "וּ"): " to the initial vav",
    #
    ("+ḥlm dt", "וֹ"): " to vav",
    ("+shva", "ךְ"): " to kaf sofit",
    ("+shva", "נְ"): " to nun",
    #
    ("עֲ/עַ", "עַ"): " under ayin",
    #
    ("-dg", "מ"): " from mem",
}


_SUMMARY_MAP = {
    "אֻ/אוּ": "changed a qubuts to a shuruq",
    "+mqf": "added a maqaf",
    "+dg": "added a dagesh",
    "-dg": "removed a dagesh",
    "הּ": "added a mapiq to he",
    "+shrq dt": "added a shuruq dot",
    "+ḥlm dt": "added a ḥolam malei dot",
    "+shva": "added a sheva",
    "עֲ/עַ": "changed a ḥataf pataḥ to a pataḥ",
    "?": "",
}
