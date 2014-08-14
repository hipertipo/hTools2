import os
from mojo.UI import HelpWindow

# get docs path
lib_path = os.path.dirname(__file__)
lib_path = os.path.dirname(lib_path)
lib_path = os.path.dirname(lib_path)
docs_path = os.path.join(os.path.dirname(lib_path), "Docs/build/html/index.html")
if os.path.exists(docs_path):
    HelpWindow(docs_path, title="hTools2 Docs", developer='Gustavo Ferreira', developerURL='http://hipertipo.com/')
