# [h] rename anchors in selected glyphs

from vanilla import *

import hTools2.modules.anchors
reload(hTools2.modules.anchors)

from hTools2.modules.anchors import rename_anchor

# dialog

class renameAnchorsDialog(object):

    _title = 'anchors'
    _padding = 10
    _column_1 = 33
    _column_2 = 70
    _box_height = 20
    _row_height = 30

    _height = (_row_height * 3) + (_padding * 2) 
    _width = _column_1 + _column_2 + (_padding * 2)

    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # old name
        x = self._padding
        y = self._padding
        self.w._old_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "old",
                    sizeStyle='small')
        x += self._column_1
        self.w._old_name_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='old name',
                    text='',
                    sizeStyle='small')
        # new name
        x = self._padding
        y += self._row_height
        self.w._new_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "new",
                    sizeStyle='small')
        x += self._column_1
        self.w._new_name_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='new name',
                    text='',
                    sizeStyle='small')
        # button
        x = self._padding
        y += self._row_height
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._row_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        # self.w.setDefaultButton(self.w.button_apply)
        # self.w.button_close.bind(".", ["command"])
        # self.w.button_close.bind(unichr(27), [])
        self.w.open()
        
    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # get parameters
                _old = self.w._old_name_value.get()
                _new = self.w._new_name_value.get()
                boolstring = (False, True)
                # print info
                print 'changing anchor names...\n'
                print '\told name: %s' % _old
                print '\tnew name: %s' % _new
                print 
                # batch change anchors names
                for gName in f.selection:
                    if gName is not None:
                        # rename anchor                
                        has_name = rename_anchor(f[gName], _old, _new)
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

