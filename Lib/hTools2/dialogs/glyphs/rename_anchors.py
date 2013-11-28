# [h] rename anchors in selected glyphs

# imports

from mojo.roboFont import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import rename_anchor

# objects

class renameAnchorsDialog(object):

    '''A dialog to rename the anchors in the selected glyphs of the current font.'''

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
                    (self._width, self._height),
                    self._title,
                    closable=True)
        x = self._padding
        y = self._padding
        # old name label
        self.w._old_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "old",
                    sizeStyle='small')
        x += self._column_1
        # old name
        self.w._old_name_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='old name',
                    text='',
                    sizeStyle='small')
        x = self._padding
        y += self._row_height
        # new name label
        self.w._new_name_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "new",
                    sizeStyle='small')
        x += self._column_1
        # new name
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
                    "rename",
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
                print 'renaming anchors in glyphs...\n'
                print '\told name: %s' % _old
                print '\tnew name: %s' % _new
                print
                print '\t',
                # batch change anchors names
                glyph_names = get_glyphs(f)
                for glyph_name in glyph_names:
                    print glyph_name,
                    # rename anchor
                    f[glyph_name].prepareUndo('rename anchor')
                    has_name = rename_anchor(f[glyph_name], _old, _new)
                    f[glyph_name].performUndo()
                    f[glyph_name].update()
                # done
                f.update()
                print
                print '\n...done.\n'
                # no glyph selected
            else:
                print 'please select one or more glyphs before running the script.\n'
        # no glyph selected
        else:
            print 'please open a font first.\n'
