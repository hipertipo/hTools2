# [h] hTools2.modules.pshinting

from robofab.pens.marginPen import MarginPen

#----------
# ps stems
#----------

def get_vstems(font):
    ref_glyph = 'l'
    ref_y = font.info.xHeight / 2.0
    g = font[ref_glyph]
    pen = MarginPen(g, ref_y, isHorizontal=True)
    g.draw(pen)
    # try:
    print len(g)
    print ref_y
    print pen.getMargins.__doc__ #, pen.getMargins()
    print pen.getMargins()
    left_edge, right_edge = pen.getMargins()
    stem = right_edge - left_edge
    return [stem]
    # except:
    #     return []

def get_hstems(font):
    ref_glyph = 'H'
    g = font[ref_glyph]
    ref_x = g.width / 2.0
    pen = MarginPen(g, ref_x, isHorizontal=False)
    g.draw(pen)
    # try:
    bottom_edge, top_edge = pen.getMargins()
    stem = top_edge - bottom_edge
    return [stem]
    # except:
    #     return []

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
    zones.append(font['o'].box[1]) # baseline_bottom
    zones.append(0) # baseline_top
    zones.append(font['x'].box[3]) # xheight_bottom
    zones.append(font['o'].box[3]) # xheight_top
    zones.append(font['g'].box[1]) # descender_bottom
    zones.append(font['p'].box[1]) # descender_top
    zones.append(font['d'].box[3]) # ascender_bottom
    zones.append(font['germandbls'].box[3]) # ascender_top
    zones.sort()
    return zones

def set_bluezones(font, bluezones=None):
    if not bluezones:
        bluezones = get_bluezones(font)
    font.info.postscriptBlueValues = bluezones

