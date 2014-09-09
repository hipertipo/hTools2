# [h] transfer anchors between two fonts

# imports

try:
    from mojo.roboFont import AllFonts
    from mojo.events import addObserver, removeObserver

except ImportError:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.anchors import transfer_anchors
from hTools2.modules.messages import no_font_open

# objects

class transferAnchorsDialog(hDialog):

    """A dialog to transfer anchors from selected glyphs in one font to the same glyphs in another font.

    .. image:: imgs/glyphs/anchors-transfer.png

    """

    # attributes

    all_fonts = []
    all_fonts_names = []

    # methods

    def __init__(self):
        self._get_fonts()
        # create window
        self.title = 'anchors'
        self.column_1 = 130
        self.width = 123
        self.height = (self.text_height * 4) + (self.button_height) + (self.padding_y * 4)# - 2
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y - 1
        # source font label
        self.w._source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "source",
                    sizeStyle=self.size_style)
        y += self.text_height
        # source font value
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        # target font label
        self.w._target_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "target",
                    sizeStyle=self.size_style)
        y += self.text_height
        # target font value
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # buttons
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "copy",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # bind
        self.w.bind("became key", self.update_callback)
        self.w.bind("close", self.on_close_window)
        # observers
        addObserver(self, "update_callback", "newFontDidOpen")
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.w.open()

    # callbacks

    def _get_fonts(self):
        self.all_fonts = AllFonts()
        self.all_fonts_names = []
        for font in self.all_fonts:
            self.all_fonts_names.append(get_full_name(font))

    def update_callback(self, sender):
        self._get_fonts()
        self.w._source_value.setItems(self.all_fonts_names)
        self.w._target_value.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        if len(self.all_fonts) > 0:
            # get parameters
            source_font = self.all_fonts[self.w._source_value.get()]
            target_font = self.all_fonts[self.w._target_value.get()]
            # print info
            print 'transfering anchors...\n'
            print '\tsource: %s' % get_full_name(source_font)
            print '\ttarget: %s' % get_full_name(target_font)
            print
            print '\t',
            # batch transfer anchors
            skipped = []
            for glyph_name in get_glyphs(source_font):
                if len(source_font[glyph_name].anchors) > 0:
                    if target_font.has_key(glyph_name):
                        print glyph_name,
                        # prepare undo
                        target_font[glyph_name].prepareUndo('transfer anchors')
                        # transfer anchors
                        transfer_anchors(source_font[glyph_name], target_font[glyph_name])
                        # update
                        target_font[glyph_name].update()
                        # activate undo
                        target_font[glyph_name].performUndo()
                    else:
                        skipped.append(glyph_name)
                else:
                    # glyph does not have anchors
                    pass
            # done
            print
            target_font.update()
            if len(skipped) > 0:
                print '\n\tglyphs %s not in target font.\n' % skipped
            print '...done.\n'
        else:
            print no_font_open # 'please open at least one font.\n'

    def on_close_window(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
