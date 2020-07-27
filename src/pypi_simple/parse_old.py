from typing       import Dict, Iterator, List, Optional, Tuple, Union
from urllib.parse import urljoin
from warnings     import warn
from bs4          import BeautifulSoup
from .classes     import DistributionPackage
from .parse_repo  import parse_repo_links

def parse_simple_index(html: Union[str, bytes], base_url: Optional[str] = None,
                       from_encoding: Optional[str] = None) \
        -> Iterator[Tuple[str, str]]:
    """
    Parse a simple repository's index page and return a generator of ``(project
    name, project URL)`` pairs

    .. deprecated:: 0.7.0
        Use `parse_repo_index_page()` or `parse_links_stream()` instead

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        URLs returned (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: Iterator[Tuple[str, str]]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    warn(
        'parse_simple_index() is deprecated.'
        '  Use parse_repo_index_page() or parse_links_stream() instead.',
        DeprecationWarning,
    )
    for link in parse_repo_links(html, base_url, from_encoding)[1]:
        yield (link.text, link.url)

def parse_project_page(html: Union[str, bytes], base_url: Optional[str] = None,
                       from_encoding: Optional[str] = None,
                       project_hint: Optional[str] = None) \
        -> List[DistributionPackage]:
    """
    Parse a project page from a simple repository and return a list of
    `DistributionPackage` objects

    .. deprecated:: 0.7.0
        Use `parse_repo_project_page()` instead

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        packages' URLs (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :param Optional[str] project_hint: The name of the project whose page is
        being parsed; used to disambiguate the parsing of certain filenames
    :rtype: List[DistributionPackage]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    warn(
        'parse_project_page() is deprecated.'
        '  Use parse_repo_project_page() instead.',
        DeprecationWarning,
    )
    return [
        DistributionPackage.from_link(link, project_hint)
        for link in parse_repo_links(html, base_url, from_encoding)[1]
    ]

def parse_links(html: Union[str, bytes], base_url: Optional[str] = None,
                from_encoding: Optional[str] = None) \
        -> Iterator[Tuple[str, str, Dict[str, Union[str, List[str]]]]]:
    """
    Parse an HTML page and return a generator of links, where each link is
    represented as a triple of link text, link URL, and a `dict` of link tag
    attributes (including the unmodified ``href`` attribute).

    Link text has all leading & trailing whitespace removed.

    Keys in the attributes `dict` are converted to lowercase.

    .. deprecated:: 0.7.0
        Use `parse_repo_links()` instead

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        URLs returned (usually the URL of the page being parsed)
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes` (usually the ``charset``
        parameter of the response's :mailheader:`Content-Type` header)
    :rtype: Iterator[Tuple[str, str, Dict[str, Union[str, List[str]]]]]
    """
    warn(
        'parse_links() is deprecated.  Use parse_repo_links() instead.',
        DeprecationWarning,
    )
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    base_tag = soup.find('base', href=True)
    if base_tag is not None:
        if base_url is None:
            base_url = base_tag['href']
        else:
            base_url = urljoin(base_url, base_tag['href'])
    if base_url is None:
        def basejoin(url: str) -> str:
            return url
    else:
        def basejoin(url: str) -> str:
            assert isinstance(base_url, str)
            return urljoin(base_url, url)
    for link in soup.find_all('a', href=True):
        yield (
            ''.join(link.strings).strip(),
            basejoin(link['href']),
            link.attrs,
        )
