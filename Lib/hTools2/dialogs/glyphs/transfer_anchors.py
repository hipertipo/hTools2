# [h] a dialog to transfer anchors between fonts

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2 import hConstants
from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.anchors import transfer_anchors

# objects

class transferAnchorsDialog(hConstants):

    """A dialog to transfer anchors from selected glyphs in one font to the same glyphs in another font."""

    # attributes

    all_fonts = []
    all_fonts_names = []

    # methods

    def __init__(self):
        self._update_fonts()
        # create window
        self.title = 'anchors'
        self.column_1 = 130
        self.width = 123
        self.height = (self.text_height * 4) + (self.button_height * 2) + (self.padding_y * 5) - 2
        self.w = FloatingWindow(
                    (self.width, self.height),
                    self.title)
        x = self.padding_x
        y = self.padding_y - 3
        # source font label
        self.w._source_label = TextBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "source font",
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
                    "target font",
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
                    "transfer",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # update button
        y += (self.button_height + self.padding_y)
        self.w.button_update = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "update",
                    callback=self.update_fonts_callback,
                    sizeStyle=self.size_style)
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
            _source_font = self.all_fonts[self.w._source_value.get()]
            _target_font = self.all_fonts[self.w._target_value.get()]
            # print info
            print 'transfering anchors...\n'
            print '\tsource: %s' % get_full_name(_source_font)
            print '\ttarget: %s' % get_full_name(_target_font)
            print
            print '\t',
            # batch transfer anchors
            _skipped = []
            for glyph_name in get_glyphs(_source_font):
                if len(_source_font[glyph_name].anchors) > 0:
                    if _target_font.has_key(glyph_name):
                        print glyph_name,
                        # prepare undo
                        _target_font[glyph_name].prepareUndo('transfer anchors')
                        # transfer anchors
                        transfer_anchors(_source_font[glyph_name], _target_font[glyph_name])
                        # update
                        _target_font[glyph_name].update()
                        # activate undo
                        _target_font[glyph_name].performUndo()
                    else:
                        _skipped.append(glyph_name)
                else:
                    # glyph does not have anchors
                    pass
            # done
            print
            _target_font.update()
            if len(_skipped) > 0:
                print '\n\tglyphs %s not in target font.\n' % _skipped
            print '...done.\n'
        else:
            print 'please open at least one font.\n'

