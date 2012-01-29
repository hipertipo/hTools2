# [h] : create interpolation lib

from hTools2.objects import hProject

interpol_lib = {
    '25' : [ '15', '55', (.75, .75) ],
    '35' : [ '15', '55', (.50, .50) ],
    '45' : [ '15', '55', (.25, .25) ],
    '65' : [ '55', '95', (.75, .75) ],
    '75' : [ '55', '95', (.50, .50) ],
    '85' : [ '55', '95', (.25, .25) ],
}

p = hProject('Synthetica')
p.libs['interpol'] = interpol_lib
p.write_lib('interpol')
