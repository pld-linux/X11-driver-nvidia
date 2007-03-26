# TODO
# - missing CC quotes somewhere: ccache: invalid option -- S
#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# without kernel packages
%bcond_without	incall		# include all tarballs
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
#
%define		_nv_ver		1.0
%define		_nv_rel		9746
%define		_min_x11	6.7.0
%define		_rel		2
#
%define		need_x86	0
%define		need_x8664	0
%if %{with incall}
%define		need_x86	1
%define		need_x8664	1
%else
%ifarch %{ix86}
%define		need_x86	1
%endif
%ifarch %{x8664}
%define		need_x8664	1
%endif
%endif

Summary:	Linux Drivers for NVIDIA GeForce/Quadro Chips
Summary(pl.UTF-8):	Sterowniki do kart graficznych NVIDIA GeForce/Quadro
Name:		X11-driver-nvidia
Version:	%{_nv_ver}.%{_nv_rel}
Release:	%{_rel}
License:	nVidia Binary
Group:		X11
# why not pkg0!?
%if %{need_x86}
Source0:	http://download.nvidia.com/XFree86/Linux-x86/%{_nv_ver}-%{_nv_rel}/NVIDIA-Linux-x86-%{_nv_ver}-%{_nv_rel}-pkg1.run
# Source0-md5:	cf0cdbd9099a6df028de429044e7f4da
%endif
%if %{need_x8664}
Source1:	http://download.nvidia.com/XFree86/Linux-x86_64/%{_nv_ver}-%{_nv_rel}/NVIDIA-Linux-x86_64-%{_nv_ver}-%{_nv_rel}-pkg1.run
# Source1-md5:	6af676cc903bff3bc141098a47f78182
%endif
Source2:	%{name}-settings.desktop
Source3:	%{name}-xinitrc.sh
Patch0:		%{name}-GL.patch
Patch1:		%{name}-conftest.patch
# http://www.minion.de/files/1.0-6629/
URL:		http://www.nvidia.com/object/linux.html
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
%endif
BuildRequires:	%{kgcc_package}
#BuildRequires:	X11-devel >= %{_min_x11}	# disabled for now
BuildRequires:	rpmbuild(macros) >= 1.330
BuildRequires:	sed >= 4.0
BuildConflicts:	XFree86-nvidia
Requires:	X11-Xserver
Requires:	X11-libs >= %{_min_x11}
Requires:	X11-modules >= %{_min_x11}
Provides:	X11-OpenGL-core
Provides:	X11-OpenGL-libGL
Provides:	XFree86-OpenGL-core
Provides:	XFree86-OpenGL-libGL
Obsoletes:	Mesa
Obsoletes:	X11-OpenGL-core
Obsoletes:	X11-OpenGL-libGL
Obsoletes:	XFree86-OpenGL-core
Obsoletes:	XFree86-OpenGL-libGL
Obsoletes:	XFree86-driver-nvidia
Obsoletes:	XFree86-nvidia
Conflicts:	XFree86-OpenGL-devel <= 4.2.0-3
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLcore.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%ifarch %{x8664}
%define		_libdir32	%{_prefix}/lib
%endif

%description
This driver set adds improved 2D functionality to the Xorg X server as
well as high performance OpenGL acceleration, AGP support, support for
most flat panels, and 2D multiple monitor support. Supported hardware:
modern NVIDIA GeForce (from GeForce2 MX) and Quadro (Quadro4 and up)
based graphics accelerators.

The older graphics chips are unsupported:
- NV1 and RIVA 128/128ZX chips are supported in the base Xorg install
  (nv driver)
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 are suported by -legacy
  drivers.

%description -l pl.UTF-8
Usprawnione sterowniki dla kart graficznych NVIDIA do serwera Xorg,
dające wysokowydajną akcelerację OpenGL, obsługę AGP i wielu monitorów
2D. Obsługują w miarę nowe karty NVIDIA GeForce (od wersji GeForce2
MX) oraz Quadro (od wersji Quadro4) do serwera Xorg/XFree86.

Starsze układy graficzne NVIDIA nie są obsługiwane przez ten pakiet:
- NV1 i Riva 128/128ZX są obsługiwane przez sterownik nv z Xorg.
- TNT/TNT2/GeForce 256/GeForce2 Ultra/Quadro2 obsługiwane są przez
  sterownik NVIDIA w wersji -legacy.

