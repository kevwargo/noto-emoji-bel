#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#     "fonttools>=4.62.1",
# ]
# ///
import sys
from pathlib import Path
from subprocess import run

from fontTools.ttLib import TTFont


def main(font_file: Path, glyph_file: Path):
    font = TTFont(font_file)
    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    for strike_index, strike in enumerate(cblc.strikes):
        for subtable in strike.indexSubTables:
            for glyph_name in subtable.names:
                # TODO: make it more robust by not relying on glyph id which may change
                # but instead reading the ligature 0x1f1e7_0x1f1fe
                if f"{glyph_name}_s{strike_index}.png" != glyph_file.name:
                    continue

                if hasattr((glyph := cbdt.strikeData[strike_index][glyph_name]), "imageData"):
                    glyph.imageData = glyph_file.read_bytes()
                    font.save(font_file)
                    print(f"Imported glyph from {glyph_file} and merged into {font_file}")

                    print("Refreshing fontconfig cache...")
                    run(["/usr/bin/fc-cache", "-s"])

                return

    print(f"WARNING! no {glyph_file.name} found in {font_file}")


if __name__ == "__main__":
    main(*map(Path, sys.argv[1:]))
