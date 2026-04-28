'use strict'

function main() {
  selfTest()

  const edits = getShVa('AutoEdits')
  const edits_nar = getEditsNotAlreadyRun(edits.values)
  const edits_by_sheet = groupEditsBySheet(edits_nar)

  const results_by_sheet = edits_by_sheet.map((e) => calcEditsForSheet(e))

  results_by_sheet.forEach((r) => writeSheetEdits(edits.sheet, r))

  logChangeToChangesSheet(edits_nar.length)
}

function logChangeToChangesSheet(numEdits) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('שינויים changes')
  const date = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy')
  const row = [date, 'BD', 'various', `Applied ${numEdits} auto-edits.`]
  sheet.insertRowBefore(2)
  sheet.getRange(2, 1, 1, row.length).setValues([row])
}

function calcEditsForSheet(edits) {
  const targ_sheet_name = getTargSheetName(edits[0])
  const targ = getShVa(targ_sheet_name)
  const targ_bti = getMapOfBcpToTargIdx(targ.values)

  const edits_by_cell = groupEditsByCell(edits)

  const results = edits_by_cell.map(
    (edits) => calcEditsForCell(targ.values, targ_bti, edits))

  logResultsForSheet(targ_sheet_name, results)

  return {
    targ_sheet: targ.sheet,
    results_by_cell: results
  }
}

function getEditsNotAlreadyRun(edits_values) {
  const edits_wi = edits_values.map((e, i) => mkRowWithIdx(e, i))
  const edits_nar = edits_wi.filter((e) => notAlreadyRun(e))
  const ntot = edits_values.length
  const nfilt = edits_nar.length
  console.log(`filtered ${ntot} edits down to ${nfilt} edits not already run`)
  return edits_nar
}

function groupEditsBySheet(edits) {
  const out = groupEditsBySomething(getTargSheetName, edits)
  out.forEach((g) => logGroupOfEditsForSheet(g))
  return out
}

function groupEditsByCell(edits) {
  return groupEditsBySomething(getCellIdStrFromEdit, edits)
}

function groupEditsBySomething(pfun, edits) {
  const edits_by_something = new Map()
  for (const edit of edits) {
    updateEditsBySomething(pfun, edits_by_something, edit)
  }
  return Array.from(edits_by_something.values())
}

function updateEditsBySomething(pfun, edits_by_something, edit) {
  const something = pfun(edit)
  if (edits_by_something.has(something)) {
    edits_by_something.get(something).push(edit)
    return
  }
  edits_by_something.set(something, [edit])
}

function mkRowWithIdx(row, idx) {
  return {row: row, idx: idx}
}

function notAlreadyRun(edit_rwi) {
    return !edit_rwi.row[EDIT_COLIDXS.fail_or_succ]
}

const EDIT_COLIDXS = {
  targ_sheet_name: 0,
  targ_bk24na_slash_chap_id: 1,
  targ_pseudoverse_id: 2,
  targ_column_letter: 3,  // C or E
  search_str: 4,
  replace_str: 5,
  fail_or_succ: 6
  // examples of chap_id include 'ג' and 'שמ"א ג'.
  // examples of pseudoverse_id include '0' (a string), 13, and 'תתת'
}

const TARG_COLIDXS = {
  bk24na_slash_chap_id: 0, // aka column A
  pseudoverse_id: 1,       // aka column B
}

function getShVa(sheet_name) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheet_name)
  return {
    sheet: sheet,
    values: sheet.getDataRange().getValues()}
}

function getTargSheetName(edit_rwi) {
  return edit_rwi.row[EDIT_COLIDXS.targ_sheet_name]
}

const COL_IDX_FROM_COLL_LETT = new Map([['C', 2], ['D', 3], ['E', 4]])

function getTargColIdx(edit_rwi) {
  const col_lett = edit_rwi.row[EDIT_COLIDXS.targ_column_letter]
  return COL_IDX_FROM_COLL_LETT.get(col_lett)
}

function getMapOfBcpToTargIdx(targ_values) {
  const pairs = targ_values.map((row, idx) => [getBcpStrFromTargRow(row), idx])
  return new Map(pairs)
}

function getBcpStrFromTargRow(targ_row) {
  const targ_row_bc = targ_row[TARG_COLIDXS.bk24na_slash_chap_id]
  const targ_row_p = targ_row[TARG_COLIDXS.pseudoverse_id]
  return mkBcpStr([targ_row_bc, targ_row_p])
}

