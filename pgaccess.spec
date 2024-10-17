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
URL:		https://pgfoundry.org/projects/pgaccess/
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



%changelog
* Mon Sep 14 2009 Thierry Vignaud <tvignaud@mandriva.com> 0.99.0.20081028-9mdv2010.0
+ Revision: 440813
- rebuild

* Fri Dec 05 2008 Adam Williamson <awilliamson@mandriva.org> 0.99.0.20081028-8mdv2009.1
+ Revision: 310411
- buildrequires tcl-devel (for the macros)
- fix categories in menu file
- fd.o icons
- move to new location per policy
- fix a bug in tablelistWidget.tcl that causes app not to run, found this fix
  elsewhere but I forget where
- less hyperbolic description
- clean spec (macros, tabs etc)
- new CVS snapshot

* Fri Aug 01 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.99.0.20040219-7mdv2009.0
+ Revision: 258930
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.99.0.20040219-6mdv2009.0
+ Revision: 246851
- rebuild
- drop old menu

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.99.0.20040219-4mdv2008.1
+ Revision: 136373
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's error: string list key "Categories" in group "Desktop Entry" does not have a semicolon (";") as trailing character


* Sat Jan 13 2007 Olivier Thauvin <nanardon@mandriva.org> 0.99.0.20040219-4mdv2007.0
+ Revision: 108354
- fix dep (#28175)

* Tue Aug 08 2006 Olivier Thauvin <nanardon@mandriva.org> 0.99.0.20040219-3mdv2007.0
+ Revision: 54184
- xdg menu
- Import pgaccess

* Mon May 01 2006 Olivier Thauvin <nanardon@mandriva.org> 0.99.0.20040219-2mdk
- Birthday rebuild

* Tue Apr 19 2005 Olivier Thauvin <nanardon@mandrake.org> 0.99.0.20040219-1mdk
- 0.99.0.20040219
- remove buggy requires
- update url

* Fri Dec 24 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 0.98.8.20030520-2mdk
- Birthday rebuild

