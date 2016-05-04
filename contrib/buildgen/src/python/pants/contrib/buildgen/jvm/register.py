# coding=utf-8
# Copyright 2014 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import

from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task

from fsqio.contrib.buildgen.jvm.map_java_exported_symbols import MapJavaExportedSymbols
from fsqio.contrib.buildgen.jvm.map_jvm_symbol_to_source_tree import MapJvmSymbolToSourceTree
from fsqio.contrib.buildgen.jvm.map_third_party_jar_symbols import MapThirdPartyJarSymbols
from fsqio.contrib.buildgen.jvm.scala.buildgen_scala import BuildgenScala
from fsqio.contrib.buildgen.jvm.scala.map_scala_library_used_addresses import (
  MapScalaLibraryUsedAddresses,
)
from fsqio.contrib.buildgen.jvm.scala.scala_exported_symbols import MapScalaExportedSymbols
from fsqio.contrib.buildgen.jvm.scala.scala_used_symbols import MapScalaUsedSymbols


def build_file_aliases():
  return BuildFileAliases()


def register_goals():

  task(
    name='map-third-party-jar-symbols',
    action=MapThirdPartyJarSymbols,
  ).install()

  task(
    name='map-scala-exported-symbols',
    action=MapScalaExportedSymbols,
  ).install()

  task(
    name='map-scala-used-symbols',
    action=MapScalaUsedSymbols,
  ).install()

  task(
    name='map-java-exported-symbols',
    action=MapJavaExportedSymbols,
  ).install()

  task(
    name='map-jvm-symbol-to-source-tree',
    action=MapJvmSymbolToSourceTree,
  ).install()

  task(
    name='map-scala-library-used-addresses',
    action=MapScalaLibraryUsedAddresses,
  ).install()

  task(
    name='scala',
    action=BuildgenScala,
  ).install('buildgen')
