# [h] test objects

import hTools2.objects
reload(hTools2.objects)

#-------
# tests
#-------

def test_hSettings():
    from hTools2.objects import hSettings
    s = hSettings()
    s.print_info()
    #s.edit_dialog()
    #s.hDict['fonts_test'] = '/myFolder/fonts/'
    #s.write()
    #s.output()

def test_hWorld():
    from hTools2.objects import hWorld
    w = hWorld()
    w.settings.print_info()
    for p in w.projects():
        print p
    
def test_hProject():
    from hTools2.objects import hProject    
    p = hProject('Guarana')
    p.print_paths()
    print '\t%s masters, %s instances' % (len(p.masters()), len(p.instances()))
                                        
def test_hFont():
    from hTools2.objects import hFont, hProject
    f = hFont(RFont(showUI=False))
    print f.ufo
    f.project = hProject('Publica')
    print f.project
    # print f.parameters
    # print f.parameters['weight']
    # print f.parameters['width']
    # print f.otf_path()

def test_hGlyph():
    from hTools2.objects import hGlyph
    g = hGlyph()

#-----------
# run tests
#-----------

#test_hSettings()
test_hWorld()
#test_hProject()
#test_hFont()
#test_hGlyph()

