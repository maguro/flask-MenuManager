# !/usr/bin/env python
#
# (C) Copyright 2014 Alan Cabrera
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from io import open

from setuptools import setup


try:
    long_description = open('README.md').read()
except:
    long_description = u"Easy websockets for bottle."

setup(
    name='flask-MenuManager',
    version='1.0',
    url='https://svn.apache.org/repos/asf/labs/panopticon/',
    license='Apache License (http://www.apache.org/licenses/LICENSE-2.0)',
    author='Alan Cabrera',
    author_email='adc@toolazydogs.com',
    description='An easy way to build and manage menus in Flask',
    # don't ever depend on refcounting to close files anywhere else
    long_description=open('README.md', encoding='utf-8').read(),

    package_dir={'': 'src'},
    packages=['flask_MenuManager'],

    zip_safe=False,
    platforms='any',

    install_requires=[
        'Flask'
    ],

    tests_require=['tox'],

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
