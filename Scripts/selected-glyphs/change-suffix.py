# [h] change suffix

f = CurrentFont()

_suffix_old = "oldstyle"
_suffix_new = "onum_pnum"

print "changing suffix of selected glyphs..."
for gName in f.selection:
    nameParts = f[gName].name.split(".")
    if len(nameParts) == 2:
        if nameParts[1] == _suffix_old:
            gNew = f[gName].copy()
            newName = "%s.%s" % (nameParts[0], _suffix_new)
            print "\trenaming %s to %s" % (gName, newName)
            try:
                f.insertGlyph(gNew, name=newName)
                f.removeGlyph(gName)
            except:
                print '#### BUG: %s' % gName
f.update()
print "...done.\n"
