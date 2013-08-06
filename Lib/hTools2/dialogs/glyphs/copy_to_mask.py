# [h] copy to mask

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.messages
    reload(hTools2.modules.messages)

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.messages import no_font_open
from hTools2.modules.fontutils import get_full_name, get_glyphs

# objects

class copyToMaskDialog(hConstants):

    """A dialog to transfer the foreground layer of the selcted glyphs in the current font to the mask layer of the same glyphs of another font."""

    # attributes

    source_layer_name = 'foreground'
    target_layer_name = 'background'

    # methods

    def __init__(self):
        self._update_fonts()
        # window
        self.title = 'copy'
        self.column_1 = 103
        self.width = self.column_1 + (self.padding_x * 2)
        self.height = (self.text_height * 4) + (self.button_height * 2) + (self.padding_y * 5) #- 2
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title,
                    closable=True)
        x = self.padding_x
        y = self.padding_y - 1
        # source label
        self.w._source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "foreground",
                    sizeStyle=self.size_style)
        y += self.text_height
        # source value
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        # target label
        self.w._target_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "background",
                    sizeStyle=self.size_style)
        y += self.text_height
        # target value
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.all_fonts_names,
                    sizeStyle=self.size_style)
        # apply button
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    sizeStyle=self.size_style,
                    callback=self.apply_callback)
        # update button
        y += (self.button_height + self.padding_y)
        self.w.button_update = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "update",
                    sizeStyle=self.size_style,
                    callback=self.update_fonts_callback)
        # open window
        self.w.open()

    # callbacks

    def _update_fonts(self):
        self.all_fonts = AllFonts()
        self.all_fonts_names = []
        for font in self.all_fonts:
            self.all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self.all_fonts_names)
        self.w._target_value.setItems(self.all_fonts_names)

    def apply_callback(self, sender):
        if len(self.all_fonts) > 0:
            # get parameters
            source_font = self.all_fonts[self.w._source_value.get()]
            target_font = self.all_fonts[self.w._target_value.get()]
            # print info
            print 'copying glyphs to mask...\n'
            print '\tsource font: %s (foreground)' % get_full_name(source_font)
            print '\ttarget font: %s (%s)' % (get_full_name(target_font), self.target_layer_name)
            print
            print '\t',
            # batch copy glyphs to mask
            for glyph_name in get_glyphs(source_font):
                print glyph_name,
                # prepare undo
                target_font[glyph_name].prepareUndo('copy glyphs to mask')
                # copy oulines to mask
                target_glyph_layer = target_font[glyph_name].getLayer(self.target_layer_name)
                pen = target_glyph_layer.getPointPen()
                source_font[glyph_name].drawPoints(pen)
                # update
                target_font[glyph_name].update()
                # activate undo
                target_font[glyph_name].performUndo()
            # done
            print
            target_font.update()
            print '\n...done.\n'
        # no font open
        else:
            print no_font_open

