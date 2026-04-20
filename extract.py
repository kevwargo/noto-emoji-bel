import os

from fontTools.ttLib import TTFont

font = TTFont("NotoColorEmoji.ttf")

cbdt = font["CBDT"]
cblc = font["CBLC"]

output_dir = "extracted_pngs"
os.makedirs(output_dir, exist_ok=True)

for strike_index, strike in enumerate(cblc.strikes):
    for subtable in strike.indexSubTables:
        # print(type(subtable.locations), subtable.locations[0])
        for glyph_name, location in subtable.locations:
            data = cbdt.strikes[strike_index].glyphs[glyph_name]

            if hasattr(data, "imageData"):
                filename = f"{output_dir}/{glyph_name}_strike{strike_index}.png"
                with open(filename, "wb") as f:
                    f.write(data.imageData)

print("Done extracting.")
