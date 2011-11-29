# [h] round to grid dialog

from AppKit import NSColor
from vanilla import * 

from robofab.world import CurrentFont

from hTools2.modules.glyphutils import alignPointsToGrid, alignAnchorsToGrid, roundMargins

# dialog

class roundToGridDialog(object):

    _title = 'round to grid'
    _gNames = []
    _width = 200
    _height = 210
    _gridsize = 120
    _mark_color = (0, 1, .5, 1)
    _mark = True

    _points = True
    _sidebearings = True
    _anchors = True
    _padding = 15
    _padding_top = 10
    _row_height = 25

    def __init__(self):
        self.w = FloatingWindow(
            (self._width, self._height),
            self._title,
            closable=False)
        # grid size
        self.w._gridsize_label = TextBox(
            (self._padding,
            self._padding_top + (self._row_height * 0),
            -self._padding,
            17),
            "grid size")
        self.w._gridsize_value = EditText(
            (100,
            self._padding_top + (self._row_height * 0),
            -self._padding,
            21),
            text = self._gridsize)
        # division
        self.w._line = HorizontalLine(
            (self._padding,
            self._padding_top + (self._row_height * 1) + 10,
            -self._padding,
            1))
        # points
        self.w._points_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 2),
            -self._padding,
            20),
            "point positions",
            value=self._points)
        # sidebearings
        self.w._sidebearings_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 3),
            -self._padding,
            20),
            "side-bearings",
            value=self._sidebearings)
        # anchors
        self.w._anchors_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 4),
            -self._padding,
            20),
            "anchor positions",
            value=self._anchors)
        # mark
        self.w._mark_checkBox = CheckBox(
            (self._padding,
            self._padding_top + (self._row_height * 5),
            -self._padding,
            20),
            "mark",
            value=self._mark)
        self.w._mark_color = ColorWell(
            (80,
            self._padding_top + (self._row_height * 5),
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
            callback=self.close_Callback)
        self.w.open()

    def apply_Callback(self, sender):
        f = CurrentFont()
        if f is not None:
            print 'processing selected glyphs...\n'
            # get options
            boolstring = [False, True]
            _points = self.w._points_checkBox.get()
            _sidebearings = self.w._sidebearings_checkBox.get()
            _anchors = self.w._anchors_checkBox.get()
            # get color
            _gridsize = int(self.w._gridsize_value.get())
            _mark = self.w._mark_checkBox.get()
            _mark_color = self.w._mark_color.get()
            _mark_color = (_mark_color.redComponent(),
                _mark_color.greenComponent(),
                _mark_color.blueComponent(),
                _mark_color.alphaComponent())
            print '\tgrid size: %s' % _gridsize
            print '\talign points to grid: %s' % boolstring[_points]
            print '\talign side-bearings: %s' % boolstring[_sidebearings]
            print '\talign anchors: %s' % boolstring[_anchors]
            print '\tmark glyphs: %s (%s)' % (boolstring[_mark], _mark_color)
            print
            print '\t', 
            # batch do stuff
            for gName in f.selection:
                print gName,
                f[gName].prepareUndo('align to grid')
                if _points:
                    roundPointsToGrid(f[gName], (_gridsize, _gridsize))
                if _anchors:
                    roundAnchorsToGrid(f[gName], (_gridsize, _gridsize))
                if _sidebearings:
                    roundMargins(f[gName], _gridsize, left=True, right=True)
                if _mark:
                    f[gName].mark = _mark_color
                f[gName].update()
                f[gName].performUndo()
            # done
            print
            f.update()
            print '\n...done.\n'
                        
    def close_Callback(self, sender):
        self.w.close()

# run

roundToGridDialog()

