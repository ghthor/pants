# coding=utf-8
# Copyright 2014 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import

from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task

from fsqio.contrib.buildgen.python.buildgen_python import BuildgenPython
from fsqio.contrib.buildgen.python.map_python_exported_symbols import MapPythonExportedSymbols


def build_file_aliases():
  return BuildFileAliases()


def register_goals():

  task(
    name='map-python-exported-symbols',
    action=MapPythonExportedSymbols,
  ).install()

  task(
    name='python',
    action=BuildgenPython,
  ).install('buildgen')
