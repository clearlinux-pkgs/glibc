PKG_NAME := glibc
include ../common/Makefile.common

update:
	pushd ~/git/glibc ; git remote update -p ; git diff glibc-2.31..origin/release/2.31/master  > ~/clear/packages/glibc/glibc-stable-branch.patch ; popd
	git diff --exit-code  glibc-stable-branch.patch || bash ./update.sh
