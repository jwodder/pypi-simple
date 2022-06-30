"""
PyPI Simple Repository API client library

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in :pep:`503` and updated by :pep:`592`, :pep:`629`, and :pep:`658`.
With it, you can query `the Python Package Index (PyPI) <https://pypi.org>`_
and other `pip <https://pip.pypa.io>`_-compatible repositories for a list of
their available projects and lists of each project's available package files.
The library also allows you to query package files for their project version,
package type, file digests, ``requires_python`` string, PGP signature URL, and
metadata URL.

Visit <https://github.com/jwodder/pypi-simple> or <https://pypi-simple.rtfd.io>
for more information.
"""

__version__ = "1.0.0.dev1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "pypi-simple@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/pypi-simple"

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/simple/"

#: The maximum supported simple repository version (See :pep:`629`)
SUPPORTED_REPOSITORY_VERSION: str = "1.0"

from .classes import DistributionPackage, IndexPage, Link, ProjectPage
from .client import PyPISimple
from .filenames import UnparsableFilenameError, parse_filename
from .parse_repo import (
    parse_repo_index_json,
    parse_repo_index_page,
    parse_repo_index_response,
    parse_repo_links,
    parse_repo_project_json,
    parse_repo_project_page,
    parse_repo_project_response,
)
from .parse_stream import parse_links_stream, parse_links_stream_response
from .progress import ProgressTracker, tqdm_progress_factory
from .util import (
    DigestMismatchError,
    NoDigestsError,
    UnexpectedRepoVersionWarning,
    UnsupportedContentTypeError,
    UnsupportedRepoVersionError,
)

__all__ = [
    "DigestMismatchError",
    "DistributionPackage",
    "IndexPage",
    "Link",
    "NoDigestsError",
    "PYPI_SIMPLE_ENDPOINT",
    "ProgressTracker",
    "ProjectPage",
    "PyPISimple",
    "SUPPORTED_REPOSITORY_VERSION",
    "UnexpectedRepoVersionWarning",
    "UnparsableFilenameError",
    "UnsupportedContentTypeError",
    "UnsupportedRepoVersionError",
    "parse_filename",
    "parse_links_stream",
    "parse_links_stream_response",
    "parse_repo_index_json",
    "parse_repo_index_page",
    "parse_repo_index_response",
    "parse_repo_links",
    "parse_repo_project_json",
    "parse_repo_project_page",
    "parse_repo_project_response",
    "tqdm_progress_factory",
]
