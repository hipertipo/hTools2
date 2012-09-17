### interpolate_glyph(glyph_name, f1, f2, f3, factor, clear=True)

Interpolates the glyphs with name `glyph_name` from masters `f1` and `f2`, with interpolation factor `(factor_x, factor_y)`, into the destination font `f3`.

The optional parameter `clear` controls if existing glyphs in `f3` should be overwritten.

    from hTools2.modules.interpol import interpolate_glyph
    f1 = RFont(u"/fonts/_Publica/_ufos/Publica_15.ufo", showUI=False)
    f2 = RFont(u"/fonts/_Publica/_ufos/Publica_55.ufo", showUI=False)
    f3 = CurrentFont()
    interpolate_glyph('a', f1, f2, f3, (.3, .7), clear=True)

### check_compatibility(f1, f2, names=None, report=True)

Checks if glyphs in `f1` and `f2` are compatible for interpolation. If `names=None`, all glyphs in `f1` will be checked – otherwise, only the ones in the list `names`. 

Glyph compatibility is indicated by colors in `f1`: glyphs marked with `green` are compatible, glyphs marked with `red` are not compatible (because contours and/or amount of points do not match), and glyphs marked with `blue` do not exist in `f2`.

    from hTools2.modules.interpol import check_compatibility
    f1 = RFont(u"/fonts/_Publica/_ufos/Publica_15.ufo", showUI=True)
    f2 = RFont(u"/fonts/_Publica/_ufos/Publica_55.ufo", showUI=True)
    check_compatibility(f1, f2, names=None, report=False)

 If `report=True`, the check results will be printed to the output window.

    check_compatibility(f1, f2, names=None, report=True)

    >>> checking compatibility between Publica 15 and Publica 55...
    >>> 
    >>>     aring is compatible
    >>>     ### dieresis.sc is not compatible
    >>>     Hcircumflex is compatible
    >>>     ### dollar is not compatible
    >>>     ### cedilla.sc is not compatible
    >>>     H.sc is compatible
    >>>     Yacute is compatible
    >>>     ...
    >>> 
    >>> ...done.
