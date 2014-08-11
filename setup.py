from distutils.core import setup
from setuptools import find_packages

setup(
    name='graphlite',
    version='1.0.0',
    packages=find_packages(),
    description='embedded graph datastore',

    author='Eugene Eeo',
    author_email='packwolf58@gmail.com',
    url='https://github.com/eugene-eeo/graphlite',
    long_description=open('README.rst').read(),
)
