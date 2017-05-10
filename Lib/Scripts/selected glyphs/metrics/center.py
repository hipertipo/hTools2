f = CurrentFont()

if f is not None:
    for glyph_name in f.selection:
        g = f[glyph_name]
        g.prepareUndo('center glyphs')
        w = g.width
        g.leftMargin = (g.leftMargin + g.rightMargin) * 0.5
        g.width = w
        g.performUndo()

