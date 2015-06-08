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


import yaml

from Area import Area
from FilesSpec import FilesSpec

if __name__ == '__main__':
#     from TestData import TestData
    from TestHelpers import TestHelpers


###
##
#


class NodeSpec(Area):
    def __init__(self,
                    filesSpecPool = None,
                    hostname = None,
                    login = None,
                    sshPrivateKeyPath = None,
                    password = None):

        Area.__init__(self,
                    hostname = hostname,
                    login = login,
                    sshPrivateKeyPath = sshPrivateKeyPath,
                    password = password)

        self.__filesSpecPool = filesSpecPool

    def getFilesSpecPool(self):
        return self.__filesSpecPool

    def getURLPool(self, asIsLocal = False):
        urlPool = []
        for filesSpec in self.__filesSpecPool:
            path = filesSpec.getPath()
            if not self.isLocal() and not asIsLocal:
                path = "%s@%s:%s" \
                                % (self.login, \
                                   self.hostname, \
                                   path)

            urlPool.append({'path': path,
                            'ignore names': filesSpec.getIgnorePool()
                            })

        return urlPool


    def pickFromFile(self, confFileName, sectionName):
        with open(confFileName, 'r') as yamlFile:
            cdd = yaml.load(yamlFile)  # cdd - configuration data dictionary.

        area = Area().pickFromFile(confFileName, sectionName)
        self.hostname = area.hostname
        self.login = area.login
        self.sshPrivateKeyPath = area.sshPrivateKeyPath
        self.password = area.password


        filesSpecConf = cdd[sectionName]['path']

        self.__filesSpecPool = []
        for name in filesSpecConf:
            self.__filesSpecPool.append(
                        FilesSpec(filesSpecConf[name]['path'],
                                    filesSpecConf[name]['ignore names']))
        return self

    def isLocal(self):
        if self.hostname: isLocal = False
        else: isLocal = True
        return isLocal


###
##
#


def doTests():
    testGetAuthKey()
    testPickFromFile()
#     testIsLocal()

def testGetAuthKey():

    nodeSpec = NodeSpec(sshPrivateKeyPath = th.td.sshPrivateKeyPath)
    assert nodeSpec.getPrivKeyPath() == th.td.sshPrivateKeyPath, "Failed with tests."

    nodeSpec = NodeSpec()
    assert nodeSpec.getPrivKeyPath() == None, "Failed with tests."


def testPickFromFile():
    nodeSpec = NodeSpec().pickFromFile(th.td.confFileName, 'donor')

    assert nodeSpec.hostname == th.td.hostname
#     assert nodeSpec._NodeSpec__filesSpecPool[0].getPath() == td.dirPathDonor
#     assert nodeSpec._NodeSpec__filesSpecPool[0].getIgnorePool() == td.ignoreNamesPool

def testIsLocal():
    nodeSpec_remote = NodeSpec().pickFromFile(th.td.confFileName, 'donor')
    nodeSpec_local = NodeSpec().pickFromFile(th.td.confFileName, 'acceptor')

    assert nodeSpec_remote.hostname != None
    assert nodeSpec_remote.isLocal() == False

    assert nodeSpec_local.hostname == None
    assert nodeSpec_local.isLocal() == True


###
##
#


if __name__ == '__main__':
    th = TestHelpers()
    th.removeTestDirTree()
    doTests()
