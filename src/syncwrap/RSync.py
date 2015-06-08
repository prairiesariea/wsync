#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
#  Copyright 2015 Prairies Ariea
#
#  This file is part of Files Sync.
#
#  Files Sync is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Files Sync is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Files Sync. If not, see <http://www.gnu.org/licenses/>.
#
##

from __future__ import print_function

import os
import sys
from re import search
from os.path import join as path

from Helper import Helper
from AreaConn import AreaConn


###
##
#


class RSync:
    def __init__(self, donor, acceptor):
        self.donor = donor
        self.acceptor = acceptor

        self.__validate()


    @property
    def donor(self):
        return self._donor

    @property
    def acceptor(self):
        return self._acceptor

    @donor.setter
    def donor(self, donor):
        self._donor = donor
        self.__validate()

    @acceptor.setter
    def acceptor(self, acceptor):
        self._acceptor = acceptor
        self.__validate()


    def __validate(self):
        assert not ( \
                    (self.donor    and not self.donor.isLocal()) \
                        and \
                    (self.acceptor and not self.acceptor.isLocal())
                ), \
                "Can have only one remote specification."

        for filesSpec in self.donor.getFilesSpecPool():
            assert not search(r'\s', filesSpec.getPath()), \
                "Spaces in top level directory name are not supported."
        for filesSpec in self.acceptor.getFilesSpecPool():
            assert not search(r'\s', filesSpec.getPath()), \
                "Spaces in top level directory name are not supported."


    def __findSSHKeyPath(self):
        sshKeyPath = None
        donorValue = self.donor.getPrivKeyPath()
        acceptorValue = self.acceptor.getPrivKeyPath()

        if donorValue:
            sshKeyPath = donorValue
        if acceptorValue:
            sshKeyPath = acceptorValue
        return sshKeyPath

    def __getURLPool(self):
        urlPool = []
        acceptorPrefix = self.acceptor.getURLPool()[0]['path'] # XXX - First path from acceptor will be used, and the dictionary is not sorted, and dictionary object is used here.

        for pair in self.donor.getURLPool(asIsLocal = False):
            donorUrl = pair['path']

            acceptorURL = os.path.normpath(path(acceptorPrefix \
                                    + os.sep \
                                    + donorUrl.strip("/").split(":", 1)[-1]))
            ignoreList = pair['ignore names']
            urlPool.append([
                                donorUrl,
                                acceptorURL,
                                ignoreList
                                ])

        return urlPool

    def __createPath(self, newPath):
        if not os.path.exists(newPath):
            os.makedirs(newPath, 0700)

    def __rsync(self, donorURL, acceptorURL, ignoreItemsPool):
        rsyncShellCommand = ["rsync",
            "--verbose",
            "--progress",
            "--stats",
            "--compress",
            "--compress-level=9",
            "--recursive",
            "--times",
            "--perms",
            "--links",
            "-L",
            "--exclude \'"
                + "\' --exclude \'".join(ignoreItemsPool)
                + "\'",
            "--rsh=\"ssh -i '%s' -C\"" % self.__findSSHKeyPath(),
            "\'" + path(donorURL, "") + "\'*",
            "\'" + acceptorURL + "\'"]

        sys.stdout.write("\nINFO:%s:%s: " % (__file__, Helper().lineno())
                            + "Is going to launch shell command: %s\n\n"
                            % " ".join(rsyncShellCommand))
        exitCode = os.system(" ".join(rsyncShellCommand))
        sys.stdout.write("\nINFO:%s:%s: " % (__file__, Helper().lineno())
                            + "Shell command finished"
                            + " with exit code '%s'.\n" % exitCode)
        self.__validateRSyncExitCode(exitCode)

        return

    def doSync(self):

        # XXX - Here is part which is an separated function.
        acceptorPathPrefix = self.acceptor.getFilesSpecPool()[0].getPath() # XXX - First path from acceptor will be used, and the dictionary is not sorted, and dictionary object is used here.
        for pathSpec in self.donor.getFilesSpecPool():
            pathFull = os.path.normpath(
                                path( acceptorPathPrefix,
                                        Helper.os_path_relpath(
                                                        pathSpec.getPath(),
                                                        os.path.abspath(os.sep)
                                        )
                                    )
                                )

            if self.acceptor.isLocal():
                self.__createPath(pathFull)
            else:
                AreaConn(self.acceptor).createPath(pathFull)

        for donorURL, acceptorURL, ignoreList in self.__getURLPool():
            self.__rsync(donorURL, acceptorURL, ignoreList)


    def __validateRSyncExitCode(self, exitCode):
        if exitCode != 0:
            raise Exception("'rsync' failed and exit code is '%s'." % exitCode)


###
##
#


from NodeSpec import NodeSpec
from TestHelpers import TestHelpers

def doTests():
    th = TestHelpers()
    th.removeTestDirTree()
    testRemoteLocalAccessCombinations(th)

def testRemoteLocalAccessCombinations(testHelper):
    th = testHelper
    th.createTestDirsTree()

    testPairs = (
                    ('donor', 'acceptor'),
                    ('pair-l2l_donor', 'pair-l2l_acceptor'),
                    ('pair-l2r_donor', 'pair-l2r_acceptor'),
                    ('pair-r2l_donor', 'pair-r2l_acceptor'),
                )

    for (donor, acceptor) in testPairs:
        node_donor = NodeSpec().pickFromFile(th.td.confFileName, donor)
        node_acceptor = NodeSpec().pickFromFile(th.td.confFileName, acceptor)
        RSync(node_donor, node_acceptor).doSync()





###
##
#


if __name__ == '__main__':
    doTests()
