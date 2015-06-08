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
from os.path import join as path
import re
import yaml
from shutil import rmtree


from TestData import TestData

class TestHelpers():
    def __init__(self, confFileName = None):
        self.td = TestData(helpersInstance = self)
        if not os.path.exists(self.td.confFileName):
            self.createConfFile()

    def removeTestDirTree(self):
        if self.td.dirChroot and os.path.exists(self.td.dirChroot):
            rmtree(self.td.dirChroot)

    def createTestDirsTree(self):
        if os.path.exists(self.td.dirChroot):
            raise Exception("Already exist test chroot '%s'. Here is \"rm -rf '%s'\"."
                                % (TestData().dirChroot, TestData().dirChroot))

        if not os.path.exists(self.td.dirPathDonor):
            os.makedirs(self.td.dirPathDonor, mode=0700)

        for name in self.td.cdd['donor']['path'].keys():
            newPath = self.td.cdd['donor']['path'][name]['path']
            if not os.path.exists(newPath):
                os.makedirs(newPath, mode=0700)
            self._mkTestSubDirSet(newPath, 3, 2)

        if not os.path.exists(self.td.dirPathAcceptor):
            os.makedirs(self.td.dirPathAcceptor, 0700)


    def _mkTestSubDirSet(self, dirName, quantity, depth):

        self._createFileIfSpecialDir(dirName, "0")

        if depth == 0:
            return

        for idx in range(0, quantity):
            if idx%2 == 0:
                newPath = path(dirName, str(idx) + " with space in name")
            else:
                newPath = path(dirName, str(idx))


            not os.path.exists(newPath) and os.mkdir(newPath, 0700)
            if idx%2 == 1: self._createIgnoreItemsInDir(newPath)

            self._mkTestSubDirSet(newPath, quantity, depth - 1 )


    def _createFileIfSpecialDir(self, dirName, marker, fileName = None):
        if fileName == None:
            fileName = "file-" + os.path.basename(dirName)

        r = re.compile(marker + r".*")
        if r.match(os.path.basename(dirName)):
            open(path(dirName, fileName), 'a').close()


    def _createIgnoreItemsInDir(self, dirName):
        for name in self.td.ignoreNamesPool[:-1]:
            newPath = path(dirName, name)
            if not os.path.exists(newPath):
                os.mkdir(newPath)
        self._createFileIfSpecialDir(dirName,
                                    "",
                                    fileName = self.td.ignoreNamesPool[-1])

    def createConfFile(self, confFileName, configurationData):
        assert not os.path.isdir(confFileName), \
                    "There is already exist directory '%s'." % confFileName \
                        + " Can not create file with this name."

        with open(confFileName, 'w') as configfile:
            yaml.dump(configurationData,
                      configfile,
                      indent=4,
                      default_flow_style=False)

        assert os.path.isfile(confFileName), \
                    "Failed to create configuration file '%s'." % confFileName


###
##
#


def doTests():
    TestHelpers().removeTestDirTree()
    TestHelpers().createTestDirsTree()
    TestHelpers().createConfFile(TestData().confFileName,
                                    TestData().configurationData)
    testConfFile()

def testConfFile():
    td = TestData()
    with open(td.confFileName, 'r') as ymlfile:
        cdd = yaml.load(ymlfile)  # Configuration data dictionary.

    assert td.hostname == cdd['donor']['hostname']
    assert td.port == cdd['donor']['port']
    assert td.login == cdd['donor']['login']
    assert td.sshPrivateKeyPath == cdd['donor']['ssh private key path']
    assert td.password == cdd['donor']['password']

    assert td.dirPathDonor == cdd['donor']['path']['opt']['path']
    assert td.ignoreNamesPool == cdd['donor']['path']['opt']['ignore names']

    assert td.dirPathAcceptor == cdd['acceptor']['path']['acceptor']['path']


###
##
#


if __name__ == '__main__':
    doTests()
