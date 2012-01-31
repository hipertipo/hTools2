# ETools

import os
from os.path import basename, splitext, join

from robofab.world import OpenFont, NewFont
from robofab.interface.all.dialogs import AskString

from hTools.world import hPaths
from hTools.objects.hProject import hProject

from hTools.tools.PathTools import walk
from hTools.tools.FontInfoTools import clearFontData, setFontNames
from hTools.tools.GenerationTools import generateOne
from hTools.tools.OutlineTools import expandGlyphs
from hTools.tools.VMetricsTools import ttinfoValue


class EWorld:

	def __init__(self, world="MacOSX", mode="ufo"):
		self.world = world
		self.mode = mode
		self.setRoot()
		self.setPaths()
		self.collectFiles()
		self.collectNames()
		self.compileDict()

	# set paths

	def setRoot(self):
		# self.root = '/_Elementar'
		self.root = hPaths["ROOTPATH_OSX"] + "_Elementar"

	def setPaths(self):
		self.vfbsPath = join(self.root)
		self.otfsPath = join(self.root, '_otfs')
		self.ttfsPath = join(self.root, '_ttfs')
		self.ufosPath = join(self.root, '_ufos')

	# get files by formats

	def _ufos(self):
		self.ufos = walk(self.ufosPath, 'ufo')
		return self.ufos

	def _vfbs(self):
		self.vfbs = walk(self.vfbsPath, 'vfb')
		return self.vfbs

	def _otfs(self):
		self.otfs = walk(self.otfsPath, 'otf')
		return self.otfs

	def _ttfs(self):
		self.ttfs = walk(self.ttfsPath, 'otf')
		return self.ttfs

	# get ENames by formats

	def _ufoNames(self):
		self.ufoNames = []
		for ufo in self.ufos:
			self.ufoNames.append(getENameFromPath(ufo))
		return self.ufoNames

	def _vfbNames(self):
		self.vfbNames = []
		for vfb in self.vfbs:
			self.vfbNames.append(getENameFromPath(vfb))
		return self.vfbNames

	def _otfNames(self):
		self.otfNames = []
		for otf in self.otfs:
			self.otfNames.append(getENameFromPath(otf))
		return self.otfNames

	def _ttfNames(self):
		self.ttfNames = []
		for ttf in self.ttfs:
			self.ttfNames.append(getENameFromPath(ttf))
		return self.ttfNames

	# update data

	def collectFiles(self):
		self._vfbs()
		self._ufos()
		self._otfs()
		self._ttfs()

	def collectNames(self):
		self._vfbNames()
		self._ufoNames()
		self._otfNames()
		self._ttfNames()

	def report(self):
		print "vfbsPath: %s" % self.vfbsPath
		print "vfbs: %s\n" % len(self.vfbs)
		print "otfsPath: %s" % self.otfsPath
		print "otfs: %s\n" % len(self.otfs)
		print "ufosPath: %s" % self.ufosPath
		print "ufos: %s\n" % len(self.ufos)
		print "ttfsPath: %s" % self.ttfsPath
		print "ttfs: %s\n" % len(self.ttfs)
	
	def createHeightsDict(self):
		heightParameters = (
			"xHeight",
			"capHeight",
			"ascender",
			"ascender_ft",
			"ascender_num",
			"descender",
			"descender_num",
			"margin_top",
			"margin_bottom",
			"extra_top",
			"extra_bottom"
			)
		heightsTable =	{
			'17' : ( 9, 12, 4, 3, 3, 4, 3, 3, 1, 3, 2 ),
			'16' : ( 9, 12, 4, 3, 3, 3, 2, 3, 1, 3, 2 ),
			'15' : ( 8, 11, 4, 3, 3, 3, 2, 3, 1, 3, 2 ),
			'14' : ( 8, 10, 3, 2, 2, 3, 2, 3, 1, 3, 2 ),
			'13' : ( 7, 9, 3, 2, 2, 3, 2, 3, 1, 3, 2 ),
			'12' : ( 7, 9, 3, 2, 2, 2, 2, 3, 1, 3, 2 ),
			'11' : ( 6, 8, 3, 2, 2, 2, 2, 3, 1, 3, 2 ),
			'10' : ( 6, 8, 2, 1, 2, 2, 2, 3, 1, 3, 2 ),
			'09' : ( 5, 7, 2, 1, 2, 2, 2, 3, 1, 3, 2 ),
			'08' : ( 4, 6, 2, 1, 2, 2, 2, 3, 1, 3, 2 ),
			'07' : ( 4, 5, 1, 1, 1, 2, 2, 3, 1, 3, 2 ),
			'06' : ( 4, 4, 1, 1, 1, 2, 2, 3, 1, 3, 2 ),
			'05' : ( 3, 4, 1, 1, 1, 1, 1, 3, 1, 3, 2 ),
			'04' : ( 2, 3, 1, 1, 1, 1, 1, 3, 1, 3, 2 ),
			'03' : ( 2, 3, 1, 1, 1, 0, 0, 3, 1, 3, 2 ),
			'02' : ( 2, 2, 0, 0, 0, 0, 0, 3, 1, 3, 2 ),
			'01' : ( 1, 1, 0, 0, 0, 0, 0, 3, 1, 3, 2 ),
			}
		vMetricsDict = {}
		for height in heightsTable.keys():
			vMetricsDict[height] = dict(zip(heightParameters, heightsTable[height]))
		self.vMetricsDict = vMetricsDict

	def addENameToDict(self, EName):
		height = EName[2:4]
		self.EDict[EName] = {}
		# set paths
		self.EDict[EName]["vfbPath"] = join(self.vfbsPath, EName + ".vfb")
		self.EDict[EName]["ufoPath"] = join(self.ufosPath, EName + ".ufo")
		self.EDict[EName]["ttfPath"] = join(self.ttfsPath, EName + ".ttf")
		self.EDict[EName]["otfPath"] = join(self.otfsPath, EName + ".otf")
		# set Elementar parameters from EName
		self.EDict[EName]["style"] = EName[1:2]
		self.EDict[EName]["height"] = height
		self.EDict[EName]["vstroke"] = EName[4:5]
		self.EDict[EName]["hstroke"] = EName[5:6]
		self.EDict[EName]["width"] = EName[6:7]
		self.EDict[EName]["type"] = EName[7:8]
		self.EDict[EName]["eSize"] = 1
		self.EDict[EName]["eSpace"] = 0
		self.EDict[EName]["unitsPerElement"] = 125

	def compileDict(self):
		self.createHeightsDict()
		self.EDict = {}
		if self.mode == 'ufo':
			for ufoPath in self.ufos:
				eName = getENameFromPath(ufoPath)
				self.addENameToDict(eName)
		else:
			for vfbPath in self.vfbs:
				eName = getENameFromPath(vfbPath)
				self.addENameToDict(eName)

