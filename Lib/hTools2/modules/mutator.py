import os
from collections import OrderedDict

from mutatorMath.ufo.document import DesignSpaceDocumentWriter # DesignSpaceDocumentReader

class DesignSpaceMaker(object):

    axes      = []
    masters   = []
    instances = []
    neutral   = None

    def __init__(self, project):
        self.project = project

        # remove existing .designspace file
        if os.path.exists(self.project.designspace_path):
            os.remove(self.project.designspace_path)

        # create fresh .designspace file
        self.doc_writer = DesignSpaceDocumentWriter(self.project.designspace_path, verbose=True)

    def add_masters(self, verbose=False):

        if verbose: print '\tadding masters...'

        for master in self.masters:
            ufo_path = os.path.join(self.project.ufos_folder, '%s.ufo' % master)

            # check if master exists
            if os.path.exists(ufo_path):

                # make Location
                L = {}
                for i in range(len(self.axes)):
                    axis  = self.axes[i]
                    param = self.masters[master][i]
                    L[axis] = param

                # add neutral
                if master == self.neutral:
                    if verbose: print '\t\tadding %s [neutral]...' % master
                    self.doc_writer.addSource(
                        ufo_path, master, location=L,
                        copyInfo=True, copyGroups=True,
                        copyLib=False, copyFeatures=False)

                # add deltas
                else:
                    if verbose: print '\t\tadding %s...' % master
                    self.doc_writer.addSource(ufo_path, master, location=L)

    def add_instances(self, verbose=False):

        if verbose: print '\tadding instances...'

        for instance in self.instances:
            ufo_filename = '%s.ufo' % instance.replace(' ', '-')
            ufo_path = os.path.join(self.project.instances_folder, ufo_filename)

            # make Location
            L = {}
            for i in range(len(self.axes)):
                axis  = self.axes[i]
                param = self.instances[instance][i]
                L[axis] = param

            # add instance
            if verbose: print '\t\tadding %s...' % instance
            self.doc_writer.startInstance(
                    fileName=ufo_path,
                    familyName='Untitled',
                    styleName=instance,
                    location=L)
            self.doc_writer.endInstance()

    def save(self, verbose=False):
        if verbose: print 'creating .designspace file...'
        # add masters
        self.add_masters(verbose)
        # add instances
        self.add_instances(verbose)
        if verbose: print '\tsaving file %s...' % self.project.designspace_path,
        # save designspace file
        self.doc_writer.save()
        if verbose: print os.path.exists(self.project.designspace_path)
        if verbose: print '...done.\n'
