## accents

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
