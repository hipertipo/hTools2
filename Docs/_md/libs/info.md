## info

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
