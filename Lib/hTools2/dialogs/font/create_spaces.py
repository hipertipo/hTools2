# [h] a dialog to create space glyphs

# imports

from vanilla import *

from mojo.roboFont import CurrentFont, CurrentGlyph

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.encoding import unicode_hexstr_to_int

# objects

class createSpaceGlyphsDialog(object):

    '''A dialog to create space glyphs in a font.'''

    _title = 'spaces'
    _padding = 10
    _padding_top = 10
    _column_1 = 55
    _field_width = 40
    _row_height = 18
    _button_height = 30
    _box_height = 23
    _height = (_row_height * 5) + (_button_height * 1) + (_padding * 8) + _box_height + 4
    _width = 123

    _hairspace_factor = .08
    _thinspace_factor = .16
    _thickspace_factor = .333
    _figurespace_factor = .6

    def __init__(self):
        if CurrentFont() is not None:
            self.font = CurrentFont()
            self.w = FloatingWindow(
                        (self._width, self._height),
                        self._title,
                        closable=True)
            # current font
            x = self._padding
            y = self._padding
            self.w.box = Box(
                        (x, y,
                        -self._padding,
                        self._box_height))
            self.w.box.text = TextBox(
                        (5, 0,
                        -self._padding,
                        self._row_height),
                        text=get_full_name(self.font),
                        sizeStyle='small')
            # hair space
            y += self._row_height + 18
            self.w._hairspace_label = TextBox(
                        (x, y,
                        self._column_1,
                        self._row_height),
                        "hair",
                        sizeStyle='small')
            x += self._column_1
            self.w._hairspace_value = EditText(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        text=int(self.font.info.unitsPerEm * self._hairspace_factor),
                        sizeStyle='small')
            # thin space
            x = self._padding
            y += self._row_height + self._padding
            self.w._thinspace_label = TextBox(
                        (x, y,
                        self._column_1,
                        self._row_height),
                        "thin",
                        sizeStyle='small')
            x += self._column_1
            self.w._thinspace_value = EditText(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        text=int(self.font.info.unitsPerEm * self._thinspace_factor),
                        sizeStyle='small')
            # thick space
            x = self._padding
            y += self._row_height + self._padding
            self.w._thickspace_label = TextBox(
                        (x, y,
                        self._column_1,
                        self._row_height),
                        "thick",
                        sizeStyle='small')
            x += self._column_1
            self.w._thickspace_value = EditText(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        text=int(self.font.info.unitsPerEm * self._thickspace_factor),
                        sizeStyle='small')
            # figure space
            x = self._padding
            y += self._row_height + self._padding
            self.w._figurespace_label = TextBox(
                        (x, y,
                        self._column_1,
                        self._row_height),
                        "figure",
                        sizeStyle='small')
            x += self._column_1
            self.w._figurespace_value = EditText(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        text=int(self.font.info.unitsPerEm * self._figurespace_factor),
                        sizeStyle='small')
            # zero width space
            x = self._padding
            y += self._row_height + self._padding
            self.w._zerowidth_label = TextBox(
                        (x, y,
                        self._column_1,
                        self._row_height),
                        "0 width",
                        sizeStyle='small')
            x += self._column_1
            self.w._zerowidth_value = EditText(
                        (x, y,
                        -self._padding,
                        self._row_height),
                        text='0',
                        readOnly=True,
                        sizeStyle='small')
            # buttons
            x = self._padding
            y += self._row_height + self._padding
            self.w._button_apply = SquareButton(
                        (x, y,
                        -self._padding,
                        self._button_height),
                        "create",
                        sizeStyle='small',
                        callback = self.apply_callback)
            # y += self._button_height + self._padding
            # self.w._button_switch = SquareButton(
            #             (x, y,
            #             -self._padding,
            #             self._button_height),
            #             "update",
            #             sizeStyle='small',
            #             callback=self.update_font_callback)
            # open window
            self.w.open()
        # no font open
        else:
            print 'please open a font first.\n'

    def apply_callback(self, sender):
        _hairspace = int(self.w._hairspace_value.get())
        _thinspace = int(self.w._thinspace_value.get())
        _thickspace = int(self.w._thickspace_value.get())
        _figurespace = int(self.w._figurespace_value.get())
        # boolstring = (False, True)
        if self.font is not None:
            # print info
            print 'creating space glyphs...\n'
            print '\thair space: %s units' % _hairspace
            print '\tthin space: %s units' % _thinspace
            print '\tthick space: %s units' % _thickspace
            print '\tfigure space: %s units' % _figurespace
            print '\tzero-width space: 0'
            # hair space
            self.font.newGlyph('hairspace')
            self.font['hairspace'].width = _hairspace
            self.font['hairspace'].unicode = unicode_hexstr_to_int('uni200A')
            self.font['hairspace'].update()
            # thin space
            self.font.newGlyph('thinspace')
            self.font['thinspace'].width = _thinspace
            self.font['thinspace'].unicode = unicode_hexstr_to_int('uni2009')
            self.font['thinspace'].update()
            # thick space
            self.font.newGlyph('thickspace')
            self.font['thickspace'].width = _thickspace
            self.font['thickspace'].unicode = unicode_hexstr_to_int('uni2004')
            self.font['thickspace'].update()
            # figure space
            self.font.newGlyph('figurespace')
            self.font['figurespace'].width = _figurespace
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
            print 'No font selected, please close the dialog and try again.\n'

    def update_font_callback(self, sender):
        self.font = CurrentFont()
        self.w.box.text.set(get_full_name(self.font))

    def close_callback(self, sender):
        self.w.close()
