# [h] clean-up spacing groups

'''Clean-up quoted glyph-names in FontLab dirty spacing groups.'''

# function

def clean_FL_groups(font):
    '''remove quotes from names of master glyphs in FL spacing classes'''
    for group_name in f.groups.keys():
        glyph_names = []
        for glyph_name in f.groups[group_name]:
            if glyph_name.count("'") > 0:
                glyph_name = glyph_name.replace("'", "")
            glyph_names.append(glyph_name)
        f.groups[group_name] = glyph_names
        # print group_name
        # print f.groups[group_name]
        # print

# run

f = CurrentFont()
clean_FL_groups(f)
