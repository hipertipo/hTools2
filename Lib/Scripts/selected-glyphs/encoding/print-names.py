# [h] print selected glyphs

'''Print the names of the selected glyphs as plain text or Python list..'''

# import

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from hTools2.modules.fontutils import print_selected_glyphs

# settings

# mode=0 : list of Python strings
# mode=1 : plain list with linebreaks

_mode = 0

# run

font = CurrentFont()
print_selected_glyphs(font, mode=_mode)
