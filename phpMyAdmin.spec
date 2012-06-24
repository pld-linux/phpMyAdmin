Summary:	phpMyAdmin - web-based mysql administration
Summary(pl):	phpMyAdmin - administracja bazami mysql przez WWW
Name:		phpMyAdmin
Version:	2.2.0
Release:	1
License:	GPL
Group:		Applications/Databases/Interfaces
Group(de):	Applikationen/Dateibanken/Schnittstellen
Group(pl):	Aplikacje/Bazy danych/Interfejsy
Source0:	http://prdownloads.sourceforge.net/phpmyadmin/%{name}-%{version}-php.tar.bz2
Url:		http://sourceforge.net/projects/phpmyadmin/
Requires:	mysql
Requires:	php >= 4
Requires:	webserver
Buildarch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_myadmindir	/home/httpd/html/myadmin

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
  - communicate in more than 20 different languages

%description -l pl
phpMyAdmin potrafi zarz�dza� ca�ymi bazami MySQL (potrzebne
uprawnienia super-user'a) jak i pojedynczymi bazami danych. B�dziesz
potrzebowa� u�ytkownika, kt�ry ma prawa zapisu/odczytu tylko tych baz,
kt�rymi chcesz administrowa� (zajrzyj do odpowiedniej cz�ci manual'a
MySQL). Aktualnie phpMyAdmin potrafi:
  - tworzy� i usuwa� bazy
  - create, copy, drop oraz alter na tabelach
  - dodawa�, usuwa� i edytowa� pola
  - wykonywa� dowolne zapytania SQL
  - zarz�dza� kluczami na rekordach
  - wczytywa� tekst z plik�w do tabel
  - obs�ugiwa� ponad 20 j�zyk�w
  - zarz�dza� wieloma serverami i pojedy�czymi bazami danych
  - eksportowa� i importowa� dane do warto�ci CSV
  - tworzy� i czyta� zrzuty tabel


%prep
%setup -q 
%build

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_myadmindir}/{lang,images}

cp *.php $RPM_BUILD_ROOT%{_myadmindir}
cp *.js $RPM_BUILD_ROOT%{_myadmindir}
cp *.html $RPM_BUILD_ROOT%{_myadmindir}
cp images/*.gif $RPM_BUILD_ROOT%{_myadmindir}/images
cp lang/*.php $RPM_BUILD_ROOT%{_myadmindir}/lang

gzip -9nf Documentation.txt ANNOUNCE.txt README TODO ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %attr(755,http,http) %{_myadmindir}
%attr(640,http,http) %config(noreplace) %{_myadmindir}/config.inc.php
%attr(644,http,http) %{_myadmindir}/d*.php
%attr(644,http,http) %{_myadmindir}/footer.inc.php
%attr(644,http,http) %{_myadmindir}/grab_globals.inc.php
%attr(644,http,http) %{_myadmindir}/header.inc.php
%attr(644,http,http) %{_myadmindir}/index.php
%attr(644,http,http) %{_myadmindir}/l*.php
%attr(644,http,http) %{_myadmindir}/main.php
%attr(644,http,http) %{_myadmindir}/ob_lib.inc.php
%attr(644,http,http) %{_myadmindir}/phpinfo.php
%attr(644,http,http) %{_myadmindir}/s*.php
%attr(644,http,http) %{_myadmindir}/tbl_*.php
%attr(644,http,http) %{_myadmindir}/user_details.php

%attr(644,http,http) %{_myadmindir}/*.js
%attr(644,http,http) %{_myadmindir}/*.html
%attr(644,http,http) %{_myadmindir}/lang/*.php
%attr(644,http,http) %{_myadmindir}/images/*.gif
