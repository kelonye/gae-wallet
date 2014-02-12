#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='gae-wallet',
    version='0.0.1',
    description='Pesapal NDB Model',
    author='Mitchel Kelonye',
    author_email='kelonyemitchel@gmail.com',
    url='https://github.com/kelonye/gae-wallet',
    packages=['gae_wallet',],
    package_dir = {'gae_wallet': 'lib'},
    license='MIT',
    zip_safe=True
)