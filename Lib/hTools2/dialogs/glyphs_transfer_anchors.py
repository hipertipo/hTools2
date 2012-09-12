# [h] a dialog to transfer glyphs between fonts

# reload when debugging

import hTools2
reload(hTools2)

if hTools2.DEBUG:

    import hTools2.modules.fontutils
    reload(hTools2.modules.fontutils)

    import hTools2.modules.anchors
    reload(hTools2.modules.anchors)

# imports

try:
    from mojo.roboFont import AllFonts
except:
    from robofab.world import AllFonts

from vanilla import *

from hTools2.modules.fontutils import get_full_name, get_glyphs
from hTools2.modules.anchors import transfer_anchors

# objects

class transferAnchorsDialog(object):

    '''transfer anchors from selected glyphs in one font to the same glyphs in another font'''

    #------------
    # attributes
    #------------

    _title = 'anchors'
    _padding = 10
    _row_height = 25
    _line_height = 20
    _button_height = 30
    _column_1 = 130
    _width = 123
    _height = (_line_height * 2) + (_row_height * 2) + (_button_height * 2) + (_padding * 5) - 2

    _all_fonts_names = []

    #---------
    # methods
    #---------

    def __init__(self):
        self._update_fonts()
        # create window
        self.w = FloatingWindow(
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # source font label
        self.w._source_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "source font",
                    sizeStyle='small')
        y += self._line_height
        # source font value
        self.w._source_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        y += self._line_height + self._padding
        # target font label
        self.w._target_label = TextBox(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    "target font",
                    sizeStyle='small')
        y += self._line_height
        # target font value
        self.w._target_value = PopUpButton(
                    (x, y,
                    -self._padding,
                    self._line_height),
                    self._all_fonts_names,
                    sizeStyle='small')
        # buttons
        y += self._line_height + self._padding + 7
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "transfer",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # update button
        y += self._button_height + self._padding
        self.w.button_update = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "update",
                    callback=self.update_fonts_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    # callbacks

    def _update_fonts(self):
        self._all_fonts = AllFonts()
        self._all_fonts_names = []
        for font in self._all_fonts:
            self._all_fonts_names.append(get_full_name(font))

    def update_fonts_callback(self, sender):
        self._update_fonts()
        self.w._source_value.setItems(self._all_fonts_names)
        self.w._target_value.setItems(self._all_fonts_names)

    def apply_callback(self, sender):
        if len(self._all_fonts) > 0:
            # get parameters
            _source_font = self._all_fonts[self.w._source_value.get()]
            _target_font = self._all_fonts[self.w._target_value.get()]
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
