from setuptools import setup, find_packages

# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='pyjsonable',
    version='0.0.2',
    author=u'Grace Carey',
    author_email='gracecareymail@gmail.com',
    packages=find_packages(),
    url='https://github.com/gracecarey/pyjsonable',
    license='BSD',
    description='Native, validatable python objects serializable by json.dumps()',
)