# [h] move selected glyphs

from mojo.roboFont import CurrentFont, CurrentGlyph, version
from vanilla import *
from hTools2 import hDialog
from hTools2.dialogs.misc import Arrows, Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.messages import no_glyph_selected, no_font_open, no_layer_selected

class moveGlyphsDialog(hDialog):

    '''A dialog to move the selected glyphs in a font.

    .. image:: imgs/glyphs/move.png

    '''

    move_value = 70

    def __init__(self, verbose=True):
        self.title = "move"
        self.verbose = verbose
        self.height = self.square_button*3 + self.padding_y*5 + self.text_height*4 - 7
        self.w = HUDFloatingWindow((self.width, self.height), self.title)
        # arrows
        x = y = 0
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
                (x, y, -self.padding_x, self.text_height),
                "foreground",
                value=True,
                sizeStyle=self.size_style)
        y += self.text_height
        self.w.layers = CheckBox(
                (x, y, -self.padding_x, self.text_height),
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
                layers     = self.w.layers.get()

                if (layers and foreground) is not False:
                    boolstring = [ False, True ]

                    # print info
                    if self.verbose:
                        print 'moving selected glyphs...\n'
                        print '\tx: %s' % x
                        print '\ty: %s' % y
                        print '\tlayers: %s' % boolstring[layers]
                        print
                        print '\t',

                    # move glyphs
                    for glyph_name in glyph_names:
                        if self.verbose:
                            print glyph_name,

                        # all layers
                        if layers:
                            for layer_name in f.layerOrder:
                                glyph = f[glyph_name].getLayer(layer_name)
                                glyph.prepareUndo('move')
                                # RF 2.0
                                if version[0] == '2':
                                    glyph.moveBy((x, y))
                                # RF 1.8.X
                                else:
                                    glyph.move((x, y))
                                glyph.performUndo()

                        # active layer
                        if foreground:
                            f[glyph_name].prepareUndo('move')
                            # RF 2.0
                            if version[0] == '2':
                                f[glyph_name].moveBy((x, y))
                            # RF 1.8.X
                            else:
                                f[glyph_name].move((x, y))
                            f[glyph_name].performUndo()

                        # RF 2.0
                        if version[0] == '2':
                            f[glyph_name].changed()
                        # RF 1.8.X
                        else:
                            f[glyph_name].update()

                    # done with font
                    # RF 2.0
                    if version[0] == '2':
                        f.changed()
                    # RF 1.8.X
                    else:
                        f.update()

                    if self.verbose:
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
