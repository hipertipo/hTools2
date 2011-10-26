# fileutils

import os

def walk(folder, extension):
	files = []
	names = os.listdir(folder)
	for n in names:
		p = os.path.join(folder, n)
		if n[-3:] == extension:
			files.append(p)
	return files

def deleteFiles(fileList):
	for f in fileList:
		os.remove(f)

def getGlyphs(f):
	gNames = []
	cg = CurrentGlyph()
	if cg is not None:
		gNames.append(cg.name)
	for g in f:
		if g.selected == True:
			if g.name not in gNames:
				gNames.append(g.name)
	return gNames
