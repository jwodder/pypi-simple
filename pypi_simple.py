"""
PyPI Simple Repository API client library

``pypi-simple`` is a client library for the Python Simple Repository API as
specified in `PEP 503 <https://www.python.org/dev/peps/pep-0503/>`_.  With it,
you can query PyPI and other pip-compatible repositories for a list of their
available projects and lists of each project's available package files.  The
library also allows you to query package files for their project version,
package type, file digests, ``requires_python`` string, and PGP signature URL.

Visit <https://github.com/jwodder/pypi-simple> for more information.
"""

__version__      = '0.2.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'pypi-simple@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/pypi-simple'

import re
import attr
from   bs4                    import BeautifulSoup
from   packaging.utils        import canonicalize_name as normalize
import requests
from   six.moves.urllib.parse import urljoin, urlunparse, urlparse

__all__ = [
    'DistributionPackage',
    'PYPI_SIMPLE_ENDPOINT',
    'PyPISimple',
]

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple(object):
    """
    A client for fetching package information from a Python simple package
    repository

    :param str endpoint: The base URL of the simple API instance to query;
        defaults to the base URL for PyPI's simple API
    """

    def __init__(self, endpoint=PYPI_SIMPLE_ENDPOINT):
        self.endpoint = endpoint.rstrip('/') + '/'
        self.s = requests.Session()

    def get_projects(self):
        """
        Returns a generator of names of projects available in the repository.
        The names are not normalized.

        .. warning::

            PyPI's project index file is very large and takes several seconds
            to parse.  Use this method sparingly.
        """
        r = self.s.get(self.endpoint)
        r.raise_for_status()
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        for name, _ in parse_simple_index(r.content, r.url, charset):
            yield name

    def get_project_files(self, project):
        """
        Returns a list of `DistributionPackage` objects representing all of the
        package files available in the repository for the given project.

        When fetching the project's information from the repository, a 404
        response is treated the same as an empty page, resulting in an empty
        list.  All other HTTP errors cause a `requests.HTTPError` to be raised.

        :param str project: The name of the project to fetch information on.
            The name does not need to be normalized.
        """
        url = self.get_project_url(project)
        r = self.s.get(url)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        return parse_project_page(r.content, r.url, charset)

    def get_project_url(self, project):
        """
        Returns the URL for the given project's page in the repository.

        :param str project: The name of the project to build a URL for.  The
            name does not need to be normalized.
        """
        return self.endpoint + normalize(project) + '/'


@attr.s
class DistributionPackage(object):
    """
    Information about a versioned archived file from which a Python project
    release can be installed
    """

    #: The basename of the package file
    filename = attr.ib()

    #: The URL from which the package file can be downloaded
    url = attr.ib()

    #: An optional version specifier string declaring the Python version(s) in
    #: which the package can be installed
    requires_python = attr.ib(default=None)

    #: Whether the package file is accompanied by a PGP signature file
    has_sig = attr.ib(default=False)

    @property
    def project(self):
        """
        The name of the project (as extracted from the filename), or `None` if
        the filename cannot be parsed
        """
        return parse_filename(self.filename)[0]

    @property
    def version(self):
        """
        The project version (as extracted from the filename), or `None` if the
        filename cannot be parsed
        """
        return parse_filename(self.filename)[1]

    @property
    def package_type(self):
        """
        The type of the package, or `None` if the filename cannot be parsed.
        The recognized package types are:

        - ``'dumb'``
        - ``'egg'``
        - ``'msi'``
        - ``'rpm'``
        - ``'sdist'``
        - ``'wheel'``
        - ``'wininst'``
        """
        return parse_filename(self.filename)[2]

    @property
    def sig_url(self):
        """
        If ``has_sig`` is true, this equals the URL of the package file's PGP
        signature file; otherwise, it equals `None`.
        """
        if self.has_sig:
            u = urlparse(self.url)
            return urlunparse((u[0], u[1], u[2] + '.asc', '', '', ''))
        else:
            return None

    def get_digests(self):
        """
        Extracts the hash digests from the package file's URL and returns a
        `dict` mapping hash algorithm names to hex-encoded digest strings
        """
        name, sep, value = urlparse(self.url).fragment.partition('=')
        return {name: value} if value else {}


