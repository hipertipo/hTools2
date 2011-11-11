# [h] hTools2.modules.ftp

import os

from ftplib import FTP

def connectToServer(url, login, password, folder, verbose=False):
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

def uploadFile(filePath, FTPconnection):
	file = open(filePath, 'rb')
	fileName = os.path.split(filePath)[1]
	FTPconnection.storbinary('STOR ' + fileName, file)
	file.close()
