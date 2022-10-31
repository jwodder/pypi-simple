from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Any, Optional
from urllib.parse import urlparse, urlunparse
from mailbits import ContentType
import requests
from .errors import UnparsableFilenameError, UnsupportedContentTypeError
from .filenames import parse_filename
from .html import Link, RepositoryPage
from .pep691 import File, Project, ProjectList
from .util import basejoin, check_repo_version


@dataclass
class DistributionPackage:
    """
    Information about a versioned archive file from which a Python project
    release can be installed

    .. versionchanged:: 1.0.0

        ``yanked`` field replaced with `is_yanked` and `yanked_reason`
    """

    #: The basename of the package file
    filename: str

    #: The URL from which the package file can be downloaded, with any hash
    #: digest fragment removed
    url: str

    #: The name of the project (as extracted from the filename), or `None` if
    #: the filename cannot be parsed
    project: Optional[str]

    #: The project version (as extracted from the filename), or `None` if the
    #: filename cannot be parsed
    version: Optional[str]

    #: The type of the package, or `None` if the filename cannot be parsed.
    #: The recognized package types are:
    #:
    #: - ``'dumb'``
    #: - ``'egg'``
    #: - ``'msi'``
    #: - ``'rpm'``
    #: - ``'sdist'``
    #: - ``'wheel'``
    #: - ``'wininst'``
    package_type: Optional[str]

    #: A collection of hash digests for the file as a `dict` mapping hash
    #: algorithm names to hex-encoded digest strings
    digests: dict[str, str]

    #: An optional version specifier string declaring the Python version(s) in
    #: which the package can be installed
    requires_python: Optional[str]

    #: Whether the package file is accompanied by a PGP signature file.  This
    #: is `None` if the package repository does not report such information.
    has_sig: Optional[bool]

    #: Whether the package file has been "yanked" from the package repository
    #: (meaning that it should only be installed when that specific version is
    #: requested)
    is_yanked: bool = False

    #: If the package file has been "yanked" and a reason is given, this
    #: attribute will contain that (possibly empty) reason
    yanked_reason: Optional[str] = None

    #: Whether the package file is accompanied by a Core Metadata file.  This
    #: is `None` if the package repository does not report such information.
    has_metadata: Optional[bool] = None

    #: If the package repository provides a Core Metadata file for the package,
    #: this is a (possibly empty) `dict` of digests of the file, given as a
    #: mapping from hash algorithm names to hex-encoded digest strings;
    #: otherwise, it is `None`
    metadata_digests: Optional[dict[str, str]] = None

    @property
    def sig_url(self) -> str:
        """
        The URL of the package file's PGP signature file, if it exists; cf.
        `has_sig`
        """
        u = urlparse(self.url)
        return urlunparse((u[0], u[1], u[2] + ".asc", "", "", ""))

    @property
    def metadata_url(self) -> str:
        """
        The URL of the package file's Core Metadata file, if it exists; cf.
        `has_metadata`
        """
        u = urlparse(self.url)
        return urlunparse((u[0], u[1], u[2] + ".metadata", "", "", ""))

    @classmethod
    def from_link(
        cls, link: Link, project_hint: Optional[str] = None
    ) -> DistributionPackage:
        """
        Construct a `DistributionPackage` from a `Link` on a project page.

        :param Link link: a link parsed from a project page
        :param Optional[str] project_hint: Optionally, the expected value for
            the project name (usually the name of the project page on which the
            link was found).  The name does not need to be normalized.
        :rtype: DistributionPackage
        """
        try:
            project, version, pkg_type = parse_filename(link.text, project_hint)
        except UnparsableFilenameError:
            project = None
            version = None
            pkg_type = None
        urlbits = urlparse(link.url)
        dgst_name, _, dgst_value = urlbits.fragment.partition("=")
        digests = {dgst_name: dgst_value} if dgst_value else {}
        url = urlunparse(urlbits._replace(fragment=""))
        has_sig: Optional[bool]
        gpg_sig = link.get_str_attrib("data-gpg-sig")
        if gpg_sig is not None:
            has_sig = gpg_sig.lower() == "true"
        else:
            has_sig = None
        mddigest = link.get_str_attrib("data-dist-info-metadata")
        metadata_digests: Optional[dict[str, str]]
        if mddigest is not None:
            metadata_digests = {}
            m = re.fullmatch(r"(\w+)=([0-9A-Fa-f]+)", mddigest)
            if m:
                metadata_digests[m[1]] = m[2]
        else:
            metadata_digests = None
        yanked_reason = link.get_str_attrib("data-yanked")
        return cls(
            filename=link.text,
            url=url,
            has_sig=has_sig,
            requires_python=link.get_str_attrib("data-requires-python"),
            project=project,
            version=version,
            package_type=pkg_type,
            is_yanked=yanked_reason is not None,
            yanked_reason=yanked_reason,
            digests=digests,
            metadata_digests=metadata_digests,
            has_metadata=metadata_digests is not None,
        )

    @classmethod
    def from_json_data(
        cls,
        data: Any,
        project_hint: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> DistributionPackage:
        """
        Construct a `DistributionPackage` from an object taken from the
        ``"files"`` field of a :pep:`691` project detail JSON response.

        :param data: a file dictionary
        :param Optional[str] project_hint: Optionally, the expected value for
            the project name (usually the name of the project page on which the
            link was found).  The name does not need to be normalized.
        :param Optional[str] base_url: an optional URL to join to the front of
            a relative file URL (usually the URL of the page being parsed)
        :rtype: DistributionPackage
        :raises ValueError: if ``data`` is not a `dict`
        """
        return cls.from_file(File.parse_obj(data), project_hint, base_url)

    @classmethod
    def from_file(
        cls,
        file: File,
        project_hint: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> DistributionPackage:
        """:meta private:"""
        try:
            project, version, pkg_type = parse_filename(file.filename, project_hint)
        except UnparsableFilenameError:
            project = None
            version = None
            pkg_type = None
        return cls(
            filename=file.filename,
            url=basejoin(base_url, file.url),
            has_sig=file.gpg_sig,
            requires_python=file.requires_python,
            project=project,
            version=version,
            package_type=pkg_type,
            is_yanked=file.is_yanked,
            yanked_reason=file.yanked_reason,
            digests=file.hashes,
            metadata_digests=file.metadata_digests,
            has_metadata=file.has_metadata,
        )


@dataclass
class ProjectPage:
    """A parsed project page from a simple repository"""

    #: The name of the project the page is for
    project: str

    #: A list of packages (as `DistributionPackage` objects) listed on the
    #: project page
    packages: list[DistributionPackage]

    #: The repository version reported by the page, or `None` if not specified
    repository_version: Optional[str]

    #: The value of the :mailheader:`X-PyPI-Last-Serial` response header
    #: returned when fetching the page, or `None` if not specified
    last_serial: Optional[str]

    @classmethod
    def from_html(
        cls,
        project: str,
        html: str | bytes,
        base_url: Optional[str] = None,
        from_encoding: Optional[str] = None,
    ) -> ProjectPage:
        """
        .. versionadded:: 1.0.0

        Parse an HTML project page from a simple repository into a
        `ProjectPage`.  Note that the `last_serial` attribute will be `None`.

        :param str project: The name of the project whose page is being parsed
        :param html: the HTML to parse
        :type html: str or bytes
        :param Optional[str] base_url:
            an optional URL to join to the front of the packages' URLs (usually
            the URL of the page being parsed)
        :param Optional[str] from_encoding:
            an optional hint to Beautiful Soup as to the encoding of ``html``
            when it is `bytes` (usually the ``charset`` parameter of the
            response's :mailheader:`Content-Type` header)
        :rtype: ProjectPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        """
        page = RepositoryPage.from_html(html, base_url, from_encoding)
        return cls(
            project=project,
            packages=[
                DistributionPackage.from_link(link, project) for link in page.links
            ],
            repository_version=page.repository_version,
            last_serial=None,
        )

    @classmethod
    def from_json_data(cls, data: Any, base_url: Optional[str] = None) -> ProjectPage:
        """
        .. versionadded:: 1.0.0

        Parse an object decoded from an
        :mimetype:`application/vnd.pypi.simple.v1+json` response (See
        :pep:`691`) into a `ProjectPage`.  The `last_serial` attribute will be
        set to the value of the ``.meta._last-serial`` field, if any.

        :param data: The decoded body of the JSON response
        :param Optional[str] base_url:
            an optional URL to join to the front of any relative file URLs
            (usually the URL of the page being parsed)
        :rtype: ProjectPage
        :raises ValueError: if ``data`` is not a `dict`
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        """
        project = Project.parse_obj(data)
        check_repo_version(project.meta.api_version)
        return ProjectPage(
            project=project.name,
            packages=[
                DistributionPackage.from_file(f, project.name, base_url)
                for f in project.files
            ],
            repository_version=project.meta.api_version,
            last_serial=project.meta.last_serial,
        )

    @classmethod
    def from_response(cls, r: requests.Response, project: str) -> ProjectPage:
        """
        .. versionadded:: 1.0.0

        Parse a project page from a `requests.Response` returned from a
        (non-streaming) request to a simple repository, and return a
        `ProjectPage`.

        :param requests.Response r: the response object to parse
        :param str project: the name of the project whose page is being parsed
        :rtype: ProjectPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        :raises UnsupportedContentTypeError:
            if the response has an unsupported :mailheader:`Content-Type`
        """
        ct = ContentType.parse(r.headers.get("content-type", "text/html"))
        if ct.content_type == "application/vnd.pypi.simple.v1+json":
            page = cls.from_json_data(r.json(), r.url)
        elif (
            ct.content_type == "application/vnd.pypi.simple.v1+html"
            or ct.content_type == "text/html"
        ):
            page = cls.from_html(
                project=project,
                html=r.content,
                base_url=r.url,
                from_encoding=ct.params.get("charset"),
            )
        else:
            raise UnsupportedContentTypeError(r.url, str(ct))
        if page.last_serial is None:
            page.last_serial = r.headers.get("X-PyPI-Last-Serial")
        return page


@dataclass
class IndexPage:
    """A parsed index/root page from a simple repository"""

    #: The project names listed in the index.  The names are not normalized.
    projects: list[str]

    #: The repository version reported by the page, or `None` if not specified
    repository_version: Optional[str]

    #: The value of the :mailheader:`X-PyPI-Last-Serial` response header
    #: returned when fetching the page, or `None` if not specified
    last_serial: Optional[str]

    @classmethod
    def from_html(
        cls, html: str | bytes, from_encoding: Optional[str] = None
    ) -> IndexPage:
        """
        .. versionadded:: 1.0.0

        Parse an HTML index/root page from a simple repository into an
        `IndexPage`.  Note that the `last_serial` attribute will be `None`.

        :param html: the HTML to parse
        :type html: str or bytes
        :param Optional[str] from_encoding:
            an optional hint to Beautiful Soup as to the encoding of ``html``
            when it is `bytes` (usually the ``charset`` parameter of the
            response's :mailheader:`Content-Type` header)
        :rtype: IndexPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        """
        page = RepositoryPage.from_html(html, from_encoding=from_encoding)
        return cls(
            projects=[link.text for link in page.links],
            repository_version=page.repository_version,
            last_serial=None,
        )

    @classmethod
    def from_json_data(cls, data: Any) -> IndexPage:
        """
        .. versionadded:: 1.0.0

        Parse an object decoded from an
        :mimetype:`application/vnd.pypi.simple.v1+json` response (See
        :pep:`691`) into an `IndexPage`.  The `last_serial` attribute will be
        set to the value of the ``.meta._last-serial`` field, if any.

        :param data: The decoded body of the JSON response
        :rtype: IndexPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        :raises ValueError: if ``data`` is not a `dict`
        """
        plist = ProjectList.parse_obj(data)
        check_repo_version(plist.meta.api_version)
        return IndexPage(
            projects=[p.name for p in plist.projects],
            repository_version=plist.meta.api_version,
            last_serial=plist.meta.last_serial,
        )

    @classmethod
    def from_response(cls, r: requests.Response) -> IndexPage:
        """
        .. versionadded:: 1.0.0

        Parse an index page from a `requests.Response` returned from a
        (non-streaming) request to a simple repository, and return an
        `IndexPage`.

        :param requests.Response r: the response object to parse
        :rtype: IndexPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        :raises UnsupportedContentTypeError:
            if the response has an unsupported :mailheader:`Content-Type`
        """
        ct = ContentType.parse(r.headers.get("content-type", "text/html"))
        if ct.content_type == "application/vnd.pypi.simple.v1+json":
            page = cls.from_json_data(r.json())
        elif (
            ct.content_type == "application/vnd.pypi.simple.v1+html"
            or ct.content_type == "text/html"
        ):
            page = cls.from_html(html=r.content, from_encoding=ct.params.get("charset"))
        else:
            raise UnsupportedContentTypeError(r.url, str(ct))
        if page.last_serial is None:
            page.last_serial = r.headers.get("X-PyPI-Last-Serial")
        return page
