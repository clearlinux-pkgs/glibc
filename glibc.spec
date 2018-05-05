%define keepstatic 1
%define glibc_target x86_64-generic-linux

Name:           glibc
Version:        2.27
Release:        176
License:        GPL-2.0
Summary:        GNU C library
Url:            http://www.gnu.org/software/libc/libc.html
Group:          libs
Source0:        http://ftp.gnu.org/gnu/glibc/glibc-2.27.tar.gz


Patch4:		0001-Set-host.conf-multi-to-on-by-default.patch
Patch6:		skip-error-msg-ld.so.conf.patch
Patch7:		ldconfig-format-new.patch
Patch8:		0001-sysdeps-unix-Add-support-for-usr-lib32-as-a-system-l.patch
Patch9:		nsswitch-altfiles.patch
Patch10:	ld-so-cache-in-var.patch
Patch11:	fewerlocales.patch
Patch12:	mkdir-ldconfig.patch
Patch13:	locale-var-cache.patch
Patch14:	nonscd.patch
Patch17:	alternate_trim.patch
Patch18:	madvise-bss.patch
Patch19:	spinaphore.patch
Patch20:	tzselect-proper-zone-file.patch
Patch21:	large-page-huge-page.patch
Patch23:	use_madv_free.patch
Patch24:	malloc_tune.patch
Patch26:	0001-misc-Support-fallback-stateless-shells-path-in-absen.patch
#Patch27:	ldconfig-Os.patch
Patch28:	stateless.patch
Patch29:	nsswitch-altfiles-bugfix.patch
Patch32:	mathlto.patch
Patch35:	vzeroupper-2.27.patch
# backports of libm work
Patch38:        0001-x86-64-Remove-sysdeps-x86_64-fpu-s_sinf.S.patch
Patch39:        0001-sin-cos-slow-paths-avoid-slow-paths-for-small-inputs.patch
Patch40:        0002-sin-cos-slow-paths-remove-large-range-reduction.patch
Patch41:        0003-sin-cos-slow-paths-remove-slow-paths-from-small-rang.patch
Patch42:        0004-sin-cos-slow-paths-remove-slow-paths-from-huge-range.patch
Patch43:        0005-sin-cos-slow-paths-remove-unused-slowpath-functions.patch
Patch44:        0006-sin-cos-slow-paths-refactor-duplicated-code-into-dos.patch
Patch45:        0007-sin-cos-slow-paths-refactor-sincos-implementation.patch
Patch50:	pause.patch
Patch51:        gcc-8-fix.patch

BuildRequires:	grep
BuildRequires:	texinfo
BuildRequires:	linux-libc-headers
BuildRequires:	gettext-dev
BuildRequires:	bison
BuildRequires:	gcc-dev32 gcc-libgcc32 gcc-libstdc++32
BuildRequires:	python3-dev


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
Obsoletes:	libc-bin

%description bin
GNU C library.

%package locale
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          libs
Provides:	libc6-locale
Obsoletes:	libc6-locale

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

%package -n libc6
License:        GPL-2.0
Summary:        GNU C library
Group:          libs
Requires(pre):       filesystem
Provides:       glibc
Provides:       libcidn1
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

%description dev
GNU C library.

%package -n libc6-dev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Provides:	libc6-dev
Requires: glibc-dev

%description -n libc6-dev
GNU C library.

%package dev32
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Requires:	glibc-libc32
Requires:	libc6-dev

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

%description staticdev
GNU C library.

%package extras
Summary:        extra components for glibc
Group:          libs

%description extras
GNU C library extra components.

%prep
%setup -q
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch24 -p1
%patch26 -p1
#%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch32 -p1
%patch35 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch50 -p1
%patch51 -p1

%build
export SOURCE_DATE_EPOCH=1484361909
export LANG=C

mkdir ../glibc-buildroot
pushd ../glibc-buildroot

export CFLAGS="-O3 -march=westmere -mtune=skylake -g2 -m64  -Wl,-z,max-page-size=0x1000 "
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.27/configure \
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
    --localedir=/usr/lib/locale \
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
    --enable-lock-elision=yes \
    --enable-bind-now  \
    --enable-tunables \
    --enable-stack-protector=strong \
    --enable-obsolete-nsl \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/lib/locale

