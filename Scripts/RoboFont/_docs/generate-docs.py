# [h] : generate documentation

import pycco

from hTools2.modules.fileutils import walk

source_files = []

docs_folder = '/_code/hTools2/Docs/'

pycco.process(sources, preserve_paths=True, outdir=_outdir)

#html_doc = pycco.generate_documentation(sources[0], outdir=_outdir, preserve_paths=True)
#print html_doc
