# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='ucp',
    version='0.1.0',
    description='Unified Cloud Provider',
    long_description=readme,
    author='Mayowa Aladeojebi',
    author_email='mayowa.aladeojebi@stelligent.com',
    url='https://github.com/stelligent/ucp',
    license=license,
    packages=find_packages(exclude=('docs')),
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/ucp'],
    include_package_data=True
)