make %{?_smp_mflags}
popd


mkdir ../glibc-buildroot-avx2
pushd ../glibc-buildroot-avx2

export CFLAGS="-O3 -march=haswell -mtune=skylake -g2 -m64  -Wl,-z,max-page-size=0x1000 "
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.27/configure \
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
    --localedir=/usr/lib/locale \
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
    --enable-lock-elision=yes \
    --enable-bind-now  \
    --enable-tunables \
    --enable-stack-protector=strong \
    --enable-obsolete-nsl \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/lib/locale

make %{?_smp_mflags}
popd

mkdir ../glibc-buildroot-avx512
pushd ../glibc-buildroot-avx512

export CFLAGS="-O3 -march=skylake-avx512 -mtune=skylake -g2 -m64  -Wl,-z,max-page-size=0x1000 "
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../glibc-2.27/configure \
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
    --localedir=/usr/lib/locale \
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
    --enable-lock-elision=yes \
    --enable-bind-now  \
    --enable-tunables \
    --enable-stack-protector=strong \
    --enable-obsolete-nsl \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/lib/locale

make %{?_smp_mflags}
popd

mkdir ../glibc-buildroot32
pushd ../glibc-buildroot32

unset ASFLAGS
export CFLAGS="-O3 -m32 -march=westmere -mtune=skylake -g2  -Wl,-z,max-page-size=0x1000 -m32"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000"

../glibc-2.27/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib32/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib32 \
    --localedir=/usr/lib/locale \
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
    --enable-lock-elision=yes \
    --enable-bind-now  \
    --enable-tunables \
    --enable-stack-protector=strong \
    --enable-obsolete-nsl \
    libc_cv_slibdir=/usr/lib32 \
    libc_cv_complocaledir=/usr/lib/locale \
    CC="gcc -m32" CXX="g++ -m32" i686-linux-gnu


make %{?_smp_mflags}
popd

%install
export SOURCE_DATE_EPOCH=1484361909

unset LDFLAGS
unset CFLAGS

# first we install the 32 bit build, so that any overlap gets resolved in
# favor of the 64 bit build
pushd ../glibc-buildroot32

make install DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}
popd

pushd ../glibc-buildroot-avx2
mkdir -p %{buildroot}/usr/lib64/haswell
cp math/libm.so %{buildroot}/usr/lib64/haswell/libm-2.27.so
cp mathvec/libmvec.so %{buildroot}/usr/lib64/haswell/libmvec-2.27.so
cp crypt/libcrypt.so %{buildroot}/usr/lib64/haswell/libcrypt-2.27.so
cp libc.so  %{buildroot}/usr/lib64/haswell/libc-2.27.so
ln -s libm-2.27.so %{buildroot}/usr/lib64/haswell/libm.so.6
ln -s libmvec-2.27.so %{buildroot}/usr/lib64/haswell/libmvec.so.1
ln -s libcrypt-2.27.so %{buildroot}/usr/lib64/haswell/libcrypt.so.1
ln -s libc-2.27.so  %{buildroot}/usr/lib64/haswell/libc.so.6
popd

pushd ../glibc-buildroot-avx512
mkdir -p %{buildroot}/usr/lib64/haswell/avx512_1
cp math/libm.so %{buildroot}/usr/lib64/haswell/avx512_1/libm-2.27.so
cp mathvec/libmvec.so %{buildroot}/usr/lib64/haswell/avx512_1/libmvec-2.27.so
ln -s libm-2.27.so %{buildroot}/usr/lib64/haswell/avx512_1/libm.so.6
ln -s libmvec-2.27.so %{buildroot}/usr/lib64/haswell/avx512_1/libmvec.so.1
popd



pushd ../glibc-buildroot

make install DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}

for r in bootparam_prot.x nlm_prot.x rstat.x 	  yppasswd.x klm_prot.x rex.x sm_inter.x mount.x 	  rusers.x spray.x nfs_prot.x rquota.x key_prot.x; do
    h=`echo $r|sed -e's,\.x$,.h,'`
    install -m 0644 ./sunrpc/rpcsvc/$h %{buildroot}/usr/include/rpcsvc/
