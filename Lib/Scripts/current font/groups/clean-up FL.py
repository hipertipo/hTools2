# [h] clean-up spacing groups

'''Clean-up quoted glyph-names in FontLab spacing groups.'''

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from hTools2.modules.messages import no_font_open

def clean_FL_groups(font):
    '''remove quotes from names of master glyphs in FL spacing classes'''
    for group_name in f.groups.keys():
        glyph_names = []
        for glyph_name in f.groups[group_name]:
            if glyph_name.count("'") > 0:
                glyph_name = glyph_name.replace("'", "")
            glyph_names.append(glyph_name)
        f.groups[group_name] = glyph_names

f = CurrentFont()

if f is not None:
    clean_FL_groups(f)

else:
    no_font_open
