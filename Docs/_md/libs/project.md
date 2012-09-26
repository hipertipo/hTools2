## project

The `project` lib contains custom data about the project.

### `libs['project']['parameters']`

A dictionary containing names of variation axes as keys, and and a list with the available coordenates for each axis as values.

    parameters = {
        'style' : [ 'Roman', 'Italic' ],
        'weight' : [ 'Light', 'Book', 'Medium', 'Regular', 'Bold', 'Black' ],
        'width' : [ 'Condensed', 'Normal' ],
    }

    p = hProject('Publica')
    p.libs['project']['parameters'] = parameters
    p.write_lib('project')

### `libs['project']['parameters_order']`

A list with the order of the parameters. This order is used in the naming and sorting of font files.

    parameters_order = [ 'style', 'weight', 'width' ]

### `libs['project']['parameters_separator']`

A boolean expressing the project’s setting for separator in file names. If `separator=True`, the individual parameters in filenames are separated with hyphens, otherwise parameters are combined without separation.

### `libs['project']['grid']`

The basic gridsize used for all fonts in the project.
