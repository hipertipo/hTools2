# [h] : git tools

# imports

import os
import subprocess

# objects

class GitHandler(object):

    """A simple object to call commands on a git repository."""

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
        process = subprocess.Popen(_command,
               cwd=self.folder,
               stdout=subprocess.PIPE,
               stderr=subprocess.PIPE,
               shell=False)
        (output, error) = process.communicate()
        # return
        if len(output) > 0:
            return output
        else:
            return error

    def status(self):
        # output = self.command(['status', '--%s' % mode])
        output = self.command(['status'])
        return output

    def add(self, file_name=None, all_files=True, track=True):
        if file_name:
            output = self.command('add %s' % file_name)
        else:
            if all_files:
                output = self.command('add .')
            if track:
                output = self.command('add -A')
        return output

    def commit(self, message):
        output = self.command(['commit', '-m %s' % message])
        return output

    def log(self, n=10):
        #output = self.command(['log', '--pretty=oneline', '-%s' % n])
        output = self.command(['log', '--pretty=format:%H %ad %an %s', '-%s' % n])
        return output

    def diff(self, mode='raw'):
        ### modes: raw, numstat, shortstat, summary, patch-with-stat, name-status, name-only
        ### see http://git-scm.com/docs/git-diff
        output = self.command(['diff', '--%s' % mode])
        return output

    def remote(self):
        output = self.command('remote')
        remotes = output.split()
        return remotes

    def push(self, remote=None, branch=None):
        if (branch and remote) is None:
            output = self.command('push')
        else:
            if remote:
                if branch:
                    output = self.command(['push', remote, branch])
                else:
                    output = self.command(['push', remote])
        return output
