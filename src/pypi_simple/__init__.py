"""
PyPI Simple Repository API client library

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in `PEP 503 <https://www.python.org/dev/peps/pep-0503/>`_ and updated
by `PEP 592 <https://www.python.org/dev/peps/pep-0592/>`_.  With it, you can
query PyPI and other pip-compatible repositories for a list of their available
projects and lists of each project's available package files.  The library also
allows you to query package files for their project version, package type, file
digests, ``requires_python`` string, and PGP signature URL.

Visit <https://github.com/jwodder/pypi-simple> for more information.
"""

__version__      = '0.7.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'pypi-simple@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/pypi-simple'

from .client    import PYPI_SIMPLE_ENDPOINT, PyPISimple
from .distpkg   import DistributionPackage
from .filenames import parse_filename
from .parsing   import parse_links, parse_project_page, parse_simple_index

__all__ = [
    'DistributionPackage',
    'PYPI_SIMPLE_ENDPOINT',
    'PyPISimple',
    'parse_filename',
    'parse_links',
    'parse_project_page',
    'parse_simple_index',
]