function getBcpStrFromEdit(edit) {
  const edit_bc = edit.row[EDIT_COLIDXS.targ_bk24na_slash_chap_id]
  const edit_p = edit.row[EDIT_COLIDXS.targ_pseudoverse_id]
  const edit_bcp_pair = [edit_bc, edit_p]
  return mkBcpStr(edit_bcp_pair)
}

function getCellIdStrFromEdit(edit) {
  const bcp_str = getBcpStrFromEdit(edit)
  const edit_column_letter = edit.row[EDIT_COLIDXS.targ_column_letter]  // C or E
  return `${bcp_str}/${edit_column_letter}`
}

function mkBcpStr(bcp_pair) {
  const [bcp_pair_bc, bcp_pair_p] = bcp_pair
  return `${bcp_pair_bc}/${bcp_pair_p}`
}

function getRowOfTarg(targ_values, targ_bti, edit) {
  const bcp = getBcpStrFromEdit(edit)
  const targ_row_idx = targ_bti.get(bcp)
  return [targ_row_idx, targ_values[targ_row_idx]]
}

function calcEditsForCell(targ_values, targ_bti, edits) {
  const [targ_row_idx, targ_row] = getRowOfTarg(targ_values, targ_bti, edits[0])
  const targ_col_idx = getTargColIdx(edits[0])
  const targ_cell = targ_row[targ_col_idx]

  const results_of_edits = calcEditsForCell2(targ_cell, edits)

  return {
    targ_row_idx: targ_row_idx,
    targ_col_idx: targ_col_idx,
    new_targ_cell: results_of_edits.new_targ_cell,
    fswis: results_of_edits.fswis
  }
}

function calcEditsForCell2(targ_cell, edits_for_cell) {
  const history = [targ_cell]
  const fswis = []
  for (const edit of edits_for_cell) {
    const replace_result = replace(history[0], edit.row)
    const ntc = replace_result.new_targ_cell
    if (ntc !== null) {
      history.unshift(ntc)
    }
    const fswi = mkFswi(replace_result.fail_or_succ, edit.idx)
    fswis.push(fswi)
  }
  return {
    new_targ_cell: history.length > 1 ? history[0] : null,
    fswis: fswis,
  }
}

function mkFswi(fail_or_succ, idx) { // fail_or_succ with [edit] idx
    return {fail_or_succ: fail_or_succ, idx: idx}
}

function replace(targ_cell, edit_row) {
  const search_str = edit_row[EDIT_COLIDXS.search_str]
  const replace_str = edit_row[EDIT_COLIDXS.replace_str]

  return replace2(search_str, replace_str, targ_cell)
}

function replace2(edit_from, edit_to, targ_cell) {
  const io_first = targ_cell.indexOf(edit_from)
  if (io_first === -1) {
    return mkReplaceOut('failure_found_0')
  }
  const io_last = targ_cell.lastIndexOf(edit_from)
  if (io_first !== io_last) {
    return mkReplaceOut('failure_found_gt_1')
  }
  const new_targ_cell = targ_cell.replace(edit_from, edit_to)
  return mkReplaceOut('success', new_targ_cell)
}

function mkReplaceOut(fail_or_succ, new_targ_cell=null) {
  return {fail_or_succ: fail_or_succ, new_targ_cell: new_targ_cell}
}

function writeSheetEdits(edits_sheet, results_for_sheet) {
  results_for_sheet.results_by_cell.forEach(
    (r) => writeCellEdits(edits_sheet, results_for_sheet.targ_sheet, r))
}

function writeCellEdits(edits_sheet, targ_sheet, result) {
  if (result.new_targ_cell !== null) {
    writeCellEditToTargSheet(targ_sheet, result)
  }
  result.fswis.forEach((fswi) =>
    writeFailOrSuccToEditSheet(edits_sheet, fswi))
}

function writeFailOrSuccToEditSheet(edits_sheet, fswi) {
  const rownum = 1 + fswi.idx
  const colnum = 1 + EDIT_COLIDXS.fail_or_succ
  const numrows = 1
  const numcols = 2
  const range = edits_sheet.getRange(rownum, colnum, numrows, numcols)
  const fail_or_succ = fswi.fail_or_succ
  const date = new Date().toDateString()
  const range_vals = [[fail_or_succ, date]]
  range.setValues(range_vals)
}

