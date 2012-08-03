# [h] a dialog to paint and select glyphs by color

# objects

class paintGlyphsDialog(object):

    'paint and select glyphs by color'

    #------------
    # attributes
    #------------

    _title = 'color'
    _row_height = 25
    _button_height = 30
    _padding = 10
    _padding_top = 10
    _width = 123
    _height = (_button_height * 3) + (_padding * 3)

    _mark_color = random_color()

    #---------
    # methods
    #---------

    def __init__(self):
        self.w = FloatingWindow(
                (self._width, self._height),
                self._title,
                closable=True)
        # mark color
        x = self._padding
        y = self._padding
        self.w.mark_color = ColorWell(
                (x, y,
                -self._padding,
                self._button_height),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        y += self._button_height - 1
        self.w.button_paint = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "paint",
                callback=self.paint_callback,
                sizeStyle='small')
        y += self._button_height + self._padding_top
        self.w.button_select = SquareButton(
                (x, y,
                -self._padding,
                self._button_height),
                "select",
                callback=self.select_callback,
                sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def paint_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            _mark_color = self.w.mark_color.get()
            _mark_color = (_mark_color.redComponent(),
                        _mark_color.greenComponent(),
                        _mark_color.blueComponent(),
                        _mark_color.alphaComponent())
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                print 'painting selected glyphs...\n'
                print '\tcolor: %s %s %s %s' % _mark_color
                print '\tglyphs: %s' % glyph_names
                for glyph_name in glyph_names:
                    f[glyph_name].prepareUndo('paint glyph')
                    f[glyph_name].mark = _mark_color
                    f[glyph_name].performUndo()
                print
                print '...done.\n'
            # no glyph selected
            else:
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'

    def select_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                glyph_name = get_glyphs(f)[0]
                color = f[glyph_name].mark
                print 'selecting glyphs...\n'
                # print '\tcolor: %s %s %s %s' % color
                glyph_names = []
                for glyph in f:
                    if glyph.mark == color:
                        glyph_names.append(glyph.name)
                print '\tglyphs: %s' % glyph_names
                f.selection = glyph_names
                print
                print 'done.\n'
            # no glyph selected
            else:
                print 'please select a glyph first.\n'
        # no font open
        else:
            print 'please open a font first.\n'
