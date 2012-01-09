# hTools2.modules.interpol

#---------------
# interpolation
#---------------

def interpolateGlyph(gName, f1, f2, f3, factor, clear=True):
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

def interpolateKerning(f1, f2, f3, factor):
	k1 = f1.kerning
	k2 = f2.kerning
	k3 = f3.kerning
	k3.interpolate(k1, k2, factor, True)
	f3.update()

#---------------
# compatibility
#---------------

def checkCompatibility_FL(f1, f2, glyphNames=None, report=True):
	if glyphNames != None:
		gNames = glyphNames
	else:
		gNames = f1.keys()
	for g in f1:
		g.mark = 0
	f1.update()
	green, red, blue = 100, 255, 160
	if report == True:
		print 'checking compatibility between %s and %s...\n' % (f1.info.fullName, f2.info.fullName)
	for name in gNames:
		if f2.has_key(name):
			f2[name].mark = 0
			# if not compatible
			if f1[name].isCompatible(f2[name], False) == False:
				f2[name].mark = red
				f2[name].update()
				if report == True:
					print "\t%s is **not** compatible:" % name
					for error in f1[name].isCompatible(f2[name], True)[1]:
						print "\t\t%s" % error
			# if compatible
			else:
				f2[name].mark = green
				f2[name].update()
				if report == True:
					print "\t%s is compatible." % name
		# if glyphs not in f2
		else:
			f1[name].mark = blue
			f1[name].update()
			if report == True:
				print "\t%s is **not** compatible:" % name
				print "\t\t%s is not in font 2." % name
	# update fonts
	f2.update()
	f1.update()
	if report == True:
		print '\n...done.\n'
