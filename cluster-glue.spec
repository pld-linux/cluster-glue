# TODO:
# - pldize ha_logd initscript (look heartbeat.init?)
# - stonith-libs? pils? (any sense? libs are small and have little external dependencies)
# - separate some stonith plugins which have external dependencies?
#
# Conditional build:
%bcond_without	vacm	# VACM stonith plugin
#
Summary:	Reusable cluster components
Summary(pl.UTF-8):	Komponenty klastrowe wielokrotnego użytku
Name:		cluster-glue
Version:	1.0.12
Release:	1
License:	GPL v2+ and LGPL v2+
Group:		Aplications/System
#Source0Download: http://linux-ha.org/wiki/Downloads
Source0:	http://hg.linux-ha.org/glue/archive/glue-%{version}.tar.bz2
# Source0-md5:	ec620466d6f23affa3b074b72bca7870
#Source1:	logd.service
Patch0:		%{name}-link.patch
Patch1:		%{name}-opt.patch
Patch2:		%{name}-rc.patch
Patch3:		x32-long-long-time-types.patch
URL:		http://linux-ha.org/wiki/Cluster_Glue
BuildRequires:	OpenIPMI-devel >= 1.4
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	curl-devel
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-dtd44-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	help2man
BuildRequires:	libaio-devel
BuildRequires:	libltdl-devel
BuildRequires:	libnet-devel >= 1.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel >= 5.4
BuildRequires:	openhpi-devel
BuildRequires:	openssl-devel
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%{?with_vacm:BuildRequires:	vacm-devel}
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(post,preun,postun):	systemd-units
Requires:	systemd-units
Requires:	%{name}-libs = %{version}-%{release}
Requires:	perl-TimeDate
Requires:	rc-scripts
Provides:	group(haclient)
Provides:	user(hacluster)
# Directives to allow upgrade from combined heartbeat packages
Provides:	heartbeat-pils = 3.0.0-1
Obsoletes:	heartbeat-common
Obsoletes:	heartbeat-pils < 3.0.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A collection of common tools that are useful for writing cluster
managers such as Pacemaker. Provides a local resource manager that
understands the OCF and LSB standards, and an interface to common
STONITH devices.

%description -l pl.UTF-8
Zbiór wspólnych narzędzi przydatnych przy pisaniu zarządców klastrów,
takich jak Pacemaker. Pakiet zawiera zarządcę zasobów lokalnych
zgodnego ze standardami OCF i LSB oraz interfejs do wspólnych urządzeń
STONITH.

%package libs
Summary:	Reusable cluster libraries
Summary(pl.UTF-8):	Biblioteki klastrowe wielokrotnego użytku
Group:		Libraries
Obsoletes:	libheartbeat2

%description libs
A collection of libraries that are useful for writing cluster managers
such as Pacemaker.

%description libs -l pl.UTF-8
Zbiór bibliotek przydatnych przy pisaniu zarządców klastrów, takich
jak Pacemaker.

%package libs-devel
Summary:	Header files for writing cluster managers
Summary(pl.UTF-8):	Pliki nagłówkowe do pisania zarządców klastrów
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 2.0
Requires:	libltdl-devel
Obsoletes:	libheartbeat-devel

%description libs-devel
Header files useful for writing cluster managers such as Pacemaker.

%description libs-devel -l pl.UTF-8
Pliki nagłówkowe przydatne przy pisaniu zarządców klastrów, takich jak
Pacemaker.

%package tests
Summary:	Tests for cluster-glue framework
Summary(pl.UTF-8):	Testy dla szkieletu cluster-glue
Group:		Development
Requires:	%{name}-libs = %{version}-%{release}

%description tests
Tests for cluster-glue framework.

%description tests -l pl.UTF-8
Testy dla szkieletu cluster-glue.

%package stonith
Summary:	Provides an interface to Shoot The Other Node In The Head
Summary(pl.UTF-8):	Interfejs do "odstrzelenia" drugiego węzła w klastrze
Group:		Applications/System
Requires:	OpenIPMI >= 2.0.3
Provides:	heartbeat-stonith = 3.0.0-1
Obsoletes:	heartbeat-stonith < 3.0.0-1

%description stonith
Provides an interface to Shoot The Other Node In The Head.

%description stonith -l pl.UTF-8
STONITH (Shoot The Other Node In The Head) to interfejs służący do
"odstrzelenia" drugiego węzła w klastrze.

%prep
%setup -q -n Reusable-Cluster-Components-glue--glue-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%ifarch x32
%patch3 -p1
%endif

