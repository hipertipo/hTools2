# [h] build hTools2 html documentation

#---------
# imports
#---------

import os

import markdown
import codecs

from hTools2.objects import hWorld
from hTools2.modules.fileutils import walk
from hTools2.modules.ftp import *

#------------
# data index
#------------

_index = {

    'about' : [
        'introduction',
        'overview',
        'conventions',
        'installation'
    ],

    'modules' : [
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
    'dialogs',
]

#----------
# settings
#----------

PATH_BASE =     '/_code/hTools2/Docs/'
PATH_HTML =     '_html/'
PATH_CSS =      '_css/'
PATH_MD =       '_md/'
PATH_IMGS =     '_imgs/'
PATH_FTP =      'www/hipertipo.org/temp/hTools2/'

#-----------
# functions
#-----------

def build_html():

    print 'building docs...'

    _md_path = os.path.join(PATH_BASE, PATH_MD)

    html_code = u''
    html_code += '<!DOCTYPE html>\n'
    html_code += '<html lang="en">\n'
    html_code += '<meta charset="utf-8" />\n'
    html_code += '<head>\n'
    html_code += '<title>hTools2 Docs</title>\n'
    html_code += '<script src="http://code.jquery.com/jquery-latest.min.js"></script>\n'
    html_code += '<script src="../_js/scroll.js"></script>\n'
    html_code += '<link href="../_css/base.css" rel="stylesheet" />\n'
    html_code += '</head>\n'
    html_code += '<body>\n'

    # navigation

    html_code += '<div id="nav">\n'
    html_code += '<h1><a href="#top">hTools2 v1.5</a></h1>\n'

    count = 0
    html_code += '<div>\n'
    for section in _index_order:
        _section_path = os.path.join(_md_path, section)
        if count == 2:
            html_code += '</div>\n'
            html_code += '<div>\n'
        html_code += '<h4>%s</h4>\n' % section
        html_code += '<ul>\n'
        for item in _index[section]:
            _item_path = os.path.join(_section_path, item + '.md')
            if os.path.exists(_item_path):
                _md_file = codecs.open(_item_path, mode="r", encoding="utf-8")
                _title = _md_file.readline()
                _title = _title[3:-1]
                _title = _title.lower()
                _anchor = _title.replace(' ', "_")
                html_code += '<li><a href="#%s">%s</a></li>\n' % (_anchor, _title)
        html_code += '</ul>\n'
        count += 1
    html_code += '</div>\n'

    html_code += '</div>\n'

    # content

    html_code += '<div id="content">\n'
    html_code += '<a name="top"></a>\n'
    for section in _index_order:
        _section_path = os.path.join(_md_path, section)
        for item in _index[section]:
            _item_path = os.path.join(_section_path, item + '.md')
            if os.path.exists(_item_path):
                _md_file = codecs.open(_item_path, mode="r", encoding="utf-8")
                _md_text = _md_file.read()
                _html = markdown.markdown(_md_text)
                _anchor = item.lower()
                _anchor = _anchor.replace('-', "_")
                html_code += '<a name="%s"></a>\n' % _anchor
                html_code += _html
    html_code += '</div>\n'

    html_code += '</body>\n'
    html_code += '</html>\n'

    _html_folder = os.path.join(PATH_BASE, PATH_HTML)
    _html_path = os.path.join(_html_folder, 'index.html')

    _html_file = codecs.open(_html_path, "w", encoding="utf-8", errors="xmlcharrefreplace")
    _html_file.write(html_code)
    _html_file.close()

    print '...done.\n'

def upload_docs():
    print 'uploading docs...'
    # get ftp settings
    w = hWorld()
    _url = w.settings.hDict['ftp']['url']
    _login = w.settings.hDict['ftp']['login']
    _password = w.settings.hDict['ftp']['password']
    # upload html
    _folder_html = os.path.join(PATH_FTP, '_html')
    F = connect_to_server(_url, _login, _password, _folder_html, verbose=False)
    _html_folder = os.path.join(PATH_BASE, PATH_HTML)
    _html_path = os.path.join(_html_folder, 'index.html')
    print '\tuploading html...'
    upload_file(_html_path, F)
    F.quit()
    # upload css
    _folder_css = os.path.join(PATH_FTP, '_css')
    F = connect_to_server(_url, _login, _password, _folder_css, verbose=False)
    _css_folder = os.path.join(PATH_BASE, PATH_CSS)
    _css_path = os.path.join(_css_folder, 'base.css')
    print '\tuploading css...'
    upload_file(_css_path, F)
    # done
    print '...done.'

#-----
# run
#-----

build_html()
upload_docs()
