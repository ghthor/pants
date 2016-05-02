# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import

import pkgutil
import sys


python_third_party_map = {
  'ansicolors': '3rdparty/python:ansicolors',
  'apache': {
    'aurora': '3rdparty/python:apache.aurora.client',
  },
  'apscheduler': '3rdparty/python:APScheduler',
  'argcomplete': '3rdparty/python:argcomplete',
  'astroid': '3rdparty/python:astroid',
  'bs4': '3rdparty/python:beautifulsoup4',
  'boto': '3rdparty/python:boto',
  'bson': '3rdparty/python:pymongo',
  'colors': '3rdparty/python:ansicolors',
  'concurrent': '3rdparty/python:futures',
  'configobj': '3rdparty/python:configobj',
  'cookies': '3rdparty/python:cookies',
  'coverage': '3rdparty/python:coverage',
  'dateutil': '3rdparty/python:python-dateutil',
  'docutils': '3rdparty/python:docutils',
  'dns': '3rdparty/python:dnspython',
  'fake_filesystem': '3rdparty/python:pyfakefs',
  'fake_filesystem_glob': '3rdparty/python:pyfakefs',
  'fake_filesystem_shutil': '3rdparty/python:pyfakefs',
  'fasteners': '3rdparty/python:fasteners',
  'flask': '3rdparty/python:flask',
  'fs_cython_multilogistic_regression': '3rdparty/python:fs-cython-multilogistic-regression',
  'futures': '3rdparty/python:futures',
  'gen': {
    'apache': {
      'aurora': '3rdparty/python:apache.aurora.client',
    },
  },
  'google': {
    'protobuf': '3rdparty/python:protobuf',
  },
  'gunicorn': '3rdparty/python:gunicorn',
  'jsoncomment': '3rdparty/python:jsoncomment',
  'jsonschema': '3rdparty/python:jsonschema',
  'kafka': '3rdparty/python:kafka-python',
  'kazoo': '3rdparty/python:kazoo',
  'keyczar': '3rdparty/python:python-keyczar',
  'lmdb': '3rdparty/python:lmdb',
  'luigi': '3rdparty/python:luigi',
  'lvm': '3rdparty/python:lvm',
  'lxml': '3rdparty/python:lxml',
  'mako': '3rdparty/python:Mako',
  'markdown': '3rdparty/python:Markdown',
  'mock': '3rdparty/python:mock',
  'motor': '3rdparty/python:motor',
  'mox': '3rdparty/python:mox',
  'path': '3rdparty/python:path',
  'pathspec': '3rdparty/python:pathspec',
  'pep8': '3rdparty/python:pep8',
  'pex': '3rdparty/python:pex',
  'phabricator': '3rdparty/python:phabricator',
  'psutil': '3rdparty/python:psutil',
  'psycopg2': '3rdparty/python:psycopg2',
  'pybindxml': '3rdparty/python:pybindxml',
  'pycurl': '3rdparty/python:pycurl',
  'pyflakes': '3rdparty/python:pyflakes',
  'pygments': '3rdparty/python:Pygments',
  'pymongo': '3rdparty/python:pymongo',
  'pymysql': '3rdparty/python:PyMySQL',
  'pysnmp': '3rdparty/python:pysnmp',
  'pystache': '3rdparty/python:pystache',
  'pytest': '3rdparty/python:pytest',
  'pytest-cov': '3rdparty/python:pytest-cov',
  'pywatchman': '3rdparty/python:pywatchman',
  'redis': '3rdparty/python:Redis',
  'repoze': '3rdparty/python:repoze.lru',
  'requests': '3rdparty/python:requests',
  'requests_futures': '3rdparty/python:requests-futures',
  'scrapy': '3rdparty/python:scrapy',
  'setproctitle': '3rdparty/python:setproctitle',
  'setuptools': '3rdparty/python:setuptools',
  'simplejson': '3rdparty/python:simplejson',
  'six': '3rdparty/python:six',
  'sqlalchemy': '3rdparty/python:SQLAlchemy',
  'supervisor': '3rdparty/python:supervisor',
  'thrift': '3rdparty/python:thrift',
  'tornado': '3rdparty/python:tornado',
  'tornadoredis': '3rdparty/python:tornado-redis',
  'toro': '3rdparty/python:toro',
  'twisted': '3rdparty/python:Twisted',
  'twitter': {
    'common': {
      'collections': '3rdparty/python:twitter.common.collections',
      'confluence': '3rdparty/python:twitter.common.confluence',
      'dirutil': '3rdparty/python:twitter.common.dirutil',
    },
  },
  'wheel': '3rdparty/python:wheel',
  'whoops': '3rdparty/python:whoops',
  'yaml': '3rdparty/python:PyYAML',
}


def get_system_modules(first_party_packages):
  """Return the list of all loaded modules that are not declared as first or third party libraries.

  Callers should cache this return value instead of recalculating repeatedly.
  :param list first_party_packages: A list of all package names produced by this repo, e.g. ['foursquare', 'fsqio']).
  """
  # Get list of all loaded modules.
  loaded_modules = [m for _, m, _ in list(pkgutil.iter_modules())]
  interpreter_modules = list(sys.builtin_module_names)
  modules = sorted(loaded_modules + interpreter_modules)

  # Filter out all modules that are declared as first or third party packages.
  return sorted([m for m in modules if m not in python_third_party_map and m not in first_party_packages])
