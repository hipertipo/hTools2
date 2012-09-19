## sysutils

#### `get_context()`

Checks the environment from which the current script is being called, and returns a string with the matching identification.

The possible values are `RoboFont`, `FontLab` and `NoneLab`.

    from hTools2.modules.sysutils import get_context
    print get_context()

    >>> RoboFont
