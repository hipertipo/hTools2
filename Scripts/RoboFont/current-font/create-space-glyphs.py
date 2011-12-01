# [h] create space glyphs

from AppKit import NSColor
from vanilla import *

from random import random

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.colorsys import hsv_to_rgb

# dialog

class createSpaceGlyphsDialog(object):

    _title = 'create space glyphs'
    R, G, B = hsv_to_rgb(random(), 1.0, 1.0)
    _mark_color = (R, G, B, 1)
    _height = 350
    _padding = 15
    _padding_top = 10
    _column_1 = 160
    _field_width = 60
    _row_height = 30
    _hairspace_factor = .08
    _thinspace_factor = .16
    _thickspace_factor = .333
    _figurespace_factor = .6    
    
    def __init__(self):
        self._width = self._column_1 + self._field_width + (self._padding * 3)
        if CurrentFont() is not None:
            self.font = CurrentFont()
            self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title,
                closable = True)
            # current font
            self.w.box = Box(
                (self._padding,
                self._padding_top + (self._row_height * 0),
                -self._padding,
                26))
            self.w.box.text = TextBox(
                (5, 1, -10, 20),
                text = get_full_name(self.font),
                sizeStyle = 'small')
            # hair space
            self.w._hairspace_label = TextBox(
                (self._padding,
                self._padding_top + (self._row_height * 1) + 10,
                self._column_1,
                20),
                "hair space")
            self.w._hairspace_value = EditText(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 1) + 10,
                self._field_width,
                20),
                text = int(self.font.info.unitsPerEm * self._hairspace_factor))
            # thin space
            self.w._thinspace_label = TextBox(
                (self._padding,
                self._padding_top + (self._row_height * 2) + 10,
                self._column_1,
                20),
                "thin space")
            self.w._thinspace_value = EditText(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 2) + 10,
                self._field_width,
                20),
                text = int(self.font.info.unitsPerEm * self._thinspace_factor))
            # thick space
            self.w._thickspace_label = TextBox(
                (self._padding,
                self._padding_top + (self._row_height * 3) + 10,
                self._column_1,
                20),
                "thick space")
            self.w._thickspace_value = EditText(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 3) + 10,
                self._field_width,
                20),
                text = int(self.font.info.unitsPerEm * self._thickspace_factor))
            # figure space
            self.w._figurespace_label = TextBox(
                (self._padding,
                self._padding_top + (self._row_height * 4) + 10,
                self._column_1,
                20),
                "figure space")
            self.w._figurespace_value = EditText(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 4) + 10,
                self._field_width,
                20),
                text = int(self.font.info.unitsPerEm * self._figurespace_factor))
            # zero width space
            self.w._zerowidth_label = TextBox(
                (self._padding,
                self._padding_top + (self._row_height * 5) + 10,
                self._column_1,
                20),
                "zero-width space")
            self.w._zerowidth_value = EditText(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 5) + 10,
                self._field_width,
                20),
                text = '0',
                readOnly = True)
            # division
            self.w.line_1 = HorizontalLine(
                (self._padding,
                self._padding_top + (self._row_height * 6) + 15,
                -self._padding,
                1))
            # auto unicodes
            self.w._set_unicode_checkbox = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 7),
                self._column_1,
                20),
                "auto unicodes",
                value = True)
            # mark color
            self.w._mark_checkbox = CheckBox(
                (self._padding,
                self._padding_top + (self._row_height * 8),
                self._column_1,
                20),
                "mark",
                value = True)
            self.w._mark_color = ColorWell(
                (self._column_1 + (self._padding * 2),
                self._padding_top + (self._row_height * 8),
                self._field_width,
                20),
                color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
            # buttons
            self.w._button_apply = Button(
                (self._padding,
                -65,
                -self._padding,
                20),
                "create glyphs",
                sizeStyle = 'small',
                callback = self.apply_callback)
            self.w._button_switch = Button(
                (self._padding,
                -35,
                -self._padding,
                20),
                "switch to current font",
                sizeStyle = 'small',
                callback = self.update_font_callback)
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
        _set_unicode = int(self.w._set_unicode_checkbox.get())
        _mark = self.w._mark_checkbox.get()
        _mark_color = self.w._mark_color.get()
        _mark_color = (_mark_color.redComponent(),
            _mark_color.greenComponent(),
            _mark_color.blueComponent(),
            _mark_color.alphaComponent())
        boolstring = (False, True)
        if self.font is not None:
            # print info
            print 'creating space glyphs...\n'
            print '\thair space: %s units' % _hairspace
            print '\tthin space: %s units' % _thinspace
            print '\tthick space: %s units' % _thickspace
            print '\tfigure space: %s units' % _figurespace
            print '\tset unicode: %s' % boolstring[_set_unicode]
            print '\tmark: %s' % boolstring[_mark]
            # hair space
            self.font.newGlyph('hairspace')
            self.font['hairspace'].width = _hairspace
            self.font['hairspace'].mark = _mark_color
            self.font['hairspace'].autoUnicodes()
            self.font['hairspace'].update()
            # thin space
            self.font.newGlyph('thinspace')
            self.font['thinspace'].width = _thinspace
            self.font['thinspace'].mark = _mark_color
            self.font['thinspace'].autoUnicodes()
            self.font['thinspace'].update()
            # thick space
            self.font.newGlyph('thickspace')
            self.font['thickspace'].width = _thickspace
            self.font['thickspace'].mark = _mark_color
            self.font['thickspace'].autoUnicodes()
            self.font['thickspace'].update()
            # figure space
            self.font.newGlyph('figurespace')
            self.font['figurespace'].width = _figurespace
            self.font['figurespace'].mark = _mark_color
            self.font['figurespace'].autoUnicodes()
            self.font['figurespace'].update()
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
        
# run
        
createSpaceGlyphsDialog()

