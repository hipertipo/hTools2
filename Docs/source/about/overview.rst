========
Overview
========

-----
About
-----

``hTools2`` is a collection of tools and objects for type-design & font-production work. It is written in Python_ and specially tailored for use with RoboFont_.

The core Python modules and objects can also be used with `FontLab Studio`_, ‘NoneLab’ (pure Python) and `DrawBot`_.

.. _Python : http://python.org/
.. _RoboFont : http://robofont.com/
.. _FontLab Studio: http://www.fontlab.com/font-editor/fontlab-studio/
.. _DrawBot : http://drawbot.com/

``hTools2`` is built with RoboFab_ and vanilla_. It uses the UFO_ font format to store font sources, and plist_ files to store different kinds of font data.

.. _RoboFab : http://robofab.org/
.. _vanilla : http://code.typesupply.com/wiki/Vanilla
.. _UFO : http://unifiedfontobject.org/
.. _plist : https://en.wikipedia.org/wiki/Property_list

---------
Structure
---------

:py:mod:`hTools2` is organized in three main packages: :py:mod:`modules`, :py:mod:`objects` and :py:mod:`dialogs`.

.. ![hTools2](hTools2.png "hTools2 contents")

The additional package :py:mod:`extras` is used to keep custom modules which are not part of the public distribution of :py:mod:`hTools2`.

^^^^^^^
Modules
^^^^^^^

Modules are the base layer of :py:mod:`hTools2`, and are used to collect and organize low-level, generic, reusable functions.

.. ![modules](modules.png "modules")

Each module is dedicated to one aspect of font data – for example :py:mod:`interpol` contains functions to work with interpolation, :py:mod:`anchors` deals with anchors, and so on.

:py:mod:`hTools2` modules rely heavily on underlying functionality provided by RoboFab_ and RoboFont_ to manipulate fonts.

.. _RoboFab : http://robofab.org/ 
.. _RoboFont : http://robofont.com/ 

:py:mod:`hTools2` also integrates a few third-party external modules in a special :py:mod:`extras` package, for example :py:mod:`colorsys` for dealing with color conversions and :py:mod:`nudge` for special manipulation of bezier points.

^^^^^^^
Objects
^^^^^^^

:py:mod:`hTools2` objects are built on top of the functionality contained in the modules, and provide a simple API for manipulating font files and related data in projects.

.. ![objects](objects.png "objects")

^^^^
Libs
^^^^

Metadata in font projects is stored in standardized ``plist`` and plain text files.

.. ![libs](libs.png "libs")

^^^^^^^
Dialogs
^^^^^^^

Scripts and dialogs make :py:mod:`hTools2` objects and modules easily accessible in applications. Current scripts in :py:mod:`hTools2` are built specially for use with RoboFont.

.. ![dialogs](dialogs.png "dialogs")

In RoboFont, scripts can be accessed with the ‘Extensions’ section of the main application menu, or via keyboard shortcuts (if properly configured).
