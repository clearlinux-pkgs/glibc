PKG_NAME := glibc

include ../common/Makefile.common

GLIBC_GIT = ~/git/glibc
GLIBC_VER = 2.34

GLIBC_TAG = glibc-$(GLIBC_VER)
GLIBC_BRANCH = origin/release/$(GLIBC_VER)/master

update:
	test -d $(GLIBC_GIT) || git clone https://sourceware.org/git/glibc.git $(GLIBC_GIT)
	git -C $(GLIBC_GIT) remote update -p
	git -C $(GLIBC_GIT) rev-parse --verify --quiet refs/tags/$(GLIBC_TAG) > /dev/null
	git -C $(GLIBC_GIT) rev-parse --verify --quiet $(GLIBC_BRANCH) > /dev/null
	git -C $(GLIBC_GIT) shortlog $(GLIBC_TAG)..$(GLIBC_BRANCH) > glibc-stable-branch.patch
	git -C $(GLIBC_GIT) diff $(GLIBC_TAG)..$(GLIBC_BRANCH) >> glibc-stable-branch.patch
	! git diff --quiet glibc-stable-branch.patch
	git -C $(GLIBC_GIT) describe --abbrev=10 --match 'glibc-*' $(GLIBC_BRANCH) > REVISION
	$(MAKE) bumpnogit
	git commit -m "stable update to `cat REVISION`" -a
	test -n "$(NO_KOJI)" || $(MAKE) koji-nowait
