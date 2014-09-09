# [h] change suffix in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.glyphutils import has_suffix, change_suffix
from hTools2.modules.messages import no_font_open, no_glyph_selected

# objects

class changeSuffixDialog(hDialog):

    """A dialog to change the suffix of the selected glyphs.

    .. image:: imgs/glyphs/names-suffix-0.png
    .. image:: imgs/glyphs/names-suffix-1.png
    .. image:: imgs/glyphs/names-suffix-2.png
    .. image:: imgs/glyphs/names-suffix-3.png

    """

    # attributes

    #: The old suffix to be substituted.
    old_suffix = ''

    #: New suffix for glyph names.
    new_suffix = ''

    #: Overwrite (or not) if glyph with new name already exists in font.
    overwrite = True

    # methods

    def __init__(self):
        self.title = 'suffix'
        self.height = (self.text_height * 3) + (self.padding_y * 5) + self.button_height
        self.column_1 = 33
        self.column_2 = 70
        self.w = FloatingWindow((self.width, self.height), self.title,)
        # old suffix
        x = self.padding_x
        y = self.padding_y
        self.w.old_suffix_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "old",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.old_suffix_value = EditText(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    text=self.old_suffix,
                    placeholder='old suffix',
                    sizeStyle=self.size_style)
        # new suffix
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.new_suffix_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "new",
                    sizeStyle=self.size_style)
        x += self.column_1
        self.w.new_suffix_value = EditText(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    text=self.new_suffix,
                    placeholder='new suffix',
                    sizeStyle=self.size_style)
        y += (self.text_height + self.padding_y)
        # checkbox overwrite
        self.w.overwrite_checkbox = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "overwrite",
                    value=self.overwrite,
                    sizeStyle=self.size_style)
        # apply button
        x = self.padding_x
        y += (self.text_height + self.padding_y)
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "apply",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    def apply_callback(self, sender):
        # get font
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                boolstring = [ False, True ]
                # get parameters
                self.old_suffix = self.w.old_suffix_value.get()
                self.new_suffix = self.w.new_suffix_value.get()
                self.overwrite = self.w.overwrite_checkbox.get()
                # print info
                print 'changing glyph name suffixes...\n'
                print '\told suffix: %s' % (self.old_suffix)
                print '\tnew suffix: %s' % (self.new_suffix)
                print '\toverwrite: %s' % boolstring[self.overwrite]
                print
                # batch change glyph names
                for glyph_name in glyph_names:
                    g = f[glyph_name]
                    # get glyphs with matching suffix
                    if has_suffix(g, self.old_suffix):
                        # switch suffixes : one.osf -> one.onum
                        if len(self.old_suffix) > 0 and len(self.new_suffix) > 0:
                            new_name = change_suffix(g, self.old_suffix, self.new_suffix)
                        # remove suffix : one.osf -> one
                        elif len(self.old_suffix) > 0 and len(self.new_suffix) == 0:
                            new_name = change_suffix(g, self.old_suffix, None)
                        # add suffix : one -> one.onum
                        elif len(self.old_suffix) == 0 and len(self.new_suffix) > 0:
                            new_name = '%s.%s' % (glyph_name, self.new_suffix)
                        else:
                            new_name = glyph_name
                        # new name not in font (rename)
                        if new_name != glyph_name:
                            if not f.has_key(new_name):
                                print '\trenaming %s to %s...' % (glyph_name, new_name)
                                g.name = new_name
                            # new name in font
                            else:
                                # overwrite
                                if self._overwrite:
                                    print "\toverwriting '%s' with '%s'" % (new_name, glyph_name)
                                    f.removeGlyph(_new_name)
                                    f.update()
                                    g.name = new_name
                                    g.update()
                                # do not overwrite
                                else:
                                    print "\t'%s' already exists in font, skipping '%s'" % (new_name, glyph_name)
                    # glyph does not have suffix
                    else:
                        pass
                    # done glyph
                # done font
                f.update()
                print
                print '...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
        pass
