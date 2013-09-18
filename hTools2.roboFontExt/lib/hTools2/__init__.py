# [h] hTools2

"""hTools2, a UFO-based Python-powered font production toolkit."""

#: The root folder for all project folders. By default, ``/_fonts``.
ROOT = '/_fonts'

#: Debug mode. Set to ``True`` during development to always reload modules.
DEBUG = True

#:The current version number of ``hTools2``.
VERSION = 1.6

class hConstants(object):

    """An object collecting constants and default settings for dialogs."""

    #: Horizontal padding in dialogs.
    padding_x = 10
    #: Vertical padding in dialogs.
    padding_y = 10
    #: Height of text elements in dialogs.
    text_height = 20
    #: Size of individual button in nudge button set.
    nudge_button = 18
    #: Size of square button in cross nudge button set.
    square_button = 35
    #: Height of standard button in dialogs.
    button_height = 25
    #: Can nummerical text input be edited directly with the keyboard? A boolean. Set to ``True`` as default.
    read_only = True
    #: The size style of text and standard dialog elements. Possible options are ``small``, ``regular``, ``mini``.
    size_style = 'small'
    #: The body width of vertical dialogs.
    body = 103
    #: The height of rhe progress bar.
    progress_bar = 18

