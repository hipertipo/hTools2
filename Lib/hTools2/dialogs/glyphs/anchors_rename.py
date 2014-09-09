# [h] rename anchors in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.modules.anchors import rename_anchor
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class renameAnchorsDialog(hDialog):

    """A dialog to rename the anchors in the selected glyphs of the current font.

    .. image:: imgs/glyphs/anchors-rename.png

    """

    # attributes

    column_1 = 33
    column_2 = 70

    # methods

    def __init__(self):
        self.title = 'anchors'
        self.height = (self.text_height * 2) + (self.padding_y * 4) + self.button_height
        self.w = FloatingWindow((self.width, self.height), self.title)
        x = self.padding_x
        y = self.padding_y
        # old name label
        self.w._old_name_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "old",
                    sizeStyle=self.size_style)
        x += self.column_1
        # old name
        self.w._old_name_value = EditText(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    placeholder='old name',
                    text='',
                    sizeStyle=self.size_style)
        x = self.padding_x
        y += self.text_height + self.padding_y
        # new name label
        self.w._new_name_label = TextBox(
                    (x, y,
                    self.column_1,
                    self.text_height),
                    "new",
                    sizeStyle=self.size_style)
        x += self.column_1
        # new name
        self.w._new_name_value = EditText(
                    (x, y,
                    self.column_2,
                    self.text_height),
                    placeholder='new name',
                    text='',
                    sizeStyle=self.size_style)
        # button
        x = self.padding_x
        y += self.text_height + self.padding_y
        self.w.button_apply = SquareButton(
                    (x, y,
                    -self.padding_x,
                    self.button_height),
                    "rename",
                    callback=self.apply_callback,
                    sizeStyle=self.size_style)
        # open window
        self.w.open()

    def apply_callback(self, sender):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                # get parameters
                old = self.w._old_name_value.get()
                new = self.w._new_name_value.get()
                boolstring = (False, True)
                # print info
                print 'renaming anchors in glyphs...\n'
                print '\told name: %s' % old
                print '\tnew name: %s' % new
                print
                print '\t',
                # change anchors names
                for glyph_name in glyph_names:
                    print glyph_name,
                    # rename anchor
                    f[glyph_name].prepareUndo('rename anchor')
                    has_name = rename_anchor(f[glyph_name], old, new)
                    f[glyph_name].performUndo()
                    f[glyph_name].update()
                # done
                f.update()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
