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


Name:           files-sync
Version:        0.0
Release:        %( echo "0" )
Summary:        Files 'rsync' with predefined args and between remote and local nodes.

License:        GPL 3
URL:            http://github.com
Source0:        http://github.com/.../%{name}-%{version}.tar.gz

requires:       python python-argparse python-libs PyYAML python-crypto

BuildArch:      noarch

%global __os_install_post %{nil}

%description
This is a tool to wrap around 'rsync' between remote and local nodes. Arguments are passed via configuration files.

%prep
%setup -q

%build
%configure

%install
%make_install

%post
true

%preun
rm -rf /opt/%{name}

%files
/opt/%{name}

## There is 'changelog' section below. It's format is strict.
## New change log insertions can be done using command:
##    rpmdev-bumpspec --comment="Descriptive text." --userstring="A Name <a-name@github.com>" this.spec
#%changelog
#* Sun Apr 19 2015 A Name <a-name@github.com> 0.0-0
#- Package created.
