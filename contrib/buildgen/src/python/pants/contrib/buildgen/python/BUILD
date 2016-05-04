# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

contrib_plugin(
  name='plugin',
  dependencies=[
    'contrib/buildgen/src/python/pants/contrib/buildgen/core:plugin',
    'contrib/buildgen/src/python/pants/contrib/buildgen/python:buildgen_python',
    'contrib/buildgen/src/python/pants/contrib/buildgen/python:map_python_exported_symbols',
    'contrib/buildgen/src/python/pants/contrib/buildgen/python:python_import_parser',
    'contrib/buildgen/src/python/pants/contrib/buildgen/python:third_party_map_python',
    'src/python/pants/build_graph',
    'src/python/pants/goal:task_registrar',
  ],
  distribution_name='fsqio.pants.contrib.buildgen.python',
  description="Foursquare's Buildgen Pants plugin for Python",
  additional_classifiers=[
    'Topic :: Software Development :: Code Generators'
  ],
  build_file_aliases=True,
  register_goals=True,
)
