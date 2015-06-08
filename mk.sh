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


declare -r  shellCodeTrue=0
declare -r  shellCodeFalse=1

declare -r  thisDir="$( dirname "$( readlink -f "${0}" )" )"

declare -r  rpmName="files-sync"
declare -r  rpmVersion=0.0
declare -r  rpmRevision=0

declare -r  dirPrjTop="${thisDir}"
declare -r  dirRpmWorking="${dirPrjTop}/rpmbuild"
declare -r  subDirSrc="src"
declare -r  dirSrc="${dirPrjTop}/${subDirSrc}"
declare -r  dirOutput="${dirPrjTop}/output"
declare -r  testConfShortFileName="test.conf"

declare -r  fileSrcGZipShortName="${rpmName}-${rpmVersion}.tar.gz"

declare -r  dirInstall="${RPM_BUILD_ROOT}/opt/files-sync"

declare -ra srcFilesPool=( \
                "${subDirSrc}/ecdsa/*" \
                "${subDirSrc}/paramiko/*" \
                "${subDirSrc}/${mainAppExectutableShortName}" \
                "configure" \
                "Makefile" \
                "mk.sh" \
                "${rpmName}.spec" \
                "README" \
                "LICENSE" \
                )
declare -r  mainAppExectutableShortName="${rpmName}"

declare -rA installFilesToDirPool=( \
                ["README"]="${dirInstall}" \
                ["LICENSE"]="${dirInstall}" \
                ["${dirSrc}/ecdsa/*"]="${dirInstall}/ecdsa" \
                ["${dirSrc}/paramiko/*"]="${dirInstall}/paramiko" \
                ["${dirSrc}/syncwrap/*.py"]="${dirInstall}/syncwrap" \
                ["${dirSrc}/${mainAppExectutableShortName}"]="${dirInstall}" \
                )
declare -ra trashFilesPool=(\
                            "${dirSrc}/ecdsa/*.pyc" \
                            "${dirSrc}/paramiko/*.pyc" \
                            "${dirSrc}/syncwrap/*.pyc"\
                            "${dirSrc}/*.pyc"\
                            "${dirSrc}/__pycache__"\
                            "${dirSrc}/syncwrap/${testConfShortFileName}"\
                            "/tmp/${testConfShortFileName}"\
                            )

declare -ra rpmBuildTreeDirsPool=(\
                        "BUILD" \
                        "BUILDROOT" \
                        "RPMS" \
                        "SOURCES" \
                        "SPECS" \
                        "SRPMS")


###
##
#


function validatePathPool {
    local -ra pathPool=("${@}")
    local     path=""
    local     isPathValid=${shellCodeFalse}

    for path in "${pathPool[@]}" ; do
        if (! isPathWithSpaces "${path}") \
            && [ -n "${path}" ]
        then
            isPathValid=${shellCodeTrue}
        else
            isPathValid=${shellCodeFalse}
            break
        fi
    done

    if [ "${isPathValid}" == "${shellCodeTrue}" ] ; then
        return "${isPathValid}"
    else
        echo "ERROR:${0}:${LINENO}: Path '${path}' is not valid." >&2
        exit ${isPathValid}
    fi

}


function isPathWithSpaces {
    local -r path="${1}"
    local -r pathSpacesFiltered="${path%[[:space:]]*}"

    local isHaveSpace=${shellCodeTrue}

    if [ "${#path}" != "${#pathSpacesFiltered}" ] ; then
        isHaveSpace=${shellCodeTrue}
        echo "WARNING:${0}:${LINENO}: Path '${path}' have spaces." >&2
    else
        isHaveSpace=${shellCodeFalse}
    fi

    return ${isHaveSpace}
}


function fDefault {
    echo "INFO:${0}:${LINENO}: Nothing to be done here." >&2
}

function fCreateRpmbuildTree {
    for dirName in "${rpmBuildTreeDirsPool[@]}" ; do \
        mkdir -p "${dirRpmWorking}/${dirName}" ;\
    done
}

