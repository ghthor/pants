# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_tests(
  name = 'argutil',
  sources = ['test_argutil.py'],
  coverage = ['pants.util.argutil'],
  dependencies = [
    'src/python/pants/util:argutil',
  ],
)

python_tests(
  name = 'collections',
  sources = ['test_collections.py'],
  coverage = ['pants.util.collections'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:collections',
  ]
)

python_tests(
  name = 'contextutil',
  sources = ['test_contextutil.py'],
  coverage = ['pants.util.contextutil'],
  dependencies = [
    '3rdparty/python:future',
    '3rdparty/python:mock',
    'src/python/pants/util:contextutil',
    'src/python/pants/util:process_handler',
  ]
)

python_tests(
  name = 'dirutil',
  sources = ['test_dirutil.py'],
  coverage = ['pants.util.dirutil'],
  dependencies = [
    '3rdparty/python:future',
    '3rdparty/python:mock',
    'src/python/pants/util:contextutil',
    'src/python/pants/util:dirutil',
    'src/python/pants/util:objects',
  ]
)

python_tests(
  name = 'eval',
  sources = ['test_eval.py'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:eval',
  ]
)

python_tests(
  name = 'fileutil',
  sources = ['test_fileutil.py'],
  dependencies = [
    'src/python/pants/util:contextutil',
    'src/python/pants/util:fileutil',
  ]
)

python_tests(
  name = 'filtering',
  sources = ['test_filtering.py'],
  dependencies = [
    'src/python/pants/util:filtering',
  ]
)

python_tests(
  name = 'memo',
  sources = ['test_memo.py'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:memo',
    'src/python/pants/util:meta',
  ]
)

python_tests(
  name = 'meta',
  sources = ['test_meta.py'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:meta',
    'tests/python/pants_test:test_base',
  ]
)

python_tests(
  name = 'netrc',
  sources = ['test_netrc.py'],
  dependencies = [
    '3rdparty/python:future',
    '3rdparty/python:mock',
    'src/python/pants/util:netrc',
  ]
)

python_tests(
  name = 'objects',
  sources = ['test_objects.py'],
  coverage = ['pants.util.objects'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:objects',
    'tests/python/pants_test:base_test',
  ]
)

python_tests(
  name = 'osutil',
  sources = ['test_osutil.py'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:osutil',
    'tests/python/pants_test:test_base',
  ]
)

python_tests(
  name = 'process_handler',
  sources = ['test_process_handler.py'],
  dependencies = [
    'src/python/pants/util:process_handler',
  ]
)

python_tests(
  name = 'retry',
  sources = ['test_retry.py'],
  dependencies = [
    '3rdparty/python:mock',
    'src/python/pants/util:retry',
  ]
)

python_tests(
  name = 'socket',
  sources = ['test_socket.py'],
  coverage = ['pants.util.socket'],
  dependencies = [
    '3rdparty/python:mock',
    'src/python/pants/util:socket',
  ]
)

python_tests(
  name = 'strutil',
  sources = ['test_strutil.py'],
  dependencies = [
    '3rdparty/python:future',
    'src/python/pants/util:strutil',
  ]
)

python_tests(
  name = 'tarutil',
  sources = ['test_tarutil.py'],
  dependencies = [
    'src/python/pants/util:dirutil',
    'src/python/pants/util:tarutil',
  ]
)

python_library(
  name='xml_test_base',
  sources = ['xml_test_base.py'],
  dependencies = [
    'src/python/pants/util:contextutil',
  ]
)

python_tests(
  name = 'xml_parser',
  sources = ['test_xml_parser.py'],
  dependencies = [
    'src/python/pants/util:xml_parser',
    'tests/python/pants_test/util:xml_test_base',
  ]
)
