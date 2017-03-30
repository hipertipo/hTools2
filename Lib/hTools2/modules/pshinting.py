# [h] hTools2.modules.pshinting

#----------
# ps stems
#----------

def get_vstems(font, glyphs=['l', 'I']):
    from mojo.tools import IntersectGlyphWithLine
    ref_y = font.info.xHeight / 2.0
    stems = []
    for glyph_name in glyphs:
        if font.has_key(glyph_name):
            g = font[glyph_name]
            try:
                # get margins
                left_edge, right_edge = IntersectGlyphWithLine(glyph,
                        ((0, ref_y), (700, ref_y)),
                        canHaveComponent=False, addSideBearings=False)
                # calculate stem from margins
                stem = int(right_edge - left_edge)
                stems.append(stem)
            except:
                # glyph is empty
                pass
    return stems

def get_hstems(font, glyphs=['H']):
    stems = []
    for glyph_name in glyphs:
        if font.has_key(glyph_name):
            g = font[glyph_name]
            ref_x = g.width / 2.0
            try:
                # get margins
                bottom_edge, top_edge = IntersectGlyphWithLine(glyph,
                        ((ref_x, 0), (ref_x, 700)),
                        canHaveComponent=False, addSideBearings=False)
                # calculate stem from margins
                stem = int(top_edge - bottom_edge)
                stems.append(stem)
            except:
                # glyph is empty
                pass
    return stems

def set_vstems(font, stems):
    font.info.postscriptStemSnapV = stems

def set_hstems(font, stems):
    font.info.postscriptStemSnapH = stems

def set_stems(font, vstems=None, hstems=None):
    if not vstems:
        vstems = get_vstems(font)
    if not hstems:
        hstems = get_hstems(font)
    set_vstems(font, vstems)
    set_hstems(font, hstems)

#---------------
# ps blue zones
#---------------

def get_bluezones(font):
    zones = []
    # baseline
    zones.append(font['o'].box[1])
    zones.append(0)
    # xheight
    zones.append(font['x'].box[3])
    zones.append(font['o'].box[3])
    # descender
    zones.append(font['g'].box[1])
    zones.append(font['p'].box[1])
    # asscender
    zones.append(font['d'].box[3])
    zones.append(font['f'].box[3])
    # capheight
    # zones.append(font['H'].box[3])
    # zones.append(font['O'].box[3])
    # done
    zones.sort()
    return zones

def set_bluezones(font, bluezones=None):
    if not bluezones:
        bluezones = get_bluezones(font)
    font.info.postscriptBlueValues = bluezones
