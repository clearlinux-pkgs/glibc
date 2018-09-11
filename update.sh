#!/usr/bin/bash
git commit -m "stable branch update" glibc-stable-branch.patch
make bump
make koji-nowait
