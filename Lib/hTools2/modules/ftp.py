# [h] hTools2.modules.ftp

"""Tools to connect to a FTP server, upload files etc."""

# This module uses the `ftplib` library to handle FTP connection and upload.
# http://docs.python.org/library/ftplib.html

import os
from ftplib import FTP

def connect_to_server(url, login, password, folder, verbose=False):
    """Connects to the FTP server using the given connection settings.

    Use the given ``url``, ``login`` and ``password`` information to make a connection. Move to the given ``folder`` (if it exists), and return a ``FTP`` object.

    To get to the lower level details about the FTP connection, use the optional parameter ``verbose=True``.

    """
    # create FTP connection
    ftp = FTP(url, login, password)
    if verbose == True:
        print "%s" % ftp.getwelcome()
    # move to folder
    ftp.cwd(folder)
    if verbose == True:
        ftp.retrlines('LIST')
        print
    return ftp

def upload_file(filePath, FTPconnection):
    """Upload the file at ``file_path`` to a FTP server, using the given ``ftp_connection``."""
    file = open(filePath, 'rb')
    fileName = os.path.split(filePath)[1]
    FTPconnection.storbinary('STOR ' + fileName, file)
    file.close()




