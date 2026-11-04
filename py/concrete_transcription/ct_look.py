"""Print an image's size and mode, and write an enlarged copy for viewing.

Written for the concrete-transcription trial, 2026-11-03.  Usage, from the
MAM-basics clone's root:

    ./.venv/Scripts/python.exe py/main_concrete_transcription.py look
        <image> <out.png> <scale> [x0 y0 x1 y1]

The optional box crops before enlarging.  Enlarging is bicubic, for viewing only.
"""

from PIL import Image


def run(src, out, scale, box):
    image = Image.open(src)
    print(image.format, image.size, image.mode, image.info.get("dpi"))
    if box:
        image = image.crop(tuple(box))
    image = image.convert("RGB")
    big = image.resize(
        (image.width * scale, image.height * scale), Image.Resampling.BICUBIC
    )
    big.save(out)
    print(out, big.size)
