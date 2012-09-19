## Overview

hTools2 is organized in three main layers:

- modules
- objects
- dialogs

### Modules

Modules are the base layer of hTools, and are used to collect and organize low-level, generic, reusable functions.

Each module is dedicated to one aspect of font data – for example `interpol.py` contains functions to work with interpolation, `anchors.py` deals with anchors, and so on.

hTools modules rely heavily on RoboFab to manipulate .ufo font files.

hTools also integrates a few third-party external modules in a special `hTools.extras` folder – for example `colorsys.py` for dealing with color conversions, `nudge.py` for special manipulation of bezier points etc.

### Objects

hTools objects are built on top of the functionality contained in the modules, and provide a simple API for manipulating font files and related data in projects.

### Dialogs

Scripts and dialogs make hTools2 objects and modules easily accessible in applications. Current scripts in hTools2 are built specially for use with RoboFont and NodeBox.

In RoboFont, scripts can be accessed with the ‘Extensions’ section of the main application menu, or via keyboard shortcuts (if properly configured).

In addition to RoboFont scripts, hTools also includes a second set of scripts for use with [NodeBox](http://nodebox.net/). These scripts deal mainly with special visualizations of glyphs and fonts, for use during proofing and for output of visual presentation material.
