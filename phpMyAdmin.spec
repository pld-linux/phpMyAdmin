Summary:	phpMyAdmin - web-based MySQL administration
Summary(pl):	phpMyAdmin - administracja bazami MySQL przez WWW
Name:		phpMyAdmin
# NOTE: bump _rel with every new patchlevel
Version:	2.6.1
Release:	2
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/phpmyadmin/%{name}-%{version}.tar.bz2
# Source0-md5:	eaa23b48760f2b31a8725bf85b0acecd
Source1:	%{name}.conf
Patch0:		%{name}-config.patch
URL:		http://www.phpmyadmin.net/
#Requires:	mysql
Requires(postun):	perl-base
Requires:	php-mysql
Requires:	php-pcre
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_myadmindir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

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
%setup -q
%patch -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_myadmindir}/{css,lang,libraries/{auth,export,dbg,dbi,transformations}} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

install *.php *.html *.css $RPM_BUILD_ROOT%{_myadmindir}
#install images/*.{gif,png} $RPM_BUILD_ROOT%{_myadmindir}/images
install lang/*.php $RPM_BUILD_ROOT%{_myadmindir}/lang
cp -rf themes  $RPM_BUILD_ROOT%{_myadmindir}/
install css/* $RPM_BUILD_ROOT%{_myadmindir}/css
install libraries/*.{js,php} $RPM_BUILD_ROOT%{_myadmindir}/libraries
install libraries/auth/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/auth
install libraries/export/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/export
install libraries/dbg/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/dbg
install libraries/dbi/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/dbi
install libraries/transformations/*.php $RPM_BUILD_ROOT%{_myadmindir}/libraries/transformations

cp -rf scripts $RPM_BUILD_ROOT%{_myadmindir}

install config.inc.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.inc.php $RPM_BUILD_ROOT%{_myadmindir}/config.inc.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
	    /usr/sbin/apachectl restart 1>&2
	fi
fi

%triggerpostun -- phpMyAdmin <= 2.5.3-2
if [ -f /home/services/httpd/html/myadmin/config.inc.php.rpmsave ]; then
	mv -f /home/services/httpd/html/myadmin/config.inc.php.rpmsave /etc/phpMyAdmin/config.inc.php
else
	if [ -f /home/httpd/html/myadmin/config.inc.php.rpmsave ]; then
		mv -f /home/httpd/html/myadmin/config.inc.php.rpmsave /etc/phpMyAdmin/config.inc.php
	fi
fi
for i in `grep -lr "/home/\(services/\)*httpd/html/myadmin" /etc/httpd/*`; do
	cp $i $i.backup
	%{__perl} -pi -e "s#/home/httpd/html/myadmin#%{_myadmindir}#g" $i
	%{__perl} -pi -e "s#/home/services/httpd/html/myadmin#%{_myadmindir}#g" $i
	echo "File changed by trigger: $i (backup: $i.backup)"
done
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%files
%defattr(644,root,root,755)
%doc Documentation.* CREDITS ChangeLog INSTALL README TODO translators.html scripts
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%dir %{_myadmindir}
%{_myadmindir}/css
%{_myadmindir}/themes
%{_myadmindir}/scripts
%{_myadmindir}/lang
%{_myadmindir}/libraries
%{_myadmindir}/*.css
%{_myadmindir}/*.html
%{_myadmindir}/*.php
