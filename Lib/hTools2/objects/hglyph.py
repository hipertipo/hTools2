# [h] hTools2.objects.hglyph

# imports

from hfont import hFont

# objects

class hGlyph:

    """An object to wrap single glyphs, making it easier to access their parent :py:class:`hFont` and :py:class:`hProject` objects."""

    # attributes

    #: An RGlyph object with glyph data.
    glyph = None

    #: The glyph's parent `hFont` object.
    font = None

    # methods

    def __init__(self, glyph):
        self.glyph = glyph
        self.font = hFont(self.glyph.getParent())

    def __repr__(self):
        return '<hGlyph>'
