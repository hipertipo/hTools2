# [h] print selected glyphs

'''Print the names of the selected glyphs as plain text or Python list..'''

# import

from hTools2.modules.fontutils import print_selected_glyphs

# mode 0 : list of Python strings
# mode 1 : plain list with linebreaks

font = CurrentFont()
print_selected_glyphs(font, mode=1)
