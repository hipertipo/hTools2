This module uses the [`ftplib`](http://docs.python.org/library/ftplib.html) library to handle FTP connection and upload.

### connect_to_server(url, login, password, folder, verbose=False)

Connects to the FTP server at `url` using the given `login` and `password`, moves to `folder` (if it exists), and returns a `FTP` object.

    from hTools2.modules.ftp import connect_to_server
    ftp_ = connect_to_server(url, login, password, folder)
    print ftp_

    >>> <ftplib.FTP instance at 0x1210625a8>

To get the lower level details about the FTP connection, use the optional parameter `verbose=True`.

    from hTools2.modules.ftp import connect_to_server
    ftp_ = connect_to_server(url, login, password, folder, verbose=True)

    >>> 220 ProFTPD 1.3.3a Server (vps001.server001.datenfalke.biz FTP Server) [::ffff:93.90.177.245]
    >>> drwxrwxr-x   2 hipertipo 33          36864 Jan 10 07:43 elementar
    >>> drwxrwxr-x   2 hipertipo 33           4096 Oct 29 01:51 emono
    >>> drwxrwxr-x   2 hipertipo 33           4096 Nov 15 07:46 publica
    >>> ...

### upload_file(file_path, ftp_connection)

Uploads the file at `file_path` to a FTP server, using the given `ftp_connection`.

    from hTools2.modules.ftp import connect_to_server, upload_file

    # FTP and file settings
    ftp_url = 'server1.myserver.com'
    ftp_folder = 'www/mysite/fonts'
    ftp_login = 'username'
    ftp_password = 'XXXXXX'
    my_file = '/fonts/MyFont.otf'

    # create FTP connection
    F = connect_to_server(ftp_url, ftp_login, ftp_password, ftp_folder)

    # upload file
    upload_file(myFile, F)

    # close FTP connection
    F.quit()
