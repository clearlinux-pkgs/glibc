%define keepstatic 1
%define glibc_target x86_64-generic-linux
%define abi_package %{nil}

# glibc is important enough to have debug info always
%define debug_package %{nil}
%define __strip /bin/true



Name:           glibc
Version:        2.39
Release:        632
License:        GPL-2.0
Summary:        GNU C library
Url:            http://www.gnu.org/software/libc/libc.html
Group:          libs
Source0:        https://ftp.gnu.org/gnu/glibc/glibc-2.39.tar.xz

Patch1:                glibc-stable-branch.patch

Patch4:		0001-Set-host.conf-multi-to-on-by-default.patch
Patch7:		ldconfig-format-new.patch
Patch8:		0001-sysdeps-unix-Add-support-for-usr-lib32-as-a-system-l.patch
#Patch9:		nsswitch-altfiles.patch
Patch9:		nsswitch.patch
Patch10:	ld-so-cache-in-var.patch
Patch12:	mkdir-ldconfig.patch
Patch13:	locale-var-cache.patch
Patch14:	nonscd.patch
Patch20:	tzselect-proper-zone-file.patch
Patch23:	use_madv_free.patch
Patch24:	malloc_tune.patch
Patch25:        calloc.patch
Patch26:	0001-misc-Support-fallback-stateless-shells-path-in-absen.patch
Patch28:	stateless.patch
#Patch29:	nsswitch-altfiles-bugfix.patch
Patch36:	populate.patch
# backports of libm work
Patch38:        0001-x86-64-Remove-sysdeps-x86_64-fpu-s_sinf.S.patch
Patch39: 	tune_adaptive_spin.patch
Patch51:        gcc-8-fix.patch
Patch54: 	0001-Set-vector-width-and-alignment-to-fix-GCC-AVX-issue.patch
Patch55: 	disable-vectorization-even-more.patch
Patch56:	0001-Force-ffsll-to-be-64-bytes-aligned.patch
Patch57:        nofma4.patch

Patch62:	limit-avx512-freq-damage.patch

Patch63:	utf8-locale-naming.patch

# cves: patches 101 through 200

BuildRequires:	grep
BuildRequires:	texinfo
BuildRequires:	linux-libc-headers
BuildRequires:	gettext-dev
BuildRequires:	bison
BuildRequires:	gcc-dev32 gcc-libgcc32 gcc-libstdc++32
BuildRequires:	python3-dev
BuildRequires:	util-linux

BuildRequires:  gcc14 gcc14-dev
#BuildRequires:  rpcsvc-proto-dev


%description
GNU C library.

%package doc
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          doc

%description doc
GNU C library.

%package bin
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          libs
Provides:       catchsegv
Provides:       sln
Provides:       ldd
Provides:	libc-bin
Obsoletes:	libc-bin < 2.29

%description bin
GNU C library.

%package locale
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          libs
Provides:	libc6-locale
Obsoletes:	libc6-locale < 2.29

%description locale
GNU C library.

%package nscd
License:        GPL-2.0
Summary:        GNU C library
Group:          libs
Provides:	nscd

%description nscd
GNU C library.

%package utils
License:        GPL-2.0
Summary:        GNU C library
Group:          libs

%description utils
GNU C library.

%package bench
License:        GPL-2.0
Summary:        GNU C library
Group:          libs

%description bench
GNU C library.

%package -n libc6
License:        GPL-2.0
Summary:        GNU C library
Group:          libs
Requires(pre):       filesystem
Provides:       glibc
Provides:       glibc-extra-nss
Provides:       libsotruss
Provides:       libmemusage
Provides:       libsegfault
Provides:       libthread-db1
Provides:       rtld(GNU_HASH)
Requires:       nss-altfiles-lib
Provides:	libc6
# to provide nss_altfiles for passwd aka root account
Requires:       clr-systemd-config-data

%description -n libc6
GNU C library.


%package lib-avx2
License:        GPL-2.0
Summary:        GNU C library

%description lib-avx2
GNU C library.

%package dev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Requires:	rpcsvc-proto-dev
Requires:	libxcrypt-dev

%description dev
GNU C library.

%package -n libc6-dev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Provides:	libc6-dev
Requires:       glibc-dev = %{version}-%{release}

%description -n libc6-dev
GNU C library.

%package dev32
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Requires:       glibc-libc32 = %{version}-%{release}
Requires:       libc6-dev = %{version}-%{release}

%description dev32
GNU C library.


%package libc32
License:        GPL-2.0
Summary:        GNU C library
Group:          devel

