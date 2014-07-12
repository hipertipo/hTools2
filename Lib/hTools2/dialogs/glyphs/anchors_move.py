# [h] move anchors in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont

except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
from hTools2.dialogs.misc import Arrows, Spinner
from hTools2.modules.fontutils import get_glyphs
from hTools2.modules.anchors import move_anchors
from hTools2.modules.messages import no_glyph_selected, no_font_open

# objects

class moveAnchorsDialog(hDialog):

    '''A dialog to move the anchors in the selected glyphs of the current font.

    .. image:: imgs/glyphs/move-anchors.png

    '''

    # attributes

    move_default = 70

    anchors_top = True
    anchors_bottom = False
    anchors_left = False
    anchors_right = False
    anchors_base = True
    anchors_accents = True
    anchors_layers = False

    # methods

    def __init__(self):
        self.title = "anchors"
        self.width = (self.square_button * 3) + (self.padding_x * 2) - 2
        self.height = (self.square_button * 3) + (self.padding_y * 7) + (self.text_height * 3) + self.nudge_button + 3
        self.w = FloatingWindow((self.width, self.height), self.title)
        #---------------
        # arrow buttons
        #---------------
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
        #----------
        # spinners
        #----------
        x = 0
        y += self.w.arrows.getPosSize()[3]
        self.w.spinner = Spinner(
                    (x, y),
                    default=self.move_default,
                    integer=True,
                    label='delta')
        #------------
        # checkboxes
        #------------
        # top anchors
        x = self.padding_x
        y += self.w.spinner.getPosSize()[3]
        shift_x = ((self.width - (self.padding_x * 2)) / 4) + 1
        self.w.anchors_top = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "T",
                    value=self.anchors_top,
                    sizeStyle=self.size_style)
        # bottom anchors
        x += shift_x
        self.w.anchors_bottom = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "B",
                    value=self.anchors_bottom,
                    sizeStyle=self.size_style)
        x += shift_x
        self.w.anchors_left = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "L",
                    value=self.anchors_left,
                    sizeStyle=self.size_style)
        x += shift_x
        self.w.anchors_right = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "R",
                    value=self.anchors_right,
                    sizeStyle=self.size_style)
        # base anchors
        x = self.padding_x
        y += self.text_height + (self.padding_y / 2)
        self.w.anchors_base = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "base",
                    value=self.anchors_base,
                    sizeStyle=self.size_style)
        # accent anchors
        x += (shift_x * 2) - 3
        self.w.anchors_accents = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "accent",
                    value=self.anchors_accents,
                    sizeStyle=self.size_style)
        # all layers
        x = self.padding_x
        y += self.text_height + (self.padding_y / 2)
        self.w.anchors_layers = CheckBox(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    "all layers",
                    value=self.anchors_layers,
                    sizeStyle=self.size_style)
        # open dialog
        self.w.open()

    # callbacks

    def up_left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((-value, value))

    def up_right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((value, value))

    def down_left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((-value, -value))

    def down_right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((value, -value))

    def left_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((-value, 0))

    def right_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((value, 0))

    def up_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((0, value))

    def down_callback(self, sender):
        value = int(self.w.spinner.value.get())
        self.move_anchors((0, -value))

    # apply

    def get_parameters(self):
        # get values
        anchors_top = self.w.anchors_top.get()
        anchors_bottom = self.w.anchors_bottom.get()
        anchors_left = self.w.anchors_left.get()
        anchors_right = self.w.anchors_right.get()
        anchors_base = self.w.anchors_base.get()
        anchors_accents = self.w.anchors_accents.get()
        self._anchors_layers = self.w.anchors_layers.get()
        # make list with anchor names
        anchor_names = []
        if anchors_top:
            if anchors_base:
                anchor_names.append('top')
            if anchors_accents:
                anchor_names.append('_top')
        if anchors_bottom:
            if anchors_base:
                anchor_names.append('bottom')
            if anchors_accents:
                anchor_names.append('_bottom')
        if anchors_left:
            if anchors_base:
                anchor_names.append('left')
            if anchors_accents:
                anchor_names.append('_left')
        if anchors_right:
            if anchors_base:
                anchor_names.append('right')
            if anchors_accents:
                anchor_names.append('_right')
        # save names
        self.anchor_names = anchor_names

    def move_anchors(self, (x, y)):
        f = CurrentFont()
        if f is not None:
            glyph_names = get_glyphs(f)
            if len(glyph_names) > 0:
                self.get_parameters()
                print 'moving anchors in glyphs...\n'
                print '\tanchors: %s' % self.anchor_names
                print '\tmove: %s, %s' % (x, y)
                print
                print '\t',
                for glyph_name in glyph_names:
                    print glyph_name,
                    if self.anchors_layers:
                        for layer_name in f.layerOrder:
                            layer_glyph = f[glyph_name].getLayer(layer_name)
                            layer_glyph.prepareUndo('move anchors')
                            move_anchors(layer_glyph, self.anchor_names, (x, y))
                            layer_glyph.performUndo()
                            layer_glyph.update()
                        # f[glyph_name].update()
                    else:
                        f[glyph_name].prepareUndo('move anchors')
                        move_anchors(f[glyph_name], self.anchor_names, (x, y))
                        f[glyph_name].performUndo()
                    # done glyph
                    f[glyph_name].update()
                f.update()
                print
                print '\n...done.\n'
            # no glyph selected
            else:
                print no_glyph_selected
        # no font open
        else:
            print no_font_open
