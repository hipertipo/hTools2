colors = ximport("colors")

import os

import hTools.tools.ETools_NodeBoxTools
reload(hTools.tools.ETools_NodeBoxTools)

from robofab.world import RFont, OpenFont
from hTools.tools.ETools_NodeBoxTools import NodeBoxPen, ESprite

class ESymbolsCSS:
	
	_ufo_path = u"/Users/gferreira0/Dropbox/hipertipo/hFonts/_ESymbols/_ufos/ESymbols_17.ufo"
	_ignore = [ '', '_element' ]
	_base_path = u"/ESprites/"
	
	def __init__(self):
		self._font = RFont(self._ufo_path)
		for group in self._font.groups.keys():
			for gName in self._font.groups[group]:
				if gName not in self._ignore:
					print '%s%s.png' % (self._base_path, gName)

C = ESymbolsCSS()

