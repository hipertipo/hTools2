# [h] transform selected glyphs

from vanilla import *
from AppKit import NSColor

class transformSelectedGlyphsDialog(object):

    _title = 'transform selected glyphs'
    _clear = False
    _round = False
    _decompose = False
    _order = False
    _direction = False
    _overlaps = False
    _extremes = False
    _mark = True
    _gNames = []
    _mark_color = (1, 0, 0, 1)
    _width = 220
    _height = 285
    _row_height = 25
    _padding = 15
    _padding_top = 10

    def __init__(self):
        self.w = FloatingWindow(
            (self._width, self._height),
            self._title,
            closable=False)
        # checkboxes
        self.w.clear_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 0),
            -self._padding,
            20),
            "clear outlines",
            callback = self.clear_Callback,
            value = self._clear)
        self.w.round_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 1),
            -self._padding,
            20),
            "round point positions",
            callback = self.round_Callback,
            value = self._round)
        self.w.decompose_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 2),
            -self._padding,
            20),
            "decompose",
            callback = self.decompose_Callback,
            value = self._decompose)
        self.w.order_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 3),
            -self._padding,
            20),
            "auto contour order",
            callback = self.order_Callback,
            value = self._order)
        self.w.direction_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 4),
            -self._padding,
            20),
            "auto contour direction",
            callback = self.direction_Callback,
            value = self._direction)
        self.w.overlaps_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 5),
            -self._padding,
            20),
            "remove overlaps",
            callback = self.overlaps_Callback,
            value = self._overlaps)
        self.w.extremes_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 6),
            -self._padding,
            20),
            "add extreme points",
            callback = self.extremes_Callback,
            value = self._extremes)
        # mark
        self.w.line = HorizontalLine(
            (self._padding,
            self._padding_top + (self._row_height * 7) + 10,
            -self._padding,
            1))
        self.w.mark_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 8),
            -self._padding,
            20),
            "mark",
            callback = self.mark_Callback,
            value=self._mark)
        self.w.mark_color = ColorWell(
            (80,
            self._padding_top + (self._row_height * 8),
            -self._padding,
            20),
            color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_apply = Button(
            (self._padding,
            -55,
            (self._width/2) - 20,
            0),
            "apply",
            callback = self.apply_Callback)
        self.w.button_close = Button(
            ((self._width/2) + 5,
            -55,
            -self._padding,
            0),
            "close",
            callback = self.close_Callback)
        self.w.open()

    def clear_Callback(self, sender):
        self._clear = sender.get()

    def round_Callback(self, sender):
        self._round = sender.get()

    def decompose_Callback(self, sender):
        self._decompose = sender.get()

    def order_Callback(self, sender):
        self._order = sender.get()

    def direction_Callback(self, sender):
        self._direction = sender.get()

    def overlaps_Callback(self, sender):
        self._overlaps = sender.get()

    def extremes_Callback(self, sender):
        self._extremes = sender.get()

    def mark_Callback(self, sender):
        self._mark = sender.get()

    def apply_Callback(self, sender):
        f = CurrentFont()
        if f is not None:
            _mark_color = self.w.mark_color.get()
            _mark_color = (
                _mark_color.redComponent(),
                _mark_color.greenComponent(),
                _mark_color.blueComponent(),
                _mark_color.alphaComponent())
            print 'transforming selected glyphs...\n'
            for gName in f.selection:
                try:
                    print '\ttransforming %s...' % gName
                    if self._clear:
                        print '\tdeleting outlines %s' % gName
                        f[gName].prepareUndo('clear glyph contents')
                        f.newGlyph(gName, clear=True)
                        f[gName].performUndo()
                    if self._round:
                        print '\trounding %s' % gName
                        f[gName].prepareUndo('round point positions')
                        f[gName].round()
                        f[gName].performUndo()
                    if self._decompose:
                        print '\t\tdecomposing...'
                        f[gName].prepareUndo('decompose')
                        f[gName].decompose()
                        f[gName].performUndo()
                    if self._overlaps:
                        print '\t\tremoving overlaps...'
                        f[gName].prepareUndo('remove overlaps')
                        f[gName].removeOverlap()
                        f[gName].performUndo()
                    if self._extremes:
                        print '\t\tadding extreme points...'
                        f[gName].prepareUndo('add extreme points')
                        f[gName].extremePoints()
                        f[gName].performUndo()
                    if self._order:
                        print '\t\tauto contour order...'
                        f[gName].prepareUndo('auto contour order')
                        f[gName].autoContourOrder()
                        f[gName].performUndo()    
                    if self._direction:
                        print '\t\tauto contour direction...'
                        f[gName].prepareUndo('auto contour directions')
                        f[gName].correctDirection()
                        f[gName].performUndo()
                    if self._mark:
                        print '\t\tmark glyphs...'
                        f[gName].prepareUndo('mark')
                        f[gName].mark = _mark_color
                        f[gName].performUndo()
                    print
                except:
                    print '\tcannot transform %s\n' % gName
            # done
            print '...done.\n'
        # no font open 
        else:
            print 'please open a font.\n'

    def close_Callback(self, sender):
        self.w.close()

# run

transformSelectedGlyphsDialog()

