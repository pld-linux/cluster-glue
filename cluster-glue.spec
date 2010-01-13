
%define		subver	rc2
%define		rel		0.1
Summary:	Reusable cluster components
Name:		cluster-glue
Version:	1.0.2
Release:	0.%{subver}.%{rel}
License:	GPLv2+ and LGPLv2+
Group:		Base
URL:		http://www.clusterlabs.org
Source0:	http://www.linux-ha.org/w/images/3/3d/Cluster-glue-%{version}-%{subver}.tar.bz2
# Source0-md5:	1f83b6bd83d9cae5310c32d14fecf2fd
BuildRequires:	OpenIPMI-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
#BuildRequires:	docbook-dtds
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel
BuildRequires:	libltdl-devel
BuildRequires:	libnet-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt
BuildRequires:	net-snmp-devel >= 5.4
BuildRequires:	openhpi-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	which
Requires:	perl-TimeDate
# Directives to allow upgrade from combined heartbeat packages
Provides:	heartbeat-pils = 3.0.0-1
Provides:	heartbeat-stonith = 3.0.0-1
Obsoletes:	heartbeat-common
Obsoletes:	heartbeat-pils < 3.0.0-1
Obsoletes:	heartbeat-stonith < 3.0.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A collection of common tools that are useful for writing cluster
managers such as Pacemaker. Provides a local resource manager that
understands the OCF and LSB standards, and an interface to common
STONITH devices.

%package libs
Summary:	Reusable cluster libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libheartbeat2

%description libs
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%package libs-devel
Summary:	Headers and libraries for writing cluster managers
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	libheartbeat-devel

%description libs-devel
Headers and shared libraries for a useful for writing cluster managers
such as Pacemaker.

%prep
%setup -q -n %{name}-%{version}-%{subver}

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%{__make}
%configure \
	--enable-fatal-warnings=yes \
	--with-daemon-group=haclient \
	--with-daemon-user=hacluster\
	--docdir=%{_docdir}/%{name}-%{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

## tree fix up
# Dont package static libs
find $RPM_BUILD_ROOT -name '*.a' -exec rm {} \;
find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
