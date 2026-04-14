'use strict'

const MAMGO_AUTO_EDITS_REPO = 'bdenckla/mamgo-auto-edits'
const MAMGO_AUTO_EDITS_JSON_PATH = 'diff_mamws_mamgo-auto-edits.json'

function makeNoCacheUrl(baseUrl) {
  if (typeof baseUrl !== 'string' || baseUrl.length === 0) {
    throw new Error(
      'Run importAutoEdits, not makeNoCacheUrl. makeNoCacheUrl expects a non-empty URL string.'
    )
  }

  const separator = baseUrl.indexOf('?') >= 0 ? '&' : '?'
  return `${baseUrl}${separator}cachebust=${Date.now()}`
}

function importAutoEdits() {
  function getMainHeadShaFromBranchApi() {
    const branchApiUrl = makeNoCacheUrl(
      `https://api.github.com/repos/${MAMGO_AUTO_EDITS_REPO}/branches/main`)

    const branchResponse = UrlFetchApp.fetch(branchApiUrl, {
      headers: {
        Accept: 'application/vnd.github+json',
        'Cache-Control': 'no-cache',
        Pragma: 'no-cache',
      },
      muteHttpExceptions: true,
    })

    if (branchResponse.getResponseCode() !== 200) {
      throw new Error(
        'GitHub branch API response: ' +
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

  function getMainHeadShaFromAtomFeed() {
    const atomUrl = makeNoCacheUrl(
      `https://github.com/${MAMGO_AUTO_EDITS_REPO}/commits/main.atom`)

    const atomResponse = UrlFetchApp.fetch(atomUrl, {
      headers: {
        'Cache-Control': 'no-cache',
        Pragma: 'no-cache',
      },
      muteHttpExceptions: true,
    })

    if (atomResponse.getResponseCode() !== 200) {
      throw new Error(
        'GitHub commit Atom feed response: ' +
          atomResponse.getResponseCode() +
          ' ' +
          atomResponse.getContentText()
      )
    }

    const atomText = atomResponse.getContentText()
    const commitMatch = atomText.match(/Grit::Commit\/([0-9a-f]{40})/)
    if (!commitMatch) {
      throw new Error('GitHub commit Atom feed did not include a commit SHA')
    }

    return commitMatch[1]
  }

  function getMainHeadSha() {
    try {
      const headSha = getMainHeadShaFromBranchApi()
      console.log(`Resolved main HEAD SHA from branch API: ${headSha}`)
      return headSha
    } catch (branchError) {
      console.log(
        'Branch API HEAD lookup failed; falling back to public Atom feed. ' +
          branchError.message
      )
    }

    try {
      const headSha = getMainHeadShaFromAtomFeed()
      console.log(`Resolved main HEAD SHA from Atom feed: ${headSha}`)
      return headSha
    } catch (atomError) {
      throw new Error(
        'Could not resolve main HEAD SHA from either source. Atom fallback error: ' +
          atomError.message
      )
    }
  }

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
  const url = makeNoCacheUrl(
    `https://raw.githubusercontent.com/${MAMGO_AUTO_EDITS_REPO}/${headSha}/${MAMGO_AUTO_EDITS_JSON_PATH}`)

  console.log(`Importing auto-edits from commit ${headSha}`)

  const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true })
  console.log(`Raw JSON fetch response code: ${response.getResponseCode()}`)
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

  const responseText = response.getContentText()
  console.log(`Raw JSON fetch content length: ${responseText.length}`)

  const edits = JSON.parse(responseText)
  console.log(`Parsed auto-edits count: ${edits.length}`)

  if (edits.length === 0) {
    console.log('No edits to import.')
    return
  }

  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('AutoEdits')
  console.log(`AutoEdits sheet found: ${Boolean(sheet)}`)

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
  console.log(`Preparing to append ${rows.length} rows at row ${startRow}`)
  const range = sheet.getRange(startRow, 1, rows.length, numCols)
  range.setNumberFormat('@')
  range.setValues(rows)

  console.log(`Appended ${rows.length} edits starting at row ${startRow}.`)
}
