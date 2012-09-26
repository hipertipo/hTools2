## interpol

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
