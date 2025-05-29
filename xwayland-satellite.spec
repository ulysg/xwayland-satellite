%bcond_without check

Name:           xwayland-satellite
Version:        0.6
Release:        %autorelease
Summary:        Run Xwayland apps with any Wayland compositor

License:        MPL-2.0
URL:            https://github.com/Supreeeme/xwayland-satellite
Source:         https://github.com/Supreeeme/xwayland-satellite/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  clang
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-cursor)
Requires:       xorg-x11-server-Xwayland

%description 
xwayland-satellite grants rootless Xwayland integration to any Wayland
compositor implementing xdg_wm_base. This is particularly useful for compositors
that (understandably) do not want to go through implementing support for
rootless Xwayland themselves.

%prep
%autosetup -n %{name}-%{version} -p1
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build -f systemd
%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies

%install
%cargo_install
mkdir -p %{buildroot}/usr/lib/systemd/user/
cp -a resources/xwayland-satellite.service %{buildroot}/usr/lib/systemd/user/
sed -i "s:/usr/local/bin:%{_bindir}:" %{buildroot}/usr/lib/systemd/user/xwayland-satellite.service

%files
%license LICENSE
%license LICENSE.dependencies
%doc README.md
%{_bindir}/xwayland-satellite
/usr/lib/systemd/user/xwayland-satellite.service

%changelog
%autochangelog
