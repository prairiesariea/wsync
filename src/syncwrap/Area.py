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


import os, sys, inspect
parentDirectory =  os.path.realpath(
                    os.path.join(
                        os.path.dirname(
                            inspect.getfile(
                                inspect.currentframe())),
                    ".."))
if parentDirectory not in sys.path: sys.path.insert(1, parentDirectory)

import yaml
from paramiko.ssh_exception import PasswordRequiredException
from paramiko import RSAKey

from Helper import Helper

if __name__ == '__main__':
    from TestData import TestData
    from TestHelpers import TestHelpers


###
##
#


class Area:
    def __init__(self,
                    hostname = None,
                    port = 22,
                    login = None,
                    sshPrivateKeyPath = os.path.expanduser('~/.ssh/id_rsa'),
                    privKey = None,
                    password = None):
        self.hostname = hostname
        self.port = port
        self.login = login
        self.sshPrivateKeyPath = sshPrivateKeyPath
        self.password = password


    def getLoginSpec(self):
        return "%s@%s" % (self.login, self.hostname)


    def getSSHLoginCmd(self):
        return "ssh -i '%s' %s" % (self.sshPrivateKeyPath,
                                        self.getLoginSpec())


    def pickFromFile(self, confFileName, sectionName):
        with open(confFileName, 'r') as ymlfile:
            cdd = yaml.load(ymlfile)  # FilesSpec - configuration data dictionary.

        self.hostname = cdd[sectionName]['hostname']
        self.login = cdd[sectionName]['login']
        self.sshPrivateKeyPath = cdd[sectionName]['ssh private key path']
        self.password = cdd[sectionName]['password']

        return self


    def getPrivKeyPath(self):
        return self.sshPrivateKeyPath

    def getPrivKey(self):
        try:
            privKey = RSAKey(filename = self.sshPrivateKeyPath)
        except PasswordRequiredException:
            sys.stderr.write("WARNING:%s:%s: " \
                                % (__file__, Helper().lineno())\
                                + "Private key '%s' is encrypted." \
                                % self.sshPrivateKeyPath
                                + "It will not be used.\n")
            privKey = None
        return privKey



###
##
#


def doTests():
    testGetLoginSpec()
    testGetSSHLoginCmd()
    testPickFromFile()


def testGetLoginSpec():
    area = Area(hostname = td.hostname, login = td.login)

    expectedString = "%s@%s" % (td.login, td.hostname)
    obtainedString = area.getLoginSpec()

    assert expectedString == obtainedString, "Failed with tests."


def testGetSSHLoginCmd():
    area = Area(td.hostname, td.port, td.login, td.sshPrivateKeyPath)

    expectedString = "ssh -i '%s' %s@%s" % (td.sshPrivateKeyPath,
                                                td.login,
                                                td.hostname)
    obtainedString = area.getSSHLoginCmd()

    assert expectedString == obtainedString, "Failed with tests."


def testPickFromFile():
    area = Area()
    area.pickFromFile(td.confFileName, 'donor')

    assert area.hostname == td.hostname # XXX - Other 'Area' atrributes are not validated.
    assert area.login == td.login
    assert area.sshPrivateKeyPath == td.sshPrivateKeyPath
    assert area.password == td.password


###
##
#


if __name__ == '__main__':
    td = TestData(helpersInstance = TestHelpers())
    doTests()
