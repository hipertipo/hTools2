# [h] batch genenerate webfonts

import os

from mojo.roboFont import RFont

from hTools2.objects import hSettings, hProject, hFont
from hTools2.modules.fileutils import walk, deleteFiles
from hTools2.modules.ftp import connectToServer, uploadFile
from hTools2.plugins.KLTF_WOFF import compressFont

projects = [ 'Publica' ]

_clear = False
_generate = False
_upload = True

s = hSettings()
url = s.hDict['ftp']['url']
login = s.hDict['ftp']['login']
password = s.hDict['ftp']['password']
folder = s.hDict['ftp']['folder']

for pName in projects:
    p = hProject(pName)

    # clear old woff files
    if _clear:
        woffs = p.woffs()
        if len(woffs) > 0:
            print 'deleting old woff fonts...\n'
            deleteFiles(woffs)          

    # generate woffs
    if _generate:
        print 'generating instances in project %s...' % pName
        for otf_path in p.otfs():
            _folder = p.paths['woffs']
            _file = os.path.split(otf_path)[1].split('.')[0] + '.woff'
            woff_path = os.path.join(_folder, _file)
            print "\tgenerating %s..." % woff_path
            compressFont(otf_path, woff_path)
        print '...done.\n'

# upload to ftp
if _upload:
    for pName in projects:
        p = hProject(pName)
        fonts_folder = os.path.join(s.hDict['ftp']['folder'], p.name.lower())
        F = connectToServer(url, login, password, fonts_folder, verbose=False)
        print "uploading woffs to server..."
        for woff_path in p.woffs():
            print "\tuploading %s..." % woff_path
            uploadFile(woff_path, F)
        F.quit()
        print "...done.\n"

