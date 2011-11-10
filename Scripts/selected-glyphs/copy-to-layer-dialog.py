# [h] copy selected glyphs to layer dialog

from vanilla import *
from AppKit import NSColor

# from hTools2.modules.fileutils import getGlyphs

#f = CurrentFont()
#for gName in f.selection:
#    print gName

class copySelectedGlyphsToLayerDialog(object):

    _title = 'copy to layer'
    _mark_color = (1, 0, 0, 1)

    def __init__(self, font):
        self.font = font
        self.w = FloatingWindow((190, 140), self._title, closable=False)
        # target layer
        self.w._layers_label = TextBox((10, 10, -10, 17), "target layer")
        self.w._layers_value = PopUpButton((10, 35, -10, 20), self.font.layerOrder)
        # color
        self.w.mark_checkbox = CheckBox((10, 70, -10, 20), "mark glyphs", value=True)
        self.w.mark_color = ColorWell((120, 70, -13, 20), color=NSColor.colorWithCalibratedRed_green_blue_alpha_(*self._mark_color))
        # buttons
        self.w.button_apply = Button((10, -45, 80, 0), "apply", callback=self.apply_callback)
        self.w.button_close = Button((-90, -45, 80, 0), "close", callback=self.close_callback)
        self.w.open()

    def apply_callback(self, sender):
        _layer_index = self.w._layers_value.get()
        _layer_name = self.font.layerOrder[_layer_index]

        _mark = self.w.mark_checkbox.get()
        _mark_color = self.w.mark_color.get()
        _mark_color = (_mark_color.redComponent(), _mark_color.greenComponent(), _mark_color.blueComponent(), _mark_color.alphaComponent())

        print 'copying outlines to %s...' % _layer_name
        for gName in self.font.selection:
            f[gName].prepareUndo('change sidebearings')
            print '\t%s' % gName,
            f[gName].copyToLayer(_layer_name, clear=True)
            if _mark:
                f[gName].mark = _mark_color
            f[gName].performUndo()
            f[gName].update()
        print '...done.\n'

    def close_callback(self, sender):
        self.w.close()

f = CurrentFont()
copySelectedGlyphsToLayerDialog(f)


#swapToLayer(layerName)
#font.removeLayer(layerName)

