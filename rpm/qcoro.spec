%global qt6_build_dir release-qt6
%global _description %{expand:
The QCoro library provides set of tools to make use of the C++20 coroutines
in connection with certain asynchronous Qt actions.

The major benefit of using coroutines with Qt types is that it allows writing
asynchronous code as if it were synchronous and, most importantly, while the
coroutine is co_awaiting, the Qt event loop runs as usual, meaning that your
application remains responsive.}

Name: qcoro
Version: 0.11.0
Release: 7%{?dist}

License: MIT
Summary: C++ Coroutines for Qt
URL: https://github.com/qcoro/qcoro
Source0:    %{name}-%{version}.tar.bz2

BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtwebsockets-devel
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: qt6-qtbase-private-devel

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja

%description %_description

%package qt6
Summary: C++ Coroutines for Qt 6

%package qt6-devel
Summary: Development files for QCoro (Qt 6 version)
Requires: %{name}-qt6%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}

%description qt6 %_description
%description qt6-devel %_description


%prep
%autosetup -n %{name}-%{version}/upstream -p1

%build

mkdir -p %{qt6_build_dir}
pushd %{qt6_build_dir}
%cmake -G Ninja \
    -S .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DECM_MKSPECS_INSTALL_DIR=%{_libdir}/qt6/mkspecs/modules \
    -DUSE_QT_VERSION:STRING=6 \
    -DBUILD_TESTING:BOOL=ON \
    -DQCORO_BUILD_EXAMPLES:BOOL=ON \
    -DQCORO_ENABLE_ASAN:BOOL=OFF \
    -DQCORO_WITH_QML:BOOL=ON \
    -DQCORO_WITH_QTDBUS:BOOL=ON \
    -DQCORO_WITH_QTNETWORK:BOOL=ON \
    -DQCORO_WITH_QTQUICK:BOOL=ON \
    -DQCORO_WITH_QTWEBSOCKETS:BOOL=ON
%cmake_build
popd


%install
pushd %{qt6_build_dir}
%cmake_install
popd

%files qt6
%doc README.md
%license LICENSES/*
%{_libdir}/libQCoro6*.so.0*

%files qt6-devel
%{_includedir}/qcoro6/
%{_libdir}/cmake/QCoro6*/
%{_libdir}/libQCoro6*.so
%{_libdir}/qt6/mkspecs/modules/qt_QCoro*.pri
