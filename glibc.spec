%define keepstatic 1
%define glibc_target x86_64-generic-linux

Name:           glibc
Version:        2.22
Release:        78
License:        GPL-2.0
Summary:        GNU C library
Url:            http://www.gnu.org/software/libc/libc.html
Group:          libs
Source0:        http://ftp.gnu.org/gnu/glibc/glibc-2.22.tar.gz
Patch1:         0001-Add-avx2-fake-capability-like-tls.patch
Patch2:		ldso-malloc-size.patch
Patch3:         0001-Set-host.conf-multi-to-on-by-default.patch
Patch6:         skip-error-msg-ld.so.conf.patch
Patch7:         ldconfig-format-new.patch
Patch8:         ldconfig-do-not-search-non-lib64.patch
Patch9:         nsswitch-altfiles.patch
Patch10:        ld-so-cache-in-var.patch
Patch11:	fewerlocales.patch
Patch12:        mkdir-ldconfig.patch
Patch14:        locale-var-cache.patch
Patch15:	nonscd.patch
Patch16:	cve-2015-8777.patch
Patch17:	strcpy.patch
Patch18:	alternate_trim.patch
Patch19:	madvise-bss.patch


BuildRequires:  grep
BuildRequires:  texinfo
BuildRequires:  linux-libc-headers
BuildRequires:	gettext-dev
BuildRequires:	bison
BuildRequires:  libgd-dev


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
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1

%build
mkdir ../glibc-buildroot
cd ../glibc-buildroot

export CFLAGS="-O3 -march=westmere -mtune=haswell -g2 -m64  -Wl,-z,max-page-size=0x1000"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000"

../glibc-2.22/configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=%{_libdir}/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=%{_libdir} \
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
    libc_cv_slibdir=%{_libdir} \
    libc_cv_localedir=/usr/lib/locale

make %{?_smp_mflags}

%install

unset LDFLAGS
unset CFLAGS

pushd ../glibc-buildroot

make install DESTDIR=%{buildroot} install_root=%{buildroot}

for r in bootparam_prot.x nlm_prot.x rstat.x 	  yppasswd.x klm_prot.x rex.x sm_inter.x mount.x 	  rusers.x spray.x nfs_prot.x rquota.x key_prot.x; do
    h=`echo $r|sed -e's,\.x$,.h,'`
    install -m 0644 ./sunrpc/rpcsvc/$h %{buildroot}%{_includedir}/rpcsvc/
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

%check
pushd ../glibc-buildroot
make check %{?_smp_mflags} || :
popd


%files -n libc-bin
%{_bindir}/catchsegv
%{_bindir}/ldd
/sbin/sln

%files -n nscd
/usr/sbin/nscd

%files -n glibc-utils
%{_bindir}/locale
%{_bindir}/getconf
%{_bindir}/iconv
%{_bindir}/gencat
%{_bindir}/rpcgen
%{_bindir}/tzselect
%{_bindir}/getent
%{_bindir}/pcprofiledump
%{_bindir}/sprof
%{_bindir}/pldd
%exclude %{_bindir}/mtrace
%{_bindir}/sotruss
%{_bindir}/xtrace
/usr/sbin/zic
/usr/sbin/iconvconfig
/usr/sbin/zdump

