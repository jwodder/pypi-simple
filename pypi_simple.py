"""
PyPI Simple Repository API client library

Visit <https://github.com/jwodder/pypi-simple> for more information.
"""

__version__      = '0.1.0.dev1'
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

PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple(object):
    def __init__(self, endpoint=PYPI_SIMPLE_ENDPOINT):
        self.endpoint = endpoint.rstrip('/') + '/'
        self.s = requests.Session()

    def get_projects(self):
        r = self.s.get(self.endpoint)
        r.raise_for_status()
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        for name, _ in parse_simple_index(r.content, r.url, charset):
            yield name

    def get_project_files(self, project):
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
        # Return the URL in the simple API used for the given project
        return self.endpoint + normalize(project) + '/'


@attr.s
class DistributionPackage(object):
    filename = attr.ib()
    url = attr.ib()
    requires_python = attr.ib(default=None)
    has_sig = attr.ib(default=False)

    @property
    def project(self):
        return parse_filename(self.filename)[0]

    @property
    def version(self):
        return parse_filename(self.filename)[1]

    @property
    def package_type(self):
        return parse_filename(self.filename)[2]

    @property
    def sig_url(self):
        # Returns None if no signature
        if self.has_sig:
            u = urlparse(self.url)
            return urlunparse((u[0], u[1], u[2] + '.asc', '', '', ''))
        else:
            return None

    def get_digests(self):
        # Returns a dict mapping hash name to hex string
        name, sep, value = urlparse(self.url).fragment.partition('=')
        return {name: value} if value else {}


def parse_simple_index(html, base_url=None, from_encoding=None):
    # Returns a generator of (project name, url) pairs
    for filename, url, _ in parse_links(html, base_url, from_encoding):
        yield (filename, url)

def parse_project_page(html, base_url=None, from_encoding=None):
    # Returns a list of DistributionPackage objects
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

ARCHIVE_EXT = r'\.(?:tar|tar\.(?:bz2|gz|lz|lzma|xz|Z)|tbz|tgz|tlz|txz|zip)'
PLAT_NAME = r'(?:aix|cygwin|darwin|linux|macosx|solaris|sunos|[wW]in)[-.\w]*'
PYVER = r'py\d+\.\d+'

PACKAGE_TYPES = [
    # See <https://git.io/fAclc>:
    ('dumb', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                        r'-(?P<version>.+?)'
                        r'\.' + PLAT_NAME
                        + ARCHIVE_EXT + '$')),

    # See <https://setuptools.readthedocs.io/en/latest/formats.html#filename-embedded-metadata>:
    # Note that, unlike the other formats, the project name & version for an
    # egg cannot contain hyphens.
    ('egg', re.compile(r'^(?P<project>[A-Za-z0-9._]+)'
                       r'-(?P<version>[^-]+)'
                       r'(?:-' + PYVER + '(?:-' + PLAT_NAME + ')?)?\.egg$')),

    # See <https://git.io/fAclv>:
    ('msi', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                       r'-(?P<version>.+?)'
                       r'\.' + PLAT_NAME +
                       r'(?:-' + PYVER + r')?'
                       r'\.msi$')),

    ('sdist', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                         r'-(?P<version>.+)'
                         + ARCHIVE_EXT + '$')),

    # Regex adapted from <https://git.io/fAclu>:
    ('wheel', re.compile(r'^(?P<project>.+?)'
                         r'-(?P<version>.*?)'
                         r'(-\d[^-]*?)?-.+?-.+?-.+?'
                         r'\.whl$')),

    # See <https://git.io/fAclL>:
    ('wininst', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                           r'-(?P<version>.+?)'
                           r'\.' + PLAT_NAME +
                           r'(?:-' + PYVER + r')?'
                           r'\.exe$')),
]

def parse_filename(filename):
    """
    Given the filename of a distribution package, return a triple of the
    project name, project version, and package type.  The name and version are
    spelled the same as they appear in the filename; no normalization is
    performed.

    The package type may be any of the following strings:

    - ``'dumb'``
    - ``'egg'``
    - ``'msi'``
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
