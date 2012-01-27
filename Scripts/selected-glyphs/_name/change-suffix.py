# [h] change glyph suffix

from vanilla import *

from hTools2.modules.glyphutils import has_suffix, change_suffix

# dialog

class changeSuffixDialog(object):

    _title = 'suffix'
    _padding = 10
    _column_1 = 33
    _column_2 = 70
    _box_height = 20
    _row_height = 30

    _height = (_row_height * 3) + (_padding * 2) 
    _width = _column_1 + _column_2 + (_padding * 2)

    _old_suffix = ''
    _new_suffix = ''
    
    def __init__(self):
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title,
                    closable=True)
        # old suffix
        x = self._padding
        y = self._padding
        self.w._old_suffix_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "old",
                    sizeStyle='small')
        x += self._column_1
        self.w._old_suffix_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder='old suffix',
                    text=self._old_suffix,
                    callback=self.old_suffix_callback,
                    sizeStyle='small')
        # new suffix
        x = self._padding
        y += self._row_height
        self.w._new_suffix_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "new",
                    sizeStyle='small')
        x += self._column_1
        self.w._new_suffix_value = EditText(
                    (x, y,
                    self._column_2,
                    self._box_height),
                    placeholder = 'optional',
                    text = self._new_suffix,
                    callback=self.new_suffix_callback,
                    sizeStyle='small')
        # apply button
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
        #self.w.setDefaultButton(self.w.button_apply)
        #self.w.button_close.bind(".", ["command"])
        #self.w.button_close.bind(unichr(27), [])
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
                boolstring = (False, True)
                # print info
                print 'changing glyph name suffixes...\n'
                print '\told suffix: %s' % _old
                print '\tnew suffix: %s' % _new
                print
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
                                g.update()
                                print
                            else:
                                g.name = _new_name
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
