# [h] hTools2.modules.interpol

'''
hTools2.modules.interpol
========================

Functions
---------

### `interpolate_glyph(glyph_name, f1, f2, f3, factor, clear=True)`

Interpolates the glyphs with name `glyph_name` from masters `f1` and `f2`, with interpolation factor `(factor_x, factor_y)`, into the destination font `f3`.

The optional parameter `clear` controls if existing glyphs in `f3` should be overwritten.

    from hTools2.modules.interpol import interpolate_glyph
    f1 = RFont(u"/fonts/_Publica/_ufos/Publica_15.ufo", showUI=False)
    f2 = RFont(u"/fonts/_Publica/_ufos/Publica_55.ufo", showUI=False)
    f3 = CurrentFont()
    interpolate_glyph('a', f1, f2, f3, (.3, .7), clear=True)

### `check_compatibility(f1, f2, names=None, report=True)`

Checks if glyphs in `f1` and `f2` are compatible for interpolation. If `names=None`, all glyphs in `f1` will be checked – otherwise, only the ones in the list `names`. 

Glyph compatibility is indicated by colors in `f1`: glyphs marked with `green` are compatible, glyphs marked with `red` are not compatible (because contours and/or amount of points do not match), and glyphs marked with `blue` do not exist in `f2`.

    from hTools2.modules.interpol import check_compatibility
    f1 = RFont(u"/fonts/_Publica/_ufos/Publica_15.ufo", showUI=True)
    f2 = RFont(u"/fonts/_Publica/_ufos/Publica_55.ufo", showUI=True)
    check_compatibility(f1, f2, names=None, report=False)

 If `report=True`, the check results will be printed to the output window.

    check_compatibility(f1, f2, names=None, report=True)

    >>> checking compatibility between Publica 15 and Publica 55...
    >>> 
    >>>     aring is compatible
    >>>     ### dieresis.sc is not compatible
    >>>     Hcircumflex is compatible
    >>>     ### dollar is not compatible
    >>>     ### cedilla.sc is not compatible
    >>>     H.sc is compatible
    >>>     Yacute is compatible
    >>>     ...
    >>> 
    >>> ...done.

'''

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.color import clear_color, clear_colors, named_colors

def interpolate_glyph(gName, f1, f2, f3, factor, clear=True):
	if f2.has_key(gName):
		if clear:
			g = f3.newGlyph(gName, clear=True)
		else:
			g = f3[gName]
		g.interpolate(factor, f1[gName], f2[gName])
		g.update()
		f3.update()
	else:
		print 'glyph %s not contained in font 2' % gName 

def interpolate_kerning(f1, f2, f3, factor):
	k1 = f1.kerning
	k2 = f2.kerning
	k3 = f3.kerning
	k3.interpolate(k1, k2, factor, True)
	f3.update()

def check_compatibility(f1, f2, names=None, report=True):
	# glyph names
	if names != None:
		gNames = names
	else:
		gNames = f1.keys()
	# colors
	clear_colors(f1)
	green = named_colors['green']
	red = named_colors['red']
	blue = named_colors['blue']
	# check glyphs
	if report == True:
		print 'checking compatibility between %s and %s...\n' % (get_full_name(f1), get_full_name(f2))
	for name in gNames:
		if f2.has_key(name):
			clear_color(f2[name])
			# if not compatible
			if f1[name].isCompatible(f2[name], False) is not True:
				f2[name].mark = red
				if report == True:
					print "\t### %s is not compatible" % name
			# if compatible
			else:
				f2[name].mark = green
				if report == True:
					print "\t%s is compatible" % name
		# if glyphs not in f2
		else:
			f1[name].mark = blue
			if report == True:
				print "\t### %s is not in font 2" % name
	# update fonts
	f2.update()
	f1.update()
	if report == True:
		print '\n...done.\n'
