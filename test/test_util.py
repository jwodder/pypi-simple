import pytest
from pypi_simple import UnexpectedRepoVersionWarning
from pypi_simple.util import check_repo_version


def test_check_repo_version_greater_minor() -> None:
    with pytest.warns(UnexpectedRepoVersionWarning) as record:
        check_repo_version("1.3", "1.2")
    assert len(record) == 1
    assert str(record[0].message) == (
        "Repository's version (1.3) has greater minor component than supported"
        " version (1.2)"
    )
