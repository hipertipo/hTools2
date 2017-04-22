# [h] preview glyph interpolation with another font

import os
from vanilla import *
from AppKit import NSColor
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.roboFont import AllFonts, CurrentFont, RGlyph, CurrentGlyph
from mojo.events import addObserver, removeObserver
from mojo.drawingTools import *
from hTools2 import hDialog
from hTools2.modules.fontutils import get_full_name
from hTools2.extras.grapefruit import Color

# object

class interpolationPreviewDialog(hDialog, BaseWindowController):

    """A dialog to preview glyph interpolation with another font.

    .. image:: imgs/glyphs/interpolation-preview.png

    """

    # attributes

    #: The amount of interpolation steps to preview.
    steps = 7

    #: A second font for use as the second interpolation master.
    f2 = None

    #: Default color of the interpolation preview.
    mark_color = 0, 0.5, 1, 0.65

    #: Default color of the interpolation preview.
    mark_color_2 = mark_color

    #: Turn console notifications on/off.
    verbose = True

    # methods

    def __init__(self):
        # make window
        self.width *= 2
        self.height = self.text_height + self.button_height*3 + self.padding*4
        self.w = FloatingWindow((self.width, self.height), "interpol")
        # get colors
        x = y = p = self.padding
        self.w.mark_color = ColorWell(
                (x, y, -p, self.button_height),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self.mark_color))
        y += self.button_height + p
        self.w.mark_color_2 = ColorWell(
                (x, y, -p, self.button_height),
                color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self.mark_color_2))
        # show all fonts
        self.get_fonts()
        y += self.button_height + p
        self.w.f2 = PopUpButton(
                    (x, y, -p, self.text_height),
                    sorted(self.all_fonts.keys()),
                    sizeStyle='small')
        # show preview checkbox
        y += self.text_height + p*0.5
        self.w.on_off_button = CheckBox(
                (x, y, -p, self.button_height),
                "show preview",
                value=True,
                sizeStyle='small',
                callback=self.view_callback
            )
        # turn visualization ON
        self.on()
        # add observers
        addObserver(self, "update_callback", "newFontDidOpen")
        addObserver(self, "update_callback", "fontDidOpen")
        addObserver(self, "update_callback", "fontDidClose")
        # open window
        self.setUpBaseWindowBehavior()
        self.w.open()

    # callbacks

    def windowCloseCallback(self, sender):
        self.off()
        super(interpolationPreviewDialog, self).windowCloseCallback(sender)
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")

    def view_callback(self, sender):
        if sender.get():
            self.on()
        else:
            self.off()
        # update glyph view
        g = CurrentGlyph()
        g.update()

    def update_callback(self, sender):
        # print 'updating fonts'
        self.get_fonts()
        self.w.f2.setItems(sorted(self.all_fonts.keys()))

    # methods

    def get_fonts(self):
        self.all_fonts = {}
        all_fonts = AllFonts()
        if len(all_fonts) > 0:
            for font in all_fonts:
                self.all_fonts[(get_full_name(font))] = font

    def on(self):
        addObserver(self, "draw_background", "drawBackground")
        if self.verbose:
            print 'interpolation preview is ON'

    def off(self):
        removeObserver(self, "drawBackground")
        if self.verbose:
            print 'interpolation preview is OFF'

    def draw_background(self, notification):
        s  = notification['scale']
        g1 = notification['glyph']
        # get colors
        _mark_color = self.w.mark_color.get()
        _mark_color = (
            _mark_color.redComponent(),
            _mark_color.greenComponent(),
            _mark_color.blueComponent(),
            _mark_color.alphaComponent(),
        )
        _mark_color_2 = self.w.mark_color_2.get()
        _mark_color_2 = (
            _mark_color_2.redComponent(),
            _mark_color_2.greenComponent(),
            _mark_color_2.blueComponent(),
            _mark_color_2.alphaComponent(),
        )
        # get fonts
        f1 = CurrentFont()
        i  = self.w.f2.get()
        f2 = self.all_fonts[sorted(self.all_fonts.keys())[i]]
        r = 2
        # interpolate steps
        if f1 != f2:
            # check if f2 has this glyph
            if f2.has_key(g1.name):
                g2 = f2[g1.name]
                # check if glyph in f2 is compatible
                if g1.isCompatible(g2):
                    # create colors
                    c1 = Color.NewFromRgb(*_mark_color)
                    c2 = Color.NewFromRgb(*_mark_color_2)
                    colors = c1.Gradient(c2, self.steps)
                    # create steps and draw
                    for i in range(self.steps):
                        factor = i * (1.0 / (self.steps-1))
                        g3 = RGlyph()
                        g3.interpolate(factor, g1, g2)
                        save()
                        fill(None)
                        stroke(*colors[i])
                        strokeWidth(s)
                        if g3.width != g1.width:
                            diff = g3.width - g1.width
                            translate(-diff*0.5, 0)
                        drawGlyph(g3)
                        for c in g3.contours:
                            for pt in c.points:
                                rect(pt.x-r, pt.y-r, r*2, r*2)
                        restore()
                    # done
                    # restore()
            else:
                if self.verbose:
                    print '%s not in font 2' % g1.name

if __name__ == '__main__':

    interpolationPreviewDialog()
