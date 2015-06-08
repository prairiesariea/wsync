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
import pwd
import os
from os.path import dirname
from os.path import join as path
import inspect
import copy


class TestData():
    def __init__(self, confFileName = None, helpersInstance = None):
        if confFileName == None:
            projectTopDir =  os.path.realpath(
                os.path.join(
                    dirname(
                        inspect.getfile(
                            inspect.currentframe())),
                    "..", "..", "tmp")) # Speculative - double ".." later may not be a wanted value.

            self.confFileName = path(projectTopDir, "test-auto-generated.conf")
        else:
            self.confFileName = confFileName

        self.dirChroot = path(os.path.abspath(os.sep), "tmp", "RSyncTests")

        self.__setTestConfigDataTemplates()
        self.cdd = self.__setTestConfigDataObject()
        self.__setDirectAccessVarsHeap()

        self.configurationData

        if helpersInstance:
            helpersInstance.createConfFile(self.confFileName,
                                            self.configurationData)

    def __setTestConfigDataTemplates(self):
        """
            Here are top level subsections of configuration file as Python data
            structures. There are _subsections_ only. At the moment of writing
            this data's structure is corresponding YAML structure.
        """
        self.donorTS = { # Template Spec - Donor Test Data Template Specification (conf file whole subsection).
                'path': {
                    'opt': {
                        'path': path(self.dirChroot, "donor", 'opt'),
                        'ignore names':
                                        ["ignore name 01 with space in name",
                                           "ignore_name_02",
                                           "ignore_name_03"]
                    },
                    'var': {
                        'path': path(self.dirChroot, "donor", 'var'),
                        'ignore names':
                                        ["ignore name 01 with space in name",
                                           "ignore_name_02",
                                           "ignore_name_03"]
                    },
                },
                'hostname': '',
                'port': 22,
                'login': pwd.getpwuid(os.getuid()).pw_name,
                'ssh private key path': path(os.path.expanduser("~"),
                                            ".ssh",
                                            "fake_id_rsa"),
                'password': '123'
                }

        self.acceptorTS = { # Template Spec - Acceptor Test Data Template Specification (conf file whole subsection).
                'path': {
                    'acceptor': {
                        'path': path(self.dirChroot, "acceptor"),
                        'ignore names': []
                    }
                },
                'hostname': 'centos',
                'port': 22,
                'login': pwd.getpwuid(os.getuid()).pw_name,
                'ssh private key path': path(os.path.expanduser("~"),
                                            ".ssh",
                                            "fake_id_rsa"),
                'password': ''
                }

    def __setTestConfigDataObject(self):
        """
            Here is setup of structure corresponding to full configuration file.
            There are several independent and full sections of a conf. file.
        """
        assert self.donorTS
        assert self.acceptorTS

        localDonorSpec = copy.deepcopy(self.donorTS)
        remoteDonorSpec = copy.deepcopy(self.donorTS)
        localDonorSpec['hostname'] = ''
        remoteDonorSpec['hostname'] = 'centos2'

        localAcceptorSpec = copy.deepcopy(self.acceptorTS)
        remoteAcceptorSpec = copy.deepcopy(self.acceptorTS)
        localAcceptorSpec['hostname'] = ''
        remoteAcceptorSpec['hostname'] = 'centos2'


        self.configurationData = { # This dictionary is Python representation of configuration file. Keys from this dictionary are top level identifiers for test purpose configuration file.
            'donor': localDonorSpec,
            'acceptor': remoteAcceptorSpec,
            'pair-l2r_donor': localDonorSpec,
            'pair-l2r_acceptor': remoteAcceptorSpec,
            'pair-l2l_donor': localDonorSpec,
            'pair-l2l_acceptor': localAcceptorSpec,
            'pair-r2l_donor': remoteDonorSpec,
            'pair-r2l_acceptor': localAcceptorSpec,
            } # "r2l" acronym is "remote 2 local", and so on.


        # XXX - Set really existent path in this sync sequence. ???
        remoteDonorSpec['path']['opt']['path'] \
            = remoteAcceptorSpec['path']['acceptor']['path']
        remoteDonorSpec['path']['var']['path'] \
            = remoteAcceptorSpec['path']['acceptor']['path']
        self.configurationData['pair-r2l_donor'] = remoteDonorSpec
        self.configurationData['pair-r2l_acceptor'] = localAcceptorSpec

        return self.configurationData

    def __setDirectAccessVarsHeap(self):
        """
            Miscellaneous purpose variables. Usually they are used as shortcuts.
        """
        assert self.donorTS
        assert self.acceptorTS

        self.hostname = self.donorTS['hostname']
        self.port = self.donorTS['port']
        self.login = self.donorTS['login']
        self.sshPrivateKeyPath = self.donorTS['ssh private key path']
        self.password = self.donorTS['password']

        self.dirPathDonor = self.donorTS['path']['opt']['path']
        self.ignoreNamesPool = self.donorTS['path']['opt']['ignore names']

        self.dirPathAcceptor = self.acceptorTS['path']['acceptor']['path']


if __name__ == '__main__':
    pass
