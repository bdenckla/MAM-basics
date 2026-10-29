# This script is driven by the portable Python workflow, for example:
#
#    .venv/Scripts/python.exe py/main_mega.py --generate-only

import fontforge  # pyright: reportMissingImports=false

base = "font-m-TaD/Taamey_D"
font = fontforge.open(base + "-nofea.sfd")
font.mergeFeature(base + ".fea")
font.save(base + ".sfd")
font.generate(base + ".ttf")
font.generate(base + ".woff")
font.generate(base + ".woff2")
