# [h] change glyph suffix

from vanilla import *
from AppKit import NSColor

from random import random

from hTools2.modules.glyphutils import has_suffix, change_suffix
from hTools2.modules.color import randomColor

# dialog

class changeSuffixDialog(object):

    _title = 'change suffix'
    _height = 140
    _width = 210
    _padding = 10
    _column_1 = 100
    _row_height = 30
    _mark_color = randomColor()
    _old_suffix = ''
    _new_suffix = ''
    
    def __init__(self):
        self.w = FloatingWindow(
                (self._width,
                self._height),
                self._title,
                closable=False)
        # old suffix
        self.w._old_suffix_label = TextBox(
                (self._padding,
                self._padding + (self._row_height * 0),
                -self._padding,
                20),
                "old suffix")
        self.w._old_suffix_value = EditText(
                ((self._width / 2),
                self._padding + (self._row_height * 0),
                -self._padding,
                20),
                placeholder = 'old suffix',
                text = self._old_suffix,
                callback=self.old_suffix_callback)
        # new suffix
        self.w._new_suffix_label = TextBox(
                (self._padding,
                self._padding + (self._row_height * 1),
                -self._padding,
                20),
                "new suffix")
        self.w._new_suffix_value = EditText(
                ((self._width / 2),
                self._padding + (self._row_height * 1),
                -self._padding,
                20),
                placeholder = 'optional',
                text = self._new_suffix,
                callback=self.new_suffix_callback)
        # mark color
        self.w.mark_checkbox = CheckBox(
                (self._padding,
                self._padding + (self._row_height * 2),
                -self._padding,
                20),
                "mark",
                value = True)
        self.w.mark_color = ColorWell(
                ((self._width / 2),
                self._padding + (self._row_height * 2),
                -self._padding,
                20),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_close = Button(
                (self._padding,
                -35,
                (self._width / 2) - 10,
                20),
                "close",
                callback=self.close_callback)
        self.w.button_apply = Button(
                ((self._width / 2) + 10,
                -35,
                -self._padding,
                20),
                "apply",
                callback=self.apply_callback)
        # open window
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()

    def old_suffix_callback(self, sender):
        self._old_suffix = sender.get()

    def new_suffix_callback(self, sender):
        self._new_suffix = sender.get()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _old = self._old_suffix
                _new = self._new_suffix
                _mark = self.w.mark_checkbox.get()
                _mark_color = self.w.mark_color.get()
                boolstring = (False, True)
                # print info
                print 'changing glyph name suffixes...\n'
                print '\told suffix: %s' % _old
                print '\tnew suffix: %s' % _new
                print '\tmark: %s' % boolstring[_mark]
                print
                _mark_color = (_mark_color.redComponent(),
                    _mark_color.greenComponent(),
                    _mark_color.blueComponent(),
                    _mark_color.alphaComponent())
                # batch change names
                for gName in f.selection:
                    if gName is not None:
                        if has_suffix(gName, _old):
                            g = f[gName]
                            # make new name
                            _new_name = change_suffix(gName, _old, _new)
                            print '\trenaming %s to %s...' % (gName, _new_name)
                            if f.has_key(_new_name):
                                print '\toverwriting %s' % _new_name
                                f.removeGlyph(_new_name)
                                g.name = _new_name
                                g.mark = _mark_color
                                g.update()
                                print
                            else:
                                g.name = _new_name
                                if _mark:
                                    g.mark = _mark_color
                                    g.update()
                # done
                f.update()
                print
                print '...done.\n'
                # no glyph selected
            else:
                print 'please select one or more glyphs before running the script.\n'
        # no glyph selected
        else:
            print 'please open a font first.\n'
        pass

    def close_callback(self, sender):
        self.w.close()

# run script

changeSuffixDialog()
