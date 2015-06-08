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


if __name__ == '__main__':
    from TestData import TestData
    from TestHelpers import TestHelpers


###
##
#


class FilesSpec():
    def __init__(self, path = None, ignoreNamesPool = None):
        self.__path = path
        self.__ignoreNamesPool = ignoreNamesPool

    def getPath(self):
        return self.__path

    def getIgnorePool(self):
        return self.__ignoreNamesPool

###
##
#


def doTests():
    fileSpec = FilesSpec(td.dirPathDonor,td.ignoreNamesPool)
    assert fileSpec.getPath() == td.dirPathDonor
    assert fileSpec.getIgnorePool() == td.ignoreNamesPool


###
##
#


if __name__ == '__main__':
    td = TestData(helpersInstance = TestHelpers())
    doTests()
