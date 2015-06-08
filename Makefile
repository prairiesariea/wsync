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


makeWrapperExePath="$(abspath $(dir $(lastword $(MAKEFILE_LIST))))/mk.sh"

default:
	bash "${makeWrapperExePath}" --default

create-rpmbuild-tree:
	bash "${makeWrapperExePath}" --create-rpmbuild-tree

build-rpm: create-rpmbuild-tree pack-sources
	bash "${makeWrapperExePath}" --build-rpm

unpack-rpm:
	bash "${makeWrapperExePath}" --unpack-rpm

save-results:
	bash "${makeWrapperExePath}" --save-results

pack-sources:
	bash "${makeWrapperExePath}" --pack-sources

tests:
	bash "${makeWrapperExePath}" --tests

install:
	bash "${makeWrapperExePath}" --install

clean: clean-sources clean-build-area
	bash "${makeWrapperExePath}" --clean

clean-sources:
	bash "${makeWrapperExePath}" --clean-sources

clean-build-area:
	bash "${makeWrapperExePath}" --clean-build-area
