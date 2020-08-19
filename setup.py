 # -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='clusterms',
      version='20200706',

      packages=find_packages(),
      description='Tools to interact with EMBL cluster.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Martin Schorb',
      author_email='schorb@embl.de',
      license='GPLv3',
      install_requires=[
      'numpy'
      ],
      entry_points={
          "console_scripts": ["submit_slurm = cluster_ms.submit_slurm:main"]
      }
      )