done

mkdir -p %{buildroot}/var/cache/locale

iconvconfig --prefix=%{buildroot}

make localedata/install-locales  DESTDIR=%{buildroot} install_root=%{buildroot}  %{?_smp_mflags}

# Make ldconfig not fail
install -d %{buildroot}/var/cache/ldconfig

install -d %{buildroot}%{_datadir}/defaults/etc/
mv %{buildroot}%{_sysconfdir}/rpc %{buildroot}%{_datadir}/defaults/etc/rpc

popd

pushd localedata
# Generate out of locale-archive an (en_US.) UTF-8 locale
mkdir -p %{buildroot}/usr/lib/locale
I18NPATH=. GCONV_PATH=../../glibc-buildroot/iconvdata LC_ALL=C ../../glibc-buildroot/locale/localedef --no-archive --prefix=%{buildroot} --alias-file=../intl/locale.alias -i locales/en_US -c -f charmaps/UTF-8 en_US.UTF-8
mv %{buildroot}/usr/lib/locale/en_US.utf8 %{buildroot}/usr/lib/locale/en_US.UTF-8
popd

ln -sfv /var/cache/locale/locale-archive %{buildroot}/usr/lib/locale/locale-archive

mkdir -p %{buildroot}/usr/lib
ln -s ../lib32/ld-linux.so.2  %{buildroot}/usr/lib/ld-linux.so.2


%check
pushd ../glibc-buildroot
make check %{?_smp_mflags} || :
popd

%files bin
/usr/bin/catchsegv
/usr/bin/ldd
/sbin/sln

%files nscd
/usr/sbin/nscd

%files utils
/usr/bin/locale
/usr/bin/getconf
/usr/bin/iconv
/usr/bin/gencat
/usr/bin/rpcgen
/usr/bin/tzselect
/usr/bin/getent
/usr/bin/pcprofiledump
/usr/bin/sprof
/usr/bin/pldd
%exclude /usr/bin/mtrace
/usr/bin/sotruss
/usr/bin/xtrace
/usr/sbin/zic
/usr/sbin/iconvconfig
/usr/sbin/zdump

%files -n libc6
%dir /usr/lib/locale
/usr/lib/locale/en_US.UTF-8
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
/usr/lib64/gconv/gconv-modules.cache
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
/usr/lib64/ld-2.27.so
/usr/lib64/ld-linux-x86-64.so.2
/usr/lib64/libBrokenLocale-2.27.so
/usr/lib64/libBrokenLocale.so.1
/usr/lib64/libSegFault.so
/usr/lib64/libanl-2.27.so
/usr/lib64/libanl.so.1
/usr/lib64/libc-2.27.so
/usr/lib64/libc.so.6
/usr/lib64/libcidn-2.27.so
/usr/lib64/libcidn.so.1
/usr/lib64/libcrypt-2.27.so
/usr/lib64/libcrypt.so.1
/usr/lib64/libdl-2.27.so
/usr/lib64/libdl.so.2
/usr/lib64/libm-2.27.so
/usr/lib64/libm.so.6
/usr/lib64/libmemusage.so
/usr/lib64/libnsl-2.27.so
/usr/lib64/libnsl.so.1
/usr/lib64/libnss_dns-2.27.so
/usr/lib64/libnss_dns.so.2
/usr/lib64/libnss_files-2.27.so
/usr/lib64/libnss_files.so.2
/usr/lib64/libnss_hesiod-2.27.so
/usr/lib64/libnss_hesiod.so.2
/usr/lib64/libnss_compat-2.27.so
/usr/lib64/libnss_compat.so
/usr/lib64/libnss_compat.so.2
/usr/lib64/libpcprofile.so
/usr/lib64/libpthread-2.27.so
/usr/lib64/libpthread.so.0
/usr/lib64/libresolv-2.27.so
/usr/lib64/libresolv.so.2
/usr/lib64/librt-2.27.so
/usr/lib64/librt.so.1
/usr/lib64/libthread_db-1.0.so
/usr/lib64/libthread_db.so.1
/usr/lib64/libutil-2.27.so
/usr/lib64/libutil.so.1
/usr/lib64/libmvec-2.27.so
/usr/lib64/libmvec.so
/usr/lib64/libmvec.so.1
%{_datadir}/defaults/etc/rpc

