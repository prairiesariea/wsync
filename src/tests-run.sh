#!/bin/bash

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


PS4="+:\${0}:\${LINENO}: "
set -x
set -e

declare -r thisDir="$( dirname "${0}" )"

declare -r testDirTop="/tmp/RSyncTests"
declare -r hostsInvolved=("centos" "centos2")
declare -r sshKey="${HOME}/.ssh/fake_id_rsa"

declare -r syncWrapLibLocation="${thisDir}/syncwrap"
declare -r exampleAutoGenConfFile="${thisDir}/../tmp/test-auto-generated.conf"

export PYTHONDONTWRITEBYTECODE="true"

declare -r  pythonExe="python2"

declare -ra testTargets=(\
                    "${syncWrapLibLocation}/TestHelpers.py" \
                    "${syncWrapLibLocation}/Area.py" \
                    "${syncWrapLibLocation}/FilesSpec.py" \
                    "${syncWrapLibLocation}/NodeSpec.py" \
                    "${syncWrapLibLocation}/AreaConn.py" \
                    "${syncWrapLibLocation}/RSync.py" \
                    )


###
##
#


function cleanTestArea {
    local host=""

    rm -rf '${testDirTop}'
    for host in "${hostsInvolved[@]}" ; do
        ssh -i "${sshKey}" "${USER}@${host}" "rm -rf '${testDirTop}'"
    done
}


###
##
#


cleanTestArea
for fName in "${testTargets[@]}" ; do
    "${pythonExe}" "${fName}"
done


"${thisDir}/files-sync" --create-example-conf "${exampleAutoGenConfFile}"
"${thisDir}/files-sync" --conf "${exampleAutoGenConfFile}"


set +x
echo -ne "\n"
echo "INFO:${0}:${LINENO}: Job done."
