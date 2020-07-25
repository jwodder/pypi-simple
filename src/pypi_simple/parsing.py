from typing       import Dict, Iterable, List, Optional, Tuple, Union, cast
from urllib.parse import urljoin
from bs4          import BeautifulSoup
from .distpkg     import DistributionPackage
from .filenames   import parse_filename

def parse_simple_index(html: Union[str, bytes], base_url: Optional[str] = None,
                       from_encoding: Optional[str] = None) \
        -> Iterable[Tuple[str, str]]:
    """
    Parse a simple repository's index page and return a generator of ``(project
    name, project URL)`` pairs

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        URLs returned
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes`
    :rtype: Iterable[Tuple[str, str]]
    """
    for filename, url, _ in parse_links(html, base_url, from_encoding):
        yield (filename, url)

def parse_project_page(html: Union[str, bytes], base_url: Optional[str] = None,
                       from_encoding: Optional[str] = None,
                       project_hint: Optional[str] = None) \
        -> List[DistributionPackage]:
    """
    Parse a project page from a simple repository and return a list of
    `DistributionPackage` objects

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        packages' URLs
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes`
    :param Optional[str] project_hint: The name of the project whose page is
        being parsed; used to disambiguate the parsing of certain filenames
    :rtype: List[DistributionPackage]
    """
    files = []
    for filename, url, attrs in parse_links(html, base_url, from_encoding):
        project, version, pkg_type = parse_filename(filename, project_hint)
        has_sig: Optional[bool]
        try:
            has_sig = cast(str, attrs["data-gpg-sig"]).lower() == 'true'
        except KeyError:
            has_sig = None
        files.append(DistributionPackage(
            filename = filename,
            url = url,
            has_sig = has_sig,
            requires_python = cast(
                Optional[str],
                attrs.get('data-requires-python'),
            ),
            project = project,
            version = version,
            package_type = pkg_type,
            yanked = cast(Optional[str], attrs.get('data-yanked')),
        ))
    return files

def parse_links(html: Union[str, bytes], base_url: Optional[str] = None,
                from_encoding: Optional[str] = None) \
        -> Iterable[Tuple[str, str, Dict[str, Union[str, List[str]]]]]:
    """
    Parse an HTML page and return a generator of links, where each link is
    represented as a triple of link text, link URL, and a `dict` of link tag
    attributes (including the unmodified ``href`` attribute).

    Link text has all leading & trailing whitespace removed.

    Keys in the attributes `dict` are converted to lowercase.

    :param html: the HTML to parse
    :type html: str or bytes
    :param Optional[str] base_url: an optional URL to join to the front of the
        URLs returned
    :param Optional[str] from_encoding: an optional hint to Beautiful Soup as
        to the encoding of ``html`` when it is `bytes`
    :rtype: Iterable[Tuple[str, str, Dict[str, Union[str, List[str]]]]]
    """
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
