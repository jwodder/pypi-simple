import platform
from   typing          import Any, Iterable, List, Optional
from   packaging.utils import canonicalize_name as normalize
import requests
from   .               import __url__, __version__
from   .distpkg        import DistributionPackage
from   .parsing        import parse_project_page, parse_simple_index

#: The base URL for PyPI's simple API
PYPI_SIMPLE_ENDPOINT: str = 'https://pypi.org/simple/'

#: The User-Agent header used for requests; not used when the user provides eir
#: own session object
USER_AGENT: str = 'pypi-simple/{} ({}) requests/{} {}/{}'.format(
    __version__,
    __url__,
    requests.__version__,
    platform.python_implementation(),
    platform.python_version(),
)

class PyPISimple:
    """
    A client for fetching package information from a Python simple package
    repository

    :param str endpoint: The base URL of the simple API instance to query;
        defaults to the base URL for PyPI's simple API

    :param auth: Optional login/authentication details for the repository;
        either a ``(username, password)`` pair or `another authentication
        object accepted by requests
        <https://requests.readthedocs.io/en/master/user/authentication/>`_

    :param session: Optional `requests.Session` object to use instead of
        creating a fresh one
    """

    def __init__(self, endpoint: str = PYPI_SIMPLE_ENDPOINT, auth: Any = None,
                 session: Optional[requests.Session] = None) -> None:
        self.endpoint: str = endpoint.rstrip('/') + '/'
        self.s: requests.Session
        if session is not None:
            self.s = session
        else:
            self.s = requests.Session()
            self.s.headers["User-Agent"] = USER_AGENT
        if auth is not None:
            self.s.auth = auth

    def get_projects(self) -> Iterable[str]:
        """
        Returns a generator of names of projects available in the repository.
        The names are not normalized.

        .. warning::

            PyPI's project index file is very large and takes several seconds
            to parse.  Use this method sparingly.
        """
        r = self.s.get(self.endpoint)
        r.raise_for_status()
        charset: Optional[str]
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        for name, _ in parse_simple_index(r.content, r.url, charset):
            yield name

    def get_project_files(self, project: str) -> List[DistributionPackage]:
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
        charset: Optional[str]
        if 'charset' in r.headers.get('content-type', '').lower():
            charset = r.encoding
        else:
            charset = None
        return parse_project_page(r.content, r.url, charset, project)

    def get_project_url(self, project: str) -> str:
        """
        Returns the URL for the given project's page in the repository.

        :param str project: The name of the project to build a URL for.  The
            name does not need to be normalized.
        """
        return self.endpoint + normalize(project) + '/'
