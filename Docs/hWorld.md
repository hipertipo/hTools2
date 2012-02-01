class hWorld
============

The `hWorld` object represents the local root folder where all projects live. It uses the root folder defined in the linked `hSettings` object to collect all existing projects in a list.

Attributes
----------

### hWorld.settings

A `hSettings` object, with information about the current system.

### context

The environment under which the current script is being acessed.

The possible options are:

- `RoboFont`
- `FontLab`
- `NoneLab`

Methods
-------

### hWorld.projects()

Returns a list of projects in the current root folder.

Project folder names start with an underscore, for example `_Publica`.
