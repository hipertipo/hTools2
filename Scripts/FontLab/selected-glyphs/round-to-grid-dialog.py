# [h] round to grid dialog

'''shift all points above/below movable line'''

from robofab.world import CurrentFont, CurrentGlyph
from dialogKit import *

from hTools2.modules.color import *
from hTools2.modules.glyphutils import roundPointsToGrid, roundAnchorsToGrid, roundMargins

# from hTools.tools.ColorTools import randomColor
# from hTools.tools.UFOTools import getGlyphs
# from hTools.tools.OutlineTools import selectPoints, deselectPoints, shiftSelectedPoints

# --------------------------------------------------------------------------
#  dialog

class RoundToGridDialog(object):

	_points = True
	_anchors = True
	_sidebearings = True
	_mark = True
	_mark_color = randomColor_FL()
	_gridsize = 30

	_height = 235
	_column_1 = 120
	_title = 'round to grid'
	_padding_top = 10
	_padding = 10
	_bWidth = 80
	_row_height = 30
	_bSpacing = 0

	def __init__(self):
		self._width = self._column_1 + self._bWidth + (self._padding_top * 3)
		self.w = ModalDialog(
				(self._width,
				self._height),
				self._title,
				okCallback=self.okCallback)
		# grid size
		self.w.gridsize_label = TextBox(
				(self._padding,
				self._padding_top + (self._row_height * 0),
				self._column_1,
				self._row_height),
				"grid size:")
		self.w.gridsize_value = EditText(
				(self._column_1,
				self._padding_top + (self._row_height * 0),
				self._bWidth,
				self._row_height),
				self._gridsize,
				callback=self.gridsize_callback)
		# points
		self.w.points_checkbox = CheckBox(
				(self._padding,
				self._padding_top + (self._row_height * 1),
				-0,
				self._row_height),
				"points",
				callback=self.points_callback,
				value=self._points)
		# anchors
		self.w.anchors_checkbox = CheckBox(
				(self._padding,
				self._padding_top + (self._row_height * 2),
				-0,
				self._row_height),
				"anchors",
				callback=self.anchors_callback,
				value=self._anchors)
		# side-bearings
		self.w.sidebearings_checkbox = CheckBox(
				(self._padding,
				self._padding_top + (self._row_height * 3),
				-0,
				self._row_height),
				"side-bearings",
				callback=self.sidebearings_callback,
				value=self._sidebearings)
		# mark
		self.w.mark_checkbox = CheckBox(
				(self._padding,
				self._padding_top + (self._row_height * 4),
				-0,
				self._row_height),
				"mark",
				callback=self.mark_callback,
				value=True)
		# apply
		self.w.apply_button = Button(
				(self._padding,
				(2 * self._padding) + ((self._row_height) * 4),
				self._width - (2 * self._padding_top),
				self._row_height),
				'apply',
				callback=self.apply_callback)
		# open window
		self.w.open()

	def gridsize_callback(self, sender):
		self._gridsize = sender.get()

	def points_callback(self, sender):
		self._points = sender.get()

	def anchors_callback(self, sender):
		self._anchors = sender.get()

	def sidebearings_callback(self, sender):
		self._sidebearings = sender.get()

	def mark_callback(self, sender):
		self._mark = sender.get()

	def apply_callback(self, sender):
		self.font = CurrentFont()
		if self.font is not None:
			gNames = self.font.selection
			if len(gNames) > 0:
				print 'rounding glyphs to grid...\n'
				print '\tgrid size: %s' % self._gridsize
				print '\tpoints: %s' % self._points
				print '\tanchors: %s' % self._anchors
				print '\tside-bearings: %s' % self._sidebearings
				print '\tmark: %s' % self._mark
				print '\t',
				for gName in gNames:
					print gName,
					if self._points:
						roundPointsToGrid(self.font[gName], (self._gridsize, self._gridsize))
					if self._anchors:
						roundAnchorsToGrid(self.font[gName], (self._gridsize, self._gridsize))
					if self._sidebearings:
						roundMargins(self.font[gName], self._gridsize, left=True, right=True)
					if self._mark:
						self.font[gName].mark = self._mark_color
					self.font[gName].update()
				print
				self.font.update()
				print '\n...done.\n'
			
	def okCallback(self, sender):
		# print "...done.\n"
		pass

#------
# run!
#------

RoundToGridDialog()

