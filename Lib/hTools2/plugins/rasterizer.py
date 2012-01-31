# hTools2.plugins.rasterizer

from robofab.world import NewFont

from hTools2.modules.primitives import *

class EGlyph:

	def __init__(self, sourceGlyph):
		self.g = sourceGlyph

	def scan(self, res):
		# get margins
		self.leftMargin = self.g.leftMargin / res
		self.rightMargin = self.g.rightMargin / res
		# get bounding box
		xMin = int(self.g.box[0])
		yMin = int(self.g.box[1])
		xMax = int(self.g.box[2])
		yMax = int(self.g.box[3])
		yValues = range(yMin, yMax, res)
		yValues.reverse()
		xValues = range(xMin, xMax, res)
		# scan lines
		lines = {}
		for y in yValues:
			lineNumber = y / res
			bits = []
			for x in xValues:
				if self.g.pointInside((x + (res/2), y + (res/2))):
					bits.append(1,)
				else:
					bits.append(0,)
			lines[str(lineNumber)] = bits
		self.coordenates = lines
		self._save_bits_to_lib()

	def _save_bits_to_lib(self):
		self.g.lib["rasterizer.coordenates"] = self.coordenates
		self.g.lib["rasterizer.margins"] = self.leftMargin, self.rightMargin

	def _read_bits_from_lib(self):
		self.coordenates = self.g.lib["rasterizer.coordenates"]
		self.leftMargin, self.rightMargin = self.g.lib["rasterizer.margins"]

	def _print(self, black="#", white="-"):
		# see if glyph has been scanned already
		if hasattr(self, 'coordenates') is not True:
			try:
				self._read_bits_from_lib()
			except:
				self.scan()
		marginLeft = white
		marginRight = white + ' '
		lineNumbers = self.coordenates.keys()
		belowBase = []
		aboveBase = []
		for l in lineNumbers:
			if l < 0:
				belowBase.append(l)
			else:
				aboveBase.append(l)
		aboveBase.sort()
		aboveBase.reverse()
		belowBase.sort()
		belowBase.reverse()
		print "-" * 30
		print "GlyphRasterizer"
		print "name: %s, leftMargin: %s, rightMargin: %s" % ( self.g.name, self.leftMargin, self.rightMargin )
		print "-" * 30
		print
		for line in aboveBase:
			print "\t", line, "\t", 
			print marginLeft * self.leftMargin,
			for bit in self.coordenates[line]:
				if bit == 1:
					print black,
				else:
					print white,
			print marginRight * self.rightMargin
		for line in belowBase:
			print "\t", line, "\t", 
			print marginLeft * self.leftMargin,
			for bit in self.coordenates[line]:
				if bit == 1:
					print black,
				else:
					print white,
			print marginRight * self.rightMargin
		print
		print "-" * 30, "\n"

	def draw(self, eSize=100, eSpacing=125, eShape=False, destGlyph=None):	
		if destGlyph == None:
			destGlyph = self.g
		# see if glyph has been scanned already
		noLib = False
		if self.g.lib.has_key("rasterizer.coordenates") != True:
			self.scan()
		# make temp glyph
		from robofab.objects.hProjectRF import RGlyph as _RGlyph
		rg = _RGlyph()
		myPen = rg.getPen()
		# prepare lines
		lineNumbers = self.g.lib["rasterizer.coordenates"].keys()
		lineNumbers.sort()
		lineNumbers.reverse()
		# draw elements to temp glyph
		for line in lineNumbers:
			bitCount = 0
			for bit in self.g.lib["rasterizer.coordenates"][line]:
				if bit == 1:
					y = int(line) * eSpacing
					x = bitCount * eSpacing
					# element shape
					if eShape == False:
						rect(myPen, x, y, eSize)
					else:
						oval(myPen, x, y, eSize)	
				bitCount = bitCount + 1
		# copy to destination glyph
		rg.update()
		destGlyph.clear()
		pen = destGlyph.getPointPen()				
		rg.drawPoints(pen)
		# set margins
		destGlyph.leftMargin = self.g.lib["rasterizer.margins"][0] * eSpacing
		destGlyph.rightMargin = (self.g.lib["rasterizer.margins"][1] * eSpacing) + (eSpacing-eSize)
		# paint
		if noLib == False:
			destGlyph.mark = colorNames["green"]
		else:
			destGlyph.mark = colorNames["red"]
		# update
		destGlyph.update()

	def rasterize(self, destGlyph=None, res=125):
		# define destination glyph
		if destGlyph == None:
			destGlyph = self.g
		# see if glyph has been scanned already
		noLib = False
		if self.g.lib.has_key("rasterizer.coordenates") != True:
			self.scan(res)
		# prepare glyphs
		eSource = "_element"
		destGlyph.clear()
		# prepare lines
		lineNumbers = self.g.lib["rasterizer.coordenates"].keys()
		lineNumbers.sort()
		lineNumbers.reverse()
	 	# place components from matrix 
		# eSize = 125
		for line in lineNumbers:
			bitCount = 0
			for bit in self.g.lib["rasterizer.coordenates"][line]:
				if bit == 1:
					x = bitCount * res
					y = int(line) * res
					destGlyph.appendComponent( eSource, (x, y), (1, 1) )
				else:
					pass
				bitCount = bitCount+1
		#set glyph data & update
		destGlyph.leftMargin = self.g.lib["rasterizer.margins"][0] * res
		destGlyph.rightMargin = self.g.lib["rasterizer.margins"][1] * res
		destGlyph.autoUnicodes()
		destGlyph.update()

def checkLib(g):
	if len(g.lib.keys()) != 0:
		return 1
		print 'glyph libs:', g.lib.keys()
	else:
		print "glyph doesn't have any libs.\n"
		return 0

def clearGlyphLibs(g):
	if checkLib(g) == True:
		g.lib = {}
		g.update()

def setElement(f, size, type='rect', magic=None):
	g = f['_element']
	g.clear()
	p = g.getPen()
	if type == 'oval':	
		oval(p, 0, 0, size)
	elif type == 'super':
		element(p, 0, 0, size, magic)
	else:
		rect(p, 0, 0, size)
	g.update()
	f.update()
