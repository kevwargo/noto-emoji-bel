#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#     "fonttools>=4.62.1",
#     "uharfbuzz",
# ]
# ///

import re
import sys
from pathlib import Path
from subprocess import run

import uharfbuzz as hb
from fontTools.ttLib import TTFont

# Belarus flag: Regional Indicator B + Regional Indicator Y
TARGET_TEXT = "\U0001f1e7\U0001f1fe"


def main(font_file: Path, glyph_file: Path):
    font = TTFont(font_file)
    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    glyph_name = find_glyph(font, font_file, TARGET_TEXT)

    # Extract the strike index from the replacement image filename.
    if not (m := re.search(r"_s(\d+)\.png$", glyph_file.name)):
        raise ValueError(f"Expected an image filename ending in _sN.png: {glyph_file}")

    strike_index = int(m.group(1))

    if strike_index >= len(cblc.strikes):
        raise ValueError(f"Invalid strike index: {strike_index}")

    strike = cbdt.strikeData[strike_index]
    glyph = strike.get(glyph_name)

    if glyph is None or not hasattr(glyph, "imageData"):
        raise RuntimeError(f"Bitmap data for {glyph_name} not found in strike {strike_index}")

    glyph.imageData = glyph_file.read_bytes()

    font.save(font_file)

    print(f"Imported {glyph_file} into {font_file}, " f"glyph {glyph_name}, strike {strike_index}")

    print("Refreshing fontconfig cache...")
    run(["/usr/bin/fc-cache", "-s"], check=True)


def find_glyph(font: TTFont, font_file: Path, text: str) -> str:
    """Resolve a Unicode sequence to its actual glyph name using HarfBuzz."""

    face = hb.Face(font_file.read_bytes())
    hb_font = hb.Font(face)

    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()

    hb.shape(hb_font, buffer)

    if len(infos := buffer.glyph_infos) != 1:
        raise RuntimeError(f"Expected one glyph for {text!r}, got {len(infos)}")

    gid = infos[0].codepoint
    glyph_order = font.getGlyphOrder()

    if gid == 0 or gid >= len(glyph_order):
        raise RuntimeError(f"Invalid glyph ID: {gid}")

    glyph_name = glyph_order[gid]

    print(f"Resolved {text!r} to {glyph_name} (GID {gid})")

    return glyph_name


if __name__ == "__main__":
    main(*map(Path, sys.argv[1:]))
