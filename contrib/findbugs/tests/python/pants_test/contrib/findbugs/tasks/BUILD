# Copyright 2016 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_tests(
  name='tasks',
  sources=['test_findbugs.py'],
  dependencies = [
    'contrib/findbugs/src/python/pants/contrib/findbugs/tasks',
    'tests/python/pants_test/tasks:task_test_base',
  ],
)

python_tests(
  name='integration',
  sources=['test_findbugs_integration.py'],
  dependencies = [
    'src/python/pants/base:build_environment',
    'src/python/pants/util:contextutil',
    'tests/python/pants_test:int-test',
  ],
  tags={'integration'},
  timeout=300,
)
