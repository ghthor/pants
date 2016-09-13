# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.


contrib_plugin(
  name='plugin',
  dependencies=[
    'contrib/webpack/src/python/pants/contrib/webpack/subsystems/resolvers',
    'contrib/webpack/src/python/pants/contrib/webpack/targets',
    'contrib/webpack/src/python/pants/contrib/webpack/tasks',
    'src/python/pants/build_graph',
    'src/python/pants/goal:task_registrar',
  ],
  distribution_name='pantsbuild.pants.contrib.webpack',
  description='Webpack Node.js support for pants.',
  build_file_aliases=True,
  register_goals=True,
  global_subsystems=True
)


python_library(
  name = 'webpack',
  sources = globs('*.py'),
  dependencies = [
    'src/python/pants/build_graph',
    'src/python/pants/goal',
    'src/python/pants/goal:task_registrar',
    'contrib/webpack/src/python/pants/contrib/webpack/targets',
    'contrib/webpack/src/python/pants/contrib/webpack/tasks',
  ],
)
