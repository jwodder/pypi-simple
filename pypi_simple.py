"""
PyPI Simple Repository API client library

Visit <https://github.com/jwodder/pypi-simple> for more information.
"""

__version__      = '0.1.0.dev1'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'pypi-simple@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/pypi-simple'

from   collections                    import OrderedDict
from   os.path                        import join
import re
import appdirs
import attr
from   bs4                            import BeautifulSoup
from   cachecontrol                   import CacheControl
from   cachecontrol.caches.file_cache import FileCache
from   packaging.utils                import canonicalize_name as normalize
import requests
from   six.moves.urllib.parse         import urljoin, urlunparse, urlparse

PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple(object):
    def __init__(self, endpoint=PYPI_SIMPLE_ENDPOINT, cache=None):
        self.endpoint = endpoint
        self.s = requests.Session()
        if cache is not None:
            self.s = CacheControl(self.s, cache=cache)
        self._projects = None

    def fetch_index(self, force=False):
        # Called automatically by any methods that need data from the index
        # force=True: forcibly refetch (still goes through cache, though)
        if self._projects is None or force:
            r = self.s.get(self.endpoint)
            r.raise_for_status()
            if 'charset' in r.headers.get('content-type', '').lower():
                charset = r.encoding
            else:
                charset = None
            self._projects = OrderedDict([
                (normalize(name), url)
                for name, url in parse_simple_index(r.content, r.url, charset)
            ])

    def list_projects(self):
        self.fetch_index()
        return list(self._projects)

    def get_project_files(self, project):
        url = self.get_project_url(project)
        if url is None:
            return []
        r = self.s.get(url)
        r.raise_for_status()
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        return parse_project_files(r.content, r.url, charset)

    def get_project_url(self, project):
        # Return the URL in the simple API used for the given project
        self.fetch_index()
        return self._projects.get(normalize(project))

    def __contains__(self, project):
        self.fetch_index()
        return normalize(project) in self._projects


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


def get_pip_cache():
    # Return the HTTP cache used by pip
    return FileCache(join(appdirs.user_cache_dir('pip'), 'http'))

def parse_simple_index(html, base_url, from_encoding=None):
    # Returns a list of (project name, url) pairs
    projects = []
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    if soup.base is not None and 'href' in soup.base.attrs:
        base_url = urljoin(base_url, soup.base['href'])
    for link in soup.find_all('a'):
        projects.append((link.string, urljoin(base_url, link['href'])))
    return projects

def parse_project_files(html, base_url, from_encoding=None):
    # Returns a list of DistributionPackage objects
    files = []
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    if soup.base is not None and 'href' in soup.base.attrs:
        base_url = urljoin(base_url, soup.base['href'])
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


ARCHIVE_EXT = r'\.(?:tar\.(?:bz2|gz|xz|Z)|tgz|zip)'

PACKAGE_TYPES = [
    ('dumb', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                        r'-(?P<version>.+?)'
                        r'\.(?:aix|cygwin|darwin|linux|macosx|solaris|sunos'
                            r'|[wW]in)[-.\w]*'
                        + ARCHIVE_EXT + '$')),

    ('egg', re.compile(r'^(?P<project>[A-Za-z0-9._]+)'
                       r'-(?P<version>[^-]+)'
                       r'(?:-[^-]+)*\.egg$')),

    ('msi', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                       r'-(?P<version>.+?)'
                       r'[-.](?:[wW]in32|win-amd64|pentium4|winxp32)'
                       r'(?:-py\d\.\d+(?:-\d+)?)?'
                       r'\.msi$')),

    ('sdist', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                         r'-(?P<version>.+)'
                        + ARCHIVE_EXT + '$')),

    ('wheel', re.compile(r'^(?P<project>[A-Za-z0-9._]+)'
                         r'-(?P<version>[^-]+)'
                         r'(?:-[^-]+)+\.whl$')),

    ('wininst', re.compile(r'^(?P<project>[-A-Za-z0-9._]+)'
                           r'-(?P<version>.+?)'
                           r'[-._](?:aix|cygwin|darwin|linux|macosx|solaris'
                                  r'|sunos|[wW]in)[-.\w]*'
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
