from __future__ import annotations
from io import StringIO
from typing import Optional
import pytest
from pypi_simple import (
    SUPPORTED_REPOSITORY_VERSION,
    Link,
    UnsupportedRepoVersionError,
    parse_links_stream,
)


@pytest.mark.parametrize(
    "html,base_url,links",
    [
        (
            """
            <html>
            <head><title>Basic test</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            """
            <html>
            <head><title>Test with base_url</title></head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "https://test.nil/base/",
            [
                Link(
                    "link1",
                    "https://test.nil/base/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://test.nil/base/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link(
                    "link1",
                    "https://nil.test/path/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two", "https://nil.test/path/two.html", {"href": "two.html"}
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base target="_new"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base/>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link(
                    "link1",
                    "https://nil.test/path/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://nil.test/path/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        # I'm not sure if this is how HTML is supposed to work, but it is how
        # pip works: <https://github.com/pypa/pip/blob/18.0/src/pip/_internal/index.py#L878>
        (
            """
            <html>
            <head>
                <title>Test with &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
                <base href="https://example.invalid/subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link(
                    "link1",
                    "https://nil.test/path/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://nil.test/path/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with both base_url and an absolute &lt;base&gt; tag</title>
                <base href="https://nil.test/path/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "https://test.nil/base/",
            [
                Link(
                    "link1",
                    "https://nil.test/path/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://nil.test/path/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with both base_url and a relative &lt;base&gt; tag</title>
                <base href="subdir/"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "https://test.nil/base/",
            [
                Link(
                    "link1",
                    "https://test.nil/base/subdir/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://test.nil/base/subdir/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test with uppercase tags &amp; attributes</title>
                <BASE HREF="https://nil.test/path/"/>
            </head>
            <body>
            <A HREF="one.html">link1</a>
            <A HREF="two.html">link-two</A>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link(
                    "link1",
                    "https://nil.test/path/one.html",
                    {"href": "one.html"},
                ),
                Link(
                    "link-two",
                    "https://nil.test/path/two.html",
                    {"href": "two.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test links with leading &amp; trailing whitespace</title>
            </head>
            <body>
            <a href="one.html"> whitespaced  </a>
            <a href="two.html">multiple words</a>
            <a href="three.html"> <!-- comment -->  preceded by a comment </a>
            </body>
            </html>
        """,
            None,
            [
                Link("whitespaced", "one.html", {"href": "one.html"}),
                Link("multiple words", "two.html", {"href": "two.html"}),
                Link(
                    "preceded by a comment",
                    "three.html",
                    {"href": "three.html"},
                ),
            ],
        ),
        (
            """
            <html>
            <head>
                <title>Test that &lt;a&gt; tags without href are ignored</title>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a name="two">target</a>
            </body>
            </html>
        """,
            None,
            [Link("link1", "one.html", {"href": "one.html"})],
        ),
        (
            """
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            '<a href="https://files.pythonhosted.org/packages/05/35/'
            "aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/"
            "txtble-0.1.0-py2.py3-none-any.whl#sha256="
            '25103e370ee304327751856ef5ecd7f59f9be88269838c7b558d4ac692d3e375"'
            ' data-requires-python="&gt;=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*,'
            ' &lt;4">txtble-0.1.0-py2.py3-none-any.whl</a><br/>',
            None,
            [
                Link(
                    "txtble-0.1.0-py2.py3-none-any.whl",
                    "https://files.pythonhosted.org/packages/05/35/aa8dc452b75"
                    "3bd9b405a0d23ee3ebac693edd2d0a5896bcc2c98f6263039/txtble-"
                    "0.1.0-py2.py3-none-any.whl#sha256=25103e370ee304327751856"
                    "ef5ecd7f59f9be88269838c7b558d4ac692d3e375",
                    {
                        "href": "https://files.pythonhosted.org/packages/05/35"
                        "/aa8dc452b753bd9b405a0d23ee3ebac693edd2d0a589"
                        "6bcc2c98f6263039/txtble-0.1.0-py2.py3-none-an"
                        "y.whl#sha256=25103e370ee304327751856ef5ecd7f5"
                        "9f9be88269838c7b558d4ac692d3e375",
                        "data-requires-python": ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                    },
                ),
            ],
        ),
        (
            '<a href="https://test.nil/simple/files/project-0.1.0-p&#xFF;42-none'
            '-any.whl">project-0.1.0-p&#xFF;42-none-any.whl</a>',
            None,
            [
                Link(
                    "project-0.1.0-p\xFF42-none-any.whl",
                    "https://test.nil/simple/files/project-0.1.0-p\xFF42-none"
                    "-any.whl",
                    {
                        "href": "https://test.nil/simple/files/project-0.1.0-"
                        "p\xFF42-none-any.whl",
                    },
                )
            ],
        ),
        (
            '<a href="https://test.nil/simple/files/project-0.1.0-p&yuml;42-none'
            '-any.whl">project-0.1.0-p&yuml;42-none-any.whl</a>',
            None,
            [
                Link(
                    "project-0.1.0-p\xFF42-none-any.whl",
                    "https://test.nil/simple/files/project-0.1.0-p\xFF42-none"
                    "-any.whl",
                    {
                        "href": "https://test.nil/simple/files/project-0.1.0-"
                        "p\xFF42-none-any.whl",
                    },
                ),
            ],
        ),
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="1.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="repository-version" content="42.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two
        """,
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
    ],
)
def test_parse_links_stream(
    html: str, base_url: Optional[str], links: list[Link]
) -> None:
    assert list(parse_links_stream(StringIO(html), base_url)) == links


@pytest.mark.parametrize(
    "htmlseq,charset,links",
    [
        ([], None, []),
        (
            [
                b"\xFF\xFE<\x00h\x00t\x00m\x00l\x00>\x00\n\x00",
                "<head><title>UTF-16LE</title></head>\n".encode("utf-16le"),
                "<body>\n".encode("utf-16le"),
                '<a href="one.html">link1</a>\n'.encode("utf-16le"),
                '<a href="two.html">link-two</a>\n'.encode("utf-16le"),
                "</body>\n".encode("utf-16le"),
                "</html>\n".encode("utf-16le"),
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"\xFF\xFE<\x00h\x00t\x00m\x00l\x00>\x00\n\x00",
                "<!-- This is a very long comment to ensure that `scan_window = 1024` bytes are consumed before reaching the end of all of the data.  What can I write about... So, how about that sports team?  Aren't they very sporty?  ... Forget it, I'll just multiply this string a few times. -->".encode(
                    "utf-16le"
                )
                * 2,
                "<head><title>UTF-16LE</title></head>\n".encode("utf-16le"),
                "<body>\n".encode("utf-16le"),
                '<a href="one.html">link1</a>\n'.encode("utf-16le"),
                '<a href="two.html">link-two</a>\n'.encode("utf-16le"),
                "</body>\n".encode("utf-16le"),
                "</html>\n".encode("utf-16le"),
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"\xFF\xFE<\x00h\x00t\x00m\x00l\x00>\x00\n\x00",
                "<head>\n".encode("utf-16le"),
                "<title>UTF-16LE</title>\n".encode("utf-16le"),
                '<meta charset="iso-8859-1"/>\n'.encode("utf-16le"),
                "</head>\n".encode("utf-16le"),
                "<body>\n".encode("utf-16le"),
                '<a href="one.html">link1</a>\n'.encode("utf-16le"),
                '<a href="two.html">link-two</a>\n'.encode("utf-16le"),
                "</body>\n".encode("utf-16le"),
                "</html>\n".encode("utf-16le"),
            ],
            "utf-8",
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-two", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>MacRoman</title>\n",
                b'<meta charset="macroman"/>\n',
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\xB9</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-π", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>Latin-1</title>\n",
                b'<meta charset="latin-1"/>\n',
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\xC3\xB0</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-\xC3\xB0", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>UTF-8</title>\n",
                b'<meta charset="latin-1"/>\n',
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\xC3\xB0</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            "utf-8",
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-\xF0", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>CP437</title>\n",
                b'<meta charset="cp437"/>\n',
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\x8E</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-Ä", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>CP437</title>\n",
                b'<meta http-equiv="Content-Type" content="text/html; charset=cp437"/>\n',
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\x8E</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-Ä", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b'<?xml version="1.0" encoding="cp437"?>\n',
                b"<html>\n",
                b"<head>\n",
                b"<title>CP437</title>\n",
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\x8E</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-Ä", "two.html", {"href": "two.html"}),
            ],
        ),
        (
            [
                b"<html>\n",
                b"<head>\n",
                b"<title>CP1252</title>\n",
                b"</head>\n",
                b"<body>\n",
                b'<a href="one.html">link1</a>\n',
                b'<a href="two.html">link-\x8E</a>\n',
                b"</body>\n",
                b"</html>\n",
            ],
            None,
            [
                Link("link1", "one.html", {"href": "one.html"}),
                Link("link-Ž", "two.html", {"href": "two.html"}),
            ],
        ),
    ],
)
def test_parse_links_stream_iterable_bytes(
    htmlseq: list[bytes], charset: Optional[str], links: list[Link]
) -> None:
    assert list(parse_links_stream(htmlseq, http_charset=charset)) == links


@pytest.mark.parametrize(
    "html,version",
    [
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="42.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "42.0",
        ),
        ### TODO: This one's behavior differs from RepositoryPage.from_html();
        ### should they be aligned?
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="1.0"/>
            <meta name="pypi:repository-version" content="5.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "5.0",
        ),
        (
            """
            <html>
            <head>
            <title>Basic test</title>
            <meta name="pypi:repository-version" content="5.0"/>
            <meta name="pypi:repository-version" content="1.0"/>
            </head>
            <body>
            <a href="one.html">link1</a>
            <a href="two.html">link-two</a>
            <span href="zero.html">not-a-link</span>
            </body>
            </html>
        """,
            "5.0",
        ),
    ],
)
def test_parse_links_stream_unsupported_version(html: str, version: str) -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        list(parse_links_stream(StringIO(html)))
    assert excinfo.value.declared_version == version
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        f"Repository's version ({version}) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )
