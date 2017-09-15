"""Setup file."""
from setuptools import setup, find_packages

from gmail_api_wrapper.version import __version__
from gmail_api_wrapper.utils import read_file

VERSION = __version__
README = read_file('README.rst', package_level=False)
name = 'gmail-api-wrapper'

setup(
    name=name,
    version=VERSION,
    license='MIT',
    description='Gmail API Wrapper - Python Client',
    long_description=README,
    author='Denis Karanja',
    author_email='dee.caranja@gmail.com',
    url='https://github.com/yoda-yoda/gmail-api-wrapper/',
    keywords=['gmail-api-wrapper', 'gmail python client'],
    packages=find_packages(exclude=['tests', ]),
    install_requires=[
        'google-api-python-client==1.6.3',
        'python-dateutil',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
)
