# [h] hTools2

"""hTools2, a UFO-based Python-powered font production toolkit."""

# objects

class hDialog(object):

    """An object collecting constants and default settings for dialogs."""

    #: Padding in dialogs.
    padding = 10

    #: Horizontal padding in dialogs (deprecated).
    padding_x = padding

    #: Vertical padding in dialogs (deprecated).
    padding_y = padding

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

    #: Height of a spinner element (value and buttons).
    spinner_height = (nudge_button * 2) + padding_y
