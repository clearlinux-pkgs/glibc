PKG_NAME := glibc
URL :=http://mirrors.kernel.org/gnu/libc/glibc-2.27.tar.xz
include ../common/Makefile.common

update:
	pushd ~/git/glibc ; git remote update -p ; git diff glibc-2.28..origin/release/2.28/master  > ~/clear/packages/glibc/glibc-stable-branch.patch ; popd
	git diff --exit-code  glibc-stable-branch.patch || bash ./update.sh
