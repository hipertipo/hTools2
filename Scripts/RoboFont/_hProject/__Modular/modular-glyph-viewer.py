import os

from vanilla import *
from mojo.canvas import Canvas
from mojo.drawingTools import *

from robofab.world import RFont, RGlyph
from fontTools.pens.basePen import BasePen

from hTools2.objects import hProject, hGlyph_base
from hTools2.modules.pens import RoboFontPen
from hTools2.modules.fileutils import get_names_from_path
from hTools2.modules.colorsys import hsv_to_rgb
from hTools2.modules.nodebox import gridfit

class ModularGlyphViewer:

    _title = 'Modular Glyph Viewer'

    _width = 800
    _height = 400

    _canvas_height = 1000
    _canvas_width = 1000

    _padding = 10
    _gridsize = 24
    _grid_res = 1

    _ufos = []
    _glyphs = []

    _col_1 = 120
    _col_2 = 160
    _row_height = 30

    _sizes = '17'
    _weights = '1 2 3'
    _resolutions = '1'

    
    def __init__(self):
        self.hGlyph = hGlyph_base('a', hProject('Modular'))
        self.w = Window((self._width, self._height), minSize=(200, 200), title=self._title)
        # glyph name input
        self.w.glyph_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 0),
            self._col_1,
            22),
            text='glyph')
        self.w.glyph_input = EditText(
            (self._col_1,
            self._padding + (self._row_height * 0),
            self._col_2,
            20),
            text = 'a',
            callback = self.glyph_callback)
        # gridsize slider
        self.w.gridsize_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 1),
            self._col_1,
            22),
            text='grid size')
        self.w.gridsize_slider = Slider(
            (self._col_1,
            self._padding + (self._row_height * 1),
            self._col_2,
            20),
            value = self._gridsize,
            minValue = self._gridsize/2,
            maxValue = 60,
            callback = self.sliderCallback)
        # sizes input
        self.w.sizes_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 2),
            100,
            22),
            text='sizes')
        self.w.sizes_input = EditText(
            (self._col_1,
            self._padding + (self._row_height * 2),
            self._col_2,
            20),
            text = self._sizes,
            callback = self.sizes_callback)
        # weights input
        self.w.weights_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 3),
            100,
            22),
            text='weights')
        self.w.weights_input = EditText(
            (self._col_1,
            self._padding + (self._row_height * 3),
            self._col_2,
            20),
            text = self._weights,
            callback = self.weights_callback)
        # resolutions input
        self.w.resolutions_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 4),
            100,
            22),
            text='resolutions')
        self.w.resolutions_input = EditText(
            (self._col_1,
            self._padding + (self._row_height * 4),
            self._col_2,
            20),
            text = self._resolutions,
            callback = self.resolutions_callback)
        # fontlist button
        self.w.fontlist_button = Button(
            (self._padding,
            -35,
            self._col_1 + self._col_2,
            20),
            'update canvas',
            callback=self.fontlist_callback)
        # canvas
        self.w.canvas = Canvas(
            ((self._padding*2) + self._col_1 + self._col_2, 0, -0, -0),
            canvasSize = (self._canvas_width, self._canvas_height),
            delegate = self,
            acceptsMouseMoved = False)
        # open window
        self.w.open()

    #--------------
    # UI callbacks
    #--------------
    
    def sliderCallback(self, sender):
        self._gridsize = int(sender.get())
        self.w.canvas.update()

    def sizes_callback(self, sender):
        self._sizes = self.w.sizes_input.get()

    def weights_callback(self, sender):
        self._weights = self.w.weights_input.get()

    def resolutions_callback(self, sender):
        self._resolutions = self.w.resolutions_input.get()

    def glyph_callback(self, sender):
        self.hGlyph.gName = sender.get()

    def fontlist_callback(self, sender):
        # get parameters
        self._ufo_paths = []
        self._ufos = []
        # get font paths
        for _sz in self._sizes.split(' '):
            for _wt in self._weights.split(' '):
                for _rs in self._resolutions.split(' '):
                    _ufo_name = '%s_%s-%s-%s.ufo' % (self.hGlyph.project.name, _sz, _wt, _rs)
                    _ufo_path = os.path.join(self.hGlyph.project.paths['ufos'], _ufo_name)
                    if os.path.exists(_ufo_path):
                        _ufo = RFont(_ufo_path, showUI=False)
                        self._ufos.append(_ufo)
        self.w.canvas.update()

    #----------------------
    # custom drawing stuff
    #----------------------

    def drawGrid(self):
        fill(.9)
        stroke(None)
        x = self._gridsize/self._grid_res
        y = self._gridsize/self._grid_res
        x, y = gridfit(x, y, self._gridsize/self._grid_res)
        while x < self._canvas_width:
            rect(x, 0, 1, self._canvas_height)
            x += self._gridsize/self._grid_res
        while y < self._canvas_height:
            rect(0, y, self._canvas_width, 1)
            y += self._gridsize/self._grid_res

    def drawOrigin(self):
        x = 5 * self._gridsize
        y = 5 * self._gridsize
        x, y = gridfit(x, y, self._gridsize/self._grid_res)
        fill(.7)
        rect(x, 0, 1, self._canvas_height)
        rect(0, y, self._canvas_width, 1)

    def drawGlyphs(self):
        if len(self._ufos) > 0:
            _color_step =  1.0 / len(self._ufos)
            _alpha = 0.3 + (_color_step / 3)
            _units_per_element = 120
            x = 5 * self._gridsize
            y = 5 * self._gridsize
            x, y = gridfit(x, y, self._gridsize/self._grid_res)
            save()
            translate(x, y)
            scale((1.0 / _units_per_element) * self._gridsize)
            for ufo in self._ufos:
                glyph = ufo[self.hGlyph.gName]
                pen = RoboFontPen(glyphSet=ufo)
                # make color
                R, G, B = hsv_to_rgb(0.5 + _color_step / 10, 1.0, 1.0)
                fill(R, G, B, _alpha)
                # draw glyph
                newPath()
                glyph.draw(pen)
                drawPath()
                _color_step += _color_step
            restore()

    #-------------------------
    # canvas delegate methods
    #-------------------------
    
    def draw(self):
        self.drawGrid()
        self.drawOrigin()
        self.drawGlyphs()
    
    def mouseDown(self, event):
        #print event
        pass


ModularGlyphViewer()    
