# [h] dialog to change suffix in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont
except:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import has_suffix, change_suffix

# objects

class changeSuffixDialog(object):

    """A dialog to change the suffix of the selected glyphs."""

    #------------
    # attributes
    #------------

    _title = 'suffix'
    _padding = 10
    _column_1 = 33
    _column_2 = 70
    _box_height = 20
    _button_height = 30

    _height = (_box_height * 3) + (_padding * 5) + _button_height
    _width = 123

    _old_suffix = ''
    _new_suffix = ''
    _overwrite = True

    #---------
    # methods
    #---------

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
        y += (self._box_height + self._padding)
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
                    placeholder='optional',
                    text=self._new_suffix,
                    callback=self.new_suffix_callback,
                    sizeStyle='small')
        y += (self._box_height + self._padding)
        # checkbox overwrite
        self.w._overwrite_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    "overwrite",
                    value=self._overwrite,
                    callback=self.overwrite_callback,
                    sizeStyle='small')
        # apply button
        x = self._padding
        y += (self._box_height + self._padding)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self._padding,
                    self._button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle='small')
        # open window
        self.w.open()

    def old_suffix_callback(self, sender):
        self._old_suffix = sender.get()

    def new_suffix_callback(self, sender):
        self._new_suffix = sender.get()

    def overwrite_callback(self, sender):
        self._overwrite = sender.get()

    def apply_callback(self, sender):
        boolstring = [ False, True ]
        f = CurrentFont()
        if f is not None:
            if len(f.selection) > 0:
                # print info
                print 'changing glyph name suffixes...\n'
                print '\told suffix: %s' % self._old_suffix
                print '\tnew suffix: %s' % self._new_suffix
                print '\toverwrite: %s' % boolstring[self._overwrite]
                print
                # batch change glyph names
                for glyph_name in get_glyphs(f):
                    g = f[glyph_name]
                    # get glyphs with matching suffix
                    if has_suffix(g, self._old_suffix):
                        # make new name
                        if len(self._new_suffix) > 0:
                            _new_name = change_suffix(g, self._old_suffix, self._new_suffix)
                        else:
                            _new_name = change_suffix(g, self._old_suffix, None)
                        # if new name not in font, rename
                        if not f.has_key(_new_name):
                            print '\trenaming %s to %s...' % (glyph_name, _new_name)
                            g.name = _new_name
                        # new name in font
                        else:
                            # overwrite existing
                            if self._overwrite:
                                print "\toverwriting '%s' with '%s'" % (_new_name, glyph_name)
                                f.removeGlyph(_new_name)
                                f.update()
                                g.name = _new_name
                                g.update()
                            # do not overwrite
                            else:
                                print "\t'%s' already exists in font, skipping '%s'" % (_new_name, glyph_name)
                    # glyph name does not have suffix
                    else:
                        pass
                    # done glyph
                # done font
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
