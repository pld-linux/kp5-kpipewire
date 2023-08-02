#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.7
%define		qtver		5.15.2
%define		kpname		kpipewire
Summary:	a set of convenient classes to use PipeWire in Qt projects
Name:		kp5-%{kpname}
Version:	5.27.7
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	1d759ab0bb02f630385e4dc267aaef6e
URL:		http://www.kde.org/
BuildRequires:	Qt5WaylandClient-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	ffmpeg-devel
BuildRequires:	kf5-extra-cmake-modules
BuildRequires:	kf5-kwayland-devel
BuildRequires:	kf5-plasma-wayland-protocols-devel
BuildRequires:	ninja
BuildRequires:	pipewire-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
kpipewire offers a set of convenient classes to use PipeWire
(https://pipewire.org/) in Qt projects.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cmake >= 3.16

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKPipeWire.so.5
%{_libdir}/libKPipeWire.so.5.*.*
%ghost %{_libdir}/libKPipeWireRecord.so.5
%{_libdir}/libKPipeWireRecord.so.5.*.*
%dir %{_libdir}/qt5/qml/org/kde/pipewire
%{_libdir}/qt5/qml/org/kde/pipewire/libKPipeWireDeclarative.so
%{_libdir}/qt5/qml/org/kde/pipewire/qmldir
%dir %{_libdir}/qt5/qml/org/kde/pipewire/record
%{_libdir}/qt5/qml/org/kde/pipewire/record/libKPipeWireRecordDeclarative.so
%{_libdir}/qt5/qml/org/kde/pipewire/record/qmldir
%{_datadir}/qlogging-categories5/kpipewire.categories
%{_datadir}/qlogging-categories5/kpipewirerecord.categories
%ghost %{_libdir}/libKPipeWireDmaBuf.so.5
%{_libdir}/libKPipeWireDmaBuf.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPipeWire
%{_libdir}/cmake/KPipeWire
%{_libdir}/libKPipeWire.so
%{_libdir}/libKPipeWireRecord.so
%{_libdir}/libKPipeWireDmaBuf.so
