# [h] transfer vertical metrics

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name
from hTools2.modules.messages import no_font_open

# objects

class transferVMetricsDialog(hDialog):

    """A dialog to transfer the vertical metrics from one font to another.

    .. image:: imgs/font/copy-vmetrics.png

    """

    all_fonts_names = []

    def __init__(self):
        self.title = 'vmetrics'
        self.column_1 = 103
        self.width = self.column_1 + (self.padding_x * 2)
        self.height = (self.text_height * 4) + self.button_height + (self.padding_y * 4)
        self.w = FloatingWindow((self.width, self.height), self.title)
        # source font
        x = self.padding_x
        y = self.padding_y
        self.w.source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "source",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.source_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # target font
        y += self.text_height + self.padding_y
        self.w.target_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "target",
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.target_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # buttons
        y += self.text_height + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
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
        self.get_fonts()

    def get_fonts(self):
        self.all_fonts = AllFonts()
        if len(self.all_fonts) > 0:
            self.all_fonts_names = []
            for f in self.all_fonts:
                font_name = get_full_name(f)
                self.all_fonts_names.append(font_name)
            self.w.source_value.setItems(self.all_fonts_names)
            self.w.target_value.setItems(self.all_fonts_names)
        # no font open
        else:
            print no_font_open

    def apply_callback(self, sender):
        # get parameters
        source_font = self.all_fonts[self.w.source_value.get()]
        target_font = self.all_fonts[self.w.target_value.get()]
        # print info
        print 'copying vmetrics...\n'
        print '\tsource font: %s' % get_full_name(source_font)
        print '\ttarget font: %s' % get_full_name(target_font)
        # copy vmetrics
        target_font.info.xHeight = source_font.info.xHeight
        target_font.info.capHeight = source_font.info.capHeight
        target_font.info.ascender = source_font.info.ascender
        target_font.info.descender = source_font.info.descender
        target_font.info.unitsPerEm = source_font.info.unitsPerEm
        # done
        print
        target_font.update()
        print '...done.\n'

    def on_close_window(self, sender):
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")

    def update_callback(self, sender):
        self.get_fonts()
