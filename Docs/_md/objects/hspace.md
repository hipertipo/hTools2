## hSpace

The `hSpace` object represents a parametric variation space inside `hWorld`. Its purpose is to quickly address collections and subsets of fonts, using parameter ranges for weight value, width value, project name etc.

### Attributes

#### `hSpace.project`

The project to which the space applies.

#### `hSpace.parameters`

A dictionary containing parameter names and related value ranges.

    parameters = {
        'weight' : [1, 3, 5],
        'width' : [3, 4, 5]
    }

#### `hSpace.parameters_order`

A list with the order in which the parameters appear (for use in font names, lists etc).

#### `hSpace.parameters_separator`

The character used as separator in font file names.

#### `hSpace.fonts`

Returns a list with the parametric positions of all fonts in the current `hSpace`.


### Methods

#### `hSpace.build()`

Builds the variation space defined in `hSpace.params_dict`, using the order specified in `hSpace. params_order` to create the individual font names.

#### `hSpace.ufos()`

Returns a list of ufo paths for all existing fonts in the current `hSpace`.

    s = hSpace('QuanticaBitmap')
    s.parameters['size'] = [ '09', '10', '11', '12' ]
    s.parameters['weight'] = [ '1' ]
    s.parameters['resolution'] = [ '1' ]
    s.parameters_order = [ 'size', 'weight', 'resolution' ]
    s.build()

    print s.fonts

    >>> ['09-1-1', '10-1-1', '11-1-1', '12-1-1']

    print s.ufos()

    >>> ['/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_09-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_10-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_11-1-1.ufo', '/fonts/_QuanticaBitmap/_ufos/QuanticaBitmap_12-1-1.ufo']

#### `transfer_glyphs(glyphs_groups, axis, params)`

Batch transfer glyphs from one set of fonts to another.

    from hTools2.objects import hSpace
    project = 'QuanticaBitmap'
    gstring = '@currency'
    var = ( 'size', '17', '18', )
    ranges = {
        'resolution' : [ '1', ],
    }

    s = hSpace(project)
    s.transfer_glyphs(gstring, var, ranges)
