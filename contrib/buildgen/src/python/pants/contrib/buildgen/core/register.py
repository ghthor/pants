# coding=utf-8
# Copyright 2014 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import

from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.task_registrar import TaskRegistrar as task

from fsqio.contrib.buildgen.core.buildgen import Buildgen
from fsqio.contrib.buildgen.core.buildgen_aggregate_targets import BuildgenAggregateTargets
from fsqio.contrib.buildgen.core.buildgen_target_bag import BuildgenTargetBag
from fsqio.contrib.buildgen.core.buildgen_timestamp import BuildgenTimestamp
from fsqio.contrib.buildgen.core.map_derived_targets import MapDerivedTargets
from fsqio.contrib.buildgen.core.map_sources_to_addresses_mapper import MapSourcesToAddressesMapper


def build_file_aliases():
  return BuildFileAliases(
    targets={
      'buildgen_target_bag': BuildgenTargetBag,
    },
  )

def register_goals():

  task(
    name='map-derived-targets',
    action=MapDerivedTargets,
  ).install()

  task(
    name='map-sources-to-addresses-mapper',
    action=MapSourcesToAddressesMapper,
  ).install()

  task(
    name='buildgen',
    action=Buildgen,
  ).install()

  task(
    name='aggregate-targets',
    action=BuildgenAggregateTargets,
  ).install('buildgen')

  task(
    name='timestamp',
    action=BuildgenTimestamp,
  ).install('buildgen')