def parse_simple_index(html, base_url=None, from_encoding=None):
    """
    Parse a simple repository's index page and return a generator of ``(project
    name, project URL)`` pairs

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to prepend to the URLs returned
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    for filename, url, _ in parse_links(html, base_url, from_encoding):
        yield (filename, url)

def parse_project_page(html, base_url=None, from_encoding=None):
    """
    Parse a project page from a simple repository and return a list of
    `DistributionPackage` objects

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to prepend to the packages' URLs
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    files = []
    for filename, url, attrs in parse_links(html, base_url, from_encoding):
        files.append(DistributionPackage(
            filename = filename,
            url = url,
            has_sig = attrs.get('data-gpg-sig', 'false').lower() == 'true',
            requires_python = attrs.get('data-requires-python'),
        ))
    return files

def parse_links(html, base_url=None, from_encoding=None):
    """
    Parse an HTML page and return a generator of links, where each link is
    represented as a triple of link text, link URL, and a `dict` of link tag
    attributes (including the unmodified ``href`` attribute).

    Link text has all leading & trailing whitespace removed.

    Keys in the attributes `dict` are converted to lowercase.

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to prepend to the URLs returned
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    base_tag = soup.find('base', href=True)
    if base_tag is not None:
        base_url = urljoin(base_url, base_tag['href'])
    # Note that ``urljoin(None, x) == x``
    for link in soup.find_all('a', href=True):
        yield (
            ''.join(link.strings).strip(),
            urljoin(base_url, link['href']),
            link.attrs,
        )

PROJECT_NAME = r'[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?'
PROJECT_NAME_NODASH = r'[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?'
VERSION = r'[A-Za-z0-9_.!+-]+?'
VERSION_NODASH = r'[A-Za-z0-9_.!+]+?'
ARCHIVE_EXT = r'\.(?:tar|tar\.(?:bz2|gz|lz|lzma|xz|Z)|tbz|tgz|tlz|txz|zip)'
PLAT_NAME = r'(?:aix|cygwin|darwin|linux|macosx|solaris|sunos|[wW]in)[-.\w]*'
PYVER = r'py[0-9]+\.[0-9]+'

PACKAGE_TYPES = [
    # See <https://git.io/fAclc>:
    ('dumb', re.compile(r'^(?P<project>{})-(?P<version>{})\.{}{}$'
                       .format(PROJECT_NAME, VERSION, PLAT_NAME, ARCHIVE_EXT))),

    # See <https://setuptools.readthedocs.io/en/latest/formats.html#filename-embedded-metadata>:
    ('egg', re.compile(r'^(?P<project>{})-(?P<version>{})(?:-{}(?:-{})?)?\.egg$'
               .format(PROJECT_NAME_NODASH, VERSION_NODASH, PYVER, PLAT_NAME))),

    # See <https://git.io/fAclv>:
    ('msi', re.compile(r'^(?P<project>{})-(?P<version>{})\.{}(?:-{})?\.msi$'
                       .format(PROJECT_NAME, VERSION, PLAT_NAME, PYVER))),

    # See <http://ftp.rpm.org/max-rpm/ch-rpm-file-format.html>:
    # (The architecture pattern is mainly just a guess based on what's
    # currently on PyPI.)
    ('rpm', re.compile(r'^(?P<project>{})-(?P<version>{})-[^-]+\.[A-Za-z0-9._]+\.rpm$'
                       .format(PROJECT_NAME, VERSION_NODASH))),

    ('sdist', re.compile(r'^(?P<project>{})-(?P<version>{}){}$'
                         .format(PROJECT_NAME, VERSION, ARCHIVE_EXT))),

    # Regex adapted from <https://git.io/fAclu>:
    ('wheel', re.compile(r'^(?P<project>{})-(?P<version>{})(-[0-9][^-]*?)?'
                         r'-.+?-.+?-.+?\.whl$'
                         .format(PROJECT_NAME_NODASH, VERSION_NODASH))),

    # See <https://git.io/fAclL>:
    ('wininst', re.compile(r'^(?P<project>{})-(?P<version>{})\.{}(?:-{})?\.exe$'
                           .format(PROJECT_NAME, VERSION, PLAT_NAME, PYVER))),
]

def parse_filename(filename):
    """
    Given the filename of a distribution package, returns a triple of the
    project name, project version, and package type.  The name and version are
    spelled the same as they appear in the filename; no normalization is
    performed.

    The package type may be any of the following strings:

    - ``'dumb'``
    - ``'egg'``
    - ``'msi'``
    - ``'rpm'``
    - ``'sdist'``
    - ``'wheel'``
    - ``'wininst'``

    If the filename cannot be parsed, ``(None, None, None)`` is returned.
    """
    for pkg_type, rgx in PACKAGE_TYPES:
        m = rgx.match(filename)
        if m:
            return (m.group('project'), m.group('version'), pkg_type)
    return (None, None, None)
