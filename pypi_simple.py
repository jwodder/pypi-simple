PYPI_ENDPOINT = 'https://pypi.org/simple/'

class PyPISimple:
    def __init__(self, endpoint=PYPI_ENDPOINT, cache=None):
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

    ### Something for forcibly refetching the index page?


class ProjectFile:
    @property
    def filename(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def requires_python(self):
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

    ### file hashes


def get_pip_cache():
    # Return the HTTP cache used by pip
    raise NotImplementedError

def parse_simple_index(html, base_url):
    # Returns a list of (project name, url) pairs
    raise NotImplementedError

def parse_project_files(html, base_url):
    # Returns a list of ProjectFile objects
    raise NotImplementedError
