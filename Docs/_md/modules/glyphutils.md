## glyphutils

### Functions

#### `center_glyph(glyph)`

Centers the `glyph` in its width, leaving `leftMargin` and `rightMargin` with equal values.

    from hTools2.modules.glyphutils import center_glyph
    f = CurrentFont()
    glyph = f['a']
    print glyph.leftMargin, glyph.rightMargin

    >>> 40 78

    center_glyph(glyph)
    print glyph.leftMargin, glyph.rightMargin

    >>> 59 59

#### `round_width(glyph, gridsize)`

Rounds `glyph.width` to a multiple of `gridsize`.

    from hTools2.modules.glyphutils import round_width
    f = CurrentFont()
    glyph = f['a']
    print glyph.width

    >>> 525

    round_width(glyph, 100)
    print glyph.width

    >>> 500.0

#### `round_margins(glyph, gridsize, left=True, right=True)`

Rounds `glyph.leftMargin` and `glyph.rightMargin` to multiples of `gridsize`.

Use the optional parameters `left` and `right` to turn individual margins of/off.

    from hTools2.modules.glyphutils import round_margins
    f = CurrentFont()
    glyph = f['a']
    print glyph.leftMargin, glyph.rightMargin

    >>> 58 31

    round_margins(glyph, 10)
    print glyph.leftMargin, glyph.rightMargin

    >>> 50.0 30.0

    round_margins(glyph, 11, left=True, right=False)
    print glyph.leftMargin, glyph.rightMargin

    >>> 55.0 30.0

    round_margins(glyph, 11, left=False, right=True)
    print glyph.leftMargin, glyph.rightMargin

    >>> 55.0 33.0

#### `has_suffix(glyph, suffix)`

Checks if the name of `glyph` has the extension `suffix`, and returns `True` or `False`.

    from hTools2.modules.glyphutils import has_suffix
    f = CurrentFont()
    glyph = f['a']
    print has_suffix(glyph, 'alt')

    >>> False

    glyph = f['a.alt']
    print has_suffix(glyph, 'alt')

    >>> True

#### `change_suffix(glyph, old_suffix, new_suffix=None)`

Returns a new modified name for `glyph`, using `new_suffix` in place of `old_suffix`. If `new_suffix=None`, the suffix is removed and only the base glyph name is used.

    from hTools2.modules.glyphutils import change_suffix
    f = CurrentFont()
    glyph = f['a.alt']
    print change_suffix(glyph, 'alt', 'ALT')

    >>> a.ALT

    print change_suffix(glyph, 'alt')

    >>> a

#### `round_points(glyph, (sizeX, sizeY))`

Rounds the position of all `points` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_points
    f = CurrentFont()
    glyph = f['c']
    for c in glyph:
        for p in c.points:
            print p.x, p.y

    >>> 386 93
    >>> 335 44
    >>> 255 44
    >>> 184 44
    >>> 124 94
    >>> 124 237
    >>> ...

    round_points(glyph, (100, 200))
    for c in glyph:
        for p in c.points:
            print p.x, p.y

    >>> 400.0 0.0
    >>> 300.0 0.0
    >>> 300.0 0.0
    >>> 200.0 0.0
    >>> 100.0 0.0
    >>> 100.0 200.0
    >>> ...

#### `round_bpoints(glyph, (sizeX, sizeY))`

Rounds the position of all `bPoints` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_bpoints
    f = CurrentFont()
    glyph = f['o']
    for c in glyph:
        for p in c.bPoints:
            print p.anchor

    >>> (386, 237)
    >>> (255, 44)
    >>> (124, 237)
    >>> (256, 419)
    >>> ...

    round_bpoints(glyph, (100, 100))
    for c in glyph:
        for p in c.bPoints:
            print p.anchor

    >>> (400.0, 200.0)
    >>> (300.0, 0.0)
    >>> (100.0, 200.0)
    >>> (300.0, 400.0)
    >>> ...

#### `round_anchors(glyph, (sizeX, sizeY))`

Rounds the position of all `anchors` in `glyph` to the gridsize `(sizeX,sizeY)`.

    from hTools2.modules.glyphutils import round_anchors
    f = CurrentFont()
    glyph = f['a']
    for a in glyph.anchors:
        print a.name, a.x, a.y

    >>> top 252 527
    >>> bottom 493 0

    round_anchors(glyph, (50, 50))
    for a in glyph.anchors:
        print a.name, a.x, a.y

    >>> top 250 550
    >>> bottom 500 0

#### `select_points_y(glyph, linePos, above=True)`

Selects all points in `glyph` above/below the `linePos(y)`.

    from hTools2.modules.glyphutils import select_points_y
    f = CurrentFont()
    glyph = f['a']
    print glyph.selection

    >>> []

    select_points_y(glyph, 300, above=True)
    print glyph.selection

    >>> [<Point x:135 y:472>, <Point x:194 y:418>, <Point x:354 y:317>, <Point x:87 y:417>, <Point x:252 y:418>, <Point x:424 y:314>, <Point x:424 y:418>, ...]

#### `select_points_x(glyph, linePos, left=True)`

Selects all points in `glyph` to left/right of `linePos(x)`.

    from hTools2.modules.glyphutils import select_points_x
    f = CurrentFont()
    glyph = f['a']
    print glyph.selection

    >>> []

    select_points_x(glyph, 300, left=False)
    print glyph.selection

    >>> [<Point x:424 y:80>, <Point x:357 y:65>, <Point x:357 y:17>, <Point x:424 y:418>, <Point x:351 y:21>, <Point x:364 y:472>, <Point x:458 y:-9>, <Point x:474 y:-9>, <Point x:494 y:-8>, <Point x:424 y:314>, <Point x:371 y:230>, <Point x:371 y:279>, <Point x:433 y:48>, <Point x:318 y:418>, ...]

#### `deselect_points(glyph)`

Deselect any selected `point` in `glyph`.

    from hTools2.modules.glyphutils import deselect_points
    f = CurrentFont()
    glyph = f['a']
    deselect_points(glyph)

#### `shift_selected_points_y(glyph, delta, anchors=False)`

Shift the selected points in `glyph` vertically by `delta` units. If `anchors=True`, anchors will be shifted as well.

    add example

#### `shift_selected_points_x(glyph, delta, anchors=False)`

Shift the selected points in `glyph` horizontally by `delta` units. If `anchors=True`, anchors will be shifted as well.

    add example

#### `clear_glyph_libs(glyph)`

Delete all libs in `glyph`.

    from hTools2.modules.glyphutils import clear_glyph_libs
    f = CurrentFont()
    glyph = f['a']
    print glyph.lib.keys()

    >>> ['com.typemytype.robofont.mark']

    clear_glyph_libs(glyph)
    print glyph.lib.keys()

    >>> []