sed -i -e's;#!/usr/bin/env \(python\|perl\);#!/usr/bin/\1;' \
					lib/plugins/stonith/external/*

%build
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--docdir=%{_docdir}/%{name}-%{version} \
	--disable-fatal-warnings \
	--disable-static \
	--enable-ipmilan \
	--with-daemon-group=haclient \
	--with-daemon-user=hacluster \
	--with-initdir=/etc/rc.d/init.d \
	--with-rundir=/var/run
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -delete

#%{__sed} -e 's;@libdir@;%{_libdir};g' \
#	%{SOURCE1} > $RPM_BUILD_ROOT%{systemdunitdir}/logd.service

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 60 haclient
%useradd -u 17 -d /var/lib/heartbeat/cores/hacluster -c "Heartbeat User" -g haclient hacluster

%post
/sbin/chkconfig --add logd
%service logd restart
%systemd_post logd.service

%preun
if [ "$1" = "0" ]; then
	%service -q logd stop
	/sbin/chkconfig --del logd
fi
%systemd_preun logd.service

%postun
if [ "$1" = "0" ]; then
	%userremove hacluster
	%groupremove haclient
fi
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog logd/logd.cf doc/stonith/README*
%attr(754,root,root) /etc/rc.d/init.d/logd
%{systemdunitdir}/logd.service

%attr(755,root,root) %{_sbindir}/ha_logger
%attr(755,root,root) %{_sbindir}/hb_report
%attr(755,root,root) %{_sbindir}/lrmadmin
%attr(755,root,root) %{_sbindir}/meatclient
%attr(755,root,root) %{_sbindir}/cibsecret
%{_mandir}/man1/ha_logger.1*
%{_mandir}/man8/ha_logd.8*
%{_mandir}/man8/hb_report.8*
%{_mandir}/man8/lrmadmin.8*
%{_mandir}/man8/meatclient.8*

%dir %{_datadir}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/ha_cf_support.sh
%attr(755,root,root) %{_datadir}/%{name}/openais_conf_support.sh
%attr(755,root,root) %{_datadir}/%{name}/utillib.sh
%attr(755,root,root) %{_datadir}/%{name}/ha_log.sh

%dir %{_libdir}/heartbeat/plugins/RAExec
%dir %{_libdir}/heartbeat/plugins/InterfaceMgr
%dir %{_libdir}/heartbeat/plugins/compress
%attr(755,root,root) %{_libdir}/heartbeat/lrmd
%attr(755,root,root) %{_libdir}/heartbeat/ha_logd
%attr(755,root,root) %{_libdir}/heartbeat/plugins/InterfaceMgr/generic.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/heartbeat.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/lsb.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/ocf.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/compress/bz2.so
%attr(755,root,root) %{_libdir}/heartbeat/plugins/compress/zlib.so

%dir /var/lib/heartbeat
%attr(711,root,root) %dir /var/lib/heartbeat/cores
%attr(700,root,root) %dir /var/lib/heartbeat/cores/root
%attr(700,hacluster,root) %dir /var/lib/heartbeat/cores/hacluster
# we don't want any files owned by nobody
%attr(700,root,root) %dir /var/lib/heartbeat/cores/nobody

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
%dir %{_libdir}/heartbeat
%dir %{_libdir}/heartbeat/plugins
# also used by resource-agents runtime package (shouldn't agent_config.h be in resource-agents-devel?)
%dir %{_includedir}/heartbeat

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblrm.so
%attr(755,root,root) %{_libdir}/libpils.so
%attr(755,root,root) %{_libdir}/libplumb.so
%attr(755,root,root) %{_libdir}/libplumbgpl.so
%attr(755,root,root) %{_libdir}/libstonith.so
%{_includedir}/clplumbing
%{_includedir}/heartbeat/compress.h
%{_includedir}/heartbeat/glue_config.h
%{_includedir}/heartbeat/ha_msg.h
%{_includedir}/heartbeat/lrm
%{_includedir}/stonith
%{_includedir}/pils

%files tests
%defattr(644,root,root,755)
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
%{_datadir}/%{name}/lrmtest/testcases/stonith
%{_datadir}/%{name}/lrmtest/testcases/stonith.exp
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/testcases/*filter
%attr(755,root,root) %{_datadir}/%{name}/lrmtest/testcases/*.sh

%files stonith
%defattr(644,root,root,755)
%doc doc/stonith/README*
%attr(755,root,root) %{_sbindir}/stonith
%{_mandir}/man8/stonith.8*
%dir %{_libdir}/stonith
%dir %{_libdir}/stonith/plugins
%dir %{_libdir}/stonith/plugins/external
%attr(755,root,root) %{_libdir}/stonith/plugins/external/*
%dir %{_libdir}/stonith/plugins/stonith2
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/apcmaster.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/apcmastersnmp.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/apcsmart.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/baytech.so
# R: openhpi
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/bladehpi.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/cyclades.so
# R: curl libxml2
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/drac3.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/external.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/ibmhmc.so
# R: OpenIPMI
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/ipmilan.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/meatware.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/null.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/nw_rpc100s.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/rcd_serial.so
# R: libxml2
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/rhcs.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/rps10.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/ssh.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/suicide.so
%if %{with vacm}
# R: vacm-libs
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/vacm.so
%endif
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/wti_mpc.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/wti_nps.so
%attr(755,root,root) %{_libdir}/stonith/plugins/stonith2/ribcl.py
%attr(755,root,root) %{_libdir}/stonith/plugins/xen0-ha-dom0-stonith-helper
