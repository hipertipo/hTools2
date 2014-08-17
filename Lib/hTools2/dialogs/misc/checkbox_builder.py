# [h] checkbox builder (hTools1 classic)

### thanks to Tal Leming for valuable tips many years ago in the RoboFab list

# imports

from dialogKit import ModalDialog, CheckBox, HorizontalLine

# objects

class checkBoxBuilder(object):

    """An object to create a modal dialog for selecting items in a list.

    .. image:: imgs/misc/checkbox-builder.png

    .. code-block:: python

        from hTools2.dialogs.misc import checkBoxBuilder

        L = [
            ('apples', True),
            ('bananas', True),
            ('tomatos', False),
        ]

        B = checkBoxBuilder(L)

        print B.selected

        >>> ['apples', 'bananas']

    """

    # attributes

    _box_height = 23
    _padding = 10

    _select_all = False
    _checkboxes = {}

    cancelled = False
    selected = []

    # methods

    def __init__(self, items_list, title="select options", width=320, sort=False):
        self._title  = title
        self._width  = width
        self._height = (self._padding * 2) + ( (len(items_list) + 2) * self._box_height ) + 50
        # sort items
        if sort:
            tmp = list(items_list)
            tmp.sort()
            items_list = tuple(tmp)
        self._items_list = items_list
        # init window
        self.w = ModalDialog(
                    (self._width,
                    self._height),
                    self._title,
                    okCallback=self.ok_callback,
                    cancelCallback=self.cancel_callback)
        x = self._padding
        y = self._padding
        # select all / none
        self.w._select_all_checkbox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    'select/deselect all',
                    value=self._select_all,
                    callback=self._select_all_callback)
        y += (self._box_height)
        # division line
        self.w.line = HorizontalLine(
                    (x, y,
                    -self._padding,
                    self._box_height))
        # create checkboxes from list
        for item in self._items_list:
            self._add_checkbox(item)
        # open window
        self.w.open()

    def _add_checkbox(self, (title, value)):
        number = len(self._checkboxes) + 2
        attribute_name = "checkBox%d" % number
        x = self._padding
        y = self._padding + (number * self._box_height)
        checkBox = CheckBox(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    title,
                    value=value,
                    callback=self.checkbox_callback)
        setattr(self.w, attribute_name, checkBox)
        self._checkboxes[checkBox] = (title, value)

    def _select_all_callback(self, sender):
        self._select_all = sender.get()
        # update internal values
        for _checkbox in self._checkboxes.keys():
            title, value = self._checkboxes[_checkbox]
            self._checkboxes[_checkbox] = (title, self._select_all)
        # update dialog
        for _checkbox in dir(self.w):
            if _checkbox[:8] == 'checkBox':
                exec "self.w.%s.set(%s)" % (_checkbox, self._select_all)

    def checkbox_callback(self, sender):
        title, value = self._checkboxes[sender]
        value = sender.get()
        self._checkboxes[sender] = (title, value)

    def ok_callback(self, sender):
        _checkboxes = self._checkboxes.keys()
        _checkboxes.sort()
        for _checkbox in _checkboxes:
            title, value = self._checkboxes[_checkbox]
            if value == True:
                self.selected.append(title)

    def cancel_callback(self, sender):
        self.cancelled = True
