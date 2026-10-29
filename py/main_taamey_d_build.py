# SPDX-License-Identifier: GPL-2.0-or-later
# Part of Taamey D's build, which may be redistributed and modified under the terms of
# the GNU General Public License, version 2 or (at your option) any later version.
"""Build Taamey D's font files from its sources, by hand, when the sources change.

Run it from the repository root:

    .venv/Scripts/python.exe py/main_taamey_d_build.py

Under Taamey-D/font-m-TaD/, it fills three templates, writing Taamey_D.fea,
Taamey_D-nofea.sfd and license.txt. Then it runs FontForge, with Taamey-D/ as FontForge's
working directory, on font-m-TaD/ffscript_generate_sfd_n_ttf.py, which writes
Taamey_D.sfd, Taamey_D.ttf, Taamey_D.woff and Taamey_D.woff2. It finds FontForge through
--fontforge, then fontforge on PATH, then, on Windows, FontForgeBuilds/fontforge.bat under
ProgramFiles or ProgramFiles(x86).

This file and its package, py/taamey_d_build/, are to ship in the font's source archives
under GPL-2.0-or-later, so they import only each other and the standard library.
"""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys

from taamey_d_build import fill_in_template

REPO_ROOT = Path(__file__).resolve().parent.parent
# FontForge's working directory, relative to REPO_ROOT.
FONT_TREE = Path("Taamey-D")
# The font's sources and generated files, relative to FONT_TREE.
FONT_DIRECTORY = Path("font-m-TaD")
FONT_STEM = "Taamey_D"
FONTFORGE_SCRIPT = FONT_DIRECTORY / "ffscript_generate_sfd_n_ttf.py"


def find_fontforge(explicit_path=None):
    """Prefer an explicit command, then PATH, then the existing Windows layouts."""
    if explicit_path:
        command = shutil.which(explicit_path)
        if command:
            return str(Path(command).absolute())
        raise RuntimeError(f"FontForge command not found: {explicit_path}")
    command = shutil.which("fontforge")
    if command:
        return str(Path(command).absolute())
    if os.name == "nt":
        for variable in ("ProgramFiles", "ProgramFiles(x86)"):
            directory = os.environ.get(variable)
            if directory:
                batch = Path(directory) / "FontForgeBuilds" / "fontforge.bat"
                if batch.is_file():
                    return str(batch)
    raise RuntimeError("FontForge not found; put it on PATH or pass --fontforge")


def run(command, description, cwd=REPO_ROOT, environment=None):
    print(f"== {description} ==", flush=True)
    result = subprocess.run(command, cwd=cwd, env=environment, check=False)
    if result.returncode:
        raise RuntimeError(f"{description} failed (exit {result.returncode})")


def run_fontforge(command):
    # FontForge runs in FONT_TREE, so that the script's base, "font-m-TaD/Taamey_D",
    # resolves alike from a repository checkout and from an extracted source archive.
    arguments = [command, "-script", FONTFORGE_SCRIPT.as_posix()]
    environment = None
    if os.name == "nt" and Path(command).suffix.lower() in {".bat", ".cmd"}:
        # cmd needs its own quoting, rather than the C argv quoting used by
        # subprocess for lists. Expand the path from the environment once so
        # spaces, &, %, Unicode, and ! in installation paths remain literal.
        environment = os.environ.copy()
        environment["TAAMEY_D_FONTFORGE"] = command
        shell = os.environ.get("COMSPEC", "cmd.exe")
        arguments = (
            f'"{shell}" /d /s /v:off /c '
            f'""%TAAMEY_D_FONTFORGE%" -script {FONTFORGE_SCRIPT.as_posix()}"'
        )
    run(
        arguments,
        "Generate Taamey D with FontForge",
        cwd=REPO_ROOT / FONT_TREE,
        environment=environment,
    )


def generate(fontforge):
    pairs = (
        (f"{FONT_STEM}.sym.fea", f"{FONT_STEM}.fea"),
        (f"{FONT_STEM}-nofea.sym.sfd", f"{FONT_STEM}-nofea.sfd"),
        ("license.sym.txt", "license.txt"),
    )
    for source, destination in pairs:
        output = (FONT_TREE / FONT_DIRECTORY / destination).as_posix()
        # Preserve the Windows generated-file attributes. POSIX needs no attrib
        # equivalent; do not alter its permission bits.
        if os.name == "nt":
            run(["attrib", "-r", output], "Unlock generated template")
        print(f"== Fill {output} ==", flush=True)
        fill_in_template.fill_in(
            FONT_STEM,
            REPO_ROOT / FONT_TREE / FONT_DIRECTORY / source,
            REPO_ROOT / output,
        )
        if os.name == "nt":
            run(["attrib", "+r", output], "Protect generated template")
    run_fontforge(fontforge)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fontforge", help="FontForge executable or Windows batch path"
    )
    args = parser.parse_args()
    try:
        fontforge = find_fontforge(args.fontforge)
        generate(fontforge)
    except (OSError, RuntimeError, ValueError) as error:
        raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
    main()
