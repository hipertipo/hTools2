# [h] clear font guides

'''Remove all global guides in the font.'''

# imports

from hTools2.modules.fontutils import get_glyphs, clear_guides

# run

f = CurrentFont()
clear_guides(f)
