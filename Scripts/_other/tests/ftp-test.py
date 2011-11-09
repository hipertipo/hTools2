# [h] : connect to FTP server

from hTools2.objects import hSettings
from hTools2.modules.ftp import connectToServer

s = hSettings()

url = s.hDict['ftp']['url']
login = s.hDict['ftp']['login']
password = s.hDict['ftp']['password']
folder = s.hDict['ftp']['folder']

ftp_connection = connectToServer(url, login, password, folder, verbose=True)