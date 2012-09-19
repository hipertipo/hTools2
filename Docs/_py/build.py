# [h] build hTools2 html documentation

#---------
# imports
#---------

import os

import markdown
import codecs

from hTools2.modules.fileutils import walk

#------------
# data index
#------------

_index = {

    'introduction' : [
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
        'glyphs_copy_to_mask',
        'glyphs_mask',
        'glyphs_copy_to_layer',
        'glyphs_mirror',
        'glyphs_copy_paste',
        'glyphs_round_to_grid',
        'glyphs_shift_points',
        'glyphs_move',
        'glyphs_scale',
        'glyphs_skew',
        'glyphs_rasterize',
        'glyphs_actions',
        'glyphs_slide',
        'glyphs_set_width',
        'glyphs_set_margins',
        'glyphs_copy_margins',
        'glyphs_copy_widths',
        'glyphs_interpolate',
        'glyphs_paint',
        'glyphs_move_anchors',
        'glyphs_rename_anchors',
        'glyphs_transfer_anchors',
        'glyphs_change_suffix',
        'folder_actions',
        'folder_generate',
        'folder_otfs2ufos',
        'font_rename_glyphs',
        'font_create_spaces',
        'font_print_groups',
        'font_delete_layer',
        'font_import_layer',
        'font_adjust_vmetrics',
        'font_transfer_vmetrics',
    ],

}

_index_order = [
    'introduction',
    'modules',
    'objects',
    'dialogs',
]

#----------
# settings
#----------

PATH_BASE = '/_code/hTools2/Docs/'
PATH_HTML = '_html/'
PATH_CSS = '_css/'
PATH_MD = '_md/'
PATH_IMGS = '_imgs/'

#-----------
# functions
#-----------

def build_html():

    _md_path = os.path.join(PATH_BASE, PATH_MD)

    html_code = u''
    html_code += '%s\n' % '<!DOCTYPE html>'
    html_code += '%s\n' % '<html lang="en">'
    html_code += '%s\n' % '<meta charset="utf-8" />'
    html_code += '%s\n' % '<head>'
    html_code += '%s\n' % '<title>hTools2 Docs</title>'
    html_code += '%s\n' % '<script src="http://code.jquery.com/jquery-latest.min.js"></script>'
    html_code += '%s\n' % '<script src="../_js/scroll.js"></script>'
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
                _anchor = _title
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

#-----
# run
#-----

build_html()
