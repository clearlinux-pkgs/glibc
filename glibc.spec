%define keepstatic 1
%define glibc_target x86_64-generic-linux

Name:           glibc
Version:        2.25
Release:        122
License:        GPL-2.0
Summary:        GNU C library
Url:            http://www.gnu.org/software/libc/libc.html
Group:          libs
Source0:        http://ftp.gnu.org/gnu/glibc/glibc-2.25.tar.gz
Patch1:         0001-Check-if-SSE-is-available-with-HAS_CPU_FEATURE.patch
Patch2:         0002-Add-sysdeps-x86-dl-procinfo.c.patch
Patch3:         0003-x86-Set-dl_platform-and-dl_hwcap-from-CPU-features.patch
Patch4:         0001-Set-host.conf-multi-to-on-by-default.patch
Patch6:         skip-error-msg-ld.so.conf.patch
Patch7:         ldconfig-format-new.patch
Patch8:         0001-sysdeps-unix-Add-support-for-usr-lib32-as-a-system-l.patch
Patch9:         nsswitch-altfiles.patch
Patch10:        ld-so-cache-in-var.patch
Patch11:	    fewerlocales.patch
Patch12:        mkdir-ldconfig.patch
Patch13:        locale-var-cache.patch
Patch14:	    nonscd.patch
Patch15:	    fix_cpp_building.patch
Patch16:	    alternate_trim.patch
Patch17:	    madvise-bss.patch
Patch19:	    spinaphore.patch
Patch20:	    tzselect-proper-zone-file.patch
Patch21:	    large-page-huge-page.patch
Patch22:	    cve-2016-6323.nopatch
Patch23:	use_madv_free.patch
Patch24:	malloc_tune.patch
Patch25:	prefer_erms.patch
Patch26:	0001-misc-Support-fallback-stateless-shells-path-in-absen.patch


Patch100:       CVE-2016-10228.nopatch

BuildRequires:  grep
BuildRequires:  texinfo
BuildRequires:  linux-libc-headers
BuildRequires:	gettext-dev
BuildRequires:	bison
BuildRequires:  gcc-dev32 gcc-libgcc32 gcc-libstdc++32


%description
GNU C library.

%package doc
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          doc

%description doc
GNU C library.

%package -n libc-bin
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          libs
Provides:       catchsegv
Provides:       sln
Provides:       ldd

%description -n libc-bin
GNU C library.

%package -n libc6-locale
License:        GPL-2.0 and LGPL-2.1
Summary:        GNU C library
Group:          libs

%description -n libc6-locale
GNU C library.

%package -n nscd
License:        GPL-2.0
Summary:        GNU C library
Group:          libs

%description -n nscd
GNU C library.

%package -n glibc-utils
License:        GPL-2.0
Summary:        GNU C library
Group:          libs
Provides:       eglibc-utils

%description -n glibc-utils
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
# to provide nss_altfiles for passwd aka root account
Requires:       clr-systemd-config-data

%description -n libc6
GNU C library.

%package -n libc6-dev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel

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

%package -n glibc-staticdev
License:        GPL-2.0
Summary:        GNU C library
Group:          devel
Provides:       eglibc-staticdev

%description -n glibc-staticdev
GNU C library.

%package extras
Summary:        extra components for glibc
Group:          libs

%description extras
GNU C library extra components.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
#%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
#%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
#%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1




%build
export SOURCE_DATE_EPOCH=1484361909

mkdir ../glibc-buildroot
pushd ../glibc-buildroot

export CFLAGS="-O3 -march=westmere -mtune=haswell -g2 -m64  -Wl,-z,max-page-size=0x1000"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000"

../glibc-2.25/configure \
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
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/lib/locale

make %{?_smp_mflags}
popd

mkdir ../glibc-buildroot32
pushd ../glibc-buildroot32

export CFLAGS="-O3 -m32 -march=westmere -mtune=haswell -g2  -Wl,-z,max-page-size=0x1000 -m32"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000"

../glibc-2.25/configure \
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

make install DESTDIR=%{buildroot} install_root=%{buildroot}
popd

pushd ../glibc-buildroot

make install DESTDIR=%{buildroot} install_root=%{buildroot}

for r in bootparam_prot.x nlm_prot.x rstat.x 	  yppasswd.x klm_prot.x rex.x sm_inter.x mount.x 	  rusers.x spray.x nfs_prot.x rquota.x key_prot.x; do
    h=`echo $r|sed -e's,\.x$,.h,'`
    install -m 0644 ./sunrpc/rpcsvc/$h %{buildroot}/usr/include/rpcsvc/
