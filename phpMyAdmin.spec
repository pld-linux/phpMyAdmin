# TODO
# - add codepress (http://codepress.org/index.php) patch
Summary:	phpMyAdmin - web-based MySQL administration
Summary(pl.UTF-8):	phpMyAdmin - administracja bazami MySQL przez WWW
Name:		phpMyAdmin
Version:	3.1.2
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phpmyadmin/%{name}-%{version}-all-languages.tar.bz2
# Source0-md5:	cb6a6db5d684f94e71f864071b5b0d7a
Source1:	%{name}.conf
Source2:	%{name}-lighttpd.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-ServerSelectDisplayName.patch
Patch2:		%{name}-ServerSelectDisplayName-config.patch
URL:		http://www.phpmyadmin.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	php-common >= 4:5.2
Requires:	php-ctype
Requires:	php-mbstring
Requires:	php-mcrypt
Requires:	php-mysql
Requires:	php-pcre
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
Suggests:	php-mysqli
Suggests:	webserver(indexfile)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

%description
phpMyAdmin can administer a whole MySQL-server (needs a super-user)
but also a single database. To accomplish the latter you'll need a
properly set up MySQL-user who can read/write only the desired
database. It's up to you to look up the appropiate part in the MySQL
manual. Currently phpMyAdmin can:
- create and drop databases
- create, copy, drop and alter tables
- delete, edit and add fields
- execute any SQL-statement, even batch-queries
- manage keys on fields
- load text files into tables
- create (*) and read dumps of tables
- export (*) and import data to CSV values
- administer multiple servers and single databases
- check referencial integrity
- create complex queries automatically connecting required tables
- create PDF graphics of your database layout
- communicate in more than 50 different languages

%description -l pl.UTF-8
phpMyAdmin potrafi zarządzać całymi bazami MySQL (potrzebne
uprawnienia superużytkownika) jak i pojedynczymi bazami danych.
Potrzebny jest użytkownik, który ma prawa zapisu/odczytu tylko tych
baz, którymi chcemy administrować (więcej informacji w odpowiedniej
podręcznika MySQL). Aktualnie phpMyAdmin potrafi:
- tworzyć i usuwać bazy
- wykonywać create, copy, drop oraz alter na tabelach
- dodawać, usuwać i modyfikować pola
- wykonywać dowolne zapytania SQL
- zarządzać kluczami na rekordach
- wczytywać tekst z plików do tabel
- obsługiwać ponad 20 języków
- zarządzać wieloma serwerami i pojedynczymi bazami danych
- eksportować i importować dane do wartości CSV
- tworzyć i czytać zrzuty tabel

%prep
%setup -q -n %{name}-%{version}-all-languages
%patch0 -p1
%patch1 -p0
%patch2 -p0

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}/{js,lang,libraries/{auth/swekey,dbg,dbi,engines,export,tcpdf/font,import,transformations}}}

install *.php *.html *.css $RPM_BUILD_ROOT%{_appdir}
install lang/*.php $RPM_BUILD_ROOT%{_appdir}/lang
cp -rf pmd $RPM_BUILD_ROOT%{_appdir}
cp -rf themes $RPM_BUILD_ROOT%{_appdir}
cp -rf js $RPM_BUILD_ROOT%{_appdir}
install libraries/*.php $RPM_BUILD_ROOT%{_appdir}/libraries
install libraries/auth/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/auth
install libraries/auth/swekey/*.{php,crt} $RPM_BUILD_ROOT%{_appdir}/libraries/auth/swekey
install libraries/dbg/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/dbg
install libraries/dbi/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/dbi
install libraries/engines/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/engines
install libraries/export/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/export
install libraries/import/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/import
install libraries/tcpdf/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/tcpdf
install libraries/tcpdf/font/*.{php,z} $RPM_BUILD_ROOT%{_appdir}/libraries/tcpdf/font
install libraries/transformations/*.php $RPM_BUILD_ROOT%{_appdir}/libraries/transformations

install libraries/config.default.php $RPM_BUILD_ROOT%{_sysconfdir}/config.inc.php
ln -sf %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

cp -f libraries/import/README{,-import}
cp -f libraries/transformations/README{,-transformations}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc Documentation.* CREDITS ChangeLog INSTALL README TODO translators.html scripts libraries/import/README-import libraries/transformations/README-transformations libraries/transformations/TEMPLATE* libraries/transformations/*.sh lang/*.sh
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%dir %{_appdir}
%{_appdir}/js
%{_appdir}/lang
%{_appdir}/libraries
%{_appdir}/pmd
%{_appdir}/themes
%{_appdir}/*.css
%{_appdir}/*.html
%{_appdir}/*.php
