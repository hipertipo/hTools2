hSettings
=========

An object used to store information about local settings and preferences.

When initialized, `hSettings` reads the root folder for projects from `hTools2.ROOT` and loads the `hSettings.plist` file from this directory into a dictionary, `hSettings.hDict`.

Attributes
----------

### hSettings.hDict

A dictionary containing several kinds of information about the local installation.

### hSettings.path

The full path to the `hSettings.plist` file.

### hSettings._root

The path to the local root folder for project files, imported from `hTools2.ROOT`.

This is the only path in `hTools2` that needs to be hardcoded.

### hSettings._filename

The name of the settings file. By default, `hSettings.plist`.

Methods
-------

### hSettings.read()

Read the local `hSettings.plist` file at `hSettings.path` into `hSettings.hDict`.

### hSettings.write()

Write the contents of `hSettings.hDict` to the `hSettings.plist` file.

### hSettings.print_()

Prints the contents of `hSettings.hDict` to the output window.

Example
-------

	# read the hSettings object

	s = hSettings()
	print s

	>>> <hTools2.objects.hSettings instance at 0x11f6617a0\>

	# view settings dictionary

	print s.hDict.keys()

	>>> ['ftp_password', 'ftp_login', 'ftp_url', 'ftp_folder', 'root']

	for k in s.hDict.keys():
    	print k, s.hDict[k]

	>>> ftp_password None
	>>> ftp_login None
	>>> ftp_url None
	>>> root None
	>>> ftp_folder None
