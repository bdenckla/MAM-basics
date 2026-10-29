# Taamey D 1.2 distribution support

These support inputs accompany the 22,484-byte Taamey D 1.2 font whose SHA-256 is
`34e415bd2a28d4d0d407aa2138a43a1a87d9519a6df39933ec05976051032b2c`.
The font itself is not an input in this directory: it is the site's one copy,
[`gh-pages/woff2/Taamey_D.woff2`](../../../gh-pages/woff2/Taamey_D.woff2), which
`py/py_html/taamey_d_assets.py` checks against that SHA-256. It is the
`Taamey_D/Taamey_D.woff2` member of `Taamey_D.zip` in the Taamey D release snapshot
`1.2-MAM-basics-1f1be97138d5`, which this repository publishes from
[`gh-pages/taamey-d/downloads/snapshots/1.2-MAM-basics-1f1be97138d5/`](../../../gh-pages/taamey-d/downloads/snapshots/1.2-MAM-basics-1f1be97138d5/provenance.json),
at <https://bdenckla.github.io/MAM-basics/taamey-d/downloads/snapshots/1.2-MAM-basics-1f1be97138d5/>.
[`SOURCE.txt`](SOURCE.txt) records the source-download details;
[`SOURCE-INVENTORY.json`](SOURCE-INVENTORY.json) records the release identities and every
archive member's size and SHA-256. [`BUILD.txt`](BUILD.txt) describes the build inputs, the
build procedure, and the rebuild check.

## Publication mapping

The asset publisher must make byte-for-byte copies, without reserializing JSON or text:

| Canonical input | Published destination |
|---|---|
| `Taamey_D-1.2-sources.zip` | `gh-pages/font-sources/taamey-d-1.2/` with the same filename |
| `FONT-NOTICE.txt`, `GPL-2.0.txt`, `SOURCE-INVENTORY.json`, `BUILD.txt`, `SOURCE.txt` | `gh-pages/font-sources/taamey-d-1.2/` with the same filenames |
| `FONT-NOTICE.txt`, `GPL-2.0.txt` | `gh-pages/woff2/`, beside the font, with the same filenames |
| `PRODUCT-WOFF2-SOURCE.txt` | `SOURCE.txt` in `gh-pages/woff2/` |

`README.md` and `PRODUCT-WOFF2-SOURCE.txt` are not copied to the shared download directory.
The SOURCE template requires no placeholder substitution. Its relative source-download links
resolve from `gh-pages/woff2/` to the shared directory on the same website. Pages should expose
a discoverable link to the font's `woff2/SOURCE.txt`, as the Phonetic MAM and Yeivin ITM
landing pages do; a CSS font reference alone does not advertise the source download.

Publish the source download and notices alongside the binary. Keep them available while the
associated font is distributed. Keep every archive and all source bytes unchanged; any future
font replacement requires checking its actual license, source, hashes, and publication mapping
again. The release snapshot is on the same website too, but it is the release tool's, so this
package remains the maintained same-host source provision for the site's font.

## Scope and rights

The ZIP is the release snapshot's `Taamey_D-sources.zip`, unchanged but for its file name.
It holds nine files, each at its path in this repository: under `Taamey-D/font-m-TaD/`, the
outline and feature templates, the license template and its expansion, and the FontForge
script; and the build, `py/main_taamey_d_build.py`, with the three modules of its package,
`py/taamey_d_build/`. It holds neither the notices nor the inventory, so
`py/py_html/taamey_d_assets.py` pins each of those files by SHA-256 and requires the archive's
members to be exactly those the inventory lists. Do not format or execute the archived code as
part of publishing these assets.

The font notice preserves the exact copyright, GPL version 2 grant, and document-embedding
exception wording from the font's OpenType name table, which is unchanged since 0.921; it is
1.1's `FONT-NOTICE.txt`, unchanged. Blank-line whitespace was removed and a final newline
added. The GPL text is an unmodified download from the Free Software Foundation. The GPL and
font notice govern the font and its corresponding source; this repository makes no new GPL
version 3 or CC0 grant over those bytes. The exception does not remove the distribution
requirements for the font itself.

The snapshot's `provenance.json` lists the font archive and this source archive, with their
members, under one source commit of this repository, `1f1be97138d5b9ac5464c2de912299828bf9fccb`.
A build from nothing but the archive's nine files reproduced the font byte for byte in one
environment, which `BUILD.txt` names; that is a check, not a pinned build environment.
