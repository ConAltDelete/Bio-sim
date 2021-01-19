# -*- coding: utf-8 -*-
__author__ = 'Mats Hoem Olsen'
__email__ = 'mats.hoem.olsen@nmbu.no'
"""
To create biosim package, first run this command in python termimal at the directory of this file
> python setup.py sdist
To install the biosim package, first move the package file to destination directory, unpack it,
then run
> python setup.py install
"""
from distutils.core import setup
setup(name='BioSim',
 version='2.0',
 description='BioSim, but cooler',
 author='Mats Hoem Olsen, Roy Erling Granheim',
 author_email='mats.hoem.olsen@nmbu.no,roy.erling.granheim@nmbu.no',
 url='',
 requires=['numpy', 'pandas', 'matplotlib'],
 packages=['biosim']
 )