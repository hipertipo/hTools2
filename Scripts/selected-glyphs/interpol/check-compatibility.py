# [h] check compatibility for interpolation

# imports

from robofab.interface.all.dialogs import SelectFont
from hTools2.modules.interpol import check_compatibility

# get fonts

f1 = SelectFont()
f2 = SelectFont()

# get glyphs

if len(f1.selection) > 0:
    glyph_names = f1.selection
else:
    glyph_names = f1.keys()

# run!

check_compatibility(f2, f1, names=glyph_names, report=False)
