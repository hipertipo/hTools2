## fontutils

#### `get_spacing_groups(font)`

Returns a dictionary containing the `left` and `right` spacing groups in the font.

    from hTools2.modules.fontutils import get_spacing_groups

    f = CurrentFont()
    spacing_groups = get_spacing_groups(f)
    print spacing_groups.keys()

    >>> ['right', 'left']

    print spacing_groups['left'].keys()

    >>> ['_left_a', '_left_f', '_left_H', '_left_n', ... ]

    print spacing_groups['left']['_left_a']

    >>> ['a', 'schwa', 'ae']

#### `get_glyphs(font)`

Returns a list with the names of glyphs currently selected or active in the `font`.

The behavior of this function is slightly different than RoboFab’s `f.selection`, because it also includes the contents of `CurrentGlyph()`.

For the example below, imagine that the glyphs `b c d` are selected in the font window, and `a` is in an open glyph window.

    from hTools2.modules.fontutils import get_glyphs
    f = CurrentFont()
    print get_glyphs(f)

    >>> ['a', 'b', 'c', 'd']

    print f.selection

    >>> ['b', 'c', 'd']

#### `print_selected_glyphs(f, mode=1)`

Prints the selected glyphs to the output window.

Two different modes are supported: `mode=0` prints the glyph names as a list of Python strings, while `mode=1` prints the glyph names as a plain list (with linebreaks).

    from hTools2.modules.fontutils import print_selected_glyphs
    f = CurrentFont()
    print_selected_glyphs(f, mode=0)

    >>> "b", "c", "d"

    print_selected_glyphs(f, mode=1)

    >>> b
    >>> c
    >>> d

#### `delete_groups(font)`

Deletes all groups in the font.

    from hTools2.modules.fontutils import delete_groups
    f = CurrentFont()
    print f.groups
    print len(f.groups)

    >>> <Group object>
    >>> 41

    delete_groups(f)
    print len(f.groups)

    >>> 0

#### `print_groups(font, mode=0)`

Prints all groups and glyphs in the font.

If `mode=0`, groups and glyphs are printed as nicely formatted text:

    from hTools2.modules.fontutils import print_groups
    f = CurrentFont()
    print_groups(f, mode=0)

    >>> printing groups in font <Font Publica 55>...
    >>>
    >>> groups order:
    >>>
    >>>     invisible
    >>>     latin_lc_basic
    >>>     latin_lc_alternates
    >>>     numbers_proportional_oldstyle
    >>>     latin_uc_basic
    >>>     ...
    >>>
    >>> groups:
    >>>
    >>> slashes:
    >>> slash backslash bar brokenbar
    >>>
    >>> numbers_proportional_lining:
    >>> zero.pnum_lnum_zero zero.pnum_lnum one.pnum_lnum ...
    >>>
    >>> ...
    >>>
    >>> ...done.

If `mode=1`, groups and glyphs are printed in OpenType classes format:

    from hTools2.modules.fontutils import *
    f = CurrentFont()
    print_groups(f, mode=1)

    >>> printing groups in font <Font Publica 55>...
    >>>
    >>> @accents_lc = [ acute acute.i cedilla circumflex dieresis grave tilde ];
    >>> @currency = [ cent dollar Euro sterling florin currency yen ];
    >>> @dashes = [ hyphen endash emdash underscore ];
    >>> @invisible = [ .notdef ];
    >>> ...
    >>>
    >>> ...done.

And if `mode=2`, groups and glyphs are printed as Python lists:

    from hTools2.modules.fontutils import *
    f = CurrentFont()
    print_groups(f, mode=2)

    >>> printing groups in font <Font Publica 55>...
    >>>
    >>> ['invisible', 'latin_lc_basic', 'latin_lc_alternates', ... ]
    >>>
    >>> slashes = ['slash', 'backslash', 'bar', 'brokenbar']
    >>> numbers_proportional_lining = ['zero.pnum_lnum_zero', 'zero.pnum_lnum', 'one.pnum_lnum', ... ]
    >>> ...
    >>>
    >>> ...done.

#### `get_full_name(font)`

Returns the full name of the font (family name + style name).

    from hTools2.modules.fontutils import get_full_name
    f = CurrentFont()
    print get_full_name(f)

    >>> Publica 55

#### `full_name(family, style)`

Returns a ‘full name’ from `family` and `style` names, separated by a `space` character. If the `style` is Regular, only the `family` is used.

    from hTools2.modules.fontutils import full_name
    f = CurrentFont()
    print full_name('Publica', 'Regular')

    >>> Publica

    print full_name('Publica', 'Black')

    >>> Publica Black

    print full_name('Publica', '55')

    >>> Publica 55

#### `font_name(family, style)`

Same as `full_name()`, but `family` and `style` names are separated by a `hyphen` instead of `space`.

    from hTools2.modules.fontutils import full_name
    f = CurrentFont()
    print font_name('Publica', '55')

    >>> Publica-55

#### `get_names_from_path(font_path)`

Returns `family` and `style` names from the given `font_path`. Only works if .ufo file names follow [hTools conventions](http://hipertipo.com/content/htools2/about/conventions/).

    from hTools2.modules.fontutils import get_names_from_path
    f = CurrentFont()
    print get_names_from_path(f.path)

    >>> (u'Publica', u'55')

#### `decompose(font)`

Decomposes any composed glyph in the `font`.

    # first, check glyphs for components
    f = CurrentFont()
    for g in f:
        if len(g.components) > 1:
            print g, g.components

    >>> <Glyph ij (foreground)> [<Component for i>, <Component for j>]
    >>> <Glyph aacute (foreground)> [<Component for a>, <Component for acute>]
    >>> <Glyph uni01C6 (foreground)> [<Component for z>, <Component for d>]
    >>> ...

    from hTools2.modules.fontutils import decompose
    f = CurrentFont()
    decompose(f)

    # check for components again, just to make sure
    composed = []
    for g in f:
        if len(g.components) > 1:
            composed.append(g.name)
    print composed

    >>> []

#### `auto_contour_order(font)`

Automatically sets contour order for all glyphs in the `font`.

    from hTools2.modules.fontutils import auto_contour_order
    f = CurrentFont()
    auto_contour_order(f)

#### `auto_contour_direction(font)`

Automatically sets contour directions for all glyphs in the `font`.

    from hTools2.modules.fontutils import auto_contour_direction
    f = CurrentFont()
    auto_contour_direction(f)

#### `auto_order_direction(font)`

Automatically sets contour order and direction for all glyphs in the `font`, in one go.

    from hTools2.modules.fontutils import auto_order_direction
    f = CurrentFont()
    auto_order_direction(f)

#### `add_extremes(font)`

Add extreme points to all glyphs in the `font`, if they are missing.

    from hTools2.modules.fontutils import add_extremes
    f = CurrentFont()
    add_extremes(f)

#### `align_to_grid(font, (sizeX, sizeY))`

Aligns all points of all glyphs in the `font` to a grid with size `(sizeX,sizeY)`.

    from hTools2.modules.fontutils import align_to_grid
    f = CurrentFont()
    align_to_grid(f, (100, 100))
