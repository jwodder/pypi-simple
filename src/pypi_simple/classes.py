from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Any, Optional
from urllib.parse import urlparse, urlunparse
from .filenames import parse_filename
from .util import basejoin


@dataclass
class Link:
    """A hyperlink extracted from an HTML page"""

    #: The text inside the link tag, with leading & trailing whitespace removed
    #: and with any tags nested inside the link tags ignored
    text: str

    #: The URL that the link points to, resolved relative to the URL of the
    #: source HTML page and relative to the page's ``<base>`` href value, if
    #: any
    url: str

    #: A dictionary of attributes set on the link tag (including the unmodified
    #: ``href`` attribute).  Keys are converted to lowercase.  Most attributes
    #: have `str` values, but some (referred to as "CDATA list attributes" by
    #: the HTML spec; e.g., ``"class"``) have values of type ``list[str]``
    #: instead.
    attrs: dict[str, str | list[str]]


@dataclass
class DistributionPackage:
    """
    Information about a versioned archive file from which a Python project
    release can be installed
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
    ) -> "DistributionPackage":
        """
        Construct a `DistributionPackage` from a `Link` on a project page.

        :param Link link: a link parsed from a project page
        :param Optional[str] project_hint: Optionally, the expected value for
            the project name (usually the name of the project page on which the
            link was found).  The name does not need to be normalized.
        :rtype: DistributionPackage
        """

        def get_str_attrib(attrib: str) -> Optional[str]:
            value = link.attrs.get(attrib)
            if value is not None:
                assert isinstance(value, str)
            return value

        project, version, pkg_type = parse_filename(link.text, project_hint)
        urlbits = urlparse(link.url)
        dgst_name, _, dgst_value = urlbits.fragment.partition("=")
        digests = {dgst_name: dgst_value} if dgst_value else {}
        url = urlunparse(urlbits._replace(fragment=""))
        has_sig: Optional[bool]
        gpg_sig = get_str_attrib("data-gpg-sig")
        if gpg_sig is not None:
            has_sig = gpg_sig.lower() == "true"
        else:
            has_sig = None
        mddigest = get_str_attrib("data-dist-info-metadata")
        metadata_digests: Optional[dict[str, str]]
        if mddigest is not None:
            metadata_digests = {}
            m = re.fullmatch(r"(\w+)=([0-9A-Fa-f]+)", mddigest)
            if m:
                metadata_digests[m[1]] = m[2]
        else:
            metadata_digests = None
        yanked_reason = get_str_attrib("data-yanked")
        return cls(
            filename=link.text,
            url=url,
            has_sig=has_sig,
            requires_python=get_str_attrib("data-requires-python"),
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
    def from_pep691_details(
        cls,
        data: Any,
        project_hint: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> "DistributionPackage":
        """
        Construct a `DistributionPackage` from an object taken from the
        ``"files"`` field of a :pep:`691` project detail response.

        :param data: a file dictionary
        :param Optional[str] project_hint: Optionally, the expected value for
            the project name (usually the name of the project page on which the
            link was found).  The name does not need to be normalized.
        :param Optional[str] base_url: an optional URL to join to the front of
            a relative file URL (usually the URL of the page being parsed)
        :rtype: DistributionPackage
        :raises TypeError: if ``data`` is not a `dict`
        """
        if not isinstance(data, dict):
            raise TypeError(
                f"JSON file details object is {type(data)} instead of a dict"
            )
        project, version, pkg_type = parse_filename(data["filename"], project_hint)
        yanked = data.get("yanked", False)
        yanked_reason: Optional[str]
        if isinstance(yanked, str):
            is_yanked = True
            yanked_reason = yanked
        else:
            is_yanked = bool(yanked)
            yanked_reason = None
        mddigest = data.get("dist-info-metadata")
        metadata_digests: Optional[dict[str, str]]
        if mddigest is None:
            has_metadata = None
            metadata_digests = None
        elif mddigest is False:
            has_metadata = False
            metadata_digests = None
        elif mddigest is True:
            has_metadata = True
            metadata_digests = {}
        else:
            has_metadata = True
            metadata_digests = mddigest
        return cls(
            filename=data["filename"],
            url=basejoin(base_url, data["url"]),
            has_sig=data.get("gpg-sig"),
            requires_python=data.get("requires-python"),
            project=project,
            version=version,
            package_type=pkg_type,
            is_yanked=is_yanked,
            yanked_reason=yanked_reason,
            digests=data["hashes"],
            metadata_digests=metadata_digests,
            has_metadata=has_metadata,
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
