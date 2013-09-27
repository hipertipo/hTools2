# [h] paint and arrange groups

'''Paint each group of glyphs in the font with a different color.'''

# import

from hTools2.modules.color import paint_groups

# run

f = CurrentFont()
paint_groups(f)
