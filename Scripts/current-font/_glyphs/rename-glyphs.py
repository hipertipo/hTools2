# [h] batch rename glyphs

from hTools2.modules.color import *

def readNamesListFromFile(filePath):
    lines_raw = open(filePath, 'r').readlines()
    _names_list = []
    for line in lines_raw:
        if line[:1] != '#':
            old_name, new_name = line.split(' ')
            old_name = old_name.strip()
            new_name = new_name.strip()
            _names_list.append([old_name, new_name])
    return _names_list

def renameGlyphsFromList(font, namesList, overwrite=True, mark=True):
    print 'renaming glyphs...\n'
    for pair in namesList:
        oldName, newName = pair
        renameGlyph(f, oldName, newName, overwrite, mark)
    print
    print '...done.\n'

def renameGlyph(font, old_name, new_name, overwrite=True, mark=True):
    if font.has_key(old_name):
        g = font[old_name]
        # if new name already exists in font
        if font.has_key(new_name):
            # option [1] (default): overwrite
            if overwrite is True:
                print '\trenaming "%s" to "%s" (overwriting existing glyph)...' % (old_name, new_name)
                font.removeGlyph(new_name)
                g.name = new_name
                if mark:
                    g.mark = namedColors['orange']
                g.update()
            # option [2]: skip, do not overwrite
            else:
                print '\tskipping "%s", "%s" already exists in font.' % (old_name, new_name)
                if mark:
                    g.mark = namedColors['red']
                g.update()
        # if new name not already in font, simply rename glyph
        else:
            print '\trenaming "%s" to "%s"...' % (old_name, new_name)
            g.name = new_name
            if mark:
                g.mark = namedColors['green']
            g.update()
        # done glyph
    else:
        print '\tskipping "%s", glyph does not exist in font.' % old_name
    # done font
    f.update()

#-----
# run 
#-----

f = CurrentFont()

list_file = u"/Users/gferreira0/Desktop/nameslist.txt"
names_list = readNamesListFromFile(list_file)

renameGlyphsFromList(f, names_list, overwrite=True, mark=True)

