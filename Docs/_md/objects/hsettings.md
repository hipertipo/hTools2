## hSettings

An object to store information about local settings and preferences.

When initialized, `hSettings` reads the root folder for projects from `hTools2.ROOT`, loads the `hSettings.plist` file from this directory into a dictionary, and stores it in `hSettings.hDict`.


### Attributes

#### hSettings.hDict

A dictionary containing general information about the local installation.

Currently, `hDict` contains only a few entries for FTP settings, and an additional custom test folder for .otfs.

    from hTools2.objects import hSettings
    s = hSettings()
    print s.hDict.keys()

    >>> ['test', 'ftp']

    for k in s.hDict['ftp'].keys():
        print k, s.hDict['ftp'][k]

    >>> url myserver.com
    >>> folder www/mysite/assets/fonts
    >>> password abcd1234
    >>> login username

#### hSettings.path

The full path to the `hSettings.plist` file.

    from hTools2.objects import hSettings
    s = hSettings()
    print s.path

    >>> /fonts/hSettings.plist

#### hSettings.root

The path to the local root folder for project files, imported from `hTools2.ROOT`. This is the only hardcoded path in `hTools2`.

    from hTools2.objects import hSettings
    s = hSettings()
    print s.root

    >>> /fonts

#### hSettings.filename

The name of the settings file. By default, `hSettings.plist`.

    from hTools2.objects import hSettings
    s = hSettings()
    print s.filename

    >>> hSettings.plist

### Methods

#### hSettings.read()

Reads the local `hSettings.plist` file at `hSettings.path` into `hSettings.hDict`. This method is called when the `hSettings` object is initialized.

#### hSettings.write()

Writes the contents of `hSettings.hDict` to the `hSettings.plist` file.
