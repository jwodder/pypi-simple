from collections  import namedtuple
from urllib.parse import urlparse, urlunparse

class DistributionPackage(
    namedtuple(
        'DistributionPackage',
        'filename url project version package_type requires_python has_sig'
        ' yanked',
    )
):
    """
    Information about a versioned archived file from which a Python project
    release can be installed

    .. attribute:: filename

        The basename of the package file

    .. attribute:: url

        The URL from which the package file can be downloaded

    .. attribute:: project

        The name of the project (as extracted from the filename), or `None` if
        the filename cannot be parsed

    .. attribute:: version

        The project version (as extracted from the filename), or `None` if the
        filename cannot be parsed

    .. attribute:: package_type

        The type of the package, or `None` if the filename cannot be parsed.
        The recognized package types are:

        - ``'dumb'``
        - ``'egg'``
        - ``'msi'``
        - ``'rpm'``
        - ``'sdist'``
        - ``'wheel'``
        - ``'wininst'``

    .. attribute:: requires_python

        An optional version specifier string declaring the Python version(s) in
        which the package can be installed

    .. attribute:: has_sig

        Whether the package file is accompanied by a PGP signature file.   This
        is `None` if the package repository does not report such information.

    .. attribute:: yanked

        If the package file has been "yanked" from the package repository
        (meaning that it should only be installed when that specific version is
        requested), this attribute will be a string giving the reason why it
        was yanked; otherwise, it is `None`.
    """

    @property
    def sig_url(self):
        """
        The URL of the package file's PGP signature file, if it exists; cf.
        ``has_sig``
        """
        u = urlparse(self.url)
        return urlunparse((u[0], u[1], u[2] + '.asc', '', '', ''))

    def get_digests(self):
        """
        Extracts the hash digests from the package file's URL and returns a
        `dict` mapping hash algorithm names to hex-encoded digest strings
        """
        name, sep, value = urlparse(self.url).fragment.partition('=')
        return {name: value} if value else {}
