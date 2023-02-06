# -*- coding: utf-8 -*-

from setuptools import setup

version = '1.0.20'


setup(
    name='django-detect',
    version=version,
    keywords='django-detect',
    description='Django UserAgent Detect',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    url='https://github.com/Brightcells/django-detect',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['detect'],
    py_modules=[],
    install_requires=['django-six'],

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
