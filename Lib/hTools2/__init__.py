# [h] hTools2

'''hTools2, a UFO-based Python-powered font production toolkit.'''

# constants

#: The root folder for all project folders. By default, ``/_fonts``.
ROOT = '/_fonts'

#: Debug mode. Set to ``True`` during development to always reload modules.
DEBUG = True

#: The current version number of ``hTools2``.
VERSION = 1.6

# objects

class hDialog(object):

    '''An object collecting constants and default settings for dialogs.'''

    #: Horizontal padding in dialogs.
    padding_x = 10

    #: Vertical padding in dialogs.
    padding_y = 10

    #: Height of text elements in dialogs.
    text_height = 20

    #: Height of text elements in dialogs.
    text_input = 18

    #: Height of standard button in dialogs.
    button_height = 25

    #: Size of individual button in nudge button set.
    nudge_button = 18

    #: Size of square button in cross nudge button set.
    square_button = 35

    #: Can nummerical text input be edited directly with the keyboard? A boolean. Set to ``True`` as default.
    read_only = False

    #: The size style of text and standard dialog elements. Possible options are ``small``, ``regular``, ``mini``.
    size_style = 'small'

    #: The default width of vertical dialogs (palettes).
    width = 123

    #: The height of the progress bar.
    progress_bar = 18

    #: Print (or not) messages to the console when running scripts.
    verbose = True