class ESpace(EWorld):

	styles = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' ]
	heights = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17' ]
	weights = [ '11', '12', '21', '22', '31', '32', '41', '42', '43' ]
	widths = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
	types = [ 'A', 'B' ]
	propWidths = False

	def __init__(self, world="MacOSX", mode="ufo"):
		EWorld.__init__(self, world, mode)
		self.update()

	def compile(self):
		self.parameters = {
			"styles" : self.styles,
			"heights" : self.heights,
			"weights" : self.weights,
			"widths" : self.widths,
			"types" : self.types,
			}

	def buildNames(self):
		self.ENames = []
		for style in self.styles:
			for height in self.heights:
				# proportional widths
				if self.propWidths == True:
					wdCount = -1
					vStroke = 1
					vStroke_prev = None
					for weight in self.weights:
						# decrease width only for vStroke increments 
						vStroke_prev, vStroke = vStroke, weight[0]
						if vStroke > vStroke_prev:
							wdCount = wdCount + 1
						for wd in range(len(self.widths)-wdCount):
							width = self.widths[wd]
							for type in self.types:
								EName = "E%s%s%s%s%s" % ( style, height, weight, width, type )
								self.ENames.append(EName)
				# nummerical widths
				else:
					for weight in self.weights:
						for width in self.widths:
							for type in self.types:
								EName = "E%s%s%s%s%s" % ( style, height, weight, width, type )
								self.ENames.append(EName)

	def update(self):
		self.compile()
		self.compileDict()
		self.buildNames()
		self.buildColors()

	def buildColors(self):
		self.colorsDict = {}
		for _ht in range(len(self.heights)):
			ht = self.heights[_ht]
			for _wt in range(len(self.weights)):
				wt = self.weights[_wt]
				for _wd in range(len(self.widths)):
					wd = self.widths[_wd]
					E = "%s%s%s" % (ht, wt, wd)
					# colors
					c_ht = ( 1.0 / len(self.heights) ) * (_ht+1)
					c_wt = ( 1.0 / len(self.weights) ) * (_wt+1)
					c_wd = ( 1.0 / len(self.widths) ) * (_wd+_wt+1) # prop widths
					# inverted colors
					_c_ht = 1 - ( 1.0 / len(self.heights) ) * (_ht+1)
					_c_wt = 1 - ( 1.0 / len(self.weights) ) * (_wt)
					_c_wd = 1 - ( 1.0 / len(self.widths) ) * (_wd+_wt) # prop widths
					# self.colorsDict[E] = (_c_ht, c_wt, _c_wd) # cmyk
					self.colorsDict[E] = (c_ht, _c_wt, c_wd) # rgb

	def openVFBs(self):
		print "opening vfbs..."
		for EName in self.existingVFBs():
			e = EFont(EName, self)
			f = e.openVFB(setInfo=True)
		print "...done.\n"

	def existingVFBs(self):
		existingVFBs = []
		for name in self.ENames:
			if name in self.vfbNames:
				existingVFBs.append(name)
		return existingVFBs

	def existingUFOs(self):
		existingUFOs = []
		for name in self.ENames:
			if name in self.ufoNames:
				existingUFOs.append(name)
		return existingUFOs

	def existingOTFs(self):
		existingOTFs = []
		for name in self.ENames:
			if name in self.otfNames:
				existingOTFs.append(name)
		return existingOTFs

