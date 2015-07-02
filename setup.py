from setuptools import find_packages

# # -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='pyjsonable',
    version='0.4',
    author=u'Grace Carey',
    author_email='gracecareymail@gmail.com',
    packages=find_packages(),
    url='https://github.com/gracecarey/pyjsonable',
    license='BSD',
    description='Native, validatable python objects serializable by json.dumps()',
    install_requires=[
        'django>=1.7',
        'openpyxl==2.2.1',
        'python-dateutil',
        'django-report-utils==0.3.4',
        'djangorestframework>=3.0.4',
    ],
    zip_safe=False
)