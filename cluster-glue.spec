# TODO
# - filterout fix needed:
#   ./.libs/ipmilan.so: undefined reference to `stonith_free_hostlist'
#   ./.libs/ipmilan.so: undefined reference to `PILCallLog'
#   collect2: ld returned 1 exit status
#   gmake[4]: *** [ipmilantest] Error 1
#   gmake[4]: Leaving directory `/home/users/glen/rpm/BUILD.x86_64-linux/cluster-glue-1.0.2-rc2/lib/plugins/stonith'
# - pld deps for "docbook-dtds"
# - tests packaged in -devel to own pkg or just rm -rf
%define		subver	rc2
%define		rel		0.1
Summary:	Reusable cluster components
Name:		cluster-glue
Version:	1.0.2
Release:	0.%{subver}.%{rel}
License:	GPL v2+ and LGPL v2+
Group:		Base
URL:		http://www.clusterlabs.org/
Source0:	http://www.linux-ha.org/w/images/3/3d/Cluster-glue-%{version}-%{subver}.tar.bz2
# Source0-md5:	1f83b6bd83d9cae5310c32d14fecf2fd
BuildRequires:	OpenIPMI-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
BuildRequires:	docbook-dtd44-xml
#BuildRequires:	docbook-dtds
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel
BuildRequires:	libltdl-devel
BuildRequires:	libnet-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel >= 5.4
BuildRequires:	openhpi-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	which
Requires:	perl-TimeDate
# Directives to allow upgrade from combined heartbeat packages
Provides:	heartbeat-pils = 3.0.0-1
Provides:	heartbeat-stonith = 3.0.0-1
Obsoletes:	heartbeat-common
Obsoletes:	heartbeat-pils < 3.0.0-1
Obsoletes:	heartbeat-stonith < 3.0.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_ld	-Wl,--as-needed

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
%configure \
	--with-initdir=/etc/rc.d/init.d \
	--enable-fatal-warnings=yes \
	--with-daemon-group=haclient \
	--with-daemon-user=hacluster\
	--docdir=%{_docdir}/%{name}-%{version} \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -delete

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS logd/logd.cf doc/stonith/README*
%attr(754,root,root) /etc/rc.d/init.d/logd

%attr(755,root,root) %{_sbindir}/ha_logger
%attr(755,root,root) %{_sbindir}/hb_report
%attr(755,root,root) %{_sbindir}/lrmadmin
%attr(755,root,root) %{_sbindir}/meatclient
%attr(755,root,root) %{_sbindir}/stonith
%attr(755,root,root) %{_sbindir}/sbd
%{_mandir}/man1/ha_logger.1*
%{_mandir}/man8/ha_logd.8*
%{_mandir}/man8/hb_report.8*
%{_mandir}/man8/meatclient.8*
%{_mandir}/man8/stonith.8*

%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/ha_cf_support.sh
%attr(755,root,root) %{_datadir}/%{name}/openais_conf_support.sh
%attr(755,root,root) %{_datadir}/%{name}/utillib.sh
%attr(755,root,root) %{_datadir}/%{name}/combine-logs.pl
%attr(755,root,root) %{_datadir}/%{name}/ha_log.sh

%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%dir %{_libdir}/heartbeat/plugins/RAExec
%dir %{_libdir}/heartbeat/plugins/InterfaceMgr
%attr(755,root,root) %{_libdir}/heartbeat/lrmd
%attr(755,root,root) %{_libdir}/heartbeat/ha_logd
%attr(755,root,root) %{_libdir}/heartbeat/plugins/InterfaceMgr/generic.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/heartbeat.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/lsb.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/ocf.so

%dir %{_libdir}/stonith
%dir %{_libdir}/stonith/plugins
%dir %{_libdir}/stonith/plugins/stonith2
%{_libdir}/stonith/plugins/external
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/*.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/ribcl.py
%attr(755,root,root) %{_libdir}/stonith/plugins/xen0-ha-dom0-stonith-helper

%dir %{_var}/lib/heartbeat
%dir %{_var}/lib/heartbeat/cores
%dir %attr(700,root,root) %{_var}/lib/heartbeat/cores/root
%dir %attr(700,nobody,nobody) %{_var}/lib/heartbeat/cores/nobody
%dir %attr(700,hacluster,haclient) %{_var}/lib/heartbeat/cores/hacluster

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblrm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblrm.so.2
%attr(755,root,root) %{_libdir}/libpils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpils.so.2
%attr(755,root,root) %{_libdir}/libplumb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplumb.so.2
%attr(755,root,root) %{_libdir}/libplumbgpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libplumbgpl.so.2
%attr(755,root,root) %{_libdir}/libstonith.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstonith.so.1

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblrm.so
%attr(755,root,root) %{_libdir}/libpils.so
%attr(755,root,root) %{_libdir}/libplumb.so
%attr(755,root,root) %{_libdir}/libplumbgpl.so
%attr(755,root,root) %{_libdir}/libstonith.so
%{_includedir}/clplumbing
%{_includedir}/heartbeat
%{_includedir}/stonith
%{_includedir}/pils

%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
%attr(755,root,root) %{_libdir}/heartbeat/ipctest
%attr(755,root,root) %{_libdir}/heartbeat/ipctransientclient
%attr(755,root,root) %{_libdir}/heartbeat/ipctransientserver
%attr(755,root,root) %{_libdir}/heartbeat/transient-test.sh
%attr(755,root,root) %{_libdir}/heartbeat/base64_md5_test
%attr(755,root,root) %{_libdir}/heartbeat/logtest

%dir %{_libdir}/heartbeat/plugins/test
%attr(755,root,root) %{_libdir}/heartbeat/plugins/test/test.so

%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lrmtest
%{_datadir}/%{name}/lrmtest/README.regression
%{_datadir}/%{name}/lrmtest/defaults
%{_datadir}/%{name}/lrmtest/descriptions
%{_datadir}/%{name}/lrmtest/language
%{_datadir}/%{name}/lrmtest/lrmadmin-interface
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/LRMBasicSanityCheck
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/lrmregtest*
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/*.sh

%dir %{_datadir}/%{name}/lrmtest/testcases
%{_datadir}/%{name}/lrmtest/testcases/BSC
%{_datadir}/%{name}/lrmtest/testcases/basicset
%{_datadir}/%{name}/lrmtest/testcases/metadata
%{_datadir}/%{name}/lrmtest/testcases/metadata.exp
%{_datadir}/%{name}/lrmtest/testcases/rscexec
%{_datadir}/%{name}/lrmtest/testcases/rscexec.exp
%{_datadir}/%{name}/lrmtest/testcases/rscmgmt
%{_datadir}/%{name}/lrmtest/testcases/rscmgmt.exp
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/testcases/*filter
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/testcases/*.sh
