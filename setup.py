# -*- coding: utf-8 -*-
#
# Flask-WaffleConf - https://github.com/rmed/flask-waffleconf
#
# Copyright (C) 2015  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description
with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='Flask-WaffleConf',
    version='0.3.0',
    url='https://github.com/rmed/flask-waffleconf',
    license='GPLv2+',
    author='Rafael Medina García',
    author_email='rafamedgar@gmail.com.com',
    description='Store variables in database and update them at runtime',
    long_description=long_description,
    packages=['flask_waffleconf'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
