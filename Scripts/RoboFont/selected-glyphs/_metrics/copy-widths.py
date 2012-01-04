# [h] copy widths dialog

'''copy width of selected glyphs in one font to the same glyphs in another font'''

from vanilla import *
from AppKit import NSColor

from hTools2.modules.fontutils import get_full_name
from hTools2.modules.glyphutils import centerGlyph
from hTools2.modules.color import randomColor

class copyWidthsDialog(object):

    _title = 'copy widths'
    _mark_color_source = randomColor()
    _mark_color_dest = randomColor()
    _all_fonts_names = []
    _width = 280
    _height = 300
    _padding = 15
    _padding_top = 10

    def __init__(self, ):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title,
                closable = False)
        self._all_fonts = AllFonts()
        for f in self._all_fonts:
            self._all_fonts_names.append(get_full_name(f))
        # source font
        self.w._source_label = TextBox(
                (self._padding,
                self._padding_top,
                -self._padding,
                17),
                "source font:")
        self.w._source_value = PopUpButton(
                (self._padding,
                35,
                -self._padding,
                20),
                self._all_fonts_names)
        # mark source
        self.w.mark_source_checkbox = CheckBox(
                (self._padding,
                65,
                -self._padding,
                20),
                "mark glyphs",
                value = True)
        self.w.mark_source_color = ColorWell(
                (120,
                65,
                -13,
                20),
                color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color_source))
        # dest font
        self.w._dest_label = TextBox(
                (self._padding,
                100,
                -self._padding,
                17),
                "target font:")
        self.w._dest_value = PopUpButton(
                (self._padding,
                125,
                -self._padding,
                20),
                self._all_fonts_names)
        # mark dest
        self.w.mark_dest_checkbox = CheckBox(
                (self._padding,
                155,
                -self._padding,
                20),
                "mark glyphs",
                value = True)
        self.w.mark_dest_color = ColorWell(
                (120,
                155,
                -13,
                20),
                color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color_dest))
        self.w.line = HorizontalLine(
                (self._padding,
                200,
                -self._padding,
                1))
        # center
        self.w.center_checkbox = CheckBox(
                (self._padding,
                215,
                -self._padding,
                20),
                "center glyphs",
                value = False)
        self.w.line2 = HorizontalLine(
                (self._padding,
                250,
                -self._padding,
                1))
        # buttons
        self.w.button_apply = Button(
                (self._padding,
                -50,
                self._width / 2 - 15,
                0),
                "apply",
                callback = self.apply_callback)
        self.w.button_close = Button(
                (self._width / 2 + 5,
                -50,
                -self._padding,
                0),
                "close",
                callback = self.close_callback)
        # open window 
        self.w.open()

    def apply_callback(self, sender):
        boolstring = [False, True]
        # source font
        _source_font_index = self.w._source_value.get()
        _source_font = self._all_fonts[_source_font_index]
        _source_font_name = self._all_fonts_names[_source_font_index]
        _source_mark = self.w.mark_source_checkbox.get()
        _source_mark_color = self.w.mark_source_color.get()
        _source_mark_color = (_source_mark_color.redComponent(),
                _source_mark_color.greenComponent(),
                _source_mark_color.blueComponent(),
                _source_mark_color.alphaComponent())
        # dest font
        _dest_font_index = self.w._dest_value.get()            
        _dest_font = self._all_fonts[_dest_font_index]
        _dest_font_name = self._all_fonts_names[_dest_font_index]
        _dest_mark = self.w.mark_dest_checkbox.get()
        _dest_mark_color = self.w.mark_dest_color.get()
        _dest_mark_color = (_dest_mark_color.redComponent(),
                _dest_mark_color.greenComponent(),
                _dest_mark_color.blueComponent(),
                _dest_mark_color.alphaComponent())
        # center
        _center = self.w.center_checkbox.get()
        # print info
        print 'copying widths...\n'
        print '\tsource font: %s' % _source_font_name
        print '\ttarget font: %s' % _dest_font_name
        print
        print '\tcenter: %s' % boolstring[_center]
        print
        # batch copy side-bearings
        for gName in _source_font.selection:
            try:
                # set undo
                _source_font[gName].prepareUndo('copy width')
                _dest_font[gName].prepareUndo('copy width')
                # copy
                print '\t%s' % gName,
                _dest_font[gName].width = _source_font[gName].width
                # center
                if _center:
                    centerGlyph(_dest_font[gName])
                # mark
                if _source_mark:
                    _source_font[gName].mark = _source_mark_color
                    _source_font[gName].update()
                if _dest_mark:
                    _dest_font[gName].mark = _dest_mark_color
                    _dest_font[gName].update()
                # call undo
                _dest_font.performUndo()
                _dest_font.update()
                _dest_font.performUndo()
                _dest_font.update()
            except:
                print '\tcannot process %s' % gName
        print
        print '\n...done.\n'

    def close_callback(self, sender):
        self.w.close()

# run

copyWidthsDialog()

