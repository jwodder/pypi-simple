from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from .util import basejoin, check_repo_version


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


def parse_repo_links(
    html: str | bytes,
    base_url: Optional[str] = None,
    from_encoding: Optional[str] = None,
) -> tuple[dict[str, str], list[Link]]:
    """
    Parse an HTML page from a simple repository and return a ``(metadata,
    links)`` pair.

    The ``metadata`` element is a ``dict[str, str]``.  Currently, the only key
    that may appear in it is ``"repository_version"``, which maps to the
    repository version reported by the HTML page in accordance with :pep:`629`.
    If the HTML page does not contain a repository version, this key is absent
    from the `dict`.

    The ``links`` element is a list of `Link` objects giving the hyperlinks
    found in the HTML page.

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        links' URLs (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: tuple[dict[str, str], list[Link]]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    soup = BeautifulSoup(html, "html.parser", from_encoding=from_encoding)
    base_tag = soup.find("base", href=True)
    if base_tag is not None:
        if base_url is None:
            base_url = base_tag["href"]
        else:
            base_url = urljoin(base_url, base_tag["href"])
    metadata = {}
    pep629_meta = soup.find(
        "meta",
        attrs={"name": "pypi:repository-version", "content": True},
    )
    if pep629_meta is not None:
        metadata["repository_version"] = pep629_meta["content"]
        check_repo_version(metadata["repository_version"])
    links = []
    for link in soup.find_all("a", href=True):
        links.append(
            Link(
                text="".join(link.strings).strip(),
                url=basejoin(base_url, link["href"]),
                attrs=link.attrs,
            )
        )
    return (metadata, links)
