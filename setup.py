# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='usp',
    version='0.1.0',
    description='Univeral Service Provider',
    long_description=readme,
    author='Mayowa Aladeojebi',
    author_email='mayowa.aladeojebi@stelligent.com',
    url='https://github.com/stelligent/usp',
    license='MIT',
    packages=find_packages(exclude=('tests', 'docs'))
)

