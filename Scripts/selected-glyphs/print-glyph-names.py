#[h] print selected glyphs

'''print selected glyphs'''

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

f = CurrentFont()
printSelectedGlyphs(f, mode=0)
