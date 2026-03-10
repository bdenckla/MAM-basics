"""Write a survey result dict to an xlsx spreadsheet."""

import openpyxl


def _write_list_of_dicts(wsheet, records):
    if not records:
        return
    headers = list(records[0].keys())
    wsheet.append(headers)
    for rec in records:
        wsheet.append([rec[h] for h in headers])


def _add_sheet(wbook, name, first_ref):
    if first_ref[0]:
        wsheet = wbook.active
        wsheet.title = name
        first_ref[0] = False
    else:
        wsheet = wbook.create_sheet(title=name)
    return wsheet


def write_xlsx(data, out_path):
    """Write survey data (a dict of sheet_name -> value) to an xlsx file.

    Values can be:
    - a list of dicts (one sheet with headers from dict keys)
    - a dict of {sub_name: list-of-dicts} (one sheet per sub_name)
    - a string (one sheet with the string in cell A1)
    """
    wbook = openpyxl.Workbook()
    first_ref = [True]
    for name, value in data.items():
        if isinstance(value, str):
            wsheet = _add_sheet(wbook, name, first_ref)
            wsheet.append([value])
        elif isinstance(value, dict):
            for sub_name, sub_value in value.items():
                sheet_name = f"{name}_{sub_name}"
                wsheet = _add_sheet(wbook, sheet_name, first_ref)
                _write_list_of_dicts(wsheet, sub_value)
        else:
            wsheet = _add_sheet(wbook, name, first_ref)
            _write_list_of_dicts(wsheet, value)
    wbook.save(out_path)
