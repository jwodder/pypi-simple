import attr

PYPI_SIMPLE_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple:
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
class ProjectFile:  ### Rename to "DistributionPackage" or similar?
    filename = attr.ib()
    url = attr.ib()
    requires_python = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.project, self.version, self.package_type \
            = parse_filename(self.filename)

    @property
    def has_sig(self):
        raise NotImplementedError

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
    raise NotImplementedError

def parse_project_files(html, base_url, from_encoding=None):
    # Returns a list of ProjectFile objects
    raise NotImplementedError

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
    raise NotImplementedError
