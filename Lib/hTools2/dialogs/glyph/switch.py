# [h] switch glyph dialog

# imports

from vanilla import *

try:
    from mojo.roboFont import AllFonts, CurrentFont, CurrentGlyph
    from mojo.UI import CurrentGlyphWindow, OpenGlyphWindow
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts, CurrentFont, CurrentGlyph

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

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

# objects

class switchGlyphDialog(hDialog):

    """A dialog to navigate through glyphs, fonts and layers of all open fonts.

    .. image:: imgs/glyph/switch.png

    """

    # methods

    def __init__(self):
        # get fonts
        self.get_fonts()
        if len(self.all_fonts) > 0:
            self.title = "switch"
            self.text_height += 3
            self.square_button -= 4
            self.height = (self.square_button * 3) + (self.padding_y * 2)
            self.width = 320
            self.w = FloatingWindow((self.width, self.height), self.title)
            # move buttons
            x = self.padding_x
            y = self.padding_y
            x1 = x + (self.square_button * 1) - 1
            x2 = x + (self.square_button * 2) - 2
            self.w._up = SquareButton(
                        (x1, y,
                        self.square_button,
                        self.square_button),
                        unichr(8673),
                        callback=self._up_callback)
            self.w._up_right = SquareButton(
                        (x2 + 8, y,
                        self.square_button - 8,
                        self.square_button - 8),
                        unichr(8599),
                        callback=self._up_right_callback,
                        sizeStyle=self.size_style)
            y += self.square_button - 1
            self.w._left = SquareButton(
                        (x, y,
                        self.square_button,
                        self.square_button),
                        unichr(8672),
                        callback=self._left_callback)
            self.w._right = SquareButton(
                        (x2, y,
                        self.square_button,
                        self.square_button),
                        unichr(8674),
                        callback=self._right_callback)
            y += self.square_button - 1
            self.w._down_left = SquareButton(
                        (x, y + 8,
                        self.square_button - 8,
                        self.square_button - 8),
                        unichr(8601),
                        callback=self._down_left_callback,
                        sizeStyle=self.size_style)
            self.w._down = SquareButton(
                        (x1, y,
                        self.square_button,
                        self.square_button),
                        unichr(8675),
                        callback=self._down_callback)
            # location
            y = self.padding_y
            x3 = x2 + self.square_button + 16
            self.w.box_font = Box(
                        (x3, y,
                        -self.padding_x,
                        self.text_height))
            self.w.box_font.text = TextBox(
                        (5, 0,
                        -self.padding_x,
                        -0),
                        '',
                        sizeStyle=self.size_style)
            y += self.text_height + self.padding_y
            self.w.box_glyph = Box(
                        (x3, y,
                        -self.padding_x,
                        self.text_height))
            self.w.box_glyph.text = TextBox(
                        (5, 0,
                        -self.padding_x,
                        -0),
                        '',
                        sizeStyle=self.size_style)
            y += self.text_height + self.padding_y
            self.w.box_layer = Box(
                        (x3, y,
                        -self.padding_x,
                        self.text_height))
            self.w.box_layer.text = TextBox(
                        (5, 0,
                        -self.padding_x,
                        -0),
                        '',
                        sizeStyle=self.size_style)
            # open
            if self.update():
                # bind
                # self.w.bind("became key", self.update_callback)
                self.w.bind("close", self.on_close_window)
                # observers
                addObserver(self, "update_callback", "newFontDidOpen")
                addObserver(self, "update_callback", "fontDidOpen")
                addObserver(self, "update_callback", "fontDidClose")
                # open window
                self.w.open()
        else:
            print no_font_open

    # methods

    def get_fonts(self):
        self.all_fonts = AllFonts()

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
        self.w.box_font.text.set(get_full_name(self.font))
        self.w.box_glyph.text.set(self.glyph.name)
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
                    print no_glyph_selected
                    return False
            else:
                print no_font_open
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

    def update_callback(self, sender):
        self.get_fonts()
        self.update()

    def on_close_window(self, sender):
            removeObserver(self, "newFontDidOpen")
            removeObserver(self, "fontDidOpen")
            removeObserver(self, "fontDidClose")
