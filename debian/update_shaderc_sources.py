#!/usr/bin/env python

# Copyright 2016 The Shaderc Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Get source files for Shaderc and its dependencies from public repositories.
   This is the debian packaging version of the script, which fetches the tarball
   archives, rather than cloning the whole repository.
"""

from __future__ import print_function

import argparse
import json
import distutils.dir_util
import os.path
import subprocess
import sys

KNOWN_GOOD_FILE = 'known_good.json'

# Maps a site name to its hostname.
SITE_TO_HOST = { 'github' : 'github.com',
                 'gitlab' : 'gitlab.com'}

VERBOSE = True


def command_output(cmd, directory, fail_ok=False):
    """Runs a command in a directory and returns its standard output stream.

    Captures the standard error stream.

    Raises a RuntimeError if the command fails to launch or otherwise fails.
    """
    if VERBOSE:
        print('In {d}: {cmd}'.format(d=directory, cmd=cmd))
    p = subprocess.Popen(cmd,
                         cwd=directory,
                         stdout=subprocess.PIPE)
    (stdout, _) = p.communicate()
    if p.returncode != 0 and not fail_ok:
        raise RuntimeError('Failed to run {} in {}'.format(cmd, directory))
    if VERBOSE:
        print(stdout)
    return stdout


class GoodCommit(object):
    """Represents a good commit for a repository."""

    def __init__(self, json):
        """Initializes this good commit object.

        Args:
        'json':  A fully populated JSON object describing the commit.
        """
        self._json = json
        self.name = json['name']
        self.site = json['site']
        self.subrepo = json['subrepo']
        self.subdir = json['subdir'] if ('subdir' in json) else '.'
        self.commit = json['commit']

    def GetUrl(self, style='https'):
        """Returns the URL for the repository."""
        host = SITE_TO_HOST[self.site]
        sep = '/' if (style is 'https') else ':'
        return '{style}://{host}{sep}{subrepo}{sep}archive{sep}{commit}.tar.gz'.format(
                    style=style,
                    host=host,
                    sep=sep,
                    subrepo=self.subrepo,
		    commit=self.commit)

    def FetchArchive(self):
        distutils.dir_util.mkpath(self.subdir)
	tarballname = '{name}.tgz'.format(name=self.name)
        command_output(['wget', self.GetUrl(), '-O', tarballname], self.subdir)
	command_output(['tar', 'xf', tarballname, '--strip-components=1'], self.subdir)
        command_output(['rm', tarballname], self.subdir)


def GetGoodCommits(known_good_file):
    """Returns the latest list of GoodCommit objects."""
    with open(known_good_file) as known_good:
        return [GoodCommit(c) for c in json.loads(known_good.read())['commits']]


def main():
    parser = argparse.ArgumentParser(description='Get Shaderc source dependencies at a known-good commit')
    parser.add_argument('--dir', dest='dir', default='src',
                        help="Set target directory for Shaderc source root. Default is \'src\'.")
    parser.add_argument('--file', dest='known_good_file', default=KNOWN_GOOD_FILE,
                        help="The file containing known-good commits. Default is \'' + KNOWN_GOOD_FILE + '\'.")

    args = parser.parse_args()

    commits = GetGoodCommits(args.known_good_file)

    distutils.dir_util.mkpath(args.dir)
    print('Change directory to {d}'.format(d=args.dir))
    os.chdir(args.dir)

    # Create the subdirectories in sorted order so that parent git repositories
    # are created first.
    for c in sorted(commits, cmp=lambda x,y: cmp(x.subdir, y.subdir)):
        print('Get {n}\n'.format(n=c.name))
        c.FetchArchive()

    print('Remeber to run "git add -f src", and check that it looks sane')
    sys.exit(0)



if __name__ == '__main__':
    main()
