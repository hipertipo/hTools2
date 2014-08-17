# [h] libutils

"""A collection of functions to check the integrity of libs."""

### thanks to Frederik Berlaen ###

# functions

def check_value(value):
    if isinstance(value, list):
        check_list(value)
    elif isinstance(value, dict):
        check_dict(value)
    elif value == None:
        print "----------- error -------------"
    elif isinstance(value, (int, float, str)):
        pass
    else:
        print value

def check_list(L):
    for value in L:
        checkValue(value)

def check_dict(D):
    for key, value in D.items():
        print key
        checkValue(value)

def check_font_lib(font):
    print 'checking integrity of font libs...'
    check_value(dict(font.lib))
    print '...done.\n'

def check_glyph_libs(font):
    print 'checking integrity of glyph libs...'
    for g in font:
        print g.name, check_value(dict(g.lib))
    print '...done.\n'
