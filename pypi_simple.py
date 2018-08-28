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
class ProjectFile:
    filename = attr.ib()
    url = attr.ib()
    requires_python = attr.ib(default=None)

    @property
    def project(self):
        raise NotImplementedError

    @property
    def version(self):
        raise NotImplementedError

    @property
    def has_sig(self):
        raise NotImplementedError

    @property
    def sig_url(self):
        # Returns None if no signature
        raise NotImplementedError

    @property
    def package_type(self):  ### Rethink name
        # wheel, sdist, egg, etc.
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
