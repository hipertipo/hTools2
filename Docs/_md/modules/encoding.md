### import_encoding(file_path)

Import group and glyphs names from an `.enc` file. Returns a dictionary with glyph groups, and a list with the order of the groups.

    from hTools2.modules.encoding import import_encoding
    enc_file = u"/fonts/_Publica/_libs/Publica.enc"
    groups, order = import_encoding(enc_file)
    print groups.keys()

    >>> ['small_caps_extra', 'punctuation', 'small_caps_basic', ... 'symbols', 'quotes', 'spaces' ]

    print order

    >>> 'invisible', 'lowercase_basic', 'lowercase_extra', ...

### clear_unicodes(font)

Remove unicodes from all glyphs in the font.

    from hTools2.modules.encoding import clear_unicodes
    f = CurrentFont()
    clear_unicodes(f)

### auto_unicodes(font)

Automatically set unicode values for all glyphs in the font.

    from hTools2.modules.encoding import auto_unicodes
    f = CurrentFont()
    auto_unicodes(f)    

### auto_unicode(glyph)

Automatically set unicode value(s) for the specified glyph. The method uses RoboFab’s `glyph.autoUnicodes()` function for common glyphs, and complements it with additional values from `unicodes_extra`.

    from hTools2.modules.encoding import auto_unicode, clear_unicodes
    f = CurrentFont()
    clear_unicodes(f)

    # set unicode for 'a' (uses RoboFab)
    print f['a'].unicodes

    >>> []

    auto_unicode(f['a'])
    print f['a'].unicodes

    >>> [97]

    # set unicode for 'dotlessj' (uses unicodes_extra)
    print f['dotlessj'].unicodes

    >>> []

    auto_unicode(f['dotlessj'])
    print f['dotlessj'].unicodes

    >>> [567]

### unicode_int_to_hexstr(intUnicode, add0x=False, addUni=False)

Convert unicode integers to hexadecimal. See also the reverse function `unicode_hexstr_to_int`.

    from hTools2.modules.encoding import unicode_int_to_hexstr
    f = CurrentFont()
    print f['a'].unicodes

    >>> [97]

Note that `glyph.unicodes` is a list (a glyph can have many unicodes), so we need to pass the first value only.

    print unicode_int_to_hexstr(f['a'].unicodes[0])

    >>> 0061

 The optional parameters `uni` and `_0x` add the respective prefixes.

    print unicode_int_to_hexstr(f['a'].unicodes[0], uni=True)

    >>> uni0061

    print unicode_int_to_hexstr(f['a'].unicodes[0], _0x=True)

    >>> 0x0061

### unicode_hexstr_to_int(hexUnicode, replaceUni=True)

Convert a unicode hexadecimal value into an integer. It does exactly the reverse of `unicode_int_to_hexstr`.

    from hTools2.modules.encoding import unicode_int_to_hexstr, unicode_hexstr_to_int
    f = CurrentFont()
    print f['a'].unicodes[0]

    >>> 97

    uni_hex = unicode_int_to_hexstr(f['a'].unicodes[0])
    print uni_hex

    >>> 0061

    print unicode_hexstr_to_int(uni_hex)

    >>> 97

### unicodes_extra

A dictionary containing additional `glyphName` to `unicode` mappings.

### unicode2psnames

A dictionary mapping `unicode` values to `psNames` (standard glyph names).
