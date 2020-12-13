"""
PyPI Simple Repository API client library

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in :pep:`503` and updated by :pep:`592` and :pep:`629`.  With it, you
can query `the Python Package Index (PyPI) <https://pypi.org>`_ and other `pip
<https://pip.pypa.io>`_-compatible repositories for a list of their available
projects and lists of each project's available package files.  The library also
allows you to query package files for their project version, package type, file
digests, ``requires_python`` string, and PGP signature URL.

Visit <https://github.com/jwodder/pypi-simple> or <https://pypi-simple.rtfd.io>
for more information.
"""

__version__      = '0.8.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'pypi-simple@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/pypi-simple'

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT: str = 'https://pypi.org/simple/'

#: The maximum supported simple repository version (See :pep:`629`)
SUPPORTED_REPOSITORY_VERSION: str = '1.0'

from .classes      import DistributionPackage, IndexPage, Link, ProjectPage
from .client       import PyPISimple
from .filenames    import parse_filename
from .parse_old    import parse_links, parse_project_page, parse_simple_index
from .parse_repo   import parse_repo_index_page, parse_repo_index_response, \
                            parse_repo_links, parse_repo_project_page, \
                            parse_repo_project_response
from .parse_stream import parse_links_stream, parse_links_stream_response
from .util         import UnsupportedRepoVersionError

__all__ = [
    'DistributionPackage',
    'IndexPage',
    'Link',
    'PYPI_SIMPLE_ENDPOINT',
    'ProjectPage',
    'PyPISimple',
    'SUPPORTED_REPOSITORY_VERSION',
    'UnsupportedRepoVersionError',
    'parse_filename',
    'parse_links',
    'parse_links_stream',
    'parse_links_stream_response',
    'parse_project_page',
    'parse_repo_index_page',
    'parse_repo_index_response',
    'parse_repo_links',
    'parse_repo_project_page',
    'parse_repo_project_response',
    'parse_simple_index',
]
