# [h] move anchors in selected glyphs

# imports

try:
    from mojo.roboFont import CurrentFont
except ImportError:
    from robofab.world import CurrentFont

from vanilla import *

from hTools2 import hDialog
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
        x = self.padding_x
        y = self.padding_y
        x1 = x + (self.square_button * 1) - 1
        x2 = x + (self.square_button * 2) - 2
        # up
        self.w.up = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8673),
                    callback=self.up_callback)
        # up left
        self.w.up_left = SquareButton(
                    (x, y,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8598),
                    callback=self.up_left_callback,
                    sizeStyle=self.size_style)
        # up right
        self.w.up_right = SquareButton(
                    (x2 + 8, y,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8599),
                    callback=self.up_right_callback,
                    sizeStyle=self.size_style)
        y += self.square_button - 1
        # left
        self.w.left = SquareButton(
                    (x, y,
                    self.square_button,
                    self.square_button),
                    unichr(8672),
                    callback=self.left_callback)
        # right
        self.w.right = SquareButton(
                    (x2, y,
                    self.square_button,
                    self.square_button),
                    unichr(8674),
                    callback=self.right_callback)
        y += self.square_button - 1
        # down left
        self.w.down_left = SquareButton(
                    (x, y + 8,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8601),
                    callback=self.down_left_callback,
                    sizeStyle=self.size_style)
        # down
        self.w.down = SquareButton(
                    (x1, y,
                    self.square_button,
                    self.square_button),
                    unichr(8675),
                    callback=self.down_callback)
        # down right
        self.w.down_right = SquareButton(
                    (x2 + 8, y + 8,
                    self.square_button - 8,
                    self.square_button - 8),
                    unichr(8600),
                    callback=self.down_right_callback,
                    sizeStyle=self.size_style)
        # move offset
        y += self.square_button + self.padding_y
        self.w.move_value = EditText(
                    (x, y,
                    -self.padding_x,
                    self.text_height),
                    self.move_default,
                    sizeStyle=self.size_style,
                    readOnly=self.read_only)
        #----------
        # spinners
        #----------
        y += self.text_height + self.padding_y
        self.w.minus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.minus_001_callback)
        x += self.nudge_button - 1
        self.w.plus_001 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.plus_001_callback)
        x += self.nudge_button - 1
        self.w._minus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.minus_010_callback)
        x += self.nudge_button - 1
        self.w.plus_010 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.plus_010_callback)
        x += self.nudge_button - 1
        self.w.minus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '-',
                    sizeStyle=self.size_style,
                    callback=self.minus_100_callback)
        x += self.nudge_button - 1
        self.w.plus_100 = SquareButton(
                    (x, y,
                    self.nudge_button,
                    self.nudge_button),
                    '+',
                    sizeStyle=self.size_style,
                    callback=self.plus_100_callback)
        #------------
        # checkboxes
        #------------
        # top anchors
        x = self.padding_x
        y += self.padding_y + self.nudge_button
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

    # spinners

    def minus_001_callback(self, sender):
        value = int(self.w.move_value.get()) - 1
        if value >= 0:
            self.w.move_value.set(value)

    def minus_010_callback(self, sender):
        value = int(self.w.move_value.get()) - 10
        if value >= 0:
            self.w.move_value.set(value)

    def minus_100_callback(self, sender):
        value = int(self.w.move_value.get()) - 100
        if value >= 0:
            self.w.move_value.set(value)

    def plus_001_callback(self, sender):
        value = int(self.w.move_value.get()) + 1
        self.w.move_value.set(value)

    def plus_010_callback(self, sender):
        value = int(self.w.move_value.get()) + 10
        self.w.move_value.set(value)

    def plus_100_callback(self, sender):
        value = int(self.w.move_value.get()) + 100
        self.w.move_value.set(value)

    # callbacks

    def up_left_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((-value, value))

    def up_right_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((value, value))

    def down_left_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((-value, -value))

    def down_right_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((value, -value))

    def left_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((-value, 0))

    def right_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((value, 0))

    def up_callback(self, sender):
        value = int(self.w.move_value.get())
        self.move_anchors((0, value))

    def down_callback(self, sender):
        value = int(self.w.move_value.get())
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