function fBuildRpm {
    cp \
        --force \
        "${dirPrjTop}/${rpmName}.spec" \
        "${dirRpmWorking}/SPECS"

    cp \
        --force \
        "${dirPrjTop}/${fileSrcGZipShortName}" \
        "${dirRpmWorking}/SOURCES/${fileSrcGZipShortName}"

    rpmbuild \
            --define "revisNum ${rpmRevision}" \
            --define "_topdir ${dirRpmWorking}" \
            -ba "${dirRpmWorking}/SPECS/${rpmName}.spec"

    set +x
    echo "There are RPMs, if any: "
    find "${dirRpmWorking}/RPMS" \
            -type f \
            -iname "*.rpm" \
                -o -iname "*.src.rpm"
    set -x
}


function fUnPackRPM {
    local fName=""
    local unZipDir=""

    while read fName ; do
        if [ -z "${fName}" ] ; then
            echo "WARNING:${0}:${LINENO}: There is no RPM files found in directory '${dirOutput}'." >&2
            exit ${shellCodeFalse}
        fi
        unZipDir="${dirOutput}/$( basename "${fName}" ).content"
        mkdir -p "${unZipDir}"
        cd "${unZipDir}"
        rpm2cpio "${fName}" | cpio -idmv
    done <<< "$( find "${dirOutput}" -iname "*.rpm" )"
}


function fSaveResults {
    mkdir -p "${dirOutput}"
    find "${dirRpmWorking}/RPMS" \
            "${dirRpmWorking}/SRPMS" \
                -type f \
                \( \
                    -iname "*.rpm" \
                    -o -iname "*.src.rpm" \
                \) \
                -exec cp "{}" "${dirOutput}" \;
    set +x
    echo -ne "\n\n"
    echo "See files at directory '${dirOutput}'"
    echo -ne "\n\n"
    set -x

}


function fPackSources {
    tar \
        --create \
        --gzip \
        --transform="s,^,${rpmName}-${rpmVersion}/," \
        --file="${fileSrcGZipShortName}" \
        ${srcFilesPool[@]} # tar ... --transform EXPRESSION ... - Use sed replace EXPRESSION to transform file.
}

function fTests {
    "${dirSrc}/tests-run.sh"
}

function fInstall {
    local   pathSpec=""

    install \
        --directory \
        --mode 755 \
        "${dirInstall}"

    for pathSpec in "${!installFilesToDirPool[@]}" ; do
        if [ -d "${pathSpec}" ] ; then
            install \
                --directory \
                --mode 755 \
                "${installFilesToDirPool["${pathSpec}"]}"
        else
            install \
                --directory \
                --mode 755 \
                "${installFilesToDirPool["${pathSpec}"]}"
            install \
                --verbose \
                -D \
                --mode 644 \
                ${pathSpec} \
                "${installFilesToDirPool["${pathSpec}"]}" # install ... -D ... - Create all leading components of DEST except the last, then copy SOURCE to DEST.
        fi
    done
    chmod 755 "${dirInstall}/${mainAppExectutableShortName}"
}


function fClean {
    rm -rf "${dirOutput}"
}


function fCleanSources {
    validatePathPool "${trashFilesPool[@]}"
    rm -rf ${trashFilesPool[@]}
}


function fCleanBuildArea {
    rm -rf "${dirRpmWorking}"/*
}


###
##
#


for cliArg in "${@}" ; do
    option="${cliArg%%=*}"
    value="${cliArg#*=}"
    case "${option}" in
        --default)
            fDefault
        ;;
        --create-rpmbuild-tree)
            fCreateRpmbuildTree
        ;;
        --build-rpm)
            fBuildRpm
        ;;
        --unpack-rpm)
            fUnPackRPM
        ;;
        --save-results)
            fSaveResults
        ;;
        --pack-sources)
            fPackSources
        ;;
        --tests)
            fTests
        ;;
        --install)
            fInstall
        ;;
        --clean)
            fClean
        ;;
        --clean-sources)
            fCleanSources
        ;;
        --clean-build-area)
            fCleanBuildArea
        ;;
        *)
            echo "ERROR:${0}:${LINENO}: Unknow CLI option '${cliArg}'." >&2
            exit ${shellCodeFalse}
        ;;
    esac
done


set +x
echo -ne "\n\n"
echo "INFO:${0}:${LINENO}: Job done." >&2
echo -ne "\n"
