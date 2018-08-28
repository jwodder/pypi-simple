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
from   six.moves.urllib.parse import urljoin

PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple(object):
    def __init__(self, endpoint=PYPI_SIMPLE_ENDPOINT, cache=None):
        raise NotImplementedError

    def fetch_index(self, force=False):
        # Called automatically by any methods that need data from the index
        # force=True: forcibly refetch
        raise NotImplementedError

    def list_projects(self):
        raise NotImplementedError

    def get_project_files(self, project):
        ### Project lookup needs to be name normalization-aware
        raise NotImplementedError

    def get_project_url(self, project):
        # Return the URL in the simple API used for the given project
        raise NotImplementedError

    def __contains__(self, project):
        raise NotImplementedError


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
        raise NotImplementedError

    def get_digests(self):
        # Returns a dict mapping hash name to hex string
        raise NotImplementedError


def get_pip_cache():
    # Return the HTTP cache used by pip
    raise NotImplementedError

def parse_simple_index(html, base_url, from_encoding=None):
    # Returns a list of (project name, url) pairs
    projects = []
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    for link in soup.find_all('a'):
        projects.append((link.string, urljoin(base_url, link['href'])))
    return projects

def parse_project_files(html, base_url, from_encoding=None):
    # Returns a list of DistributionPackage objects
    files = []
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    for link in soup.find_all('a'):
        pkg = DistributionPackage(
            filename=link.string,
            url=urljoin(base_url, link['href']),
        )
        if 'data-gpg-sig' in link.attrs:
            pkg.has_sig = (link['data-gpg-sig'].lower() == 'true')
        if 'data-requires-python' in link.attrs:
            pkg.requires_python = link['data-requires-python']
        files.append(pkg)
    return files


ARCHIVE_EXT = r'\.(?:tar\.(?:bz2|gz|xz|Z)|zip)'

PACKAGE_TYPES = [
    ('dumb', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                        r'-(?P<version>.+?)'
                        r'\.(?:aix|cygwin|darwin|linux|macosx|solaris|sunos'
                            r'|win)[-.\w]*'
                        + ARCHIVE_EXT + '$')),

    ('egg', re.compile(r'^(?P<project>[A-Za-z0-9._]+)'
                       r'-(?P<version>[^-]+)'
                       r'(?:-[^-]+)*\.egg$')),

    ('sdist', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                         r'-(?P<version>.+)'
                        + ARCHIVE_EXT + '$')),

    ('wheel', re.compile(r'^(?P<project>[A-Za-z0-9._]+)'
                         r'-(?P<version>[^-]+)'
                         r'(?:-[^-]+)+\.whl$')),

    ('wininst', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                           r'-(?P<version>.+?)'
                           r'[._](?:aix|cygwin|darwin|linux|macosx|solaris'
                                 r'|sunos|win)[-.\w]*'
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
