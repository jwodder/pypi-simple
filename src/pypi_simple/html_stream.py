from __future__ import annotations
from codecs import getincrementaldecoder
from collections.abc import Iterable, Iterator
from html.parser import HTMLParser
from itertools import chain
from typing import AnyStr, Optional, cast
from urllib.parse import urljoin
from bs4.dammit import EncodingDetector
import requests
from .html import Link
from .util import check_repo_version

# List taken from BeautifulSoup4 source
EMPTY_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "keygen",
    "link",
    "menuitem",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
    "basefont",
    "bgsound",
    "command",
    "frame",
    "image",
    "isindex",
    "nextid",
    "spacer",
}


class LinkParser(HTMLParser):
    def __init__(self, base_url: Optional[str] = None) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url: Optional[str] = base_url
        self.base_seen = False
        self.tag_stack: list[str] = []
        self.finished_links: list[Link] = []
        self.link_tag_stack: list[dict[str, str]] = []

    def fetch_links(self) -> list[Link]:
        links = self.finished_links
        self.finished_links = []
        return links

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag not in EMPTY_TAGS:
            self.tag_stack.append(tag)
        attrdict = {k: v or "" for k, v in attrs}
        if tag == "base" and "href" in attrdict and not self.base_seen:
            if self.base_url is None:
                self.base_url = attrdict["href"]
            else:
                self.base_url = urljoin(self.base_url, attrdict["href"])
            self.base_seen = True
        elif tag == "a":
            attrdict["#text"] = ""
            self.link_tag_stack.append(attrdict)
        elif (
            tag == "meta"
            and attrdict.get("name") == "pypi:repository-version"
            and "content" in attrdict
        ):
            check_repo_version(attrdict["content"])

    def handle_endtag(self, tag: str) -> None:
        for i in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[i] == tag:
                for t in self.tag_stack[i:]:
                    if t == "a":
                        self.end_link_tag()
                del self.tag_stack[i:]
                break

    def end_link_tag(self) -> None:
        attrs = self.link_tag_stack.pop()
        if "href" in attrs:
            text = attrs.pop("#text")
            if self.base_url is not None:
                url = urljoin(self.base_url, attrs["href"])
            else:
                url = attrs["href"]
            self.finished_links.append(
                Link(
                    text=text.strip(),
                    url=url,
                    attrs=cast("dict[str, str | list[str]]", attrs),
                )
            )

    def handle_data(self, data: str) -> None:
        for link in self.link_tag_stack:
            link["#text"] += data

    def close(self) -> None:
        while self.link_tag_stack:
            self.handle_endtag("a")
        super().close()


