The `hFont` object represents a ufo font source, wrapped in a few useful functions. It must be initialized with a `RFont` object as argument:

    from robofab.world import RFont
    from hTools2.objects import hFont
    ufo = RFont('/fonts/_Publica/_ufos/Publica_55.ufo', showUI=False) 
    font = hFont(ufo)
    print font

    >>> <hTools2.objects.hFont instance at 0x1228591b8>

It’s also possible to initiate `hFont` using `CurrentFont()`:
   
    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    print font

    >>> <hTools2.objects.hFont instance at 0x129af09e0>


## Attributes

### hFont.project

The parent `hProject` object to which the `hFont` belongs, with all its attributes and methods.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    print font.project
    print font.project.name

    >>> <hTools2.objects.hProject instance at 0x125c03ea8>
    >>> Publica

    print font.project.libs.keys()

    >>> ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

### hFont.ufo

The .ufo file containing the actual font.

See the [UFO documentation](http://unifiedfontobject.org/) for more information about the UFO format, and the [RoboFab documentation](http://robofab.com/objects/font.html) for information about the available methods and attributes for `RFont`.

### hFont.file_name

The name of the ufo file, without the extension.

### hFont.style_name

The `styleName` of the font, parsed from the name of the ufo file on initialization. See the method `init_from_filename()` for details.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    print font.ufo
    print font.file_name
    print font.style_name

    >>> <Font Publica 55>
    >>> Publica_55
    >>> 55


## Methods

### hFont.init_from_filename()

Initiates the `hFont` object from the ufo file in `hFont.ufo`.

The method parses the ufo file name, and uses the resulting names to initiate a parent `hProject` object. This object is then stored at `hFont.project`, and the parsed name parts become the attributes `file_name` and `style_name`.

This system only works if the .ufo files are named according to [hTools conventions](http://hipertipo.com/content/htools2/about/conventions/).

### hFont.auto_unicodes()

Automatically sets unicodes for all glyphs in `hFont.ufo`.

### hFont.order_glyphs()

Automatically sets the order of the glyphs in the font, based on the list in `hFont.project.libs['groups']['order']`.

### hFont.paint_groups()

Paints and orders the glyphs in the font according to their groups, using glyph groups and order from the project’s group libs.

### hFont.print_info()

Prints different kinds of font information.

### hFont.import_groups_from_encoding()

Imports glyph names and order from the project’s encoding file, and stores it in a temporary `groups` lib.

### hFont.full_name()

The full name of the font, made of the project’s name in `hFont.project.name` and the style name in `hFont.style_name`.

### hFont.otf_path()

Returns the default path for .otf font generation, in the projects `_otfs/` folder.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    print font.otf_path()

    >>> /fonts/_Publica/_otfs/Publica_55.otf

### hFont.woff_path()

Returns the default path for .woff font generation, in the projects `_woffs/` folder.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    print font.woff_path()

    >>> /fonts/_Publica/_woffs/Publica_55.woff

### hFont.generate_otf()

Generates a .otf font file using the default settings.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    font.generate_otf()

### hFont.generate_woff()

Generates a woff font file from the available otf font.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    font.generate_woff()

*Note: This function only works if Karsten Lücke’s `KLTF_WOFF` plugin is installed.*

### hFont.upload_woff()

Uploads the font’s woff file (if available) to the project’s folder in the FTP server.

    from hTools2.objects import hFont
    font = hFont(CurrentFont())
    font.upload_woff()
