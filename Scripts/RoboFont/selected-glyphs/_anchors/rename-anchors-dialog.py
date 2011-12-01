# [h] rename anchors in selected glyphs

from AppKit import NSColor
from vanilla import *

from hTools2.modules.color import randomColor
from hTools2.modules.anchors import renameAnchor

# dialog

class renameAnchorsDialog(object):

    _title = 'rename anchors'
    _mark_color = randomColor()
    _height = 140
    _width = 210
    _padding = 10
    _column_1 = 100
    _row_height = 30
    
    def __init__(self):
        self.w = FloatingWindow(
            (self._width,
            self._height),
            self._title,
            closable = False)
        # old name
        self.w._old_name_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 0),
            -self._padding,
            20),
            "old name")
        self.w._old_name_value = EditText(
            ((self._width / 2),
            self._padding + (self._row_height * 0),
            -self._padding,
            20),
            placeholder = 'old name',
            text = '')
        # new name
        self.w._new_name_label = TextBox(
            (self._padding,
            self._padding + (self._row_height * 1),
            -self._padding,
            20),
            "new name")
        self.w._new_name_value = EditText(
            ((self._width / 2),
            self._padding + (self._row_height * 1),
            -self._padding,
            20),
            placeholder = 'new name',
            text = '')
        # mark color
        self.w.mark_checkbox = CheckBox(
            (self._padding,
            70,
            -self._padding,
            20),
            "mark",
            value = True)
        self.w.mark_color = ColorWell(
            ((self._width / 2),
            70,
            -self._padding,
            20),
            color = NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_close = Button(
            (self._padding,
            -35,
            (self._width / 2) - 10,
            20),
            "close",
            callback = self.close_callback)
        self.w.button_apply = Button(
            ((self._width / 2) + 10,
            -35,
            -self._padding,
            20),
            "apply",
            callback = self.apply_callback)
        # open window
        self.w.setDefaultButton(self.w.button_apply)
        self.w.button_close.bind(".", ["command"])
        self.w.button_close.bind(unichr(27), [])
        self.w.open()
        
    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _old = self.w._old_name_value.get()
                _new = self.w._new_name_value.get()
                _mark = self.w.mark_checkbox.get()
                _mark_color = self.w.mark_color.get()
                boolstring = (False, True)
                # print info
                print 'changing anchor names...\n'
                print '\told name: %s' % _old
                print '\tnew name: %s' % _new
                print '\tmark: %s' % boolstring[_mark]
                print         
                # batch change anchors names
                _mark_color = (_mark_color.redComponent(),
                    _mark_color.greenComponent(),
                    _mark_color.blueComponent(),
                    _mark_color.alphaComponent())
                for gName in f.selection:
                    if gName is not None:
                        # rename anchor                
                        has_name = renameAnchor(f[gName], _old, _new)
                        # mark
                        if has_name:
                            if _mark:
                                f[gName].mark = _mark_color
                        f[gName].update()
                # done
                f.update()
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
        
# run
        
renameAnchorsDialog()
