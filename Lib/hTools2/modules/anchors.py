# [h] hTools2.modules.anchors

'''Tools to remove, create, move and transfer anchors.'''

#------------------
# font-level tools
#------------------

def get_anchors(font, glyph_names=None):
    '''Get all anchors in glyphs as a dictionary.'''
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

def clear_anchors(font, glyph_names=None):
    '''Delete all anchors in font.'''
    if glyph_names is None:
        glyph_names = font.keys()
    for glyph_name in glyph_names:
        if len(font[glyph_name].anchors) > 0:
            font[glyph_name].clearAnchors()
            font[glyph_name].update()
    font.update()

#-------------------
# glyph-level tools
#-------------------

def rename_anchor(glyph, old_name, new_name):
    '''Rename anchors with name ``old_name`` in ``glyph`` to ``new_name``.'''
    has_name = False
    if len(glyph.anchors) > 0:
        for a in glyph.anchors:
            if a.name == old_name:
                has_name = True
                a.name = new_name
                glyph.update()
    return has_name

def transfer_anchors(source_glyph, dest_glyph):
    '''Transfer all anchors in ``source_glyph`` to ``dest_glyph``.'''
    has_anchor = False
    if len(source_glyph.anchors) > 0 :
        # collect anchors in source glyph
        has_anchor = True
        anchorsDict = {}
        for a in source_glyph.anchors:
            anchorsDict[a.name] = a.position
        # clear anchors in dest glyph
        dest_glyph.clearAnchors()
        # place anchors in dest glyph
        for anchor in anchorsDict:
            dest_glyph.appendAnchor(anchor, anchorsDict[anchor])
            dest_glyph.update()
    # done
    return has_anchor

def move_anchors(glyph, anchor_names, (delta_x, delta_y)):
    '''Move named anchors by ``(x,y)`` units.'''
    for anchor in glyph.anchors:
        if anchor.name in anchor_names:
            anchor.move((delta_x, delta_y))
            glyph.update()

def create_anchors(glyph, top=True, bottom=True, accent=False, top_delta=20, bottom_delta=20):
    '''Create ``top`` and ``bottom`` anchors at relative positions.'''
    # make anchors list
    anchor_names = []
    if top:
        anchor_names.append('top')
    if bottom:
        anchor_names.append('bottom')
    # run
    font = glyph.getParent()
    has_anchor = False
    anchors = []
    # get existing anchors
    if len(glyph.anchors) > 0 :
        has_anchor = True
        for a in glyph.anchors:
            anchors.append(a.name)
    # add only new anchors
    x = glyph.width / 2
    for anchor_name in anchor_names:
        # add underscore if accent
        if accent:
            anchor_name = '_' + anchor_name
        if anchor_name not in anchors:
            # make anchor y-position
            if anchor_name in [ 'top', '_top' ]:
                y = font.info.xHeight + top_delta
            else:
                y = 0 - bottom_delta
            # place anchor
            glyph.appendAnchor(anchor_name, (x, y))
    # done glyph
    glyph.update()
