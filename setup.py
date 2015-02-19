#!/usr/bin/env/python
from setuptools import setup

setup(
    name='ckanext-donneesqctheme',
    version='0.1',
    description='',
    license='AGPL3',
    author='',
    author_email='',
    url='',
    namespace_packages=['ckanext'],
    packages=['ckanext.donneesqctheme'],
    zip_safe=False,
    entry_points = """
        [ckan.plugins]
        donneesqc_theme = ckanext.donneesqctheme.plugins:CustomTheme
        donneesqc_extrapages = ckanext.donneesqctheme.plugins:ContactPagesPlugin
    """
)
