#!/usr/bin/env python

from os.path import join, dirname

execfile(join(dirname(__file__), 'src', 'UnixFilesystemLibrary', 'version.py'))

from distutils.core import setup

CLASSIFIERS = """
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

long_description=open(join(dirname(__file__), 'README.rst',)).read()

setup(
  name             = 'robotframework-unixfilesystemlibrary',
  version          = VERSION,
  description      = 'Robot Framework UNIX Filesystem Library',
  long_description = long_description,
  author           = 'Chris Hirsch',
  author_email     = 'chris@base2technology.com',
  url              = 'https://github.com/ChrisHirsch/robotframework-unixfilesystem',
  license          = 'Apache License 2.0',
  keywords         = 'robotframework testing testautomation unix filesystem attributes',
  platforms        = 'any',
  zip_safe         = False,
  classifiers      = CLASSIFIERS.splitlines(),
  package_dir      = {'' : 'src'},
  install_requires = ['robotframework'],
  extras_require = dict(test=['zope.testing']),
  packages         = ['UnixFilesystemLibrary'],
)
