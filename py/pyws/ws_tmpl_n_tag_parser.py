"""Exports parse"""

from pyws import ws_tmpl_parser as wttmpl_parser
from pyws import ws_abtag_parser as abtag_parser
from pyws import ws_unparse


def parse(string):
    """Chain the Wikitext template and Wikitext abtag parsers"""
    # wtseq: sequence of wtels
    # wtels: Wikitext elements
    assert not string.endswith("|")
    wtseq = abtag_parser.parse(wttmpl_parser.parse(string))
    assert string == ws_unparse.unparse(wtseq)
    return wtseq
