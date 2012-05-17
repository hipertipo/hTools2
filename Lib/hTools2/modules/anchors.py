# [h] hTools2.modules.anchors

'''
hTools2.modules.anchors
=======================

Functions
---------

### `get_anchors(font, glyph_names=None)`

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

### `rename_anchor(glyph, old_name, new_name)`

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

### `transfer_anchors(source_glyph, dest_glyph)`

Transfer the existing anchors in `source_glyph` to `dest_glyph`.

    from hTools2.modules.anchors import transfer_anchors
    f1 = RFont('/fonts/_Publica/_ufos/Publica_55.ufo')
    f2 = RFont('/fonts/_Publica/_ufos/Publica_95.ufo')
    glyph_name = 'a'
    transfer_anchors(f1[glyph_name], f2[glyph_name])

### `move_anchors(glyph, anchor_names, (x, y))`

Move all anchors with `anchor_names` in `glyph` by `(x, y)` units.

    add example

'''

# font-level tools

def get_anchors(font, glyph_names=None):
	anchors_dict = {}
	if glyph_names == None:
		_glyph_names = font.keys()
	else:
		_glyph_names = glyph_names
	for glyph_name in _glyph_names:
		g = font[glyph_name]
		if len(g.anchors) > 0:
			anchors = []
			for a in g.anchors:
				anchors.append((a.name, a.position))
			anchors_dict[g.name] = anchors
	return anchors_dict

# glyph-level tools

def rename_anchor(glyph, old_name, new_name):
    has_name = False
    if len(glyph.anchors) > 0:
        for a in glyph.anchors:
            if a.name == old_name:
                has_name = True
                a.name = new_name
                glyph.update()
    return has_name

def transfer_anchors(source_glyph, dest_glyph):
	has_anchor = False
	if len(source_glyph.anchors) > 0 :
		has_anchor = True
		anchorsDict = {}
		for a in source_glyph.anchors:
			anchorsDict[a.name] = a.position
		dest_glyph.clearAnchors()
		for anchor in anchorsDict:
			dest_glyph.appendAnchor(anchor, anchorsDict[anchor])
			dest_glyph.update()
	return has_anchor

def move_anchors(glyph, anchor_names, (delta_x, delta_y)):
	for anchor in glyph.anchors:
		if anchor.name in anchor_names:
			anchor.move((delta_x, delta_y))
			glyph.update()
