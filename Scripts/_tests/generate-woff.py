# [h] batch genenerate instances

from hTools2.objects import hProject
from hTools2.modules.fileutils import walk, deletFiles
from hTools2.modules.ftp import *
from hTools2.plugins.KLTF_WOFF import compressFont

projects = [ 'Quantica', 'Publica', ]

for pName in projects:
    p = hProject(pName)
    print 'generating instances in project %s...' % pName
    # clear test fonts
    print '\tdeleting fonts in %s...' % p.paths['test']
    otfs_test = walk(p.paths['test'], 'otf')
    for i in p.instances():
        ufo = RFont(i, showUI=False)
        f = hFont(ufo)
        if round:
            f.ufo.round()
        otf_path = f.otf_path(test=True)
        print '\tgenerating otf as %s' % otf_path
        ufo.removeOverlap()
        ufo.generate(otf_path, 'otf', glyphOrder=[])
        ufo.close()
        # upload to ftp
        if ftp == True:
            print "\tuploading font to server...\n"
            fonts_folder = os.path.join(s.hDict['ftp']['folder'], p.name.lower())
            F = connectToServer(url, login, password, fonts_folder, verbose=False)
            uploadFile(otf_path, F)
            F.quit()
    print '...done.\n'

