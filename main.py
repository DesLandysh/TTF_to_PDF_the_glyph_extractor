# works with non-bytes representation cmap tables, only unicode cmap tables
# works only with better-vcr-6.1.ttf font
# actually for this font it was written
# and even with this font, it works not quite smoothly

from fpdf import FPDF
from fontTools import ttLib
import numpy as np

fontPath = "better-vcr-6.1.ttf"
fontFamilyName = "RogueLike_RPG_MultyLang"

from_font = ttLib.TTFont(fontPath)

# total glyphs in font
total = from_font['maxp'].numGlyphs
print(f'There are {total} glyphs in the font')

# extract cmap tables
cm = from_font['cmap'].__dict__['tables']

# quantity of tables
qnty_tables = len(cm)
print(f'the number of cmap table in this font is {qnty_tables}')

# extract dicts of glyphs in different formats from cmap table
all_tabs_expanded = []
for i in range(0, qnty_tables):
    all_tabs_expanded.append(cm[i].__dict__)

# choose most valuable
valuable_tables = [all_tabs_expanded[0], all_tabs_expanded[3]]


def tab_to_lists(table_dict: dict) -> list:
    """ Return list of lists
    `counts` shows the order number in a table of glyphs, just for usability
    `dex_gl` is the representation symbols in decimal code,
    `hex_gl` is the representation symbols in hex code,
    `ch_gl` is the render of the glyph/symbol, how it looks on screen,
    `name_gl` is the given name of the glyph if it has.

    :return list[char, hex, dec, name] - order can be changed
    """
    dex_gl, hex_gl, ch_gl, name_gl = ["DEX"], ["HEX"], ["CHAR"], ["NAME"]
    counter, counts = 1, ["№"]
    table = list(zip(table_dict.keys(), table_dict.values()))
    table = table[-1][1:][0]  # drop unnecessary info
    table_tuple = [(k, v)for k, v in table.items()]

    for tup_item in table_tuple:
        item = tup_item[0]
        if item is int:
            dex_gl.append(int(item))
        else:
            dex_gl.append(item)

        ch_gl.append(chr(int(item)))
        hex_gl.append(hex(int(item)))
        name_gl.append(tup_item[1])

        counts.append(counter)
        counter += 1

    return [counts, ch_gl, hex_gl, dex_gl, name_gl]


def create_pdf(table, output_file: str) -> None:
    """Set up the pdf page, create a tables cells,
    and create a pdf file in current folder """

    font_size = 12
    pdf = FPDF(orientation="P", unit="pt", format="A4")
    pdf.font_size = font_size
    pdf.add_page()
    pdf.add_font(family=fontFamilyName, fname=fontPath, uni=True)
    pdf.set_font(family=fontFamilyName, size=font_size)
    col_width = pdf.w / 6
    row_height = pdf.font_size
    spacing = 2
    for row in table:
        for item in row:
            # `C` for CENTER, L for LEFT, R for RIGHT
            pdf.cell(col_width, row_height*spacing, txt=str(item), border=1, align="L")
        pdf.ln(row_height*spacing)
    pdf.output(output_file)


# convert cmap tables into list of values for each table
tab_list = []
for tab in valuable_tables:
    tab_list.append(tab_to_lists(table_dict=tab))

# create a separate pdf file for each cmap table
for index, in_row_tab in enumerate(tab_list):
    # rows to columns
    in_col_table = np.transpose(in_row_tab)
    create_pdf(table=in_col_table, output_file=f'{fontFamilyName}_v{index}.pdf')
