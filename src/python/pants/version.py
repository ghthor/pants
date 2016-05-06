# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from pants.base.revision import Revision


<<<<<<< HEAD
VERSION = '1.1.0-pre5'
=======
VERSION = '1.0.1'

>>>>>>> 55ee845... Commit the changes needed to build buildgen modules

PANTS_SEMVER = Revision.semver(VERSION)
