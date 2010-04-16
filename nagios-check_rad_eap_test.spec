%define name    nagios-rad_eap_test
%define version 0.23
%define release %mkrel 1

Name:       %{name}
Version:    %{version}
Release:    %{release}
Summary:    Nagios compatible shell script used for testing radius EAP methods
Group:      Networking/Other
License:    BSD
URL:        http://wiki.eduroam.cz/rad_eap_test/
Source:     http://wiki.eduroam.cz/rad_eap_test/rad_eap_test-%{version}.tar.bz2
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}

%description
rad_eap_test is used to test availability of radius servers in monitoring
solutions as nagios. rad_eap_test is only wrapper shell script around
eapol_test from wpa_supplicant project. rad_eap_test  generates configuration
for eapol_test, runs it and after processing eapol_test messages returns status
code. Status code is processed by monitoring tools as nagios.

%prep
%setup -q -n rad_eap_test-%{version}

# fix eapol_test location
perl -pi -e 's|EAPOL_PROG=.*|EAPOL_PROG=%{_sbindir}/eapol_test|' rad_eap_test

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/nagios/plugins
install -m 755 rad_eap_test %{buildroot}%{_datadir}/nagios/plugins

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/rad_eap_test.cfg <<'EOF'
define command {
	command_name    rad_eap_test
	command_line    %{_datadir}/nagios/plugins/rad_eap_test -H $HOSTADDRESS$
}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog COPYING README doc
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/rad_eap_test.cfg
%{_datadir}/nagios/plugins/rad_eap_test

