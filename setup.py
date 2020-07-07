 # -*- coding: utf-8 -*-

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='slurmcluster',
      version='20200706',
      py_modules=['submit_slurm'],
      description='Tools to interact with EMBL cluster.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Martin Schorb',
      author_email='schorb@embl.de',
      license='GPLv3',
      install_requires=[
      'numpy'
      ],
      )
