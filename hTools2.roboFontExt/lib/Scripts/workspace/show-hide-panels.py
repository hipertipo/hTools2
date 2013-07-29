# [h] show/hide panels

### thanks Frederik ###

from AppKit import NSApp, NSPanel

from mojo.extensions import getExtensionDefault, setExtensionDefault

# get panels
windows = NSApp.windows()
panels = [ window for window in windows if isinstance(window, NSPanel) ]

# print panels

# get state
show_panels = getExtensionDefault('com.hipertipo.showHidePanels', fallback=True)

# show panels
if show_panels:
    for panel in panels:
        panel.orderOut_(None)
    setExtensionDefault('com.hipertipo.showHidePanels', False)

# hide panels
if show_panels is False:
    for panel in panels:
        panel.orderBack_(None)
    setExtensionDefault('com.hipertipo.showHidePanels', True)
