

#### `get_anchors(font, glyph_names=None)`

Get all anchors in the glyphs with the given `glyph_names` as a dictionary. If no `glyph_names` are specified, all glyphs in the font will be used.

Every anchor is stored in a tuple of `name` and `(x,y)` position.

    from hTools2.modules.anchors import get_anchors
    f = CurrentFont()
    anchors = get_anchors(f, glyph_names=['a', 'c', 'e'])
    print anchors.keys()

    >>> ['a', 'c', 'e']

    for k in anchors.keys():
        print k, anchors[k]

    >>> a [('top', (252, 527)), ('bottom', (493, 0))]
    >>> c [('top', (243, 527)), ('bottom', (236, 0))]
    >>> e [('top', (254, 527)), ('bottom', (370, 20))]

#### `rename_anchor(glyph, old_name, new_name)`

Rename anchors with name `old_name` in `glyph` to `new_name`.

    from hTools2.modules.anchors import rename_anchor
    f = CurrentFont()
    glyph = f['a']
    for a in glyph.anchors:
        print a.name,

    >>> top bottom

    rename_anchor(glyph, 'top', 'TOP')
    for a in glyph.anchors:
        print a.name,

    >>> TOP bottom

#### `transfer_anchors(source_glyph, dest_glyph)`

Transfer all existing anchors in `source_glyph` to `dest_glyph`.

    from hTools2.modules.anchors import transfer_anchors
    f1 = RFont('/fonts/_Publica/_ufos/Publica_55.ufo')
    f2 = RFont('/fonts/_Publica/_ufos/Publica_95.ufo')
    glyph_name = 'a'
    transfer_anchors(f1[glyph_name], f2[glyph_name])

#### `move_anchors(glyph, anchor_names, (x, y))`

Move all anchors with `anchor_names` in `glyph` by `(x, y)` units.

    from hTools2.modules.anchors import move_anchors
    font = CurrentFont()
    glyph_name = 'a'
    move_anchors(f[glyph_name], ['top', 'bottom'], (20, 40))
