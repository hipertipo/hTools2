===========
Conventions
===========

Part of the functionality in :py:mod:`hTools2` depends on a few conventions being followed – for example, the way font files are named, the project sub-folders structure, the name of data files etc.

This applies only to the objects in :py:mod:`hTools2.objects`, and to the dialogs which use these objects. All modules and generic dialogs work fine without any special setting.

--------
Overview
--------

In :py:mod:`hTools2`, each font-family is a separate project, and all projects are stored in one main root folder.

Every project contains a set of sub-folders to collect and organize ``,ufo`` sources, generated ``.otf`` fonts, additional data files etc. The same folder structure is used for all projects. Additional 'custom' folders per project are allowed.

Every project also contains a set of files with font-related data – for example, data for building composed glyphs, data for generating instances with interpolation, data about vertical metrics, data about the character set and glyph groups etc.

-------------------
The ``ROOT`` folder
-------------------

The paths system in :py:mod:`hTools2` is bootstrapped from one single path: the root folder in which all projects are contained. The default root folder is ``/_fonts``.

The path to this folder is stored in :py:attr:`hTools2.ROOT`, and currently needs to be edited by hand in the file ``hTools2/__init__.py``.::

    ROOT = '/_fonts'

This is the only hardcoded path in hTools2. After set, this path can be read via :py:attr:`hSettings.root`.

---------------
Project folders
---------------

All project folders live inside the ``ROOT`` folder. Project folder names start with an underscore, followed by the name of the font family. For example, the folder containing the files for the type family ‘Publica’ must be named ``_Publica``.::

    fonts/
        _Publica/
        _Quantica/
        ...
        test/
        ...

A typical root folder with projects would look like this:

.. ![hWorld](world.png "project folders")

Folders which do not start with an underscore are not recognized as projects, and are simply ignored by the tools.

-------------------
Project sub-folders
-------------------

In hTools2:

- every font-family is a project,
- every project is a folder, and
- every project contains a standard set of folders and files.

A typical project folder looks like this::

    _Publica/
        _docs/
        _libs/
        _otfs/
        _temp/
        _ttfs/
        _ufos/
        _vfbs/
        _woffs/

------------
Project libs
------------

Project libs are different kinds of data files contained in the `_libs/` folder of each project.::

    _libs/
        Publica.enc
        accents.plist
        composed.plist
        groups.plist
        info.plist
        interpol.plist
        spacing.plist
        vmetrics.plist

--------------
FTP connection
--------------

:py:mod:`hTools2` also includes a few functions to connect to a FTP server and upload files. This is specially handy for working with webfonts and live tests.

The FTP connection settings (``URL``, ``login``, ``password``) are stored in the :py:class:`hSettings` object, and can be edited with a special dialog.