%description libc32
GNU C library.

%package staticdev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Requires:	gcc-staticdev

%description staticdev
GNU C library.

%package extras
Summary:        extra components for glibc
Group:          libs

%description extras
GNU C library extra components.

%prep
%setup -q

%patch1 -p1
%patch4 -p1
#%patch7 -p1
%patch8 -p1
%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch20 -p1
%patch24 -p1
#%patch25 -p1
%patch26 -p1
%patch28 -p1
%patch39 -p1
#%patch36 -p1
#%patch51 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1

%patch62 -p1
%patch63 -p1


%patch9 -p1

%build
export SOURCE_DATE_EPOCH=1484361909
export LANG=C
export GCC_IGNORE_WERROR=1


# Keep only the UTF-8 locales...
supported=./localedata/SUPPORTED
sed -nr '/^(#|SUPPORTED-LOCALES=|.*\/UTF-8)/p' $supported > $supported.new
mv -v $supported.new $supported

mkdir ../glibc-buildroot
pushd ../glibc-buildroot

export CFLAGS="-O3 -march=westmere -mtune=sapphirerapids -g1 -m64  -Wl,-z,max-page-size=0x1000 -fPIC -falign-functions=32 -gz"
export ASFLAGS=""
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.39/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --enable-crypt \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --disable-silent-rules \
    --disable-dependency-tracking \
    --enable-kernel=3.10 \
    --without-cvs \
    --disable-profile \
    --disable-debug \
    --without-gd  \
    --enable-clocale=gnu \
    --enable-add-ons \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=%{glibc_target} \
    --host=%{glibc_target} \
    --with-pkgversion='Clear Linux Software for Intel Architecture' \
    --enable-lock-elision=no \
    --enable-bind-now  \
    --enable-tunables \
    --enable-obsolete-nsl \
    --disable-cet \
    --enable-static-pie \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale

make %{?_smp_mflags}
make USE_CLOCK_GETTIME=1 bench-build %{?_smp_mflags}
popd


mkdir ../glibc-buildroot-avx2
pushd ../glibc-buildroot-avx2

export CFLAGS="-O3 -march=haswell -mtune=sapphirerapids -g1 -m64  -Wl,-z,max-page-size=0x1000 -fPIC  -Wl,-z,x86-64-v3 -gz"
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1 "
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.39/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --disable-silent-rules \
    --disable-dependency-tracking \
    --enable-kernel=3.10 \
    --without-cvs \
    --disable-profile \
    --disable-debug \
    --without-gd  \
    --enable-clocale=gnu \
    --enable-add-ons \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=%{glibc_target} \
    --host=%{glibc_target} \
    --with-pkgversion='Clear Linux Software for Intel Architecture' \
    --enable-lock-elision=no \
    --enable-bind-now  \
    --enable-tunables \
    --enable-obsolete-nsl \
    --disable-cet \
    --enable-static-pie \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale

make 
#%{?_smp_mflags}
popd

mkdir ../glibc-buildroot-avx512
pushd ../glibc-buildroot-avx512

export CFLAGS="-O3 -march=x86-64-v4 -mtune=sapphirerapids -g1 -m64  -Wl,-z,max-page-size=0x1000 -fPIC -Wl,-z,x86-64-v4 -gz"
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -D__AVX512__=1 -msse2avx -D__FMA__=1 "
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.39/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --disable-silent-rules \
    --disable-dependency-tracking \
    --enable-kernel=3.10 \
    --without-cvs \
    --disable-profile \
    --disable-debug \
    --without-gd  \
    --enable-clocale=gnu \
    --enable-add-ons \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=%{glibc_target} \
    --host=%{glibc_target} \
    --with-pkgversion='Clear Linux Software for Intel Architecture' \
    --enable-lock-elision=no \
    --enable-bind-now  \
    --enable-tunables \
    --enable-obsolete-nsl \
    --disable-cet \
    --enable-static-pie \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale

make %{?_smp_mflags}
popd

mkdir ../glibc-buildroot32
pushd ../glibc-buildroot32

unset ASFLAGS
export CFLAGS="-O3 -m32 -march=westmere -mtune=sapphirerapids -mstackrealign -g1  -Wl,-z,max-page-size=0x1000 -gdwarf-4 -gz"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000"

