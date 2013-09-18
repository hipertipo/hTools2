# [h] hTools2.objects.hglyph

# imports

from hfont import hFont

# objects

class hGlyph:

    """An object to wrap single glyphs, making it easier to access their parent :py:class:`hFont` and :py:class:`hProject` objects.

    .. py:attribute:: glyph

    The actual glyph from a ``.ufo`` font (an :py:class:`RGlyph` object).

    .. py:attribute:: font

    The glyph's parent :py:class:`hFont` object.

    """
    glyph = None
    font = None

    def __init__(self, glyph):
        self.glyph = glyph
        self.font = hFont(self.glyph.getParent())

    def __repr__(self):
        return '<hGlyph>'