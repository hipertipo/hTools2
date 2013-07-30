# [h] hTools2

"""hTools2, a UFO-based Python-powered font production toolkit.

.. py:attribute:: ROOT

The root folder for all project folders. By default, ``/_fonts``.

.. py:attribute:: DEBUG

Debug mode. Set to ``True`` during development to always reload modules.

.. py:attribute:: VERSION

The current version number of ``hTools2``.

"""

ROOT = '/_fonts'
DEBUG = True
VERSION = 1.6

class hConstants(object):

    """An object collecting constants and default settings for dialogs.

    .. py:attribute:: padding_x

    Horizontal padding in dialogs.

    .. py:attribute:: padding_y

    Vertical padding in dialogs.

    .. py:attribute:: text_height

    Height of text elements in dialogs.

    .. py:attribute:: nudge_button

    Size of individual button in nudge button set.

    .. py:attribute:: square_button

    Size of square button in cross nudge button set.

    .. py:attribute:: button_height

    Height of standard button in dialogs.

    .. py:attribute:: read_only

    Can nummerical text input be edited directly with the keyboard? A boolean. Set to ``False`` as default.

    .. py:attribute:: size_style

    The size style of text and standard dialog elements. Possible options are ``small``, ``regular``, ``mini``.

    """

    padding_x = 10
    padding_y = 10
    text_height = 20
    nudge_button = 18
    square_button = 35
    button_height = 30
    read_only = True
    size_style = 'small'
