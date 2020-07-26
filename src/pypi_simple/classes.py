from typing       import Dict, List, NamedTuple, Optional, Union
from urllib.parse import urlparse, urlunparse
from .filenames   import parse_filename

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
    """

    #: The basename of the package file
    filename: str

    #: The URL from which the package file can be downloaded
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

    #: Whether the package file is accompanied by a PGP signature file.   This
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
        return urlunparse((u[0], u[1], u[2] + '.asc', '', '', ''))

    def get_digests(self) -> Dict[str, str]:
        """
        Extracts the hash digests from the package file's URL and returns a
        `dict` mapping hash algorithm names to hex-encoded digest strings
        """
        name, sep, value = urlparse(self.url).fragment.partition('=')
        return {name: value} if value else {}

    @classmethod
    def from_link(cls, link: Link, project_hint: Optional[str] = None) \
            -> 'DistributionPackage':
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
        has_sig: Optional[bool]
        gpg_sig = get_str_attrib("data-gpg-sig")
        if gpg_sig is not None:
            has_sig = gpg_sig.lower() == 'true'
        else:
            has_sig = None
        return cls(
            filename        = link.text,
            url             = link.url,
            has_sig         = has_sig,
            requires_python = get_str_attrib("data-requires-python"),
            project         = project,
            version         = version,
            package_type    = pkg_type,
            yanked          = get_str_attrib("data-yanked"),
        )


class ProjectPage(NamedTuple):
    """
    .. versionadded:: 0.7.0

    A parsed project page fom a simple repository
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
