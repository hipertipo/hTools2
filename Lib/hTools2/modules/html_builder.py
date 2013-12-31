# [h] hTools2.modules.html_builder

#---------
# imports
#---------

import os
import codecs
import markdown
import subprocess

#-----------
# constants
#-----------

LANG_CODES = {
    # https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    'arabic' : 'ar',
    'english' : 'en',
    'malayalam' : 'ml',
    'chinese' : 'zh',
    'japanese' : 'ja',
    'uyghur' : 'ug',
    'farsi' : 'fa',
    'hindi' : 'hi',
}

#-----------
# functions
#-----------

def get_html(markdown_path):
    '''Get generated html code from markdown file at the given path.'''
    src_file = codecs.open(markdown_path, mode="r", encoding="utf-8")
    src_text = src_file.read()
    html_text = markdown.markdown(src_text, extensions=['meta', 'attr_list'])
    return html_text

def get_metadata(markdown_path):
    '''Get metadata from markdown file at the given path.'''
    src_file = codecs.open(markdown_path, mode="r", encoding="utf-8")
    src_text = src_file.read()
    md = markdown.Markdown(extensions = ['meta'])
    html_text = md.convert(src_text)
    return md.Meta

def compile_sass(sass_path):
    '''Compile a ``.sass`` file (and dependencies) into a single ``.css`` file.'''
    css_path = os.path.splitext(sass_path)[0] + '.css'
    subprocess.call(['sass', sass_path, css_path])

#---------
# objects
#---------

class HTMLBuilder(object):

    # attributes

    #: Contents of the html ``<title>`` element.
    title = None

    #: Base folder of the html website.
    base_dir = None

    #: Name of the folder containing markdown text sources.
    src_folder_name = '_src'

    #: Name of the folder containing ``.sass`` sources and compiled ``.css.`` files.
    css_folder_name = '_css'

    #: Name of the folder containing images.
    imgs_folder_name = '_imgs'

    #: Name of the folder containing javascript files.
    js_folder_name = '_js'

    # methods

    def __init__(self, path):
        self.base_dir = path

    @property
    def src_dir(self):
        return os.path.join(self.base_dir, self.src_folder_name)

    @property
    def css_dir(self):
        return os.path.join(self.base_dir, self.css_folder_name)

    @property
    def js_dir(self):
        return os.path.join(self.base_dir, self.js_folder_name)

    @property
    def imgs_dir(self):
        return os.path.join(self.base_dir, self.css_folder_name)

    def html_(self):
        '''Open the ``<html>`` tag.'''
        html = '<!DOCTYPE html>\n'
        html += '<html lang="en">\n'
        html += '<meta charset="utf-8" />\n'
        return html

    def _html(self):
        '''Close the ``</html>`` tag.'''
        return '</html>\n'

    def head_(self):
        '''Open the ``<head>`` tag.'''
        return '<head>\n'

    def _head(self):
        '''Close the ``</head>`` tag.'''
        return '</head>\n'

    def body_(self):
        '''Open the ``<body>`` tag.'''
        return '<body>\n'

    def _body(self):
        '''Close the ``</body>`` tag.'''
        return '</body>\n'

    def _title_(self, title):
        '''Create the ``title`` element.'''
        return '<title>%s</title>\n' % title

    def _css_(self, base=None):
        '''Create a link to the ``css`` file.'''
        return '<link href="%s%s/styles.css" rel="stylesheet" />\n' % (base, self.css_folder_name)

    def save_html(self, html, folder, file_name):
        '''Save html code to a ``.html`` file with ``file_name`` in the given ``folder``.'''
        html_path = os.path.join(folder, '%s.html' % file_name)
        html_file = codecs.open(html_path, "w", encoding="utf-8", errors="xmlcharrefreplace")
        html_file.write(html)
        html_file.close()

    def build_css(self):
        '''Build a single ``.css`` file from all ``.sass`` sources.'''
        css_name = 'styles'
        sass_path = os.path.join(self.css_dir, '%s.sass' % css_name)
        compile_sass(sass_path)
