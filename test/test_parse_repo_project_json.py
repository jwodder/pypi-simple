import json
from pathlib import Path
import pytest
from pypi_simple import (
    SUPPORTED_REPOSITORY_VERSION,
    DistributionPackage,
    ProjectPage,
    UnsupportedRepoVersionError,
    parse_repo_project_json,
)

DATA_DIR = Path(__file__).with_name("data")


def test_empty() -> None:
    assert parse_repo_project_json(
        {"files": [], "name": "-NIL-", "meta": {"api-version": "1.0"}}
    ) == ProjectPage(
        project="-NIL-",
        packages=[],
        repository_version="1.0",
        last_serial=None,
    )


@pytest.mark.parametrize(
    "filename,page",
    [
        (
            "argset.json",
            ProjectPage(
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
                        yanked=None,
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
                        yanked=None,
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "8a41ee4789d37517c259984c11f2aa3639a90dc8fa446ff905ecc5fe6623c12d"
                        },
                    ),
                ],
                repository_version="1.0",
                last_serial="10562871",
            ),
        ),
        (
            "yanked.json",
            ProjectPage(
                project="yanked",
                packages=[
                    DistributionPackage(
                        filename="yanked-0.0.0-py3-none-any.whl",
                        project="yanked",
                        version="0.0.0",
                        package_type="wheel",
                        url="https://files.pythonhosted.org/packages/9b/af/67c4c6b7f98f2789e4073a0b589f71ad865b3bb8d3e508c51d5f70962fb1/yanked-0.0.0-py3-none-any.whl",
                        requires_python="",
                        has_sig=None,
                        yanked="",
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "81aaff3b2a51d570771c32656909950387c7380d321b0305aaad1cd692645932"
                        },
                    ),
                    DistributionPackage(
                        filename="yanked-0.0.0.tar.gz",
                        project="yanked",
                        version="0.0.0",
                        package_type="sdist",
                        url="https://files.pythonhosted.org/packages/2c/9b/23d7985793a487f53fdfbc78e6180cb74b293d200da94895a8a932a4ccc6/yanked-0.0.0.tar.gz",
                        requires_python="",
                        has_sig=None,
                        yanked="not good",
                        metadata_digests=None,
                        has_metadata=None,
                        digests={
                            "sha256": "ca14bde2c9c14a5fe7ad9ab9078fdcd8fe09b6de4ca341cc9c286159a8acba41"
                        },
                    ),
                ],
                repository_version="1.0",
                last_serial=None,
            ),
        ),
    ],
)
def test_parse_repo_project_json(filename: str, page: ProjectPage) -> None:
    with (DATA_DIR / filename).open() as fp:
        data = json.load(fp)
    assert parse_repo_project_json(data) == page


def test_parse_repo_project_json_relative_urls() -> None:
    with (DATA_DIR / "argset-relative.json").open() as fp:
        data = json.load(fp)
    assert parse_repo_project_json(
        data, "https://test.nil/simple/argset/"
    ) == ProjectPage(
        project="argset",
        packages=[
            DistributionPackage(
                filename="argset-0.1.0-py3-none-any.whl",
                project="argset",
                version="0.1.0",
                package_type="wheel",
                url="https://test.nil/simple/argset/packages/argset-0.1.0-py3-none-any.whl",
                requires_python="~=3.6",
                has_sig=None,
                yanked=None,
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
                url="https://test.nil/simple/argset/packages/argset-0.1.0.tar.gz",
                requires_python="~=3.6",
                has_sig=None,
                yanked=None,
                metadata_digests=None,
                has_metadata=None,
                digests={
                    "sha256": "8a41ee4789d37517c259984c11f2aa3639a90dc8fa446ff905ecc5fe6623c12d"
                },
            ),
        ],
        repository_version="1.0",
        last_serial="10562871",
    )


def test_parse_repo_project_json_unsupported_version() -> None:
    with pytest.raises(UnsupportedRepoVersionError) as excinfo:
        parse_repo_project_json(
            {
                "files": [],
                "meta": {"api-version": "42.0"},
                "name": "futuristic",
            },
        )
    assert excinfo.value.declared_version == "42.0"
    assert excinfo.value.supported_version == SUPPORTED_REPOSITORY_VERSION
    assert str(excinfo.value) == (
        "Repository's version (42.0) has greater major component than"
        f" supported version ({SUPPORTED_REPOSITORY_VERSION})"
    )