def parse_links_stream_response(
    r: requests.Response, chunk_size: int = 65535
) -> Iterator[Link]:
    """
    Parse an HTML page from a streaming `requests.Response` object and yield
    each hyperlink encountered in the document as a `Link` object.

    See `parse_links_stream()` for more information.

    :param requests.Response r: the streaming response object to parse
    :param int chunk_size: how many bytes to read from the response at a time
    :rtype: Iterator[Link]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    return parse_links_stream(
        r.iter_content(chunk_size),
        base_url=r.url,
        http_charset=r.encoding,
    )


def parse_links_stream(
    htmlseq: Iterable[AnyStr],
    base_url: Optional[str] = None,
    http_charset: Optional[str] = None,
) -> Iterator[Link]:
    """
    Parse an HTML page given as an iterable of `bytes` or `str` and yield each
    hyperlink encountered in the document as a `Link` object.

    This function consumes the elements of ``htmlseq`` one at a time and yields
    the links found in each segment before moving on to the next one.  It is
    intended to be faster than `RepositoryPage.from_html()`, especially when
    the complete document is very large.

    .. warning::

        This function is rather experimental.  It does not have full support
        for web encodings, encoding detection, or handling invalid HTML.  It
        also leaves CDATA list attributes on links as strings instead of
        converting them to lists.

    :param Iterable[AnyStr] htmlseq: an iterable of either `bytes` or `str`
        that, when joined together, form an HTML document to parse
    :param Optional[str] base_url: an optional URL to join to the front of the
        links' URLs (usually the URL of the page being parsed)
    :param Optional[str] http_charset: the document's encoding as declared by
        the transport layer, if any; e.g., as declared in the ``charset``
        parameter of the :mailheader:`Content-Type` header of the HTTP response
        that returned the document
    :rtype: Iterator[Link]
    :raises UnsupportedRepoVersionError: if the repository version has a
        greater major component than the supported repository version
    """
    textseq = iterhtmldecode(htmlseq, http_charset=http_charset)
    parser = LinkParser(base_url=base_url)
    for piece in textseq:
        parser.feed(piece)
        for link in parser.fetch_links():
            yield link
    parser.close()
    for link in parser.fetch_links():
        yield link


def iterhtmldecode(
    iterable: Iterable[AnyStr],
    http_charset: Optional[str] = None,
    default_encoding: str = "cp1252",
    errors: str = "replace",
    scan_window: int = 1024,
) -> Iterator[str]:
    """
    Given an HTML document in the form of an iterable of `bytes`, try to
    determine the document's encoding while consuming as little of the iterable
    as necessary, and then decode the elements of the iterable one at a time.

    As a convenience, if an iterable of `str` objects is passed, the elements
    of the iterable are yielded unmodified.

    This function follows a vastly simplified form of the WHATWG's
    `"Determining the Character Encoding" specification <encspec_>`_.  In
    particular, it determines the character encoding by consulting the
    following sources, in order, and using the first one found:

    - byte-order mark
    - HTTP charset
    - encoding declared in document
    - default encoding

    .. _encspec:
       https://html.spec.whatwg.org/multipage/parsing.html
       #determining-the-character-encoding

    :param Iterable[AnyStr] iterable: an iterable of either `bytes` or `str`
        that, when joined together, form an HTML document
    :param Optional[str] http_charset: the document's encoding as declared by
        the transport layer, if any; e.g., as declared in the ``charset``
        parameter of the :mailheader:`Content-Type` header of the HTTP response
        that returned the document
    :param str default_encoding: the default encoding to fall back to if none
        of the other sources succeed in determining the encoding; defaults to
        CP1252
    :param str errors: the error handler to use when decoding the document;
        defaults to ``"replace"``
    :param int scan_window: how many bytes to consume from the iterable when
        checking for an encoding declaration
    :rtype: Iterator[str]
    """

    # We can't use UnicodeDammit directly for this because (a) it gives the
    # encoding extracted from the `Content-Type` header precedence over the
    # encoding indicated by the BOM, when it should be the other way around,
    # and (b) it assumes it's got the whole document to work with and will fail
    # if the given blob ends in the middle of a multibyte character encoding.

    iterator = iter(iterable)
    try:
        initblob = next(iterator)
    except StopIteration:
        return iter(cast("list[str]", []))
    if isinstance(initblob, str):
        return chain([initblob], iterator)
    while len(initblob) < scan_window:
        try:
            initblob += next(iterator)
        except StopIteration:
            break
    enc: Optional[str]
    initblob, enc = EncodingDetector.strip_byte_order_mark(initblob)
    if enc is None:
        if http_charset is not None:
            enc = http_charset
        else:
            enc = EncodingDetector.find_declared_encoding(
                initblob,
                is_html=True,
                search_entire_document=True,
            )
            if enc is None:
                enc = default_encoding
    assert isinstance(enc, str)
    return iterdecode(chain([initblob], iterator), enc, errors=errors)


def iterdecode(
    iterable: Iterable[bytes],
    encoding: str,
    errors: str = "strict",
) -> Iterator[str]:
    """
    Decode an iterable of `bytes` that together form a single document one
    element at a time.

    :param Iterable[bytes] iterable: the bytes to decode
    :param str encoding: the encoding to decode from
    :param str errors: the error handler to use
    :rtype: Iterator[str]
    """
    decoder = getincrementaldecoder(encoding)(errors=errors)
    for blob in iterable:
        yield decoder.decode(blob)
    yield decoder.decode(b"", True)
