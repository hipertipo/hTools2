# [h] move selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont, CurrentGlyph

except ImportError:
    from robofab.world import CurrentFont, CurrentGlyph

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Arrows, Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open, no_layer_selected

# objects

class moveGlyphsDialog(hDialog):

    """A dialog to move the selected glyphs in a font.

    .. image:: imgs/glyphs/move.png

    """

    # attributes

    move_value = 70

    # methods

    def __init__(self):
        self.title = "move"
        self.height = (self.square_button * 3) + (self.padding_y * 5) + (self.text_height * 4) - 7
        self.w = FloatingWindow((self.width, self.height), self.title)
        # arrows
        x = 0
        y = 0
        self.w.arrows = Arrows(
                    (x, y),
                    callbacks=dict(
                        left=self.left_callback, 
                        right=self.right_callback, 
                        up=self.up_callback, 
                        down=self.down_callback,
                        leftDown=self.down_left_callback, 
                        rightDown=self.down_right_callback, 
                        leftUp=self.up_left_callback, 
                        rightUp=self.up_right_callback,
                    ),
                    arrows=[
                        'left', 'right', 'up', 'down',
                        'leftUp', 'leftDown', 'rightUp', 'rightDown',
                    ])
        # spinner
        x = 0
        y += self.w.arrows.getPosSize()[3]
        self.w.spinner = Spinner(
                    (x, y),
                    default='20',
                    integer=True,
                    label='delta')
        # checkboxes
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        self.w.foreground = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "foreground",
                    value=True,
                    sizeStyle=self.size_style)
        y += self.text_height
        self.w.layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "layers",
                    value=False,
                    sizeStyle=self.size_style)
        # open dialog
        self.w.open()

    # arrows callbacks

    def up_left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((-value, value))

    def up_right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((value, value))

    def down_left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((-value, -value))

    def down_right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((value, -value))

    def left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((-value, 0))

    def right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((value, 0))

    def up_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((0, value))

    def down_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_glyphs((0, -value))

    # apply transformation

    def move_glyphs(self, (x, y)):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            # transform glyphs
            if len(glyph_names) > 0:
                # get options
                foreground = self.w.foreground.get()
                layers = self.w.layers.get()
                if (layers and foreground) is not False:
                    boolstring = [ False, True ]
                    # print info
                    print 'moving selected glyphs...\n'
                    print '\tx: %s' % x
                    print '\ty: %s' % y
                    print '\tlayers: %s' % boolstring[layers]
                    print
                    print '\t',
                    # move glyphs
                    for glyph_name in glyph_names:
                        print glyph_name,
                        f[glyph_name].prepareUndo('move')
                        # all layers
                        if layers:
                            for layer_name in f.layerOrder:
                                glyph = f[glyph_name].getLayer(layer_name)
                                glyph.move((x, y))
                        # active layer
                        if foreground:
                            f[glyph_name].move((x, y))
                        # done glyph
                        f[glyph_name].performUndo()
                        f[glyph_name].update()
                    # done font
                    f.update()
                    print
                    print '\n...done.\n'
                # no layer selected
                else:
                    print no_layer_selected
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
