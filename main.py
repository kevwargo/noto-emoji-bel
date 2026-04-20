#!/usr/bin/env python3

import os

from fontTools.ttLib import TTFont


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
        for sub in strike.indexSubTables:
            print(f"    Glyphs: {len(sub.locations)}")


def extract_pngs(font, output_dir="extracted_pngs"):
    """Extract all PNG glyphs."""
    if "CBDT" not in font or "CBLC" not in font:
        raise ValueError("Font does not contain CBDT/CBLC tables")

    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    os.makedirs(output_dir, exist_ok=True)

    count = 0

    for strike_index, strike in enumerate(cblc.strikes):
        for subtable in strike.indexSubTables:
            for glyph_name in subtable.names:
                glyph = cbdt.strikeData[strike_index][glyph_name]

                if hasattr(glyph, "imageData"):
                    filename = f"{output_dir}/{glyph_name}_s{strike_index}.png"
                    with open(filename, "wb") as f:
                        f.write(glyph.imageData)
                    count += 1

    print(f"✅ Extracted {count} PNGs to '{output_dir}'")


def replace_pngs(font, input_dir="modified_pngs"):
    """Replace PNG glyphs with modified ones."""
    if "CBDT" not in font or "CBLC" not in font:
        raise ValueError("Font does not contain CBDT/CBLC tables")

    cbdt = font["CBDT"]
    cblc = font["CBLC"]

    replaced = 0

    for strike_index, strike in enumerate(cblc.strikes):
        for subtable in strike.indexSubTables:
            for glyph_name in subtable.names:
                path = f"{input_dir}/{glyph_name}_s{strike_index}.png"

                if not os.path.exists(path):
                    continue

                with open(path, "rb") as f:
                    new_data = f.read()

                glyph = cbdt.strikeData[strike_index][glyph_name]

                if hasattr(glyph, "imageData"):
                    glyph.imageData = new_data
                    replaced += 1

    print(f"✅ Replaced {replaced} glyph(s)")


def save_font(font, output_path):
    """Save modified font."""
    font.save(output_path)
    print(f"💾 Saved font to '{output_path}'")


def unicode_to_glyph(font, codepoint):
    """Convert Unicode codepoint (int) to glyph name."""
    cmap = font.getBestCmap()
    return cmap.get(codepoint, None)


def demo_workflow():
    """Example usage."""
    font_path = "NotoColorEmoji.ttf"
    output_font = "CustomEmoji.ttf"

    font = load_font(font_path)

    inspect_font(font)

    # Step 1: Extract PNGs
    extract_pngs(font, "extracted_pngs")

    print("\n👉 Edit PNGs in 'extracted_pngs', copy changed ones to 'modified_pngs'\n")

    input("Press Enter after editing PNGs...")

    # Step 2: Replace PNGs
    replace_pngs(font, "modified_pngs")

    # Step 3: Save
    save_font(font, output_font)


if __name__ == "__main__":
    demo_workflow()
