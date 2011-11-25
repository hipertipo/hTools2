# [h] print selected glyphs

# from hTools2.modules.fontutils import printSelectedGlyphs

def printSelectedGlyphs(f, mode=1):
	gNames = f.selection
	# mode 1 = plain gNames list
	if mode == 1:
		for gName in gNames:
			print gName
		print
	# mode 0 = Python string
	elif mode == 0:
		s = ''
		for gName in gNames:
			s = s + '"%s", ' % gName
		print s
		print
	else:
		print "invalid mode.\n"

font = CurrentFont()
printSelectedGlyphs(font, mode=0)
