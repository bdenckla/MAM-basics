# Taamey D 0.921 distribution support

These immutable support inputs accompany the frozen 21,148-byte font whose SHA-256 is
`5cc8df8ae3311b91e506edbb294561f6f0e39ebe4260bdb972c90902186c2474`.
The font itself is not an input in this directory. [`SOURCE.txt`](SOURCE.txt) records the
source-download details; [`SOURCE-INVENTORY.json`](SOURCE-INVENTORY.json) records the pinned
upstream bytes. [`BUILD.txt`](BUILD.txt) describes the reviewed single-font input closure,
the upstream procedure, and the unverified exact-build limitation.

## Publication mapping

The asset publisher must make byte-for-byte copies, without reserializing JSON or text:

| Canonical input | Published destination |
|---|---|
| `Taamey_D-0.921-source-40115a364a4e.zip` | `gh-pages/font-sources/taamey-d-0.921/` with the same filename |
| `FONT-NOTICE.txt`, `GPL-2.0.txt`, `SOURCE-INVENTORY.json`, `BUILD.txt`, `SOURCE.txt` | `gh-pages/font-sources/taamey-d-0.921/` with the same filenames |
| `FONT-NOTICE.txt`, `GPL-2.0.txt` | Each of `gh-pages/phonetic-mam/woff2/` and `gh-pages/yeivin-itm/woff2/`, with the same filenames |
| `PRODUCT-WOFF2-SOURCE.txt` | `SOURCE.txt` in each of those two product `woff2/` directories |

`README.md` and `PRODUCT-WOFF2-SOURCE.txt` are not copied to the shared download directory.
The product SOURCE template is already valid for both product paths and requires no
placeholder substitution. Its relative source-download link resolves to the shared directory
on the same website. Product pages should expose a discoverable link to their font's
`woff2/SOURCE.txt`; a CSS font reference alone does not advertise the source download.

Publish the source download and notices alongside the binary. Keep them available while the
associated font is distributed. Keep every archive and all source bytes unchanged; any future
font replacement requires checking its actual license, source, hashes, and publication mapping
again. An upstream URL alone is not the maintained same-host source provision.

## Scope and rights

The ZIP contains all eight files used by the pinned upstream single-font build path, their
inventory, the complete GPL version 2 text, the font notice, and build guidance. Upstream source
files are preserved byte for byte, including their historical formatting. Do not format or
execute the archived upstream code as part of publishing these assets.

The font notice preserves the exact copyright, GPL version 2 grant, and document-embedding
exception wording from the font's OpenType name table. Blank-line whitespace was removed and
a final newline added. The GPL text is an unmodified download from the Free Software
Foundation. The GPL and font notice govern the font and corresponding upstream source; this
repository makes no new GPL version 3 or CC0 grant over those bytes. The exception does not
remove the distribution requirements for the font itself.

The archive is a source distribution, not a claim that the frozen WOFF2 was independently
rebuilt. The pinned upstream commit contains the byte-identical WOFF2 and these source inputs,
and the single-font source input closure was inspected. Upstream leaves toolchain versions
unfixed. No upstream build script was run during preparation.
