# [h] slide layer 2

from vanilla import *

from mojo.UI import CurrentGlyphWindow, OpenGlyphWindow

from hTools2.modules.fontutils import get_full_name, get_glyphs

# functions

def next_glyph(font, index):
    try:
        next = font.glyphOrder[index+1]
    except IndexError:
        next = font.glyphOrder[0]
    return next

def previous_glyph(font, index):
    try:
        prev = font.glyphOrder[index-1]
    except IndexError:
        prev = font.glyphOrder[-1]
    return prev

# the dialog

class glyphSwitcherDialog(object):

    _title = "switcher"
    _padding_top = 8
    _padding = 10
    _button_1 = 30
    _button_2 = 18
    _line_height = 18
    _box_height = 23
    _width = 320
    _height = (_button_1 * 3) + (_padding_top * 2)

    _move_default = 70

    def __init__(self):
        # get fonts
        self.all_fonts = AllFonts()
        if len(self.all_fonts) > 0:
            self.w = FloatingWindow(
                        (self._width,
                        self._height),
                        self._title)
            # move buttons
            p = self._padding
            b1 = self._button_1
            b2 = self._button_2
            box = self._box_height
            x = self._padding
            y = self._padding_top
            x1 = x + b1 - 1
            x2 = x + (b1 * 2) - 2
            # buttons
            self.w._up = SquareButton(
                        (x1, y,
                        b1, b1),
                        unichr(8673),
                        callback=self._up_callback)
            self.w._up_right = SquareButton(
                        (x2 + 8, y,
                        b1 - 8, b1 - 8),
                        unichr(8599),
                        callback=self._up_right_callback,
                        sizeStyle='small')
            y += b1 - 1
            self.w._left = SquareButton(
                        (x, y,
                        b1, b1),
                        unichr(8672),
                        callback=self._left_callback)
            self.w._right = SquareButton(
                        (x2, y,
                        b1, b1),
                        unichr(8674),
                        callback=self._right_callback)
            y += b1 - 1
            self.w._down = SquareButton(
                        (x1, y,
                        b1, b1),
                        unichr(8675),
                        callback=self._down_callback)
            self.w._down_left = SquareButton(
                        (x, y + 8,
                        b1 - 8, b1 - 8),
                        unichr(8601),
                        callback=self._down_left_callback,
                        sizeStyle='small')
            # location
            y = p
            x3 = x2 + b1 + 16
            self.w.box_font = Box(
                        (x3, y,
                        -self._padding,
                        self._box_height))
            self.w.box_font.text = TextBox(
                        (5, 0,
                        -self._padding,
                        -0),
                        '',
                        sizeStyle='small')
            y += self._box_height + self._padding_top
            self.w.box_glyph = Box(
                        (x3, y,
                        -self._padding,
                        self._box_height))
            self.w.box_glyph.text = TextBox(
                        (5, 0,
                        -self._padding,
                        -0),
                        '',
                        sizeStyle='small')
            y += self._box_height + self._padding_top
            self.w.box_layer = Box(
                        (x3, y,
                        -self._padding,
                        self._box_height))
            self.w.box_layer.text = TextBox(
                        (5, 0,
                        -self._padding,
                        -0),
                        '',
                        sizeStyle='small')
            # open
            if self.update():
                self.w.open()
        else:
            print 'please open at least one font first.\n'

    # methods

    def next_glyph(self):
        next = next_glyph(self.font, self.glyph_index)
        try:
            self.glyph_window.setGlyphByName(next)
        except AttributeError:
            self.glyph_window = CurrentGlyphWindow()
            self.glyph_window.setGlyphByName(next)
        self.update()

    def previous_glyph(self):
        prev = previous_glyph(self.font, self.glyph_index)
        try:
            self.glyph_window.setGlyphByName(prev)
        except AttributeError:
            self.glyph_window = CurrentGlyphWindow()
            self.glyph_window.setGlyphByName(prev)
        self.update()

    def layer_down(self):
        try:
            self.glyph_window.layerDown()
        except AttributeError:
            self.glyph_window = CurrentGlyphWindow()
            self.glyph_window.layerDown()
        self.update()

    def layer_up(self):
        try:
            self.glyph_window.layerUp()
        except AttributeError:
            self.glyph_window = CurrentGlyphWindow()
            self.glyph_window.layerUp()
        self.update()

    def _update_text_box(self):
        self.w.box_font.text.set('%s [%s]' % (get_full_name(self.font), self.font_index))
        self.w.box_glyph.text.set('%s [%s]' % (self.glyph.name, self.glyph_index))
        self.w.box_layer.text.set(self.glyph.layerName)

    def update(self):
        self.glyph_window = CurrentGlyphWindow()
        if self.glyph_window is not None:
            self.glyph = CurrentGlyph()
            self.font = self.glyph.getParent()
            self.glyph_index = self.font.glyphOrder.index(self.glyph.name)
            self.font_index = self.all_fonts.index(self.font)
            self._update_text_box()
            return True
        else:
            f = CurrentFont()
            if f is not None:
                self.font = f
                self.font_index = self.all_fonts.index(self.font)
                glyph_names = get_glyphs(f) 
                if len(glyph_names) > 0:
                    self.glyph = self.font[glyph_names[0]]
                    self.glyph_index = self.font.glyphOrder.index(self.glyph.name)
                    self.glyph_window = OpenGlyphWindow(self.glyph, newWindow=False)
                    self._update_text_box()
                    return True
                else:
                    print 'please select a glyph first.\n'
                    return False
            else:
                print 'please open a font first.\n'
                return False

    # callbacks

    def _left_callback(self, sender):
        self.previous_glyph()

    def _right_callback(self, sender):
        self.next_glyph()

    def _up_callback(self, sender):
        self.layer_up()

    def _down_callback(self, sender):
        self.layer_down()

    def _up_right_callback(self, sender):
        if len(self.all_fonts) > 1:
            # get next font
            f = CurrentFont()
            i = self.all_fonts.index(f)
            try:
                next_i = i + 1
                next_font = self.all_fonts[next_i]
            except IndexError:
                next_i = 0
                next_font = self.all_fonts[next_i]
            # get glyph
            g_current = CurrentGlyph()
            if g_current is not None:
                if next_font.has_key(g_current.name):
                    next_glyph = next_font[g_current.name]
                else:
                    next_glyph = next_font[next_font.glyphOrder[0]]
                # switch to glyph window
                G = OpenGlyphWindow(next_glyph, newWindow=False)            
                # update UI
                self.update()

    def _down_left_callback(self, sender):
        if len(self.all_fonts) > 1:
            # get next font
            f = CurrentFont()
            i = self.all_fonts.index(f)
            try:
                prev_i = i - 1
                prev_font = self.all_fonts[prev_i]
            except IndexError:
                prev_i = -1
                prev_font = self.all_fonts[prev_i]
            # get glyph
            g_current = CurrentGlyph()
            if g_current is not None:
                if prev_font.has_key(g_current.name):
                    prev_glyph = prev_font[g_current.name]
                else:
                    prev_glyph = prev_font[prev_font.glyphOrder[0]]
                # switch to glyph window
                G = OpenGlyphWindow(prev_glyph, newWindow=False)            
                # update UI
                self.update()

# run

glyphSwitcherDialog()
