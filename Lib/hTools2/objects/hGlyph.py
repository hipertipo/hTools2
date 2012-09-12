# [h] hGlyph

# objects

class hGlyph:

    '''An object to wrap single glyphs, making it easier to access their parent `hFont` and `hProject` objects.'''

    # the actual glyph from a .ufo font (an `RGlyph` object)
    glyph = None

    # the glyph's parent `hFont` object
    font = None

    def __init__(self, glyph):
        self.glyph = glyph
        self.font = hFont(self.glyph.getParent())

class hGlyph_NodeBox(hGlyph):

    def __init__(self, glyph):
        hGlyph.__init__(self, glyph)

    def draw(self, pos, ctx, scale_=.5, baseline=False, origin=False, margin=False, vmetrics=False):
        x, y = pos
        if baseline:
            draw_horizontal_line(y, ctx)
        if origin:
            draw_vertical_line(x, ctx)
        pen = NodeBoxPen(self.font.ufo._glyphSet, ctx)
        ctx.push()
        ctx.transform('CORNER')
        ctx.translate(x, y)
        ctx.scale(scale_)
        ctx.nostroke()
        ctx.beginpath()
        self.glyph.draw(pen)
        _path = ctx.endpath(draw=False)
        ctx.drawpath(_path)
        ctx.pop()
        if margin:
            width = round(self.glyph.width * scale_)
            draw_vertical_line(x + width, ctx)
        if vmetrics:
            xheight = round(self.font.ufo.info.xHeight * scale_)
            descender = round(self.font.ufo.info.descender * scale_)
            ascender = round(self.font.ufo.info.ascender * scale_)
            draw_horizontal_line(y - xheight, ctx)
            draw_horizontal_line(y - descender, ctx)
            draw_horizontal_line(y - ascender, ctx)
