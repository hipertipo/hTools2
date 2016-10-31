# [h] hTools2.modules.pshinting

from robofab.pens.marginPen import MarginPen

#----------
# ps stems
#----------

def get_vstems(font, glyphs=['l', 'I']):
    ref_y = font.info.xHeight / 2.0
    stems = []
    for glyph_name in glyphs:
        g = font[glyph_name]
        # get margins
        pen = MarginPen(g, ref_y, isHorizontal=True)
        g.draw(pen)
        # calculate stem from margins
        try:
            left_edge, right_edge = pen.getMargins()
            stem = int(right_edge - left_edge)
            stems.append(stem)
        except:
            pass # glyph is empty
    return stems

def get_hstems(font, glyphs=['H']):
    stems = []
    for glyph_name in glyphs:
        g = font[glyph_name]
        ref_x = g.width / 2.0
        # get margins
        pen = MarginPen(g, ref_x, isHorizontal=False)
        g.draw(pen)
        # calculate stem from margins
        try:
            bottom_edge, top_edge = pen.getMargins()
            stem = int(top_edge - bottom_edge)
            stems.append(stem)
        except:
            pass # glyph is empty
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
