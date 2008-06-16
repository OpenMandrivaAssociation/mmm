%define name mmm
%define version 0.02
%define release %mkrel 2

Summary: MMM Mirror Manager
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
License: GPL
Group: Networking
Url: http://mmm.zarb.org/
BuildRoot: %{_tmppath}/%{name}-buildroot
Requires: rsync
BuildRequires:    rpm-helper >= 0.16
BuildArch: noarch
BuildRequires: rsync perl(CGI) perl(Config::IniFiles) perl(Digest::MD5) 
BuildRequires: perl(File::Temp) perl(Getopt::Long) perl(HTTP::Request)
BuildRequires: perl(IO::Select) perl(LWP::UserAgent) perl(Sys::Hostname)
BuildRequires: perl(URI) perl(XML::Simple) perl-XML-Parser

%description
MMM is a tool to easilly manage multiple mirroring process using a predefined 
mirror list.

It support: 
 - per tree delay between two sync process,
 - automatic mirror switch in case of failure,
 - mirror status report.

%package cgi
Group: Networking
Requires(post):   rpm-helper >= 0.16
Requires(postun): rpm-helper >= 0.16
Summary: MMM cgi report
Requires: %name = %version-%release

%description cgi
MMM is a tool to easilly manage multiple mirroring process using a predefined 
mirror list.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%make

perl -pi -e 's:^mirrordir.*=.*:mirrordir = %_sysconfdir/%name/mirrorlist:' config/mmm.cfg 
perl -pi -e 's:^statedir.*=.*:statedir = /var/spool/mmm:' config/mmm.cfg 

%check
%make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# apache configuration
install -d -m 755 %{buildroot}%{_webappconfdir}
cat > %{buildroot}%{_webappconfdir}/%{name}.conf <<EOF
ScriptAlias /mmm /var/www/cgi-bin/mmm_status

<Location "/mmm">
        SetEnv MMM_CONFIG %_sysconfdir/mmm/mmm.cfg
</Location>
EOF

mkdir -p %{buildroot}/var/www/cgi-bin
install -m 755 bin/mmm_status %{buildroot}/var/www/cgi-bin/mmm_status

mkdir -p %buildroot%_sysconfdir/%name
mkdir -p %buildroot%_sysconfdir/%name/mirrorlist
cp -a -f config/mmm.cfg %buildroot%_sysconfdir/%name/mmm.cfg

mkdir -p %buildroot/var/spool/%name

%clean
rm -rf $RPM_BUILD_ROOT

%post cgi
%_post_webapp

%postun cgi
%_postun_webapp

%files
%defattr(-,root,root)
%doc examples www/index.html
%config(noreplace) %_sysconfdir/%name
%_bindir/*
%{perl_vendorlib}/*
%{_mandir}/*/*
%dir /var/spool/%name

%files cgi
%defattr(-,root,root)
%config(noreplace) %{_webappconfdir}/%{name}.conf
/var/www/cgi-bin/mmm_status


