# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup

version = '1.0.4'


setup(
    name='django-detect',
    version=version,
    keywords='django-detect',
    description="Django UserAgent Detect",
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/django-detect',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['detect', ],
    py_modules=[],
    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
    ],
)
