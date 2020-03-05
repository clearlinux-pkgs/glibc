PKG_NAME := glibc
include ../common/Makefile.common

GLIBC_GIT = ~/git/glibc

update:
	git -C $(GLIBC_GIT) remote update -p
	git -C $(GLIBC_GIT) diff glibc-2.30..origin/release/2.30/master > glibc-stable-branch.patch
	git diff --exit-code glibc-stable-branch.patch || bash ./update.sh