/usr/lib64/haswell/libm-2.27.so
/usr/lib64/haswell/libm.so.6

/sbin/ldconfig
%exclude /var/cache/ldconfig

%files lib-avx2
/usr/lib64/haswell/libmvec*
/usr/lib64/haswell/libc*
/usr/lib64/haswell/avx512_1/*

# TODO: SPLIT!
%files locale
/usr/lib/locale
%exclude /usr/lib/locale/locale-archive
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
/usr/include/rpcsvc/
/usr/include/scsi/
/usr/include/sys/
/usr/lib64/Mcrt1.o
/usr/lib64/Scrt1.o
/usr/lib64/crt1.o
/usr/lib64/crti.o
/usr/lib64/crtn.o
/usr/lib64/gcrt1.o
/usr/lib64/libBrokenLocale.so
/usr/lib64/libanl.so
/usr/lib64/libc.so
/usr/lib64/libc_nonshared.a
/usr/lib64/libcidn.so
/usr/lib64/libcrypt.so
/usr/lib64/libdl.so
/usr/lib64/libm.so
/usr/lib64/libmvec_nonshared.a
/usr/lib64/libnsl.so
/usr/lib64/libnss_dns.so
/usr/lib64/libnss_files.so
/usr/lib64/libnss_hesiod.so
/usr/lib64/libpthread.so
/usr/lib64/libpthread_nonshared.a
/usr/lib64/libresolv.so
/usr/lib64/librt.so
/usr/lib64/libthread_db.so
/usr/lib64/libutil.so

%files dev32
/usr/lib32/*.a
/usr/lib32/*.so
/usr/lib32/*.o

%files libc32
/usr/lib/ld-linux.so.2
/usr/bin/lddlibc4

/usr/lib32/glibc/getconf
/usr/lib32/gconv/
/usr/lib32/audit/sotruss-lib.so
/usr/lib32/ld-linux.so.2
/usr/lib32/libBrokenLocale.so.1
/usr/lib32/libanl.so.1
/usr/lib32/libc.so.6
/usr/lib32/libcidn.so.1
/usr/lib32/libcrypt.so.1
/usr/lib32/libdl.so.2
/usr/lib32/libm.so.6
/usr/lib32/libnsl.so.1
/usr/lib32/libnss_db.so.2
/usr/lib32/libnss_dns.so.2
/usr/lib32/libnss_files.so.2
/usr/lib32/libnss_hesiod.so.2
/usr/lib32/libnss_nis.so.2
/usr/lib32/libnss_nisplus.so.2
/usr/lib32/libpthread.so.0
/usr/lib32/libresolv.so.2
/usr/lib32/librt.so.1
/usr/lib32/libthread_db.so.1
/usr/lib32/libutil.so.1
/usr/lib32/libnss_compat.so.2

%files staticdev
/usr/lib64/libBrokenLocale.a
/usr/lib64/libanl.a
/usr/lib64/libc.a
/usr/lib64/libcrypt.a
/usr/lib64/libdl.a
/usr/lib64/libg.a
#/usr/lib64/libieee.a
/usr/lib64/libm.a
/usr/lib64/libmcheck.a
/usr/lib64/libnsl.a
/usr/lib64/libpthread.a
/usr/lib64/libresolv.a
/usr/lib64/librpcsvc.a
/usr/lib64/librt.a
/usr/lib64/libutil.a
/usr/lib64/libm-2.27.a
/usr/lib64/libmvec.a


%files doc
%{_infodir}/libc*.info*

%files extras
/usr/bin/makedb
/usr/lib64/libnss_db-2.27.so
/usr/lib64/libnss_db.so.2
/usr/lib64/libnss_db.so
/usr/lib64/libnss_nis-2.27.so
/usr/lib64/libnss_nis.so
/usr/lib64/libnss_nis.so.2
/usr/lib64/libnss_nisplus-2.27.so
/usr/lib64/libnss_nisplus.so
/usr/lib64/libnss_nisplus.so.2
%exclude %{_localstatedir}/db/Makefile

%files -n libc6-dev

