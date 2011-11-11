# [h] hTools2.modules.fileutils

import os

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		file_name, file_extension = os.path.splitext(n)
		if file_extension[1:] == extension:
			files.append(p)
	return files

def deleteFiles(fileList):
	for f in fileList:
		os.remove(f)

def getGlyphs(f):
	from robofab.world import CurrentGlyph
	gNames = []
	cg = CurrentGlyph()
	if cg is not None:
		gNames.append(cg.name)
	for g in f:
		if g.selected == True:
			if g.name not in gNames:
				gNames.append(g.name)
	return gNames

def get_names_from_path(fontpath):
	_file = os.path.basename(fontpath)
	_file_name = os.path.splitext(_file)[0]
	try:
		family_name, style_name = _file_name.split('_')
	except ValueError:
		family_name, style_name = _file_name.split('-')
	return '%s %s' % ( family_name, style_name )
