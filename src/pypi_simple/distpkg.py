from typing       import Dict, NamedTuple, Optional
from urllib.parse import urlparse, urlunparse

class DistributionPackage(NamedTuple):
    """
    Information about a versioned archived file from which a Python project
    release can be installed
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
