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

import os, sys, inspect
parentDirectory =  os.path.realpath(
                    os.path.join(
                        os.path.dirname(
                            inspect.getfile(
                                inspect.currentframe())),
                    ".."))
if parentDirectory not in sys.path: sys.path.insert(1, parentDirectory)

from os.path import join as path
import errno

import paramiko


if __name__ == '__main__':
    from TestData import TestData
    from TestHelpers import TestHelpers
    from Area import Area


###
##
#


class AreaConn():
    def __init__(self, area):
        self.area = area
        self.__knownHostsFilePath = os.path.expanduser('~/.ssh/known_hosts')
        self.__knownHostsFilePathMSWin = os.path.expanduser('~/ssh/known_hosts')

        if os.path.isfile(self.__knownHostsFilePathMSWin) \
                and not os.path.isfile(self.__knownHostsFilePath):
            self.__knownHostsFilePath = self.__knownHostsFilePathMSWin


    def __getKnownHostData(self):
        try:
            knowHostsData = paramiko.util.load_host_keys(
                                                self.__knownHostsFilePath)
        except IOError:
            raise Exception("Failed to process known SSH hosts file '%s'." \
                                                % self.__knownHostsFilePath)

        wantedHostIdentityData = knowHostsData.lookup("[%s]:%s" \
                                    % (self.area.hostname, self.area.port)) # XXX - !!?

        if not wantedHostIdentityData:
            wantedHostIdentityData = knowHostsData.lookup(self.area.hostname)

        if not wantedHostIdentityData:
            raise Exception("Failed to get data from"
                    + " known SSH hosts file '%s'." \
                                % self.__knownHostsFilePath
                    + " Is it have appropriate key?"
                    + " What about: ssh-keygen -H -F \"%s\" ?" \
                                % self.area.hostname)

        return wantedHostIdentityData


    def __evaluateKnownHostKey(self):
        wantedHostIdentityData = self.__getKnownHostData()
        hostKeyTypeName = wantedHostIdentityData.keys()[0]
        hostKey = wantedHostIdentityData[hostKeyTypeName]

        return hostKey


    def doAction(self, routineName, *tArgs, **dArgs):
        with paramiko.Transport((self.area.hostname, self.area.port)) \
                as transport:
            transport.connect(
                        self.__evaluateKnownHostKey(),
                        self.area.login,
                        pkey = self.area.getPrivKey())

            with paramiko.SFTPClient.from_transport(transport) as sftp:
                if getattr(paramiko.SFTPClient, routineName, None):
                    wantedClass = paramiko.SFTPClient
                    tArgs = (sftp,) + tArgs
                else:
                    wantedClass = AreaConn
                    tArgs = (self,sftp) + tArgs
                    dArgs.pop('sftp', None)

                returnedObj = None
                try:
                    returnedObj = getattr(wantedClass, routineName)(*tArgs,
                                                                        **dArgs)
                except:
                    sys.stderr.write("Got exception from: %s.%s(%s,%s)\n" \
                                        % (wantedClass,
                                            routineName,
                                            tArgs,
                                            dArgs))
                    raise
            transport.close()
        return returnedObj


    def listdir(self, *tArgs, **dArgs):
        return self.doAction('listdir', *tArgs, **dArgs)


    def isPathExists(self, path, *tArgs, **dArgs):
        return self.doAction('_isPathExistsAction', path, *tArgs, **dArgs)


    def _isPathExistsAction(self, sftp, path, *tArgs, **dArgs):
        try:
            sftp.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                return False
            raise Exception("Unexpected error number '%s'" % e.errno
                            + "while checking of path '%s' existance." % path)
        else:
            return True


#     def mkdir(self, *tArgs, **dArgs):
#         if not self.doAction('_isPathExistsAction', *tArgs, **dArgs):
#             self.doAction('mkdir', *tArgs, **dArgs)


    def createPath(self, fullName, *tArgs, **dArgs):
        self.doAction('_createPathAction', fullName, *tArgs, **dArgs)

    def _createPathAction(self, sftp, fullName, *tArgs, **dArgs):
        if self._isPathExistsAction(sftp, fullName, *tArgs, **dArgs):
            return

        upName, basename = os.path.split(fullName.rstrip(os.sep))
        if self._isPathExistsAction(sftp, upName, *tArgs, **dArgs):
            sftp.mkdir(fullName, *tArgs, **dArgs)
        else:
            self._createPathAction(sftp, upName, *tArgs, **dArgs)
            sftp.mkdir(fullName, *tArgs, **dArgs)


    def rmdirectory(self, *tArgs, **dArgs):
        if self.doAction('_isPathExistsAction', *tArgs, **dArgs):
            self.doAction('rmdir', *tArgs, **dArgs)


#     def chdir(self, *tArgs, **dArgs):
#         return self.doAction('chdir', *tArgs)


#     def close(self, *tArgs, **dArgs):
#         return self.doAction('close', *tArgs)


###
##
#


def doTests():
    area = Area().pickFromFile(td.confFileName, 'acceptor')
    testConnectionOpenClose(area)
    testDirCreateWalkRemove(area)


def testConnectionOpenClose(area):
    area = Area().pickFromFile(td.confFileName, 'acceptor')
    areaConn = AreaConn(area)
    areaConn.listdir('.')


def testDirCreateWalkRemove(area):
    areaConn = AreaConn(area)
    rootPath = td.dirPathAcceptor
    subDirName = "testDirCreateWalkRemove"
    fullPath = path(rootPath, subDirName)

    areaConn.createPath(fullPath, mode=0700)
    areaConn.isPathExists(fullPath)
    areaConn.rmdirectory(fullPath)
    areaConn.createPath(fullPath, mode=0700)

    obtainedListing = areaConn.listdir(rootPath)

    assert subDirName in obtainedListing

    areaConn.rmdirectory(fullPath)
    areaConn.rmdirectory(rootPath)


###
##
#


if __name__ == '__main__':
    td = TestData(helpersInstance = TestHelpers())
    doTests()
