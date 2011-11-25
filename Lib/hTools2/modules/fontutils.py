# [h] hTools2.modules.fontutils

def full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

def decompose(font):
	for g in font:
		g.decompose()

def autoContourOrderDirection(font):
	for g in font:
		g.autoContourOrder()
		g.correctDirection()

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