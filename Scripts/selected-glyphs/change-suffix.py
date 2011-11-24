# [h] change glyphsuffix

f = CurrentFont()

_suffix_old = "oldstyle"
_suffix_new = "onum_pnum"

print "changing suffix of selected glyphs...\n"
for gName in f.selection:
    nameParts = f[gName].name.split(".")
    if len(nameParts) == 2:
        if nameParts[1] == _suffix_old:
            g = f[gName]
            new_name = "%s.%s" % (nameParts[0], _suffix_new)
            print "\trenaming %s to %s..." % (gName, new_name)
            g.name = new_name
            g.update()
f.update()
print "\n...done.\n"
