# [h] edit hWorld settings dialog

from vanilla import *
from vanilla.dialogs import getFolder

import hTools2.objects
import hTools2.modules.ftp

reload(hTools2.objects)
reload(hTools2.modules.ftp)

from hTools2.objects import hSettings, hWorld
from hTools2.modules.ftp import connect_to_server, upload_file


class hSettingsDialog(object):

    _title = "hSettings"
    _padding = 10
    _column_1 = 80
    _column_2 = 280
    _button_1_width = 50
    _box_height = 20
    _box_width_small = 120
    _button_1_height = 20
    _button_2_height = 25
    _width = _column_1 + _column_2 + (_padding * 3) + _button_1_width
    _height = (_box_height * 3) + (_padding * 5) + _button_1_height + 5

    def __init__(self):
        self.world = hWorld()
        self.w = FloatingWindow(
                    (self._width,
                    self._height),
                    self._title)
        # FTP URL
        x = self._padding
        y = self._padding
        self.w.ftp_url_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "FTP server",
                    sizeStyle="small")
        x += self._column_1
        self.w.ftp_url_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self.world.settings.hDict['ftp']['url'],
                    sizeStyle="small")
        # FTP login
        x = self._padding
        y += self._box_height + self._padding
        self.w.ftp_login_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "FTP login",
                    sizeStyle="small")
        x += self._column_1
        self.w.ftp_login_value = EditText(
                    (x, y,
                    self._box_width_small,
                    self._box_height),
                    self.world.settings.hDict['ftp']['login'],
                    sizeStyle="small")
        # password
        x = (self._width / 2) + 10
        self.w.ftp_password_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "password",
                    sizeStyle="small")
        x += self._column_1
        self.w.ftp_password_value = EditText(
                    (x, y,
                    self._box_width_small,
                    self._box_height),
                    self.world.settings.hDict['ftp']['password'],
                    sizeStyle="small")
        # FTP folder
        x = self._padding
        y += self._box_height + self._padding
        self.w.ftp_folder_label = TextBox(
                    (x, y,
                    self._column_1,
                    self._box_height),
                    "FTP folder",
                    sizeStyle="small")
        x += self._column_1
        self.w.ftp_folder_value = EditText(
                    (x, y,
                    -self._padding,
                    self._box_height),
                    self.world.settings.hDict['ftp']['folder'],
                    sizeStyle="small")
        y += self._box_height + self._padding
        # save button
        x = self._padding
        _button_width = (self._width - (self._padding * 3)) / 2
        # test ftp
        self.w.button_test_ftp = SquareButton(
                    (x, y,
                    _button_width,
                    self._button_2_height),
                    "test FTP connection",
                    callback=self.test_ftp_callback,
                    sizeStyle="small")
        x += _button_width + self._padding
        self.w.button_save = SquareButton(
                    (x, y,
                    _button_width,
                    self._button_2_height),
                    "save",
                    callback=self.save_callback,
                    sizeStyle="small")
        # open
        self.w.open()

    # callbacks

    def test_ftp_callback(self, sender):
        _url = self.w.ftp_url_value.get()
        _login = self.w.ftp_login_value.get()
        _password = self.w.ftp_password_value.get()
        _folder = self.w.ftp_folder_value.get()
        F = connectToServer(_url, _login, _password, _folder, verbose=True)
        F.quit()

    def _root_get_folder_callback(self, sender):
        _folder = getFolder()
        self.w.root_folder_value.set(_folder[0])

    def _test_get_folder_callback(self, sender):
        _folder = getFolder()
        self.w.test_folder_value.set(_folder[0])

    def save_callback(self, sender):
        print "saving hSettings...",
        self.world.settings.hDict['ftp'] = {}
        self.world.settings.hDict['ftp']['url'] = self.w.ftp_url_value.get()
        self.world.settings.hDict['ftp']['login'] = self.w.ftp_login_value.get()
        self.world.settings.hDict['ftp']['password'] = self.w.ftp_password_value.get()
        self.world.settings.hDict['ftp']['folder'] = self.w.ftp_folder_value.get()
        self.world.settings.write()
        print 'done.\n'
        # self.world.settings.print_()

# run

hSettingsDialog()

