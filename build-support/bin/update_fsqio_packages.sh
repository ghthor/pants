#!/bin/bash

# Get version as arg. Test against a hardcoded upper bound (1.5.0 or whatever)
if [ -z ${1+x} ]; then
  echo "Pass the modules version. Check version.py but make sure that you are incrementing the version on PyPi!"
  exit -1
fi

# TODO(mateo): Error if upper bound is higher than the passed in version.
UPPER_BOUND='1.5.0'
LOWER_BOUND='1.0.0'

# Get the created buildgen modules
tarballs=$(find dist -name 'fsqio*.tar.gz')
# Sanity checks
[ ${#tarballs[@]} -eq 0 ] && echo "No buildgen packages found!" && exit -1

# Untar them.
for i in $tarballs; do echo "Untarring $i..." && tar xfz $i -C dist; done

# Get the files to update.
files=$(grep -Hlr "pantsbuild.pants==$1" dist)
for i in $files; do
  echo "Rewriting pantsbuild dependencies listed in $i..."
  sed -i "s/pantsbuild.pants==$1/pantsbuild.pants>=$LOWER_BOUND,<$UPPER_BOUND/g" $i
done

# This last bit does not quite work - but it is close. It was late at night and I gave up
# but all that is needed is to glob the filenames (with no path) as seen in "uncompressed" variable below.
# As written it returns things like './fsqio-buildgen....' which doesn't work. Super close though.

# Remake packages
# cd dist
# uncompressed=$(find . -name "fsqio*$1")
# for i in $uncompressed; do
#   # Remove the original packages to ensure we don't upload the unadjusted originals.
#   #rm -rf $1.tar.gz
#   [[ -d $i ]] || (echo "Could not find uncompressed directory!" && cd - && exit -2)
#   echo "Compressing $i..."
#   tar zcf $i.tar.gz $i
#   #rm -rf $i
# done
# cd -
