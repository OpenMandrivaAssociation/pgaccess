%define name pgaccess
%define srcver 0_99_0_20040219
%define version %( echo %srcver | sed 's/_/./g')
%define release %mkrel 4

Summary: A tcl/tk client for postgresql
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{srcver}.tar.bz2
Source20: pgaccess-16.png
Source21: pgaccess-32.png
Source22: pgaccess-48.png
License: GPL
Group: Databases
Url: http://pgfoundry.org/projects/pgaccess/
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: tk >= 8.0
Requires: tcl >= 8.0
Requires: tcl-tcllib
BuildArch: noarch

%description
A free graphical database management tool for PostgreSQL.
PgAccess has been written by Constantin Teodorescu using Visual Tcl, 
the best tool for developing Tcl/Tk applications I've ever seen.

%prep
%setup -q -n %{name}-%{srcver}

rm -fr win32

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%name
mkdir -p $RPM_BUILD_ROOT{%{_miconsdir},%{_iconsdir},%{_liconsdir}}
mkdir -p $RPM_BUILD_ROOT%_menudir

perl -pi -e 's|/usr/local|%{_datadir}|' pgaccess

cat <<EOF >$RPM_BUILD_ROOT%{_bindir}/pgaccess
#!/bin/sh
export PGACCESS_HOME="/usr/share/pgaccess"

\$PGACCESS_HOME/pgaccess.tcl $* &
EOF

#mv pgaccess.tcl $RPM_BUILD_ROOT%{_bindir}/pgaccess

cp -vfr * $RPM_BUILD_ROOT%{_datadir}/%name
rm -fr $RPM_BUILD_ROOT%{_datadir}/%name/doc

mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat <<EOF >$RPM_BUILD_ROOT%{_menudir}/%name
?package(%name):\
needs="x11"\
section="More Applications/Databases"\
longtitle="PostgreSQL Tcl/Tk front-end"\
title="PostgreSQL Access"\
icon="pgaccess.png"\
command="pgaccess" \
xdg="true"
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=PostgreSQL Access
Comment=PostgreSQL Tcl/Tk front-end
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=DATABASE;X-MandrivaLinux-MoreApplications-Databases
EOF

install -D -m644 %{SOURCE20} $RPM_BUILD_ROOT%{_miconsdir}/pgaccess.png
install -D -m644 %{SOURCE21} $RPM_BUILD_ROOT%{_iconsdir}/pgaccess.png
install -D -m644 %{SOURCE22} $RPM_BUILD_ROOT%{_liconsdir}/pgaccess.png

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc doc/ README
%attr(755,root,root) %{_bindir}/%name
%dir %{_datadir}/%name
%{_datadir}/%name/*
%_menudir/%name
%{_datadir}/applications/mandriva-%{name}.desktop
%_miconsdir/%name.png
%_iconsdir/%name.png
%_liconsdir/%name.png



