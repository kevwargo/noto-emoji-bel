#!/usr/bin/env python3

from pathlib import Path

from fontTools.ttLib import TTFont

SOURCE = "NotoColorEmoji.ttf"
OUTPUT = "CustomEmoji.ttf"
SOURCE_BITMAPS = Path("bitmaps/src")
MODIFIED_BITMAPS = Path("bitmaps/mod")


def load_font(path):
    """Load a TTF font."""
    return TTFont(path)


def inspect_font(font):
    """Print basic info about CBDT/CBLC tables and strikes."""
    print("Tables:", font.keys())

    if "CBLC" not in font or "CBDT" not in font:
        print("❌ No CBDT/CBLC tables found (not a bitmap emoji font)")
        return

    cblc = font["CBLC"]

    print(f"✅ Found {len(cblc.strikes)} strike(s)")
    for i, strike in enumerate(cblc.strikes):
        print(f"  Strike {i}:")
        for subtable in strike.indexSubTables:
            print(f"    Glyphs: {len(subtable.locations)} {len(subtable.names)} {dir(subtable)}")


def extract_pngs(font, output_dir: Path):
    """Extract all PNG glyphs."""
    if "CBDT" not in font or "CBLC" not in font:
        raise ValueError("Font does not contain CBDT/CBLC tables")

    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0

    for strike_index, strike in enumerate(cblc.strikes):
        for subtable in strike.indexSubTables:
            for location, glyph_name in zip(subtable.locations, subtable.names):
                glyph = cbdt.strikeData[strike_index][glyph_name]

                if hasattr(glyph, "imageData"):
                    (output_dir / f"{glyph_name}_s{strike_index}.png").write_bytes(glyph.imageData)
                    count += 1

    print(f"✅ Extracted {count} PNGs to '{output_dir}'")


def replace_pngs(font, input_dir: Path):
    """Replace PNG glyphs with modified ones."""
    if "CBDT" not in font or "CBLC" not in font:
        raise ValueError("Font does not contain CBDT/CBLC tables")

    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    for strike_index, strike in enumerate(cblc.strikes):
        for subtable in strike.indexSubTables:
            for glyph_name in subtable.names:
                if not (path := input_dir / f"{glyph_name}_s{strike_index}.png").exists():
                    continue

                if hasattr((glyph := cbdt.strikeData[strike_index][glyph_name]), "imageData"):
                    glyph.imageData = path.read_bytes()
                    print(f"✅ Replaced {path}")


def save_font(font, output_path):
    """Save modified font."""
    font.save(output_path)
    print(f"💾 Saved font to '{output_path}'")


def main():
    font = load_font(SOURCE)
    inspect_font(font)
    extract_pngs(font, SOURCE_BITMAPS)

    print(f"\n👉 Edit PNGs in {SOURCE_BITMAPS}, copy changed ones to {MODIFIED_BITMAPS}\n")

    input("Press Enter after editing PNGs...")

    # Step 2: Replace PNGs
    replace_pngs(font, MODIFIED_BITMAPS)

    # Step 3: Save
    save_font(font, OUTPUT)


if __name__ == "__main__":
    main()
