"""Setup file."""
from setuptools import setup, find_packages

from gmail_api_wrapper.version import __version__
from gmail_api_wrapper.utils import read_file

VERSION = __version__
README = read_file('README.md')
LICENSE = read_file('LICENSE')

setup(
    name='gmail-api-wrapper',
    version=VERSION,
    license=LICENSE,
    description='Python Gmail API Wrapper',
    long_description=README,
    author='Denis Karanja',
    author_email='dee.caranja@gmail.com',
    packages=find_packages(exclude=['tests', ]),
    install_requires=[
        'google-api-python-client==1.6.3',
        'python-dateutil',
    ],
    include_package_data=True,
)
