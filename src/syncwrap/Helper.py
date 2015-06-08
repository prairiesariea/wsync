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

import inspect
import sys
import os
import re

class Helper:
    def lineno(self):
        return inspect.currentframe().f_back.f_lineno

    @staticmethod
    def os_path_relpath(*tArgs, **dArgs):
        relativePath = os.path.relpath(*tArgs, **dArgs)

        pivotPythonVersion = (2,7)
        thisPythonVersion = (sys.version_info[0],sys.version_info[1])

        if thisPythonVersion[0] <= pivotPythonVersion[0] \
                and thisPythonVersion[1] < pivotPythonVersion[1]:
            sys.stderr.write("WARNING:%s:%s: " % (__file__, Helper().lineno())
                                + "Running with this Python version %s" \
                                    % str(sys.version_info)
                                + " is deprecated.\n")

            relativePath = re.sub('^(\.\./)*', '', relativePath)
            #relativePath = relativePath.replace('../', '')

        return relativePath

###
##
#


if __name__ == '__main__':
    pass