function writeCellEditToTargSheet(sheet, result) {
  const rownum = 1 + result.targ_row_idx
  const colnum = 1 + result.targ_col_idx
  const cell = sheet.getRange(rownum, colnum)
  cell.setValue(result.new_targ_cell)
}

function logGroupOfEditsForSheet(edits) {
  const sheet_name = getTargSheetName(edits[0])
  if (edits.length > 1) {
    console.log(`created group of ${edits.length} edits for ${sheet_name}`)
  }
}

function logResultsForSheet(targ_sheet_name, results_by_cell) {
  const failures_by_cell = results_by_cell.filter(hasNonNullNewTargCell)
  const num_cell_edits = results_by_cell.length
  const num_cell_fails = num_cell_edits - failures_by_cell.length
  const num_sr_fails = results_by_cell.reduce(sum_failures_in_cell, 0)
  console.log(`sheet ${targ_sheet_name} has ${num_cell_fails} cell edit failures out of ${num_cell_edits} cell edits`)
  console.log(`sheet ${targ_sheet_name} has ${num_sr_fails} search-and-replace failures`)
}

function hasNonNullNewTargCell(result_for_cell) {
  return result_for_cell.new_targ_cell !== null
}

function sum_failures_in_cell(accum, result_for_cell)
{
  return accum + count_failures_in_fswis(result_for_cell.fswis)
}

function count_failures_in_fswis(fswis) {
  const fswi_failures = fswis.filter((fswi) => isNotSuccess(fswi))
  return fswi_failures.length
}

function isNotSuccess(fswi) {
  return fswi.fail_or_succ !== 'success'
}

function mkSelfTestCase(targ_cell, edit_specs, new_targ_cell) {
  // edit_spec: search_str, replace_str, fail_or_succ_str
  const edits = edit_specs.map((s, idx) => mkEditForSelfTest(s[0], s[1], idx))
  const fwsis = edit_specs.map((s, idx) => mkFswi(s[2], idx))
  return {
    targ_cell: targ_cell,
    edits_for_cell: edits,
    expected_out: {
      new_targ_cell: new_targ_cell,
      fswis: fwsis
    }
  }
}

const SELF_TEST_CASES = Array()
SELF_TEST_CASES.push(mkSelfTestCase(
  'foo bar',
  [
    ['foo', 'FOO', 'success'],
    ['bar', 'BAR', 'success'],
  ],
  'FOO BAR'
))
SELF_TEST_CASES.push(mkSelfTestCase(
  'foo bar',
  [
    ['fxx', 'FOO', 'failure_found_0'],
    ['bar', 'BAR', 'success'],
  ],
  'foo BAR'
))
SELF_TEST_CASES.push(mkSelfTestCase(
  'foo bar',
  [
    ['foo', 'FOO', 'success'],
    ['bxx', 'BAR', 'failure_found_0'],
  ],
  'FOO bar'
))
SELF_TEST_CASES.push(mkSelfTestCase(
  'foo bar',
  [
    ['foo', 'FOO', 'success'],
    ['fxx', 'FOO', 'failure_found_0'],
    ['bar', 'BAR', 'success'],
  ],
  'FOO BAR'
))
SELF_TEST_CASES.push(mkSelfTestCase(
  'foo bar foo',
  [
    ['foo', 'FOO', 'failure_found_gt_1'],
  ],
  null
))

function selfTest() {
  SELF_TEST_CASES.forEach(selfTestOneCase)
}

function selfTestOneCase(cas) {
  const out = calcEditsForCell2(cas.targ_cell, cas.edits_for_cell)
  const expected_out = cas.expected_out
  if (!deepEqual(out, expected_out)) {
    console.error('Self-test failed: the following two are not equal:')
    console.error(out)
    console.error(expected_out)
  }
}

function deepEqual(a, b) {
  return JSON.stringify(a) === JSON.stringify(b)
}

function mkEditRowForSelfTest(search_str, replace_str) {
  const edit_row = Array(5)
  edit_row[EDIT_COLIDXS.search_str] = search_str
  edit_row[EDIT_COLIDXS.replace_str] = replace_str
  return edit_row
}

function mkEditForSelfTest(search_str, replace_str, idx) {
  return mkRowWithIdx(mkEditRowForSelfTest(search_str, replace_str), idx)
}
