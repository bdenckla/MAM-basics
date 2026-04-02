'use strict'

function getMainHeadSha() {
  const branchApiUrl =
    'https://api.github.com/repos/bdenckla/mamgo-auto-edits/branches/main'

  const branchResponse = UrlFetchApp.fetch(branchApiUrl, {
    headers: { Accept: 'application/vnd.github+json' },
    muteHttpExceptions: true,
  })

  if (branchResponse.getResponseCode() !== 200) {
    throw new Error(
      'Could not resolve main HEAD SHA. GitHub API response: ' +
        branchResponse.getResponseCode() +
        ' ' +
        branchResponse.getContentText()
    )
  }

  const branchPayload = JSON.parse(branchResponse.getContentText())
  if (!branchPayload.commit || !branchPayload.commit.sha) {
    throw new Error('GitHub branch API response did not include commit.sha')
  }

  return branchPayload.commit.sha
}

function importAutoEdits() {
  // This is intentionally a 2-step fetch:
  // 1) Get main HEAD SHA from the GitHub API.
  // 2) Fetch the JSON from raw.githubusercontent.com using that SHA in the path.
  //
  // Why this seemingly extra complexity?
  // raw.githubusercontent.com branch URLs (like /main/...) are CDN-cached and
  // can lag behind a just-pushed commit for several minutes. A SHA-based raw
  // URL points to immutable content for one commit, so once we resolve HEAD,
  // we fetch exactly that version without waiting for branch-cache expiry.
  const headSha = getMainHeadSha()
  const url =
    'https://raw.githubusercontent.com/bdenckla/mamgo-auto-edits/' +
    headSha +
    '/diff_mamws_mamgo-auto-edits.json'

  const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true })
  if (response.getResponseCode() !== 200) {
    throw new Error(
      'Could not fetch auto-edits JSON at SHA ' +
        headSha +
        '. response: ' +
        response.getResponseCode() +
        ' ' +
        response.getContentText()
    )
  }

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
