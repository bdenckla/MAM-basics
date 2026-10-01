from itertools import starmap
import yeivin_itm.helpers as hlp
import py_html.legacy_html as aht_html


def defn_table(type_defn_pairs):
    type_defn_rows = list(starmap(_type_defn_outside_of_type_column, type_defn_pairs))
    intro = aht_html.para(["Types used in the table above:"])
    table_proper = hlp.table_std(type_defn_rows, coldirs=["rtl", "ltr"])
    return intro, table_proper


def type_defn_in_type_column(inner, defn_items):
    return _type_defn(inner, defn_items, in_type_column=True)


def str_cond(as_rich_text, as_plain_text=""):
    return lambda as_str: as_plain_text if as_str else as_rich_text


def _type_defn_outside_of_type_column(inner, defn_items):
    return _type_defn(inner, defn_items, in_type_column=False)


def _type_defn(inner, defn_items, in_type_column):
    defn = aht_html.maybe_join(as_str=in_type_column, str_or_fns=defn_items)
    if in_type_column:
        return aht_html.span(inner, {"title": defn})
    return [inner, defn]
