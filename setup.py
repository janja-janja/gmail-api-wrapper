"""Setup file."""
from setuptools import setup, find_packages

from gmail_api_wrapper.version import __version__

VERSION = __version__

with open('README.md') as readme:
    README = readme.read()

setup(
    name='gmail-api-wrapper',
    version=VERSION,
    description='Python Gmail API Wrapper',
    long_description=README,
    author='Denis Karanja',
    author_email='dee.caranja@gmail.com',
    packages=find_packages(exclude=['tests', ]),
    install_requires=[
        'google-api-python-client==1.6.2',
        'python-dateutil',
    ],
    include_package_data=True,
)
