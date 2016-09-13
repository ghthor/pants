webpack_module(
  name='web-project',
  sources=globs('package.json', 'webpack.config.js', 'src/*', 'test/*', 'npm-shrinkwrap.json'),
  dependencies=[
    'contrib/node/examples/3rdparty/node/webpack',
    'contrib/node/examples/3rdparty/node/mocha',
    'contrib/node/examples/3rdparty/node/react',
    'contrib/node/examples/src/node/server-project',
    'contrib/node/examples/src/node/web-build-tool',
    'contrib/node/examples/src/node/web-component-button',
  ]
)

node_test(
  name='unit',
  dependencies=[
    ':web-project'
  ]
)
