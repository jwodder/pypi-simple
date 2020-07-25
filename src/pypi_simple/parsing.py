from urllib.parse import urljoin
from bs4          import BeautifulSoup
from .distpkg     import DistributionPackage
from .filenames   import parse_filename

def parse_simple_index(html, base_url=None, from_encoding=None):
    """
    Parse a simple repository's index page and return a generator of ``(project
    name, project URL)`` pairs

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to join to the front of the URLs
        returned
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    for filename, url, _ in parse_links(html, base_url, from_encoding):
        yield (filename, url)

def parse_project_page(html, base_url=None, from_encoding=None,
                                            project_hint=None):
    """
    Parse a project page from a simple repository and return a list of
    `DistributionPackage` objects

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to join to the front of the packages'
        URLs
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    :param str project_hint: The name of the project whose page is being
        parsed; used to disambiguate the parsing of certain filenames
    """
    files = []
    for filename, url, attrs in parse_links(html, base_url, from_encoding):
        project, version, pkg_type = parse_filename(filename, project_hint)
        try:
            has_sig = attrs["data-gpg-sig"].lower() == 'true'
        except KeyError:
            has_sig = None
        files.append(DistributionPackage(
            filename = filename,
            url = url,
            has_sig = has_sig,
            requires_python = attrs.get('data-requires-python'),
            project = project,
            version = version,
            package_type = pkg_type,
            yanked = attrs.get('data-yanked'),
        ))
    return files

def parse_links(html, base_url=None, from_encoding=None):
    """
    Parse an HTML page and return a generator of links, where each link is
    represented as a triple of link text, link URL, and a `dict` of link tag
    attributes (including the unmodified ``href`` attribute).

    Link text has all leading & trailing whitespace removed.

    Keys in the attributes `dict` are converted to lowercase.

    :param html: the HTML to parse
    :type html: str or bytes
    :param str base_url: an optional URL to join to the front of the URLs
        returned
    :param str from_encoding: an optional hint to Beautiful Soup as to the
        encoding of ``html``
    """
    soup = BeautifulSoup(html, 'html.parser', from_encoding=from_encoding)
    base_tag = soup.find('base', href=True)
    if base_tag is not None:
        base_url = urljoin(base_url, base_tag['href'])
    # Note that ``urljoin(None, x) == x``
    for link in soup.find_all('a', href=True):
        yield (
            ''.join(link.strings).strip(),
            urljoin(base_url, link['href']),
            link.attrs,
        )
