from setuptools import setup, find_packages
import os

version = "0.4"
shortdesc ="Plone Add-On to manage and display locations."
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(name='collective.gmaplocation',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='web zope plone google maps',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      license='GNU General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'yafowil.yaml>0.9',
          'yafowil.plone',
          'archetypes.schemaextender',
          'bda.plone.ajax',
          'collective.js.jqueryui',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,      
      )