../glibc-2.39/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --enable-crypt \
    --libexecdir=/usr/lib32/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib32 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --disable-silent-rules \
    --disable-dependency-tracking \
    --enable-kernel=3.10 \
    --without-cvs \
    --disable-profile \
    --disable-debug \
    --without-gd  \
    --enable-clocale=gnu \
    --enable-add-ons \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=i686-generic-linux \
    --host=i686-linux-gnu \
    --target=i686-generic-linux \
    --with-pkgversion='Clear Linux Software for Intel Architecture' \
    --enable-lock-elision=no \
    --enable-bind-now  \
    --enable-tunables \
    --enable-obsolete-nsl \
    --disable-cet \
    --enable-static-pie \
    libc_cv_slibdir=/usr/lib32 \
    libc_cv_complocaledir=/usr/share/locale \
    libc_cv_can_use_register_asm_ebp=no \
    CC="gcc -m32" CXX="g++ -m32" i686-linux-gnu


make %{?_smp_mflags}
popd

mkdir ../glibc-buildrootapx
pushd ../glibc-buildrootapx

unset ASFLAGS
unset LDFLAGS
export CFLAGS="-O3 -march=haswell -mtune=sapphirerapids -g1 -m64  -Wl,-z,max-page-size=0x1000 -fPIC  -Wl,-z,x86-64-v3 -gz -mapxf -mavx10.1"
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1 "
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "
export CC=/usr/bin/gcc-14

../glibc-2.39/configure \
    --prefix=/usr \
    --disable-werror \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --disable-silent-rules \
    --disable-dependency-tracking \
    --enable-kernel=6.1 \
    --without-cvs \
    --disable-profile \
    --disable-debug \
    --without-gd  \
    --enable-clocale=gnu \
    --enable-add-ons \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=%{glibc_target} \
    --host=%{glibc_target} \
    --with-pkgversion='Clear Linux Software for Intel Architecture' \
    --enable-lock-elision=no \
    --enable-bind-now  \
    --enable-tunables \
    --enable-obsolete-nsl \
    --disable-cet \
    --enable-static-pie \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale


make %{?_smp_mflags}
popd


%install
export SOURCE_DATE_EPOCH=1484361909
export GCC_IGNORE_WERROR=1

unset LDFLAGS
unset CFLAGS

# first we install the 32 bit build, so that any overlap gets resolved in
# favor of the 64 bit build
pushd ../glibc-buildroot32

make install DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}
popd

pushd ../glibc-buildroot-avx2
mkdir -p %{buildroot}/V3/usr/lib64/
cp math/libm.so %{buildroot}/V3/usr/lib64/libm.so.6
cp mathvec/libmvec.so %{buildroot}/V3/usr/lib64/libmvec.so.1
cp libc.so  %{buildroot}/V3/usr/lib64/libc-2.39.so
popd

pushd ../glibc-buildroot-avx512
mkdir -p %{buildroot}/V4/usr/lib64/
cp math/libm.so %{buildroot}/V4/usr/lib64/libm.so.6
cp mathvec/libmvec.so %{buildroot}/V4/usr/lib64/libmvec.so.1
popd

pushd ../glibc-buildrootapx
mkdir -p %{buildroot}/VA/usr/lib64/
cp math/libm.so %{buildroot}/VA/usr/lib64/libm.so.6
cp libc.so  %{buildroot}/VA/usr/lib64/libc-2.39.so
popd



pushd ../glibc-buildroot

make install DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}


mkdir -p %{buildroot}/var/cache/locale

# FIXME: As of glibc 2.39, the --prefix flag to iconvconfig appears to behave
# differently, since it hardcodes the prefix path to the cache's module lookup
# path, which in turn breaks iconv completely (unless GCONV_PATH is set in the
# environment). Once that issue is resolved (or another BKM is found),
# re-enable the cache by running the iconvconfig command below. The cache
# improves performance of iconv, so we want it to be enabled...
# Upstream report to track:
# https://sourceware.org/bugzilla/show_bug.cgi?id=28199
rm -fv %{buildroot}/usr/lib64/gconv/gconv-modules.cache
#iconvconfig --prefix=%{buildroot}


make -s -O localedata/install-locales  DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}

# Make ldconfig not fail
install -d %{buildroot}/var/cache/ldconfig

install -d %{buildroot}%{_datadir}/defaults/etc/
mv %{buildroot}%{_sysconfdir}/rpc %{buildroot}%{_datadir}/defaults/etc/rpc