class EFont:
	
	eSize = 1
	eSpace = 0
	unitsPerElement = 125
	encoding = 'Std'

	def __init__(self, EName, ESpace):
		self.EName = EName
		# EParameters
		self.style = ESpace.EDict[EName]['style']
		self.height = ESpace.EDict[EName]['height']
		self.vstroke = ESpace.EDict[EName]['vstroke']
		self.hstroke = ESpace.EDict[EName]['hstroke']
		self.width = ESpace.EDict[EName]['width']
		self.type = ESpace.EDict[EName]['type']
		# vMetrics
		self.vMetrics = ESpace.vMetricsDict[self.height]
		# paths
		self.vfbPath = ESpace.EDict[EName]["vfbPath"]
		self.ufoPath = ESpace.EDict[EName]["ufoPath"]

	def createELibs(self, f):
		elementar = {
			"EName" : self.EName,
			"style" : self.style,
			"height" : self.height,
			"vstroke" : self.vstroke,
			"hstroke" : self.hstroke,
			"width" : self.width,
			"type" : self.type,
			"eSize" : self.eSize,
			"eSpace" : self.eSpace,
			"emsPerElement" : self.emsPerElement
			}
		paths = {
			"ufoPath" : self.ufoPath,
			"vfbPath" : self.vfbPath
			}
		f.lib['elementar'] = elementar
		f.lib['paths'] = paths
		f.lib['vMetrics'] = self.vMetrics
		f.update()

	def openVFB(self, setInfo=False):
		f = OpenFont(self.vfbPath)
		if setInfo == True:
			clearFontData(f)
			setENames(f, self)
			setEMetrics(f, self)
		f.lib["project"] = "Elementar"
		return f

	def importUFO(self):
		# use this function in FontLab
		f = NewFont()
		try:
			f.readUFO(self.ufoPath, doProgress=True)
		except:
			print '%s does not exist, creating empty font.' % self.EName
		return f

	def openUFO(self):
		# use this function in NoneLab
		f = OpenFont(self.ufoPath)
		return f

	def saveToUfo(self, f):
		f.writeUFO(self.ufoPath, doProgress=False)

