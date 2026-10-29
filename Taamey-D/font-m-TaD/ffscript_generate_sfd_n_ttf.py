# This script is driven by the portable Python workflow, run from the repository root:
#
#    .venv/Scripts/python.exe py/main_taamey_d_build.py

import fontforge  # pyright: reportMissingImports=false

base = "font-m-TaD/Taamey_D"
font = fontforge.open(base + "-nofea.sfd")
font.mergeFeature(base + ".fea")
font.save(base + ".sfd")
font.generate(base + ".ttf")
font.generate(base + ".woff")
font.generate(base + ".woff2")
