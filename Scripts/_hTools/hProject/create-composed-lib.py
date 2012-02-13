from hTools2.objects import hFont

ufo = CurrentFont()

font = hFont(ufo)

print font.project.libs['composed'] 

_composed = {
    # latin_lc
    'ae' : [ 'a', 'e' ],
    'dcroat' : [ 'd' ],
    'eng' : [ 'n', 'j' ],
    'hbar' : [ 'h' ],
    'ij' : [ 'i', 'j' ],
    'lslash' : [ 'l' ],
    'oe' : [ 'o', 'e' ],
    'oslash' : [ 'o' ],
    'tbar' : [ 't' ],
    'thorn' : [ 'p' ],
    # latin_uc
    'AE' : [ 'A', 'E' ],
    'Dcroat' : [ 'D' ],
    'Eth' : [ 'Dcroat' ],
    'Eng' : [ 'N', 'j' ],
    'Hbar' : [ 'H' ],
    'IJ' : [ 'I', 'J' ],
    'Lslash' : [ 'L' ],
    'OE' : [ 'O', 'E' ],
    'Oslash' : [ 'O' ],
    'Tbar' : [ 'T' ],
    'Thorn' : [ 'P' ],
}

font.project.libs['composed'] = _composed
font.project.write_lib('composed')

print font.project.libs['composed'] 


