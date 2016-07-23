#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA


setup(
    name='django-queryset-splitter',
    version='0.0.0',
    license='MIT License',
    platforms=['any'],
    packages=['django_queryset_splitter'],
    tests_require=[
        'Django',
        'pytest',
        'pytest-django',
        'tox',
    ],
    # classifiers=[
    #     'Development Status :: 4 - Beta',
    #     'Environment :: Web Environment',
    #     'Framework :: Django',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    #     'Programming Language :: Python',
    #     'Programming Language :: Python :: 2',
    #     'Programming Language :: Python :: Implementation :: PyPy',
    #     'Topic :: Utilities',
    # ],
)
