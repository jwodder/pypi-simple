import re
from typing import Any, Dict, List, NamedTuple, Optional, Union
from urllib.parse import urlparse, urlunparse
from warnings import warn
from .filenames import parse_filename
from .util import basejoin


class Link(NamedTuple):
    """
    .. versionadded:: 0.7.0

    A hyperlink extracted from an HTML page
    """

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
    #: the HTML spec; e.g., ``"class"``) have values of type ``List[str]``
    #: instead.
    attrs: Dict[str, Union[str, List[str]]]


class DistributionPackage(NamedTuple):
    """
    Information about a versioned archive file from which a Python project
    release can be installed

    .. versionchanged:: 0.5.0
        `yanked` attribute added

    .. versionchanged:: 0.9.0
        `has_metadata`, `metadata_url`, and `metadata_digests` attributes added

    .. versionchanged:: 0.10.0
        `digests` attribute added
    """

    #: The basename of the package file
    filename: str

    #: The URL from which the package file can be downloaded, with any hash
    #: digest fragment removed
    #:
    #: .. versionchanged:: 0.10.0
    #:     Hash digest fragments are now stripped from the URL
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

    #: An optional version specifier string declaring the Python version(s) in
    #: which the package can be installed
    requires_python: Optional[str]

    #: Whether the package file is accompanied by a PGP signature file.  This
    #: is `None` if the package repository does not report such information.
    #:
    #: .. versionchanged:: 0.7.0
    #:     Will now be `None` if not specified by repository; previously would
    #:     be `False` in such a situation
    has_sig: Optional[bool]

    #: If the package file has been "yanked" from the package repository
    #: (meaning that it should only be installed when that specific version is
    #: requested), this attribute will be a string giving the reason why it was
    #: yanked; otherwise, it is `None`.
    yanked: Optional[str]

    #: A collection of hash digests for the file as a `dict` mapping hash
    #: algorithm names to hex-encoded digest strings
    digests: Dict[str, str]

    #: Whether the package file is accompanied by a Core Metadata file.  This
    #: is `None` if the package repository does not report such information.
    #:
    #: .. versionchanged:: 0.10.0
    #:     Will now be `None` if not specified by repository
    has_metadata: Optional[bool] = None

    #: If the package repository provides a Core Metadata file for the package,
    #: this is a (possibly empty) `dict` of digests of the file, given as a
    #: mapping from hash algorithm names to hex-encoded digest strings;
    #: otherwise, it is `None`
    metadata_digests: Optional[Dict[str, str]] = None

    @property
    def sig_url(self) -> str:
        """
        The URL of the package file's PGP signature file, if it exists; cf.
        `has_sig`

        .. versionchanged:: 0.6.0
            Now always defined; would previously be `None` if `has_sig` was
            false
        """
        u = urlparse(self.url)
        return urlunparse((u[0], u[1], u[2] + ".asc", "", "", ""))

    @property
    def metadata_url(self) -> str:
        """
        The URL of the package file's Core Metadata file, if it exists; cf.
        `has_metadata`

        .. versionchanged:: 0.10.0
            Now always defined; would previously be `None` if `has_metadata`
            was false
        """
        u = urlparse(self.url)
        return urlunparse((u[0], u[1], u[2] + ".metadata", "", "", ""))

    def get_digests(self) -> Dict[str, str]:
        """
        Returns the hash digests for the file as a `dict` mapping hash
        algorithm names to hex-encoded digest strings

        .. deprecated:: 0.10.0

            Use `digests` instead
        """
        warn(
            "The get_digests() method is deprecated.  Use the `digests`"
            " attribute instead.",
            DeprecationWarning,
        )
        return self.digests

    @classmethod
    def from_link(
        cls, link: Link, project_hint: Optional[str] = None
    ) -> "DistributionPackage":
        """
        .. versionadded:: 0.7.0

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
        metadata_digests: Optional[Dict[str, str]]
        if mddigest is not None:
            metadata_digests = {}
            m = re.fullmatch(r"(\w+)=([0-9A-Fa-f]+)", mddigest)
            if m:
                metadata_digests[m[1]] = m[2]
        else:
            metadata_digests = None
        return cls(
            filename=link.text,
            url=url,
            has_sig=has_sig,
            requires_python=get_str_attrib("data-requires-python"),
            project=project,
            version=version,
            package_type=pkg_type,
            yanked=get_str_attrib("data-yanked"),
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
        .. versionadded:: 0.10.0

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
        yankfield = data.get("yanked", False)
        yanked: Optional[str]
        if yankfield is True:
            yanked = ""
        elif yankfield is False:
            yanked = None
        else:
            if not isinstance(yankfield, str):
                raise TypeError(f'"yanked" field is not a str: {yankfield!r}')
            yanked = yankfield
        mddigest = data.get("dist-info-metadata")
        metadata_digests: Optional[Dict[str, str]]
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
            yanked=yanked,
            digests=data["hashes"],
            metadata_digests=metadata_digests,
            has_metadata=has_metadata,
        )


class ProjectPage(NamedTuple):
    """
    .. versionadded:: 0.7.0

    A parsed project page from a simple repository
    """

    #: The name of the project the page is for
    project: str

    #: A list of packages (as `DistributionPackage` objects) listed on the
    #: project page
    packages: List[DistributionPackage]

    #: The repository version reported by the page, or `None` if not specified
    repository_version: Optional[str]

    #: The value of the :mailheader:`X-PyPI-Last-Serial` response header
    #: returned when fetching the page, or `None` if not specified
    last_serial: Optional[str]


class IndexPage(NamedTuple):
    """
    .. versionadded:: 0.7.0

    A parsed index/root page from a simple repository
    """

    #: The project names listed in the index.  The names are not normalized.
    projects: List[str]

    #: The repository version reported by the page, or `None` if not specified
    repository_version: Optional[str]

    #: The value of the :mailheader:`X-PyPI-Last-Serial` response header
    #: returned when fetching the page, or `None` if not specified
    last_serial: Optional[str]
