# hWorld doctests

# import

from hTools2.objects import hWorld

# object

class hWorld_test(object):

    """An interactive tests session for the :py:class:`hWorld` object.

    >>> from hTools2.objects import hWorld
    >>> w = hWorld()
    >>> print w.settings
    <hSettings>

    >>> print w.context
    NoneLab

    >>> print w.projects()
    ['Calligraphica', 'Elementar', 'Geometrica', 'Gothica', 'Grow', 'Guarana', 'Imperial', 'Jornalistica', 'Magnetica', 'Mechanica', 'Modular', 'Publica', 'Quantica', 'QuanticaBitmap', 'Segments', 'Synthetica']

    """

# test

if __name__ == "__main__":
    import doctest
    doctest.testmod()
