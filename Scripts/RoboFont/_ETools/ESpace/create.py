# [e] batch create EFonts

import os

from vanilla import *

from robofab.objects.objectsRF import NewFont

from hTools.tools.ETools import EWorld, EFont, ESpace

class createEFontsDialog(object):

    _title = 'create EFonts' 
    _padding = 10
    _column1 = 60
    _column2 = 320
    _box_height = 20
    _button_height = 25
    _width = _column1 + _column2 + (_padding * 3)
    _height = (_box_height * 4) + _button_height + (_padding * 6)
    _verbose = False

    _styles = "B H S"
    _heights = "01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17"
    _weights = "11 12 21 22 31 32 41 42"
    _widths = "1 2 3 4 5 6 7 8 9"
    _propWidths = False

    def __init__(self):
        self.world = EWorld(mode='ufo')
        self.space = ESpace()
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title)
        # styles
        self.w.styles_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 0),
                self._column1,
                self._box_height),
                "styles:",
                sizeStyle='small')
        self.w.stylesInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 0),
                self._column2,
                self._box_height),
                self._styles,
                sizeStyle='small')
        # heights
        self.w.heights_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 1),
                self._column1,
                self._box_height),
                "heights:",
                sizeStyle='small')
        self.w.heightsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 1),
                self._column2,
                self._box_height),
                self._heights,
                sizeStyle='small')
        # weights
        self.w.weights_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 2),
                self._column1,
                self._box_height),
                "weights:",
                sizeStyle='small')
        self.w.weightsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 2),
                self._column2,
                self._box_height),
                self._weights,
                sizeStyle='small')
        # width
        self.w.widths_label = TextBox(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 3),
                self._column1,
                self._box_height ),
                "widths:",
                sizeStyle='small')
        self.w.widthsInput = EditText(
                ((2 * self._padding) + (1 * self._column1),
                self._padding + ((self._box_height + self._padding) * 3),
                self._column2 / 2,
                self._box_height),
                self._widths,
                sizeStyle='small')
        self.w.propWidthsInput = CheckBox(
                ((3 * self._padding) + (1 * self._column1) + (self._column2 / 2),
                self._padding + ((self._box_height + self._padding) * 3),
                self._column2 / 2,
                self._box_height),
                'proportional widths',
                sizeStyle='small',
                value=self._propWidths)
        self.w.button_open = SquareButton(
                (self._padding,
                self._padding + ((self._box_height + self._padding) * 4),
                -self._padding,
                self._button_height),
                "create EFonts",
                callback=self.open_callback,
                sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def update(self):
        self.space.styles = self.w.stylesInput.get().split()
        self.space.heights = self.w.heightsInput.get().split()
        self.space.weights = self.w.weightsInput.get().split()
        self.space.widths = self.w.widthsInput.get().split()
        self.space.propWidths = self.w.propWidthsInput.get()
        self.space.types = [ 'A' ]
        self.space.compile()
        self.space.buildNames()

    def open_callback(self, sender):
        self.update()
        print "batch creating EFonts...\n"
        for EName in self.space.ENames:
            if EName in self.world.ufoNames:        
                print '\tEFont %s already exists.' % EName
            else:
                f = NewFont()
                ufoPath = os.path.join(self.world.ufosPath, EName+'.ufo')
                print '\tcreating EFont %s.ufo...' % EName
                f.save(destDir=ufoPath)
        print "\n...done.\n"

# run

createEFontsDialog()
