
%define		_rc	rc1
Summary:	phpMyAdmin - web-based MySQL administration
Summary(pl):	phpMyAdmin - administracja bazami MySQL przez WWW
Name:		phpMyAdmin
Version:	2.5.2
Release:	0.%{_rc}.4
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phpmyadmin/%{name}-%{version}-%{_rc}-php.tar.bz2
# Source0-md5:	f6a0ef4c6ed1f61390b270f0fcd024e1
Patch0:		%{name}-config.patch
URL:		http://www.phpmyadmin.net/
BuildRequires:	rpm-php-pearprov
#Requires:	mysql
Requires:	php-mysql
Requires:	php
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
phpMyAdmin potrafi zarz±dzaæ ca³ymi bazami MySQL (potrzebne
uprawnienia super-user'a) jak i pojedynczymi bazami danych. Bêdziesz
potrzebowa³ u¿ytkownika, który ma prawa zapisu/odczytu tylko tych baz,
którymi chcesz administrowaæ (zajrzyj do odpowiedniej czê¶ci manual'a
MySQL). Aktualnie phpMyAdmin potrafi:
  - tworzyæ i usuwaæ bazy
  - create, copy, drop oraz alter na tabelach
  - dodawaæ, usuwaæ i edytowaæ pola
  - wykonywaæ dowolne zapytania SQL
  - zarz±dzaæ kluczami na rekordach
  - wczytywaæ tekst z plików do tabel
  - obs³ugiwaæ ponad 20 jêzyków
  - zarz±dzaæ wieloma serwerami i pojedyñczymi bazami danych
  - eksportowaæ i importowaæ dane do warto¶ci CSV
  - tworzyæ i czytaæ zrzuty tabel

%prep
%setup -q -n %{name}-%{version}-%{_rc}
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_myadmindir}/{css,lang,images,libraries/{auth,export}}

install *.php *.html *.css badwords.txt $RPM_BUILD_ROOT%{_myadmindir}
install images/*.{gif,png} $RPM_BUILD_ROOT%{_myadmindir}/images
install lang/*.php $RPM_BUILD_ROOT%{_myadmindir}/lang
install css/* $RPM_BUILD_ROOT%{_myadmindir}/css
install libraries/*.{js,php} $RPM_BUILD_ROOT%{_myadmindir}/libraries
install libraries/auth/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/auth
install libraries/export/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/export

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Documentation.txt ANNOUNCE.txt README TODO ChangeLog
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_myadmindir}/config.inc.php
%dir %{_myadmindir}
%{_myadmindir}/css
%{_myadmindir}/images
%{_myadmindir}/lang
%{_myadmindir}/libraries
%{_myadmindir}/badwords.txt
%{_myadmindir}/*.css
%{_myadmindir}/*.html
%{_myadmindir}/[!c]*.php
%{_myadmindir}/c[!o]*.php
