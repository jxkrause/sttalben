from setuptools import setup, find_packages
import os
from sttalben import _version_

def open_file(fname):
    """helper function to open a local file"""
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name = 'sttalben',
    version = _version_,
    author = 'Jens Krause',
    author_email = 'jxkrause@posteo.de',
    packages=find_packages(),
        # url='https://github.com/...',
    license = 'GPL',
    classifiers = [
        'Programming Language :: Python :: 3.8',
    ],
    description = 'sttalben - Datenbank für Musikalben',
    long_description = open_file('README.md').read(),
    # end-user dependencies for your library
    install_requires = [
        'pandas',
        'sqlalchemy',
        'python-dotenv'
    ],
    # include additional data
    package_data = {
        'sttalben': ['columns.txt']
    }
)
