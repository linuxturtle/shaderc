#!/bin/sh
# Script to output a version string with the number of commits since the common
# ancestor appended to the manually hardcoded API version
BUILD_COMMIT_ID=upstream-unstable

CURRENT_BASE="2018.0-dev"
# There are no tags, so manually hardcode commit ID where CURRENT_BASE was created.
CURRENT_BASE_COMMIT="dbb0f14bcda1fc42a7cd9a3dd8d78d797b2d5448"

NB_OF_COMMITS=`git log --oneline $CURRENT_BASE_COMMIT..$BUILD_COMMIT_ID | wc -l`
echo "$CURRENT_BASE+$NB_OF_COMMITS"
