from __future__ import annotations
import filecmp
import json
from pathlib import Path
from types import TracebackType
from typing import Optional
import pytest
from pytest_mock import MockerFixture
import requests
import responses
from pypi_simple import (
    DigestMismatchError,
    DistributionPackage,
    IndexPage,
    NoDigestsError,
    NoSuchProjectError,
    ProgressTracker,
    ProjectPage,
    PyPISimple,
    UnsupportedContentTypeError,
)

DATA_DIR = Path(__file__).with_name("data")


@pytest.mark.parametrize(
    "content_type",
    [
        "text/html",
        "text/html; charset=utf-8",
        "application/vnd.pypi.simple.v1+html",
        "application/vnd.pypi.simple.v1+html; charset=utf-8",
    ],
)
@responses.activate
def test_session(mocker: MockerFixture, content_type: str) -> None:
    session_dir = DATA_DIR / "session01"
    with (session_dir / "simple.html").open() as fp:
        responses.add(
            method=responses.GET,
            url="https://test.nil/simple/",
            body=fp.read(),
            content_type=content_type,
            headers={"x-pypi-last-serial": "12345"},
        )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        body="This URL should only be requested once.",
        status=500,
    )
    with (session_dir / "in-place.html").open() as fp:
        responses.add(
            method=responses.GET,
            url="https://test.nil/simple/in-place/",
            body=fp.read(),
            content_type=content_type,
            headers={"X-PYPI-LAST-SERIAL": "54321"},
        )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/nonexistent/",
        body="Does not exist",
        status=404,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        spy = mocker.spy(simple.s, "get")
        assert simple.get_index_page(timeout=3.14) == IndexPage(
            projects=["in_place", "foo", "BAR"],
            last_serial="12345",
            repository_version="1.0",
        )
        (call,) = spy.call_args_list
        assert call[1]["timeout"] == 3.14
        spy.reset_mock()
        assert simple.get_project_url("IN.PLACE") == "https://test.nil/simple/in-place/"
        assert simple.get_project_page("IN.PLACE", timeout=2.718) == ProjectPage(
            project="IN.PLACE",
            packages=[
                DistributionPackage(
                    filename="in_place-0.1.1-py2.py3-none-any.whl",
                    project="in_place",
                    version="0.1.1",
                    package_type="wheel",
                    url="https://files.pythonhosted.org/packages/34/81/2baaaa588ee1a6faa6354b7c9bc365f1b3da867707cd136dfedff7c06608/in_place-0.1.1-py2.py3-none-any.whl",
                    digests={
                        "sha256": "e0732b6bdc2f1bfc4e1b96c1de2fbbd053bb2a9534547474a0485baa339bfa97"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="in_place-0.1.1.tar.gz",
                    project="in_place",
                    version="0.1.1",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/b9/ba/f1c67fb32c37ba4263326ae4ac6fd00b128025c9289b2fb31a60a0a22f90/in_place-0.1.1.tar.gz",
                    digests={
                        "sha256": "ffa729fd0b818ac750aa31bafc886f266380e1c8557ba38f70f422d2f6a77e23"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="in_place-0.2.0-py2.py3-none-any.whl",
                    project="in_place",
                    version="0.2.0",
                    package_type="wheel",
                    url="https://files.pythonhosted.org/packages/9f/46/9f5679f3b2068e10b33c16a628a78b2b36531a9df08671bd0104f11d8461/in_place-0.2.0-py2.py3-none-any.whl",
                    digests={
                        "sha256": "e1ad42a41dfde02092b411b1634a4be228e28c27553499a81ef04b377b28857c"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="in_place-0.2.0.tar.gz",
                    project="in_place",
                    version="0.2.0",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/f0/51/c30f1fad2b857f7b5d5ff76ec01f1f80dd0f2ab6b6afcde7b2aed54faa7e/in_place-0.2.0.tar.gz",
                    digests={
                        "sha256": "ff783dca5d06f85b8d084871abd11a170d732423edb48c53ccb68c55fcbbeb76"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="in_place-0.3.0-py2.py3-none-any.whl",
                    project="in_place",
                    version="0.3.0",
                    package_type="wheel",
                    url="https://files.pythonhosted.org/packages/6f/84/ced31e646df335f8cd1b7884e3740b8c012314a28504542ef5631cdc1449/in_place-0.3.0-py2.py3-none-any.whl",
                    digests={
                        "sha256": "af5ce9bd309f85a6bbe4119acbc0a67cda68f0ae616f0a76a947addc62791fda"
                    },
                    requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="in_place-0.3.0.tar.gz",
                    project="in_place",
                    version="0.3.0",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/b6/cd/1dc736d5248420b15dd1546c2938aec7e6dab134e698e0768f54f1757af7/in_place-0.3.0.tar.gz",
                    digests={
                        "sha256": "4758db1457c8addcd5f5b15ef870eab66b238e46e7d784bff99ab1b2126660ea"
                    },
                    requires_python=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
            ],
            last_serial="54321",
            repository_version="1.0",
        )
        (call,) = spy.call_args_list
        assert call[1]["timeout"] == 2.718
        with pytest.raises(NoSuchProjectError) as excinfo:
            simple.get_project_page("nonexistent")
        assert excinfo.value.project == "nonexistent"
        assert excinfo.value.url == "https://test.nil/simple/nonexistent/"
        assert str(excinfo.value) == (
            "No details about project 'nonexistent' available at"
            " https://test.nil/simple/nonexistent/"
        )


@responses.activate
def test_project_hint_received() -> None:
    """
    Test that the argument to ``get_project_page()`` is used to disambiguate
    filenames
    """
    with (DATA_DIR / "aws-adfs-ebsco.html").open() as fp:
        responses.add(
            method=responses.GET,
            url="https://test.nil/simple/aws-adfs-ebsco/",
            body=fp.read(),
            content_type="text/html",
        )
    with PyPISimple("https://test.nil/simple/") as simple:
        assert simple.get_project_page("aws-adfs-ebsco") == ProjectPage(
            project="aws-adfs-ebsco",
            packages=[
                DistributionPackage(
                    filename="aws-adfs-ebsco-0.3.6-2.tar.gz",
                    project="aws-adfs-ebsco",
                    version="0.3.6-2",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/13/b7/a69bdbf294db5ba0973ee45a2b2ce7045030cd922e1c0ca052d102c45b95/aws-adfs-ebsco-0.3.6-2.tar.gz",
                    digests={
                        "sha256": "6eadd17408e1f26a313bc75afaa3011333bc2915461c446720bafd7608987e1e"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
                DistributionPackage(
                    filename="aws-adfs-ebsco-0.3.7-1.tar.gz",
                    project="aws-adfs-ebsco",
                    version="0.3.7-1",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/86/8a/46c2a99113cfbb7d6c089b2128ca9e4faaea1f6a1d4e17577fd9a3396bee/aws-adfs-ebsco-0.3.7-1.tar.gz",
                    digests={
                        "sha256": "7992abc36d0061896a3f06f055e053ffde9f3fcf483340adfa675c65ebfb3f8d"
                    },
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://test.nil/simple",
        "https://test.nil/simple/",
    ],
)
@pytest.mark.parametrize(
    "project",
    [
        "some-project",
        "some.project",
        "SOME_PROJECT",
    ],
)
def test_get_project_url(endpoint: str, project: str) -> None:
    with PyPISimple(endpoint) as simple:
        assert (
            simple.get_project_url(project) == "https://test.nil/simple/some-project/"
        )


@responses.activate
def test_redirected_project_page() -> None:
    responses.add(
        method=responses.GET,
        url="https://nil.test/simple/project/",
        status=301,
        headers={"Location": "https://test.nil/simple/project/"},
    )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/project/",
        body='<a href="../files/project-0.1.0.tar.gz">project-0.1.0.tar.gz</a>',
        content_type="text/html",
    )
    with PyPISimple("https://nil.test/simple/") as simple:
        assert simple.get_project_page("project") == ProjectPage(
            project="project",
            packages=[
                DistributionPackage(
                    filename="project-0.1.0.tar.gz",
                    project="project",
                    version="0.1.0",
                    package_type="sdist",
                    url="https://test.nil/simple/files/project-0.1.0.tar.gz",
                    digests={},
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )


@pytest.mark.parametrize(
    "content_type,body_decl",
    [
        ("text/html; charset=utf-8", b""),
        ("text/html", b'<?xml encoding="utf-8"?>'),
        (
            "text/html",
            b'<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>',
        ),
    ],
)
@responses.activate
def test_utf8_declarations(content_type: str, body_decl: bytes) -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/project/",
        body=body_decl
        + b'<a href="../files/project-0.1.0-p\xC3\xBF42-none-any.whl">project-0.1.0-p\xC3\xBF42-none-any.whl</a>',
        content_type=content_type,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        assert simple.get_project_page("project") == ProjectPage(
            project="project",
            packages=[
                DistributionPackage(
                    filename="project-0.1.0-p\xFF42-none-any.whl",
                    project="project",
                    version="0.1.0",
                    package_type="wheel",
                    url="https://test.nil/simple/files/project-0.1.0-p\xFF42-none-any.whl",
                    digests={},
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )


@pytest.mark.parametrize(
    "content_type,body_decl",
    [
        ("text/html; charset=iso-8859-2", b""),
        ("text/html", b'<?xml encoding="iso-8859-2"?>'),
        (
            "text/html",
            b'<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-2"/>',
        ),
    ],
)
@responses.activate
def test_latin2_declarations(content_type: str, body_decl: bytes) -> None:
    # This test is deliberately weird in order to make sure the code is
    # actually paying attention to the encoding declarations and not just
    # assuming UTF-8 because the input happens to be valid UTF-8.
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/project/",
        body=body_decl
        + b'<a href="../files/project-0.1.0-p\xC3\xBF42-none-any.whl">project-0.1.0-p\xC3\xBF42-none-any.whl</a>',
        content_type=content_type,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        assert simple.get_project_page("project") == ProjectPage(
            project="project",
            packages=[
                DistributionPackage(
                    filename="project-0.1.0-p\u0102\u017C42-none-any.whl",
                    project="project",
                    version="0.1.0",
                    package_type="wheel",
                    url="https://test.nil/simple/files/project-0.1.0-p\u0102\u017C42-none-any.whl",
                    digests={},
                    requires_python=None,
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=False,
                ),
            ],
            last_serial=None,
            repository_version=None,
        )


def test_auth_new_session() -> None:
    with PyPISimple("https://test.nil/simple/", auth=("user", "password")) as simple:
        assert simple.s.auth == ("user", "password")


def test_custom_session() -> None:
    s = requests.Session()
    with PyPISimple("https://test.nil/simple/", session=s) as simple:
        assert simple.s is s
        assert simple.s.auth is None


def test_auth_custom_session() -> None:
    with PyPISimple(
        "https://test.nil/simple/",
        auth=("user", "password"),
        session=requests.Session(),
    ) as simple:
        assert simple.s.auth == ("user", "password")


def test_auth_override_custom_session() -> None:
    s = requests.Session()
    s.auth = ("login", "secret")
    with PyPISimple(
        "https://test.nil/simple/",
        auth=("user", "password"),
        session=s,
    ) as simple:
        assert simple.s.auth == ("user", "password")


@responses.activate
def test_stream_project_names(mocker: MockerFixture) -> None:
    session_dir = DATA_DIR / "session01"
    with (session_dir / "simple.html").open() as fp:
        responses.add(
            method=responses.GET,
            url="https://test.nil/simple/",
            body=fp.read(),
            content_type="text/html",
            headers={"x-pypi-last-serial": "12345"},
        )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        body="This URL should only be requested once.",
        status=500,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        spy = mocker.spy(simple.s, "get")
        assert list(simple.stream_project_names(timeout=1.618)) == [
            "in_place",
            "foo",
            "BAR",
        ]
        (call,) = spy.call_args_list
        assert call[1]["timeout"] == 1.618


@responses.activate
def test_stream_project_names_json() -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        json={
            "meta": {"_last-serial": 14267765, "api-version": "1.0"},
            "projects": [{"name": "argset"}, {"name": "banana"}, {"name": "coconut"}],
        },
        content_type="application/vnd.pypi.simple.v1+json",
        headers={"x-pypi-last-serial": "12345"},
    )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        body="This URL should only be requested once.",
        status=500,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        assert list(simple.stream_project_names()) == ["argset", "banana", "coconut"]


@responses.activate
def test_json_session(mocker: MockerFixture) -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        json={
            "meta": {"_last-serial": 14267765, "api-version": "1.0"},
            "projects": [{"name": "argset"}, {"name": "banana"}, {"name": "coconut"}],
        },
        content_type="application/vnd.pypi.simple.v1+json",
        headers={"x-pypi-last-serial": "12345"},
    )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        body="This URL should only be requested once.",
        status=500,
    )
    with (DATA_DIR / "argset.json").open() as fp:
        data = json.load(fp)
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/argset/",
        json=data,
        content_type="application/vnd.pypi.simple.v1+json",
        headers={"X-PYPI-LAST-SERIAL": "54321"},
    )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/nonexistent/",
        body="Does not exist",
        status=404,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        spy = mocker.spy(simple.s, "get")
        assert simple.get_index_page(timeout=3.14) == IndexPage(
            projects=["argset", "banana", "coconut"],
            last_serial="14267765",
            repository_version="1.0",
        )
        (call,) = spy.call_args_list
        assert call[1]["timeout"] == 3.14
        spy.reset_mock()
        assert simple.get_project_page("ARGSET", timeout=2.718) == ProjectPage(
            project="argset",
            packages=[
                DistributionPackage(
                    filename="argset-0.1.0-py3-none-any.whl",
                    project="argset",
                    version="0.1.0",
                    package_type="wheel",
                    url="https://files.pythonhosted.org/packages/b5/2b/7aa284f345e37f955d86e4cd57b1039b573552b0fc29d1a522ec05c1ee41/argset-0.1.0-py3-none-any.whl",
                    requires_python="~=3.6",
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=None,
                    digests={
                        "sha256": "107a632c7112faceb9fd6e93658dd461154713db250f7ffde5bd473e17cf1db5"
                    },
                ),
                DistributionPackage(
                    filename="argset-0.1.0.tar.gz",
                    project="argset",
                    version="0.1.0",
                    package_type="sdist",
                    url="https://files.pythonhosted.org/packages/d0/ee/1c25e68d029e8daaf3228dababbf3261fa5d9569f6f705867b2ad4df9b6d/argset-0.1.0.tar.gz",
                    requires_python="~=3.6",
                    has_sig=None,
                    is_yanked=False,
                    yanked_reason=None,
                    metadata_digests=None,
                    has_metadata=None,
                    digests={
                        "sha256": "8a41ee4789d37517c259984c11f2aa3639a90dc8fa446ff905ecc5fe6623c12d"
                    },
                ),
            ],
            last_serial="10562871",
            repository_version="1.0",
        )
        (call,) = spy.call_args_list
        assert call[1]["timeout"] == 2.718
        with pytest.raises(NoSuchProjectError) as excinfo:
            simple.get_project_page("nonexistent")
        assert excinfo.value.project == "nonexistent"
        assert excinfo.value.url == "https://test.nil/simple/nonexistent/"
        assert str(excinfo.value) == (
            "No details about project 'nonexistent' available at"
            " https://test.nil/simple/nonexistent/"
        )


@responses.activate
def test_unsupported_content_type() -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/",
        json={
            "meta": {"_last-serial": 14267765, "api-version": "1.0"},
            "projects": [{"name": "argset"}, {"name": "banana"}, {"name": "coconut"}],
        },
    )
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/empty/",
        json={"files": [], "name": "empty", "meta": {"api-version": "1.0"}},
        content_type="application/json; charset=utf-8",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        with pytest.raises(UnsupportedContentTypeError) as excinfo:
            simple.get_index_page()
        assert excinfo.value.url == "https://test.nil/simple/"
        assert excinfo.value.content_type == "application/json"
        assert (
            str(excinfo.value)
            == "Response from https://test.nil/simple/ has unsupported Content-Type 'application/json'"
        )
        with pytest.raises(UnsupportedContentTypeError) as excinfo:
            simple.get_project_page("empty")
        assert excinfo.value.url == "https://test.nil/simple/empty/"
        assert excinfo.value.content_type == 'application/json; charset="utf-8"'
        assert (
            str(excinfo.value)
            == "Response from https://test.nil/simple/empty/ has unsupported Content-Type 'application/json; charset=\"utf-8\"'"
        )


@responses.activate
def test_download(tmp_path: Path) -> None:
    src_file = DATA_DIR / "click_loglevel-0.4.0.post1-py3-none-any.whl"
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=src_file.read_bytes(),
        content_type="application/zip",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests={
                "sha256": "f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c"
            },
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        simple.download_package(pkg, dest)
        assert dest.exists()
        assert filecmp.cmp(src_file, dest, shallow=False)


@responses.activate
def test_download_no_digests(tmp_path: Path) -> None:
    src_file = DATA_DIR / "click_loglevel-0.4.0.post1-py3-none-any.whl"
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=src_file.read_bytes(),
        content_type="application/zip",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests={},
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        with pytest.raises(NoDigestsError) as excinfo:
            simple.download_package(pkg, dest)
        assert str(excinfo.value) == "No digests with known algorithms available"
        assert not dest.exists()


@responses.activate
def test_download_bad_digests(tmp_path: Path) -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=b"\0\1\2\3\4\5",
        content_type="application/octet-stream",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests={
                "sha256": "f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c"
            },
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        with pytest.raises(DigestMismatchError) as excinfo:
            simple.download_package(pkg, dest)
        assert str(excinfo.value) == (
            "sha256 digest of downloaded file is"
            " '17e88db187afd62c16e5debf3e6527cd006bc012bc90b51a810cd80c2d511f43'"
            " instead of expected"
            " 'f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c'"
        )
        assert not dest.exists()


@responses.activate
def test_download_bad_digests_keep(tmp_path: Path) -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=b"\0\1\2\3\4\5",
        content_type="application/octet-stream",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests={
                "sha256": "f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c"
            },
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        with pytest.raises(DigestMismatchError) as excinfo:
            simple.download_package(pkg, dest, keep_on_error=True)
        assert str(excinfo.value) == (
            "sha256 digest of downloaded file is"
            " '17e88db187afd62c16e5debf3e6527cd006bc012bc90b51a810cd80c2d511f43'"
            " instead of expected"
            " 'f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c'"
        )
        assert dest.exists()
        assert dest.read_bytes() == b"\0\1\2\3\4\5"


@pytest.mark.parametrize(
    "digests",
    [
        {},
        {"sha256": "f3449b5d28d6cba5bfbeed371ad59950aba035730d5cc28a32b4e7632e17ed6c"},
    ],
)
@responses.activate
def test_download_bad_digests_no_verify(
    tmp_path: Path, digests: dict[str, str]
) -> None:
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=b"\0\1\2\3\4\5",
        content_type="application/octet-stream",
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests=digests,
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        simple.download_package(pkg, dest, verify=False)
        assert dest.exists()
        assert dest.read_bytes() == b"\0\1\2\3\4\5"


class SpyingProgressTracker:
    def __init__(self) -> None:
        self.content_length: Optional[int] = None
        self.enter_called = False
        self.exit_called = False
        self.updates: list[int] = []

    def __enter__(self) -> SpyingProgressTracker:
        self.enter_called = True
        return self

    def __exit__(
        self,
        _exc_type: Optional[type[BaseException]],
        _exc_val: Optional[BaseException],
        _exc_tb: Optional[TracebackType],
    ) -> None:
        self.exit_called = True

    def update(self, increment: int) -> None:
        self.updates.append(increment)


@responses.activate
def test_download_progress(tmp_path: Path) -> None:
    size = 1 << 20
    responses.add(
        method=responses.GET,
        url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
        body=b"\0" * size,
        content_type="application/octet-stream",
        auto_calculate_content_length=True,
    )
    with PyPISimple("https://test.nil/simple/") as simple:
        pkg = DistributionPackage(
            filename="click_loglevel-0.4.0.post1-py3-none-any.whl",
            project="click-loglevel",
            version="0.4.0.post1",
            package_type="wheel",
            url="https://test.nil/simple/packages/click_loglevel-0.4.0.post1-py3-none-any.whl",
            digests={
                "sha256": "30e14955ebf1352266dc2ff8067e68104607e750abb9d3b36582b8af909fcb58"
            },
            requires_python=None,
            has_sig=None,
            is_yanked=False,
            yanked_reason=None,
            metadata_digests=None,
            has_metadata=False,
        )
        dest = tmp_path / str(pkg.project) / pkg.filename
        spy = SpyingProgressTracker()

        def progress_cb(content_length: Optional[int]) -> ProgressTracker:
            spy.content_length = content_length
            return spy

        simple.download_package(pkg, dest, progress=progress_cb)
        assert spy.content_length == size
        assert spy.enter_called
        assert spy.exit_called
        assert spy.updates == [65535] * (size // 65535) + [size % 65535]
