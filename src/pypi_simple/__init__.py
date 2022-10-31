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

__version__ = "1.0.0"
__author__ = "John Thorvald Wodder II"
__author_email__ = "pypi-simple@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/pypi-simple"

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT: str = "https://pypi.org/simple/"

#: The maximum supported simple repository version (See :pep:`629`)
SUPPORTED_REPOSITORY_VERSION: str = "1.0"

#: :mailheader:`Accept` header value for accepting either the HTML or JSON
#: serialization without a preference
ACCEPT_ANY: str = ", ".join(
    [
        "application/vnd.pypi.simple.v1+json",
        "application/vnd.pypi.simple.v1+html",
        "text/html;q=0.01",
    ]
)

#: :mailheader:`Accept` header value for accepting only the JSON serialization
ACCEPT_JSON_ONLY = "application/vnd.pypi.simple.v1+json"

#: :mailheader:`Accept` header value for accepting only the HTML serialization
ACCEPT_HTML_ONLY = ", ".join(
    [
        "application/vnd.pypi.simple.v1+html",
        "text/html;q=0.01",
    ]
)

#: :mailheader:`Accept` header value for accepting either the HTML or JSON
#: serialization with a preference for JSON
ACCEPT_JSON_PREFERRED = ", ".join(
    [
        "application/vnd.pypi.simple.v1+json",
        "application/vnd.pypi.simple.v1+html;q=0.5",
        "text/html;q=0.01",
    ]
)

#: :mailheader:`Accept` header value for accepting either the HTML or JSON
#: serialization with a preference for HTML
ACCEPT_HTML_PREFERRED = ", ".join(
    [
        "application/vnd.pypi.simple.v1+html",
        "text/html;q=0.5",
        "application/vnd.pypi.simple.v1+json;q=0.1",
    ]
)

from .classes import DistributionPackage, IndexPage, ProjectPage
from .client import NoSuchProjectError, PyPISimple
from .errors import (
    DigestMismatchError,
    NoDigestsError,
    UnexpectedRepoVersionWarning,
    UnparsableFilenameError,
    UnsupportedContentTypeError,
    UnsupportedRepoVersionError,
)
from .filenames import parse_filename
from .html import Link, RepositoryPage
from .html_stream import parse_links_stream, parse_links_stream_response
from .progress import ProgressTracker, tqdm_progress_factory

__all__ = [
    "DigestMismatchError",
    "DistributionPackage",
    "IndexPage",
    "Link",
    "NoDigestsError",
    "NoSuchProjectError",
    "PYPI_SIMPLE_ENDPOINT",
    "ProgressTracker",
    "ProjectPage",
    "PyPISimple",
    "RepositoryPage",
    "SUPPORTED_REPOSITORY_VERSION",
    "UnexpectedRepoVersionWarning",
    "UnparsableFilenameError",
    "UnsupportedContentTypeError",
    "UnsupportedRepoVersionError",
    "parse_filename",
    "parse_links_stream",
    "parse_links_stream_response",
    "tqdm_progress_factory",
]
