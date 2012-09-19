## hLibs

`hLibs` is a collection of files containing font-related data.

Each lib lives in a separate file in the project’s `libs` folder. Most libs are stored as `.plist` files. Glyph order and groups are stored in an `.enc` file, features are stored in `.fea` files.

### encoding.enc

Encoding files are simple text files with an `.enc` extension. They are the default way of specifying character sets in each project, and are used to order glyphs and paint groups in the fonts.

Below is small sample encoding file. The first line is the title, usually the name of the project (this line is skipped when parsing). Lines starting with `% ` followed by a series of hyphens indicate group names, and the following lines correspond to the glyphs contained in this group.

    %% [h] Publica
    % --------------- group_name
    glyph_name
    % --------------- latin_lc_basic
    a
    b
    c
    d
	…
    %

### groups.plist

The `groups` lib can be created dynamically from the encoding file, or can be edited separately like other libs.

<table>
	<tr>
		<th>group</th>
		<th>glyphs</th>
	</tr>
	<tr>
		<td>latin_lc_basic</td>
		<td>a b c d e f g h i j k l m n o p q r s t u v w x y z</td>
	</tr>
	<tr>
		<td>latin_uc_basic</td>
		<td>A B C D E F G H I J K L M N O P Q R S T U V W X Y Z</td>
	</tr>
	<tr>
		<td>punctuation_basic</td>
		<td>period comma colon semicolon</td>
	</tr>
</table>

### info.plist

The `info` lib contains font meta-data related to the author, foundry, license etc.

    from hTools2.objects import hProject
    p = hProject('Publica')
    print p.libs['info'].keys()

    >>> ['version-minor', 'notice', 'designer-url', 'vendor', 'copyright', 'license', 'trademark', 'license-url', 'foundry', 'note', 'designer', 'year', 'vendor-url', 'version-major']

<table>
	<tr>
		<th>lib entry</th>
		<th>example data</th>
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

### vmetrics.plist

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

<table>
	<tr>
		<th></th>
		<th>xheight</th>
		<th>ascender</th>
		<th>descender</th>
		<th>capheight</th>
		<th>upm</th>
	</tr>
	<tr>
		<th>default</th>
		<td>400</td>
		<td>700</td>
		<td>-200</td>
		<td>800</td>
		<td>1000</td>
	</tr>
	<tr>
		<th>Bold</th>
		<td>420</td>
		<td>720</td>
		<td>-180</td>
		<td>820</td>
		<td></td>
	</tr>
	<tr>
		<th>Black</th>
		<td>440</td>
		<td>740</td>
		<td>-160</td>
		<td></td>
		<td></td>
	</tr>
</table>

### accents.plist

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

<table>
	<tr>
		<th>glyph name</th>
		<th>base glyph</th>
		<th>components/anchors</th>
	</tr>
	<tr>
		<td>aacute</td>
		<td>a</td>
		<td>acute top</td>
	</tr>
	<tr>
		<td>ccedilla</td>
		<td>c</td>
		<td>cedilla bottom</td>
	</tr>
	<tr>
		<td>ntilde</td>
		<td>n</td>
		<td>tilde top</td>
	</tr>
</table>

### composed.plist

The `composed` lib contains recipes for building glyphs out of other glyphs – for example `ae`, `oslash`, `ij` etc.

<table>
	<tr>
		<th>glyph name</th>
		<th>components</th>
	</tr>
	<tr>
		<th>oe</th>
		<th>o oe</th>
	</tr>
	<tr>
		<td>ij</td>
		<td>i j</td>
	</tr>
	<tr>
		<td>fi</td>
		<td>f i</td>
	</tr>
	<tr>
		<td>ffi</td>
		<td>f f i</td>
	</tr>
</table>

### spacing.plist

The `spacing` lib contains a collection of left and right spacing groups.

    from hTools2.objects import hProject
    p = hProject('Guarana')
    print p.libs['spacing'].keys()

    >>> ['right', 'left']

    print p.libs['spacing']['left'].keys()

    >>> ['_left_a', '_left_f', '_left_H', '_left_n', '_left_O', '_left_o', '_left_V', '_left_u', '_left_v']

    print p.libs['spacing']['right']['_right_n']

    >>> ['n', 'h', 'm']

<table>
	<tr>
		<th>group name</th>
		<th>side*</th>
		<th>glyphs</th>
	</tr>
	<tr>
		<td>n</td>
		<td>left</td>
		<td>n m i</td>
	</tr>
	<tr>
		<td>o</td>
		<td>left</td>
		<td>o d q g</td>
	</tr>
	<tr>
		<td>H</td>
		<td>left</td>
		<td>B D E F H I K L M N P R</td>
	</tr>
	<tr>
		<td>O</td>
		<td>left</td>
		<td>C G Q</td>
	</tr>
</table>

### interpol.plist

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

<table>
	<tr>
		<th>instance name</th>
		<th>master 1</th>
		<th>master 2</th>
		<th>factor x</th>
		<th>factor y</th>
	</tr>
	<tr>
		<td>Medium</td>
		<td>Regular</td>
		<td>Bold</td>
		<td>.75</td>
		<td>.5</td>
	</tr>
	<tr>
		<td>Semibold</td>
		<td>Light</td>
		<td>Regular</td>
		<td>.65</td>
		<td>.75</td>
	</tr>
</table>

For more complex interpolation systems using more than two masters, use Superpolator.
