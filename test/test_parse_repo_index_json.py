import pytest
from pypi_simple import (
    SUPPORTED_REPOSITORY_VERSION,
    IndexPage,
    UnsupportedRepoVersionError,
    parse_repo_index_json,
)


def test_empty() -> None:
    assert parse_repo_index_json(
        {"meta": {"api-version": "1.0"}, "projects": []}
    ) == IndexPage(
        projects=[],
        repository_version="1.0",
        last_serial=None,
    )


def test_parse_repo_index_json() -> None:
    assert parse_repo_index_json(
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


def test_parse_repo_index_json_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        parse_repo_index_json(
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
