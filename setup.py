from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='dash_billing',
      version=version,
      description="Dash billing plugin for horizon(diablo)",
      long_description="""- billing middleware for horizon(diablo)""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Nachi Ueno',
      author_email='ueno.nachi@lab.ntt.co.jp',
      url='https://github.com/ntt-pf-lab/dash_billing',
      license='Apache License',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      scripts=['bin/nova-notification'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
