## hWorld

The `hWorld` object represents the local root folder, where all project folders live.

## Attributes

### hWorld.settings

A `hSettings` object with information about the local system.

    from hTools2.objects import hWorld
    w = hWorld()
    print w.settings

    >>> <hTools2.objects.hSettings instance at 0x12ac6b560>

### hWorld.context

The environment in which the current script is running.

The possible options are: `RoboFont`, `FontLab` and `NoneLab`.

    from hTools2.objects import hWorld
    w = hWorld()
    print w.context

    >>> RoboFont


## Methods

### hWorld.projects()

Returns a list of all project folders contained in the root folder.

According to [hTools conventions](http://hipertipo.com/content/htools2/about/conventions/), project folder names need to start with an underscore.

    from hTools2.objects import hWorld
    w = hWorld()
    print w.projects()

    >>> ['Elementar', 'EMono', 'Modular', ... , 'Publica']