class EName:

	_EStyles = {
		'B' : 'Sans A',
		'H' : 'Sans B',
		'C' : 'Sans C',
		'D' : 'Sans D',
		'U' : 'Sans E',
		'G' : 'Sans G',
		'I' : 'Italic A',
		'S' : 'Serif A',
		'Z' : 'Serif B',
		'Y' : 'Mono A',
		}
	encoding = 'Std'

	def __init__(self, eName):
		self.style = eName[1:2]
		self.height = eName[2:4]
		self.weight = eName[4:6]
		self.width = eName[6:7]
		self.type = eName[7:8]

	def styleName(self):
		return self._EStyles[self.style]

	def name(self):
		return 'E%s%s%s%s%s' % ( self.style, self.height, self.weight, self.width, self.type )

	def longName(self):
		return 'Elementar %s %s %s %s' % ( self.styleName(), self.height, self.weight, self.width)

	def otfName(self, mode=0):
		#--------------------
		# mode 0: long name
		# mode 1: short name
		#--------------------
		if mode == 1:
			fontFileName = self.name()
		else:
			fontFileName = "Elementar %s %s - %s %s %s" % ( self.styleName(), self.encoding, self.height, self.weight, self.width )
			fontFileName = ''.join(fontFileName.split())
		return fontFileName

def getENameFromPath(path):
	filename = basename(path)
	EName = splitext(filename)[0]
	return EName

def setENames(f, e, mode=None, element=None):
	# mode 1 : EB13113A | Regular
	if mode == 1:
		styleName = 'Regular'
		if element:
			eShape, eSize = element
			familyName = 'E%s%s%s%s%s%s%s%s' % (e.style, e.height, e.vstroke, e.hstroke, e.width, e.type, eShape, eSize)
			
		else:
			familyName = 'E%s%s%s%s%s%s' % (e.style, e.height, e.vstroke, e.hstroke, e.width, e.type)
	# mode 2 : Elementar Sans A Std | 13 11 3 
	elif mode == 2:
		encoding = 'Std'
		E = EName(e.EName)
		familyName = 'Elementar %s %s' % ( E.styleName(), encoding )
		if element:
			eShape, eSize = element
			styleName = '%s %s%s %s %s %s' % ( e.height, e.vstroke, e.hstroke, e.width, eShape, eSize )
		else:
			styleName = '%s %s%s %s' % ( e.height, e.vstroke, e.hstroke, e.width )
	# mode 0 : Elementar | B 13 11 3 A
	else:
		familyName = 'Elementar'
		if element:
			eShape, eSize = element		
			styleName = '%s %s %s%s %s %s %s %s' % (e.style, e.height, e.vstroke, e.hstroke, e.width, e.type, eShape, eSize)
		else:
			styleName = '%s %s %s%s %s %s' % (e.style, e.height, e.vstroke, e.hstroke, e.width, e.type)
	# set names
	setFontNames(f, familyName, styleName)
	f.update()