%package devel
Summary:	OpenGL for X11R6 development (only gl?.h)
Summary(pl.UTF-8):	Pliki nagłówkowe OpenGL dla systemu X11R6 (tylko gl?.h)
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	OpenGL-devel-base
Obsoletes:	OpenGL-devel-base
Obsoletes:	XFree86-driver-nvidia-devel
Conflicts:	XFree86-OpenGL-devel < 4.3.99.902-0.3

%description devel
Base headers (only gl?.h) for OpenGL for X11R6 for nvidia drivers.

%description devel -l pl.UTF-8
Podstawowe pliki nagłówkowe (tylko gl?.h) OpenGL dla systemu X11R6 dla
sterowników nvidii.

%package progs
Summary:	Tools for advanced control of nVidia graphic cards
Summary(pl.UTF-8):	Narzędzia do zarządzania kartami graficznymi nVidia
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Obsoletes:	XFree86-driver-nvidia-progs

%description progs
Tools for advanced control of nVidia graphic cards.

%description progs -l pl.UTF-8
Narzędzia do zarządzania kartami graficznymi nVidia.

%package -n kernel%{_alt_kernel}-video-nvidia
Summary:	nVidia kernel module for nVidia Architecture support
Summary(de.UTF-8):	Das nVidia-Kern-Modul für die nVidia-Architektur-Unterstützung
Summary(pl.UTF-8):	Moduł jądra dla obsługi kart graficznych nVidia
Version:	%{_nv_ver}.%{_nv_rel}
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
Requires:	dev >= 2.7.7-10
%{?with_dist_kernel:%requires_releq_kernel}
Provides:	X11-driver-nvidia(kernel)
Obsoletes:	XFree86-nvidia-kernel

%description -n kernel%{_alt_kernel}-video-nvidia
nVidia Architecture support for Linux kernel.

%description -n kernel%{_alt_kernel}-video-nvidia -l de.UTF-8
Die nVidia-Architektur-Unterstützung für den Linux-Kern.

%description -n kernel%{_alt_kernel}-video-nvidia -l pl.UTF-8
Obsługa architektury nVidia dla jądra Linuksa. Pakiet wymagany przez
sterownik nVidii dla Xorg/XFree86.

%prep
cd %{_builddir}
rm -rf NVIDIA-Linux-x86*-%{_nv_ver}-%{_nv_rel}-pkg*
%ifarch %{ix86}
/bin/sh %{SOURCE0} --extract-only
%setup -qDT -n NVIDIA-Linux-x86-%{_nv_ver}-%{_nv_rel}-pkg1
%else
/bin/sh %{SOURCE1} --extract-only
%setup -qDT -n NVIDIA-Linux-x86_64-%{_nv_ver}-%{_nv_rel}-pkg1
%endif
%patch0 -p1
#%patch1 -p1
sed -i 's:-Wpointer-arith::' usr/src/nv/Makefile.kbuild

%build
%if %{with kernel}
cd usr/src/nv/
ln -sf Makefile.kbuild Makefile
cat >> Makefile <<'EOF'

$(obj)/nv-kernel.o: $(src)/nv-kernel.o.bin
	cp $< $@
EOF
mv nv-kernel.o{,.bin}
%build_kernel_modules -m nvidia
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with userspace}
install -d $RPM_BUILD_ROOT%{_libdir}/modules/{drivers,extensions} \
	$RPM_BUILD_ROOT{/usr/include/GL,/usr/%{_lib}/tls,%{_bindir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir},/etc/X11/xinit/xinitrc.d}

ln -sf $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_prefix}/../lib

install usr/bin/nvidia-settings $RPM_BUILD_ROOT%{_bindir}
install usr/bin/nvidia-xconfig $RPM_BUILD_ROOT%{_bindir}
install usr/share/pixmaps/nvidia-settings.png $RPM_BUILD_ROOT%{_pixmapsdir}
install usr/share/man/man1/nvidia-[sx]* $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/nvidia-settings.desktop
install %{SOURCE3} $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/nvidia-settings.sh
install usr/lib/libnvidia-tls.so.%{version} $RPM_BUILD_ROOT/usr/%{_lib}
install usr/lib/tls/libnvidia-tls.so.%{version} $RPM_BUILD_ROOT/usr/%{_lib}/tls
install usr/lib/libGL{,core}.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install usr/X11R6/lib/modules/extensions/libglx.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/modules/extensions
install usr/X11R6/lib/modules/libnvidia-wfb.so.%{version} \
	$RPM_BUILD_ROOT%{_libdir}/modules