%files -n libc6
%dir /usr/lib/locale
/usr/lib/locale/en_US.UTF-8
%{_libdir}/audit/sotruss-lib.so
%{_libdir}/gconv
%{_libdir}/glibc/getconf
%{_libdir}/ld-2.22.so
%{_libdir}/ld-linux-x86-64.so.2
%{_libdir}/libBrokenLocale-2.22.so
%{_libdir}/libBrokenLocale.so.1
%{_libdir}/libSegFault.so
%{_libdir}/libanl-2.22.so
%{_libdir}/libanl.so.1
%{_libdir}/libc-2.22.so
%{_libdir}/libc.so.6
%{_libdir}/libcidn-2.22.so
%{_libdir}/libcidn.so.1
%{_libdir}/libcrypt-2.22.so
%{_libdir}/libcrypt.so.1
%{_libdir}/libdl-2.22.so
%{_libdir}/libdl.so.2
%{_libdir}/libm-2.22.so
%{_libdir}/libm.so.6
%{_libdir}/libmemusage.so
%{_libdir}/libnsl-2.22.so
%{_libdir}/libnsl.so.1
%{_libdir}/libnss_compat-2.22.so
%{_libdir}/libnss_compat.so.2
%{_libdir}/libnss_dns-2.22.so
%{_libdir}/libnss_dns.so.2
%{_libdir}/libnss_files-2.22.so
%{_libdir}/libnss_files.so.2
%{_libdir}/libnss_hesiod-2.22.so
%{_libdir}/libnss_hesiod.so.2
%{_libdir}/libnss_nis-2.22.so
%{_libdir}/libnss_nis.so.2
%{_libdir}/libnss_nisplus-2.22.so
%{_libdir}/libnss_nisplus.so.2
%{_libdir}/libpcprofile.so
%{_libdir}/libpthread-2.22.so
%{_libdir}/libpthread.so.0
%{_libdir}/libresolv-2.22.so
%{_libdir}/libresolv.so.2
%{_libdir}/librt-2.22.so
%{_libdir}/librt.so.1
%{_libdir}/libthread_db-1.0.so
%{_libdir}/libthread_db.so.1
%{_libdir}/libutil-2.22.so
%{_libdir}/libutil.so.1
/usr/lib64/libmvec-2.22.so
/usr/lib64/libmvec.so
/usr/lib64/libmvec.so.1
%{_datadir}/defaults/etc/rpc

/sbin/ldconfig
%dir /var/cache/ldconfig

# TODO: SPLIT!
%files -n libc6-locale
%{_datadir}/locale
/usr/lib/locale/locale-archive
/var/cache/locale/locale-archive
%{_datadir}/i18n
%{_bindir}/localedef

%files -n libc6-dev
%{_includedir}/*.h
%{_includedir}/arpa/
%{_includedir}/bits/
%{_includedir}/gnu/
%{_includedir}/net/
%{_includedir}/netash/
%{_includedir}/netatalk/
%{_includedir}/netax25/
%{_includedir}/neteconet/
%{_includedir}/netinet/
%{_includedir}/netipx/
%{_includedir}/netiucv/
%{_includedir}/netpacket/
%{_includedir}/netrom/
%{_includedir}/netrose/
%{_includedir}/nfs/
%{_includedir}/protocols/
%{_includedir}/rpc/
%{_includedir}/rpcsvc/
%{_includedir}/scsi/
%{_includedir}/sys/
%{_libdir}/Mcrt1.o
%{_libdir}/Scrt1.o
%{_libdir}/crt1.o
%{_libdir}/crti.o
%{_libdir}/crtn.o
%{_libdir}/gcrt1.o
%{_libdir}/libBrokenLocale.so
%{_libdir}/libanl.so
%{_libdir}/libc.so
%{_libdir}/libc_nonshared.a
%{_libdir}/libcidn.so
%{_libdir}/libcrypt.so
%{_libdir}/libdl.so
%{_libdir}/libm.so
%{_libdir}/libnsl.so
%{_libdir}/libnss_compat.so
%{_libdir}/libnss_dns.so
%{_libdir}/libnss_files.so
%{_libdir}/libnss_hesiod.so
%{_libdir}/libnss_nis.so
%{_libdir}/libnss_nisplus.so
%{_libdir}/libpthread.so
%{_libdir}/libpthread_nonshared.a
%{_libdir}/libresolv.so
%{_libdir}/librt.so
%{_libdir}/libthread_db.so
%{_libdir}/libutil.so

%files -n glibc-staticdev
%{_libdir}/libBrokenLocale.a
%{_libdir}/libanl.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%{_libdir}/libm.a
%{_libdir}/libmcheck.a
%{_libdir}/libnsl.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librpcsvc.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

/usr/lib64/libmvec.a


%files doc
%{_infodir}/libc*.info*

%files extras
%{_bindir}/makedb
%{_libdir}/libnss_db-2.22.so
%{_libdir}/libnss_db.so.2
%{_libdir}/libnss_db.so
%exclude %{_localstatedir}/db/Makefile

