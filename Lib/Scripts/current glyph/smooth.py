# [h] convert selected points to `smooth`

g = CurrentGlyph()
g.prepareUndo('convert to smooth')

for c in g:
    for s in c:
        for p in s.points:
            if p not in s.offCurve and p.selected:
                s.smooth = True

g.performUndo()
