from __future__ import annotations

from pathlib import Path
import re
import zipfile
from xml.etree import ElementTree as ET

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}

CONTROL_CHARS = {
    "\u00a0": " ",
}

# These three Aleppo crops are intentional manual overrides of the DOCX-embedded
# source image, so extraction must leave them untouched when they already exist.
# (The count read "two" until 2026-08-18, while the set below has always had three.)
#
# Spelled relative to the DATA root, which is what export_images below measures
# each output path against -- not relative to the working directory, and not to the
# repo the code lives in.  Those two roots are one directory today and stop being
# one when the Python moves to MAM-basics; hkq_paths' module docstring states the
# distinction.
PRESERVED_EXTRACTED_IMAGE_PATHS = frozenset(
    {
        "gh-pages/img/row013_aleppo_01.png",
        "gh-pages/img/row014_aleppo_01.png",
        "gh-pages/img/row023_aleppo_01.png",
    }
)


def normalize_text(text: str) -> str:
    for old, new in CONTROL_CHARS.items():
        text = text.replace(old, new)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def paragraph_text(paragraph: ET.Element) -> str:
    texts = [node.text or "" for node in paragraph.findall(".//w:t", NS)]
    return normalize_text("".join(texts))


def cell_payload(cell: ET.Element, rel_map: dict[str, str]) -> dict[str, object]:
    parts = []
    for para in cell.findall("./w:p", NS):
        text = paragraph_text(para)
        if text:
            parts.append(text)

    image_targets = []
    for blip in cell.findall(".//a:blip", NS):
        rel_id = blip.attrib.get(f"{{{NS['r']}}}embed")
        if rel_id is not None:
            image_targets.append(rel_map[rel_id])

    return {
        "text": "\n".join(parts),
        "image_targets": image_targets,
    }


def slugify(label: str) -> str:
    text = label.strip().lower()
    text = re.sub(r"[^0-9a-z]+", "_", text)
    return text.strip("_") or "entry"


def intro_markdown(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""

    title = paragraphs[0]
    body = paragraphs[1:]
    lines = [f"# {title}", ""]
    bullet_mode = False
    for paragraph in body:
        if paragraph == "Breakdown of the 77 Readings:":
            lines.append("## Breakdown of the 77 Readings")
            lines.append("")
            bullet_mode = True
            continue

        if bullet_mode and re.match(r"^[0-9]+ Instances?:", paragraph):
            lines.append(f"- {paragraph}")
            continue

        if paragraph == "Sincerely,":
            bullet_mode = False
            if lines and lines[-1] != "":
                lines.append("")

        lines.append(paragraph)
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + "\n"


def export_images(
    archive: zipfile.ZipFile,
    row_number: int,
    column_key: str,
    targets: list[str],
    image_dir: Path,
    data_root: Path,
) -> list[str]:
    exported_paths = []
    for image_index, target in enumerate(targets, start=1):
        extension = Path(target).suffix or ".bin"
        filename = f"row{row_number:03d}_{column_key}_{image_index:02d}{extension}"
        output_path = image_dir / filename
        try:
            rel_output_path = output_path.resolve().relative_to(data_root.resolve())
        except ValueError as exc:
            raise ValueError(
                f"image path {output_path!s} is outside data root {data_root!s}"
            ) from exc

        rel_output_path_str = rel_output_path.as_posix()
        source_bytes = archive.read(f"word/{target}")
        if output_path.exists():
            if rel_output_path_str in PRESERVED_EXTRACTED_IMAGE_PATHS:
                exported_paths.append(rel_output_path_str)
                continue

            existing_bytes = output_path.read_bytes()
            if existing_bytes != source_bytes:
                raise ValueError(
                    "refusing to overwrite existing extracted image with different bytes: "
                    f"row={row_number}, column={column_key}, target={target}, "
                    f"output_path={output_path!s}"
                )
        else:
            output_path.write_bytes(source_bytes)

        exported_paths.append(rel_output_path_str)
    return exported_paths
