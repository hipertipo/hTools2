# [h] hTools2.modules.gstring

# functions

def make_string(names_list, spacer=None):
    """
    Makes a string of text from a list of `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    """
    if spacer is not None:
        _spacer = spacer
    else:
        _spacer = ''
    _string = _spacer
    for glyph_name in names_list:
        for k in unicode2psnames.keys():
            if unicode2psnames[k] == glyph_name:
                char = unichr(k)
                _string = _string + char + _spacer
            else:
                continue
    return _string

def make_string_names(names_list, spacer=None):
    """
    Makes a string of slash-separated `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.

    """
    if spacer is not None:
        _spacer = '/' + spacer
    else:
        _spacer = ''
    _glyph_names = ''
    for glyph_name in names_list:
        _glyph_names = _glyph_names + '/' + glyph_name + _spacer
    return _glyph_names

# def all_glyphs(groups, spacer=None):
#     """
#     Returns a string with all glyphs in the given groups dict.

#     """
#     all_glyphs = ""
#     skip = ['invisible']
#     for group_name in groups.keys():
#         if group_name in skip:
#             pass
#         else:
#             glyph_names_list = groups[group_name]
#             all_glyphs += make_string(glyph_names_list, spacer)
#     return all_glyphs
