## Overview

`hTools2` is organized in three main layers: *modules*, *objects* and *dialogs*.

![hTools2](../_imgs/hTools2.png "hTools2 contents")

To each of these layers corresponds one folder inside the `hTools2` package.

The fourth folder, `extras`, is used to keep custom modules which are not part of the public distribution of `hTools2`.

### Modules

Modules are the base layer of `hTools2`, and are used to collect and organize low-level, generic, reusable functions.

![modules](../_imgs/modules.png "modules")

Each module is dedicated to one aspect of font data – for example `interpol.py` contains functions to work with interpolation, `anchors.py` deals with anchors, and so on.

`hTools2` modules rely heavily on underlying functionality provided by RoboFab and RoboFont to manipulate fonts.

`hTools2` also integrates a few third-party external modules in a special `extras` folder, for example `colorsys.py` for dealing with color conversions and `nudge.py` for special manipulation of bezier points.

### Objects

`hTools2` objects are built on top of the functionality contained in the modules, and provide a simple API for manipulating font files and related data in projects.

![objects](../_imgs/objects.png "objects")

### Dialogs

Scripts and dialogs make `hTools2` objects and modules easily accessible in applications. Current scripts in `hTools2` are built specially for use with RoboFont and NodeBox.

![dialogs](../_imgs/dialogs.png "dialogs")

In RoboFont, scripts can be accessed with the ‘Extensions’ section of the main application menu, or via keyboard shortcuts (if properly configured).

In addition to RoboFont scripts, hTools also includes a second set of scripts for use with [NodeBox](http://nodebox.net/). These scripts deal mainly with special visualizations of glyphs and fonts, for use during proofing and for output of visual presentation material.