%ifarch %{x8664}
# support for running 32-bit OpenGL applications on 64-bit AMD64 Linux installations
#install -d $RPM_BUILD_ROOT%{_libdir32}
#install usr/lib32%{?with_tls:/tls}/libnvidia-tls.so.%{version} $RPM_BUILD_ROOT%{_libdir32}
#install usr/lib32/libGL{,core}.so.%{version} $RPM_BUILD_ROOT%{_libdir32}
%endif

install usr/X11R6/lib/modules/drivers/nvidia_drv.so $RPM_BUILD_ROOT%{_libdir}/modules/drivers
install usr/X11R6/lib/libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}
install usr/X11R6/lib/libXvMCNVIDIA.a $RPM_BUILD_ROOT%{_libdir}
install usr/include/GL/*.h	$RPM_BUILD_ROOT/usr/include/GL

ln -sf libGL.so.1 $RPM_BUILD_ROOT%{_libdir}/libGL.so
ln -sf libglx.so.%{version} $RPM_BUILD_ROOT%{_libdir}/modules/extensions/libglx.so
ln -sf libnvidia-wfb.so.%{version} $RPM_BUILD_ROOT%{_libdir}/modules/libwfb.so
ln -sf libXvMCNVIDIA.so.%{version} $RPM_BUILD_ROOT%{_libdir}/libXvMCNVIDIA.so

# OpenGL ABI for Linux compatibility
ln -sf %{_libdir}/libGL.so.1 $RPM_BUILD_ROOT/usr/%{_lib}/libGL.so.1
ln -sf %{_libdir}/libGL.so $RPM_BUILD_ROOT/usr/%{_lib}/libGL.so
%endif

%if %{with kernel}
%install_kernel_modules -m usr/src/nv/nvidia -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
cat << EOF

 *******************************************************
 *                                                     *
 *  NOTE:                                              *
 *  You must install:                                  *
 *  kernel-video-nvidia-%{version}                   *
 *  for this driver to work                            *
 *                                                     *
 *******************************************************

EOF

%postun	-p /sbin/ldconfig

%post	-n kernel%{_alt_kernel}-video-nvidia
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-video-nvidia
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc LICENSE
%doc usr/share/doc/{README.txt,NVIDIA_Changelog,XF86Config.sample}
#%%lang(de) %doc usr/share/doc/README.DE
%attr(755,root,root) %{_libdir}/libGL.so.*.*
%attr(755,root,root) %{_libdir}/libGL.so
%attr(755,root,root) %{_libdir}/libGLcore.so.*.*
%attr(755,root,root) %{_libdir}/libXvMCNVIDIA.so.*.*
%dir /usr/%{_lib}/tls
%attr(755,root,root) /usr/%{_lib}/libnvidia-tls.so.*.*.*
%attr(755,root,root) /usr/%{_lib}/tls/libnvidia-tls.so.*.*.*
%ifarch %{x8664}
# support for running 32-bit OpenGL applications on 64-bit AMD64 Linux installations
#dir %{_libdir32}
#attr(755,root,root) %{_libdir32}/libGL.so.*.*
#attr(755,root,root) %{_libdir32}/libGLcore.so.*.*
#attr(755,root,root) %{_libdir32}/libXvMCNVIDIA.so.*.*
#attr(755,root,root) %{_libdir32}/libnvidia-tls.so.*.*.*
%endif
%attr(755,root,root) /usr/%{_lib}/libGL.so.1
%attr(755,root,root) /usr/%{_lib}/libGL.so
%attr(755,root,root) %{_libdir}/modules/lib*
%attr(755,root,root) %{_libdir}/modules/extensions/libglx.so*
%attr(755,root,root) %{_libdir}/modules/drivers/nvidia_drv.so
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-video-nvidia
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*.ko*
%endif

%if %{with userspace}
%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libXvMCNVIDIA.so
/usr/include/GL/*.h
# -static
%{_libdir}/libXvMCNVIDIA.a

%files progs
%defattr(644,root,root,755)
%doc usr/share/doc/nvidia-settings-user-guide.txt
%attr(755,root,root) %{_bindir}/nvidia-settings
%attr(755,root,root) %{_bindir}/nvidia-xconfig
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/*.sh
%{_desktopdir}/*.desktop
%{_mandir}/man1/*
%{_pixmapsdir}/*
%endif
