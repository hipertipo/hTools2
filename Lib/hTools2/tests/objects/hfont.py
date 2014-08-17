# hFont doctests

# import

from hTools2.objects import hFont

# object

class hFont_test(object):

    """An interactive tests session for the :py:class:`hFont` object.

    >>> from robofab.world import RFont
    >>> from hTools2.objects import hFont
    >>> ufo = RFont('/_fonts/_Publica/_ufos/Publica_55.ufo')
    >>> font = hFont(ufo)
    >>> print font
    <hFont Publica 55>

    >>> print font.project
    <hProject Publica>
    >>> print font.project.name
    Publica

    >>> print font.project.libs.keys()
    ['info', 'composed', 'accents', 'spacing', 'project', 'groups', 'interpol', 'vmetrics']

    >>> print font.ufo
    <RFont font for Publica 55>

    >>> print font.file_name
    Publica_55

    >>> print font.style_name
    55

    >>> print font.otf_path()
    /_fonts/_Publica/_otfs/Publica_55.otf

    >>> print font.woff_path()
    /_fonts/_Publica/_woffs/Publica_55.woff

"""

# test

if __name__ == "__main__":
    import doctest
    doctest.testmod()
