# [h] close all panels

from AppKit import NSApp, NSPanel

windows = NSApp.windows()
panels = [window for window in windows if isinstance(window, NSPanel)]

for panel in panels:
    panel.performClose_(None)
