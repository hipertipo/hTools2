# [h] clean dirty FL spacing groups

f = CurrentFont()

for group_name in f.groups.keys():
    glyph_names = []
    for glyph_name in f.groups[group_name]:
        if glyph_name.count("'") > 0:
            glyph_name = glyph_name.replace("'", "")
        glyph_names.append(glyph_name)
    f.groups[group_name] = glyph_names

    print group_name
    print f.groups[group_name]
    print
