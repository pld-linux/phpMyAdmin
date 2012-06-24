Summary:	phpMyAdmin - web-based MySQL administration
Summary(pl):	phpMyAdmin - administracja bazami MySQL przez WWW
Name:		phpMyAdmin
Version:	2.2.5
Release:	1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://prdownloads.sourceforge.net/phpmyadmin/%{name}-%{version}-php.tar.bz2
URL:		http://sourceforge.net/projects/phpmyadmin/
Requires:	mysql
Requires:	php-mysql
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
  - zarz�dza� wieloma serwerami i pojedy�czymi bazami danych
  - eksportowa� i importowa� dane do warto�ci CSV
  - tworzy� i czyta� zrzuty tabel

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_myadmindir}/{lang,images,libraries,libraries/auth}

install *.php *.html badwords.txt $RPM_BUILD_ROOT%{_myadmindir}
install images/*.{gif,png} $RPM_BUILD_ROOT%{_myadmindir}/images
install lang/*.php $RPM_BUILD_ROOT%{_myadmindir}/lang
install libraries/*.{js,php} $RPM_BUILD_ROOT%{_myadmindir}/libraries
install libraries/auth/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/auth

gzip -9nf Documentation.txt ANNOUNCE.txt README TODO ChangeLog

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%dir %{_myadmindir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_myadmindir}/config.inc.php
%{_myadmindir}/d*.php
%{_myadmindir}/footer.inc.php
%{_myadmindir}/header.inc.php
%{_myadmindir}/index.php
%{_myadmindir}/l*.php
%{_myadmindir}/main.php
%{_myadmindir}/mult_submits.inc.php
%{_myadmindir}/phpinfo.php
%{_myadmindir}/read_dump.php
%{_myadmindir}/s*.php
%{_myadmindir}/tbl_*.php
%{_myadmindir}/user_details.php
%{_myadmindir}/badwords.txt

%{_myadmindir}/*.html
%{_myadmindir}/lang/*.php
%{_myadmindir}/images
%{_myadmindir}/libraries
