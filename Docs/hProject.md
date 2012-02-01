hProject
========

The `hProject` object represents a family of fonts and related data, contained in a common folder with a pre-defoned sub-folder structure:

```
  _MyProject/
    _docs/
      *.*
    _libs/
      accents.plist
      charset.enc
      composed.plist
      groups.plist
      info.plist
      interpol.plist
      spacing.plist
      vmetrics.plist
    _otfs/
      *.otf
    _temp/
      *.*
    _ttfs/
      *.ttf
    _ufos/
      *.ufo
    _vfbs/
      *.vfb
    _woffs/
      *.woff
```

Methods
-------

### hProject.read_libs()

Read all project libs from their `.plist` files into one dictionary.

### hProject.import_encoding()

Import glyph names and order from the project’s encoding file.

### hProject.write_lib(lib_name)

Write the lib with the given name to its `.plist` file.

### hProject.write_libs()

Write all libraries in project to their corresponding `.plist` files.

Attributes
----------

...