done

mkdir -p %{buildroot}/var/cache/locale

iconvconfig --prefix=%{buildroot}

make localedata/install-locales  DESTDIR=%{buildroot} install_root=%{buildroot}

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

%files -n libc-bin
/usr/bin/catchsegv
/usr/bin/ldd
/sbin/sln

%files -n nscd
/usr/sbin/nscd

%files -n glibc-utils
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
/usr/lib64/gconv
/usr/lib64/glibc/getconf
/usr/lib64/ld-2.25.so
/usr/lib64/ld-linux-x86-64.so.2
/usr/lib64/libBrokenLocale-2.25.so
/usr/lib64/libBrokenLocale.so.1
/usr/lib64/libSegFault.so
/usr/lib64/libanl-2.25.so
/usr/lib64/libanl.so.1
/usr/lib64/libc-2.25.so
/usr/lib64/libc.so.6
/usr/lib64/libcidn-2.25.so
/usr/lib64/libcidn.so.1
/usr/lib64/libcrypt-2.25.so
/usr/lib64/libcrypt.so.1
/usr/lib64/libdl-2.25.so
/usr/lib64/libdl.so.2
/usr/lib64/libm-2.25.so
/usr/lib64/libm.so.6
/usr/lib64/libmemusage.so
/usr/lib64/libnsl-2.25.so
/usr/lib64/libnsl.so.1
/usr/lib64/libnss_compat-2.25.so
/usr/lib64/libnss_compat.so.2
/usr/lib64/libnss_dns-2.25.so
/usr/lib64/libnss_dns.so.2
/usr/lib64/libnss_files-2.25.so
/usr/lib64/libnss_files.so.2
/usr/lib64/libnss_hesiod-2.25.so
/usr/lib64/libnss_hesiod.so.2
/usr/lib64/libnss_nis-2.25.so
/usr/lib64/libnss_nis.so.2
/usr/lib64/libnss_nisplus-2.25.so
/usr/lib64/libnss_nisplus.so.2
/usr/lib64/libpcprofile.so
/usr/lib64/libpthread-2.25.so
/usr/lib64/libpthread.so.0
/usr/lib64/libresolv-2.25.so
/usr/lib64/libresolv.so.2
/usr/lib64/librt-2.25.so
/usr/lib64/librt.so.1
/usr/lib64/libthread_db-1.0.so
/usr/lib64/libthread_db.so.1
/usr/lib64/libutil-2.25.so
/usr/lib64/libutil.so.1
/usr/lib64/libmvec-2.25.so
/usr/lib64/libmvec.so
/usr/lib64/libmvec.so.1
%{_datadir}/defaults/etc/rpc

/sbin/ldconfig
%exclude /var/cache/ldconfig

# TODO: SPLIT!
%files -n libc6-locale
/usr/lib/locale
/usr/lib/locale/locale-archive
%exclude /var/cache/locale/locale-archive
%{_datadir}/i18n
/usr/bin/localedef

%files -n libc6-dev
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
/usr/lib64/libnss_compat.so
/usr/lib64/libnss_dns.so
/usr/lib64/libnss_files.so
/usr/lib64/libnss_hesiod.so
/usr/lib64/libnss_nis.so
/usr/lib64/libnss_nisplus.so
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
/usr/lib32/libnss_compat.so.2
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


%files -n glibc-staticdev
/usr/lib64/libBrokenLocale.a
/usr/lib64/libanl.a
/usr/lib64/libc.a
/usr/lib64/libcrypt.a
/usr/lib64/libdl.a
/usr/lib64/libg.a
/usr/lib64/libieee.a
/usr/lib64/libm.a
/usr/lib64/libmcheck.a
/usr/lib64/libnsl.a
/usr/lib64/libpthread.a
/usr/lib64/libresolv.a
/usr/lib64/librpcsvc.a
/usr/lib64/librt.a
/usr/lib64/libutil.a
/usr/lib64/libm-2.25.a
/usr/lib64/libmvec.a


%files doc
%{_infodir}/libc*.info*

%files extras
/usr/bin/makedb
/usr/lib64/libnss_db-2.25.so
/usr/lib64/libnss_db.so.2
/usr/lib64/libnss_db.so
%exclude %{_localstatedir}/db/Makefile

