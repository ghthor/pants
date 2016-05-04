# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

contrib_plugin(
  name='plugin',
  dependencies=[
    'contrib/buildgen/src/python/pants/contrib/buildgen/core:plugin',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm:map_java_exported_symbols',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm:map_jvm_symbol_to_source_tree',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm:map_third_party_jar_symbols',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm:scalac_buildgen_task_mixin',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm:third_party_map_jvm',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm/scala:buildgen_scala',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm/scala:map_scala_library_used_addresses',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm/scala:scala_exported_symbols',
    'contrib/buildgen/src/python/pants/contrib/buildgen/jvm/scala:scala_used_symbols',
    'src/python/pants/build_graph',
    'src/python/pants/goal:task_registrar',
  ],
  distribution_name='fsqio.pants.contrib.buildgen.jvm',
  description="Foursquare's Buildgen Pants plugin for the JVM",
  additional_classifiers=[
    'Topic :: Software Development :: Code Generators'
  ],
  build_file_aliases=True,
  register_goals=True,
)
