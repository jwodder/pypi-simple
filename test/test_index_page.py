from pathlib import Path
import pytest
from pypi_simple import (
    SUPPORTED_REPOSITORY_VERSION,
    IndexPage,
    UnsupportedRepoVersionError,
)

DATA_DIR = Path(__file__).with_name("data")


def test_from_html_empty() -> None:
    assert IndexPage.from_html("") == IndexPage(
        projects=[],
        repository_version=None,
        last_serial=None,
    )


@pytest.mark.parametrize(
    "filename,encoding,page",
    [
        (
            "simple01.html",
            "utf-8",
            IndexPage(
                projects=[
                    "a",
                    "a00k5pgrtn",
                    "a10ctl",
                    "a10-horizon",
                    "a10-neutronclient",
                    "a10-neutron-lbaas",
                    "a10-openstack-lbaas",
                    "a10-openstack-lib",
                    "a10sdk",
                    "a2d_diary",
                    "a2m.itertools",
                    "a2p2",
                    "a2pcej",
                    "a2svm",
                    "a2w",
                    "a2x",
                    "a318288f-60c1-4176-a6be-f8a526b27661",
                    "A3MIO",
                    "a3rt-sdk-py",
                    "a4t-party_contact",
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
        (
            "simple_base.html",
            "utf-8",
            IndexPage(
                projects=[
                    "a",
                    "a00k5pgrtn",
                    "a10ctl",
                    "a10-horizon",
                    "a10-neutronclient",
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
        (
            "simple_repo_version.html",
            "utf-8",
            IndexPage(
                projects=[
                    "a",
                    "a00k5pgrtn",
                    "a10ctl",
                    "a10-horizon",
                    "a10-neutronclient",
                ],
                repository_version="1.0",
                last_serial=None,
            ),
        ),
        (
            "simple_devpi.html",
            "utf-8",
            IndexPage(
                projects=[
                    "devpi",
                    "devpi-client",
                    "devpi-common",
                    "devpi-jenkins",
                    "devpi-ldap",
                    "devpi-lockdown",
                    "devpi-postgresql",
                    "devpi-server",
                    "devpi-web",
                    "ploy-ezjail",
                    "pytest",
                    "waitress",
                    "0",
                    "0-0",
                    "0-0-1",
                    "0-core-client",
                    "0-orchestrator",
                    "00smalinux",
                ],
                repository_version=None,
                last_serial=None,
            ),
        ),
    ],
)
def test_from_html(filename: str, encoding: str, page: IndexPage) -> None:
    html = (DATA_DIR / filename).read_bytes()
    assert IndexPage.from_html(html, encoding) == page


def test_from_html_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        IndexPage.from_html(
            """
            <!DOCTYPE html>
            <html>
              <head>
                <title>Simple index</title>
                <meta name="pypi:repository-version" content="42.0"/>
              </head>
              <body>
                <a href="a/">a</a>
                <a href="a00k5pgrtn/">a00k5pgrtn</a>
                <a href="a10ctl/">a10ctl</a>
                <a href="a10-horizon/">a10-horizon</a>
                <a href="a10-neutronclient/">a10-neutronclient</a>
                </body>
            </html>
        """
        )
    assert excinfo.value.declared_version == "42.0"
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        "Repository's version (42.0) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )


def test_from_json_data_empty() -> None:
    assert IndexPage.from_json_data(
        {"meta": {"api-version": "1.0"}, "projects": []}
    ) == IndexPage(
        projects=[],
        repository_version="1.0",
        last_serial=None,
    )


def test_from_json_data() -> None:
    assert IndexPage.from_json_data(
        {
            "meta": {"_last-serial": 14267765, "api-version": "1.0"},
            "projects": [{"name": "apple"}, {"name": "banana"}, {"name": "coconut"}],
        }
    ) == IndexPage(
        projects=[
            "apple",
            "banana",
            "coconut",
        ],
        repository_version="1.0",
        last_serial="14267765",
    )


def test_from_json_data_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        IndexPage.from_json_data(
            {
                "meta": {"api-version": "42.0"},
                "projects": [{"name": "xyzzy"}, {"name": "plover"}, {"name": "plugh"}],
            }
        )
    assert excinfo.value.declared_version == "42.0"
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        "Repository's version (42.0) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )
