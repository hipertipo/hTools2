# [h] hTools2.modules.gstring

def make_string(names_list, spacer=None):
    '''Makes a string of text from a list of `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.'''
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
    '''Makes a string of slash-separated `glyph_names`. Optionally, uses a `spacer` glyph between the glyphs.'''
    if spacer is not None:
        _spacer = '/' + spacer
    else:
        _spacer = ''
    _glyph_names = ''
    for glyph_name in names_list:
        _glyph_names = _glyph_names + '/' + glyph_name + _spacer
    return _glyph_names
