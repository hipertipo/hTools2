## hGlyph

The `hGlyph` object wraps single glyphs, making it easier to access its parent `hFont` and `hProject` objects.

It is intended mainly as a base class for more specialized glyph-level objects, such as `hGlyph_NodeBox` (for drawing glyphs in a NodeBox canvas) or `RasterGlyph` (for converting an outline shape into a element matrix).

### Attributes

#### hGlyph.glyph

The actual glyph from a .ufo font, as an `RGlyph` object.

#### hGlyph.font

The glyph’s parent `hFont` object.
