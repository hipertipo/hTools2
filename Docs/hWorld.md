class hWorld
============


Attributes
----------

### settings

A `hSettings` object, with information about the current system.

### context

The environment under which the current script is being acessed.

The possible options are:

- `RoboFont`
- `FontLab`
- `NoneLab`


Methods
-------

### projects()

Returns a list of projects in the current root folder.

Project folder names start with an underscore, for example `_Publica`.

