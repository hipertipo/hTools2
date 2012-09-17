Part of the functionality in hTools depends on a few conventions being followed – for example, the way font files are named, the project sub-folders structure, the name of data files etc.

This applies only to the objects in `hTools2.objects`, and to the dialogs which use these objects (‘hDialogs’). All modules and generic dialogs work fine without any special setting.

## Overview

In hTools, each font-family is a separate project, and all projects are stored in one main root folder.

Every project contains a set of dedicated sub-folders – for example for .ufo font sources, generated .otf fonts, additional data files etc. The same folder structure is used for all projects, but additional ‘custom’ folders per project are allowed.

Every project also contains a set of files with font-related data – for example a list of recipes for building composed glyphs, recipes for generating instances with interpolation, data about vertical metrics, an index of glyph names and groups, etc.

To use the existing interpolation tools for work on large families, it is also necessary to adopt a consistent naming scheme with numbers instead of style names.

## The ROOT folder

The whole hTools object model and paths system is bootstrapped using one single path: the folder in which all projects are contained. The default root folder is `/fonts`.

The path to this folder is stored in `hTools2.ROOT`, and needs to be edited by hand in the `hTools2/__init__.py` file. This is the only hardcoded path in hTools2.

After set, this path can be read via `hSettings.root`.

## Project folders

All project folders live inside the root folder.

Project folder names start with an underscore, followed by the name of the family. For example, the folder containing the files for the typeface family ‘Publica’ must be named `_Publica`.

A typical root folder with projects would look like this:

    fonts/
        _Publica/
        _Quantica/
        ...
        test/
        ...

Folders which do not start with an underscore are not recognized as projects, and are simply ignored by the tools.

## Project sub-folders

In hTools, every font-family is a project, and every project is a folder containing a standard set of font sources, sub-folders and data files.

A typical project folder looks like this:

    _Publica/
        _docs/  
        _libs/
        _otfs/
        _temp/
        _ttfs/
        _ufos/
        _vfbs/
        _woffs/

## Project libs

Project libs is a collective name for various kinds of data files contained in the `_libs/` folder of each project.

Included in the libs are recipes for building accented glyphs, recipes for generating instances with interpolation, data about vertical metrics, an index of glyph names and groups, etc.

    _libs/
        Publica.enc
        accents.plist
        composed.plist
        groups.plist
        info.plist
        interpol.plist
        spacing.plist
        vmetrics.plist

## FTP connection

hTools also includes a few functions to connect to a FTP server and upload files. This is specially handy for working with webfonts and live tests.

The FTP connection settings (URL, login, password) are stored in the `hSettings` object, and can be edited with a special dialog.
