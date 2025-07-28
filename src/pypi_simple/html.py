from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
from .enums import ProjectStatus
from .util import basejoin, check_repo_version


@dataclass
class RepositoryPage:
    """
    .. versionadded:: 1.0.0

    A parsed HTML page from a :pep:`503` simple repository
    """

    #: The repository version, if any, reported by the page in accordance with
    #: :pep:`629`
    repository_version: Optional[str]

    #: A list of hyperlinks found on the page
    links: list[Link]

    #: .. versionadded:: 1.4.0
    #:
    #: ``<meta/>`` tags found on the page whose ``name`` attributes start with
    #: ``pypi:``.  This is a dict in which the keys are ``name`` attributes
    #: with leading ``"pypi:"`` removed and in which the values are the
    #: corresponding ``content`` attributes.
    pypi_meta: dict[str, list[str]]

    @property
    def tracks(self) -> list[str]:
        """
        .. versionadded:: 1.4.0

        Repository "tracks" metadata.  See `PEP 708`__.

        __ https://peps.python.org/pep-0708/#repository-tracks-metadata
        """
        return self.pypi_meta.get("tracks", [])

    @property
    def alternate_locations(self) -> list[str]:
        """
        .. versionadded:: 1.4.0

        Repository "alternate locations" metadata.  See `PEP 708`__.

        __ https://peps.python.org/pep-0708/#alternate-locations-metadata
        """
        return self.pypi_meta.get("alternate-locations", [])

    @property
    def status(self) -> ProjectStatus | None:
        """
        .. versionadded:: 1.7.0

        Project status marker, or `None` if not specified.  See :pep:`792`.
        """
        if st := self.pypi_meta.get("project-status"):
            return ProjectStatus(st[0])
        else:
            return None

    @property
    def status_reason(self) -> str | None:
        """
        .. versionadded:: 1.7.0

        Freeform text contextualizing `status`, or `None` if not specified.
        See :pep:`792` for more information.
        """
        return self.pypi_meta.get("project-status-reason", [None])[0]

    @classmethod
    def from_html(
        cls,
        html: str | bytes,
        base_url: Optional[str] = None,
        from_encoding: Optional[str] = None,
    ) -> RepositoryPage:
        """
        Parse an HTML page from a simple repository into a `RepositoryPage`.

        :param html: the HTML to parse
        :type html: str or bytes
        :param Optional[str] base_url:
            an optional URL to join to the front of the links' URLs (usually
            the URL of the page being parsed)
        :param Optional[str] from_encoding:
            an optional hint to Beautiful Soup as to the encoding of ``html``
            when it is `bytes` (usually the ``charset`` parameter of the
            response's :mailheader:`Content-Type` header)
        :rtype: RepositoryPage
        :raises UnsupportedRepoVersionError:
            if the repository version has a greater major component than the
            supported repository version
        """
        soup = BeautifulSoup(html, "html.parser", from_encoding=from_encoding)
        base_tag = soup.find("base", href=True)
        if base_tag is not None:
            assert isinstance(base_tag, Tag)
            href = base_tag["href"]
            assert isinstance(href, str)
            if base_url is None:
                base_url = href
            else:
                base_url = urljoin(base_url, href)
        meta: dict[str, list[str]] = {}
        for tag in soup.find_all(
            "meta", attrs={"name": re.compile(r"^pypi:"), "content": True}
        ):
            assert isinstance(tag, Tag)
            name = tag["name"]
            assert isinstance(name, str)
            assert name.startswith("pypi:")
            content = tag["content"]
            assert isinstance(content, str)
            meta.setdefault(name[5:], []).append(content)
        try:
            repository_version = meta["repository-version"][0]
        except LookupError:
            repository_version = None
        if repository_version is not None:
            check_repo_version(repository_version)
        links = []
        for link in soup.find_all("a", href=True):
            links.append(
                Link(
                    text="".join(link.strings).strip(),
                    url=basejoin(base_url, link["href"]),
                    attrs=link.attrs,
                )
            )
        return cls(repository_version=repository_version, links=links, pypi_meta=meta)


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

    def get_str_attrib(self, attrib: str) -> Optional[str]:
        """:meta private:"""
        value = self.attrs.get(attrib)
        if value is not None:
            assert isinstance(value, str)
        return value
