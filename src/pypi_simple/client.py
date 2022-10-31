from __future__ import annotations
from collections.abc import Callable, Iterator
import os
from pathlib import Path
import platform
from types import TracebackType
from typing import Any, AnyStr, Optional
from mailbits import ContentType
from packaging.utils import canonicalize_name as normalize
import requests
from . import ACCEPT_ANY, PYPI_SIMPLE_ENDPOINT, __url__, __version__
from .classes import DistributionPackage, IndexPage, ProjectPage
from .errors import UnsupportedContentTypeError
from .html_stream import parse_links_stream_response
from .progress import ProgressTracker, null_progress_tracker
from .util import AbstractDigestChecker, DigestChecker, NullDigestChecker

#: The User-Agent header used for requests; not used when the user provides eir
#: own session object
USER_AGENT: str = "pypi-simple/{} ({}) requests/{} {}/{}".format(
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

    .. versionchanged:: 1.0.0

        ``accept`` parameter added

    :param str endpoint: The base URL of the simple API instance to query;
        defaults to the base URL for PyPI's simple API

    :param auth: Optional login/authentication details for the repository;
        either a ``(username, password)`` pair or `another authentication
        object accepted by requests
        <https://requests.readthedocs.io/en/master/user/authentication/>`_

    :param session: Optional `requests.Session` object to use instead of
        creating a fresh one

    :param str accept:
        The :mailheader:`Accept` header to send in requests in order to specify
        what serialization format the server should return; defaults to
        `ACCEPT_ANY`
    """

    def __init__(
        self,
        endpoint: str = PYPI_SIMPLE_ENDPOINT,
        auth: Any = None,
        session: Optional[requests.Session] = None,
        accept: str = ACCEPT_ANY,
    ) -> None:
        self.endpoint: str = endpoint.rstrip("/") + "/"
        self.s: requests.Session
        if session is not None:
            self.s = session
        else:
            self.s = requests.Session()
            self.s.headers["User-Agent"] = USER_AGENT
        if auth is not None:
            self.s.auth = auth
        self.accept = accept

    def __enter__(self) -> PyPISimple:
        return self

    def __exit__(
        self,
        _exc_type: Optional[type[BaseException]],
        _exc_val: Optional[BaseException],
        _exc_tb: Optional[TracebackType],
    ) -> None:
        self.s.close()

    def get_index_page(
        self,
        timeout: float | tuple[float, float] | None = None,
        accept: Optional[str] = None,
    ) -> IndexPage:
        """
        Fetches the index/root page from the simple repository and returns an
        `IndexPage` instance.

        .. warning::

            PyPI's project index file is very large and takes several seconds
            to parse.  Use this method sparingly.

        .. versionchanged:: 1.0.0

            ``accept`` parameter added

        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: float | tuple[float,float] | None
        :param Optional[str] accept:
            The :mailheader:`Accept` header to send in order to
            specify what serialization format the server should return;
            defaults to the value supplied on client instantiation
        :rtype: IndexPage
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises UnsupportedContentTypeError: if the repository responds with an
            unsupported :mailheader:`Content-Type`
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        r = self.s.get(
            self.endpoint, timeout=timeout, headers={"Accept": accept or self.accept}
        )
        r.raise_for_status()
        return IndexPage.from_response(r)

    def stream_project_names(
        self,
        chunk_size: int = 65535,
        timeout: float | tuple[float, float] | None = None,
        accept: Optional[str] = None,
    ) -> Iterator[str]:
        """
        Returns a generator of names of projects available in the repository.
        The names are not normalized.

        Unlike `get_index_page()`, this function makes a streaming request to
        the server and parses the document in chunks.  It is intended to be
        faster than the other methods, especially when the complete document is
        very large.

        .. warning::

            This function is rather experimental.  It does not have full
            support for web encodings, encoding detection, or handling invalid
            HTML.

        .. note::

            If the server responds with a JSON representation of the Simple API
            rather than an HTML representation, the response body will be
            loaded & parsed in its entirety before yielding anything.

        .. versionchanged:: 1.0.0

            ``accept`` parameter added

        :param int chunk_size: how many bytes to read from the response at a
            time
        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: float | tuple[float,float] | None
        :param Optional[str] accept:
            The :mailheader:`Accept` header to send in order to
            specify what serialization format the server should return;
            defaults to the value supplied on client instantiation
        :rtype: Iterator[str]
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises UnsupportedContentTypeError: if the repository responds with an
            unsupported :mailheader:`Content-Type`
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        with self.s.get(
            self.endpoint,
            stream=True,
            timeout=timeout,
            headers={"Accept": accept or self.accept},
        ) as r:
            r.raise_for_status()
            ct = ContentType.parse(r.headers.get("content-type", "text/html"))
            if ct.content_type == "application/vnd.pypi.simple.v1+json":
                page = IndexPage.from_json_data(r.json())
                yield from page.projects
            elif (
                ct.content_type == "application/vnd.pypi.simple.v1+html"
                or ct.content_type == "text/html"
            ):
                for link in parse_links_stream_response(r, chunk_size):
                    yield link.text
            else:
                raise UnsupportedContentTypeError(r.url, str(ct))

    def get_project_page(
        self,
        project: str,
        timeout: float | tuple[float, float] | None = None,
        accept: Optional[str] = None,
    ) -> ProjectPage:
        """
        Fetches the page for the given project from the simple repository and
        returns a `ProjectPage` instance.  Raises `NoSuchProjectError` if the
        repository responds with a 404.  All other HTTP errors cause a
        `requests.HTTPError` to be raised.

        .. versionchanged:: 1.0.0

            - A 404 now causes `NoSuchProjectError` to be raised instead of
              returning `None`

            - ``accept`` parameter added

        :param str project: The name of the project to fetch information on.
            The name does not need to be normalized.
        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: float | tuple[float,float] | None
        :param Optional[str] accept:
            The :mailheader:`Accept` header to send in order to
            specify what serialization format the server should return;
            defaults to the value supplied on client instantiation
        :rtype: ProjectPage
        :raises NoSuchProjectError: if the repository responds with a 404 error
            code
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code other than 404
        :raises UnsupportedContentTypeError: if the repository responds with an
            unsupported :mailheader:`Content-Type`
        :raises UnsupportedRepoVersionError: if the repository version has a
            greater major component than the supported repository version
        """
        url = self.get_project_url(project)
        r = self.s.get(url, timeout=timeout, headers={"Accept": accept or None})
        if r.status_code == 404:
            raise NoSuchProjectError(project, url)
        r.raise_for_status()
        return ProjectPage.from_response(r, project)

    def get_project_url(self, project: str) -> str:
        """
        Returns the URL for the given project's page in the repository.

        :param str project: The name of the project to build a URL for.  The
            name does not need to be normalized.
        :rtype: str
        """
        return self.endpoint + normalize(project) + "/"

    def download_package(
        self,
        pkg: DistributionPackage,
        path: AnyStr | os.PathLike[AnyStr],
        verify: bool = True,
        keep_on_error: bool = False,
        progress: Optional[Callable[[Optional[int]], ProgressTracker]] = None,
        timeout: float | tuple[float, float] | None = None,
    ) -> None:
        """
        Download the given `DistributionPackage` to the given path.

        If an error occurs while downloading or verifying digests, and
        ``keep_on_error`` is not true, the downloaded file is not saved.

        Download progress can be tracked (e.g., for display by a progress bar)
        by passing an appropriate callable as the ``progress`` argument.  This
        callable will be passed the length of the downloaded file, if known,
        and it must return a `ProgressTracker` — a context manager with an
        ``update(increment: int)`` method that will be passed the size of each
        downloaded chunk as each chunk is received.

        :param DistributionPackage pkg: the distribution package to download
        :param path:
            the path at which to save the downloaded file; any parent
            directories of this path will be created as needed
        :param bool verify:
            whether to verify the package's digests against the downloaded file
        :param bool keep_on_error:
            whether to keep (true) or delete (false) the downloaded file if an
            error occurs
        :param progress: a callable for constructing a progress tracker
        :param timeout: optional timeout to pass to the ``requests`` call
        :type timeout: float | tuple[float,float] | None
        :raises requests.HTTPError: if the repository responds with an HTTP
            error code
        :raises NoDigestsError:
            if ``verify`` is true and the given package does not have any
            digests with known algorithms
        :raises DigestMismatchError:
            if ``verify`` is true and the digest of the downloaded file does
            not match the expected value
        """
        target = Path(os.fsdecode(path))
        target.parent.mkdir(parents=True, exist_ok=True)
        digester: AbstractDigestChecker
        if verify:
            digester = DigestChecker(pkg.digests)
        else:
            digester = NullDigestChecker()
        with self.s.get(pkg.url, stream=True, timeout=timeout) as r:
            r.raise_for_status()
            try:
                content_length = int(r.headers["Content-Length"])
            except (ValueError, KeyError):
                content_length = None
            if progress is None:
                progress = null_progress_tracker()
            try:
                with progress(content_length) as p:
                    with target.open("wb") as fp:
                        for chunk in r.iter_content(65535):
                            fp.write(chunk)
                            digester.update(chunk)
                            p.update(len(chunk))
                digester.finalize()
            except Exception:
                if not keep_on_error:
                    try:
                        target.unlink()
                    except FileNotFoundError:
                        pass
                raise


class NoSuchProjectError(Exception):
    """
    Raised by `PyPISimple.get_project_page()` when a request for a project
    fails with a 404 error code
    """

    def __init__(self, project: str, url: str) -> None:
        #: The name of the project requested
        self.project = project
        #: The URL to which the failed request was made
        self.url = url

    def __str__(self) -> str:
        return f"No details about project {self.project!r} available at {self.url}"
