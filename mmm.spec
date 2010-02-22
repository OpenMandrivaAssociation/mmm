%define name mmm
%define version 0.43
%define release %mkrel 2

Summary: MMM Mirror Manager
Name: %{name}
Version: %{version}
Release: %{release}
License: GPL
Group: Networking/WWW
Url: http://mmm.zarb.org/
Source0: %{name}-%{version}.tar.gz
Requires: rsync
BuildRequires: rsync
BuildRequires: perl(CGI)
BuildRequires: perl(Config::IniFiles)
BuildRequires: perl(Digest::MD5) 
BuildRequires: perl(File::Temp)
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Sys::Hostname)
BuildRequires: perl(IO::Select)
BuildRequires: perl(URI)
BuildRequires: perl(XML::Simple)
BuildRequires: perl-XML-Parser
BuildRequires: perl(Net::DNS)
BuildRequires: perl(Date::Calc)
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
MMM is a tool to easilly manage multiple mirroring process using a predefined 
mirror list.

It support: 
 - per tree delay between two sync process,
 - automatic mirror switch in case of failure,
 - mirror status report.

%package cgi
Group: Networking
Summary: MMM cgi report
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
Requires: %name = %version-%release

%description cgi
MMM is a tool to easilly manage multiple mirroring process using a predefined 
mirror list.

%prep
%setup -q

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor --sysconfir=%_sysconfig --localstadir=%_var/lib
%make

perl -pi -e 's:^statedir.*=.*:statedir = /var/spool/mmm:' config/mmm.cfg 

%check
%make test

%install
rm -rf %{buildroot}
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

mkdir -p %buildroot/var/lib/%name

mkdir -p %buildroot/%_sysconfdir/init.d
install -m 755 init.d/mmmd %buildroot/%_sysconfdir/init.d/mmmd

%clean
rm -rf %{buildroot}

%post cgi
%if %mdkversion < 201010
%_post_webapp
%endif

%postun cgi
%if %mdkversion < 201010
%_postun_webapp
%endif

%files
%defattr(-,root,root)
%doc examples www/index.html
%config(noreplace) %_sysconfdir/%name
%_bindir/*
%{perl_vendorlib}/*
%{_mandir}/*/*
%dir /var/lib/%name
%_sysconfdir/init.d/mmmd

%files cgi
%defattr(-,root,root)
%config(noreplace) %{_webappconfdir}/%{name}.conf
/var/www/cgi-bin/mmm_status

