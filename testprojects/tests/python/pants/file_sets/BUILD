python_library(
  name='exclude_list_of_strings',
  sources=rglobs('*.py',
                 exclude=[
                   ['aaa.py', 'dir1/aaa.py']
                 ]
                ),
)

python_library(
  name='exclude_globs',
  sources=rglobs('*.py',
                 exclude=[
                   globs('*bb.py', 'dir1/dirdir1/*aa.py')
                 ]
                ),
)

python_library(
  name='exclude_strings',
  sources=rglobs('*.py',
                 exclude=[
                  'aa.py', 'ab.py'
                 ]
                ),
)

python_library(
  name='exclude_set',
  sources=rglobs('*.py',
                 exclude=[
                   set(['aaa.py', 'a.py'])
                 ]
                ),
)

python_library(
  name='exclude_rglobs',
  sources=rglobs('*.py',
                 exclude=[
                   rglobs('*b.py')
                 ]
                ),
)

python_library(
  name='exclude_zglobs',
  sources=rglobs('*.py',
                 exclude=[
                   zglobs('**/*b.py')
                 ]
                ),
)

python_library(
  name='exclude_composite',
  sources=rglobs('*.py',
                 exclude=[
                   ['aaa.py'],
                   zglobs('**/a.py')
                 ]
                ),
)
