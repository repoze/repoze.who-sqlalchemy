# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2007, Agendaless Consulting and Contributors.
# Copyright (c) 2008, Florent Aide <florent.aide@gmail.com>.
# Copyright (c) 2008-2011, Gustavo Narea <me@gustavonarea.net>.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# http://www.repoze.org/LICENSE.txt.  A copy of the license should accompany
# this distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND
# FITNESS FOR A PARTICULAR PURPOSE
#
##############################################################################

import os
import platform
import sys

from setuptools import setup, find_packages

inPy3k = sys.version_info[0] == 3
inPyPy = platform.python_implementation == 'PyPy'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
version = open(os.path.join(here, 'VERSION.txt')).readline().rstrip()

tests_require = [
    'coverage',
    'nose',
]

if not inPy3k and not inPyPy:
    tests_require.append('elixir')
    tests_require.append('unittest2')
    # elixr 0.7.1 breaks with 0.8
    tests_require.append('sqlalchemy >= 0.5.0, <0.8dev')
else:
    tests_require.append('sqlalchemy >= 0.5.0')

setup(name='repoze.who.plugins.sa',
      version=version,
      description=('The repoze.who SQLAlchemy plugin'),
      long_description=README,
      classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Security",
        ],
      keywords='web application server wsgi sql sqlalchemy elixir ' \
               'authentication repoze',
      author="Gustavo Narea",
      author_email="repoze-dev@lists.repoze.org",
      namespace_packages=['repoze', 'repoze.who', 'repoze.who.plugins'],
      url="http://code.gustavonarea.net/repoze.who.plugins.sa/",
      license="BSD-derived (http://www.repoze.org/LICENSE.txt)",
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require={
        'testing': tests_require,
      },
      install_requires=[
        'repoze.who >= 2.1b1',
        'sqlalchemy >= 0.5.0',
      ],
      test_suite="nose.collector",
      entry_points = """\
      """
     )
