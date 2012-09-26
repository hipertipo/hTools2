## spacing

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