mkdir -p %{buildroot}/usr/lib64/glibc/benchmarks
for f in benchtests/*; do [ -x $f -a ! -d $f ] && cp -a $f %{buildroot}/usr/lib64/glibc/benchmarks; done
pushd %{buildroot}/usr/bin
find ../lib64/glibc/benchmarks -type f -exec ln -s {} . \;
popd

## Generate UTF-8 locale-related data
make -s -O %{?_smp_mflags} localedata/install-locale-files DESTDIR=%{buildroot} install_root=%{buildroot}
for origpath in %{buildroot}/usr/share/locale/*.utf8*; do
  rename -v .utf8 .UTF-8 "$origpath"
done

# Reduce footprint of localedata, since `make localedata/install-locale-files`
# passes the `--no-hard-links` option to `localedef`.
hardlink %{buildroot}/usr/share/locale

popd # ../glibc-buildroot

ln -sfv /var/cache/locale/locale-archive %{buildroot}/usr/share/locale/locale-archive

mkdir -p %{buildroot}/usr/lib
ln -s ../lib32/ld-linux.so.2  %{buildroot}/usr/lib/ld-linux.so.2

# for oracle db installer (compat link)
ln -sf libpthread.a %{buildroot}/usr/lib64/libpthread_nonshared.a

# Get things out of /sbin and /usr/sbin
mv %{buildroot}/sbin/sln %{buildroot}/usr/bin/sln
mv %{buildroot}/sbin/ldconfig %{buildroot}/usr/bin/ldconfig
mv %{buildroot}/usr/sbin/nscd %{buildroot}/usr/bin/nscd
mv %{buildroot}/usr/sbin/iconvconfig %{buildroot}/usr/bin/iconvconfig
#mv %{buildroot}/usr/sbin/zdump %{buildroot}/usr/bin/zdump
mv %{buildroot}/usr/sbin/* %{buildroot}/usr/bin/

# swup compatibility hack 
cp %{buildroot}/usr/lib64/libc.so.6 %{buildroot}/usr/lib64/libc-2.39.so
cp %{buildroot}/usr/lib64/ld-linux-x86-64.so.2 %{buildroot}/usr/lib64/ld-2.39.so
rm %{buildroot}/usr/lib64/libc.so.6
rm %{buildroot}/usr/lib64/ld-linux-x86-64.so.2
ln -s libc-2.39.so %{buildroot}/usr/lib64/libc.so.6
ln -s ld-2.39.so  %{buildroot}/usr/lib64/ld-linux-x86-64.so.2


# we don't want/need debug symbols for locale .so files, they cause binary delta thrash 
strip %{buildroot}/usr/lib64/gconv/*.so
strip --remove-section=".note.gnu.build-id" %{buildroot}/usr/lib64/gconv/*.so

%check
pushd ../glibc-buildroot
#make check %{?_smp_mflags} || :
popd

%files bin
#/usr/bin/catchsegv
/usr/bin/sln

%files nscd
/usr/bin/nscd

%files utils
%exclude /usr/bin/mtrace
/usr/bin/gencat
/usr/bin/getconf
/usr/bin/getent
/usr/bin/iconv
/usr/bin/ldd
/usr/bin/locale
/usr/bin/pcprofiledump
/usr/bin/pldd
/usr/bin/sotruss
/usr/bin/sprof
/usr/bin/tzselect
/usr/bin/xtrace
/usr/bin/iconvconfig
/usr/bin/zdump
/usr/bin/zic
/usr/bin/ld.so

%files bench
/usr/bin/bench-*
/usr/lib64/glibc/benchmarks/*

%files -n libc6
%dir /usr/share/locale
/usr/share/locale/C.UTF-8
/usr/share/locale/en_US.UTF-8
/usr/lib64/audit/sotruss-lib.so
/usr/lib64/gconv/ANSI_X3.110.so
/usr/lib64/gconv/ARMSCII-8.so
/usr/lib64/gconv/ASMO_449.so
/usr/lib64/gconv/BIG5HKSCS.so
/usr/lib64/gconv/BIG5.so
/usr/lib64/gconv/BRF.so
/usr/lib64/gconv/CP10007.so
/usr/lib64/gconv/CP1125.so
/usr/lib64/gconv/CP1250.so
/usr/lib64/gconv/CP1251.so
/usr/lib64/gconv/CP1252.so
/usr/lib64/gconv/CP1253.so
/usr/lib64/gconv/CP1254.so
/usr/lib64/gconv/CP1255.so
/usr/lib64/gconv/CP1256.so
/usr/lib64/gconv/CP1257.so
/usr/lib64/gconv/CP1258.so
/usr/lib64/gconv/CP737.so
/usr/lib64/gconv/CP770.so
/usr/lib64/gconv/CP771.so
/usr/lib64/gconv/CP772.so
/usr/lib64/gconv/CP773.so
/usr/lib64/gconv/CP774.so
/usr/lib64/gconv/CP775.so
/usr/lib64/gconv/CP932.so
/usr/lib64/gconv/CSN_369103.so
/usr/lib64/gconv/CWI.so
/usr/lib64/gconv/EUC-CN.so
/usr/lib64/gconv/EUC-JISX0213.so
/usr/lib64/gconv/EUC-JP-MS.so
/usr/lib64/gconv/EUC-JP.so
/usr/lib64/gconv/EUC-KR.so
/usr/lib64/gconv/EUC-TW.so
/usr/lib64/gconv/gconv-modules
/usr/lib64/gconv/gconv-modules.d/gconv-modules-extra.conf
/usr/lib64/libc_malloc_debug.so
/usr/lib64/libc_malloc_debug.so.0
/usr/lib64/libnss_hesiod.so
/usr/lib64/gconv/GEORGIAN-ACADEMY.so
/usr/lib64/gconv/GEORGIAN-PS.so
/usr/lib64/gconv/GOST_19768-74.so
/usr/lib64/gconv/GREEK7-OLD.so
/usr/lib64/gconv/GREEK7.so
/usr/lib64/gconv/GREEK-CCITT.so
/usr/lib64/gconv/HP-GREEK8.so
/usr/lib64/gconv/HP-ROMAN8.so
/usr/lib64/gconv/HP-ROMAN9.so
/usr/lib64/gconv/HP-THAI8.so
/usr/lib64/gconv/HP-TURKISH8.so
/usr/lib64/gconv/IEC_P27-1.so
/usr/lib64/gconv/INIS-8.so
/usr/lib64/gconv/INIS-CYRILLIC.so
/usr/lib64/gconv/INIS.so
/usr/lib64/gconv/ISIRI-3342.so
/usr/lib64/gconv/ISO_10367-BOX.so
/usr/lib64/gconv/ISO_11548-1.so
/usr/lib64/gconv/ISO-2022-CN-EXT.so
/usr/lib64/gconv/ISO-2022-CN.so
/usr/lib64/gconv/ISO-2022-JP-3.so
/usr/lib64/gconv/ISO-2022-JP.so
/usr/lib64/gconv/ISO-2022-KR.so
/usr/lib64/gconv/ISO_2033.so
/usr/lib64/gconv/ISO_5427-EXT.so
/usr/lib64/gconv/ISO_5427.so
/usr/lib64/gconv/ISO_5428.so
/usr/lib64/gconv/ISO646.so
/usr/lib64/gconv/ISO_6937-2.so
/usr/lib64/gconv/ISO_6937.so
/usr/lib64/gconv/ISO8859-10.so
/usr/lib64/gconv/ISO8859-11.so
/usr/lib64/gconv/ISO8859-13.so
/usr/lib64/gconv/ISO8859-14.so
/usr/lib64/gconv/ISO8859-15.so
/usr/lib64/gconv/ISO8859-16.so
/usr/lib64/gconv/ISO8859-1.so
/usr/lib64/gconv/ISO8859-2.so
/usr/lib64/gconv/ISO8859-3.so
/usr/lib64/gconv/ISO8859-4.so
/usr/lib64/gconv/ISO8859-5.so
/usr/lib64/gconv/ISO8859-6.so
/usr/lib64/gconv/ISO8859-7.so
/usr/lib64/gconv/ISO8859-8.so
/usr/lib64/gconv/ISO8859-9E.so
/usr/lib64/gconv/ISO8859-9.so
/usr/lib64/gconv/ISO-IR-197.so
/usr/lib64/gconv/ISO-IR-209.so
/usr/lib64/gconv/JOHAB.so
/usr/lib64/gconv/KOI8-R.so
/usr/lib64/gconv/KOI8-RU.so
/usr/lib64/gconv/KOI-8.so
/usr/lib64/gconv/KOI8-T.so
/usr/lib64/gconv/KOI8-U.so
/usr/lib64/gconv/LATIN-GREEK-1.so
/usr/lib64/gconv/LATIN-GREEK.so
/usr/lib64/gconv/libCNS.so
/usr/lib64/gconv/libGB.so
/usr/lib64/gconv/libISOIR165.so
/usr/lib64/gconv/libJIS.so
/usr/lib64/gconv/libJISX0213.so
/usr/lib64/gconv/libKSC.so
/usr/lib64/gconv/MAC-CENTRALEUROPE.so
/usr/lib64/gconv/MACINTOSH.so
/usr/lib64/gconv/MAC-IS.so
/usr/lib64/gconv/MAC-SAMI.so
/usr/lib64/gconv/MAC-UK.so
/usr/lib64/gconv/MIK.so
/usr/lib64/gconv/NATS-DANO.so
/usr/lib64/gconv/NATS-SEFI.so
/usr/lib64/gconv/PT154.so
/usr/lib64/gconv/RK1048.so
/usr/lib64/gconv/SAMI-WS2.so
/usr/lib64/gconv/SHIFT_JISX0213.so
/usr/lib64/gconv/SJIS.so
/usr/lib64/gconv/T.61.so
/usr/lib64/gconv/TCVN5712-1.so
/usr/lib64/gconv/TIS-620.so
/usr/lib64/gconv/TSCII.so
/usr/lib64/gconv/UHC.so
/usr/lib64/gconv/UNICODE.so
/usr/lib64/gconv/UTF-16.so
/usr/lib64/gconv/UTF-32.so
/usr/lib64/gconv/UTF-7.so
/usr/lib64/gconv/VISCII.so
/usr/lib64/gconv/IBM858.so
/usr/lib64/glibc/getconf
/usr/lib64/ld-linux-x86-64.so.2
/usr/lib64/ld-2.39.so
/usr/lib64/libBrokenLocale.so.1
#/usr/lib64/libSegFault.so
/usr/lib64/libanl.so.1
/usr/lib64/libc.so.6
/usr/lib64/libc-2.39.so
/usr/lib64/libdl.so.2
/usr/lib64/libm.so.6
/usr/lib64/libmemusage.so
/usr/lib64/libnsl.so.1
/usr/lib64/libnss_dns.so.2
/usr/lib64/libnss_files.so.2
/usr/lib64/libnss_hesiod.so.2
/usr/lib64/libnss_compat.so
/usr/lib64/libnss_compat.so.2
/usr/lib64/libpcprofile.so
/usr/lib64/libpthread.so.0
/usr/lib64/libresolv.so.2
/usr/lib64/librt.so.1
/usr/lib64/libthread_db.so.1
/usr/lib64/libutil.so.1
/usr/lib64/libmvec.so
/usr/lib64/libmvec.so.1
%{_datadir}/defaults/etc/rpc

/usr/lib64/libm.so.6
/V3/usr/lib64/
/V4/usr/lib64/
/VA/usr/lib64/

/usr/bin/ldconfig
%exclude /var/cache/ldconfig

%files lib-avx2

# TODO: SPLIT!
%files locale
/usr/share/locale
%exclude /usr/share/locale/C.UTF-8
# NOTE: en_US.UTF-8 locale files are installed by libc6; avoid installing them
# in the -locale subpackage, because it triggers a bug in librpm that can
# corrupt file permissions and therefore lead to corrupt swupd update content...
%exclude /usr/share/locale/en_US.UTF-8
%exclude /usr/share/locale/locale-archive
%exclude /var/cache/locale/locale-archive
%{_datadir}/i18n
/usr/bin/localedef
/usr/lib64/gconv/DEC-MCS.so
/usr/lib64/gconv/EBCDIC-AT-DE-A.so
/usr/lib64/gconv/EBCDIC-AT-DE.so
/usr/lib64/gconv/EBCDIC-CA-FR.so
/usr/lib64/gconv/EBCDIC-DK-NO-A.so
/usr/lib64/gconv/EBCDIC-DK-NO.so
/usr/lib64/gconv/EBCDIC-ES-A.so
/usr/lib64/gconv/EBCDIC-ES.so
/usr/lib64/gconv/EBCDIC-ES-S.so
/usr/lib64/gconv/EBCDIC-FI-SE-A.so
/usr/lib64/gconv/EBCDIC-FI-SE.so
/usr/lib64/gconv/EBCDIC-FR.so
/usr/lib64/gconv/EBCDIC-IS-FRISS.so
/usr/lib64/gconv/EBCDIC-IT.so
/usr/lib64/gconv/EBCDIC-PT.so
/usr/lib64/gconv/EBCDIC-UK.so
/usr/lib64/gconv/EBCDIC-US.so
/usr/lib64/gconv/ECMA-CYRILLIC.so
/usr/lib64/gconv/IBM037.so
/usr/lib64/gconv/IBM038.so
/usr/lib64/gconv/IBM1004.so
/usr/lib64/gconv/IBM1008_420.so
/usr/lib64/gconv/IBM1008.so
/usr/lib64/gconv/IBM1025.so
/usr/lib64/gconv/IBM1026.so
/usr/lib64/gconv/IBM1046.so
/usr/lib64/gconv/IBM1047.so
/usr/lib64/gconv/IBM1097.so
/usr/lib64/gconv/IBM1112.so
/usr/lib64/gconv/IBM1122.so
/usr/lib64/gconv/IBM1123.so
/usr/lib64/gconv/IBM1124.so
/usr/lib64/gconv/IBM1129.so
/usr/lib64/gconv/IBM1130.so
/usr/lib64/gconv/IBM1132.so
/usr/lib64/gconv/IBM1133.so
/usr/lib64/gconv/IBM1137.so
/usr/lib64/gconv/IBM1140.so
/usr/lib64/gconv/IBM1141.so
/usr/lib64/gconv/IBM1142.so
/usr/lib64/gconv/IBM1143.so
/usr/lib64/gconv/IBM1144.so
/usr/lib64/gconv/IBM1145.so
/usr/lib64/gconv/IBM1146.so
/usr/lib64/gconv/IBM1147.so
/usr/lib64/gconv/IBM1148.so
/usr/lib64/gconv/IBM1149.so
/usr/lib64/gconv/IBM1153.so
/usr/lib64/gconv/IBM1154.so
/usr/lib64/gconv/IBM1155.so
/usr/lib64/gconv/IBM1156.so
/usr/lib64/gconv/IBM1157.so
/usr/lib64/gconv/IBM1158.so
/usr/lib64/gconv/IBM1160.so
/usr/lib64/gconv/IBM1161.so
/usr/lib64/gconv/IBM1162.so
/usr/lib64/gconv/IBM1163.so
/usr/lib64/gconv/IBM1164.so
/usr/lib64/gconv/IBM1166.so
/usr/lib64/gconv/IBM1167.so
/usr/lib64/gconv/IBM12712.so
/usr/lib64/gconv/IBM1364.so
/usr/lib64/gconv/IBM1371.so
/usr/lib64/gconv/IBM1388.so
/usr/lib64/gconv/IBM1390.so
/usr/lib64/gconv/IBM1399.so
/usr/lib64/gconv/IBM16804.so
/usr/lib64/gconv/IBM256.so
/usr/lib64/gconv/IBM273.so
/usr/lib64/gconv/IBM274.so
/usr/lib64/gconv/IBM275.so
/usr/lib64/gconv/IBM277.so
/usr/lib64/gconv/IBM278.so
/usr/lib64/gconv/IBM280.so
/usr/lib64/gconv/IBM281.so
/usr/lib64/gconv/IBM284.so
/usr/lib64/gconv/IBM285.so
/usr/lib64/gconv/IBM290.so
/usr/lib64/gconv/IBM297.so
/usr/lib64/gconv/IBM420.so
/usr/lib64/gconv/IBM423.so
/usr/lib64/gconv/IBM424.so
/usr/lib64/gconv/IBM437.so
/usr/lib64/gconv/IBM4517.so
/usr/lib64/gconv/IBM4899.so
/usr/lib64/gconv/IBM4909.so
/usr/lib64/gconv/IBM4971.so
/usr/lib64/gconv/IBM500.so
/usr/lib64/gconv/IBM5347.so
/usr/lib64/gconv/IBM803.so
/usr/lib64/gconv/IBM850.so
/usr/lib64/gconv/IBM851.so
/usr/lib64/gconv/IBM852.so
/usr/lib64/gconv/IBM855.so
/usr/lib64/gconv/IBM856.so
/usr/lib64/gconv/IBM857.so
/usr/lib64/gconv/IBM860.so
/usr/lib64/gconv/IBM861.so
/usr/lib64/gconv/IBM862.so
/usr/lib64/gconv/IBM863.so
/usr/lib64/gconv/IBM864.so
/usr/lib64/gconv/IBM865.so
/usr/lib64/gconv/IBM866NAV.so
/usr/lib64/gconv/IBM866.so
/usr/lib64/gconv/IBM868.so
/usr/lib64/gconv/IBM869.so
/usr/lib64/gconv/IBM870.so
/usr/lib64/gconv/IBM871.so
/usr/lib64/gconv/IBM874.so
/usr/lib64/gconv/IBM875.so
/usr/lib64/gconv/IBM880.so
/usr/lib64/gconv/IBM891.so
/usr/lib64/gconv/IBM901.so
/usr/lib64/gconv/IBM902.so
/usr/lib64/gconv/IBM9030.so
/usr/lib64/gconv/IBM903.so
/usr/lib64/gconv/IBM904.so
/usr/lib64/gconv/IBM905.so
/usr/lib64/gconv/IBM9066.so
/usr/lib64/gconv/IBM918.so
/usr/lib64/gconv/IBM921.so
/usr/lib64/gconv/IBM922.so
/usr/lib64/gconv/IBM930.so
/usr/lib64/gconv/IBM932.so
/usr/lib64/gconv/IBM933.so
/usr/lib64/gconv/IBM935.so
/usr/lib64/gconv/IBM937.so
/usr/lib64/gconv/IBM939.so
/usr/lib64/gconv/IBM943.so
/usr/lib64/gconv/IBM9448.so
/usr/lib64/gconv/GB18030.so
/usr/lib64/gconv/GBBIG5.so
/usr/lib64/gconv/GBGBK.so
/usr/lib64/gconv/GBK.so

%files dev
/usr/include/*.h
/usr/include/arpa/
/usr/include/bits/
/usr/include/gnu/
/usr/include/finclude/
/usr/include/net/
/usr/include/netash/
/usr/include/netatalk/
/usr/include/netax25/
/usr/include/neteconet/
/usr/include/netinet/
/usr/include/netipx/
/usr/include/netiucv/
/usr/include/netpacket/
/usr/include/netrom/
/usr/include/netrose/
/usr/include/nfs/
/usr/include/protocols/
/usr/include/rpc/
/usr/include/scsi/
/usr/include/sys/
/usr/lib64/Mcrt1.o
/usr/lib64/Scrt1.o
/usr/lib64/crt1.o
/usr/lib64/crti.o
/usr/lib64/crtn.o
/usr/lib64/gcrt1.o
/usr/lib64/grcrt1.o
/usr/lib64/rcrt1.o
/usr/lib64/libBrokenLocale.so
/usr/lib64/libanl.so
/usr/lib64/libc.so
/usr/lib64/libc_nonshared.a
/usr/lib64/libm.so
#/usr/lib64/libnsl.so
/usr/lib64/libresolv.so
/usr/lib64/libthread_db.so
/usr/lib64/libdl.a
/usr/lib64/libpthread.a
/usr/lib64/libpthread_nonshared.a
/usr/lib64/libmvec.a
/usr/lib64/libutil.a
/usr/lib64/librt.a

%files dev32
/usr/lib32/*.a
/usr/lib32/*.o

%files libc32
/usr/lib32/*.so
/usr/lib/ld-linux.so.2

/usr/lib32/glibc/getconf
/usr/lib32/gconv/
/usr/lib32/audit/sotruss-lib.so
/usr/lib32/ld-linux.so.2
/usr/lib32/libBrokenLocale.so.1
/usr/lib32/libanl.so.1
/usr/lib32/libc.so.6
/usr/lib32/libdl.so.2
/usr/lib32/libm.so.6
/usr/lib32/libnsl.so.1
/usr/lib32/libnss_db.so.2
/usr/lib32/libnss_dns.so.2
/usr/lib32/libnss_files.so.2
/usr/lib32/libnss_hesiod.so.2
/usr/lib32/libpthread.so.0
/usr/lib32/libresolv.so.2
/usr/lib32/librt.so.1
/usr/lib32/libthread_db.so.1
/usr/lib32/libutil.so.1
/usr/lib32/libnss_compat.so.2
/usr/lib32/libc_malloc_debug.so.0

%files staticdev
/usr/lib64/libBrokenLocale.a
/usr/lib64/libanl.a
/usr/lib64/libc.a
/usr/lib64/libg.a
#/usr/lib64/libieee.a
/usr/lib64/libm.a
/usr/lib64/libmcheck.a
/usr/lib64/libresolv.a
/usr/lib64/libm-2.39.a


%files doc
%{_infodir}/libc*.info*

%files extras
/usr/bin/makedb
/usr/lib64/libnss_db.so.2
/usr/lib64/libnss_db.so
#/usr/lib64/libnss_nis-2.39.so
#/usr/lib64/libnss_nis.so
#/usr/lib64/libnss_nis.so.2
#/usr/lib64/libnss_nisplus-2.39.so
#/usr/lib64/libnss_nisplus.so
#/usr/lib64/libnss_nisplus.so.2
%exclude %{_localstatedir}/db/Makefile

%files -n libc6-dev

