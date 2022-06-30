from __future__ import annotations
import re
from typing import Optional
from .errors import UnparsableFilenameError

PROJECT_NAME = r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?"
PROJECT_NAME_NODASH = r"[A-Za-z0-9](?:[A-Za-z0-9._]*[A-Za-z0-9])?"
VERSION = r"[A-Za-z0-9_.!+-]+?"
VERSION_NODASH = r"[A-Za-z0-9_.!+]+?"
ARCHIVE_EXT = r"\.(?:tar|tar\.(?:bz2|gz|lz|lzma|xz|Z)|tbz|tgz|tlz|txz|zip)"
PLAT_NAME = r"(?:aix|cygwin|darwin|linux|macosx|solaris|sunos|[wW]in)[-.A-Za-z0-9_]*"
PYVER = r"py[0-9]+\.[0-9]+"

#: Regexes for package filenames that can be parsed unambiguously
GOOD_PACKAGE_RGXN = [
    # See <https://setuptools.readthedocs.io/en/latest
    #      /formats.html#filename-embedded-metadata>:
    (
        "egg",
        re.compile(
            r"^(?P<project>{})-(?P<version>{})(?:-{}(?:-{})?)?\.egg$".format(
                PROJECT_NAME_NODASH, VERSION_NODASH, PYVER, PLAT_NAME
            )
        ),
    ),
    # See <http://ftp.rpm.org/max-rpm/ch-rpm-file-format.html>:
    # (The architecture pattern is mainly just a guess based on what's
    # currently on PyPI.)
    (
        "rpm",
        re.compile(
            r"^(?P<project>{})-(?P<version>{})-[^-]+\.[A-Za-z0-9._]+\.rpm$".format(
                PROJECT_NAME, VERSION_NODASH
            )
        ),
    ),
    # Regex adapted from <https://github.com/pypa/pip/blob/18.0/src/pip/_internal/wheel.py#L569>:
    (
        "wheel",
        re.compile(
            r"^(?P<project>{})-(?P<version>{})(-[0-9][^-]*?)?"
            r"-.+?-.+?-.+?\.whl$".format(PROJECT_NAME_NODASH, VERSION_NODASH)
        ),
    ),
]

#: Partial regexes for package filenames with ambiguous grammars.  If a hint as
#: to the expected project name is given, it will be prepended to the regexes
#: when trying to determine a match; otherwise, a generic pattern that matches
#: all project names will be prepended.
BAD_PACKAGE_BASES = [
    # See <https://github.com/python/cpython/blob/v3.7.0/Lib/distutils/command/bdist_dumb.py#L93>:
    (
        "dumb",
        re.compile(r"-(?P<version>{})\.{}{}$".format(VERSION, PLAT_NAME, ARCHIVE_EXT)),
    ),
    # See <https://github.com/python/cpython/blob/v3.7.0/Lib/distutils/command/bdist_msi.py#L733>:
    (
        "msi",
        re.compile(
            r"-(?P<version>{})\.{}(?:-{})?\.msi$".format(VERSION, PLAT_NAME, PYVER)
        ),
    ),
    ("sdist", re.compile(r"-(?P<version>{}){}$".format(VERSION, ARCHIVE_EXT))),
    # See <https://github.com/python/cpython/blob/v3.7.0/Lib/distutils/command/bdist_wininst.py#L292>:
    (
        "wininst",
        re.compile(
            r"-(?P<version>{})\.{}(?:-{})?\.exe$".format(VERSION, PLAT_NAME, PYVER)
        ),
    ),
]

#: Regexes for package filenames with ambiguous grammars, using a generic
#: pattern that matches all project names
BAD_PACKAGE_RGXN = [
    (pkg_type, re.compile("^(?P<project>" + PROJECT_NAME + ")" + rgx.pattern))
    for pkg_type, rgx in BAD_PACKAGE_BASES
]


def parse_filename(
    filename: str, project_hint: Optional[str] = None
) -> tuple[str, str, str]:
    """
    Given the filename of a distribution package, returns a triple of the
    project name, project version, and package type.  The name and version are
    spelled the same as they appear in the filename; no normalization is
    performed.

    The package type may be any of the following strings:

    - ``'dumb'``
    - ``'egg'``
    - ``'msi'``
    - ``'rpm'``
    - ``'sdist'``
    - ``'wheel'``
    - ``'wininst'``

    Note that some filenames (e.g., :file:`1-2-3.tar.gz`) may be ambiguous as
    to which part is the project name and which is the version.  In order to
    resolve the ambiguity, the expected value for the project name (*modulo*
    normalization) can be supplied as the ``project_name`` argument to the
    function.  If the filename can be parsed with the given string in the role
    of the project name, the results of that parse will be returned; otherwise,
    the function will fall back to breaking the project & version apart at an
    unspecified point.

    .. versionchanged:: 1.0.0

        Now raises `UnparsableFilenameError` for unparsable filenames instead
        of returning all `None`\\s

    :param str filename: The package filename to parse
    :param Optional[str] project_hint: Optionally, the expected value for the
        project name (usually the name of the project page on which the
        filename was found).  The name does not need to be normalized.
    :rtype: tuple[str, str, str]
    :raises UnparsableFilenameError: if the filename cannot be parsed
    """
    for pkg_type, rgx in GOOD_PACKAGE_RGXN:
        m = rgx.match(filename)
        if m:
            return (m.group("project"), m.group("version"), pkg_type)
    if project_hint is not None:
        proj_rgx = re.sub(r"[^A-Za-z0-9]+", "[-_.]+", project_hint)
        proj_rgx = re.sub(
            r"([A-Za-z])",
            lambda m: "[" + m.group(1).upper() + m.group(1).lower() + "]",
            proj_rgx,
        )
        m = re.match(proj_rgx + r"(?=-)", filename)
        if m:
            project = m.group(0)
            rest_of_name = filename[m.end(0) :]
            for pkg_type, rgx in BAD_PACKAGE_BASES:
                m = rgx.match(rest_of_name)
                if m:
                    return (project, m.group("version"), pkg_type)
    for pkg_type, rgx in BAD_PACKAGE_RGXN:
        m = rgx.match(filename)
        if m:
            return (m.group("project"), m.group("version"), pkg_type)
    raise UnparsableFilenameError(filename)
