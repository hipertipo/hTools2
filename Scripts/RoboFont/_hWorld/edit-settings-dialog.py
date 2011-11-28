# [h] edit hWorld settings dialog

from vanilla import *

from hTools2.objects import hSettings, hWorld

class setSettingsDialog(object):

    _title = "edit hWorld settings"
    _width = 480
    _height = 375

    def __init__(self):
        self.world = hWorld()
        self.world.settings.print_info()
        self.w = FloatingWindow((self._width, self._height), self._title) # closable=False
        # root folder
        self.w.root_label = TextBox((10, 10, -10, 70), "root folder for world")
        self.w.root_get_folder_button = Button((-100, 10, -10, 20), "get folder...", sizeStyle="small")
        self.w.root_folder_value = EditText((10, 40, -10, 22), '', sizeStyle="mini")
        # test folder
        self.w.test_label = TextBox((10, 75, -10, 70), "test folder for .otf fonts")
        self.w.test_get_folder_button = Button((-100, 75, -10, 20), "get folder...", sizeStyle="small")
        self.w.test_folder_value = EditText((10, 105, -10, 22), self.world.settings.hDict['test'], sizeStyle="mini")
        # url
        self.w.ftp_url_label = TextBox((10, 140, -10, 70), "URL to FTP server")
        self.w.ftp_url_value = EditText((10, 170, -10, 22), self.world.settings.hDict['ftp']['url'], sizeStyle="mini")
        # login
        self.w.ftp_login_label = TextBox((10, 205, -10, 70), "login")
        self.w.ftp_login_value = EditText((10, 235, self._width/2-15, 22), self.world.settings.hDict['ftp']['login'], sizeStyle="mini")
        # password
        self.w.ftp_password_label = TextBox((self._width/2, 205, self._width/2-15, 70), "password")
        self.w.ftp_password_value = EditText((self._width/2+5, 235, self._width/2-15, 22), self.world.settings.hDict['ftp']['password'], sizeStyle="mini")
        # ftp folder
        self.w.ftp_folder_label = TextBox((10, 270, -10, 70), "root FTP folder for fonts")
        self.w.ftp_folder_value = EditText((10, 300, -10, 22), self.world.settings.hDict['ftp']['folder'], sizeStyle="mini")
        # apply / close
        self.w.button_close = Button((10, -30, self._width/2-10, 15), "close", callback=self.close_callback)
        self.w.button_save = Button((self._width/2+10, -30, -10, 15), "save settings", callback=self.save_callback)
        #
        self.w.open()

    def save_callback(self, sender):
        self.world.settings.hDict['root'] = self.w.root_folder_value.get()
        self.world.settings.hDict['test'] = self.w.test_folder_value.get()
        self.world.settings.hDict['ftp']['url'] = self.w.ftp_url_value.get()
        self.world.settings.hDict['ftp']['login'] = self.w.ftp_login_value.get()
        self.world.settings.hDict['ftp']['password'] = self.w.ftp_password_value.get()
        self.world.settings.hDict['ftp']['folder'] = self.w.ftp_folder_value.get()
        self.world.settings.write()
        print 'saved settings.\n'
        self.world.settings.print_info()

    def close_callback(self, sender):
        self.w.close()

setSettingsDialog()
