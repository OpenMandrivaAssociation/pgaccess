Summary:	A Tcl/Tk client for postgresql
Name:		pgaccess
# Just a CVS snapshot, versioning is historical
Version:	0.99.0.20081028
Release:	%{mkrel 9}
Source0:	%{name}-%{version}.tar.lzma
Source20:	pgaccess-16.png
Source21:	pgaccess-32.png
Source22:	pgaccess-48.png
License:	GPL
Group:		Databases
URL:		http://pgfoundry.org/projects/pgaccess/
BuildRoot:	%{_tmppath}/%{name}-buildroot
# For the macros
BuildRequires:	tcl-devel
Requires:	tk >= 8.0
Requires:	tcl >= 8.0
Requires:	tcl-tcllib
BuildArch:	noarch

%description
Graphical database management tool for PostgreSQL.

%prep
%setup -q -n %{name}
sed -i -e 's,list frame none underline,list dotbox none underline,g' lib/widgets/tablelist3.8/scripts/tablelistWidget.tcl
rm -rf op_sys

%build

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{tcl_sitelib}/%{name}

perl -pi -e 's|/usr/local|%{tcl_sitelib}|' pgaccess

cat <<EOF >%{buildroot}%{_bindir}/pgaccess
#!/bin/sh
export PGACCESS_HOME="/usr/share/tcl%{tcl_version}/pgaccess"

\$PGACCESS_HOME/pgaccess.tcl $* &
EOF

cp -vfr * %{buildroot}%{tcl_sitelib}/%{name}
rm -fr %{buildroot}%{tcl_sitelib}/%{name}/doc

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=PostgreSQL Access
Comment=PostgreSQL Tcl/Tk front-end
Exec=%{_bindir}/%{name} 
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Development;Database;
EOF

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -D -m644 %{SOURCE20} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/pgaccess.png
install -D -m644 %{SOURCE21} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/pgaccess.png
install -D -m644 %{SOURCE22} %{buildroot}%{_iconsdir}/hicolor/48x48/apps/pgaccess.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/ README
%attr(755,root,root) %{_bindir}/%{name}
%{tcl_sitelib}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/pgaccess.png

