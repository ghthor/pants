# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).


python_tests(
  name = 'interpreter_selection_integration',
  sources = ['test_interpreter_selection_integration.py'],
  dependencies = [
    'src/python/pants/util:contextutil',
    'tests/python/pants_test:int-test',
  ],
  tags = {'integration'},
)

python_tests(
  name = 'python_run_integration',
  sources = ['test_python_run_integration.py'],
  dependencies = [
    'src/python/pants/util:contextutil',
    'tests/python/pants_test:int-test',
  ],
  tags = {'integration'},
)

python_tests(
  name = 'test_interpreter_cache',
  sources = ['test_interpreter_cache.py'],
  dependencies = [
    '3rdparty/python:mock',
    '3rdparty/python:pex',
    'src/python/pants/backend/python:interpreter_cache',
    'src/python/pants/backend/python:python_setup',
    'src/python/pants/util:contextutil',
    'tests/python/pants_test/subsystem:subsystem_utils',
  ],
)
