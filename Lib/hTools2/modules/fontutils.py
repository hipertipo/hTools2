# [h] hTools2.modules.fontutils

from robofab.world import CurrentGlyph

from hTools2.modules.glyphutils import round_points


def get_glyphs(f):
	gNames = []
	cg = CurrentGlyph()
	if cg != None:
		gNames.append(cg.name)
	for g in f:
		if g.selected == True:
			if g.name not in gNames:
				gNames.append(g.name)
	gNames.sort()
	return gNames

# font info

def get_full_name(font):
    full_name = '%s %s' % (font.info.familyName, font.info.styleName)
    return full_name 

def full_name(familyName, styleName):
	if styleName == 'Regular':
		fullName = familyName
	else:
		fullName = familyName + ' ' + styleName
	return fullName

def font_name(familyName, styleName):
	if styleName == 'Regular':
		fontName = familyName
	else:
		fontName = familyName + '-' + styleName
	return fontName

def set_unique_ps_id(font):
	a, b, c, d, e, f = randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9), randint(0,9)
	_psID = "%s%s%s%s%s%s" % ( a, b, c, d, e, f )
	font.info.postscriptUniqueID = int(_psID)

def get_names_from_Path(fontPath):
	dir, file = os.path.split(fontPath)
	name, extension = os.path.splitext(file)
	try:
		familyName, styleName = name.split("_")
		return familyName, styleName
	except ValueError:
		familyName, styleName = name.split("-")
		return familyName, styleName	
	except:
		print "font path not splitable.\n"

def set_foundry_info(font, fontInfoDict):
	font.info.year = fontInfoDict['year']
	font.info.openTypeNameDesigner = fontInfoDict['designer']
	font.info.openTypeNameDesignerURL = fontInfoDict['designerURL']
	font.info.openTypeNameManufacturerURL = fontInfoDict['vendorURL']
	font.info.openTypeNameManufacturer = fontInfoDict['vendor']
	font.info.openTypeOS2VendorID = fontInfoDict['vendor']
	font.info.copyright = fontInfoDict['copyright']
	font.info.trademark = fontInfoDict['trademark']
	font.info.openTypeNameLicense = fontInfoDict['license']
	font.info.openTypeNameLicenseURL = fontInfoDict['licenseURL']
	font.info.openTypeNameDescription = fontInfoDict['notice']
	font.info.versionMajor = fontInfoDict['versionMajor']
	font.info.versionMinor = fontInfoDict['versionMinor']
	font.info.openTypeNameUniqueID = "%s : %s : %s" % (fontInfoDict['foundry'], font.info.postscriptFullName, font.info.year)
	setPSUniqueID(font)
	f.update()

def set_font_names(f, familyName, styleName):
	# family name
	f.info.familyName = familyName
	f.info.openTypeNamePreferredFamilyName = familyName
	# style name
	f.info.styleName = styleName
	f.infoopenTypeNamePreferredSubfamilyName = styleName
	# fallback name
	f.info.styleMapFamilyName = '%s%s' % (familyName, styleName)
	f.info.styleMapStyleName = "regular"
	# composed names
	f.info.postscriptFontName = '%s-%s' % (familyName, styleName)
	f.info.postscriptFullName = '%s %s' % (familyName, styleName)
	f.info.macintoshFONDName = '%s-%s' % (familyName, styleName)
	setPSUniqueID(f)
	# done
	f.update()

# glyph names

def print_selected_glyphs(f, mode=1):
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

# transformations

def decompose(font):
	for g in font:
		g.decompose()

def auto_order_direction(font):
	for g in font:
		g.autoContourOrder()
		g.correctDirection()

def align_to_grid(f, (sizeX, sizeY)):
	for g in f:
		print g
		roundPointsToGrid(g, (sizeX, sizeY))
		g.update()
	f.update()

