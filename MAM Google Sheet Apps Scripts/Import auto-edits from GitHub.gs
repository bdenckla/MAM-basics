'use strict'

function importAutoEdits() {
  const url =
    'https://raw.githubusercontent.com/bdenckla/mamgo-auto-edits/main/diff_mamws_mamgo-auto-edits.json'

  const response = UrlFetchApp.fetch(url)
  const edits = JSON.parse(response.getContentText())

  if (edits.length === 0) {
    console.log('No edits to import.')
    return
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('AutoEdits')

  const rows = edits.map((e) => [
    e.sena,
    e.bk24na_slash_chap_id,
    e.vrnu,
    e.column,
    e.search_str,
    e.replace_str,
  ])

  const startRow = sheet.getLastRow() + 1
  const numCols = rows[0].length
  const range = sheet.getRange(startRow, 1, rows.length, numCols)
  range.setNumberFormat('@')
  range.setValues(rows)

  console.log(`Appended ${rows.length} edits starting at row ${startRow}.`)
}
