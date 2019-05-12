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

__version__      = '0.5.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'pypi-simple@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/pypi-simple'

from   collections            import namedtuple
import platform
import re
from   bs4                    import BeautifulSoup
from   packaging.utils        import canonicalize_name as normalize
import requests
from   six.moves.urllib.parse import urljoin, urlunparse, urlparse

__all__ = [
    'DistributionPackage',
    'PYPI_SIMPLE_ENDPOINT',
    'PyPISimple',
    'parse_filename',
    'parse_links',
    'parse_project_page',
    'parse_simple_index',
]

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

#: The User-Agent header used for requests; not used when the user provides eir
#: own session object
USER_AGENT = 'pypi-simple/{} ({}) requests/{} {}/{}'.format(
    __version__,
    __url__,
    requests.__version__,
    platform.python_implementation(),
    platform.python_version(),
)

class PyPISimple(object):
    """
    A client for fetching package information from a Python simple package
    repository

    :param str endpoint: The base URL of the simple API instance to query;
        defaults to the base URL for PyPI's simple API

    :param auth: Optional login/authentication details for the repository;
        either a ``(username, password)`` pair or `another authentication
        object accepted by requests
        <http://docs.python-requests.org/en/master/user/authentication/>`_

    :param session: Optional `requests.Session` object to use instead of
        creating a fresh one
    """

    def __init__(self, endpoint=PYPI_SIMPLE_ENDPOINT, auth=None, session=None):
        self.endpoint = endpoint.rstrip('/') + '/'
        if session is not None:
            self.s = session
        else:
            self.s = requests.Session()
            self.s.headers["User-Agent"] = USER_AGENT
        if auth is not None:
            self.s.auth = auth

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
        return parse_project_page(r.content, r.url, charset, project)

    def get_project_url(self, project):
        """
        Returns the URL for the given project's page in the repository.

        :param str project: The name of the project to build a URL for.  The
            name does not need to be normalized.
        """
        return self.endpoint + normalize(project) + '/'


class DistributionPackage(
    namedtuple(
        'DistributionPackage',
        'filename url project version package_type requires_python has_sig'
        ' yanked',
    )
):
    """
    Information about a versioned archived file from which a Python project
    release can be installed

    .. attribute:: filename
        The basename of the package file

    .. attribute:: url
        The URL from which the package file can be downloaded

    .. attribute:: project
        The name of the project (as extracted from the filename), or `None` if
        the filename cannot be parsed

    .. attribute:: version
        The project version (as extracted from the filename), or `None` if the
        filename cannot be parsed

    .. attribute:: package_type
        The type of the package, or `None` if the filename cannot be parsed.
        The recognized package types are:

        - ``'dumb'``
        - ``'egg'``
        - ``'msi'``
        - ``'rpm'``
        - ``'sdist'``
        - ``'wheel'``
        - ``'wininst'``

    .. attribute:: requires_python
        An optional version specifier string declaring the Python version(s) in
        which the package can be installed

    .. attribute:: has_sig
        Whether the package file is accompanied by a PGP signature file

    .. attribute:: yanked
        If the package file has been "yanked" from the package repository
        (meaning that it should only be installed when that specific version is
        requested), this attribute will be a string giving the reason why it
        was yanked; otherwise, it is `None`.
    """

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
    :param str base_url: an optional URL to join to the front of the URLs
        returned
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    for filename, url, _ in parse_links(html, base_url, from_encoding):
        yield (filename, url)

