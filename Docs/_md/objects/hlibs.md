`hLibs` is not an object in the same way as the other objects in hTools, but a collection of several files containing font-related data.

Each lib lives in a separate file in the project’s `libs` folder. Most libs are stored as `.plist` files; glyph order and groups are stored in an old-school `.enc` file.

## encoding.enc

Encoding files are simple text files with an `.enc` extension. They are the default way of specifying character sets in each project, and are used to order glyphs and paint groups in the fonts.

Below is small sample encoding file. The first line is the title, usually the name of the project (this line is skipped when parsing). Lines starting with `% ` followed by a series of hyphens indicate group names, and the following lines correspond to the glyphs contained in this group.

    %% [h] Publica
    % --------------- group_name
    gname
    % --------------- latin_lc_basic
    a
    b
    c
    d
    %

## info.plist

The `info` lib contains font meta-data related to the author, foundry, license etc.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.libs['info'].keys()

    >>> ['version-minor', 'notice', 'designer-url', 'vendor', 'copyright', 'license', 'trademark', 'license-url', 'foundry', 'note', 'designer', 'year', 'vendor-url', 'version-major']

<table>
	<tr>
		<th>lib entry</th>
		<td>example data</td>
	</tr>
	<tr>
		<th>version-minor</th>
		<td>...</td>
	</tr>
	<tr>
		<th>notice</th>
		<td>...</td>
	</tr>
	<tr>
		<th>designer-url</th>
		<td>...</td>
	</tr>
	<tr>
		<th>vendor</th>
		<td>...</td>
	</tr>
	<tr>
		<th>copyright</th>
		<td>...</td>
	</tr>
	<tr>
		<th>license</th>
		<td>...</td>
	</tr>
	<tr>
		<th>trademark</th>
		<td>...</td>
	</tr>
	<tr>
		<th>license-url</th>
		<td>...</td>
	</tr>
	<tr>
		<th>foundry</th>
		<td>...</td>
	</tr>
	<tr>
		<th>note</th>
		<td>...</td>
	</tr>
	<tr>
		<th>designer</th>
		<td>...</td>
	</tr>
	<tr>
		<th>year</th>
		<td>...</td>
	</tr>
	<tr>
		<th>vendor-url</th>
		<td>...</td>
	</tr>
	<tr>
		<th>version-major</th>
		<td>...</td>
	</tr>
</table>

## vmetrics.plist

The `vmetrics` lib contains basic vertical metrics information for all fonts in the project.

    vmetrics_lib = {
        'default' : {
            'descender' : 300,
            'sc-height' : 700,
            'capheight' : 900,
            'ascender' : 800,
            'units-per-em' : 1000,
            'xheight' : 600
        },
        '15' : {...},
        '55' : {...},
        '95' : {...}
    }

## accents.plist

The `accents` lib contains a collection of glyph building recipes. It is structured as simple dictionary, with the target glyph names as keys, and a list of glyph parts (component and anchor) as value:

    accents_lib = {
        'aacute' : [ 'a', [ ('acute', 'top') ] ],
        'aringacute' : [ 'a', [ ('ring', 'top'), ('acute', 'top') ] ],
        'ccedilla' : ['c', [ ('cedilla', 'bottom') ] ],
         ...
    }

Like all other libs, the `accents` lib is generally accessed through its parent project:

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.libs['accents'].keys()

    >>> [ 'aacute', 'aringacute', 'ccedilla', ... ]

    print p.libs['accents']['aacute']

    >>> ['a', [ ['acute', 'top'] ] ]

## composed.plist

The `composed` lib contains recipes for building glyphs out of other glyphs – for example `ae`, `oslash`, `ij` etc.

## spacing.plist

The `spacing` lib contains a collection of left and right spacing groups.

    from hTools2.objects import hProject
    p = hProject('Guarana')
    print p.libs['spacing'].keys()

    >>> ['right', 'left']

    print p.libs['spacing']['left'].keys()

    >>> ['_left_a', '_left_f', '_left_H', '_left_n', '_left_O', '_left_o', '_left_V', '_left_u', '_left_v']

    print p.libs['spacing']['right']['_right_n']

    >>> ['n', 'h', 'm']

## interpol.plist

The `interpol` lib contains a list with instance names and their corresponding interpolation values: `master1`, `master2` and `(factor_x, factor_y)`.

    interpol_lib = {
        '35' : [ '15', '55', (0.5, 0.5) ],
        '75' : [ '55', '95', (0.5, 0.5) ],
        ...
    }

Like all other libs, the `interpol` lib can be accessed via the `hProject` object:

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.libs['interpol'].keys()

    >>> ['25', '45', '35', '75', '65', '85']

    print p.libs['interpol']['75']

    >>> ['55', '95', [0.5, 0.5]]
