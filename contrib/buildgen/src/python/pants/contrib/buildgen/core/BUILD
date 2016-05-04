# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

contrib_plugin(
  name='plugin',
  dependencies=[
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen_aggregate_targets',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen_base',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen_target_bag',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen_task',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:buildgen_timestamp',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:map_derived_targets',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:map_sources_to_addresses_mapper',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:source_analysis_task',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:symbol_tree',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core:third_party_map_util',
    'contrib/buildgen/src/python/fsqio/contrib/buildgen/core/subsystems:buildgen_subsystem',
    'src/python/pants/build_graph',
    'src/python/pants/goal:task_registrar',
  ],
  distribution_name='fsqio.pants.contrib.buildgen.core',
  description="Foursquare's Buildgen Pants plugin core module",
  additional_classifiers=[
    'Topic :: Software Development :: Code Generators'
  ],
  build_file_aliases=True,
  register_goals=True,
)