def setEMetrics(f, e):
	# main metrics info
	f.info.unitsPerEm = int(e.height) * e.unitsPerElement
	f.info.xHeight = e.vMetrics["xHeight"] * e.unitsPerElement
	f.info.ascender = (e.vMetrics["ascender"] + e.vMetrics["xHeight"]) * e.unitsPerElement
	f.info.descender = - e.vMetrics["descender"] * e.unitsPerElement
	f.info.capHeight = e.vMetrics["capHeight"] * e.unitsPerElement
	# linespacing etc
	naked = f.naked()
	naked.underline_position = -250
	naked.underline_thickness = 125
	ttMagic = naked.ttinfo.head_units_per_em / float(f.info.unitsPerEm)
	naked.ttinfo.hhea_ascender = ttinfoValue(f.info.ascender, ttMagic)
	naked.ttinfo.hhea_descender = ttinfoValue(f.info.descender, ttMagic)
	naked.ttinfo.hhea_line_gap = 0
	naked.ttinfo.os2_s_typo_ascender = ttinfoValue( f.info.ascender, ttMagic)
	naked.ttinfo.os2_s_typo_descender = ttinfoValue(f.info.descender, ttMagic)
	naked.ttinfo.os2_s_typo_line_gap = 0
	naked.ttinfo.os2_us_win_ascent = ttinfoValue(f.info.ascender, ttMagic)
	naked.ttinfo.os2_us_win_descent = ttinfoValue(-f.info.descender, ttMagic)
	# done
	f.update()

def setFlashMetrics(f):
	# basic dimensions
	f.info.unitsPerEm = 1000
	f.info.ascender = 1125
	f.info.descender = -250
	f.info.capHeight = 875
	f.info.xHeight = 625
	# linespacing etc
	naked = f.naked()
	naked.underline_position = -250
	naked.underline_thickness = 125
	ttMagic = naked.ttinfo.head_units_per_em / float(f.info.unitsPerEm)
	naked.ttinfo.hhea_ascender = ttinfoValue(1125, ttMagic)
	naked.ttinfo.hhea_descender = ttinfoValue(-250, ttMagic)
	naked.ttinfo.hhea_line_gap = 0
	naked.ttinfo.os2_s_typo_ascender = ttinfoValue(1125, ttMagic)
	naked.ttinfo.os2_s_typo_descender = ttinfoValue(-250, ttMagic)
	naked.ttinfo.os2_s_typo_line_gap = 0
	naked.ttinfo.os2_us_win_ascent = ttinfoValue(1125, ttMagic)
	naked.ttinfo.os2_us_win_descent = ttinfoValue(250, ttMagic)
	# done
	f.update()

def generateEFont(f, adobe=False, revert=False, rOverlap=False, close=False, encoding=None, mode=1, format='otf', elements=False):
	'''generate Elementar font'''
	p = hProject("Elementar")
	E = EName(getENameFromPath(f.path))
	# remove overlap
	if rOverlap == True:
		OutlineTools.removeOverlap(f)
	# get encoding
	if encoding == None:
		encoding = ''
	# rename element fonts
	if elements == True:
		E.type = 'A'
		# -----------------------------------------
		# mode 0: Elementar | B 13 11 3 A
		# mode 1: EB13113A | Regular
		# mode 2: Elementar Sans A Std | 13 11 3 
		# -----------------------------------------
		#e = EFont(E.name(), )
		#setENames(f, E, mode=2)
	# create font file name
	if mode == 1:
		fontFileName = E.name()
	else:
		fontFileName = E.otfName()		
	# choose font format
	if format == "ttf":
		_format = "otfttf"
		fontFilePath = os.sep.join( [p.ttfsPath, fontFileName])
	else:
		_format = "otfcff"		
		fontFilePath = os.sep.join( [p.otfsPath, fontFileName])
	# generate font in project folder
	f.generate(_format, fontFilePath)
	# generate font 'adobe/fonts/'
	if adobe == True:
		adobeFontsPath = os.sep.join( [hPaths['ADOBE_FONTS_OSX'], '_Elementar', fontFileName])
		f.generate(_format, adobeFontsPath)
	# revert to last saved
	if revert == True:
		fl.CallCommand(33233)
		loadEncoding(f, p.encodingPath)
		f.update()
	# close font without saving
	if close == True:
		f.close()