# [h] hTools2.objects.hglyph

from hfont import hFont

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
