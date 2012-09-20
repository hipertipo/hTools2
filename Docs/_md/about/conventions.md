## Conventions

Part of the functionality in hTools2 depends on a few conventions being followed – for example, the way font files are named, the project sub-folders structure, the name of data files etc.

This applies only to the objects in `hTools2.objects`, and to the dialogs which use these objects (available as a separate package named `hScripts`). All modules and generic dialogs work fine without any special setting.

### Overview

In hTools2, each font-family is a separate project, and all projects are stored in one main root folder.

Every project contains a set of sub-folders to collect and organize `.ufo` sources, generated `.otf` fonts, additional data files etc. The same folder structure is used for all projects. Additional ‘custom’ folders per project are allowed.

Every project also contains a set of files with font-related data – for example, data for building composed glyphs, data for generating instances with interpolation, data about vertical metrics, data about the character set and glyph groups etc.

#### The `ROOT` folder

The object model and paths system in hTools2 is bootstrapped from one path: the folder in which all projects are contained. The default root folder is `/_fonts`.

The path to this folder is stored in `hTools2.ROOT`, and currently needs to be edited by hand in the `hTools2/__init__.py` file – this is the only hardcoded path in hTools2. After set, this path can be read via `hSettings.root`.

#### Project folders

All project folders live inside the `root` folder:

![hWorld](../_imgs/world.png "project folders")

Project folder names start with an underscore, followed by the name of the font family. For example, the folder containing the files for the type family ‘Publica’ must be named `_Publica`.

A typical root folder with projects would look like this:

    fonts/
        _Publica/
        _Quantica/
        ...
        test/
        ...

Folders which do not start with an underscore are not recognized as projects, and are simply ignored by the tools.

#### Project sub-folders

In hTools2,

- *every font-family is a project*,
- *every project is a folder*, and
- *every project contains a standard set of folders and files*.

A typical project folder looks like this:

![hProject](../_imgs/project.png "project sub-folders")

    _Publica/
        _docs/
        _libs/
        _otfs/
        _temp/
        _ttfs/
        _ufos/
        _vfbs/
        _woffs/

#### Project libs

Project libs are different kinds of data files contained in the `_libs/` folder of each project.

![hLibs](../_imgs/libs.png "project libs")

    _libs/
        Publica.enc
        accents.plist
        composed.plist
        groups.plist
        info.plist
        interpol.plist
        spacing.plist
        vmetrics.plist

### FTP connection

hTools2 also includes a few functions to connect to a FTP server and upload files. This is specially handy for working with webfonts and live tests.

The FTP connection settings (URL, login, password) are stored in the `hSettings` object, and can be edited with a special dialog.