def parse_project_page(html, base_url=None, from_encoding=None,
                                            project_hint=None):
    """
    Parse a project page from a simple repository and return a list of
    `DistributionPackage` objects

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to join to the front of the packages'
        URLs
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    :param str project_hint: The name of the project whose page is being
        parsed; used to disambiguate the parsing of certain filenames
    """
    files = []
    for filename, url, attrs in parse_links(html, base_url, from_encoding):
        project, version, pkg_type = parse_filename(filename, project_hint)
        files.append(DistributionPackage(
            filename = filename,
            url = url,
            has_sig = attrs.get('data-gpg-sig', 'false').lower() == 'true',
            requires_python = attrs.get('data-requires-python'),
            project = project,
            version = version,
            package_type = pkg_type,
            yanked = attrs.get('data-yanked'),
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
    :param str base_url: an optional URL to join to the front of the URLs
        returned
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
PLAT_NAME = r'(?:aix|cygwin|darwin|linux|macosx|solaris|sunos|[wW]in)[-.A-Za-z0-9_]*'
PYVER = r'py[0-9]+\.[0-9]+'

#: Regexes for package filenames that can be parsed unambiguously
GOOD_PACKAGE_RGXN = [
    # See <https://setuptools.readthedocs.io/en/latest/formats.html#filename-embedded-metadata>:
    ('egg', re.compile(r'^(?P<project>{})-(?P<version>{})(?:-{}(?:-{})?)?\.egg$'
               .format(PROJECT_NAME_NODASH, VERSION_NODASH, PYVER, PLAT_NAME))),

    # See <http://ftp.rpm.org/max-rpm/ch-rpm-file-format.html>:
    # (The architecture pattern is mainly just a guess based on what's
    # currently on PyPI.)
    ('rpm', re.compile(r'^(?P<project>{})-(?P<version>{})-[^-]+\.[A-Za-z0-9._]+\.rpm$'
                       .format(PROJECT_NAME, VERSION_NODASH))),

    # Regex adapted from <https://git.io/fAclu>:
    ('wheel', re.compile(r'^(?P<project>{})-(?P<version>{})(-[0-9][^-]*?)?'
                         r'-.+?-.+?-.+?\.whl$'
                         .format(PROJECT_NAME_NODASH, VERSION_NODASH))),
]

#: Partial regexes for package filenames with ambiguous grammars.  If a hint as
#: to the expected project name is given, it will be prepended to the regexes
#: when trying to determine a match; otherwise, a generic pattern that matches
#: all project names will be prepended.
BAD_PACKAGE_BASES = [
    # See <https://git.io/fAclc>:
    ('dumb', re.compile(r'-(?P<version>{})\.{}{}$'
                        .format(VERSION, PLAT_NAME, ARCHIVE_EXT))),

    # See <https://git.io/fAclv>:
    ('msi', re.compile(r'-(?P<version>{})\.{}(?:-{})?\.msi$'
                       .format(VERSION, PLAT_NAME, PYVER))),

    ('sdist', re.compile(r'-(?P<version>{}){}$'.format(VERSION, ARCHIVE_EXT))),

    # See <https://git.io/fAclL>:
    ('wininst', re.compile(r'-(?P<version>{})\.{}(?:-{})?\.exe$'
                           .format(VERSION, PLAT_NAME, PYVER))),
]

#: Regexes for package filenames with ambiguous grammars, using a generic
#: pattern that matches all project names
BAD_PACKAGE_RGXN = [
    (pkg_type, re.compile('^(?P<project>' + PROJECT_NAME + ')' + rgx.pattern))
    for pkg_type, rgx in BAD_PACKAGE_BASES
]

def parse_filename(filename, project_hint=None):
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

    Note that some filenames (e.g., :file:`1-2-3.tar.gz`) may be ambiguous as
    to which part is the project name and which is the version.  In order to
    resolve the ambiguity, the expected value for the project name (*modulo*
    normalization) can be supplied as the ``project_name`` argument to the
    function.  If the filename can be parsed with the given string in the role
    of the project name, the results of that parse will be returned; otherwise,
    the function will fall back to breaking the project & version apart at an
    unspecified point.

    :param str filename: The package filename to parse
    :param str project_hint: Optionally, the expected value for the project
        name (usually the name of the project page on which the filename was
        found).  The name does not need to be normalized.
    """
    for pkg_type, rgx in GOOD_PACKAGE_RGXN:
        m = rgx.match(filename)
        if m:
            return (m.group('project'), m.group('version'), pkg_type)
    if project_hint is not None:
        proj_rgx = re.sub(r'[^A-Za-z0-9]+', '[-_.]+', project_hint)
        proj_rgx = re.sub(
            r'([A-Za-z])',
            lambda m: '[' + m.group(1).upper() + m.group(1).lower() + ']',
            proj_rgx,
        )
        m = re.match(proj_rgx + r'(?=-)', filename)
        if m:
            project = m.group(0)
            rest_of_name = filename[m.end(0):]
            for pkg_type, rgx in BAD_PACKAGE_BASES:
                m = rgx.match(rest_of_name)
                if m:
                    return (project, m.group('version'), pkg_type)
    for pkg_type, rgx in BAD_PACKAGE_RGXN:
        m = rgx.match(filename)
        if m:
            return (m.group('project'), m.group('version'), pkg_type)
    return (None, None, None)
