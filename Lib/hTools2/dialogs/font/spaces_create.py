# [h] a dialog to create space glyphs

# imports

from mojo.roboFont import CurrentFont, CurrentGlyph
from mojo.events import addObserver, removeObserver
from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.encoding import unicode_hexstr_to_int
from hTools2.modules.messages import no_font_open

# objects

class createSpaceGlyphsDialog(hDialog):

    """A dialog to create space glyphs in a font.

    .. image:: imgs/font/create-spaces.png

    """

    hairspace_factor = .08
    thinspace_factor = .16
    thickspace_factor = .333
    figurespace_factor = .6

    def __init__(self):
        self.title = 'spaces'
        self.column_1 = 55
        self.field_width = 40
        self.box_height = 23
        self.height = (self.text_height * 5) + (self.button_height * 1) + (self.padding_y * 8) + self.box_height + 4
        self.w = FloatingWindow((self.width, self.height), self.title)
        # current font
        x = self.padding_x
        y = self.padding_y
        self.w.box = Box(
                    (x, y,
                    -self.padding_x,
                    self.box_height))
        self.w.box.font_name = TextBox(
                    (5, 0,
                    -self.padding_x,
                    self.text_height),
                    text='(None)',
                    sizeStyle=self.size_style)
        # hair space
        y += self.text_height + 18
        self.w.hairspace_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "hair",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.hairspace_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text='',
                    sizeStyle=self.size_style)
        # thin space
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.thinspace_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "thin",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.thinspace_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text='',
                    sizeStyle=self.size_style)
        # thick space
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.thickspace_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "thick",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.thickspace_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text='',
                    sizeStyle=self.size_style)
        # figure space
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.figurespace_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "figure",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.figurespace_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text='',
                    sizeStyle=self.size_style)
        # zero width space
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.zerowidth_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "0 width",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.zerowidth_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    text='0',
                    readOnly=self.read_only,
                    sizeStyle=self.size_style)
        # buttons
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "create",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()
        # get current font
        self.get_font()

    def get_font(self):
        self.font = CurrentFont()
        if self.font is not None:
            self.w.box.font_name.set(get_full_name(self.font))
            self.w.hairspace_value.set(int(self.font.info.unitsPerEm * self.hairspace_factor))
            self.w.thickspace_value.set(int(self.font.info.unitsPerEm * self.thickspace_factor))
            self.w.thinspace_value.set(int(self.font.info.unitsPerEm * self.thinspace_factor))
            self.w.figurespace_value.set(int(self.font.info.unitsPerEm * self.figurespace_factor))
        else:
            self.w.box.font_name.set('(None)')
            self.w.hairspace_value.set('')
            self.w.thickspace_value.set('')
            self.w.thinspace_value.set('')
            self.w.figurespace_value.set('')
            print no_font_open

    def apply_callback(self, sender):
        hairspace = int(self.w.hairspace_value.get())
        thinspace = int(self.w.thinspace_value.get())
        thickspace = int(self.w.thickspace_value.get())
        figurespace = int(self.w.figurespace_value.get())
        # boolstring = (False, True)
        if self.font is not None:
            # print info
            print 'creating space glyphs...\n'
            print '\thair space: %s units' % hairspace
            print '\tthin space: %s units' % thinspace
            print '\tthick space: %s units' % thickspace
            print '\tfigure space: %s units' % figurespace
            print '\tzero-width space: 0'
            # hair space
            self.font.newGlyph('hairspace')
            self.font['hairspace'].width = hairspace
            self.font['hairspace'].unicode = unicode_hexstr_to_int('uni200A')
            self.font['hairspace'].update()
            # thin space
            self.font.newGlyph('thinspace')
            self.font['thinspace'].width = thinspace
            self.font['thinspace'].unicode = unicode_hexstr_to_int('uni2009')
            self.font['thinspace'].update()
            # thick space
            self.font.newGlyph('thickspace')
            self.font['thickspace'].width = thickspace
            self.font['thickspace'].unicode = unicode_hexstr_to_int('uni2004')
            self.font['thickspace'].update()
            # figure space
            self.font.newGlyph('figurespace')
            self.font['figurespace'].width = figurespace
            self.font['figurespace'].unicode = unicode_hexstr_to_int('uni2007')
            self.font['figurespace'].update()
            # zero-width space
            self.font.newGlyph('zerowidthspace')
            self.font['zerowidthspace'].width = 0
            self.font['zerowidthspace'].unicode = unicode_hexstr_to_int('uni200B')
            self.font['zerowidthspace'].update()
            # done
            self.font.update()
            print
            print '...done.\n'
        else:
            print no_font_open

    def update_callback(self, sender):
        self.get_font()

    def on_close_window(self, sender):
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
