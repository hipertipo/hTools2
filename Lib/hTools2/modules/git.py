# [h] : git tools

# imports

import os
import subprocess

# objects

class GitHandler(object):

    """An object to call commands on a git repository."""

    # attributes

    #: The folder in which the git repository lives.
    folder = None

    #: A list with names of remote repositories.
    remotes = []

    # functions

    def __init__(self, repo_dir):
        self.folder = repo_dir

    def command(self, command):
        """A generic function to call git commands on a repo."""
        # build command
        if type(command) is str:
            command = command.split(' ')
        _command = [ 'git' ] + command
        # run command
        pr = subprocess.Popen(_command,
               cwd=os.path.dirname(self.folder),
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE,
               shell=False)
        (out, error) = pr.communicate()
        return out, error
    
    def status(self, mode='short'):
        #out, err = self.command('status')
        out, err = self.command(['status', '--%s' % mode])
        return out

    def add(self, file_name=None, all_files=True, track=True):
        if file_name:
            self.command('add %s' % file_name)
        else:
            if all_files:
                self.command('add .')
            if track:
                self.command('add -A')

    def commit(self, message):
        out, err = self.command('commit -m %s' % message)
        return out

    def log(self, n=10):
        out, err = self.command(['log', '--pretty=format:%H; %ad; %an; %ae; %s;', '-%s' % n])
        return out

    def diff(self, mode='raw'):
        ### modes: raw, numstat, shortstat, summary, patch-with-stat, name-status, name-only
        ### see http://git-scm.com/docs/git-diff
        out, err = self.command(['diff', '--%s' % mode])
        return out

    def remote(self):
        out, err = self.command('remote')
        remotes = out.split()
        return remotes
