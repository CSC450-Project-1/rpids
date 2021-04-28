"""
Simple module that monkey patches pkg_resources.get_distribution used by dash
to determine the version of Flask-Compress which is not available with a
flask_compress.__version__ attribute. Known to work with dash==1.16.3 and
PyInstaller==3.6.
"""

import sys
from collections import namedtuple

import pkg_resources

IS_FROZEN = hasattr(sys, '_MEIPASS')

# backup true function
_true_get_distribution = pkg_resources.get_distribution
_Dist = namedtuple('_Dist', ['version'])

def _get_distribution(dist):
    if IS_FROZEN and dist == 'flask-compress':
        return _Dist('1.5.0')
    else:
        return _true_get_distribution(dist)

# monkey patch the function so it can work once frozen and pkg_resources is of
# no help
pkg_resources.get_distribution = _get_distribution
