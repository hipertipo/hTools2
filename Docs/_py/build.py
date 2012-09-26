# [h] build hTools2 documentation

# debug

import hTools2
reload(hTools2)

if hTools2.DEBUG:
    import hTools2.objects.hdocs
    reload(hTools2.objects.hdocs)

# imports

from hTools2.objects.hdocs import hDocs

# settings

_index = {

    'about' : [
        'introduction',
        'overview',
        'conventions',
        'installation'
    ],

    'modules' : [
        'modules',
        'anchors',
        'color',
        'encoding',
        'fileutils',
        'fontinfo',
        'fontutils',
        'ftp',
        'glyphutils',
        'interpol',
        'nodebox',
        'opentype',
        'pens',
        'rasterizer',
        'sysutils',
    ],

    'objects' : [
        'objects',
        'hSettings',
        'hWorld',
        'hSpace',
        'hProject',
        'hLibs',
        'hFont',
        'hGlyph',
        'hLine',
        'hParagraph',
    ],

    'libs' : [
        'libs',
        'accents',
        'composed',
        'encoding',
        'info',
        'interpol',
        'project',
        'spacing',
        'vmetrics',
    ],

    'dialogs' : [
        'all-fonts',
        'batch-folder',
        'selected-glyphs',
        'current-font',
        'current-glyph',
        'workspace',
    ],

}

_index_order = [
    'about',
    'modules',
    'objects',
    'libs',
    'dialogs',
]

_folders = {
    'root'      : '/_code/hTools2/Docs/',
    'html'      : '_html/',
    'css'       : '_css/',
    'markdown'  : '_md/',
    'images'    : '_imgs/',
    'ftp'       : 'www/hipertipo.org/temp/hTools2/',
}

# run

d = hDocs('hTools2 v1.5')
d.build(_index, _index_order, _folders)
d.upload()
