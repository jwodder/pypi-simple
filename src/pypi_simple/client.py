import platform
from   typing          import Any, Iterator, List, Optional, Tuple, Union
from   warnings        import warn
from   packaging.utils import canonicalize_name as normalize
import requests
from   .               import PYPI_SIMPLE_ENDPOINT, __url__, __version__
from   .classes        import DistributionPackage, IndexPage, ProjectPage
from   .parse_repo     import parse_repo_index_response, \
                                parse_repo_project_response
from   .parse_stream   import parse_links_stream_response

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
    repository.

    If necessary, login/authentication details for the repository can be
    specified at initialization by setting the ``auth`` parameter to either a
    ``(username, password)`` pair or `another authentication object accepted by
    requests
    <https://requests.readthedocs.io/en/master/user/authentication/>`_.

    If more complicated session configuration is desired (e.g., setting up
    caching), the user must create & configure a `requests.Session` object
    appropriately and pass it to the constructor as the ``session`` parameter.

    A `PyPISimple` instance can be used as a context manager that will
    automatically close its session on exit, regardless of where the session
    object came from.

    .. versionchanged:: 0.8.0
        Now usable as a context manager

    .. versionchanged:: 0.5.0
        ``session`` argument added

    .. versionchanged:: 0.4.0
        ``auth`` argument added

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

    def __enter__(self) -> "PyPISimple":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_tb: Any) -> None:
        self.s.close()

    def get_index_page(
        self,
        timeout: Union[float, Tuple[float,float], None] = None,
    ) -> IndexPage:
        """
        .. versionadded:: 0.7.0

        Fetches the index/root page from the simple repository and returns an
        `IndexPage` instance.

        .. warning::

            PyPI's project index file is very large and takes several seconds
            to parse.  Use this method sparingly.

        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: Union[float, Tuple[float,float], None]
        :rtype: IndexPage
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        r = self.s.get(self.endpoint, timeout=timeout)
        r.raise_for_status()
        return parse_repo_index_response(r)

    def stream_project_names(
        self,
        chunk_size: int = 65535,
        timeout: Union[float, Tuple[float,float], None] = None,
    ) -> Iterator[str]:
        """
        .. versionadded:: 0.7.0

        Returns a generator of names of projects available in the repository.
        The names are not normalized.

        Unlike `get_index_page()` and `get_projects()`, this function makes a
        streaming request to the server and parses the document in chunks.  It
        is intended to be faster than the other methods, especially when the
        complete document is very large.

        .. warning::

            This function is rather experimental.  It does not have full
            support for web encodings, encoding detection, or handling invalid
            HTML.

        :param int chunk_size: how many bytes to read from the response at a
            time
        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: Union[float, Tuple[float,float], None]
        :rtype: Iterator[str]
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        with self.s.get(self.endpoint, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            for link in parse_links_stream_response(r, chunk_size):
                yield link.text

    def get_project_page(
        self,
        project: str,
        timeout: Union[float, Tuple[float,float], None] = None,
    ) -> Optional[ProjectPage]:
        """
        .. versionadded:: 0.7.0

        Fetches the page for the given project from the simple repository and
        returns a `ProjectPage` instance.  Returns `None` if the repository
        responds with a 404.  All other HTTP errors cause a
        `requests.HTTPError` to be raised.

        :param str project: The name of the project to fetch information on.
            The name does not need to be normalized.
        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: Union[float, Tuple[float,float], None]
        :rtype: Optional[ProjectPage]
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code other than 404
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        url = self.get_project_url(project)
        r = self.s.get(url, timeout=timeout)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return parse_repo_project_response(project, r)

    def get_project_url(self, project: str) -> str:
        """
        Returns the URL for the given project's page in the repository.

        :param str project: The name of the project to build a URL for.  The
            name does not need to be normalized.
        :rtype: str
        """
        return self.endpoint + normalize(project) + '/'

    def get_projects(self) -> Iterator[str]:
        """
        Returns a generator of names of projects available in the repository.
        The names are not normalized.

        .. warning::

            PyPI's project index file is very large and takes several seconds
            to parse.  Use this method sparingly.

        .. deprecated:: 0.7.0
            Use `get_index_page()` or `stream_project_names()` instead

        :rtype: Iterator[str]
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        warn(
            'The get_projects() method is deprecated.  Use get_index_page() or'
            ' stream_project_names() instead.',
            DeprecationWarning,
        )
        page = self.get_index_page()
        return iter(page.projects)

    def get_project_files(self, project: str) -> List[DistributionPackage]:
        """
        Returns a list of `DistributionPackage` objects representing all of the
        package files available in the repository for the given project.

        When fetching the project's information from the repository, a 404
        response is treated the same as an empty page, resulting in an empty
        list.  All other HTTP errors cause a `requests.HTTPError` to be raised.

        .. deprecated:: 0.7.0
            Use `get_project_page()` instead

        :param str project: The name of the project to fetch information on.
            The name does not need to be normalized.
        :rtype: List[DistributionPackage]
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code other than 404
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        warn(
            'The get_project_files() method is deprecated.'
            '  Use get_project_page() instead.',
            DeprecationWarning,
        )
        page = self.get_project_page(project)
        if page is None:
            return []
        else:
            return page.packages
