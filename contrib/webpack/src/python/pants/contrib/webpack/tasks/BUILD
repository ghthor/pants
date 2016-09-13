# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

python_library(
  name = 'tasks',
  sources = globs('*.py'),
  dependencies = [
    'src/python/pants/util:memo',
    'src/python/pants/base:exceptions',
    'src/python/pants/base:payload',
    'src/python/pants/base:payload_field',
    'src/python/pants/base:workunit',
    'src/python/pants/build_graph',
    'src/python/pants/fs:archive',
    'src/python/pants/task',
    'src/python/pants/util:contextutil',
    'src/python/pants/util:dirutil',
    'src/python/pants/backend/codegen/tasks:simple_codegen_task',
    'contrib/node/src/python/pants/contrib/node/tasks',
    'contrib/node/src/python/pants/contrib/node/targets',
    'contrib/node/src/python/pants/contrib/node/subsystems/resolvers',
    'contrib/webpack/src/python/pants/contrib/webpack/subsystems/resolvers',
    'contrib/webpack/src/python/pants/contrib/webpack/targets',
  ],
)
